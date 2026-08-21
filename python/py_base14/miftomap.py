import ctypes
import maptype
import mapapi
import mapsyst
import vecexapi
import tkinter
from tkinter import filedialog

def LoadMif(hmap:maptype.HMAP, folder, filename, rscname) -> int:
    if hmap == 0:
        return 0
    if filename is None:
        return 0
    if rscname is None:
        return 0
    if folder is None:
        return 0
    return vecexapi.mifLoadSheetFromFolder(0,0, mapsyst.WTEXT(folder), mapsyst.WTEXT(filename), mapsyst.WTEXT(rscname), 0, 1)

def MifFolderToMap(hmap:maptype.HMAP,hobj:maptype.HOBJ) -> float: #caption:Импорт MIF/MID
    root = tkinter.Tk()
    root.withdraw() 
    folder = filedialog.askdirectory(parent=root)
    if len(folder) == 0:
        root.destroy()
        return 0
    filename = filedialog.asksaveasfilename(
        parent=root,
        filetypes=(("SITX files", "*.sitx"),
                   ("All files", "*.*")),
        title='Сохранить',
        defaultextension='.sitx',
        initialfile='boundary')    
    if len(filename) == 0:
        root.destroy()
        return 0
    rscname = filedialog.askopenfilename(
        parent=root,
        filetypes=(("RSC files", "*.rsc"),
                   ("All files", "*.*")),
        defaultextension='.rsc',
        initialfile='service')    
    root.destroy()
    if len(rscname) == 0:
        return 0
    ret = LoadMif(hmap, folder, filename, rscname)
    if ret != 0:
        mapapi.mapShowMessage(mapsyst.WTEXT('Загрузка завершена успешно'), mapsyst.WTEXT('Импорт MIF/MID'))
        return 1
    mapapi.mapShowMessage(mapsyst.WTEXT('Ошибка загрузки данных'), mapsyst.WTEXT('Импорт MIF/MID'))
    return 0
