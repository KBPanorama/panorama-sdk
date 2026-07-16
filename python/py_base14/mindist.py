#!/usr/bin/env python3

import ctypes

import mapsyst
import maptype
import mapapi
import seekapi
import graphapi
import sitapi

import threading
import time

import tkinter
import tkinter.ttk
from   tkinter.filedialog import asksaveasfilename


# ---------------------------------------------------------------
# GraphPathfinder
# класс вычисления минимальных расстояний в графе дорог
# ---------------------------------------------------------------

class GraphPathfinder:
    baseMap      = 0
    sitGraph     = 0
    outFileName  = ''
    centersA     = []
    centersB     = []
    infoA        = []
    infoB        = []
    connections  = []
    numThreads   = 8
    threads      = []
    threadActive = []
    mutex        = 0
    totalData    = 0
    processed    = 0
    isCancel     = 0
    
    def __init__(self, basemap: maptype.HMAP, sitA:maptype.HSITE, semA:str, sitB:maptype.HSITE,semB:str, sitGraph:maptype.HSITE):
        self.baseMap = basemap
        self.centersA,self.infoA = self.CollectData(sitA,semA)
        self.centersB,self.infoB = self.CollectData(sitB,semB)
        self.sitGraph = sitGraph

        numCentFrom = len(self.centersA)
        numCentTo   = len(self.centersB)

        self.totalData = numCentFrom * numCentTo
        if self.totalData == 0:
            return

        self.mutex = threading.Lock()

        progBar = mapapi.mapOpenProgressBar()

        isCancel  = 0
        processed = 0
        percent = 0
        percentPrev = 0
        for i in range(0,numCentFrom):
            for j in range(0,numCentTo):
                self.connections.append([i,j])
                processed += 1
                percentPrev = percent
                percent = int(100*processed/self.totalData)
                if percent != percentPrev:
                    isCancel = mapapi.mapProgressBar(progBar,percent,mapsyst.WTEXT('Подготовка списков'))
                    if isCancel == -1:
                        break
            if isCancel == -1:
                break
        mapapi.mapCloseProgressBar(progBar)

    def SemanticValueByName(self, hObj:maptype.HOBJ, name:str):
        _name = mapsyst.WTEXT(128)
        c = mapapi.mapSemanticAmount(hObj)
        for i in range(0,c):
            mapapi.mapSemanticFullName(hObj, i+1, _name,_name.size())
            if name == _name.string():
                _value = mapsyst.WTEXT(128)
                mapapi.mapSemanticValuePro(hObj,i+1,_value,_value.size(),0)
                return _value.string()
        return '<empty>'
    
    def WriteToFile(self, outstr):
        self.mutex.acquire()
        f = open(self.outFileName,'a')
        f.write(outstr)
        f.close()
        self.mutex.release()
    
    def CollectData(self, hsite:maptype.HSITE, _semname:str):
        centers    = []
        seminfo    = []
        c = sitapi.mapGetSiteObjectCount(self.baseMap,hsite)
        hObj = sitapi.mapCreateSiteObject(self.baseMap,hsite, maptype.IDDOUBLE2, 0)
        for i in range(0,c):
            isDeleted = seekapi.mapReadObjectByNumberEx(self.baseMap,hsite,hObj,1,i+1)
            if isDeleted == 2:
                x = ctypes.c_double(0)
                y = ctypes.c_double(0)
                if mapapi.mapGetObjectCenterEx(self.baseMap,hObj,ctypes.byref(x),ctypes.byref(y),1):
                    centers.append(maptype.DOUBLEPOINT(x,y))
                seminfo.append(self.SemanticValueByName(hObj,_semname))
        mapapi.mapFreeObject(hObj)
        return centers, seminfo
        
    def CalcThread(self, index, c_from, c_to):
        self.threadActive[index] = 1
        try:
            opennetparm = graphapi.OPENNETPARM()
            netGraph = graphapi.onOpenNetEx(self.baseMap,self.sitGraph,ctypes.byref(opennetparm))

            pathparam = graphapi.PATHPARM()
            th_processed = 0
            outstr = ''
            for i in range(c_from,c_to):
                pathparam.Point1 = self.centersA[self.connections[i][0]]
                pathparam.Point2 = self.centersB[self.connections[i][1]]
                path = graphapi.onCreatePath(netGraph, ctypes.byref(pathparam))
                if path:
                    length = graphapi.onGetPathLength(path)
                    outstr += self.infoA[self.connections[i][0]]+','+self.infoB[self.connections[i][1]]+','+str(length)+'\n'
                    graphapi.onFreePath(path)
                else:
                    outstr += self.infoA[self.connections[i][0]]+','+self.infoB[self.connections[i][1]]+',-1.0\n'
                
                th_processed += 1
                self.mutex.acquire()
                self.processed += 1
                self.mutex.release()
                
                if th_processed % 50 == 0: # запись каждые n обработок
                    self.WriteToFile(outstr)
                    outstr = ''
                    if self.isCancel == -1:
                        break
            
            if len(outstr): # записать остатки
                self.WriteToFile(outstr)
            
            graphapi.onCloseNet(netGraph)
        except Exception as e:
            self.threadActive[index] = 0
            return
        finally:
            self.threadActive[index] = 0
            return

    def CalcMinDistances(self, outFilename:str, numTh:int):
        self.outFileName = outFilename
        f = open(self.outFileName,'w')
        f.close()

        self.processed = 0
        self.threads.clear()
        self.threadActive.clear()
        self.numThreads = numTh
        step = int(self.totalData/self.numThreads)+1
        for i in range(0,self.numThreads):
            c_from = i*step
            c_to   = i*step+step
            if c_to > self.totalData:
                c_to = self.totalData
            th = threading.Thread(target=self.CalcThread, args=(i,c_from,c_to))
            self.threads.append(th)
            self.threadActive.append(0)
            
        for i in range(0,self.numThreads):
            self.threads[i].start()

        progBar = mapapi.mapOpenProgressBar()
        percentPrev = 0
        percent = 0
        while 1:
            percent = int(100*self.processed/self.totalData)
            if percent != percentPrev:
                self.isCancel = mapapi.mapProgressBar(progBar,percent,mapsyst.WTEXT('Построение маршрутов'))
                if self.isCancel == -1:
                    break
            act = 0
            for i in range(0,self.numThreads):
                act += self.threadActive[i]
            if act == 0:
                break
            time.sleep(0.2)    # 0.2 sec
        mapapi.mapCloseProgressBar(progBar)

        return self.processed

