import ctypes

import maptype
import mapapi
import mapgdi
import mapsyst
import maperr

import tkinter
from tkinter import filedialog

def CreateGridLines(hmap:maptype.HMAP,mmstep:ctypes.c_int) -> ctypes.c_int: 
    if hmap == 0:
        mapapi.mapErrorMessageUn(maperr.IDS_PARM, __name__)
        return 0    
    # Вычисление габаритов карты   
    frame = maptype.DFRAME(0,0,0,0)
    mapapi.mapGetTotalBorder(hmap,ctypes.byref(frame),maptype.PP_PLANE);
    x1 = frame.X1
    y1 = frame.Y1
    x2 = frame.X2
    y2 = frame.Y2	
    hwork = mapapi.mapCreateObject(hmap, 1, maptype.IDDOUBLE2, 0)
    imgl = mapgdi.IMGLINE(0,0)  
    imgl.Thick = 100
    imgl.Color = 0 
    mapapi.mapRegisterDrawObject(hwork,0,0)   
    mapapi.mapAppendDraw(hwork,mapgdi.IMG_LINE,ctypes.cast(ctypes.byref(imgl), ctypes.c_char_p))
    mapapi.mapAppendPointPlane(hwork,x1,y1,0)
    mapapi.mapAppendPointPlane(hwork,x2,y1,0)		   
    mapapi.mapAppendPointPlane(hwork,x2,y2,0)		   				   
    mapapi.mapAppendPointPlane(hwork,x1,y2,0)
    mapapi.mapAppendPointPlane(hwork,x1,y1,0)	
	# Нанесение сетки 
    x0 = x1 - 10.0 * mapapi.mapGetMapScale(hmap) / 1000.0
    step = mmstep * mapapi.mapGetMapScale(hmap) / 1000.0				   
    steps = x0//step
    x0 = steps * step
    y0 = y1 - 10.0 * mapapi.mapGetMapScale(hmap) / 1000.0
    steps = y0//step
    y0 = steps * step
    yr = y2 + 10.0 * mapapi.mapGetMapScale(hmap) / 1000.0
    xt = x2 + 10.0 * mapapi.mapGetMapScale(hmap) / 1000.0
    subj = 0
    x = x0
    totalcount = int((x2 - x1) / step + (y2 - y1) / step)
    hprogress = 0
    if totalcount > 100:
        hprogress = mapapi.mapOpenProgressBar()
    objindex = 0
    percent = int(0)
    while (x < x2):
        if (x < x1):
            x = x + step	
            continue
        mapapi.mapCreateSubject(hwork)    
        subj = subj + 1
        mapapi.mapAppendPointPlane(hwork, x, y0, subj)
        mapapi.mapAppendPointPlane(hwork, x, yr, subj)
        x = x + step	
    y = y0
    while (y < y2):
        if (y < y1):
             y = y + step	
             continue
        objindex = objindex + 1   
        newpercent = int(objindex * 100 / totalcount)
        if newpercent > percent:
            percent = newpercent
            ret = mapapi.mapProgressBar(hprogress, percent, mapsyst.WTEXT('Построение сетки: '))
            if ret == -1:
                break
        mapapi.mapCreateSubject(hwork)    
        subj = subj + 1
        mapapi.mapAppendPointPlane(hwork, x0, y, subj)
        mapapi.mapAppendPointPlane(hwork, xt, y, subj)
        y = y + step		  
    mapapi.mapCommitObjectAsNew(hwork)
    if hprogress != 0:
        mapapi.mapCloseProgressBar(hprogress)

    linecount = mapapi.mapPolyCount(hwork) 
    if hwork != 0:
        mapapi.mapFreeObject(hwork)
    mapapi.mapShowMessage(mapsyst.WTEXT('Сформировано линий - ' + mapapi.IntToStr(linecount)), mapsyst.WTEXT('Построение сетки'))
    return linecount



#################################################################
# Построить прямоугольную сетку с заданным шагом
#################################################################

def BuildGrid(hmap:maptype.HMAP,hobj:maptype.HOBJ) -> float: #caption:Построение прямоугольной сетки
    if hmap == 0:
        mapapi.mapErrorMessageUn(maperr.IDS_PARM, __name__)
        return 0   
    root = tkinter.Tk()
    root.title("Построение сетки")
    retcode = 0
    src_label = tkinter.Label(root, text="Шаг сетки, мм.: ")
    src_label.grid(row=0, column=0, sticky="w")
    ret_value = tkinter.IntVar(master=root)
    src_value = tkinter.IntVar(master=root)
    src_value.set(20)    
    src_entry = tkinter.Entry(root, width=10, textvariable=src_value)
    src_entry.grid(row=0,column=1, padx=5, pady=5)
    
    def Run():
        nonlocal retcode
        step = src_value.get()        
        retcode = CreateGridLines(hmap,step)
        root.destroy()

    def Close():
        root.destroy()

    message_button = tkinter.Button(root, text="Выполнить", command=Run)
    message_button.grid(row=0,column=3, padx=5, pady=5, sticky="e")
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
    mapapi.mapInvalidate();
    return retcode
