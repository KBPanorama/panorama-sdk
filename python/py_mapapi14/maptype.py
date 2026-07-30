#!/usr/bin/env python3

# ********************************************************************
# *                                                                  *
# *              Copyright (c) PANORAMA Group 1991-2026              *
# *                      All Rights Reserved                         *
# *                                                                  *
# ********************************************************************
# *                                                                  *
# *               Описание базовых типов переменных                  *
# *                                                                  *
# ********************************************************************

import os
import ctypes
import mapsyst

WCHAR = ctypes.c_char
WCHAR1 = ctypes.c_char # устанавливать размер массива в 2 раза больше вручную
PWCHAR = ctypes.c_void_p # utf-16

MAX_PATH       = 260
MAX_PATH_LONG  = 1024
LF_FACESIZE    = 32

HMAP         = ctypes.c_void_p   # Указатель на TMapAccess
HSITE        = ctypes.c_void_p   # Указатель на элемент цепочки
HDATA        = ctypes.c_void_p   # Указатель на любой элемент данных электронной карты
HOBJ         = ctypes.c_longlong # Указатель на TObjectInfo
HSELECT      = ctypes.c_void_p   # Указатель на TMapSelect
HRSC         = ctypes.c_void_p   # Указатель на TMapRsc

HPANACTION   = ctypes.c_void_p   # Указатель на TPanAction
HMAPACTION   = ctypes.c_void_p   # Указатель на TUserAction
HPANTASK     = ctypes.c_void_p   # Указатель на TPanTask
HMAPTASK     = ctypes.c_void_p   # Указатель на TUserTask
HMAPDOC      = ctypes.c_void_p   # Указатель на TMapWindow
HOBJSET      = ctypes.c_void_p   # Указатель на TObjectSet
HOBJLISTSEEK = ctypes.c_void_p   # Указатель на TSeekList
HFORMULA     = ctypes.c_void_p   # Указатель на TStrFormula
HSEMRECORD   = ctypes.c_byte     # Указатель на TSemanticRecord

HMTR3D       = ctypes.c_void_p   # Указатель на TMtr3D
HMTL3D       = ctypes.c_void_p   # Указатель на TMtr3D
HCROSS       = ctypes.c_void_p   # Указатель на TObjectCut
HCROSSPOINTS = ctypes.c_void_p   # Указатель на класс построения пересечения
HCROSSCONS   = ctypes.c_void_p   # Указатель на класс смежных участков
HPOINT       = ctypes.c_void_p   # Указатель на структуру CROSSPOINT
HDRAW        = ctypes.c_void_p   # Указатель на структуру TDrawEdit
HPRINTER     = ctypes.c_void_p   # Указатель на TPrinter
HVECT        = ctypes.c_void_p   # Указатель на TVectorImageEdit

HIMAGE       = ctypes.c_void_p   # Идентификатор TCopyImage

HMAPREG      = ctypes.c_void_p   # Идентификатор списка параметров систем отсчета
HPAINT       = ctypes.c_void_p   # Идентификатор TPaintControl
HOVL         = ctypes.c_void_p   # Идентификатор класса оверлейных операций
HALS         = ctypes.c_void_p   # Идентификатор списка районов работ
HEDTLINE     = ctypes.c_void_p   # Класс работы с линейкой шаблонов
HWFS         = ctypes.c_void_p   # Идентификатор WFS-сервиса
HGMLCLASS    = ctypes.c_void_p

HOBJLIST     = ctypes.c_void_p

# callback - типы
BREAKCALLEX     = ctypes.c_void_p     
EVENTSTATE      = ctypes.c_void_p    
BREAKCALL       = ctypes.c_void_p   
BEFOREPAINT     = ctypes.c_void_p     
MASKCALL        = ctypes.c_void_p  
EVENTCALL       = ctypes.c_void_p   
MESSAGEBOXCALL  = ctypes.c_void_p        
EVENTLOG        = ctypes.c_void_p  

# ВИДЫ ФОРМАТОВ МЕТРИКИ
IDLONG2      = 0x7FFE7FFE  # четырехбайтовая целочисленная
IDDOUBLE2    = 0x7FFC7FFC  # с плавающей запятой двойной точностью
IDBIGDOUBLE2 = 0x7FFC7FFF  # с плавающей запятой двойной точностью (>= 65535 подобъектов)
IDLONG3      = 0x7FFA7FFA  # четырехбайтовая целочисленная трехмерная
IDDOUBLE4    = 0x7FF87FFF  # с плавающей запятой двойной точностью трехмерная и поле M (double)
IDDOUBLE4F   = 0x7FF87FFE  # с плавающей запятой двойной точностью трехмерная и поле F (integer)
IDDOUBLE3    = 0x7FF87FF8  # с плавающей запятой двойной точностью трехмерная
IDBAD        = 0x7FF87FF7  # неизвестный вид

# Точность обработки координат при визуализации
DELTANULL  = 1e-3

# Точность обработки координат при выполнении расчетов
DOUBLENULL = 1e-6

# Признак ошибочного значения высоты
ERRORHEIGHT = -111111.0

# Признак ошибочной мощности слоя
ERRORPOWER = -1111111.0

# ЛОКАЛИЗАЦИЯ ОБЪЕКТА (ТИП)
LOCAL_LINE   = 0 # Линия
LOCAL_SQUARE = 1 # Полигон
LOCAL_POINT  = 2 # Точечный знак
LOCAL_TITLE  = 3 # Подпись (метка)
LOCAL_VECTOR = 4 # Векторный знак - точечный с ориентацией на вторую точку
LOCAL_MIXED  = 5 # Шаблон - комбинированная с линией и точечным знаком подпись (устаревшее)
LOCAL_COUNT  = 6
LOCAL_UP     = 6

SEMIMAGESCALE  = 31001  # МАСШТАБ ОТОБРАЖЕНИЯ ЗНАКА В ПРОЦЕНТАХ
SEMIMAGECOLOR  = 31002  # ЦВЕТ ОТОБРАЖЕНИЯ ЗНАКА RGB
SEMIMAGEHIGHT  = 31003  # ВЫСОТА ШРИФТА В ММ
SEMIMAGEFONT   = 31004  # НАЗВАНИЕ ШРИФТА
SEMIMAGETHICK  = 31005  # ТОЛЩИНА ЛИНИИ В ММ
SEMIMAGETHICK2 = 31006  # ТОЛЩИНА ОКОНЧАНИЯ ЛИНИИ В ММ
SEMCOLORWEIGHT = 31007  # ВЕС ЦВЕТА ОБЪЕКТА В ПРОЦЕНТАХ

# КОД СИСТЕМЫ КООРДИНАТ
PP_MAPOLD   = 1    # КООРДИНАТЫ ТОЧЕК В СИСТЕМЕ КАРТЫ В ДИСКРЕТАХ (УСТАРЕВШЕЕ)
PP_PICTURE  = 2    # КООРДИНАТЫ ТОЧЕК В СИСТЕМЕ ИЗОБРАЖЕНИЯ В ПИКСЕЛАХ
PP_PLANE    = 3    # КООРДИНАТЫ ТОЧЕК В ПЛОСКОЙ ПРЯМОУГОЛЬНОЙ СИСТЕМЕ НА МЕСТНОСТИ В МЕТРАХ
PP_MAP      = 3
PP_GEO      = 4    # КООРДИНАТЫ ТОЧЕК В ГЕОДЕЗИЧЕСКИХ КООРДИНАТАХ В РАДИАНАХ
PP_GEOWGS84 = 8    # КООРДИНАТЫ ТОЧЕК В ГЕОДЕЗИЧЕСКИХ КООРДИНАТАХ В РАДИАНАХ В СИСТЕМЕ WGS 84

