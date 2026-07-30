#!/usr/bin/env python3

"""
.. code-block:: none

    ********************************************************************
    *                                                                  *
    *              Copyright (c) PANORAMA Group 1991-2026              *
    *                      All Rights Reserved                         *
    *                                                                  *
    ********************************************************************
    *                                                                  *
    *      Стандартные диалоги для приложений на GIS ToolKit           *
    *                                                                  *
    *   typedef long int (WINAPI* INSERTPOINTS)(HMAP hMap,             *
    *                                        const TASKPARMEX* parm,   *
    *                                        HOBJ hobj,                *
    *                                        RECT* rect);              *
    *   HINSTANCE libInst;                                             *
    *   INSERTPOINTS pInsertPoints = (INSERTPOINTS)                    *
    *        mapLoadLibrary(MAPSCENALIB, &libInst, "tedInsertPoints"); *
    *                                                                  *
    *   long int result = pInsertPoints(hMap, parm, hobj, 0);          *
    *   mapFreeLibrary(libInst);                                       *
    *                                                                  *
    ********************************************************************
    
"""

import os
import ctypes
import mapsyst
import maptype
import mapcreat
import mapgdi

PACK_WIDTH = 1
# Доступ к режимам диалога открытия атласа

ALS_NO_CHOICE_ATLAS = 1
ALS_NO_SEND_MESSAGE = 2


#-----------------------------
class BUILDZONEPARMEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Radius",ctypes.c_double),
                ("FlagDial",ctypes.c_int),
                ("Check",ctypes.c_int),
                ("Size",ctypes.c_int),
                ("TypeZone",ctypes.c_int),
                ("EnableType",ctypes.c_int),
                ("FormZone",ctypes.c_int)]
#-----------------------------


#-----------------------------
class COPY_OPTIONS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("MapNumber",ctypes.c_int),
                ("Code",ctypes.c_int),
                ("DeleteSourceObject",ctypes.c_int),
                ("DeleteWrongSemantic",ctypes.c_int),
                ("CutByObject",ctypes.c_int),
                ("LocationPoint",ctypes.c_int),
                ("SimplifyScale",ctypes.c_int),
                ("Reserve",ctypes.c_int*(9))]
#-----------------------------




try:
    if os.environ['gisdlgsdll']:
        gisdlgsname = os.environ['gisdlgsdll']
except KeyError:
    gisdlgsname = 'gis64dlgs.dll'

try:
    dlgslib = mapsyst.LoadLibrary(gisdlgsname)
except Exception as e:
    print(e)
    dlgslib = 0

if dlgslib == 0:
    print(gisdlgsname)
