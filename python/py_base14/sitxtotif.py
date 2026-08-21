import os
import ctypes
import maptype
import mapapi
import mapsyst
import mappicex
import tkinter
from tkinter import filedialog

def SaveSitxtoTif(filename, element) -> int:
    if filename is None:
        return 0
    
    empty_pass = mapsyst.WTEXT("") 
    err = ctypes.c_int(0)
    hmap = mapapi.mapOpenAnyDataPro(mapsyst.WTEXT(filename), 0, ctypes.byref(err), empty_pass, 0)
    if hmap == 0:
        return 0

    tifname = filename + ".tif"

    frame = maptype.DFRAME(0,0,0,0)
    mapapi.mapGetTotalBorder(hmap,ctypes.byref(frame),maptype.PP_PLANE);

    ret = 0
    if mappicex.LoadDocumentImageToTiffFile(hmap, 0, mapsyst.WTEXT(tifname), frame, 24, element, 1, 0):
        ret = mapapi.mapShowMessage(mapsyst.WTEXT(tifname), mapsyst.WTEXT('Сохранен в TIF'))
    else:
        ret = mapapi.mapShowErrorMessage(mapsyst.WTEXT(tifname), mapsyst.WTEXT('Ошибка при сохранении в TIF'))
    mapapi.mapCloseData(hmap)
    return ret

def SitxToTif(hmap:maptype.HMAP,hobj:maptype.HOBJ) -> float: #caption:Карты из папки в TIF
    root = tkinter.Tk()
    root.withdraw() 
    folder = filedialog.askdirectory(parent=root)
    if len(folder) == 0:
        root.destroy()
        return 0
    root.destroy()
    count = 0;
    findext=".sitx"
    element = 4.0
    for file in os.listdir(folder):
       if file.endswith(findext):
           if SaveSitxtoTif(os.path.join(folder, file), element):
               count+=1
    if (count == 0):
        mapapi.mapShowErrorMessage(mapsyst.WTEXT('Карты из папки в TIF'), mapsyst.WTEXT('В папке не найдены карты .SITX'))
    return count
