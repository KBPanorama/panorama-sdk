import ctypes

import mapsyst
import maptype
import mapapi
import rscapi
import seekapi
import logapi
import maperr
import mapselec
import doforeach

import tkinter
from tkinter import filedialog

class ALTTOFEET(ctypes.Structure):
    _fields_ = [("srccode", ctypes.c_int),
                ("outcode", ctypes.c_int),
                ("multi", ctypes.c_double)]
    def __init__(self, _srccode: int, _outcode: int, _multi: float):
        self.srccode = _srccode
        self.outcode = _outcode
        self.multi = _multi

# Convert object altitude to feet or meters
def ObjectAltitudeToFeet(_hmap:maptype.HMAP, _hobj:maptype.HOBJ, _parm:ALTTOFEET) -> int:
    if _hobj == 0:
       return 0
    srcnumber = mapapi.mapSemanticCodeValuePro(_hobj, _parm.srccode, None, 0, 1, 0)
    if srcnumber == 0:
       return 0
    value = mapapi.mapSemanticDoubleValue(_hobj, srcnumber)
    value = value * _parm.multi
    if _parm.srccode == _parm.outcode:
       ret = mapapi.mapSetSemanticDoubleValue(_hobj, srcnumber, value)
    else:
       outnumber = mapapi.mapSemanticCodeValuePro(_hobj, _parm.outcode, None, 0, 1, 0)
       if outnumber > 0:
          ret = mapapi.mapSetSemanticDoubleValue(_hobj, outnumber, value)
       else:
          ret = mapapi.mapAppendSemanticDouble(_hobj, _parm.outcode, value)
    if ret != 0:
        return mapapi.mapCommitObject(_hobj)
    return 0

# Convert altitude to feet or meters
def SemanticAltitudeToFeet(_hmap:maptype.HMAP, _hobj:maptype.HOBJ, srccode:int, outcode:int, multi:float) -> int:
    if _hmap == 0:
        return 0

    parm = ALTTOFEET(srccode, outcode, multi)

    dofunction = doforeach.DoForEach('Пересчет высоты:', logapi.TAC_MED_SEMUPDATE)
    result = dofunction.run(ObjectAltitudeToFeet, _hmap, _hobj, parm)

    mapapi.mapShowMessage(mapsyst.WTEXT('Обработано объектов: ' + mapapi.IntToStr(result)), mapsyst.WTEXT('Пересчет высоты'))
    mapapi.mapInvalidate()
    return result

# Convert semantic altitude to feet or meters for selected objects
def ConvertSemanticAltitude(_hmap:maptype.HMAP, _hobj:maptype.HOBJ) -> float: #caption:Пересчитать высоту в семантике в футы или метры
    if _hmap == 0:
        return 0

    if seekapi.mapIsTotalSeekObjectNotEmpty(_hmap) == 0:
        if _hobj == 0:
            mapapi.mapErrorMessageUn(maperr.IDS_OBJECTSNOTSELECTED, __name__)
            return 0
    else:
        _hobj = 0

    root = tkinter.Tk()
    root.title("Пересчитать высоту в семантике")
 
    src_label = tkinter.Label(root, text="Входная семантика: ")
    out_label = tkinter.Label(root, text="Выходная семантика: ")
    src_label.grid(row=0, column=0, sticky="w")
    out_label.grid(row=1, column=0, sticky="w")

    src_value = tkinter.IntVar(master=root)
    out_value = tkinter.IntVar(master=root)

    src_entry = tkinter.Entry(root, width=10, textvariable=src_value)
    out_entry = tkinter.Entry(root, width=10, textvariable=out_value)
    src_entry.grid(row=0,column=1, padx=5, pady=5)
    out_entry.grid(row=1,column=1, padx=5, pady=5)

    semname = mapsyst.WTEXT(64)
    hrsc = rscapi.mapGetRscIdent(_hmap, _hmap)
    rscapi.mapGetRscSemanticNameUn(hrsc, 4, semname, semname.size())
    select_src = tkinter.Button(root, text=semname.string())
    select_out = tkinter.Button(root, text=semname.string())
    src_value.set(4)
    out_value.set(4)

    def SelectSemanticSrc():
        parm = maptype.TASKPARMEX()
        parm.Handle = mapapi.mapGetHandleForMessage()
        semcode = mapselec.selSemanticSelectInit(hrsc, ctypes.byref(parm), src_value.get())
        if semcode != 0:
            src_value.set(semcode)
            rscapi.mapGetRscSemanticNameUn(hrsc, semcode, semname, semname.size())
            select_src.configure(text=semname.string())

    def SelectSemanticOut():
        parm = maptype.TASKPARMEX()
        parm.Handle = mapapi.mapGetHandleForMessage()
        semcode = mapselec.selSemanticSelectInit(hrsc, ctypes.byref(parm), src_value.get())
        if semcode != 0:
            out_value.set(semcode)
            rscapi.mapGetRscSemanticNameUn(hrsc, semcode, semname, semname.size())
            select_out.configure(text=semname.string())

    select_src.configure(command=SelectSemanticSrc)
    select_src.grid(row=0, column=2, padx=10, sticky="w")
    select_out.configure(command=SelectSemanticOut)
    select_out.grid(row=1, column=2, padx=10, pady=2, sticky="w")

    type_value = tkinter.IntVar(master=root)
    type_value.set(1)
    met2feet = tkinter.Radiobutton(root, text="в футы", variable=type_value, value=1).grid(row=2, column=1, sticky="w")
    feet2met = tkinter.Radiobutton(root, text="в метры", variable=type_value, value=2).grid(row=2, column=2, sticky="w")

    ret_value = tkinter.IntVar(master=root)
    ret_value.set(0)
    multi_f = 1. / 0.3048
    multi_m = 0.3048

    def Run():
        type = type_value.get()
        if type == 2:
           multi = multi_m
        else:
           multi = multi_f

        ret = SemanticAltitudeToFeet(_hmap, _hobj, src_value.get(), out_value.get(), multi)
        ret_value.set(ret)
        root.destroy()

    def Close():
        root.destroy()

    message_button = tkinter.Button(root, text="Выполнить", command=Run)
    message_button.grid(row=3,column=1, padx=5, pady=5, sticky="e")
    message_button = tkinter.Button(root, text="Отменить", command=Close)
    message_button.grid(row=3,column=2, padx=5, pady=5, sticky="w")

    root.eval('tk::PlaceWindow . center')
    root.resizable(False, False)
    root.mainloop()
    return float(ret_value.get())