# ФЛАЖКИ ПОИСКА                      
WO_FIRST        = 0    # Первый в цепочке
WO_LAST         = 2    # Последний в цепочке
WO_NEXT         = 4    # Следующий за найденным ранее
WO_BACK         = 8    # Предыдущий от ранее найденного
WO_CANCEL       = 16   # Включая удаленные объекты
WO_INMAP        = 32   # Только по одной карте (соответствующей HSELECT)
WO_VISUAL       = 64   # Поиск только среди видимых объектов
WO_VISUALIGNORE = 128  # Поиск среди всех объектов без учета видимости
WO_SKIPTEXT     = 256  # Текст при поиске выбирать последним
WO_VISUALSCALE  = 512  # Поиск только среди видимых объектов с учетом границ видимости
WO_AREABYBORDER = 1024 # Выбор площадных объектов по контуру

# ИДЕНТИФИКАТОРЫ КОМАНД И ИХ ПАРАМЕТРОВ
MT_MAPWINPORT = 0x660
MWP_INVALIDATE = 0x105

AW_MESSAGEBOX = 0x589  # Сообщение с информационным текстом для оператора
AW_ERRORBOX   = 0x58A  # Сообщение с текстом ошибки для оператора
WM_LOGTEXT    = 0x58B  # Сообщение с текстом в протокол (wparam = const WCHAR *, lparam = 0 или MT_ERROR)

CM_PAN_SEARCH = 0x6EF                      

# ТИПЫ СООБЩЕНИЙ В ПРОТОКОЛ
MT_INFO     = 0    # Информационное сообщение
MT_ERROR    = 1    # Сообщение об ошибке
MT_WARNING  = 2    # Информационное сообщение
MT_CONTINUE = 4    # Продолжение предыдущего сообщения на той же строке
MT_NEXT     = 5    # Продолжение предыдущего сообщения на новой строке
MT_HARDERROR = 6   # Ошибки оборудования или общесистемных программных средств

# ТИПЫ СООБЩЕНИЙ НА ЭКРАНЕ
MB_OKCANCEL = 1
MB_YESNOCANCEL = 3
MB_YESNO = 4
MB_RETRYCANCEL = 5
MB_ERROR = 16
MB_WARNING = 48
MB_OK = 64

# КОДЫ ЯЗЫКА СООБЩЕНИЙ
ML_ENGLISH   = 1  # Английский
ML_RUSSIAN   = 2  # Русский
ML_FRENCH    = 3  # Французский
ML_SPANISH   = 4  # Испанский
ML_UKRAINIAN = 5  # Украинский
ML_KAZAKH    = 6  # Казахский
ML_VIETNAM   = 7  # Вьетнамский
ML_CHINESE   = 8  # Китайский

# РАЗМЕЩЕНИЕ ТОЧКИ ОТНОСИТЕЛЬНО ОТРЕЗКА
PS_FIRST   = 1   #  Совпадает с первой точкой отрезка
PS_SECOND  = 2   #  Совпадает со второй точкой отрезка
PS_BEHIND  = 3   #  Лежит позади первой точки отрезка
PS_BEYOND  = 4   #  Лежит впереди второй точки отрезка
PS_BETWEEN = 5   #  Лежит на отрезке (между точками)
PS_LEFT    = 6   #  Слева
PS_RIGHT   = 7   #  Справа

DWORD     = ctypes.c_uint
COLORREF  = DWORD
HMESSAGE  = ctypes.c_void_p
HDC       = ctypes.c_void_p
HINSTANCE = ctypes.c_void_p
HPALETTE  = ctypes.c_void_p
HWND      = ctypes.c_void_p
HBITMAP   = ctypes.c_void_p

GENERIC_READ  = 0x100000
GENERIC_WRITE = 0x0001

PACK_WIDTH = 1

#-----------------------------
class LOGFONT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("lfHeight",ctypes.c_long),
                ("lfWidth",ctypes.c_long),
                ("lfEscapement",ctypes.c_long),
                ("lfOrientation",ctypes.c_long),
                ("lfWeight",ctypes.c_long),
                ("lfItalic",ctypes.c_byte),
                ("lfUnderline",ctypes.c_byte),
                ("lfStrikeOut",ctypes.c_byte),
                ("lfCharSet",ctypes.c_byte),
                ("lfOutPrecision",ctypes.c_byte),
                ("lfClipPrecision",ctypes.c_byte),
                ("lfQuality",ctypes.c_byte),
                ("lfPitchAndFamily",ctypes.c_byte),
                ("lfFaceName",WCHAR1*LF_FACESIZE)]
#-----------------------------


#-----------------------------
class LOGFONTW(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("lfHeight",ctypes.c_long),
                ("lfWidth",ctypes.c_long),
                ("lfEscapement",ctypes.c_long),
                ("lfOrientation",ctypes.c_long),
                ("lfWeight",ctypes.c_long),
                ("lfItalic",ctypes.c_byte),
                ("lfUnderline",ctypes.c_byte),
                ("lfStrikeOut",ctypes.c_byte),
                ("lfCharSet",ctypes.c_byte),
                ("lfOutPrecision",ctypes.c_byte),
                ("lfClipPrecision",ctypes.c_byte),
                ("lfQuality",ctypes.c_byte),
                ("lfPitchAndFamily",ctypes.c_byte),
                ("lfFaceName",WCHAR1*LF_FACESIZE)]
#-----------------------------


#-----------------------------
class PALETTEENTRY(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("peRed",ctypes.c_byte),
                ("peGreen",ctypes.c_byte),
                ("peBlue",ctypes.c_byte),
                ("peFlags",ctypes.c_byte)]
#-----------------------------


#-----------------------------
class POINT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("x",ctypes.c_int),
                ("y",ctypes.c_int)]
#-----------------------------


#-----------------------------
class RECT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("left",ctypes.c_int),
                ("top",ctypes.c_int),
                ("right",ctypes.c_int),
                ("bottom",ctypes.c_int)]
#-----------------------------


#-----------------------------
class RGBQUAD(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("rgbBlue",ctypes.c_byte),
                ("rgbGreen",ctypes.c_byte),
                ("rgbRed",ctypes.c_byte),
                ("rgbReserved",ctypes.c_byte)]
#-----------------------------


#-----------------------------
class SYSTEMTIME(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("wYear",ctypes.c_ushort),
                ("wMonth",ctypes.c_ushort),
                ("wDayOfWeek",ctypes.c_ushort),
                ("wDay",ctypes.c_ushort),
                ("wHour",ctypes.c_ushort),
                ("wMinute",ctypes.c_ushort),
                ("wSecond",ctypes.c_ushort),
                ("wMilliseconds",ctypes.c_ushort)]
#-----------------------------


#-----------------------------
class LONGPOINT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("X",ctypes.c_int),
                ("Y",ctypes.c_int)]
#-----------------------------


#-----------------------------
class BIGPOINT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("X",ctypes.c_int64),
                ("x",ctypes.c_int64)]
#----------------------------- 


#-----------------------------
class DOUBLEPOINT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("X",ctypes.c_double),
                ("Y",ctypes.c_double)]
#-----------------------------


#-----------------------------
class DRAWPOINT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("X",ctypes.c_int),
                ("Y",ctypes.c_int)]
#-----------------------------


#-----------------------------
class DRAWSIZE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("CX",ctypes.c_int),
                ("CY",ctypes.c_int)]
#-----------------------------


#-----------------------------
class DRAWLINE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("First",DRAWPOINT),
                ("Second",DRAWPOINT)]
#-----------------------------


#-----------------------------
class DRAWBOX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Point1",DRAWPOINT),
                ("Point2",DRAWPOINT),
                ("Point3",DRAWPOINT),
                ("Point4",DRAWPOINT)]
#-----------------------------


#-----------------------------
class FRAME(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("X1",ctypes.c_int),
                ("Y1",ctypes.c_int),
                ("X2",ctypes.c_int),
                ("Y2",ctypes.c_int)]
