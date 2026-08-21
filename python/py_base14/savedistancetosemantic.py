import ctypes

import mapsyst
import maptype
import mapapi
import seekapi
import rscapi
import logapi
import maperr
import mapselec
import doforeach

import tkinter

class DistanceParm:
    __point = maptype.DOUBLEPOINT(0., 0.)
    __code = 0

    def __init__(self, code):
        self.__code = code

    def setpoint(self, x, y):
        self.__point.X = x
        self.__point.Y = y

    def point(self):
        return self.__point

    def code(self):
        return self.__code

def ObjectDistance(_hmap:maptype.HMAP, _hobj:maptype.HOBJ, _parm:DistanceParm) -> int:
    distance = mapapi.mapDistancePointObject(_hmap, _hobj, ctypes.byref(_parm.point()))
    iret = mapapi.mapAppendSemanticDouble(_hobj, _parm.code(), distance)
    if iret != 0:
      return mapapi.mapCommitObject(_hobj)
    return 0 

def _RunDistanceToSemantic(_hmap:maptype.HMAP, _hobj:maptype.HOBJ, _code:int) -> int:
    if _hmap == 0:
        return 0

    if _hobj == 0:
        return 0

    if _code == 0:
        return 0

    getdistance = DistanceParm(_code)

    x = ctypes.c_double(0)
    y = ctypes.c_double(0)
    mapapi.mapGetObjectCenterEx(_hmap, _hobj, ctypes.byref(x), ctypes.byref(y), 0)
    getdistance.setpoint(x, y)

    dofunction = doforeach.DoForEach('Подсчет расстояний:', logapi.TAC_MED_SEMAPPEND)
    result = dofunction.run(ObjectDistance, _hmap, 0, getdistance)

    mapapi.mapShowMessage(mapsyst.WTEXT('Обработано объектов - ' + mapapi.IntToStr(result)), mapsyst.WTEXT('Подсчет расстояний и запись в семантику'))
    return result

# Calculation of the distance from objects to point and save value in objects semantic
def DistanceToSemantic(_hmap:maptype.HMAP, _hobj:maptype.HOBJ) -> float: #caption:Вычислить расстояние до объекта и записать в его семантику
    if _hmap == 0:
        return 0

    if seekapi.mapIsTotalSeekObjectNotEmpty(_hmap) == 0:
      mapapi.mapErrorMessageUn(maperr.IDS_OBJECTSNOTSELECTED, __name__)
      return 0

    if _hobj == 0:
      mapapi.mapErrorMessageUn(maperr.IDS_OBJECTNOTSETTED, __name__)
      return 0

    seekcount = seekapi.mapTotalSeekObjectCount(_hmap)

    root = tkinter.Tk()
    root.title("Расстояние до объекта записать в семантику")

    src_label0 = tkinter.Label(root, text="Выделено объектов: ")
    src_label0.grid(row=0, column=0, sticky="w")
    src_value0 = tkinter.IntVar(master=root)
    src_value0.set(seekcount)
    src_entry0 = tkinter.Entry(root, width=10, textvariable=src_value0)
    src_entry0.grid(row=0,column=1, padx=5, pady=5)
    src_entry0['state'] = 'readonly'

    src_label = tkinter.Label(root, text="Семантика для расстояния: ")
    src_label.grid(row=1, column=0, sticky="w")
    src_value = tkinter.IntVar(master=root)
    src_entry = tkinter.Entry(root, width=10, textvariable=src_value)
    src_entry.grid(row=1,column=1, padx=5, pady=5)

    semname = mapsyst.WTEXT(128)
    hrsc = rscapi.mapGetRscIdent(_hmap, _hmap)
    rscapi.mapGetRscSemanticNameUn(hrsc, 2, semname, semname.size())
    src_select = tkinter.Button(root, text=semname.string())
    src_value.set(2)

    def SelectSemanticSrc():
        parm = maptype.TASKPARMEX()
        parm.Handle = mapapi.mapGetHandleForMessage()
        semcode = mapselec.selSemanticSelectInit(hrsc, ctypes.byref(parm), src_value.get())
        if semcode != 0:
            src_value.set(semcode)
            rscapi.mapGetRscSemanticNameUn(hrsc, semcode, semname, semname.size())
            src_select.configure(text=semname.string())

    src_select.configure(command=SelectSemanticSrc, width=30)
    src_select.grid(row=1, column=2, padx=10, sticky="w")

    ret_value = tkinter.IntVar(master=root)
    ret_value.set(0)

    def Run():
        root.destroy()
        ret = _RunDistanceToSemantic(_hmap, _hobj, src_value.get())
        ret_value.set(ret)

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
