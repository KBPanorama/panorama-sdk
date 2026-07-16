import ctypes

import mapsyst
import maptype
import mapapi
import rscapi
import seekapi
import logapi
import maperr
import mapselec

import tkinter
from tkinter import filedialog

title = "Вырезать фрагмент текста"

# Object processing
def CutObjSemantic(hobj:maptype.HOBJ, code:ctypes.c_int, startpos:ctypes.c_int, stoppos) -> int:
    if hobj == 0:
        return 0
    sembuf = mapsyst.WTEXT(1024)
    number = mapapi.mapSemanticCodeValueNameUn(hobj,code,sembuf,sembuf.size(),1)
    if (number == 0):
        return 0
    text = sembuf.string()
    newtext = text[:startpos-1] + text[stoppos:]
     
    mapapi.mapSetSemanticValueUn(hobj, number, mapsyst.WTEXT(newtext),0)
    mapapi.mapCommitObject(hobj)
    return 1

# Processing of selected objects
def CutSemantics(hmap:maptype.HMAP, hobj:maptype.HOBJ, code:ctypes.c_int, startpos:int, stoppos:int) -> int:
    if hobj != 0:
        return CutObjSemantic(hobj, code, startpos, stoppos)

    if seekapi.mapGetTotalSelectFlag(hmap) == 0:
        mapapi.mapErrorMessageUn(maperr.IDS_OBJECTSNOTSELECTED, title)
        return 0
    seekcount = seekapi.mapTotalSeekObjectCount(hmap)
    if seekcount == 0:
        mapapi.mapErrorMessageUn(maperr.IDS_OBJECTSNOTSELECTED, title)
        return 0
    hwork = mapapi.mapCreateObject(hmap, 1, maptype.IDDOUBLE2, 0)
    percent = int(0)
    objcount = 0
    hprogress = 0
    if seekcount > 1000:
        hprogress = mapapi.mapOpenProgressBar()
    logapi.mapLogCreateAction(hmap, hmap, logapi.TAC_MED_SEMUPDATE)
    flag = maptype.WO_FIRST
    while (seekapi.mapTotalSeekObject(hmap, hwork, flag) != 0):
        flag = maptype.WO_NEXT
        if CutObjSemantic(hwork, code, startpos, stoppos) != 0:
            objcount += 1
        newpercent = int(objcount * 100 / seekcount)
        if newpercent > percent:
            percent = newpercent
            if hprogress != 0:
                if mapapi.mapProgressBar(hprogress, int(percent), mapsyst.WTEXT('  Обработка семантики: ' + mapapi.IntToStr(objcount) + '/' + mapapi.IntToStr(seekcount))) == -1:
                    break
    if hwork != 0:
        mapapi.mapFreeObject(hwork)
    if hprogress != 0:
        mapapi.mapCloseProgressBar(hprogress)
    logapi.mapLogCommitActionEx(hmap, hmap, None)
    mestext = 'Обработано объектов: ' + str(objcount) 
    mapapi.mapMessageBoxUn(0, mapsyst.WTEXT(mestext), mapsyst.WTEXT(title), maptype.MB_OK)
    return objcount

# Remove piece of text in string semantics
def CutText(_hmap:maptype.HMAP, _hobj:maptype.HOBJ) -> float: #caption:Вырезать фрагмент текста
    if _hmap == 0:
        return 0

    if seekapi.mapIsTotalSeekObjectNotEmpty(_hmap) == 0:
        if _hobj == 0:
            mapapi.mapErrorMessageUn(maperr.IDS_OBJECTSNOTSELECTED, title)
            return 0
    else:
        _hobj = 0

    retvalue = 0
    seekcount = seekapi.mapTotalSeekObjectCount(_hmap)

    root = tkinter.Tk()
    root.title(title)
    
    src_label = tkinter.Label(text="Код семантики: ")
    start_label = tkinter.Label(text="Удалить с позиции: ")
    stop_label = tkinter.Label(text="До позиции: ")
    count_label = tkinter.Label(text="Выделено: " + str(seekcount))

    src_label.grid(row=0, column=0, sticky="w")
    start_label.grid(row=1, column=0, sticky="w")
    stop_label.grid(row=2, column=0, sticky="w")
    count_label.grid(row=2, column=2, sticky="w")

    src_value = tkinter.IntVar()
    start_value = tkinter.IntVar()
    stop_value = tkinter.IntVar()

    src_entry = tkinter.Entry(width=10, textvariable=src_value)
    start_entry = tkinter.Entry(width=10, textvariable=start_value)
    stop_entry = tkinter.Entry(width=10, textvariable=stop_value)

    src_entry.grid(row=0,column=1, padx=5, pady=5)
    start_entry.grid(row=1,column=1, padx=5, pady=5)
    stop_entry.grid(row=2,column=1, padx=5, pady=5)
    semname = mapsyst.WTEXT(64)
    hrsc = rscapi.mapGetRscIdent(_hmap, _hmap)
    rscapi.mapGetRscSemanticNameUn(hrsc, 9, semname, semname.size())
    select_src = tkinter.Button(text=semname.string())
    src_value.set(9)
    start_value.set(1)
    stop_value.set(3)

    def SelectSemanticSrc():
        parm = maptype.TASKPARMEX()
        parm.Handle = mapapi.mapGetHandleForMessage()
        semcode = mapselec.selSemanticSelectInit(hrsc, ctypes.byref(parm), src_value.get())
        if semcode != 0:
            src_value.set(semcode)
            rscapi.mapGetRscSemanticNameUn(hrsc, semcode, semname, semname.size())
            select_src.configure(text=semname.string())
    select_src.configure(command=SelectSemanticSrc)
    select_src.grid(row=0, column=2, padx=10, sticky="w")
    ret_value = tkinter.IntVar()
    ret_value.set(0)
    def Run():
        nonlocal retvalue
        code = src_value.get()        
        retvalue = CutSemantics(_hmap, _hobj, code, start_value.get(), stop_value.get())
        root.destroy()

    def Close():
        root.destroy()
    message_button = tkinter.Button(text="Выполнить", command=Run)
    message_button.grid(row=3,column=1, padx=5, pady=5, sticky="e")
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
    return retvalue