#-----------------------------


#-----------------------------
class DFRAME(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("X1",ctypes.c_double),
                ("Y1",ctypes.c_double),
                ("X2",ctypes.c_double),
                ("Y2",ctypes.c_double)]
#-----------------------------


#-----------------------------
class LFRAME(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("X1",ctypes.c_int64),
                ("Y1",ctypes.c_int64),
                ("X2",ctypes.c_int64),
                ("Y2",ctypes.c_int64)]
#-----------------------------


#-----------------------------
class LRECT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("left",ctypes.c_int64),
                ("top",ctypes.c_int64),
                ("right",ctypes.c_int64),
                ("bottom",ctypes.c_int64)]
#-----------------------------


#-----------------------------
class INTQUAD(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Value1",ctypes.c_char),
                ("Value2",ctypes.c_char),
                ("Value3",ctypes.c_char),
                ("Value4",ctypes.c_char)]
#-----------------------------


#-----------------------------
class INT64TWO(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Value1",ctypes.c_char),
                ("Value2",ctypes.c_char)]
#-----------------------------


#-----------------------------
class BOX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("LT",ctypes.c_int),
                ("UP",ctypes.c_int),
                ("RT",ctypes.c_int),
                ("DN",ctypes.c_int)]
#-----------------------------


#-----------------------------
class CMYKCOLOR(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("C",ctypes.c_byte),
                ("M",ctypes.c_byte),
                ("Y",ctypes.c_byte),
                ("K",ctypes.c_byte)]
#-----------------------------


#-----------------------------
class TABCOLORSITEM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("GroupId",ctypes.c_int),
                ("RgbColor",ctypes.c_uint),
                ("Cmyk",CMYKCOLOR),
                ("Flags",ctypes.c_uint),
                ("Name",WCHAR*(80))]
#-----------------------------


#-----------------------------
class POLYDATAEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Points",ctypes.POINTER(DRAWPOINT)),
                ("PolyCounts",ctypes.POINTER(ctypes.c_int)),
                ("Text",ctypes.POINTER(ctypes.POINTER(ctypes.c_char))),
                ("Semantic",ctypes.c_char_p),
                ("Count",ctypes.c_int),
                ("AlignCode",ctypes.c_short),
                ("Flags",ctypes.c_short),
                ("Border",BOX),
                ("ShowScale",ctypes.c_double),
                ("MapRsc",HRSC),
                ("Height",ctypes.c_float),
                ("DX",ctypes.c_float),
                ("DY",ctypes.c_float),
                ("Zero",ctypes.c_float)]
#-----------------------------


#-----------------------------
class POLYDATA4D(POLYDATAEX):
    _pack_ = PACK_WIDTH
    _fields_ = [("Measure",ctypes.POINTER(ctypes.c_double)),
                ("Fixed",ctypes.POINTER(ctypes.c_int64))]
#-----------------------------


#-----------------------------
class DRAWOBJECT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Draw",HDRAW),
                ("Select",HSELECT)]
#-----------------------------


#-----------------------------
class TABCMYK(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Cmyk",CMYKCOLOR*(256))]
#-----------------------------


#-----------------------------
class TEXTDATA(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_byte),
                ("Text",ctypes.c_char),
                ("Zero",ctypes.c_byte),
                ("Code",ctypes.c_byte)]
#-----------------------------


#-----------------------------
class XYLONG(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("X",ctypes.c_int),
                ("Y",ctypes.c_int)]
#-----------------------------


#-----------------------------
class XYHLONG(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("X",ctypes.c_int),
                ("Y",ctypes.c_int),
                ("H",ctypes.c_float)]
#-----------------------------


#-----------------------------
class XYHDOUBLE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("X",ctypes.c_double),
                ("Y",ctypes.c_double),
                ("H",ctypes.c_double)]
#-----------------------------


#-----------------------------
class XYHMDOUBLE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("X",ctypes.c_double),
                ("Y",ctypes.c_double),
                ("H",ctypes.c_double),
                ("M",ctypes.c_double)]
#-----------------------------


#-----------------------------
class XYHFDOUBLE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("X",ctypes.c_double),
                ("Y",ctypes.c_double),
                ("H",ctypes.c_double),
                ("F",ctypes.c_int64)]
#-----------------------------


#-----------------------------
class MAPADJACENTSECTION(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("number",ctypes.c_int),
                ("first",ctypes.c_int),
                ("last",ctypes.c_int)]
#-----------------------------


#-----------------------------
class MAPADJACENTLISTEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("ListName",ctypes.c_char),
                ("List",ctypes.c_int),
                ("Key",ctypes.c_int),
                ("Object",ctypes.c_int),
                ("Excode",ctypes.c_int),
                ("First",ctypes.c_int),
                ("Last",ctypes.c_int)]
#-----------------------------


#-----------------------------
class CONNECTPATH(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("IsForward",ctypes.c_int),
                ("FirstPoint",ctypes.c_int),
                ("LastPoint",ctypes.c_int),
                ("NearSubject",ctypes.c_int),
                ("NearFirstPoint",ctypes.c_int),
                ("NearLastPoint",ctypes.c_int)]
#-----------------------------


#-----------------------------
class WCHARLIST(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Code",ctypes.c_int64),
                ("Text",PWCHAR)]
#-----------------------------


#-----------------------------
class GEODEGREE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Degree",ctypes.c_int),
                ("Minute",ctypes.c_int),
                ("Second",ctypes.c_float)]
#-----------------------------


#-----------------------------
class SIGNDEGREE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Degree",ctypes.c_int),
                ("Minute",ctypes.c_int),
                ("Second",ctypes.c_float),
                ("Sign",ctypes.c_int)]
#-----------------------------


#-----------------------------
class MTRTILEEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Ident",ctypes.c_int),
                ("Length",ctypes.c_int),
                ("Width",ctypes.c_int),
                ("Height",ctypes.c_int),
                ("Epsg",ctypes.c_int),
                ("Level",ctypes.c_int),
                ("WidthNumber",ctypes.c_int),
                ("HeightNumber",ctypes.c_int),
                ("Unit",ctypes.c_int),
                ("UnitPlane",ctypes.c_int),
                ("ItemWidth",ctypes.c_int),
                ("ItemHeight",ctypes.c_int),
                ("MinValue",ctypes.c_int),
                ("MaxValue",ctypes.c_int),
                ("HeightPrescision",ctypes.c_int),
                ("Reserve",ctypes.c_int)]
#-----------------------------


#-----------------------------
class MTRDESCRIBEUN(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Name",WCHAR1),
                ("MinValue",ctypes.c_double),
                ("MaxValue",ctypes.c_double),
                ("ElementInPlane",ctypes.c_double),
                ("FrameMeters",DFRAME),
                ("ReliefType",ctypes.c_int),
                ("UserType",ctypes.c_int),
                ("View",ctypes.c_int),
                ("Zero",ctypes.c_int)]
#-----------------------------


#-----------------------------
class MTRCOLORDESCEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("MinHeight",ctypes.c_double),
                ("MaxHeight",ctypes.c_double),
                ("Color",COLORREF)]
#-----------------------------


