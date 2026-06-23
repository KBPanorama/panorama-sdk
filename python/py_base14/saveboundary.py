import ctypes
import maptype
import mapapi
import mapgdi
import mapsyst
import seekapi
import rscapi
import sitapi

import tkinter
from tkinter import filedialog

def CreateBoundaryList(hmap:maptype.HMAP, hsite:maptype.HSITE, filename) -> float:
    if hmap == 0:
        return 0
    if len(filename) == 0:
        return 0

    tfile = open(filename, 'w');
    if tfile is None:
        return 0
    mapname = mapsyst.WTEXT(1024)                                         # Строка для размещения номенклатуры
    sitapi.mapGetSiteSheetNameUn(hmap, hsite, 1, mapname, mapname.size()) # Запросить номенклатуру
    maxdistance = 10.0
    info1 = sitapi.mapCreateSiteObject(hmap, hsite)                       # Создать пустые объекты 
    info2 = sitapi.mapCreateSiteObject(hmap, hsite)
    typecode = 1018

    objcount = sitapi.mapGetSiteObjectCount(hmap, hsite) + 1              # Количество объектов на карте
    sembuf = mapsyst.WTEXT(1024)                                          # Строка для размещения считанной семантики   
    count = 0
    mescaption = 'Поиск приграничных участков'
    for i in range(1, objcount):                                          # Цикл по объектам карты 
        ret = seekapi.mapReadObjectByNumberEx(hmap, hsite, info1, 1, i)     # Считать очередной объект карты по порядковому номеру
        if ret != 2:
            continue
        number = mapapi.mapSemanticCodeValueNameUn(info1, typecode, sembuf, sembuf.size(), 1)     # Определить, есть ли интересующая нас семантика 
        if number == 0:
           continue
        type = mapapi.mapSemanticLongIntValue(info1, number)              # Считать значение интересующей нас семантики
        if type != 2:                                                     # Определить, есть ли интересующее нас значение семантики  
           continue
        edit = 0
        for j in range(1, objcount):                                      # Цикл по объектам карты 
            ret = seekapi.mapReadObjectByNumberEx(hmap, hsite, info2, 1, j) # Считать очередной объект карты по порядковому номеру
            if ret != 2:
                continue
            number = mapapi.mapSemanticCodeValueNameUn(info2, typecode, sembuf, sembuf.size(), 1) # Определить, есть ли интересующая нас семантика 
            if number == 0:
                continue
            type = mapapi.mapSemanticLongIntValue(info2, number)          # Считать значение интересующей нас семантики    
            if type == 2:                                                 # Определить, отличается ли значение семантики от эталонного объектам  
                continue
            dist = mapapi.mapDistanceObject(info1, info2)                 # Определить расстояние между объектами 
            if dist > maxdistance:
                continue
            edit = 1                                                      # Пометить объект для последующего сохранения
            break

        if edit == 1:                                         
            count += 1                                    
            key = mapapi.mapObjectKey(info1)                              # Запросить уникальный номер объектам 
            nomen = str(mapname.string()) 
            tfile.write(nomen + ';' + str(key)+ str('\n'))                # Записать строку в файл

    tfile.close()    
    if info1 != 0:                                                        # Почистить созданные объекты
        mapapi.mapFreeObject(info1)
    if info2 != 0:
        mapapi.mapFreeObject(info2)
    
    mapapi.mapShowMessage(mapsyst.WTEXT('Найдено объектов: ' + mapapi.IntToStr(count)), mapsyst.WTEXT(mescaption))

    return count

def SaveBoundaryList(hmap:maptype.HMAP,hobj:maptype.HOBJ) -> float: #caption:Список приграничных участков в файл
    
    if (hmap == 0):
        return 0
    
    currentmapnumber = 0
    if (mapapi.mapGetListCount(hmap) == 0):
        currentmapnumber = 1
    hsite = sitapi.mapGetSiteIdent(hmap, currentmapnumber)
    if (hsite == 0):
        return 0

    rscname = mapsyst.WTEXT(256)
    hrsc = rscapi.mapGetRscIdent(hmap, hsite)
    rscapi.mapGetRscNameUn(hrsc, rscname, rscname.size())
    text = rscname.string()
    if (text.find('survey.v6') == -1):
        mapapi.mapShowMessage(mapsyst.WTEXT('Необходимо открыть карту с классификатором survey.v6'), mapsyst.WTEXT('Поиск приграничных участков'))
        return 0
    
    root = tkinter.Tk()
    root.withdraw () # Погасить дополнительное окно в углу    
    filename = filedialog.asksaveasfilename(
        filetypes=(("TXT files", "*.txt"),
                   ("All files", "*.*")),
        title='Сохранить список',
        defaultextension='.txt',
        initialfile='boundary')    
    root.destroy()
    return CreateBoundaryList(hmap, hsite, filename)
