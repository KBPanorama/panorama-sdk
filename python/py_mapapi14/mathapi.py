#!/usr/bin/env python3

"""
.. code-block:: none

    ********************************************************************
    *                                                                  *
    *              Copyright (c) PANORAMA Group 1991-2026              *
    *                     All Rights Reserved                          *
    *                                                                  *
    ********************************************************************
    *                                                                  *
    *            Описание функций обработки топологии данных           *
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
# Коды служебных объектов для сшивки объектов соседних листов

EXCODE_VERLINE = 1000000007  # Внешний код вертикальной линии
EXCODE_HORLINE = 1000000008  # Внешний код горизонтальной линии

# Коды объектов математической основы

EXCODE_MATHLINE_FIRST  = 13110000  # Начальный код объектов математической основы
EXCODE_MERIDIAN_LINE   = 13110000  # Линии меридианов
EXCODE_MERIDIAN_TICK   = 13111000  # Выходы линий меридианов
EXCODE_PARALLEL_LINE   = 13120000  # Линии параллелей
EXCODE_PARALLEL_TICK   = 13121000  # Выходы линий параллелей
EXCODE_VER_LINEGRID    = 13210000  # Вертикальные линии прямоугольной сетки
EXCODE_HOR_LINEGRID    = 13220000  # Горизонтальные линии прямоугольной сетки
EXCODE_VER_GRIDTICK    = 13230000  # Выходы вертикальных линий сетки смежной зоны
EXCODE_HOR_GRIDTICK    = 13240000  # Выходы горизонтальных линий сетки смежной зоны
EXCODE_VER_LINECROSS   = 13410000  # Вертикальные линии пересечений координатных линий
EXCODE_HOR_LINECROSS   = 13420000  # Горизонтальные линии пересечений координатных линий
EXCODE_MERIDIAN_STROKE = 13430000  # Штрихи линий меридианов
EXCODE_PARALLEL_STROKE = 13440000  # Штрихи линий параллелей
EXCODE_MATHLINE_LAST   = 13440000  # Последний код объектов математической основы
MARK_OVERLAP           = -19999  # Значение элемента MTW - пометка наложения горизонталей


#-----------------------------
class COMPLEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("re",ctypes.c_double),
                ("im",ctypes.c_double)]
#-----------------------------


#-----------------------------
class OBJECT_CROSSING(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Handle",maptype.HWND),
                ("Hovl",maptype.HOVL),
                ("Map",maptype.HMAP),
                ("Map2",maptype.HMAP),
                ("Site",maptype.HSITE),
                ("Site2",maptype.HSITE),
                ("Precision",ctypes.c_double),
                ("SheetNumber",ctypes.c_int),
                ("SheetNumber2",ctypes.c_int),
                ("ObjectNumber",ctypes.c_int),
                ("ExcludeKey",ctypes.c_int),
                ("Function",ctypes.c_int),
                ("CodeInside",ctypes.c_int),
                ("CodeOutside",ctypes.c_int),
                ("FlagForOne",ctypes.c_int),
                ("FlagSelfcrossing",ctypes.c_int),
                ("FlagTempletSubject",ctypes.c_int),
                ("Flag3d",ctypes.c_int),
                ("TempletNumber",ctypes.c_int),
                ("Report",ctypes.c_int),
                ("FlagAdjustTemplet",ctypes.c_int),
                ("Reserve",ctypes.c_char*(136)),
                ("SmallArea",ctypes.c_double)]
#-----------------------------


#-----------------------------
class PROCSETSPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Hobjlist1",maptype.HOBJLIST),
                ("Hobjlist2",maptype.HOBJLIST),
                ("Recordname1",maptype.WCHAR1*(512)),
                ("Recordname2",maptype.WCHAR1*(512)),
                ("Mode",ctypes.c_int),
                ("Transaction",ctypes.c_int),
                ("SquareCode",ctypes.c_int),
                ("LineCode",ctypes.c_int),
                ("Adjust",ctypes.c_int),
                ("Multi",ctypes.c_int),
                ("AdjustingRange",ctypes.c_double),
                ("RecordIdent",ctypes.c_int*(2)),
                ("Reserve",ctypes.c_char*(48))]
#-----------------------------


#-----------------------------
class ROUGH(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Precision",ctypes.c_double),
                ("Scatter",ctypes.c_double),
                ("PrecisionFlag",ctypes.c_long),
                ("ScatterFlag",ctypes.c_long)]
#-----------------------------


#-----------------------------
class GEN_CODESET(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Area",ctypes.c_int),
                ("Line1",ctypes.c_int),
                ("Line2",ctypes.c_int)]
#-----------------------------


#-----------------------------
class GEN_HYDROGRAPHY(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Handle",maptype.HMESSAGE),
                ("Map",maptype.HMAP),
                ("Select",maptype.HSELECT),
                ("SelectAdjust",maptype.HSELECT),
                ("SelectBound",maptype.HSELECT),
                ("SelectPond",maptype.HSELECT),
                ("Width1",ctypes.c_double),
                ("Width2",ctypes.c_double),
                ("Precision",ctypes.c_double),
                ("Distance",ctypes.c_double),
                ("MinLength",ctypes.c_double),
                ("MinArea",ctypes.c_double),
                ("MinWidth",ctypes.c_double),
                ("DirectionLength",ctypes.c_double),
                ("DirectionOffset",ctypes.c_double),
                ("SelectAlluvion",maptype.HSELECT),
                ("SelectSplitter",maptype.HSELECT),
                ("Reserve",ctypes.c_int*(35)),
                ("Code_WaterMark",ctypes.c_int),
                ("Code_Direction",ctypes.c_int),
                ("Code_ShoreLine",ctypes.c_int),
                ("Code_WaterLine",ctypes.c_int),
                ("Code_WaterBorder",ctypes.c_int),
                ("Code_WaterCover",ctypes.c_int),
                ("Code_Shallow",ctypes.c_int),
                ("Code_Pond",ctypes.c_int),
                ("Code_Bog",ctypes.c_int),
                ("Code_Reservoir",ctypes.c_int),
                ("Code_Aquaculture",ctypes.c_int)]
#-----------------------------


#-----------------------------
class LINEARTRANSFPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("a",ctypes.c_double),
                ("b",ctypes.c_double),
                ("c",ctypes.c_double),
                ("d",ctypes.c_double),
                ("e",ctypes.c_double),
                ("f",ctypes.c_double),
                ("A",ctypes.c_double),
                ("B",ctypes.c_double),
                ("C",ctypes.c_double),
                ("D",ctypes.c_double),
                ("E",ctypes.c_double),
                ("F",ctypes.c_double),
                ("Scale",ctypes.c_double),
                ("Rotate",ctypes.c_double)]
#-----------------------------


#-----------------------------
class CALCTRANSMERCATORPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("IsCalcM",ctypes.c_int),
                ("IsSetM",ctypes.c_int),
                ("M",ctypes.c_double),
                ("IsCalcLo",ctypes.c_int),
                ("IsSetLo",ctypes.c_int),
                ("Lo",ctypes.c_double),
                ("IsCalcBo",ctypes.c_int),
                ("IsSetBo",ctypes.c_int),
                ("Bo",ctypes.c_double),
                ("IsCalcDx",ctypes.c_int),
                ("IsSetDx",ctypes.c_int),
                ("Dx",ctypes.c_double),
                ("IsCalcDy",ctypes.c_int),
                ("IsSetDy",ctypes.c_int),
                ("Dy",ctypes.c_double),
                ("IsCalcAn",ctypes.c_int),
                ("IsSetAn",ctypes.c_int),
                ("An",ctypes.c_double)]
#-----------------------------


#-----------------------------
class OBJVALUE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Value",ctypes.c_double),
                ("Key",ctypes.c_uint),
                ("Color",ctypes.c_uint)]
#-----------------------------


#-----------------------------
class RANGEITEM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("RealName",maptype.WCHAR1*(512)),
                ("Min",ctypes.c_double),
                ("Max",ctypes.c_double),
                ("Color",ctypes.c_int),
                ("Step",ctypes.c_int),
                ("Thick",ctypes.c_int),
                ("Type",ctypes.c_int),
                ("Reserve",ctypes.c_int*(2))]
#-----------------------------


#-----------------------------
class THEMATICPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Hmap",maptype.HMAP),
                ("Hsite",maptype.HSITE),
                ("Handle",maptype.HMESSAGE),
                ("SelectBound",maptype.HSELECT),
                ("ResMapName",maptype.WCHAR1*(256)),
                ("LegendName",maptype.WCHAR1*(256)),
                ("ValueFieldType",ctypes.c_int),
                ("ValueSem",ctypes.c_int),
                ("ImageType",ctypes.c_int),
                ("ConnectType",ctypes.c_int),
                ("ItemsCount",ctypes.c_int),
                ("SearchMode",ctypes.c_int),
                ("Scale",ctypes.c_int),
                ("ContourColor",ctypes.c_int),
                ("ContourThick",ctypes.c_int),
                ("Transparent",ctypes.c_int),
                ("DiaFontHeight",ctypes.c_int),
                ("DiaLabelColor",ctypes.c_int),
                ("DiaShadowColor",ctypes.c_int),
                ("DiaCircleColor",ctypes.c_int),
                ("EmptyCreate",ctypes.c_int),
                ("LegendToDiagram",ctypes.c_int),
                ("MakeNumberCheck",ctypes.c_int),
                ("RecodeCheck",ctypes.c_int),
                ("LineCutCheck",ctypes.c_int),
                ("Precision",ctypes.c_int),
                ("NoPress",ctypes.c_int),
                ("SetScale",ctypes.c_int),
                ("HatchingBgColor",ctypes.c_int),
                ("HatchingColor",ctypes.c_int),
                ("PlaceX",ctypes.c_double),
                ("PlaceY",ctypes.c_double),
                ("LegendLabelColor",ctypes.c_int),
                ("LegendLabelShadowColor",ctypes.c_int),
                ("LegendBarWide",ctypes.c_int),
                ("LegendBarHeight",ctypes.c_int),
                ("LegendInterval",ctypes.c_int),
                ("LegendFontHeight",ctypes.c_int),
                ("LegendColCount",ctypes.c_int),
                ("LegendRecodeCheck",ctypes.c_int),
                ("RegionColCount",ctypes.c_int),
                ("FlagTerritory",ctypes.c_int),
                ("NameSem",ctypes.c_int),
                ("Reserve2",ctypes.c_int),
                ("RegionX",ctypes.c_double),
                ("RegionY",ctypes.c_double),
                ("Reserve",ctypes.c_int*(56))]
#-----------------------------


#-----------------------------
class THEMDIALOGPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("ConnectField",ctypes.c_char*(256)),
                ("ValueField",ctypes.c_char*(256)),
                ("ConnectFieldType",ctypes.c_int),
                ("ConnectSem",ctypes.c_int),
                ("IndexDelimiter",ctypes.c_int),
                ("LinesBegin",ctypes.c_int),
                ("NumberConnectField",ctypes.c_int),
                ("NumberValueField",ctypes.c_int),
                ("DataType",ctypes.c_int),
                ("CodeType",ctypes.c_int),
                ("NumberColorField",ctypes.c_int),
                ("Reserve1",ctypes.c_int),
                ("Delimiter",ctypes.c_int),
                ("Quote",ctypes.c_int),
                ("Reserve",ctypes.c_int*(4))]
#-----------------------------


#-----------------------------
class TEO_PARAM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Len_Limit",ctypes.c_double),
                ("Ds_Limit",ctypes.c_double),
                ("Da_Limit",ctypes.c_double),
                ("Da",ctypes.c_double),
                ("Dxy",ctypes.c_double),
                ("Sd",ctypes.c_double),
                ("ErrorCode",ctypes.c_long),
                ("Reserve",ctypes.c_long)]
#-----------------------------


#-----------------------------
class DIAOPTIONS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Hmap",maptype.HMAP),
                ("TempMap",maptype.HMAP),
                ("Hsite",maptype.HSITE),
                ("Houtsite",maptype.HSITE),
                ("Handle",maptype.HMESSAGE),
                ("ConnectType",ctypes.c_int),
                ("Typebase",ctypes.c_int),
                ("ValueType",ctypes.c_int),
                ("PercentType",ctypes.c_int),
                ("PercentCode",ctypes.c_int),
                ("SizeCode",ctypes.c_int),
                ("EmptyCreate",ctypes.c_int),
                ("OtherColor",ctypes.c_int),
                ("OtherValue",ctypes.c_double),
                ("ImageType",ctypes.c_int),
                ("Shadow",ctypes.c_int),
                ("ShadowColor",ctypes.c_int),
                ("ContourCreate",ctypes.c_int),
                ("ContourColor",ctypes.c_int),
                ("Ex3D",ctypes.c_int),
                ("GraphColor",ctypes.c_int),
                ("NetCheck",ctypes.c_int),
                ("NetColor",ctypes.c_int),
                ("AreaCheck",ctypes.c_int),
                ("IntegrCheck",ctypes.c_int),
                ("ExBorder",ctypes.c_int),
                ("ExBorderColor",ctypes.c_int),
                ("SizeColor",ctypes.c_int),
                ("ColWide",ctypes.c_double),
                ("ColInterval",ctypes.c_double),
                ("IsMakeLegend",ctypes.c_int),
                ("LegendType",ctypes.c_int),
                ("LegendColCount",ctypes.c_int),
                ("IsSizeLegend",ctypes.c_int),
                ("LegendRadius",ctypes.c_double),
                ("LegendBarWide",ctypes.c_double),
                ("LegendBarHeight",ctypes.c_double),
                ("LegendInterval",ctypes.c_double),
                ("ColorLegendX",ctypes.c_double),
                ("ColorLegendY",ctypes.c_double),
                ("SizeLegendX",ctypes.c_double),
                ("SizeLegendY",ctypes.c_double),
                ("LegendToDiagram",ctypes.c_int),
                ("ValueToDiagram",ctypes.c_int),
                ("PercToDiagram",ctypes.c_int),
                ("LegendLabelType",ctypes.c_int),
                ("LabelFromFill",ctypes.c_int),
                ("LegendLineColor",ctypes.c_int),
                ("LegendLabelColor",ctypes.c_int),
                ("LabelShadowCheck",ctypes.c_int),
                ("LabelShadowColor",ctypes.c_int),
                ("PlacePoint",ctypes.c_int),
                ("TopLabelScale",ctypes.c_int),
                ("BotLabelScale",ctypes.c_int),
                ("FontHeight",ctypes.c_double)]
#-----------------------------


#-----------------------------
class SEMANTICPARAM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Title",maptype.WCHAR1*(512)),
                ("Code",ctypes.c_int),
                ("Color",ctypes.c_int)]
#-----------------------------


#-----------------------------
class SIZEPARAM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("SizeType",ctypes.c_int),
                ("SizeScale",ctypes.c_int),
                ("Sizecount",ctypes.c_int),
                ("SizePrec",ctypes.c_int),
                ("FixSize",ctypes.c_double),
                ("MinRadius",ctypes.c_double),
                ("MaxRadius",ctypes.c_double)]
#-----------------------------




try:
    if os.environ['gismathdll']:
        gismathname = os.environ['gismathdll']
except KeyError:
    gismathname = 'gis64math.dll'

try:
    mathlib = mapsyst.LoadLibrary(gismathname)
except Exception as e:
    print(e)
    mathlib = 0

if mathlib == 0:
    print(gismathname)
else:
    mathTransformSubjectsToObject_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathTransformSubjectsToObject', maptype.HOBJ, maptype.HOBJ)
    def mathTransformSubjectsToObject(_inhobj: maptype.HOBJ, _outhobj: maptype.HOBJ) -> int:
        """
        Преобразовать объект и все его подобъекты в общий контур, с сохранением в объект
        
        :param _inhobj: входной объект
        
        :param _outhobj: сохраняемый объект Объект без подобъектов не обрабатывает
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathTransformSubjectsToObject_t (_inhobj, _outhobj)

    mathCutObjectToTriangles_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathCutObjectToTriangles', maptype.HOBJ, maptype.HOBJ)
    def mathCutObjectToTriangles(_inhobj: maptype.HOBJ, _outhobj: maptype.HOBJ) -> int:
        """
        Нарезать контур объекта на отдельные треугольники с размещением в объекте в виде составных частей
        
        :param _inhobj: входной объект
        
        :param _outhobj: сохраняемый объект в виде составных частей (объекта с подобъектами)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathCutObjectToTriangles_t (_inhobj, _outhobj)

    mathLineInterpolate_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathLineInterpolate', maptype.HOBJ, maptype.HOBJ, ctypes.c_double)
    def mathLineInterpolate(_inhobj: maptype.HOBJ, _outhobj: maptype.HOBJ, _step: float) -> int:
        """
        Выполнить интерполирование линии
        
        :param _inhobj: входной объект
        
        :param _outhobj: выходной объект
        
        :param _step: шаг в метрах Выполняет расстановку промежуточных точек на контуре с заданным шагом Для трехмерной метрики высота промежуточных точек запрашивается из матрицы при ее наличии
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathLineInterpolate_t (_inhobj, _outhobj, _step)

    mathGetObjectCenter_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathGetObjectCenter', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mathGetObjectCenter(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить центр площадного объекта
        
        :param _hmap: идентификатор открытых данных
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _x: расчитанная координата X центра объекта в метрах в системе документа
        
        :param _y: расчитанная координата Y центра объекта в метрах в системе документа Вызывает mapGetObjectCenter из mapapi.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathGetObjectCenter_t (_hmap, _hobj, _x, _y)

    mathSetLineLength_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathSetLineLength', ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_double, ctypes.c_long)
    def mathSetLineLength(_x1: ctypes.POINTER(ctypes.c_double), _y1: ctypes.POINTER(ctypes.c_double), _x2: ctypes.POINTER(ctypes.c_double), _y2: ctypes.POINTER(ctypes.c_double), _delta: float, _number: int) -> int:
        """
        Установить заданную длину отрезка между точками с исходными координатами x1,y1 и x2,y2
        
        :param _x1: координата X первой точки отрезка
        
        :param _y1: координата Y первой точки отрезка
        
        :param _x2: координата X второй точки отрезка
        
        :param _y2: координата Y второй точки отрезка
        
        :param _delta: новое расстояние
        
        :param _number: номер редактируемой точки (``1`` - изменяются x1 и y1, ``2`` - x2 и y2)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathSetLineLength_t (_x1, _y1, _x2, _y2, _delta, _number)

    mathSeekNormalInMap_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathSeekNormalInMap', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double)
    def mathSeekNormalInMap(_p1: ctypes.POINTER(maptype.DOUBLEPOINT), _p2: ctypes.POINTER(maptype.DOUBLEPOINT), _forwleft: ctypes.POINTER(maptype.DOUBLEPOINT), _forwright: ctypes.POINTER(maptype.DOUBLEPOINT), _backleft: ctypes.POINTER(maptype.DOUBLEPOINT), _backright: ctypes.POINTER(maptype.DOUBLEPOINT), _size: float) -> int:
        """
        Построить перпендикуляры к отрезку, заданному двумя точками p1 и p2
        
        :param _p1: координаты первой точки отрезка
        
        :param _p2: координаты второй точки отрезка
        
        :param _backleft: левый перепендикуляр от первой точки отрезка
        
        :param _backright: правый перепендикуляры от первой точки отрезка
        
        :param _forwleft: левый перепендикуляр от второй точки отрезка
        
        :param _forwright: правый перепендикуляр от второй точки отрезка
        
        :param _size: длина перпендикуляров в м Построения производятся в координатах карты, без пересчета длины с учетом проекции
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathSeekNormalInMap_t (_p1, _p2, _forwleft, _forwright, _backleft, _backright, _size)

    mathSheetFromFrameEx_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathSheetFromFrameEx', ctypes.POINTER(maptype.DFRAME), ctypes.c_long, ctypes.c_long, ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.c_long)
    def mathSheetFromFrameEx(_geoframe: ctypes.POINTER(maptype.DFRAME), _maptype: int, _scale: int, _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _listregcount: int) -> int:
        """
        Создать список номенклатур в стандартной международной разграфке по заданным габаритам
        
        :param _geoframe: габариты области построения номенклатур в радианах на эллипсоиде заданной системы координат
        
        :param _maptype: тип системы координат, для которой формируются номенклатуры (``CK_42``/``CK_95``, ``UTMWGS84``, ``GCK_2011``)
        
        :param _scale: знаменатель масштаба карты (``5 000`` - ``1 000 000``), для которого формируются номенклатуры
        
        :param _listreg: адрес для записи массива структур паспортных данных листа карты
        
        :param _listregcount: максимальное число записей, под которые выделена память В каждой структуре координаты будут в системе координат зоны номенклатуры При нормальном завершении заполнятся поля структуры ``LISTREGISTER`` для каждого листа
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathSheetFromFrameEx_t (_geoframe, _maptype, _scale, _listreg, _listregcount)

    mathGetGeoFrame_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathGetGeoFrame', maptype.HOBJ, ctypes.POINTER(maptype.DFRAME))
    def mathGetGeoFrame(_hobj: maptype.HOBJ, _geoframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Запросить габариты объекта в радианах в СК-42
        
        :param _hobj: объект, определяющий область интереса
        
        :param _geoframe: возвращаемые габариты объекта в радианах (x1,x2 - широта; y1,y2 - долгота)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathGetGeoFrame_t (_hobj, _geoframe)

    mathSetListRegisterEx_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathSetListRegisterEx', ctypes.c_char_p, ctypes.c_long, ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.c_long)
    def mathSetListRegisterEx(_nomenclature: ctypes.c_char_p, _size: int, _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _scale: int) -> int:
        """
        Заполнить поля структуры LISTREGISTER паспортных данных
        
        :param _nomenclature: номенклатура листа
        
        :param _size: размер строки с именем номенклатуры
        
        :param _listreg: адрес структуры паспортных данных листа карты
        
        :param _scale: знаменатель масштаба (``5000`` - ``1000000``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathSetListRegisterEx_t (_nomenclature, _size, _listreg, _scale)

    mathSetListRegister_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathSetListRegister', ctypes.c_char_p, ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.c_long, ctypes.c_long)
    def mathSetListRegister(_array: ctypes.c_char_p, _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _scale: int, _countname: int) -> int:
        """
        Заполнить поля массива структур LISTREGISTER
        
        :param _array: адрес списка номенклатур, рассчитанных по заданной области
        
        :param _listreg: адрес массива структур паспортных данных листа карты
        
        :param _scale: знаменатель масштаба (``25000`` - ``1000000``)
        
        :param _countname: число рассчитанных номенклатур
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathSetListRegister_t (_array, _listreg, _scale, _countname)

    mathSetMapRegister_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathSetMapRegister', ctypes.POINTER(mapcreat.MAPREGISTER), ctypes.c_long)
    def mathSetMapRegister(_mapreg: ctypes.POINTER(mapcreat.MAPREGISTER), _scale: int) -> int:
        """
        Заполнить структуры MAPREGISTER паспортных данных
        
        :param _mapreg: адрес структуры паспортных данных
        
        :param _scale: знаменатель масштаба (``5000`` - ``1000000``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathSetMapRegister_t (_mapreg, _scale)

    mathSetBelongNomenclature_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathSetBelongNomenclature', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.c_long)
    def mathSetBelongNomenclature(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _count: int) -> int:
        """
        Выполнить отбраковку номенклатур, не принадлежащих заданной области
        
        :param _hobj: заданная область построения листов карты
        
        :param _listreg: адрес массива структур паспортных данных листа карты в СК-``42``
        
        :param _count: число структур массива listreg
        
        :returns: Возвращает число рассчитанных номенклатур после отбраковки и удаляет лишние записи в массиве При ошибке возвращает ноль
        :rtype: int
        """
        return mathSetBelongNomenclature_t (_hmap, _hobj, _listreg, _count)

    mathGetRuleSheetNameUn_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathGetRuleSheetNameUn', ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.c_double, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mathGetRuleSheetNameUn(_maptype: int, _scale: int, _b: float, _l: float, _name: mapsyst.WTEXT, _namesize: int, _united: int) -> int:
        """
        Определить номенклатуру листа по масштабу и геодезическим координатам
        
        :param _maptype: тип карты
        
        :param _scale: масштаб карты (от ``1000`` ``000`` до ``2000``) b,l      - геодезические координаты точки внутри листа (в градусах)
        
        :param _name: номенклатура листа (буфер для размещения результата)
        
        :param _namesize: размер буфера в байтах
        
        :param _united: признак объединенного листа: ``0`` - одинарные листы; ``1`` - сдвоенные, строенные, счетверенные
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathGetRuleSheetNameUn_t (_maptype, _scale, _b, _l, _name.buffer(), _namesize, _united)

    mathGetNomenclatureListFromAreaPro_t = mapsyst.GetProcAddress(mathlib,ctypes.c_void_p,'mathGetNomenclatureListFromAreaPro', ctypes.POINTER(maptype.DFRAME), ctypes.c_long, maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p))
    def mathGetNomenclatureListFromAreaPro(_dframe: ctypes.POINTER(maptype.DFRAME), _scale: int, _hevent: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p)) -> ctypes.c_void_p:
        """
        Запросить список номенклатур для топографической карты  в стандартной разграфке листов
        
        :param _dframe: заданные габариты района в радианах (границы района по долготе от ``-3.141592`` до ``3.141592`` радиан, по широте от -``1``,``46608`` до ``1``,``46608``)
        
        :param _scale: масштаб карты (от ``5 000`` до ``1 000 000``)
        
        :param _hevent: адрес функции обратного вызова для получения уведомлений о проценте загруженных данных (для посылки сообщений о выполнении ``WM_LIST``) ``LPARAM`` >``= 0``  - суммарное число номенклатурных листов ``WPARAM`` >``= 0``  - порядковый номер текущего обработанного номенклатурного листа Топографические карты: СК-``42``, СК-``95``, ``GCK_2011``, ``UTM`` В основу обозначения листов топографических карт любого масштаба положена номенклатура листов карты ``1 : 1 000 000``, которая имеет вид ``0``.X-``YY`` для северного полушария и ``1``.X-``YY`` для южного полушария; X - буква латинского алфавита от А до V для указания ряда, ``YY`` - цифры для указания колонки от ``01`` до ``60`` (колонки с номерами от ``01`` до ``30`` служат для обозначения западного полушария, от ``31`` до ``60`` - для обозначения восточного полушария) Для масштаба ``1 : 500 000`` на район севернее ``60`` ° с.ш. и южнее ``60`` ° ю.ш. листы сдвоены Для масштаба ``1 : 200 000`` на район севернее ``60`` ° с.ш. и южнее ``60`` ° ю.ш. листы сдвоены, севернее ``76`` ° с.ш. и южнее ``76`` ° ю.ш. строены Для масштабов от ``1 : 100 000`` до ``1 : 5 000`` на район севернее ``60`` ° с.ш. и южнее ``60`` ° ю.ш. листы сдвоены, на район севернее ``76`` ° с.ш. и южнее ``76`` ° ю.ш. счетверены
        
        :returns: Возвращает идентификатор списка номенклатур При ошибке возвращает ноль
        """
        return mathGetNomenclatureListFromAreaPro_t (_dframe, _scale, _hevent, _eventparam)

    mathGetNomenclatureAddr_t = mapsyst.GetProcAddress(mathlib,ctypes.POINTER(ctypes.POINTER(maptype.WCHAR)),'mathGetNomenclatureAddr', ctypes.c_void_p, ctypes.POINTER(ctypes.c_long))
    def mathGetNomenclatureAddr(_hnomen: ctypes.c_void_p, _nomencount: ctypes.POINTER(ctypes.c_long)) -> ctypes.POINTER(ctypes.POINTER(maptype.WCHAR)):
        """
        Получить адрес списка номенклатур
        
        :param _hnomen: идентификатор списка номенклатур (создан функцией mathGetNomenclatureListFromArea)
        
        :param _nomencount: адрес поля для записи числа элементов в списке номенклатур
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.POINTER(maptype.WCHAR))
        """
        return mathGetNomenclatureAddr_t (_hnomen, _nomencount)

    mathGetNomenclature_t = mapsyst.GetProcAddress(mathlib,ctypes.POINTER(maptype.WCHAR),'mathGetNomenclature', ctypes.c_void_p, ctypes.c_long)
    def mathGetNomenclature(_hnomen: ctypes.c_void_p, _nomnumber: int) -> ctypes.POINTER(maptype.WCHAR):
        """
        Получить номенклатуру листа по номеру в списке
        
        :param _hnomen: идентификатор списка номенклатур (создан функцией mathGetNomenclatureListFromArea)
        
        :param _nomnumber: номер записи в списке, начиная с ``1``
        
        :returns: Возвращает строку с номенклатурой листа При ошибке возвращает ноль
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mathGetNomenclature_t (_hnomen, _nomnumber)

    mathFreeNomenclatureList_t = mapsyst.GetProcAddress(mathlib,ctypes.c_void_p,'mathFreeNomenclatureList', ctypes.c_void_p)
    def mathFreeNomenclatureList(_hnomen: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Удалить список номенклатур
        
        :param _hnomen: идентификатор списка номенклатур
        """
        return mathFreeNomenclatureList_t (_hnomen)

    mathObjectCrossing_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathObjectCrossing', maptype.HOBJ, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(OBJECT_CROSSING))
    def mathObjectCrossing(_templet: maptype.HOBJ, _count: int, _codes: ctypes.POINTER(ctypes.c_long), _parm: ctypes.POINTER(OBJECT_CROSSING)) -> int:
        """
        Выполнить обработку пересечений объектов карты
        
        :param _templet: объект-шаблон (лекало) для обрезки объектов
        
        :param _count: количество типов (кодов) обрезаемых объектов
        
        :param _codes: массив кодов обрезаемых объектов: mapGetRscObjectCodeByKey() (если коды не заданы - обработать все объекты)
        
        :param _parm: параметры обработки Функция выполняет задачи: - обрезка объектов карты заданных типов по шаблону (обрезка фрагментов внутри или снаружи шаблона) - разрезание объектов карты заданных типов по шаблону (с сохранением исходного вида разрезаемых объектов, либо с назначением новых видов); - создание линейных объектов, определяющих совпадающие контура (создание границ между площадными объектами)
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mathObjectCrossing_t (_templet, _count, _codes, _parm)

    mathObjectCopyingEx_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathObjectCopyingEx', maptype.HWND, maptype.HMAP, ctypes.c_long, maptype.HMAP, ctypes.c_long, maptype.HSELECT)
    def mathObjectCopyingEx(_handle: maptype.HWND, _mapin: maptype.HMAP, _numberin: int, _mapout: maptype.HMAP, _numberout: int, _hselect: maptype.HSELECT) -> int:
        """
        Копировать объекты листа с одной карты на лист карты производного масштаба
        
        :param _handle: диалог визуального сопровождения процесса обработки
        
        :param _mapin: исходная карта
        
        :param _numberin: номер листа, на котором расположен объект
        
        :param _mapout: выходная карта
        
        :param _numberout: номер листа, на который переносится объект
        
        :param _hselect: фильтр копируемых объектов (если ``0``, то копируются все объекты) Диалогу визуального сопровождения процесса обработки посылаются сообщения: ``WM_PROGRESSBAR`` извещение об изменении состояния процесса ``WPARAM`` - текущее состояние процесса в процентах (``0````%`` - ``100````%``)
        
        :returns: Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается Используется при выполнении первого этапа генерализации карты При ошибке возвращает ноль
        :rtype: int
        """
        return mathObjectCopyingEx_t (_handle, _mapin, _numberin, _mapout, _numberout, _hselect)

    mathObjectJoiningEx_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathObjectJoiningEx', maptype.HWND, maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_double)
    def mathObjectJoiningEx(_handle: maptype.HWND, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _number: int, _delta: float) -> int:
        """
        Сшить объекты вдоль линии сводки
        
        :param _handle: диалог визуального сопровождения процесса обработки
        
        :param _hmap: исходная основная карта
        
        :param _hsite: исходная пользовательская карта
        
        :param _number: номер листа карты
        
        :param _delta: допуск при дотягивании (в метрах) Диалогу визуального сопровождения процесса обработки посылаются сообщения: ``WM_PROGRESSBAR`` извещение об изменении состояния процесса ``WPARAM`` - текущее состояние процесса в процентах (``0````%`` - ``100````%``)
        
        :returns: Если функция-отклик возвращает WM_PROGRESSBAR, то процесс завершается При ошибке возвращает ноль
        :rtype: int
        """
        return mathObjectJoiningEx_t (_handle, _hmap, _hsite, _number, _delta)

    mathDissembleUn_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathDissembleUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(ROUGH), maptype.HMESSAGE)
    def mathDissembleUn(_hmap: maptype.HMAP, _keyfile: mapsyst.WTEXT, _rough: ctypes.POINTER(ROUGH), _handle: maptype.HMESSAGE) -> int:
        """
        Выполнить генерализацию опорных пунктов
        
        :param _hmap: исходная карта
        
        :param _keyfile: имя ini-файла
        
        :param _rough: параметры обработки
        
        :param _handle: диалог визуального сопровождения процесса обработки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathDissembleUn_t (_hmap, _keyfile.buffer(), _rough, _handle)

    mathIsolineGeneralizationUn_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathIsolineGeneralizationUn', maptype.HMAP, maptype.PWCHAR, maptype.HMESSAGE)
    def mathIsolineGeneralizationUn(_hmap: maptype.HMAP, _txtname: mapsyst.WTEXT, _handle: maptype.HMESSAGE) -> int:
        """
        Выполнить генерализацию изолиний рельефа
        
        :param _hmap: исходная карта
        
        :param _txtname: полное имя ini-файла
        
        :param _handle: диалог визуального сопровождения процесса обработки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathIsolineGeneralizationUn_t (_hmap, _txtname.buffer(), _handle)

    genHydrography_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'genHydrography', ctypes.POINTER(GEN_HYDROGRAPHY), ctypes.POINTER(GEN_CODESET), ctypes.c_long)
    def genHydrography(_parm: ctypes.POINTER(GEN_HYDROGRAPHY), _codeset: ctypes.POINTER(GEN_CODESET), _setcount: int) -> int:
        """
        Генерализация площадной гидрографии
        
        :param _parm: параметры генерализации
        
        :param _codeset: массив наборов кодов
        
        :param _setcount: число наборов кодов (от ``1`` до ``RIVER_KIND_MAX``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return genHydrography_t (_parm, _codeset, _setcount)

    mapCreateEquations_t = mapsyst.GetProcAddress(mathlib,ctypes.c_void_p,'mapCreateEquations', ctypes.c_long, ctypes.c_long)
    def mapCreateEquations(_size: int, _ismhk: int) -> ctypes.c_void_p:
        """
        Создать систему нормальных уравнений
        
        :param _size: количество неизвестных
        
        :param _ismhk: ``1`` - количество уравнений больше количества неизвестных ``0`` - количество уравнений равно количеству неизвестных Для каждого полученного и больше не используемого идентификатора необходим вызов функции mapFreeEquations()
        
        :returns: Возвращает идентификатор системы уравнений При ошибке возвращает ноль
        """
        return mapCreateEquations_t (_size, _ismhk)

    mapFreeEquations_t = mapsyst.GetProcAddress(mathlib,ctypes.c_void_p,'mapFreeEquations', ctypes.c_void_p)
    def mapFreeEquations(_hequations: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Освободить идентификатор системы нормальных уравнений
        
        :param _hequations: идентификатор системы уравнений
        """
        return mapFreeEquations_t (_hequations)

    mapAddEquation_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mapAddEquation', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double))
    def mapAddEquation(_hequations: ctypes.c_void_p, _equation: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Добавить уравнение в систему нормальных уравнений
        
        :param _hequations: идентификатор системы уравнений
        
        :param _equation: коэффициенты уравнения длина = size + ``1`` (коэффициенты уравнения + остаток)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapAddEquation_t (_hequations, _equation)

    mapSolve_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mapSolve', ctypes.c_void_p)
    def mapSolve(_hequations: ctypes.c_void_p) -> int:
        """
        Решить систему уравнений
        
        :param _hequations: идентификатор системы уравнений Перед вызовом система должна быть заполнена mapAddEquation
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSolve_t (_hequations)

    mapGetResult_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mapGetResult', ctypes.c_void_p, ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def mapGetResult(_hequations: ctypes.c_void_p, _num: int, _value: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Вернуть результат решения системы нормальных уравнений
        
        :param _hequations: идентификатор системы уравнений
        
        :param _num: номер неизвестного (от ``0`` до size - ``1``)
        
        :param _value: возвращаемое значение Перед вызовом система должна быть решена mapSolve
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetResult_t (_hequations, _num, _value)

    mapCreateTransform_t = mapsyst.GetProcAddress(mathlib,ctypes.c_void_p,'mapCreateTransform', ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int)
    def mapCreateTransform(_count: int, _pointsin: ctypes.POINTER(maptype.DOUBLEPOINT), _pointsout: ctypes.POINTER(maptype.DOUBLEPOINT), _transftype: int) -> ctypes.c_void_p:
        """
        Создать класс трансформирования координат
        
        :param _count: количество точек для расчета параметров трансформирования
        
        :param _pointsin: координаты точек в исходной системе координат
        
        :param _pointsout: координаты точек в выходной системе координат
        
        :param _transftype: тип линейного трансформирования: ``LT_OFFSET`` - преобразование сдвиг X = x0 + x Y = y0 + y ``LT_OFFSETROTATE`` - преобразование сдвиг, поворот X = x0 + x ``*`` cos - y ``*`` sin Y = y0 + x ``*`` sin + y ``*`` cos ``LT_OFFSETROTATESCALE`` - преобразование масштаб, сдвиг, поворот X = x0 + x ``*`` cos ``*`` m - y ``*`` sin ``*`` m Y = y0 + x ``*`` sin ``*`` m + y ``*`` cos ``*`` m ``LT_AFFINE`` - аффинное трансформирование (полином ``1`` степени) X = a + x ``*`` b + y ``*`` c Y = d + x ``*`` e + y ``*`` f В зависимости от типа трансформирования: ``LT_OFFSET`` - минимальное количество точек ``= 1`` ``LT_OFFSETROTATE``, ``LT_OFFSETROTATESCALE`` - минимальное количество точек ``= 2`` ``LT_AFFINE`` - минимальное количество точек ``= 3`` Для каждого полученного и больше не используемого идентификатора необходим вызов функции mapFreeTransform()
        
        :returns: Возвращает идентификатор класса трансформирования координат При ошибке возвращает ноль
        """
        return mapCreateTransform_t (_count, _pointsin, _pointsout, _transftype)

    mapFreeTransform_t = mapsyst.GetProcAddress(mathlib,ctypes.c_void_p,'mapFreeTransform', ctypes.c_void_p)
    def mapFreeTransform(_htransf: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Освободить класс трансформирования координат
        
        :param _htransf: идентификатор класса трансформирования координат
        """
        return mapFreeTransform_t (_htransf)

    mapTransformIn2Out_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mapTransformIn2Out', ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapTransformIn2Out(_htransf: ctypes.c_void_p, _xin: float, _yin: float, _xout: ctypes.POINTER(ctypes.c_double), _yout: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Трансформировать координаты из исходной системы координат в выходную
        
        :param _htransf: идентификатор класса трансформирования координат xin, yin   - координаты в исходной системе координат xout, yout - вычисленные координаты в выходной системе координат
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapTransformIn2Out_t (_htransf, _xin, _yin, _xout, _yout)

    mapTransformOut2In_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mapTransformOut2In', ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapTransformOut2In(_htransf: ctypes.c_void_p, _xout: float, _yout: float, _xin: ctypes.POINTER(ctypes.c_double), _yin: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Трансформировать координаты из выходной системы координат в исходную
        
        :param _htransf: идентификатор класса трансформирования координат xout, yout - координаты в выходной системе координат xin, yin   - вычисленные координаты в исходной системе координат
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapTransformOut2In_t (_htransf, _xout, _yout, _xin, _yin)

    mapGetTransformParam_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mapGetTransformParam', ctypes.c_void_p, ctypes.POINTER(LINEARTRANSFPARM))
    def mapGetTransformParam(_htransf: ctypes.c_void_p, _parm: ctypes.POINTER(LINEARTRANSFPARM)) -> int:
        """
        Запросить вычисленные параметры траснформирования
        
        :param _htransf: идентификатор класса трансформирования координат
        
        :param _parm: параметры траснформирования
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetTransformParam_t (_htransf, _parm)

    mapCreateNonlineTransform_t = mapsyst.GetProcAddress(mathlib,ctypes.c_void_p,'mapCreateNonlineTransform', ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DFRAME), ctypes.c_long, ctypes.c_int)
    def mapCreateNonlineTransform(_count: int, _pointsin: ctypes.POINTER(maptype.DOUBLEPOINT), _pointsout: ctypes.POINTER(maptype.DOUBLEPOINT), _interestframe: ctypes.POINTER(maptype.DFRAME), _virtualpointcount: int, _transftype: int) -> ctypes.c_void_p:
        """
        Создать класс нелинейного трансформирования координат
        
        :param _count: количество точек для расчета параметров трансформирования
        
        :param _pointsin: координаты точек в исходной системе координат
        
        :param _pointsout: координаты точек в выходной системе координат
        
        :param _interestframe: область интереса - прямоугольник, ограничивающий область применения функции mapNonlineTransformIn2Out если ``= 0``, то экстраполяция искажений вне области расположения опорных точек не выполняется, в этом случае virtualpointcount должно быть равно ``0``
        
        :param _virtualpointcount: количество виртуальных точек, добавляемых по границе области интереса минимальное количество ``= 4`` если interestframe ``= 0``, то virtualpointcount должно быть равно ``0``
        
        :param _transftype: тип нелинейного трансформирования, описан в ``NONLINEARTRANSFTYPE`` В зависимости от типа трансформирования: ``NT_LINEARSHEET``, ``NT_NONLINEARSHEET`` - минимальное количество точек ``= 3`` ``NT_POLYNOM`` - минимальное количество точек = количеству коэффициентов ``NT_POLYNOMRANK2`` - минимальное количество точек ``= 6`` ``NT_POLYNOMRANK3`` - минимальное количество точек ``= 10`` ``NT_POLYNOMRANK4`` - минимальное количество точек ``= 15`` ``NT_POLYNOMRANK5`` - минимальное количество точек ``= 21`` Для каждого полученного и больше не используемого идентификатора необходим вызов функции mapFreeNonlineTransform()
        
        :returns: Возвращает идентификатор класса нелинейного трансформирования координат При ошибке возвращает ноль
        """
        return mapCreateNonlineTransform_t (_count, _pointsin, _pointsout, _interestframe, _virtualpointcount, _transftype)

    mapFreeNonlineTransform_t = mapsyst.GetProcAddress(mathlib,ctypes.c_void_p,'mapFreeNonlineTransform', ctypes.c_void_p)
    def mapFreeNonlineTransform(_htransf: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Освободить класс нелинейного трансформирования координат
        
        :param _htransf: идентификатор класса трансформирования координат
        """
        return mapFreeNonlineTransform_t (_htransf)

    mapNonlineTransformIn2Out_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mapNonlineTransformIn2Out', ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapNonlineTransformIn2Out(_htransf: ctypes.c_void_p, _xin: float, _yin: float, _xout: ctypes.POINTER(ctypes.c_double), _yout: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Нелинейное трансформирование координат из исходной системы координат в выходную
        
        :param _htransf: идентификатор класса трансформирования координат xin, yin   - координаты в исходной системе координат xout, yout - вычисленные координаты в выходной системе координат
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapNonlineTransformIn2Out_t (_htransf, _xin, _yin, _xout, _yout)

    mapNonlineTransformGetVirtualPoints_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mapNonlineTransformGetVirtualPoints', ctypes.c_void_p, ctypes.POINTER(ctypes.POINTER(maptype.DOUBLEPOINT)), ctypes.POINTER(ctypes.POINTER(maptype.DOUBLEPOINT)))
    def mapNonlineTransformGetVirtualPoints(_htransf: ctypes.c_void_p, _virtualpointsin: ctypes.POINTER(ctypes.POINTER(maptype.DOUBLEPOINT)), _virtualpointsout: ctypes.POINTER(ctypes.POINTER(maptype.DOUBLEPOINT))) -> int:
        """
        Запросить координаты виртуальных точек
        
        :param _htransf: идентификатор класса трансформирования координат
        
        :returns: virtualpointsin  - в irtualpointsin возвращается указатель на массив виртуальных точек в исходной СК virtualpointsout - в virtualpointsou возвращается указатель на массив виртуальных точек в выходной СК Возвращает координаты виртуальных точек Возвращает количество виртуальных точек, если возвращает 0, то виртуальных точек нет При ошибке возвращает ноль
        :rtype: int
        """
        return mapNonlineTransformGetVirtualPoints_t (_htransf, _virtualpointsin, _virtualpointsout)

    mapCalculateDatumEx_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mapCalculateDatumEx', ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.XYHDOUBLE), ctypes.POINTER(maptype.XYHDOUBLE), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapCalculateDatumEx(_iscalcoffset: int, _iscalcrotate: int, _iscalcscale: int, _pointcount: int, _points: ctypes.POINTER(maptype.XYHDOUBLE), _wgspoints: ctypes.POINTER(maptype.XYHDOUBLE), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        """
        Вычислить датум
        
        :param _iscalcoffset: признак вычисления линейных коэффициентов смещения
        
        :param _iscalcrotate: признак вычисления угловых коэффициентов вращения
        
        :param _iscalcscale: признак вычисления масштабного коэффициента
        
        :param _pointcount: количество точек
        
        :param _points: геодезические координаты точек на эллипсоиде ellipsoid b, l, h - широта (радианы), долгота (радианы), эллипсоидальная высота (метры)
        
        :param _wgspoints: геодезические координаты точек на ``WGS84`` b, l, h - широта (радианы), долгота (радианы), эллипсоидальная высота (метры)
        
        :param _ellipsoid: эллипсоид СК, для которой вычисляется датум
        
        :param _datum: вычисленный датум
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCalculateDatumEx_t (_iscalcoffset, _iscalcrotate, _iscalcscale, _pointcount, _points, _wgspoints, _ellipsoid, _datum)

    mapCalculateTransverseMercatorParam_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mapCalculateTransverseMercatorParam', ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(CALCTRANSMERCATORPARM))
    def mapCalculateTransverseMercatorParam(_pointcount: int, _blpoints: ctypes.POINTER(maptype.DOUBLEPOINT), _xypoints: ctypes.POINTER(maptype.DOUBLEPOINT), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _parm: ctypes.POINTER(CALCTRANSMERCATORPARM)) -> int:
        """
        Вычислить параметры местной системы координат по набору точек
        
        :param _pointcount: количество точек
        
        :param _blpoints: геодезические координаты точек:  b, l - широта (радианы), долгота (радианы)
        
        :param _xypoints: прямоугольные координаты точек в местной системе координат система координат левая, координаты в метрах
        
        :param _ellipsoid: используемый эллипсоид
        
        :param _parm: вычисляемые параметры проекции (описание в  mathapi.h) Проекция Transverse Mercator + поворот Вычисляются : - масштаб на осевом меридиане - долгота осевого меридиана - широта точки отсчета - поправка по Х - поправка по Y - угол поворота местной системы координат
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCalculateTransverseMercatorParam_t (_pointcount, _blpoints, _xypoints, _ellipsoid, _parm)

    mapFourierTransform_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mapFourierTransform', ctypes.POINTER(COMPLEX), ctypes.c_long, ctypes.c_long)
    def mapFourierTransform(_x: ctypes.POINTER(COMPLEX), _count: int, _isdirect: int) -> int:
        """
        Выполнить преобразование Фурье (дискретное быстрое + модификация для произвольного count)
        
        :param _x: массив комплексных чисел
        
        :param _count: размер массива x isdirect ``= 1`` - прямое преобразование Фурье ``= 0`` - обратное преобразование Фурье Для прямого преобразования Фурье: - на входе  - массив измерений Обычно измерения являются действительными числами, в этом случае значение измерения заносится в x.re, в x.im заносится ``0`` - на выходе - массив гармоник (комплексное число) Частота гармоники V = i / T, где i - номер гармоники (от ``1``, в ``0`` среднее значение ``*`` count) T - СУММАРНОЕ время измерения Амплитуда гармоники A = sqrt(x[i].re^``2`` + x[i].im^``2``) / count Фаза гармоники      F = atan2(x[i].im, x[i].re) Для обратного преобразования Фурье: - на входе  - массив гармоник (комплексное число) Обычно измерения являются действительными числами, в этом случае значение измерения заносится в x.re, в x.im заносится ``0`` - на выходе - массив измерений (брать действительную часть) График спектра симметричен относительно центра графика, поэтому обычно график рисуют для ``1`` <= i < count / ``2``, в этом случае амплитуду умножают на ``2``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapFourierTransform_t (_x, _count, _isdirect)

    mathMapProcessing_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathMapProcessing', maptype.HMESSAGE, maptype.HMAP, maptype.HSITE, maptype.PWCHAR)
    def mathMapProcessing(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _xmlpath: mapsyst.WTEXT) -> int:
        """
        Выполнить обработку карты
        
        :param _handle: диалог визуального сопровождения процесса обработки.
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: исходная пользовательская карта
        
        :param _xmlpath: xml-файл с параметрами обработки объектов Для обработки всей карты необходимо hsite ``= 0`` Перечень обрабатываемых процессов: - уточнение рамки листа; - ориентирование векторных знаков вдоль линейных (могут быть и площадные); - заполнение семантики ``"Расстояние до ближайшего объекта"``. Диалогу визуального сопровождения процесса обработки посылаются сообщения: ``WM_PROGRESSBARUN`` извещение об изменении состояния процесса ``WPARAM`` - текущее состояние процесса в процентах (``0````%`` - ``100````%``)
        
        :returns: Если функция-отклик возвращает WM_PROGRESSBARUN, то процесс завершается. При ошибке возвращает ноль
        :rtype: int
        """
        return mathMapProcessing_t (_handle, _hmap, _hsite, _xmlpath.buffer())

    mathCountProcessing_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathCountProcessing', maptype.PWCHAR)
    def mathCountProcessing(_xmlpath: mapsyst.WTEXT) -> int:
        """
        Запросить количество процессов в xml-файле
        
        :param _xmlpath: xml-файл с параметрами обработки объектов Вызывается перед задачей mathMapProcessing
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathCountProcessing_t (_xmlpath.buffer())

    mathGetObjectProcessing_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathGetObjectProcessing')
    def mathGetObjectProcessing() -> int:
        """
        Запросить метод обработки генерализированных объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathGetObjectProcessing_t ()

    mathSetObjectProcessing_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathSetObjectProcessing', ctypes.c_long)
    def mathSetObjectProcessing(_process_flag: int) -> int:
        """
        Установить метод обработки генерализированных объектов
        
        :param _process_flag: метод обработки: ``0`` - добавление в объект семантики ``SEMIMAGECOLOR`` ``1`` - удаление объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathSetObjectProcessing_t (_process_flag)

    mathSetMapRealBorder_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathSetMapRealBorder', maptype.HMESSAGE, maptype.HMAP)
    def mathSetMapRealBorder(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP) -> int:
        """
        Уточнить восточные и западные рамки листов в соответствии с реальными габаритами объектов в листе
        
        :param _handle: диалог визуального сопровождения процесса обработки
        
        :param _hmap: идентификатор открытых данных Диалогу визуального сопровождения процесса обработки посылаются сообщения: -  (``WM_PROGRESSBARUN``) Извещение об изменении состояния процесса ``WPARAM`` - текущее состояние процесса в процентах (``0````%`` - ``100````%``)
        
        :returns: Если функция-отклик возвращает WM_PROGRESSBARUN, то процесс завершается Уточняется при несоответствии более чем на 10" При ошибке возвращает ноль
        :rtype: int
        """
        return mathSetMapRealBorder_t (_handle, _hmap)

    mathCreatePassagesBetweenQuarters_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathCreatePassagesBetweenQuarters', maptype.HMESSAGE, maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long))
    def mathCreatePassagesBetweenQuarters(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP, _ininame: mapsyst.WTEXT, _code: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Создать проезды между кварталами
        
        :param _handle: идентификатор окна (для посылки сообщений о выполнении ``WM_PROGRESSBARUN``) ``LPARAM`` >``= 0``  - процент выполнения ``WPARAM`` ``= -1``  - комментарий (имя текущего процесса)
        
        :param _hmap: идентификатор открытых данных
        
        :param _ininame: имя файла параметров (ist)
        
        :param _code: поле для возврата кода ошибки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathCreatePassagesBetweenQuarters_t (_handle, _hmap, _ininame.buffer(), _code)

    mathGetObjectLargestSegment_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathGetObjectLargestSegment', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long)
    def mathGetObjectLargestSegment(_hobj: maptype.HOBJ, _point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT), _subject: int) -> int:
        """
        Запросить наибольший отрезок метрики объекта
        
        :param _hobj: обрабатываемый объект
        
        :param _subject: номер подобъекта
        
        :param _point1: первая точка отрезка
        
        :param _point2: вторая точка отрезка Обрабатываются линейные и площадные объекты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathGetObjectLargestSegment_t (_hobj, _point1, _point2, _subject)

    mathGetPointPositionByDistance_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathGetPointPositionByDistance', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double)
    def mathGetPointPositionByDistance(_hmap: maptype.HMAP, _firstpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _lastpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _distance: float) -> int:
        """
        Определить координаты точки на расстоянии от первой точки в метрах на местности
        
        :param _hmap: идентификатор открытых данных
        
        :param _firstpoint: первая точка отрезка
        
        :param _lastpoint: вторая точка отрезка
        
        :param _distance: расстояние от первой точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathGetPointPositionByDistance_t (_hmap, _firstpoint, _lastpoint, _distance)

    mathGetMaxVectorObjectSize_t = mapsyst.GetProcAddress(mathlib,ctypes.c_double,'mathGetMaxVectorObjectSize', maptype.HOBJ)
    def mathGetMaxVectorObjectSize(_hobj: maptype.HOBJ) -> float:
        """
        Запросить максимальный размер векторного объекта в метрах на местности
        
        :param _hobj: обрабатываемый объект
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mathGetMaxVectorObjectSize_t (_hobj)

    mathCalcLinearInterHeights_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathCalcLinearInterHeights', maptype.HOBJ, ctypes.c_int)
    def mathCalcLinearInterHeights(_hobj: maptype.HOBJ, _fixslope: int) -> int:
        """
        Выполнить расчёт неустановленных высот и исправить наклон линейного объекта гидрографии методом линейной интерполяции
        
        :param _hobj: обрабатываемый линейный объект с трёхмерной метрикой
        
        :param _fixslope: режим исправления наклона объекта для плавного убывания высот (описан в ``FIXSLOPEMODES``) Высота ``ERRORHEIGHT`` в точках, которые находятся между соседними точками, имеющими высоту, будет пересчитана методом линейной интерполяции Высота ``ERRORHEIGHT`` в точках, которые находятся до первой или после последней точки, имеющей высоту, будет заменена на высоту в первой и последней точке с заданной высотой соответственно
        
        :returns: При успешном выполнении возвращает количество обработанных контуров При ошибке возвращает ноль
        :rtype: int
        """
        return mathCalcLinearInterHeights_t (_hobj, _fixslope)

    mathCreateThematicMap_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathCreateThematicMap', maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(THEMATICPARM), ctypes.POINTER(RANGEITEM), ctypes.POINTER(OBJVALUE), ctypes.c_int)
    def mathCreateThematicMap(_sitename: mapsyst.WTEXT, _legendname: mapsyst.WTEXT, _options: ctypes.POINTER(THEMATICPARM), _values: ctypes.POINTER(RANGEITEM), _objvalue: ctypes.POINTER(OBJVALUE), _objcount: int) -> int:
        """
        Построить тематические картограммы
        
        :param _sitename: имя файла выходной карты или ``0``
        
        :param _legendname: имя файла карты легенды (может совпадать с sitename, ``0`` - не создавать легенду)
        
        :param _options: параметры построения тематических картограмм
        
        :param _values: массив описаний диапазона (количество диапазонов ItemsCount указано в ``THEMATICPARM``). ``0`` - если для файлов ``CSV`` указано поле с цветом (``THEMDIALOGPARM``::NumberColorField)
        
        :param _objvalue: массив описаний объектов
        
        :param _objcount: количество описаний объектов
        
        :returns: Возвращает количество построенных картограмм При ошибке возвращает ноль
        :rtype: int
        """
        return mathCreateThematicMap_t (_sitename.buffer(), _legendname.buffer(), _options, _values, _objvalue, _objcount)

    mathSetThematicData_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathSetThematicData', maptype.PWCHAR, ctypes.POINTER(THEMATICPARM), ctypes.POINTER(THEMDIALOGPARM), ctypes.POINTER(OBJVALUE), ctypes.c_long)
    def mathSetThematicData(_filename: mapsyst.WTEXT, _options: ctypes.POINTER(THEMATICPARM), _paramdlg: ctypes.POINTER(THEMDIALOGPARM), _objvalue: ctypes.POINTER(OBJVALUE), _objcount: int) -> int:
        """
        Заполнить массив objvalue для построения тематических картограмм
        
        :param _filename: имя файла таблицы (dbf, csv, txt)
        
        :param _options: параметры построения тематических картограмм
        
        :param _paramdlg: параметры из диалога построения тематических картограмм
        
        :param _objvalue: массив описаний объектов
        
        :param _objcount: количество описаний объектов Вызывать перед функцией mathCreateThematicMap в режимах построения ``"раскраска по значениям семантики"``: ``THEMATICPARM``::ConnectType ``= 0``,``1``,``2``
        
        :returns: Возвращает количество найденных объектов карты, соответствующих условиям отбора При ошибке возвращает ноль
        :rtype: int
        """
        return mathSetThematicData_t (_filename.buffer(), _options, _paramdlg, _objvalue, _objcount)

    mathCreateConvexPolygonByPoints_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathCreateConvexPolygonByPoints', ctypes.POINTER(maptype.XYHDOUBLE), ctypes.c_long, maptype.HOBJ)
    def mathCreateConvexPolygonByPoints(_list: ctypes.POINTER(maptype.XYHDOUBLE), _count: int, _hobj: maptype.HOBJ) -> int:
        """
        Создать выпуклый полигон по точкам
        
        :param _list: указатель на список точек
        
        :param _count: количество точек в списке
        
        :param _hobj: выходной объект, созданный по точкам из массива list Выходной объект должен быть создан заранее, внутри функции удаляется старая метрика и заполняется новая
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathCreateConvexPolygonByPoints_t (_list, _count, _hobj)

    mathCreateStarPolygonByPoints_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathCreateStarPolygonByPoints', ctypes.POINTER(maptype.XYHDOUBLE), ctypes.c_long, maptype.HOBJ)
    def mathCreateStarPolygonByPoints(_list: ctypes.POINTER(maptype.XYHDOUBLE), _count: int, _hobj: maptype.HOBJ) -> int:
        """
        Создать звездчатый полигон по точкам
        
        :param _list: указатель на список точек
        
        :param _count: количество точек в списке
        
        :param _hobj: выходной объект, созданный по точкам из массива list Выходной объект должен быть создан заранее, внутри функции удаляется старая метрика и заполняется новая
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathCreateStarPolygonByPoints_t (_list, _count, _hobj)

    mathConvexPolygon_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathConvexPolygon', maptype.HOBJ, maptype.HOBJ)
    def mathConvexPolygon(_hobjsource: maptype.HOBJ, _hobjdest: maptype.HOBJ) -> int:
        """
        Построить выпуклый многоугольник, в область которого входят все точки исходного объекта
        
        :param _hobjsource: идентификатор исходного объекта
        
        :param _hobjdest: идентификатор объекта для записи выпуклого многоугольника
        
        :returns: Возвращает количество вершин многоугольника При ошибке возвращает ноль
        :rtype: int
        """
        return mathConvexPolygon_t (_hobjsource, _hobjdest)

    mathConvexPolygonByTotalSelect_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathConvexPolygonByTotalSelect', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(ctypes.c_long))
    def mathConvexPolygonByTotalSelect(_hmap: maptype.HMAP, _hobjdest: maptype.HOBJ, _errorcode: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Построить выпуклый многоугольник по выделенным объектам карты
        
        :param _hmap: идентификатор открытых данных
        
        :param _hobjdest: идентификатор объекта для записи выпуклого многоугольника
        
        :param _errorcode: код ошибки для вывода: ``0`` - ошибок нет ``1`` - не все точки обработаны
        
        :returns: Возвращает количество вершин многоугольника При ошибке возвращает ноль
        :rtype: int
        """
        return mathConvexPolygonByTotalSelect_t (_hmap, _hobjdest, _errorcode)

    mathTheoAdjusting_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathTheoAdjusting', maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(TEO_PARAM))
    def mathTheoAdjusting(_inputname: mapsyst.WTEXT, _outputname: mapsyst.WTEXT, _param: ctypes.POINTER(TEO_PARAM)) -> int:
        """
        Уравнять теодолитный ход
        
        :param _inputname: имя исходного файла ``CSV`` с измерениями
        
        :param _outputname: имя файла ``CSV`` с результатами уравнивания
        
        :param _param: параметры обработки В исходном файле ``CSV`` колонки разделены символом ``";"`` первая строка исходного файла - заголовок таблицы, названия колонок: ``ST_NAME`` - название точки (станции) X       - координата X Y       - координата Y ``HOR`` - горизотальный угол в фоормате: ``GGG`` ``MM`` ``SS``.S ``DIR`` - дирекционный угол в фоормате:  ``GGG`` ``MM`` ``SS``.S ``DIST`` - горизонтальное проложение (в м.)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathTheoAdjusting_t (_inputname.buffer(), _outputname.buffer(), _param)

    mathMakeRectangleObject_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathMakeRectangleObject', maptype.HOBJ, ctypes.c_double, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mathMakeRectangleObject(_hobj: maptype.HOBJ, _filter: float, _mode: int, _pointnumber: int, _subject: int) -> int:
        """
        Привести объект к прямоугольному виду
        
        :param _hobj: идентификатор объекта
        
        :param _filter: уровень фильтрации объекта в метрах на местности
        
        :param _mode: режим проверки корректности преобразования: ``0`` - проверять всегда ``1`` - проверять только при условии, что разница площадей меньше ``10````%``
        
        :param _pointnumber: номер точки объекта/подобъекта
        
        :param _subject: номер подобъекта Код возврата: ``0`` - ошибка ``1`` - объект преобразован -``1`` - объект не преобразован
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mathMakeRectangleObject_t (_hobj, _filter, _mode, _pointnumber, _subject)

    mathCreateDiagram_t = mapsyst.GetProcAddress(mathlib,ctypes.c_long,'mathCreateDiagram', ctypes.POINTER(DIAOPTIONS), ctypes.POINTER(SIZEPARAM), ctypes.POINTER(SEMANTICPARAM), ctypes.c_long)
    def mathCreateDiagram(_options: ctypes.POINTER(DIAOPTIONS), _sizeparam: ctypes.POINTER(SIZEPARAM), _semanticparam: ctypes.POINTER(SEMANTICPARAM), _count: int) -> int:
        """
        Построить тематические диаграммы
        
        :param _options: общие параметры построения диаграммы
        
        :param _sizeparam: параметры для определения размера диаграммы
        
        :param _semanticparam: список характеристик для построения диаграмм
        
        :param _count: число элементов списка характеристик
        
        :returns: Возвращает количество построенных диаграмм При ошибке возвращает ноль
        :rtype: int
        """
        return mathCreateDiagram_t (_options, _sizeparam, _semanticparam, _count)



def mathapi_healthcheck():
    return 1