#-----------------------------
class MTR3DVIEWBASE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("AreaCenterX",ctypes.c_double),
                ("AreaCenterY",ctypes.c_double),
                ("CutX",ctypes.c_double),
                ("CutY",ctypes.c_double),
                ("CutZ",ctypes.c_double),
                ("CutH",ctypes.c_double),
                ("ShowScale",ctypes.c_int),
                ("ModelHeight",ctypes.c_int),
                ("GridStep",ctypes.c_int),
                ("CutShape",ctypes.c_int),
                ("ViewAngle",ctypes.c_short),
                ("RotationAngle",ctypes.c_short),
                ("Style",ctypes.c_char),
                ("ShowGrid",ctypes.c_char),
                ("Shadow",ctypes.c_char),
                ("ScaleType",ctypes.c_char),
                ("CoverMatrix",ctypes.c_char),
                ("CoverMap",ctypes.c_char),
                ("CoverRaster",ctypes.c_char),
                ("AccordScale",ctypes.c_char),
                ("CoverMtq",ctypes.c_char),
                ("IsUpdate",ctypes.c_char),
                ("Reserve",ctypes.c_char),
                ("CursorX",ctypes.c_double),
                ("CursorY",ctypes.c_double),
                ("Width",ctypes.c_int),
                ("Height",ctypes.c_int)]
#-----------------------------


#-----------------------------
class MTR3DVIEWEX(MTR3DVIEWBASE):
    _pack_ = PACK_WIDTH
    _fields_ = [("Name",ctypes.c_char)]
#-----------------------------


#-----------------------------
class MTR3DVIEWUN(MTR3DVIEWBASE):
    _pack_ = PACK_WIDTH
    _fields_ = [("Name",WCHAR1)]
#-----------------------------


#-----------------------------
class MTL3DVIEWUN(MTR3DVIEWBASE):
    _pack_ = PACK_WIDTH
    _fields_ = [("Name",WCHAR1)]
#-----------------------------


#-----------------------------
class METAFILEBUILDPARMEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Frame",DFRAME),
                ("Scale",ctypes.c_int),
                ("VisualType",ctypes.c_char),
                ("Border",ctypes.c_char),
                ("Intensity",ctypes.c_char),
                ("Black",ctypes.c_char),
                ("DontClip",ctypes.c_char),
                ("Reserve",ctypes.c_char)]
#-----------------------------


#-----------------------------
class XIMAGEDESC(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Point",ctypes.c_char_p),
                ("Width",ctypes.c_int),
                ("Height",ctypes.c_int),
                ("CellSize",ctypes.c_int),
                ("RowSize",ctypes.c_int),
                ("Depth",ctypes.c_int),
                ("Reserve",ctypes.c_int)]
#-----------------------------


#-----------------------------
class PRINTPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Scale",ctypes.c_int),
                ("TypePrint",ctypes.c_char),
                ("TypeOutput",ctypes.c_char),
                ("Mirror",ctypes.c_char),
                ("ColorModel",ctypes.c_char),
                ("Technology",ctypes.c_char),
                ("InsetPrint",ctypes.c_char),
                ("Reserve",ctypes.c_char),
                ("Service",ctypes.c_char),
                ("DontClip",ctypes.c_char),
                ("HorPixInInch",ctypes.c_double),
                ("VerPixInInch",ctypes.c_double)]
#-----------------------------


#-----------------------------
class GRIDPARMPRO_as1(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Color",ctypes.c_int),
                ("Thick",ctypes.c_int)]
class GRIDPARMPRO(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("StepX",ctypes.c_double),
                ("StepY",ctypes.c_double),
                ("BeginX",ctypes.c_double),
                ("BeginY",ctypes.c_double),
                ("Type",ctypes.c_int),
                ("Image",GRIDPARMPRO_as1),
                ("Size",ctypes.c_int),
                ("Shadow",ctypes.c_int),
                ("Under",ctypes.c_int)]
#-----------------------------


#-----------------------------
class TBUILDZONEVISIBILITY(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("PointCenter",DOUBLEPOINT),
                ("RadiusMeter",ctypes.c_double),
                ("Azimuth",ctypes.c_double),
                ("Angle",ctypes.c_double),
                ("DeltaHight",ctypes.c_double),
                ("DeltaObservation",ctypes.c_double),
                ("VisionRst",ctypes.c_int),
                ("StyleRst",ctypes.c_int),
                ("ColorRst",ctypes.c_int),
                ("Inversion",ctypes.c_int)]
#-----------------------------


#-----------------------------
class EDITVALUEPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("FixedDistance",ctypes.c_double),
                ("Regime",ctypes.c_int),
                ("Reserve",ctypes.c_int),
                ("Value",WCHAR1),
                ("Text",WCHAR1)]
#-----------------------------


#-----------------------------
class ZIPHEAD(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Label",ctypes.c_uint),
                ("Version",ctypes.c_ushort),
                ("Flag",ctypes.c_ushort),
                ("Method",ctypes.c_ushort),
                ("Time",ctypes.c_ushort),
                ("Date",ctypes.c_ushort),
                ("Crc32",ctypes.c_uint),
                ("CSize",ctypes.c_uint),
                ("USize",ctypes.c_uint),
                ("NameSize",ctypes.c_ushort),
                ("ExtSize",ctypes.c_ushort)]
#-----------------------------


#-----------------------------
class REGISTER_REGBYTE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("b1",ctypes.c_byte),
                ("b2",ctypes.c_byte),
                ("b3",ctypes.c_byte),
                ("b4",ctypes.c_byte)]
class REGISTER_REGWORD(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("w1",ctypes.c_ushort),
                ("w2",ctypes.c_ushort)]
class REGISTER(ctypes.Union):
    _pack_ = PACK_WIDTH
    _fields_ = [("Byte",REGISTER_REGBYTE),
                ("Word",REGISTER_REGWORD),
                ("Long",ctypes.c_int),
                ("Float",ctypes.c_float)]
#-----------------------------


#-----------------------------
class DOUBLEREGISTER_REGDBYTE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("b1",ctypes.c_byte),
                ("b2",ctypes.c_byte),
                ("b3",ctypes.c_byte),
                ("b4",ctypes.c_byte),
                ("b5",ctypes.c_byte),
                ("b6",ctypes.c_byte),
                ("b7",ctypes.c_byte),
                ("b8",ctypes.c_byte)]
class DOUBLEREGISTER(ctypes.Union):
    _pack_ = PACK_WIDTH
    _fields_ = [("Byte",DOUBLEREGISTER_REGDBYTE),
                ("Double",ctypes.c_double),
                ("Long64",ctypes.c_int64)]
#-----------------------------


#-----------------------------
class PALETTE256(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("palVersion",ctypes.c_ushort),
                ("palNumEntries",ctypes.c_ushort),
                ("palPalEntry",PALETTEENTRY)]
#-----------------------------


#-----------------------------
class IMAGESIZE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Number",ctypes.c_uint),
                ("Base",ctypes.c_uint),
                ("DeltaH",ctypes.c_int),
                ("DeltaV",ctypes.c_int),
                ("HorizontalSize",ctypes.c_uint),
                ("VerticalSize",ctypes.c_uint),
                ("Horizontal"  ,ctypes.c_uint,1),
                ("Vertical"    ,ctypes.c_uint,1),
                ("TwoPoint"    ,ctypes.c_uint,1),
                ("AlignV"      ,ctypes.c_uint,2),
                ("AlignH"      ,ctypes.c_uint,2),
                ("Wide"        ,ctypes.c_uint,2),
                ("Type"        ,ctypes.c_uint,8),
                ("Italic"      ,ctypes.c_uint,1),
                ("Rezerv"      ,ctypes.c_uint,14)]
#-----------------------------


#-----------------------------
class IMAGEFRAME(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("LeftTop",DOUBLEPOINT),
                ("RightTop",DOUBLEPOINT),
                ("RightBottom",DOUBLEPOINT),
                ("LeftBottom",DOUBLEPOINT)]
#-----------------------------


#-----------------------------
class PROGRESSBARSTATE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Ident",ctypes.c_void_p),
                ("Percent",ctypes.c_int),
                ("Reserve",ctypes.c_int)]
#----------------------------- 


#-----------------------------
class TASKPARMEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Handle",HMESSAGE),
                ("DocHandle",HWND),
                ("ParentWidget",ctypes.c_void_p),
                ("ParentWinHandle",ctypes.c_void_p),
                ("Reserve1",ctypes.c_void_p),
                ("Reserve2",ctypes.c_void_p)]