else:
    tedInsertPoints_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'tedInsertPoints', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ, ctypes.POINTER(maptype.RECT))
    def tedInsertPoints(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _hobj: maptype.HOBJ, _rect: ctypes.POINTER(maptype.RECT)) -> int:
        """
        Вызвать диалог "Редактирование метрики объекта"
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _parm: параметры задачи (поле Handle должно содержать идентификатор главного окна)
        
        :param _hobj: идентификатор редактируемого объекта
        
        :param _rect: местоположение открываемого диалога или ``0`` Вызов файла справки из mapscena (topic: enpoint)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return tedInsertPoints_t (_hmap, _parm, _hobj, _rect)

    tedEditSemantic_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'tedEditSemantic', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ)
    def tedEditSemantic(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _hobj: maptype.HOBJ) -> int:
        """
        Вызвать диалог "Редактирование семантики объекта"
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _parm: параметры задачи (поле Handle должно содержать идентификатор главного окна)
        
        :param _hobj: идентификатор редактируемого объекта Вызов файла справки из mapscena (topic: sokol)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return tedEditSemantic_t (_hmap, _parm, _hobj)

    tedUpdateSemantic_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'tedUpdateSemantic', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def tedUpdateSemantic(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог "Обновление семантики объектов"
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _parm: параметры задачи (поле Handle должно содержать идентификатор главного окна) Вызов файла справки из mapscena (topic: zamsem)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return tedUpdateSemantic_t (_hmap, _parm)

    semGetDateSemantic_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'semGetDateSemantic', ctypes.c_char_p, ctypes.c_long, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(maptype.POINT))
    def semGetDateSemantic(_value: ctypes.c_char_p, _size: int, _parm: ctypes.POINTER(maptype.TASKPARMEX), _point: ctypes.POINTER(maptype.POINT)) -> int:
        """
        Вызвать диалог "Редактирование семантики типа "Дата"
        
        :param _value: адрес строки, содержащей дату в виде ДД/ММ/ГГГГ (строка исходная и в неё же записывается результат)
        
        :param _size: размер строки
        
        :param _parm: структура параметров для диалога (maptype.h)
        
        :param _point: координаты верхнего левого угла диалога
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return semGetDateSemantic_t (_value, _size, _parm, _point)

    tedSetPolyTextEx_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'tedSetPolyTextEx', ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ, ctypes.c_long, ctypes.POINTER(maptype.LOGFONT), ctypes.POINTER(ctypes.c_long))
    def tedSetPolyTextEx(_taskparm: ctypes.POINTER(maptype.TASKPARMEX), _hobj: maptype.HOBJ, _subject: int, _font: ctypes.POINTER(maptype.LOGFONT), _flagchangetext: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Установить или измененить текст многострочной подписи
        
        parm           - параметры задачи (поле Handle должно содержать идентификатор главного окна)
        
        :param _hobj: идентификатор объекта типа ПОДПИСЬ
        
        :param _subject: номер подобъекта
        
        :param _font: описание шрифта
        
        :param _flagchangetext: указатель на признак изменения текста для линейки макетов или ноль
        
        :returns: При вызове диалога Выбор объекта для редактирования семантики возвращает -1 При отказе возвращает 0, иначе 1
        :rtype: int
        """
        return tedSetPolyTextEx_t (_taskparm, _hobj, _subject, _font, _flagchangetext)

    tedSetTextUn_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'tedSetTextUn', ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.RECT))
    def tedSetTextUn(_parm: ctypes.POINTER(maptype.TASKPARMEX), _caption: mapsyst.WTEXT, _ctext: mapsyst.WTEXT, _size: int, _rect: ctypes.POINTER(maptype.RECT)) -> int:
        """
        Ввести произвольный текст
        
        :param _parm: параметры задачи (поле Handle должно содержать идентификатор главного окна)
        
        :param _caption: заголовок
        
        :param _ctext: вводимый текст
        
        :param _size: размер текста
        
        :param _rect: размеры диалога
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return tedSetTextUn_t (_parm, _caption.buffer(), _ctext.buffer(), _size, _rect)

    tedUndoOperation_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'tedUndoOperation', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def tedUndoOperation(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог "Отмена транзакций"
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _parm: параметры задачи (поле Handle должно содержать идентификатор главного окна) Вызов файла справки из mapscena (topic: kon1)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return tedUndoOperation_t (_hmap, _parm)

    tedGoPoint_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'tedGoPoint', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT))
    def tedGoPoint(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _place: int, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Вызвать диалог "Перейти в заданную точку по координатам"
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _parm: параметры задачи (поле Handle должно содержать идентификатор главного окна)
        
        :param _place: формат отображаемых в диалоге координат: ``PLANEPOINT``      ``= 1``,  в метрах на местности ``MAPPOINT``        ``= 2``,  в условных единицах карты (дискретах) ``PICTUREPOINT``    ``= 3``,  в пикселах текущего полного изображения эллипсоид Красовского ``1942``г ``GEORAD``          ``= 4``,  в радианах в соответствии с проекцией ``GEOGRAD``         ``= 5``,  в градусах ``GEOGRADMIN``      ``= 6``,  в градусах, минутах, секундах общеземной эллипсоид ``WGS84`` ``GEORADWGS84``     ``= 7``,  в радианах в соответствии с проекцией ``GEOGRADWGS84``    ``= 8``,  в градусах ``GEOGRADMINWGS84`` ``= 9``,  в градусах, минутах, секундах ``PLANE42POINT``    ``= 10``, в метрах на местности по ближайшей зоне ``GEORADPZ90``      ``= 11``, в радианах в соответствии с проекцией ``GEOGRADPZ90``     ``= 12``, в градусах ``GEOGRADMINPZ90``  ``= 13``, в градусах, минутах, секундах
        
        :param _point: координаты текущей точки в метрах на карте
        
        :returns: При успешном выполнении возвращает координаты выбранной точки в метрах на карте Вызов файла справки из mapscena (topic: movement) При ошибке возвращает ноль
        :rtype: int
        """
        return tedGoPoint_t (_hmap, _parm, _place, _point)

    tedAddDataFormDirEx_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'tedAddDataFormDirEx', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_char_p, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def tedAddDataFormDirEx(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _title: ctypes.c_char_p, _flagsit: int, _flagmtw: int, _flagrsw: int, _flagmtl: int, _flagmtq: int, _flagtin: int) -> int:
        """
        Вызвать диалог "Добавление в документ данных из каталога"
        
        Могут быть добавлены векторная карта, Mtw, Rsw, Mtl, Mtq, Tin
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _parm: параметры задачи (поле Handle должно содержать идентификатор главного окна)
        
        :param _title: указатель на текст заголовка диалога или ``0``
        
        :param _flagsit: флаг запрета добавления карты (``0``-запрещено/``1``-разрешено)
        
        :param _flagmtw: флаг запрета добавления Mtw (``0``-запрещено/``1``-разрешено)
        
        :param _flagrsw: флаг запрета добавления Rsw (``0``-запрещено/``1``-разрешено)
        
        :param _flagmtl: флаг запрета добавления Mtl (``0``-запрещено/``1``-разрешено)
        
        :param _flagmtq: флаг запрета добавления Mtq (``0``-запрещено/``1``-разрешено)
        
        :param _flagtin: флаг запрета добавления Tin (``0``-запрещено/``1``-разрешено) Вызов файла справки из mapscena (topic: idn7081)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return tedAddDataFormDirEx_t (_hmap, _parm, _title, _flagsit, _flagmtw, _flagrsw, _flagmtl, _flagmtq, _flagtin)

    scnGetObjectFromRscUnEx_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'scnGetObjectFromRscUnEx', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ, ctypes.POINTER(maptype.OBJFROMRSC), maptype.PWCHAR, ctypes.c_int)
    def scnGetObjectFromRscUnEx(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _hobj: maptype.HOBJ, _objparm: ctypes.POINTER(maptype.OBJFROMRSC), _title: mapsyst.WTEXT, _checkedit: int) -> int:
        """
        Вызвать диалог "Выбор вида объекта из классификатора (в том числе для создания нового)"
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _hobj: идентификатор объекта
        
        :param _objparm: параметры для диалога выбора вида объекта name      - заголовок диалога
        
        :param _checkedit: флаг обязательного наличия карт, доступных для редактирования если checkedit ``= 1`` и нет карт доступных для редактирования при вызове диалога будет сгенерирована ошибка
        
        :returns: Возвращает внутренний код объекта При ошибке или отмене выбора возвращает 0
        :rtype: int
        """
        return scnGetObjectFromRscUnEx_t (_hmap, _parm, _hobj, _objparm, _title.buffer(), _checkedit)

    scnSetLineDraw_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'scnSetLineDraw', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ, ctypes.POINTER(ctypes.c_long), ctypes.c_long)
    def scnSetLineDraw(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _hobj: maptype.HOBJ, _regime: ctypes.POINTER(ctypes.c_long), _isnew: int) -> int:
        """
        Вызвать диалог настройки графического описания линии и полигона
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _hobj: идентификатор редактируемого объекта
        
        :param _regime: указатель на переменную, в которую будет записан выбранный способ нанесения объекта (``MC_POLYLINE``, ``MC_RECT``,...)
        
        :param _isnew: признак нового или редактируемого объекта: ``1`` - объект создается (есть кнопки способа нанесения) ``0`` - редактируется графика объекта, нет кнопок способа нанесения На момент вызова функции hobj должен быть зарегистрирован (mapRegisterDrawObject) как линейный или площадной объект (в зависимости от локализации появляются разные диалоги)
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return scnSetLineDraw_t (_hmap, _parm, _hobj, _regime, _isnew)

    scnSetLabelDraw_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'scnSetLabelDraw', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ, ctypes.POINTER(ctypes.c_long), ctypes.c_long)
    def scnSetLabelDraw(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _hobj: maptype.HOBJ, _regime: ctypes.POINTER(ctypes.c_long), _isnew: int) -> int:
        """
        Вызвать диалог настройки графического описания подписи
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _hobj: идентификатор редактируемого объекта
        
        :param _regime: указатель на переменную, в которую будет записан выбранный способ нанесения объекта (``MC_POLYLINE``, ``MC_RECT``,...)
        
        :param _isnew: признак нового или редактируемого объекта: ``1`` - объект создается (есть кнопки способа нанесения) ``0`` - редактируется графика объекта, нет кнопок способа нанесения На момент вызова функции hobj должен быть зарегистрирован (mapRegisterDrawObject) как подпись
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return scnSetLabelDraw_t (_hmap, _parm, _hobj, _regime, _isnew)

    mapExecuteGNClient_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'mapExecuteGNClient', ctypes.POINTER(maptype.TASKPARMEX))
    def mapExecuteGNClient(_parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог "Настройка вида лицензии"
        
        :param _parm: параметры задачи (поле IniName должно содержать имя ini файла, поле PathShell - каталог приложения) Вызов файла справки из mapscena (topic: idn_license)
        
        :returns: При ошибке или отказе возвращает 0
        :rtype: int
        """
        return mapExecuteGNClient_t (_parm)

    scnGetMapNumberWithTitleEx_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'scnGetMapNumberWithTitleEx', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.PWCHAR)
    def scnGetMapNumberWithTitleEx(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _maptype: ctypes.POINTER(ctypes.c_int), _accesstype: int, _current: int, _addflag: int, _title: mapsyst.WTEXT) -> int:
        """
        Выбрать номер карты (векторной, растровой, матричной) из списка
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _maptype: тип данных: ``FILE_MAP``, ``FILE_RSW``, ``FILE_MTW``
        
        :param _accesstype: тип доступа к данным: ``0`` - все, ``1`` - только для копирования, ``2`` - только с полным доступом
        
        :param _current: номер карты для установки ее текущей
        
        :param _addflag: флаг добавления карт в список
        
        :param _title: название вызывающей задачи
        
        :returns: Возвращает: -1 при отказе от выбора или отсутствии карт, иначе - номер карты в списке (с 0 для FILE_MAP и с 1 для FILE_RSW, FILE_MTW)
        :rtype: int
        """
        return scnGetMapNumberWithTitleEx_t (_hmap, _parm, _maptype, _accesstype, _current, _addflag, _title.buffer())


