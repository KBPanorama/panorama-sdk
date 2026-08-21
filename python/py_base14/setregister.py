import ctypes

import mapsyst
import maptype
import mapapi
import seekapi
import logapi
import maperr
import doforeach

import tkinter
from tkinter import filedialog
from tkinter import ttk

def SetRegister(_hmap:maptype.HMAP, _hobj:maptype.HOBJ, modevalue:int) -> int:
    if _hobj == 0:
        return 0

    if mapapi.mapPolyCount(_hobj) > 1:
        return 0

    local = mapapi.mapObjectLocal(_hobj)
    if local != maptype.LOCAL_TITLE:
        return 0

    text = mapsyst.WTEXT(1024)        
    mapapi.mapGetTextUn(_hobj,text,1024,0)
    newtext = text.string()
    code = 0;
    number = 0
    if newtext[0] == '#':
        scode = newtext[1:]
        code = int(scode)
        if code != 0:
            number = mapapi.mapSemanticCodeValueNameUn(_hobj,code,text,1024,1)
            if number != 0:
              newtext = text.string()
    if modevalue == 1:                  #'abc'
        newtext = newtext.lower()
    if modevalue == 2:                  # 'ABC
        newtext = newtext.upper()
    if modevalue == 3:                  # 'Abc'
        newtext = newtext.lower()
    t1 = newtext[0]
    t1 = t1.upper()
    newtext = t1 + newtext[1:] 
    text = newtext    
    if code == 0:
        mapapi.mapPutTextUn(_hobj,mapsyst.WTEXT(text),0)
    else:
        mapapi.mapSetSemanticValueUn(_hobj, number, mapsyst.WTEXT(text),0)
    return mapapi.mapCommitObject(_hobj)

def DoSetRegister(_hmap:maptype.HMAP, _hobj:maptype.HOBJ, mode:str) -> int:
    dofunction = doforeach.DoForEach('Установка регистра:', logapi.TAC_MED_TITLE)
    modevalue = 1
    if mode == 'abc':
        modevalue = 1
    if mode == 'ABC':
        modevalue = 2
    if mode == 'Abc':
        modevalue = 3

    result = dofunction.run(SetRegister, _hmap, _hobj, modevalue)

    mapapi.mapShowMessage(mapsyst.WTEXT('Обработка выполнена в режиме: \"' + mode + '\", обработано объектов: ' + mapapi.IntToStr(result)), mapsyst.WTEXT('Установка регистра подписей'))
    mapapi.mapInvalidate()
    return result

mode = 'Abc'  
objcount = 0
def SetLabelsRegister(_hmap:maptype.HMAP, _hobj:maptype.HOBJ) -> float: #caption:Установка регистра подписей
    if _hmap == 0:
        return 0

    if seekapi.mapIsTotalSeekObjectNotEmpty(_hmap) == 0:
        if _hobj == 0:
            mapapi.mapErrorMessageUn(maperr.IDS_OBJECTSNOTSELECTED, __name__)
            return 0
    else:
        _hobj = 0

    root = tkinter.Tk()
    root.title("Регистр")
    root.wm_attributes('-topmost', 1)
    def CallProcess():
        global mode 
        global objcount 
        mode = str(combo.get())    
        objcount = DoSetRegister(_hmap, _hobj, combo.get())
        root.destroy()
    combo = ttk.Combobox(root,values = ["Abc", "ABC", "abc"])
    combo.current(1)  
    combo['state'] = 'readonly'
    combo.grid(column=0, row=0, padx=5, pady=5)
    button = tkinter.Button(root, text="Выполнить", command=CallProcess)
    button.grid(row=0,column=1, padx=5, pady=5, sticky="e")
    root.eval('tk::PlaceWindow . center')
    root.resizable(False, False)
    root.mainloop()
    return objcount