#-----------------------------


#-----------------------------
class TMCUSERPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Name", ctypes.c_char * 32),
                ("Password", ctypes.c_char * 64)]

    # Установить имя пользователя
    def setName(self, name):
        if isinstance(name, str):
            self.Name = name.encode("utf-8")
        elif isinstance(name, ctypes.Array) and name._type_ == ctypes.c_char:
            self.Name = name.value
        elif isinstance(name, bytes):
            self.Name = name

    # Установить пароль для доступа к ГИС Серверу - переданный пароль кодируется по MD5
    def setPassword(self, password):
        if isinstance(password,str):
            from mapapi import mapStringToMd5Hash
            passwordHash = ctypes.create_string_buffer(64)
            mapStringToMd5Hash(password.encode("utf-8"),passwordHash,64)
            self.Password = passwordHash.value

    # Установить пароль для доступа к ГИС Серверу, закодированный по MD5
    def setPasswordMD5(self, password):
        if isinstance(name, str):
            self.Password = name.encode("utf-8")
        elif isinstance(name, ctypes.Array) and name._type_ == ctypes.c_char:
            self.Password = name.value
        elif isinstance(name, bytes):
            self.Password = name

#-----------------------------


#-----------------------------
class TMCUSERPARMUN(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Name",WCHAR*(64)),
                ("Password",ctypes.c_char*(64))]
#----------------------------- 


#-----------------------------
class TMCDATALISTITEMEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Ident",ctypes.c_uint),
                ("Length",ctypes.c_uint),
                ("Level",ctypes.c_uint),
                ("Flags",ctypes.c_uint),
                ("Type",ctypes.c_uint),
                ("Size",ctypes.c_uint),
                ("Date",ctypes.c_uint),
                ("Time",ctypes.c_uint)]
#-----------------------------


#-----------------------------
class TMCDATALISTITEM(TMCDATALISTITEMEX):
    _pack_ = PACK_WIDTH
    _fields_ = [("Name",WCHAR1)]
#-----------------------------


#-----------------------------
class TMCDATALIST(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Ident",ctypes.c_int),
                ("Length",ctypes.c_int),
                ("Count",ctypes.c_int),
                ("MaxLevel",ctypes.c_int),
                ("Item",TMCDATALISTITEM)]
#-----------------------------


#-----------------------------
class GSMONITOR(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Ident",ctypes.c_int),
                ("Length",ctypes.c_int),
                ("Version",ctypes.c_int),
                ("Count",ctypes.c_int),
                ("State",ctypes.c_int),
                ("BeginTime",ctypes.c_char),
                ("ParmName",ctypes.c_char),
                ("MapEdit",ctypes.c_int),
                ("MapRead",ctypes.c_int),
                ("MapCopy",ctypes.c_int),
                ("RswEdit",ctypes.c_int),
                ("RswRead",ctypes.c_int),
                ("RswCopy",ctypes.c_int),
                ("MtwEdit",ctypes.c_int),
                ("MtwRead",ctypes.c_int),
                ("MtwCopy",ctypes.c_int),
                ("MapNotPrint",ctypes.c_int),
                ("RswNotPrint",ctypes.c_int),
                ("MtwNotPrint",ctypes.c_int)]
#-----------------------------


#-----------------------------
class GSMUSEREX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Ident",ctypes.c_int),
                ("Length",ctypes.c_int),
                ("UserName",ctypes.c_char),
                ("MapCount",ctypes.c_int),
                ("RswCount",ctypes.c_int),
                ("MtwCount",ctypes.c_int),
                ("StartTime",ctypes.c_char),
                ("WorkDuration",ctypes.c_int),
                ("OperationCount",ctypes.c_int)]
#-----------------------------


#-----------------------------
class GSMUSERSHORT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Ident",ctypes.c_int),
                ("Length",ctypes.c_int),
                ("UserName",ctypes.c_char),
                ("MapCount",ctypes.c_int),
                ("RswCount",ctypes.c_int),
                ("MtwCount",ctypes.c_int),
                ("StartTime",ctypes.c_char),
                ("WorkDuration",ctypes.c_int),
                ("OperationCount",ctypes.c_int)]
#-----------------------------


#-----------------------------
class RMFTIFFINFO(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("TifSize",ctypes.c_int64),
                ("TifDate",ctypes.c_uint),
                ("TifTime",ctypes.c_uint),
                ("TofSize",ctypes.c_int64),
                ("TofDate",ctypes.c_uint),
                ("TofTime",ctypes.c_uint)]
#-----------------------------


#-----------------------------
class INSETDESC(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Ident",ctypes.c_int),
                ("Path",WCHAR1),
                ("Name",WCHAR1),
                ("FirstPlace",DOUBLEPOINT),
                ("SecondPlace",DOUBLEPOINT),
                ("FramePlace",DOUBLEPOINT),
                ("PlaceFlag",ctypes.c_int),
                ("PlaceType",ctypes.c_int),
                ("Scale",ctypes.c_int),
                ("TopScale",ctypes.c_int),
                ("BottomScale",ctypes.c_int),
                ("View",ctypes.c_int),
                ("Scheme",ctypes.c_int),
                ("BackColor",ctypes.c_int),
                ("Transparence",ctypes.c_int),
                ("BorderColor",ctypes.c_int),
                ("BorderThick",ctypes.c_int),
                ("BorderView",ctypes.c_int)]
#-----------------------------


#-----------------------------
class INSETDESCEX(INSETDESC):
    _pack_ = PACK_WIDTH
    _fields_ = [("SourceName",WCHAR1),
                ("Zposition",ctypes.c_int64)]
#-----------------------------


#-----------------------------
class ERRORINFOUN(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Free",ctypes.c_int),
                ("ErrorType",ctypes.c_int),
                ("ErrorTypeEx",ctypes.c_int),
                ("Amend",ctypes.c_int),
                ("Mark",ctypes.c_int),
                ("FirstListNumber",ctypes.c_int),
                ("FirstObjectNumber",ctypes.c_int),
                ("FirstNumberSemantic",ctypes.c_int),
                ("FirstKey",ctypes.c_int),
                ("FirstNumberSubject",ctypes.c_int),
                ("SecondListNumber",ctypes.c_int),
                ("SecondObjectNumber",ctypes.c_int),
                ("SecondNumberSemantic",ctypes.c_int),
                ("SecondKey",ctypes.c_int),
                ("SecondNumberSubject",ctypes.c_int),
                ("FirstPoint",DOUBLEPOINT),
                ("SecondPoint",DOUBLEPOINT),
                ("FirstListName",WCHAR1),
                ("SecondListName",WCHAR1),
                ("Title",WCHAR1)]
#-----------------------------


#-----------------------------
class MENUEXTEND_as1(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Command",ctypes.c_int),
                ("Check",ctypes.c_int),
                ("Text",ctypes.c_char)]
class MENUEXTEND(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Ident",ctypes.c_int),
                ("Count",ctypes.c_int),
                ("Item[32]",MENUEXTEND_as1)]
#-----------------------------


#-----------------------------
class COMMANDENABLER(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Command",ctypes.c_int),
                ("Enable",ctypes.c_int),
                ("Check",ctypes.c_int),
                ("Zero",ctypes.c_int),
                ("Menu",ctypes.POINTER(MENUEXTEND)),
                ("Text",WCHAR1)]
#-----------------------------


#-----------------------------
class VIEWHELPEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("HelpName",ctypes.c_char_p),
                ("Topic",ctypes.c_int)]
#-----------------------------


#-----------------------------
class CONTROLMENU(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Name",ctypes.c_char),
                ("Caption",ctypes.c_char),
                ("After",ctypes.c_char)]