# ---------------------------------------------------------------
# ---------------------------------------------------------------



# ---------------------------------------------------------------
# ---------------------------------------------------------------
def CalcMinDistances(hmap:maptype.HMAP, hobj:maptype.HOBJ) -> float:  #caption:Расчёт минимальных расстояний по графу дорог
    mapNames   = [] # список имён карт в составе документа
    hSites     = [] # список хэндлов карт по именам выше

    mainWindow = 0 # главное окно скрипта
    grA_name   = 0 # выбраное имя карты A
    grB_name   = 0 # выбраное имя карты B
    semA_combo = 0 # комбобокс семантик A
    semB_combo = 0 # комбобокс семантик B
    semNameA   = 0 # выбраное имя семантики A
    semNameB   = 0 # выбраное имя семантики B
    sitA       = 0 # хэндл карты A
    sitB       = 0 # хэндл карты B
    sitGraph   = 0 # хэндл графа дорог

    processed = 0

    # Сформировать список видов семантик (атрибутов) по первым 100 объектам карты
    def CollectSemNames(hMap: maptype.HMAP, hSite: maptype.HSITE):
        semNames = []
        hObj = sitapi.mapCreateSiteObject(hMap,hSite, maptype.IDDOUBLE2, 0)
        c = sitapi.mapGetSiteObjectCount(hMap,hSite)
        if c > 100: c = 100
        for i in range(0,c):
            if seekapi.mapReadObjectByNumberEx(hMap,hSite,hObj,1,i+1) == 2:
                s = mapapi.mapSemanticAmount(hObj)
                for j in range(0,s):
                    _name = mapsyst.WTEXT(128)
                    mapapi.mapSemanticFullName(hObj, j+1, _name,_name.size())
                    namestr = _name.string()
                    if namestr not in semNames:
                        semNames.append(namestr)
        mapapi.mapFreeObject(hObj)
        return semNames

    # Получить список всех карт в составе документа и найти граф
    def CollectMaps(hMap: maptype.HMAP):
        mapNames = []
        hSites   = []
        sitcount = sitapi.mapGetSiteCount(hMap)
        graph = 0
        for i in range(0,sitcount+1):
            hsite = sitapi.mapGetSiteIdent(hMap, i)
            if sitapi.mapIsSiteGraph(hMap, hsite) != 0:
                graph=hsite
            else:
                shortname = mapsyst.WTEXT(128)
                sitapi.mapGetSiteSheetNameUn(hMap,hsite,1,shortname,shortname.size())
                mapNames.append(shortname.string())
                hSites.append(hsite)
        return mapNames,hSites,graph

    def SetVars():
        nonlocal processed, semNameA, semNameB
        if sitA == 0 and sitB == 0:
            mapapi.mapMessageBoxUn(0, mapsyst.WTEXT('Не выбраны карты объектов'), mapsyst.WTEXT('Подсчет длин маршрутов'), maptype.MB_WARNING)
            return
        else:
            if sitA == 0:
                mapapi.mapMessageBoxUn(0, mapsyst.WTEXT('Не выбрана карта объектов группы A'), mapsyst.WTEXT('Подсчет длин маршрутов'), maptype.MB_WARNING)
                return
            elif sitB == 0:
                mapapi.mapMessageBoxUn(0, mapsyst.WTEXT('Не выбрана карта объектов группы B'), mapsyst.WTEXT('Подсчет длин маршрутов'), maptype.MB_WARNING)
                return

        semFrom = semNameA.get()
        semTo   = semNameB.get()

        if len(semFrom) == 0 and len(semTo) == 0:
            mapapi.mapMessageBoxUn(0, mapsyst.WTEXT('Не выбраны сохраняемые семантики объектов'), mapsyst.WTEXT('Подсчет длин маршрутов'), maptype.MB_WARNING)
            return
        else:
            if len(semFrom) == 0:
                mapapi.mapMessageBoxUn(0, mapsyst.WTEXT('Не выбрана семантика объектов группы A'), mapsyst.WTEXT('Подсчет длин маршрутов'), maptype.MB_WARNING)
                return
            elif len(semTo) == 0:
                mapapi.mapMessageBoxUn(0, mapsyst.WTEXT('Не выбрана семантика объектов группы B'), mapsyst.WTEXT('Подсчет длин маршрутов'), maptype.MB_WARNING)
                return

        files = [('CSV', '*.csv')]
        outputFileName = asksaveasfilename(filetypes = files, defaultextension = files)

        if len(outputFileName) == 0:
            mapapi.mapMessageBoxUn(0, mapsyst.WTEXT('Не выбран файл для сохранения данных'), mapsyst.WTEXT('Подсчет длин маршрутов'), maptype.MB_WARNING)
            return

        graphPathfinder = GraphPathfinder(hmap,sitA,semFrom,sitB,semTo,sitGraph)
        processed = graphPathfinder.CalcMinDistances(outputFileName,16)
        mainWindow.destroy()

    def GroupAChange(*args):
        nonlocal sitA
        sitA = 0
        for i in range(0,len(mapNames)):
            if grA_name.get() == mapNames[i]:
                sitA = hSites[i]
                semA_combo.configure(values = CollectSemNames(hmap,sitA))
                break

    def GroupBChange(*args):
        nonlocal sitB
        sitB = 0
        for i in range(0,len(mapNames)):
            if grB_name.get() == mapNames[i]:
                sitB = hSites[i]
                semB_combo.configure(values = CollectSemNames(hmap,sitB))

    mainWindow = tkinter.Tk()
    mainWindow.title("Выбор карт")

    mapNames,hSites,sitGraph = CollectMaps(hmap)

    if sitGraph == 0:
        mainWindow.geometry('256x96')
        label1   = tkinter.Label(mainWindow,text="Отсутствует граф дорог")
        label1.pack(fill='both')
    else:
        grA_label   = tkinter.Label(mainWindow,text="Карта A: ")
        grB_label   = tkinter.Label(mainWindow,text="Карта B: ")
        grA_label.grid  (row=0, column=0, sticky="w",padx=5)
        grB_label.grid  (row=1, column=0, sticky="w",padx=5)

        grA_name  = tkinter.StringVar()
        grB_name  = tkinter.StringVar()
        grA_name.trace('w',GroupAChange)
        grB_name.trace('w',GroupBChange)
        grA_combo = tkinter.ttk.Combobox(mainWindow, textvariable=grA_name, values=mapNames,width=40,height = 100)
        grB_combo = tkinter.ttk.Combobox(mainWindow, textvariable=grB_name, values=mapNames,width=40,height = 100)
        grA_combo.grid(column=1, row=0,padx=5)
        grB_combo.grid(column=1, row=1,padx=5)

        semA_label   = tkinter.Label(mainWindow,text="Семантика A (ID): ")
        semB_label   = tkinter.Label(mainWindow,text="Семантика B (ID): ")
        semA_label.grid  (row=2, column=0, sticky="w",padx=5)
        semB_label.grid  (row=3, column=0, sticky="w",padx=5)
        semNameA = tkinter.StringVar()
        semNameB   = tkinter.StringVar()
        semA_combo = tkinter.ttk.Combobox(mainWindow, textvariable=semNameA, values=[],width=40,height = 100)
        semB_combo = tkinter.ttk.Combobox(mainWindow, textvariable=semNameB, values=[],width=40,height = 100)
        semA_combo.grid(column=1, row=2,padx=5)
        semB_combo.grid(column=1, row=3,padx=5)

        ok_button = tkinter.Button(mainWindow,text="Выполнить", command=SetVars)
        ok_button.grid(row=4, column=1, padx=5, pady=5, sticky="WE")

    mainWindow.eval('tk::PlaceWindow . center')
    mainWindow.resizable(False, False)
    mainWindow.mainloop()

    mapapi.mapShowMessage(mapsyst.WTEXT("Обработано маршрутов: "+str(processed)),mapsyst.WTEXT('Подсчет длин маршрутов'))

    return int(processed)