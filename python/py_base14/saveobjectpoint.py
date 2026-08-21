import ctypes

import maptype
import mapapi
import maperr

import tkinter
from tkinter import filedialog

# Save object points to file
def SaveObjectPointsToFile(hobj:maptype.HOBJ, filename) -> int:
    if hobj == 0:
        return 0
    if len(filename) == 0:
        return 0

    tfile = open(filename, 'w');
    if tfile is None:
        return 0

    polycount = mapapi.mapPolyCount(hobj)
    message = 'polycount = ' + str(polycount) + '\0'
    for i in range(0, polycount):
        pointcount = mapapi.mapPointCount(hobj, i)
        tfile.write(str(pointcount)+ str('\n'))
        for j in range(1, pointcount + 1):
            point = maptype.DOUBLEPOINT(0, 0)
            mapapi.mapGetPlanePoint(hobj, ctypes.byref(point), j, i)
            text = str(round(point.X, 2)) + str(' ') + str(round(point.Y, 2)) + str('\n')
            tfile.write(text)

    tfile.close();
    return 1

# Choose file name and save object points
def SaveObjectPoints(hmap:maptype.HMAP,hobj:maptype.HOBJ) -> float: #caption:Сохранить координаты объекта в см в текстовый файл
    if hobj == 0:
        mapapi.mapErrorMessageUn(maperr.IDS_OBJECTNOTSETTED, __name__)
        return 0
    ftypes=[('TXT files', '*.txt'), ('All files', '*.*')]
    initname = str('object_') + str(mapapi.mapObjectKey(hobj)) + str('.txt')
    root = tkinter.Tk()
    root.withdraw() # hide tkinter window
    filename = filedialog.asksaveasfilename(parent=root, filetypes=ftypes, title='Select file for points',defaultextension='.txt',initialfile=initname)
    root.destroy()
    return SaveObjectPointsToFile(hobj, filename)