#-----------------------------


#-----------------------------
class CONTROLITEM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Name",ctypes.c_char),
                ("Caption",ctypes.c_char),
                ("Item",ctypes.c_int),
                ("SubItem",ctypes.c_int),
                ("After",ctypes.c_int),
                ("Zero",ctypes.c_int)]
#-----------------------------


#-----------------------------
class RSCCREATE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Name",ctypes.c_char*(32)),
                ("Type",ctypes.c_char*(32)),
                ("Code",ctypes.c_char*(8)),
                ("Scale",ctypes.c_int),
                ("Language",ctypes.c_int)]
#-----------------------------


#-----------------------------
class RSCCREATEUN(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Name",WCHAR1),
                ("Type",WCHAR1),
                ("Code",WCHAR1),
                ("Scale",ctypes.c_int),
                ("Language",ctypes.c_int)]
#-----------------------------


#-----------------------------
class RSCOBJECT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Name",ctypes.c_char*(32))]
#-----------------------------


#-----------------------------
class RSCOBJECTEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_ulong),
                ("Code",ctypes.c_ulong),
                ("Local",ctypes.c_ulong),
                ("Segment",ctypes.c_ulong),
                ("Scale",ctypes.c_ulong),
                ("Direct",ctypes.c_ulong),
                ("Bot",ctypes.c_ulong),
                ("Top",ctypes.c_ulong),
                ("Name",ctypes.c_char),
                ("Key",ctypes.c_char)]
#-----------------------------


#-----------------------------
class RSCSEGMENT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Order",ctypes.c_uint),
                ("Name",ctypes.c_char)]
#-----------------------------


#-----------------------------
class RSCSEMANTICEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Code",ctypes.c_int),
                ("Type",ctypes.c_int),
                ("Reply",ctypes.c_int),
                ("Enable",ctypes.c_int),
                ("Service",ctypes.c_int),
                ("Reserve",ctypes.c_int),
                ("Name",ctypes.c_char),
                ("Unit",ctypes.c_char),
                ("Minimum",ctypes.c_double),
                ("Default",ctypes.c_double),
                ("Maximum",ctypes.c_double),
                ("Size",ctypes.c_int),
                ("Decimal",ctypes.c_int),
                ("ShortName",ctypes.c_char)]
#-----------------------------


#-----------------------------
class RSCFORMULA(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Code",ctypes.c_uint),
                ("Semantic",ctypes.c_uint),
                ("Length",ctypes.c_uint),
                ("Type",ctypes.c_uint),
                ("Round",ctypes.c_uint),
                ("Precision",ctypes.c_uint),
                ("Index",ctypes.c_uint),
                ("Number",ctypes.c_uint),
                ("Name",WCHAR1)]
#-----------------------------


#-----------------------------
class SEMLIBLIST_as1(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Type",ctypes.c_int),
                ("Zero",ctypes.c_int),
                ("Name",PWCHAR)]
class SEMLIBLIST(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Ident",ctypes.c_int),
                ("Count",ctypes.c_int),
                ("Element[32]",SEMLIBLIST_as1)]
#-----------------------------


#-----------------------------
class BIGSEMANTIC(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Ident",ctypes.c_ushort),
                ("Length",ctypes.c_ushort),
                ("BigLength",ctypes.c_int)]
#-----------------------------


#-----------------------------
class SEMANTIC(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Ident",ctypes.c_ushort),
                ("Length",ctypes.c_ushort)]
#-----------------------------


#-----------------------------
class APPLYSEMANTIC(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Possible",ctypes.c_int),
                ("Must",ctypes.c_int),
                ("Image",ctypes.c_int)]
#-----------------------------


#-----------------------------
class TGROUPSEMITEM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Code", ctypes.c_uint),
                ("Flag", ctypes.c_uint)]
#-----------------------------


#-----------------------------
class RSCFONT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Font",ctypes.c_char),
                ("Name",ctypes.c_char),
                ("CharSet",ctypes.c_byte),
                ("Flags",ctypes.c_byte),
                ("FixedChar",ctypes.c_byte),
                ("Reserve",ctypes.c_byte)]
#-----------------------------


#-----------------------------
class RSCRELATION(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("ObjectCode",ctypes.c_uint),
                ("SemanticCode",ctypes.c_uint),
                ("Prefix",ctypes.c_char),
                ("Decimal",ctypes.c_char)]
#-----------------------------


#-----------------------------
class BUILDMTW(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("StructSize",ctypes.c_int),
                ("NotCheckDiskFreeSpace",ctypes.c_int),
                ("BeginX",ctypes.c_double),
                ("BeginY",ctypes.c_double),
                ("Width",ctypes.c_double),
                ("Height",ctypes.c_double),
                ("ElemSizeMeters",ctypes.c_double),
                ("ElemSizeBytes",ctypes.c_int),
                ("Unit",ctypes.c_int),
                ("ReliefType",ctypes.c_int),
                ("UserType",ctypes.c_int),
                ("Scale",ctypes.c_int),
                ("HeightSuper",ctypes.c_int),
                ("FastBuilding",ctypes.c_int),
                ("Method",ctypes.c_int),
                ("Extremum",ctypes.c_int),
                ("Free",ctypes.c_int),
                ("Border",HOBJ),
                ("LimitMatrixFrame",ctypes.c_int),
                ("NotUse3DMetric",ctypes.c_int),
                ("SurfaceSquare3DObject",ctypes.c_int),
                ("AltitudeMarksNet",ctypes.c_int),
                ("LimitMatrixByFramesOfSheets",ctypes.c_int),
                ("ElemSizeMetersX",ctypes.c_double),
                ("Reserve",ctypes.c_char)]
#-----------------------------


#-----------------------------
class MTRPROJECTIONDATA(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("StructSize",ctypes.c_int),
                ("Free",ctypes.c_int),
                ("MapType",ctypes.c_int),
                ("ProjectionType",ctypes.c_int),
                ("FirstMainParallel",ctypes.c_double),
                ("SecondMainParallel",ctypes.c_double),
                ("AxisMeridian",ctypes.c_double),
                ("MainPointParallel",ctypes.c_double),
                ("PoleLatitude",ctypes.c_double),
                ("PoleLongitude",ctypes.c_double),
                ("EllipsoidKind",ctypes.c_int),
                ("HeightSystem",ctypes.c_int),
                ("CoordinateSystem",ctypes.c_int),
                ("ZoneNumber",ctypes.c_int),
                ("FalseEasting",ctypes.c_double),
                ("FalseNorthing",ctypes.c_double),
                ("ScaleFactor",ctypes.c_double),
                ("TurnAngle",ctypes.c_double),
                ("ZoneIdent",ctypes.c_int),
                ("Reserve",ctypes.c_char)]
#-----------------------------


#-----------------------------
class BUILDSURFACE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("StructSize",ctypes.c_uint),
                ("FileMtw",ctypes.c_int),
                ("BeginX",ctypes.c_double),
                ("BeginY",ctypes.c_double),
                ("Width",ctypes.c_double),
                ("Height",ctypes.c_double),
                ("MinValue",ctypes.c_double),
                ("MaxValue",ctypes.c_double),
                ("ElemSizeMeters",ctypes.c_double),
                ("UserType",ctypes.c_int),
                ("SearchSectorCount",ctypes.c_int),
                ("UserName",ctypes.c_char),
                ("Border",HOBJ),
                ("Handle",HWND),
                ("PaletteCount",ctypes.c_int),
                ("Method",ctypes.c_int),
                ("PointCount",ctypes.c_int),
                ("SemanticCode",ctypes.c_int),
                ("LocalSurfacePointCount",ctypes.c_int),
                ("LocalSurfaceRebuildPointCount",ctypes.c_int),
                ("MaxMetricCutLength",ctypes.c_double),
                ("Use3DMetric",ctypes.c_int),
                ("SemanticCode2",ctypes.c_int),
                ("FillBorderType",ctypes.c_int),
                ("IsMetricCutLength",ctypes.c_int),
                ("IsAddPointsInEmptyRegion",ctypes.c_int),
                ("IsLimitHeight",ctypes.c_int),
                ("DistBeforePointsInEmptyRegion",ctypes.c_double),
                ("LimitOffset",ctypes.c_double),
                ("Reserve",ctypes.c_char)]