# Вызвать функцию создания диалога обработки сообщения
# hWnd     -  идентификатор окна
# message  -  строка, содержащая текст сообщения для размещения в окне диалога
# title    -  заголовок диалога
# flag     -  тип сообщения (MB_OK, MB_YESNO, MB_YESNOCANCEL)
# percent  -  значение процента выполнения
# second   -  значение оставшегося времени обработки в секундах
# Возвращает идентификатор окна диалога
# Для закрытия диалога нужно вызвать функцию scnCloseMessageBoxProcess
# При ошибке возвращает 0

#   scnOpenMessageBoxProcess_t = mapsyst.GetProcAddress(dlgslib,,'scnOpenMessageBoxProcess', maptype.HWND, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_long, ctypes.c_long, ctypes.c_long)
#   def scnOpenMessageBoxProcess(_hWnd: maptype.HWND, _message: ctypes.c_char_p, _title: ctypes.c_char_p, _flag: int, _percent: int, _second: int) -> :
#       return scnOpenMessageBoxProcess_t (_hWnd, _message, _title, _flag, _percent, _second)

    scnUpdateMessageBoxProcess_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'scnUpdateMessageBoxProcess', ctypes.c_void_p, ctypes.c_long, ctypes.c_long)
    def scnUpdateMessageBoxProcess(_hmsgproc: ctypes.c_void_p, _percent: int, _second: int) -> int:
        """
        Вызвать функцию обновления содержимого диалога
        
        :param _hmsgproc: идентификатор окна диалога обработки сообщения (получен как результат выполнения функции CallMessageBoxProcess)
        
        :param _percent: значение процента выполнения
        
        :param _second: значение оставшегося времени обработки в секундах
        
        :returns: Если диалог закрыт пользователем, то возвращает 0 В этом случае нужно вызвать scnCloseMessageBoxProcess
        :rtype: int
        """
        return scnUpdateMessageBoxProcess_t (_hmsgproc, _percent, _second)

    scnCloseMessageBoxProcess_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'scnCloseMessageBoxProcess', ctypes.c_void_p)
    def scnCloseMessageBoxProcess(_hmsgproc: ctypes.c_void_p) -> int:
        """
        Вызвать функцию закрытия диалога
        
        :param _hmsgproc: идентификатор окна диалога обработки сообщения (получен как результат выполнения функции CallMessageBoxProcess)
        
        :returns: Возвращает код нажатой кнопки - IDYES, IDNO, IDCANCEL.
        :rtype: int
        """
        return scnCloseMessageBoxProcess_t (_hmsgproc)

    scnChangeCodeSemantic_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'scnChangeCodeSemantic', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(ctypes.c_long), ctypes.c_long)
    def scnChangeCodeSemantic(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _sitenumber: ctypes.POINTER(ctypes.c_long), _code: int) -> int:
        """
        Вызвать функцию выбора кода семантики из классификатора для просмотра
        
        :param _hmap: идентификатор открытой векторной карты
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _sitenumber: номер векторной карты в цепочке от ``1`` до числа карт
        
        :param _code: код семантики для просмотра
        
        :returns: Возвращает код назначенной семантики и номер пользовательской карты (sitenumber).
        :rtype: int
        """
        return scnChangeCodeSemantic_t (_hmap, _parm, _sitenumber, _code)

    semMakeSemantic_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'semMakeSemantic', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ, ctypes.c_long)
    def semMakeSemantic(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _hobj: maptype.HOBJ, _ident: int) -> int:
        """
        Вызвать функцию редактирования семантики
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _hobj: идентификатор редактируемого объекта
        
        :param _ident: для режима Редактора ``"Создание объекта"`` ident ``= 0``, иначе ident ``= 1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return semMakeSemantic_t (_hmap, _parm, _hobj, _ident)

    tedLoadObjectsFromKML_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'tedLoadObjectsFromKML', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ, ctypes.c_char_p)
    def tedLoadObjectsFromKML(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _hobj: maptype.HOBJ, _kmlfile: ctypes.c_char_p) -> int:
        """
        Нанести объекты по координатам из файла KML
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _kmlfile: полное имя загружаемого файла
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return tedLoadObjectsFromKML_t (_hmap, _parm, _hobj, _kmlfile)

    scnDbmOpen_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'scnDbmOpen', ctypes.POINTER(maptype.TASKPARMEX))
    def scnDbmOpen(_parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Выбрать открываемый файл DBM и открыть таблицу из базы пространственных данных
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :returns: Возвращает ненулевое значение, если карта открыта или добавлена При ошибке возвращает ноль
        :rtype: int
        """
        return scnDbmOpen_t (_parm)

    scnSetDbmConnectDbParam_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'scnSetDbmConnectDbParam', ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(maptype.TSQLMap_DBConnectParmEx), maptype.PWCHAR)
    def scnSetDbmConnectDbParam(_parm: ctypes.POINTER(maptype.TASKPARMEX), _dbparams: ctypes.POINTER(maptype.TSQLMap_DBConnectParmEx), _title: mapsyst.WTEXT) -> int:
        """
        Настроить параметры подключения к базе пространственных данных, открываемой через файл DBM
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _dbparams: параметры подключения
        
        :param _title: условное имя базы данных в заголовок диалога или ``0``
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return scnSetDbmConnectDbParam_t (_parm, _dbparams, _title.buffer())

    scnDbmParam_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'scnDbmParam', ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, ctypes.c_long)
    def scnDbmParam(_parm: ctypes.POINTER(maptype.TASKPARMEX), _dbmname: mapsyst.WTEXT, _size: int) -> int:
        """
        Вызвать диалог просмотра и редактирования параметров представления пространственной БД
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _dbmname: полное имя файла ``DBM``
        
        :param _size: размер буфера для записи имени файла При вызове режима ``"Сохранить как"`` в dbmname запишется новое имя файла
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return scnDbmParam_t (_parm, _dbmname.buffer(), _size)

    svGetUserData_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'svGetUserData', ctypes.POINTER(maptype.TASKPARMEX))
    def svGetUserData(_parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог регистрации пользователя на ГИС Сервере
        
        :param _parm: параметры задачи (поле Handle должно содержать идентификатор главного окна) Для ввода имени пользователя и пароля и подключения к ГИС Серверу
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return svGetUserData_t (_parm)

    svGetUserDataEx_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'svGetUserDataEx', ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_char_p)
    def svGetUserDataEx(_parm: ctypes.POINTER(maptype.TASKPARMEX), _aliasname: ctypes.c_char_p) -> int:
        """
        Вызвать диалог регистрации пользователя на ГИС Сервере при открытии данных
        
        :param _parm: параметры задачи (поле Handle должно содержать идентификатор главного окна)
        
        :param _aliasname: алиас данных вида ``"HOST#ХОСТ:ПОРТ#ALIAS#условное_имя_карты"`` Для ввода имени пользователя и пароля и подключение к ГИС Серверу
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return svGetUserDataEx_t (_parm, _aliasname)

    svGetConnectParameters_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'svGetConnectParameters', ctypes.POINTER(maptype.TASKPARMEX))
    def svGetConnectParameters(_parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог ввода параметров соединения с ГИС Сервером
        
        :param _parm: параметры задачи (поле Handle должно содержать идентификатор главного окна) Пользователь выбирает имя хоста (или ``IP``) и номер порта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return svGetConnectParameters_t (_parm)

    svOpenDataEx_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'svOpenDataEx', ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_char_p, ctypes.c_long)
    def svOpenDataEx(_parm: ctypes.POINTER(maptype.TASKPARMEX), _name: ctypes.c_char_p, _size: int) -> int:
        """
        Вызвать диалог выбора доступных пользователю данных на ГИС Сервере
        
        :param _parm: параметры задачи (поле Handle должно содержать идентификатор главного окна)
        
        :param _name: буфер для размещения выбранного алиаса данных (выделять не менее ``MAXPATH``)
        
        :param _size: размер выделенного буфера Имя выбранного алиаса карты помещается в name
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return svOpenDataEx_t (_parm, _name, _size)

    svOpenDataAtlas_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'svOpenDataAtlas', ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_char_p, ctypes.c_long)
    def svOpenDataAtlas(_parm: ctypes.POINTER(maptype.TASKPARMEX), _name: ctypes.c_char_p, _size: int) -> int:
        """
        Вызвать диалог выбора доступных пользователю данных на ГИС Сервере
        
        для атласа
        
        :param _parm: параметры задачи (поле Handle должно содержать идентификатор главного окна)
        
        :param _name: буфер для размещения выбранного алиаса данных (выделять не менее ``MAXPATH``)
        
        :param _size: размер выделенного буфера Имя выбранного алиаса карты помещается в name
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return svOpenDataAtlas_t (_parm, _name, _size)

    svOpenDataAtlasEx_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'svOpenDataAtlasEx', ctypes.POINTER(maptype.TASKPARMEX), maptype.HWND)
    def svOpenDataAtlasEx(_parm: ctypes.POINTER(maptype.TASKPARMEX), _hwnd: maptype.HWND) -> int:
        """
        Вызвать диалог выбора доступных пользователю данных на ГИС Сервере для атласа
        
        :param _parm: параметры задачи (поле Handle должно содержать идентификатор главного окна)
        
        :param _hwnd: идентификатор окна атласа для передачи сообщений о открытии данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return svOpenDataAtlasEx_t (_parm, _hwnd)

    svGetServerData_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'svGetServerData', ctypes.POINTER(maptype.TASKPARMEX), maptype.HWND)
    def svGetServerData(_parm: ctypes.POINTER(maptype.TASKPARMEX), _hwnd: maptype.HWND) -> int:
        """
        Вызвать диалог выбора для уже зарегистрированных пользователей доступных данных на ГИС Сервере
        
        :param _parm: параметры задачи (поле Handle должно содержать идентификатор главного окна)
        
        :param _hwnd: идентификатор окна для передачи сообщений Возможен множественный выбор данных При выборе данных окну посылается сообщение ``MT_CHANGEDATAUN`` (``0x65D``, ``WPARAM`` - type : ``FILE_MAP``, ``FILE_RSW``, ``FILE_MTW``... ``LPARAM`` - имя выбранного алиаса данных (указатель на двухбайтовую строку в кодировке UTF-16)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return svGetServerData_t (_parm, _hwnd)

    svGetServerTypeData_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'svGetServerTypeData', ctypes.POINTER(maptype.TASKPARMEX), maptype.HWND, ctypes.c_long)
    def svGetServerTypeData(_parm: ctypes.POINTER(maptype.TASKPARMEX), _hwnd: maptype.HWND, _filetype: int) -> int:
        """
        Вызвать диалог выбора для уже зарегистрированных пользователей доступных данных определенного типа на ГИС Сервере
        
        :param _parm: параметры задачи (поле Handle должно содержать идентификатор главного окна)
        
        :param _hwnd: идентификатор окна для передачи сообщений
        
        :param _filetype: тип открываемых данных: ``1`` - карты, ``2`` - матрицы, ``3`` - растры, -``1`` - данные всех типов При выборе данных окну посылается сообщение ``MT_CHANGEDATAUN`` (``0x65D``, ``WPARAM`` - type : ``FILE_MAP``, ``FILE_RSW``, ``FILE_MTW``... ``LPARAM`` - имя выбранного алиаса данных (указатель на двухбайтовую строку в кодировке UTF-16) Возможен множественный выбор данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return svGetServerTypeData_t (_parm, _hwnd, _filetype)

    svOpenData_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'svOpenData', ctypes.POINTER(maptype.TASKPARMEX))
    def svOpenData(_parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог выбора доступных пользователю данных на ГИС Сервере
        
        :param _parm: параметры задачи (поле Handle должно содержать идентификатор главного окна) При выборе открываемых данных главному окну посылается сообщение ``AW_OPENDOC`` (``0x655``) c именем выбранного алиаса карты (может быть передан в mapOpenData)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return svOpenData_t (_parm)

    svAppendData_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'svAppendData', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def svAppendData(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог выбора доступных пользователю данных на ГИС Сервере для добавления к текущей открытой карте
        
        :param _parm: параметры задачи (поле Handle должно содержать идентификатор главного окна) При выборе добавляемых данных вызывается функция mapAppendData, и окну карты посылается уведомление - сообщение ``MT_CHANGEDATA`` или ``MT_CHANGEDATAUN`` (``0x65D``, ``WPARAM`` - type : ``FILE_MAP``, ``FILE_RSW``, ``FILE_MTW``...) Идентификатор окна карты запрашивается через посылку главному окну сообщения ``AW_GETCURRENTDOC`` (``0x673``, ``WPARAM`` - ``HWND`` ``*``, ``LPARAM`` - ``HMAP`` ``*``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return svAppendData_t (_hmap, _parm)

    svStringToHash_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'svStringToHash', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_long)
    def svStringToHash(_source: ctypes.c_char_p, _target: ctypes.c_char_p, _size: int) -> int:
        """
        Преобразовать строку в хэш по алгоритму MD5
        
        :param _source: исходная строка ``ANSI``
        
        :param _target: строка результата (``32`` символа и замыкающий ноль)
        
        :param _size: число байт, зарезервированных в строке (не менее ``33``)
        
        :returns: При ошибке параметров возвращает ноль
        :rtype: int
        """
        return svStringToHash_t (_source, _target, _size)

    scnOpenAtlasUn_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'scnOpenAtlasUn', ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def scnOpenAtlasUn(_parm: ctypes.POINTER(maptype.TASKPARMEX), _name: mapsyst.WTEXT, _size: int, _mode: int) -> int:
        """
        Вызвать диалог "Открыть атлас карт"
        
        :param _parm: параметры задачи (поле Handle должно содержать идентификатор главного окна)
        
        :param _name: буфер для записи имени файла атласа карт, который открывается или создается
        
        :param _size: размер буфера в байтах
        
        :param _mode: доступ к режимам диалога: ``0`` - полный доступ ``ALS_NO_CHOICE_ATLAS`` - режим редактирования выбранного атласа (выбор атласа в диалоге отменен) ``ALS_NO_SEND_MESSAGE`` - сообщение ``AW_OPENDOCUN`` главному окну не посылается
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если mode = ALS_NO_SEND_MESSAGE, то отсутствует режим Открыть данные
           Допустимо совместное использование флагов (ALS_NO_CHOICE_ATLAS | ALS_NO_SEND_MESSAGE)
           При выборе открываемых данных главному окну посылается сообщение
           AW_OPENDOCUN (``0x623``) c именем выбранной карты (может быть передано в mapOpenDataUn)
           Вызов файла справки из аrealist
        """
        return scnOpenAtlasUn_t (_parm, _name.buffer(), _size, _mode)

    scnCreateAtlasUn_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'scnCreateAtlasUn', ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def scnCreateAtlasUn(_parm: ctypes.POINTER(maptype.TASKPARMEX), _name: mapsyst.WTEXT, _size: int, _mode: int) -> int:
        """
        Вызвать диалог "Создать атлас карт"
        
        :param _parm: параметры задачи (поле Handle должно содержать идентификатор главного окна)
        
        :param _name: буфер для записи имени файла атласа карт
        
        :param _size: размер буфера в байтах
        
        :param _mode: доступ к режимам диалога: ``0`` - полный доступ ``ALS_NO_CHOICE_ATLAS`` - режим редактирования выбранного атласа (выбор атласа в диалоге отменен) ``ALS_NO_SEND_MESSAGE`` - сообщение ``AW_OPENDOCUN`` главному окну не посылается
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если mode = ALS_NO_SEND_MESSAGE, то отсутствует режим Открыть данные
           Допустимо совместное использование флагов (ALS_NO_CHOICE_ATLAS | ALS_NO_SEND_MESSAGE).
           Вызов файла справки из arealist
        """
        return scnCreateAtlasUn_t (_parm, _name.buffer(), _size, _mode)

    scnAtlasListPro_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'scnAtlasListPro', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(maptype.ALSITEM), ctypes.c_long, maptype.HALS)
    def scnAtlasListPro(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _item: ctypes.POINTER(maptype.ALSITEM), _count: int, _hals: maptype.HALS) -> int:
        """
        Вызвать диалог "Выбрать карту из списка"
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _parm: параметры задачи (поле Handle должно содержать идентификатор главного окна)
        
        :param _item: указатель на список элементов атласа, выбранных в текущей точке
        
        :param _count: число элементов в списке
        
        :param _hals: идентификатор открытого атласа
        
        :returns: Возвращает номер выбранного пользователем элемента Если функция возвращает -1, то необходимо вызвать диалог ``"Открыть атлас карт"`` Название файла справки mapscena (topic: arealist1) При ошибке возвращает ноль
        :rtype: int
        """
        return scnAtlasListPro_t (_hmap, _parm, _item, _count, _hals)

    mclOpenBuildProfEx_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_void_p,'mclOpenBuildProfEx', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(maptype.PROFBUILDPARMEX))
    def mclOpenBuildProfEx(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _profparm: ctypes.POINTER(maptype.PROFBUILDPARMEX)) -> ctypes.c_void_p:
        """
        Открыть диалог построения профиля
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _profparm: параметры построения профиля (описание в maptype.h)
        
        :returns: Возвращает указатель на диалог построения профиля (hbuildprofil) Вызов файла справки из mapscena (topic: proflin) При ошибке возвращает ноль
        
        .. note::

           Если шаг по горизонтали в profparm равен нулю, отображается весь профиль
           Указанные шаг по горизонтали и по вертикали могут быть скорректированы
           согласно масштабу и высоте
           В процессе работы диалога в profparm записываются текущие параметры
           При закрытии диалога главному окну посылается сообщение
           AW_CLOSEDIALOGNOTIFY (``0x610`` - maptype.h)
        """
        return mclOpenBuildProfEx_t (_hmap, _parm, _profparm)

    mclCloseBuildProf_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'mclCloseBuildProf', ctypes.c_void_p)
    def mclCloseBuildProf(_hbuildprofil: ctypes.c_void_p) -> int:
        """
        Закрыть диалог построения профиля
        
        :param _hbuildprofil: указатель открытого диалога построения профиля
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mclCloseBuildProf_t (_hbuildprofil)

    mclSetCurrentValue_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'mclSetCurrentValue', ctypes.c_void_p, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mclSetCurrentValue(_hbuildprofil: ctypes.c_void_p, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Отобразить профиль в текущей точке
        
        :param _hbuildprofil: указатель открытого диалога построения профиля
        
        :param _point: координаты точки в метрах на контуре объекта, по которому построен профиль Функция отображает участок профиля, на котором находится данная точка и устанавливает в окна диалога вычисленные значения по данной точке.
        """
        return mclSetCurrentValue_t (_hbuildprofil, _point)

    mclBuildZoneVisibilityUn_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'mclBuildZoneVisibilityUn', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, ctypes.POINTER(maptype.TBUILDZONEVISIBILITY))
    def mclBuildZoneVisibilityUn(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _namersw: mapsyst.WTEXT, _zonevisibility: ctypes.POINTER(maptype.TBUILDZONEVISIBILITY)) -> int:
        """
        Построить зону видимости по матрице высот в виде растрового изображения
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _namersw: полное имя растра
        
        :param _zonevisibility: параметры построения зоны (описание в maptype.h) Построение производится при наличии открытой матрицы высот Результат записывается в файл namersw
        
        :returns: Возвращает номер растра в цепочке Вызов файла справки из mapscena (topic: zonviev) При ошибке возвращает ноль
        :rtype: int
        """
        return mclBuildZoneVisibilityUn_t (_hmap, _parm, _namersw.buffer(), _zonevisibility)

    mclShowHeight_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'mclShowHeight', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mclShowHeight(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Вызвать диалог отображения высоты в точке для всех открытых матриц
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _point: координаты точки в метрах Вызов файла справки из mapscena (topic: can)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mclShowHeight_t (_hmap, _parm, _point)

    scnChooseScaleEx_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_double,'scnChooseScaleEx', ctypes.c_double)
    def scnChooseScaleEx(_currentscale: float) -> float:
        """
        Установить масштаб отображения
        
        :param _currentscale: значение текущего масштаба
        
        :returns: Функция возвращает значение установленного масштаба При ошибке возвращает ноль
        :rtype: float
        """
        return scnChooseScaleEx_t (_currentscale)

    scnGetMapPassword_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'scnGetMapPassword', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def scnGetMapPassword(_mapname: mapsyst.WTEXT, _password: mapsyst.WTEXT, _size: int) -> int:
        """
        Вызвать диалог ввода пароля для доступа к карте
        
        :param _mapname: имя карты
        
        :param _password: буфер для размещения пароля
        
        :param _size: размер буфера в байтах для пароля
        
        :returns: При отказе возвращает 0, ``1`` - нормальное завершение
        :rtype: int
        """
        return scnGetMapPassword_t (_mapname.buffer(), _password.buffer(), _size)

    scnGetUnzipPassword_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'scnGetUnzipPassword', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def scnGetUnzipPassword(_zipname: mapsyst.WTEXT, _password: mapsyst.WTEXT, _size: int) -> int:
        """
        Вызвать диалог ввода пароля для распаковки архива
        
        :param _zipname: имя файла zip
        
        :param _password: буфер для размещения пароля
        
        :param _size: размер буфера в байтах для пароля
        
        :returns: Возвращает   ``0`` - отказ от ввода ``1`` - формируется пароль
        :rtype: int
        """
        return scnGetUnzipPassword_t (_zipname.buffer(), _password.buffer(), _size)

    mclPutRadiusZoneObject_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'mclPutRadiusZoneObject', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(BUILDZONEPARMEX))
    def mclPutRadiusZoneObject(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _zoneparm: ctypes.POINTER(BUILDZONEPARMEX)) -> int:
        """
        Вызвать диалог ввода параметров для построения зоны вокруг объекта
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _zoneparm: параметры построения зоны
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mclPutRadiusZoneObject_t (_hmap, _parm, _zoneparm)

    mclCreateStatisticObject_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_void_p,'mclCreateStatisticObject', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ)
    def mclCreateStatisticObject(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _hobj: maptype.HOBJ) -> ctypes.c_void_p:
        """
        Открыть диалог "Справка об объекте местности"
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _hobj: выбранный объект
        
        :returns: При ошибке возвращает ноль
        """
        return mclCreateStatisticObject_t (_hmap, _parm, _hobj)

    mclCloseStatisticObject_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'mclCloseStatisticObject', ctypes.c_void_p)
    def mclCloseStatisticObject(_hstat: ctypes.c_void_p) -> int:
        """
        Закрыть диалог "Справка об объекте местности"
        
        :param _hstat: идентификатор открытого диалога
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mclCloseStatisticObject_t (_hstat)

    mclChangeStatisticObject_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'mclChangeStatisticObject', ctypes.c_void_p, maptype.HOBJ)
    def mclChangeStatisticObject(_hstat: ctypes.c_void_p, _hobj: maptype.HOBJ) -> int:
        """
        Обновить диалог "Справка об объекте местности"
        
        :param _hstat: идентификатор открытого диалога
        
        :param _hobj: выбранный объект
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mclChangeStatisticObject_t (_hstat, _hobj)

    scnQuestion_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'scnQuestion', maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR)
    def scnQuestion(_title: mapsyst.WTEXT, _question: mapsyst.WTEXT, _docname: mapsyst.WTEXT, _button1: mapsyst.WTEXT, _button2: mapsyst.WTEXT, _button3: mapsyst.WTEXT, _button4: mapsyst.WTEXT, _button5: mapsyst.WTEXT, _button6: mapsyst.WTEXT) -> int:
        """
        Вызвать диалог Вопрос-Ответ
        
        :param _title: строка, содержащая заголовок
        
        :param _question: содержимое вопроса
        
        :param _docname: название документа
        
        :param _button1: название ``1``-ой кнопки
        
        :param _button2: название ``2``-ой кнопки
        
        :param _button3: название ``3``-ой кнопки
        
        :param _button4: название ``4``-ой кнопки
        
        :param _button5: название ``5``-ой кнопки
        
        :param _button6: название ``6``-ой кнопки Диалог имеет заголовок, в центре сам вопрос, под ним название документа и кнопки до ``6`` шт.
        
        :returns: Возвращает: ``1`` - нажата 1-я кнопка ``2`` - нажата 2-я кнопка ``3`` - нажата 3-я кнопка ``4`` - нажата 4-я кнопка ``5`` - нажата 5-я кнопка ``6`` - нажата 6-я кнопка При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если в качестве указателя на название кнопки передается NULL, то кнопка на форме не отображается
        """
        return scnQuestion_t (_title.buffer(), _question.buffer(), _docname.buffer(), _button1.buffer(), _button2.buffer(), _button3.buffer(), _button4.buffer(), _button5.buffer(), _button6.buffer())

    scnSetCopyOptionsEx_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'scnSetCopyOptionsEx', maptype.HWND, maptype.HMAP, ctypes.POINTER(COPY_OPTIONS))
    def scnSetCopyOptionsEx(_handle: maptype.HWND, _hmap: maptype.HMAP, _options: ctypes.POINTER(COPY_OPTIONS)) -> int:
        """
        Настроить параметры копирования объектов на другую карту
        
        :param _handle: идентификатор окна родителя
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _options: параметры копирования
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return scnSetCopyOptionsEx_t (_handle, _hmap, _options)

    scnLogTextDialog_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'scnLogTextDialog', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(maptype.RECT), ctypes.POINTER(ctypes.POINTER(maptype.WCHAR)), ctypes.POINTER(ctypes.c_int), ctypes.c_long)
    def scnLogTextDialog(_hMap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _position: ctypes.POINTER(maptype.RECT), _log_list: ctypes.POINTER(ctypes.POINTER(maptype.WCHAR)), _type_message: ctypes.POINTER(ctypes.c_int), _count: int) -> int:
        """
        Открыть журнал всплывающих сообщений приложения
        
        :param _hMap: идентификатор открытых данных (документа)
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _position: размеры диалога
        
        :param _log_list: список сообщений
        
        :param _type_message: тип сообщений
        
        :param _count: число сообщений в списке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return scnLogTextDialog_t (_hMap, _parm, _position, _log_list, _type_message, _count)

    scnRunningApplication_t = mapsyst.GetProcAddress(dlgslib,ctypes.c_long,'scnRunningApplication', ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def scnRunningApplication(_parm: ctypes.POINTER(maptype.TASKPARMEX), _path: mapsyst.WTEXT, _size: int, _comment: mapsyst.WTEXT, _commentsize: int) -> int:
        """
        Открыть диалог запуска приложений
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _path: буфер для записи строки, содержащей полный путь к запускаемой задаче
        
        :param _size: размер строки в байтах
        
        :param _comment: буфер для записи строки, содержащей комментарий к задаче
        
        :param _commentsize: размер строки в байтах
        
        :returns: При выборе задачи (библиотеки) возвращает 1, при ошибке возвращает ноль
        :rtype: int
        """
        return scnRunningApplication_t (_parm, _path.buffer(), _size, _comment.buffer(), _commentsize)



def gisdlgs_healthcheck():
    return 1
