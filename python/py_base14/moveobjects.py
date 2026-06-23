import ctypes
from typing import Optional

import mapsyst
import maptype
import mapapi
import seekapi
import logapi
import maperr
import doforeach

import tkinter

_dialog_root = None

# -----------------------
# Определение локализации
# -----------------------
def _detect_lang() -> str:
    """Определяет язык интерфейса ГИС Панорама"""
    try:
        code = mapapi.mapGetMapAccessLanguage()
        if code == getattr(maptype, "ML_RUSSIAN", 2):
            return "ru"
        if code == getattr(maptype, "ML_ENGLISH", 1):
            return "en"
        return "en"
    except Exception:
        return "ru"

_LANG = _detect_lang()

_STR = {
    "ru": {
        "title": "Сдвиг объектов",
        "label_dx": "Смещение по X (вверх): ",
        "label_dy": "Смещение по Y (влево): ",
        "btn_run": "Выполнить",
        "btn_cancel": "Отменить",
        "progress": "Перемещение объектов:",
        "result_msg": "Обработано объектов - {count}",
        "result_title": "Перемещение объектов",
        "diag_dialog_open": "dialog opened",
        "diag_dialog_run": "user clicked Run, dx={dx}, dy={dy}",
        "diag_dialog_cancel": "user cancelled",
        "diag_dialog_already_open": "dialog already open, focus existing",
        "diag_done": "done, objects processed: {count}",
    },
    "en": {
        "title": "Move Objects",
        "label_dx": "Offset along X (up): ",
        "label_dy": "Offset along Y (left): ",
        "btn_run": "Run",
        "btn_cancel": "Cancel",
        "progress": "Moving objects:",
        "result_msg": "Objects processed: {count}",
        "result_title": "Move Objects",
        "diag_dialog_open": "dialog opened",
        "diag_dialog_run": "user clicked Run, dx={dx}, dy={dy}",
        "diag_dialog_cancel": "user cancelled",
        "diag_dialog_already_open": "dialog already open, focus existing",
        "diag_done": "done, objects processed: {count}",
    },
}

def tr(key: str, **kwargs) -> str:
    """Возвращает локализованную строку по ключу; подставляет параметры через format"""
    s = _STR.get(_LANG, _STR["en"]).get(key, key)
    if kwargs:
        try:
            return s.format(**kwargs)
        except Exception:
            return s
    return s

# -------------------------
# Диагностический протокол
# -------------------------
def write_diag_pair(msg_before: str, msg_after: str, msg_type: Optional[int] = None) -> None:
    """Пишет в диагностический протокол запись вида:
    TPythonScript::MoveObjects(): <msg_before>, <msg_after/param>"""
    try:
        if not mapapi.mapIsDiagnostics():
            return
        mtype = msg_type if isinstance(msg_type, int) else getattr(maptype, "MT_INFO", 0)
        prefix = "TPythonScript::MoveObjects(): "
        mapapi.mapWriteToDiagnosticsLog(mapsyst.WTEXT(prefix + msg_before), mapsyst.WTEXT(msg_after or ""), mtype)
    except Exception:
        pass

def MoveObject(_hmap:maptype.HMAP, _hobj:maptype.HOBJ, _parm:ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
    if _hobj == 0:
        return 0
    iret = mapapi.mapRelocateObjectPlane(_hobj, _parm)
    if iret != 0:
      return mapapi.mapCommitObject(_hobj)
    return 0

# Move selected objects or one object 
def MoveObjectsByDxDy(_hmap:maptype.HMAP, _hobj:maptype.HOBJ, dx, dy) -> int:
    if _hmap == 0:
        return 0

    dpoint = maptype.DOUBLEPOINT(dx, dy)
    dofunction = doforeach.DoForEach(tr("progress"), logapi.TAC_MED_MOVE)
    result = dofunction.run(MoveObject, _hmap, _hobj, ctypes.byref(dpoint))

    mapapi.mapShowMessage(
        mapsyst.WTEXT(tr("result_msg", count=mapapi.IntToStr(result))),
        mapsyst.WTEXT(tr("result_title")),
    )
    mapapi.mapInvalidate()
    write_diag_pair("MoveObjectsByDxDy(): ", tr("diag_done", count=result))
    return result


# Move selected objects or one object
def MoveObjects(_hmap:maptype.HMAP, _hobj:maptype.HOBJ) -> float: #caption:Сдвинуть объекты на заданные смещения dx,dy
    global _dialog_root

    if _hmap == 0:
        return 0

    if _dialog_root is not None:
        try:
            if _dialog_root.winfo_exists():
                write_diag_pair("MoveObjects(): ", tr("diag_dialog_already_open"))
                _dialog_root.lift()
                _dialog_root.focus_force()
                return 0
        except tkinter.TclError:
            pass
        _dialog_root = None

    if seekapi.mapIsTotalSeekObjectNotEmpty(_hmap) == 0:
        if _hobj == 0:
            mapapi.mapErrorMessageUn(maperr.IDS_OBJECTSNOTSELECTED, __name__)
            return 0
    else:
        _hobj = 0

    write_diag_pair("MoveObjects(): ", tr("diag_dialog_open"))

    root = tkinter.Tk()
    _dialog_root = root
    root.title(tr("title"))
    root.wm_attributes('-topmost', 1)
 
    dx_label = tkinter.Label(root, text=tr("label_dx"))
    dy_label = tkinter.Label(root, text=tr("label_dy"))
    dx_label.grid(row=0, column=0, sticky="w")
    dy_label.grid(row=1, column=0, sticky="w")

    dx_value = tkinter.IntVar()
    dy_value = tkinter.IntVar()

    dx_entry = tkinter.Entry(root, textvariable=dx_value)
    dy_entry = tkinter.Entry(root, textvariable=dy_value)
    dx_entry.grid(row=0,column=1, padx=5, pady=5)
    dy_entry.grid(row=1,column=1, padx=5, pady=5)

    ret_value = tkinter.IntVar()
    ret_value.set(0)

    def Close():
        global _dialog_root
        write_diag_pair("MoveObjects(): ", tr("diag_dialog_cancel"))
        _dialog_root = None
        root.destroy()

    def Run():
        write_diag_pair("MoveObjects(): ", tr("diag_dialog_run", dx=dx_value.get(), dy=dy_value.get()))
        ret = MoveObjectsByDxDy(_hmap, _hobj, dx_value.get(), dy_value.get())
        ret_value.set(ret)
        global _dialog_root
        _dialog_root = None
        root.destroy()

    message_button = tkinter.Button(root, text=tr("btn_run"), command=Run)
    message_button.grid(row=2,column=0, padx=5, pady=5, sticky="e")
    message_button = tkinter.Button(root, text=tr("btn_cancel"), command=Close)
    message_button.grid(row=2,column=1, padx=5, pady=5, sticky="w")

    root.protocol("WM_DELETE_WINDOW", Close)
    root.eval('tk::PlaceWindow . center')
    root.resizable(False, False)
    root.mainloop()
    return float(ret_value.get())