#-----------------------------


#-----------------------------
class PROFBUILDPARMEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Point",DOUBLEPOINT),
                ("Object",HOBJ),
                ("ProfStepVertical",ctypes.c_int),
                ("ProfStepHorizontal",ctypes.c_int),
                ("DeltaRight",ctypes.c_double),
                ("DeltaCurrent",ctypes.c_double),
                ("DeltaLeft",ctypes.c_double),
                ("ColorProf",ctypes.c_long),
                ("ColorLine",ctypes.c_long),
                ("IsCurvatureEarth",ctypes.c_int),
                ("IsMiddleHeight",ctypes.c_int),
                ("IsLineFL",ctypes.c_int),
                ("IsLineFCL",ctypes.c_int),
                ("IsLineCross",ctypes.c_int),
                ("IsLineNet",ctypes.c_int),
                ("IsLineRelief",ctypes.c_int)]
#-----------------------------


#-----------------------------
class MAPOBJDESCEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("ListNumber",ctypes.c_int),
                ("ObjectNumber",ctypes.c_int),
                ("Map",HSITE)]
#-----------------------------


#-----------------------------
class CROSSPOINT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("XY",DOUBLEPOINT),
                ("H",ctypes.c_double),
                ("Zero1",HOBJ),
                ("Number1",ctypes.c_int),
                ("Subject1",ctypes.c_int),
                ("Zero2",HOBJ),
                ("Number2",ctypes.c_int),
                ("Subject2",ctypes.c_int)]
#-----------------------------


#-----------------------------
class PANELINFO(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("hInst",HINSTANCE),
                ("Count",ctypes.c_int),
                ("Name",ctypes.c_char)]
#-----------------------------


#-----------------------------
class PANELPOS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Rect",RECT),
                ("Position",ctypes.c_int),
                ("Layout",ctypes.c_int)]
#-----------------------------


#-----------------------------
class BUTTONINFO(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Command",ctypes.c_int),
                ("hBitmap",HBITMAP),
                ("Sibling",ctypes.c_int)]
#-----------------------------


#-----------------------------
class TASKBUTTONINFO(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("hTask",HINSTANCE),
                ("Command",ctypes.c_int),
                ("Sibling",ctypes.c_int),
                ("hBitmap",HBITMAP),
                ("Background",ctypes.c_int),
                ("State",ctypes.c_int),
                ("Enable",ctypes.c_int),
                ("Hint",WCHAR1),
                ("Comment",WCHAR1)]
#-----------------------------


#-----------------------------
class BUTTONINFOLX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("hBitmap",HBITMAP),
                ("Hint",ctypes.c_char)]
#-----------------------------


#-----------------------------
class CONTRINFO(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("CtrlId",ctypes.c_int),
                ("hWindow",HWND),
                ("Sibling",ctypes.c_int)]
#-----------------------------


#-----------------------------
class HITCONTROLINFO(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Position",POINT),
                ("CtrlID",ctypes.c_int)]
#-----------------------------


#-----------------------------
class ACTIONHEAD(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Ident",ctypes.c_short),
                ("Task",ctypes.c_ushort),
                ("Count",ctypes.c_ushort),
                ("Type",ctypes.c_ushort),
                ("Date",ctypes.c_uint),
                ("Time",ctypes.c_uint)]
#-----------------------------


#-----------------------------
class ACTIONRECORD(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Key",ctypes.c_int),
                ("Number",ctypes.c_int),
                ("Back",ctypes.c_int),
                ("Type",ctypes.c_byte),
                ("Mask",ctypes.c_byte),
                ("List",ctypes.c_short)]
#-----------------------------


#-----------------------------
class CHANGEINFO(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("hSite",HSITE),
                ("List",ctypes.c_short),
                ("Type",ctypes.c_byte),
                ("Mask",ctypes.c_byte),
                ("Key",ctypes.c_uint),
                ("Object",ctypes.c_uint)]
#-----------------------------


#-----------------------------
class FILEMAPPING(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("hFile",ctypes.c_void_p),
                ("hMapping",ctypes.c_void_p),
                ("Address",ctypes.c_char_p),
                ("Offset",ctypes.c_ulong),
                ("Size",ctypes.c_ulong),
                ("Shift",ctypes.c_ulong)]
#-----------------------------


#-----------------------------
class PUTTOMAPINFO(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Incode",ctypes.c_int),
                ("MapNumber",ctypes.c_int),
                ("Regime",ctypes.c_int)]
#-----------------------------


#-----------------------------
class NUMBERPOINT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Point",DOUBLEPOINT),
                ("Number",ctypes.c_int),
                ("Update",ctypes.c_int),
                ("Equal",ctypes.c_int),
                ("Reserve",ctypes.c_int)]
#-----------------------------


#-----------------------------
class COMMITOBJECTPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("MinCutLength",ctypes.c_double),
                ("MinCutLengthOnBorder",ctypes.c_double),
                ("Reserve",ctypes.c_char)]
#-----------------------------


#-----------------------------
class SAVEMAPCOMPPARMUN(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Titlsave",WCHAR1),
                ("MemoryRegister",ctypes.c_double),
                ("MemoryBuffer",ctypes.c_double),
                ("Buffer",ctypes.c_double),
                ("Memory",ctypes.c_double),
                ("Value",ctypes.c_double),
                ("Flagcomp",ctypes.c_int),
                ("Index",ctypes.c_int),
                ("Indexold",ctypes.c_int),
                ("IndexSq",ctypes.c_int),
                ("Flagshow",ctypes.c_int),
                ("Regnow",ctypes.c_int),
                ("Regold",ctypes.c_int),
                ("Flagreg",ctypes.c_int),
                ("StopFlag",ctypes.c_int),
                ("Precision",ctypes.c_int)]
#-----------------------------


#-----------------------------
class SEEKDIALOGPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Distance",ctypes.c_double),
                ("Handle",HMESSAGE),
                ("Condition",ctypes.c_int),
                ("Reserve",ctypes.c_int),
                ("IsShowList1",ctypes.c_int),
                ("IsShowList2",ctypes.c_int),
                ("CrossType",ctypes.c_int),
                ("SearchType",ctypes.c_int)]
#-----------------------------


#-----------------------------
class OLELOADPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("PosX",ctypes.c_double),
                ("PosY",ctypes.c_double),
                ("Height",ctypes.c_int),
                ("Width",ctypes.c_int),
                ("PosRight",ctypes.c_char),
                ("PosBottom",ctypes.c_char),
                ("Reserve",ctypes.c_char),
                ("Path",ctypes.c_char)]
#-----------------------------


#-----------------------------
class SETVIEWSCALE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("center",POINT),
                ("percent",ctypes.c_int),
                ("zero",ctypes.c_int)]
#-----------------------------


#-----------------------------
class VEGINDEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Index",ctypes.c_int),
                ("ColorCount",ctypes.c_int),
                ("Palette",RGBQUAD),
                ("RedBandNum",ctypes.c_int),
                ("NirBandNum",ctypes.c_int),
                ("L",ctypes.c_double),
                ("Reserv",ctypes.c_double)]
#-----------------------------


#-----------------------------
class AFFINCOEFBASE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("A0",ctypes.c_double),
                ("A1",ctypes.c_double),
                ("A2",ctypes.c_double),
                ("B0",ctypes.c_double),
                ("B1",ctypes.c_double),
                ("B2",ctypes.c_double)]
#-----------------------------


#-----------------------------
class AFFINCOEF(AFFINCOEFBASE):
    _pack_ = PACK_WIDTH
#-----------------------------


#-----------------------------
class TAFPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Levels",ctypes.POINTER(ctypes.c_int)),
                ("LevelCount",ctypes.c_int),
                ("Compress",ctypes.c_int),
                ("IsPredictor",ctypes.c_int),
                ("JPEGQuality",ctypes.c_int),
                ("IsJpegYCbCr",ctypes.c_int),
                ("DeflateLevel",ctypes.c_int),
                ("TileWidth",ctypes.c_int),
                ("TileHeight",ctypes.c_int)]
#-----------------------------


#-----------------------------
class CREATETIFPARMEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("BandCount",ctypes.c_int),
                ("BitInBand",ctypes.c_int),
                ("PixelType",ctypes.c_int),
                ("Compress",ctypes.c_int),
                ("IsPredictor",ctypes.c_int),
                ("JPEGQuality",ctypes.c_int),
                ("ColorSpace",ctypes.c_int),
                ("DeflateLevel",ctypes.c_int),
                ("TileWidth",ctypes.c_int),
                ("TileHeight",ctypes.c_int),
                ("BigTIFF",ctypes.c_int),
                ("IsPlane",ctypes.c_int),
                ("Palette",RGBQUAD),
                ("IsAlpha",ctypes.c_int),
                ("IsNoData",ctypes.c_int),
                ("NoData",ctypes.c_double),
                ("Reserved",ctypes.c_int)]
#-----------------------------


#-----------------------------
class BIRMETADATA(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Bbox",DFRAME),
                ("Version",WCHAR1),
                ("Class",WCHAR1),
                ("Scheme",WCHAR1),
                ("Name",WCHAR1),
                ("Attribution",WCHAR1),
                ("Region",WCHAR1),
                ("Code",WCHAR1),
                ("DataVersion",WCHAR1),
                ("Description",WCHAR1),
                ("Geoid",WCHAR1),
                ("SatteliteName",WCHAR1),
                ("SourceDate",WCHAR1),
                ("SourceTime",WCHAR1),
                ("UpdateTime",ctypes.c_int64),
                ("Sd",ctypes.c_double),
                ("MinResolution",ctypes.c_double),
                ("MaxResolution",ctypes.c_double),
                ("ViewAngle",ctypes.c_double),
                ("SunElevation",ctypes.c_double),
                ("SunAzimuth",ctypes.c_double),
                ("SatResolution",ctypes.c_double),
                ("SatSd",ctypes.c_double),
                ("TileFormat",ctypes.c_int),
                ("TileSize",ctypes.c_int),
                ("BirFormat",ctypes.c_int),
                ("EpsgCode",ctypes.c_int),
                ("MinZoom",ctypes.c_int),
                ("MaxZoom",ctypes.c_int),
                ("MinDate",ctypes.c_int),
                ("MaxDate",ctypes.c_int),
                ("DataSetZoom",ctypes.c_int),
                ("Bands",ctypes.c_int)]
#-----------------------------


#-----------------------------
class BLOBSTRUCT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("BlobSize",ctypes.c_int),
                ("Zero",ctypes.c_int)]
#-----------------------------


#-----------------------------
class ALSITEM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Ident",ctypes.c_int),
                ("Path",ctypes.c_char*(260)),
                ("Name",ctypes.c_char*(32)),
                ("Scale",ctypes.c_int),
                ("Minimum",ctypes.c_int),
                ("Maximum",ctypes.c_int),
                ("Priority",ctypes.c_int)]
#-----------------------------


#-----------------------------
class ALSITEMEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Ident",ctypes.c_int),
                ("Scale",ctypes.c_int),
                ("Minimum",ctypes.c_int),
                ("Maximum",ctypes.c_int),
                ("Priority",ctypes.c_int),
                ("Reserve",ctypes.c_int)]
#-----------------------------


#-----------------------------
class PROFBUILDPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Point",DOUBLEPOINT),
                ("Object",HOBJ),
                ("ProfStepVertical",ctypes.c_int),
                ("ProfStepHorizontal",ctypes.c_int)]
#-----------------------------


#-----------------------------
class TSQLMap_DBConnectParmEx_au1_as2(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Host",WCHAR1*(256*2)),
                ("Database",WCHAR1*(256*2)),
                ("User",WCHAR1*(256*2)),
                ("Password",WCHAR1*(256*2))]
class TSQLMap_DBConnectParmEx_au1(ctypes.Union):
    _pack_ = PACK_WIDTH
    _fields_ = [("_TSQLMap_DBConnectParmEx_au1_as2",TSQLMap_DBConnectParmEx_au1_as2),
                ("DatabaseFile",WCHAR1*(1024*2))]
class TSQLMap_DBConnectParmEx(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Name",WCHAR1*(256*2)),
                ("_TSQLMap_DBConnectParmEx_au1",TSQLMap_DBConnectParmEx_au1),
                ("CachePath",WCHAR1*(1024*2)),
                ("Port",ctypes.c_int),
                ("EncodePsw",ctypes.c_int),
                ("Authentication",ctypes.c_int),
                ("Dbms",ctypes.c_int)]
#-----------------------------


#-----------------------------
class FITTEXT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("TextHeight",ctypes.c_double),
                ("RectWidth",ctypes.c_double),
                ("RectHeight",ctypes.c_double),
                ("FactorWidth",ctypes.c_int),
                ("Fitting",ctypes.c_int),
                ("Interval",ctypes.c_int),
                ("Error",ctypes.c_int),
                ("CutTextToLines",ctypes.c_int),
                ("TruncateLongText",ctypes.c_int),
                ("Reserve",ctypes.c_int*(4))]
#-----------------------------


#-----------------------------
class IMPORTRASTERSPARAM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("CompressMethod",ctypes.c_int),
                ("CompressValue",ctypes.c_int),
                ("FlagTiffAccess",ctypes.c_int),
                ("FlagIgnoreGeoTag",ctypes.c_int),
                ("Reserve",ctypes.c_char*(256))]
#-----------------------------


#-----------------------------
class EXPORTMATRIXPARAM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("TileWidth",ctypes.c_int),
                ("TileHeight",ctypes.c_int),
                ("BigFile",ctypes.c_int),
                ("PixelType",ctypes.c_int),
                ("Compress",ctypes.c_int),
                ("DeflateLevel",ctypes.c_int),
                ("ClearAreaOutBorder",ctypes.c_int),
                ("UseFrame",ctypes.c_int),
                ("UsePseudoCode",ctypes.c_int),
                ("Reserve",ctypes.c_int*(45)),
                ("PseudoCode",ctypes.c_double),
                ("Frame",DFRAME)]
#-----------------------------


#-----------------------------
class OBJFROMRSC(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("hSelect",HSELECT),
                ("MapSelect",ctypes.c_int),
                ("Regime",ctypes.c_int),
                ("Repeat",ctypes.c_int)]
#-----------------------------

try:
    if os.environ['gisaccesdll']:
        gisaccesname = os.environ['gisaccesdll']
except KeyError:
    gisaccesname = 'gis64acces.dll'

try:
    curLib = mapsyst.LoadLibrary(gisaccesname)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Выдать сообщение об ошибке, code - код ошибки из maperr.rh
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    ErrorMessage_t = mapsyst.GetProcAddress(curLib,ctypes.c_void_p,'ErrorMessage', ctypes.c_int, ctypes.c_char_p)
    def ErrorMessage(_code: int, _filename: ctypes.c_char_p) -> ctypes.c_void_p:
        return ErrorMessage_t (_code, _filename)
    
except Exception as e:
    print(e)
    curLib = 0

def maptype_healthcheck(): 
    return 1