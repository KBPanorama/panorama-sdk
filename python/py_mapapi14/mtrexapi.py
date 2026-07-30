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
    *                Функции библиотеки gis64mtrex.dll                 *
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
# по морским картам с классификатором s57navy.rsc

SEMANTIC_CODE_174 = 174  # Код семантики 174 (ЗНАЧЕНИЕ ИЗОБАТЫ)
SEMANTIC_CODE_179 = 179  # Код семантики 179 (ЗНАЧЕНИЕ ГЛУБИНЫ)

# Тип модели, применяемой для вычисления теоретичекой вариограммы

KM_FIRST      = 0
KM_LAST       = 7
KM_SPHEROIDAL = 0  # Сферическая
KM_CIRCULAR   = 1  # Круговая
KM_TETRASPHER = 2  # Тетрасферическая
KM_PENTASPHER = 3  # Пентасферическая
KM_EXPONENT   = 4  # Экспоненциальная
KM_GAUSS      = 5  # Гауссова
KM_RATSQUARE  = 6  # Рациональная квадратичная
KM_HOLE       = 7  # Эффекта дыры

# Признак (внутри которого или между которыми) вычисляется ковариация в кокригинге

COVFEATUREMIN = 1
COVFEATUREMAX = 3
COVFEATURE1   = 1
COVFEATURE2   = 2
COVFEATURE12  = 3


#-----------------------------
class PRIORMTRPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Free",ctypes.c_int),
                ("AbsHeightDifference",ctypes.c_double),
                ("X",ctypes.c_double),
                ("Y",ctypes.c_double),
                ("Reserve",ctypes.c_double*(4))]
#-----------------------------


#-----------------------------
class SPREADPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Free",ctypes.c_int),
                ("hWnd",maptype.HMESSAGE),
                ("IterCount",ctypes.c_int),
                ("Palette",maptype.COLORREF*(256)),
                ("PaletteCount",ctypes.c_int),
                ("IsIterMtq",ctypes.c_int),
                ("IsAllEject",ctypes.c_int),
                ("EjectSize",ctypes.c_double),
                ("AbsorbHeight",ctypes.c_double),
                ("ElemSize",ctypes.c_double),
                ("WaveHeight",ctypes.c_double),
                ("Point",maptype.DOUBLEPOINT),
                ("Reserve",ctypes.c_char*(64))]
#-----------------------------


#-----------------------------
class WZONEPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Free",ctypes.c_int),
                ("Wnd",maptype.HMESSAGE),
                ("Map",maptype.HMAP),
                ("Select",maptype.HSELECT),
                ("Frame",maptype.DFRAME),
                ("ElemSize",ctypes.c_double),
                ("dH",ctypes.c_double),
                ("Reserved",ctypes.c_char*(64))]
#-----------------------------


#-----------------------------
class DEPTHMTQPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("StructSize",ctypes.c_int),
                ("Free",ctypes.c_int),
                ("MatrixType",ctypes.c_int),
                ("MatrixNumber",ctypes.c_int),
                ("BeginX",ctypes.c_double),
                ("BeginY",ctypes.c_double),
                ("Width",ctypes.c_double),
                ("Height",ctypes.c_double),
                ("MinValue",ctypes.c_double),
                ("MaxValue",ctypes.c_double),
                ("Level",ctypes.c_double),
                ("ElemSizeMeters",ctypes.c_double),
                ("UserLabel",ctypes.c_int),
                ("Free1",ctypes.c_int),
                ("Handle",maptype.HMESSAGE),
                ("Border",maptype.HOBJ),
                ("Reserve",ctypes.c_char*(128)),
                ("UserName",ctypes.c_char*(32))]
#-----------------------------


#-----------------------------
class CALCMATRIXPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("StructSize",ctypes.c_int),
                ("Free",ctypes.c_int),
                ("MatrixType",ctypes.c_int),
                ("MatrixNumber",ctypes.c_int),
                ("BeginX",ctypes.c_double),
                ("BeginY",ctypes.c_double),
                ("Width",ctypes.c_double),
                ("Height",ctypes.c_double),
                ("MinValue",ctypes.c_double),
                ("MaxValue",ctypes.c_double),
                ("ElemSizeMeters",ctypes.c_double),
                ("Level",ctypes.c_double),
                ("Handle",maptype.HMESSAGE),
                ("Border",maptype.HOBJ),
                ("CalcSquare",ctypes.c_char),
                ("CalcVolume",ctypes.c_char),
                ("CalcMinimun",ctypes.c_char),
                ("CalcMaximun",ctypes.c_char),
                ("CalcAverage",ctypes.c_char),
                ("CalcSquareWater",ctypes.c_char),
                ("CalcVolumeLayer",ctypes.c_char),
                ("CalcTypeReserve",ctypes.c_char),
                ("Square",ctypes.c_double),
                ("Volume",ctypes.c_double),
                ("Minimun",ctypes.c_double),
                ("Maximun",ctypes.c_double),
                ("Average",ctypes.c_double),
                ("SquareWater",ctypes.c_double),
                ("SquareShallowWater",ctypes.c_double),
                ("VolumeLayer",ctypes.c_double),
                ("LevelWater",ctypes.c_double),
                ("LayerTop",ctypes.c_double),
                ("LayerBottom",ctypes.c_double),
                ("Reserve",ctypes.c_char*(80))]
#-----------------------------


#-----------------------------
class BUILDZONEFLOODPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Free1",ctypes.c_int),
                ("Handle",maptype.HMESSAGE),
                ("Point1",maptype.DOUBLEPOINT),
                ("Point2",maptype.DOUBLEPOINT),
                ("Height1",ctypes.c_double),
                ("Height2",ctypes.c_double),
                ("Width",ctypes.c_double),
                ("ElementSize",ctypes.c_double),
                ("Object",maptype.HOBJ),
                ("Active",ctypes.c_int),
                ("Free2",ctypes.c_int),
                ("Reserve",ctypes.c_char*(64))]
#-----------------------------


#-----------------------------
class FLOOD_ZONE_BY_FAIRWAY(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("HydroSelect",maptype.HSELECT),
                ("ElementSize",ctypes.c_double),
                ("SemanticFlood",ctypes.c_int),
                ("IsDepthAbsolute",ctypes.c_int),
                ("MatrixExtention",ctypes.c_int),
                ("Vicinity",ctypes.c_int),
                ("DepthMaxDistance",ctypes.c_int),
                ("Zero",ctypes.c_int),
                ("Reserve",ctypes.c_char*(88))]
#-----------------------------


#-----------------------------
class HYDRO_LAY_PARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("HydroLineArr",ctypes.POINTER(ctypes.c_int)),
                ("HydroConstArr",ctypes.POINTER(ctypes.c_int)),
                ("HydroDiffArr",ctypes.POINTER(ctypes.c_int)),
                ("HydroLineCount",ctypes.c_int),
                ("HydroConstCount",ctypes.c_int),
                ("HydroDiffCount",ctypes.c_int),
                ("ProcMode",ctypes.c_int),
                ("LowRadius",ctypes.c_int),
                ("SmoothRadius",ctypes.c_int),
                ("MinConstSquare",ctypes.c_int),
                ("Approximation",ctypes.c_int),
                ("UseMetric",ctypes.c_int),
                ("UseSemantic",ctypes.c_int),
                ("SmoothSlope",ctypes.c_int),
                ("HydroPointCount",ctypes.c_int),
                ("HydroPointArr",ctypes.POINTER(ctypes.c_int)),
                ("Reserve",ctypes.c_char*(48))]
#-----------------------------


#-----------------------------
class BUILDFLOWPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("FlowObject",maptype.HOBJ),
                ("W",ctypes.c_double),
                ("Rt",ctypes.c_double),
                ("Uo",ctypes.c_double),
                ("FlowWidth",ctypes.c_double),
                ("SoilCategory",ctypes.c_int),
                ("FlagLess35",ctypes.c_int),
                ("MinPress",ctypes.c_double),
                ("MaxPress",ctypes.c_double),
                ("FlowType",ctypes.c_int),
                ("ErrorCode",ctypes.c_int),
                ("Reserve",ctypes.c_char*(80))]
#-----------------------------


#-----------------------------
class CREATEISOLINES(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Handle",maptype.HMESSAGE),
                ("Interval",ctypes.c_double),
                ("MinLengthUnclosedContour",ctypes.c_double),
                ("MinLengthClosedContour",ctypes.c_double),
                ("MinH",ctypes.c_double),
                ("MaxH",ctypes.c_double),
                ("CodeThick",ctypes.c_long),
                ("CodeMain",ctypes.c_long),
                ("CodeAdd",ctypes.c_long),
                ("CodeBerg",ctypes.c_long),
                ("CodeSemIndicatorValue",ctypes.c_long),
                ("CodeSemIndicatorName",ctypes.c_long),
                ("FlagSmooth",ctypes.c_long),
                ("StepThick",ctypes.c_long),
                ("IndicatorValueRequestType",ctypes.c_long),
                ("Free",ctypes.c_long),
                ("IndicatorName",maptype.WCHAR1*(512)),
                ("Reserve",ctypes.c_char*(432))]
#-----------------------------


#-----------------------------
class MTRCLASS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Min",ctypes.c_double),
                ("Max",ctypes.c_double),
                ("Excode",ctypes.c_int),
                ("SerialNum",ctypes.c_int),
                ("Color",ctypes.c_int),
                ("SemanticNumber",ctypes.c_int),
                ("SemanticMin",ctypes.c_int),
                ("SemanticMax",ctypes.c_int),
                ("SemanticColor",ctypes.c_int),
                ("Reserve",ctypes.c_int)]
#-----------------------------


#-----------------------------
class BUILDDENSITY(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Radius",ctypes.c_double),
                ("ElemSize",ctypes.c_double),
                ("Palette",maptype.COLORREF*(256)),
                ("PaletteCount",ctypes.c_int),
                ("Reserved",ctypes.c_int*(63))]
#-----------------------------


#-----------------------------
class BUILDVISIBLE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Radius",ctypes.c_double),
                ("ElemSize",ctypes.c_double),
                ("Color",maptype.COLORREF),
                ("Reserved",ctypes.c_int*(63))]
#-----------------------------




try:
    if os.environ['gismtrexdll']:
        gismtrexname = os.environ['gismtrexdll']
except KeyError:
    gismtrexname = 'gis64mtrex.dll'

try:
    mtrexlib = mapsyst.LoadLibrary(gismtrexname)
except Exception as e:
    print(e)
    mtrexlib = 0

if mtrexlib == 0:
    print(gismtrexname)
else:
    mtrCalcAbsoluteHeight_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrCalcAbsoluteHeight', maptype.HMAP, ctypes.POINTER(maptype.XYHDOUBLE))
    def mtrCalcAbsoluteHeight(_hmap: maptype.HMAP, _point: ctypes.POINTER(maptype.XYHDOUBLE)) -> int:
        """
        Вычислить значение абсолютной высоты в заданной точке по данным векторной карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _point: точка на карте, в которой вычисляется абсолютная высота (point->H) Координаты точки задаются в метрах в системе координат документа
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrCalcAbsoluteHeight_t (_hmap, _point)

    mtrCalcAbsoluteHeightBySectors_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_double,'mtrCalcAbsoluteHeightBySectors', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long)
    def mtrCalcAbsoluteHeightBySectors(_hmap: maptype.HMAP, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _sectorcount: int) -> float:
        """
        Вычислить значение абсолютной высоты в заданной точке по данным векторной карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _point: точка на карте, в которой вычисляется абсолютная высота Координаты точки задаются в метрах в системе координат документа
        
        :param _sectorcount: количество направлений для поиска окружающих высот (должно быть кратно ``4``, минимальное количество направлений ``= 4``, максимальное ``= 256``)
        
        :returns: Возвращает значение высоты в метрах В случае ошибки при вычислении высоты возвращает ERRORHEIGHT
        :rtype: float
        """
        return mtrCalcAbsoluteHeightBySectors_t (_hmap, _point, _sectorcount)

    mtrCalcCharacteristic_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrCalcCharacteristic', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def mtrCalcCharacteristic(_hmap: maptype.HMAP, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _semanticcode: int, _flagselect: int, _value: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Вычислить значение характеристики в заданной точке по данным векторной карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _point: точка на карте, в которой вычисляется характеристика Координаты точки задаются в метрах в системе координат векторной карты
        
        :param _semanticcode: характеристика (задается кодом семантики)
        
        :param _flagselect: флаг использования условий отбора объектов карты
        
        :param _value: вычисленное значение характеристики
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если flagselect ``= 0``, то выполняется поиск заданной характеристики
           по всем объектам векторной карты
           Если flagselect ``= 1``, то поиск заданной характеристики выполняется
           только по объектам, удовлетворяющим условиям отбора (HSELECT),
           установленным для векторной карты
        """
        return mtrCalcCharacteristic_t (_hmap, _point, _semanticcode, _flagselect, _value)

    mtrTryBuildUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrTryBuildUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.BUILDMTW), ctypes.POINTER(PRIORMTRPARM), maptype.HMESSAGE)
    def mtrTryBuildUn(_hmap: maptype.HMAP, _filtername: mapsyst.WTEXT, _buildparm: ctypes.POINTER(maptype.BUILDMTW), _priorparm: ctypes.POINTER(PRIORMTRPARM), _handle: maptype.HMESSAGE) -> int:
        """
        Предварительно оценить характеристики матрицы, создаваемой по векторной карте на заданный участок района работ
        
        :param _hmap: идентификатор открытых данных (документа) по которым строится матрица
        
        :param _filtername: полное имя фильтра объектов Вместе с картой может располагаться фильтр объектов - текстовый файл ``MTRCREA``.``IMH``, содержащий перечень кодов объектов, используемых при построении матрицы
        
        :param _buildparm: параметры создаваемой матрицы
        
        :param _priorparm: результаты предварительной оценки
        
        :param _handle: идентификатор окна диалога, которому посылаются сообщения о ходе процесса: ``0x0581`` - сообщение о проценте выполненных работ (в ``WPARAM``), если процесс должен быть принудительно завершен, в ответ должно вернуться значение ``0x0581``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если filtername равно нулю - фильтр объектов не используется
           Если handle равно нулю - сообщения не посылаются
           В процессе оценки выполняется преобразование исходных векторных данных района в растровый вид
        """
        return mtrTryBuildUn_t (_hmap, _filtername.buffer(), _buildparm, _priorparm, _handle)

    mtrBuildFloodZoneCallback_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrBuildFloodZoneCallback', maptype.HMAP, ctypes.c_long, maptype.PWCHAR, ctypes.POINTER(maptype.XYHDOUBLE), ctypes.c_long, ctypes.c_double, ctypes.c_double, maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p))
    def mtrBuildFloodZoneCallback(_hmap: maptype.HMAP, _isfloodzoneabs: int, _mtqname: mapsyst.WTEXT, _pointarray: ctypes.POINTER(maptype.XYHDOUBLE), _pointcount: int, _areaextension: float, _mindepth: float, _fcallback: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Построить зону затопления по набору отметок уровня воды
        
        :param _hmap: идентификатор открытых данных (документа) по которым строится зона затопления
        
        :param _mtqname: полное имя создаваемой матрицы качеств
        
        :param _pointarray: адрес массива точек с отметками уровня воды Координаты точек (pointarray->X, pointarray->Y) и значения уровня (pointarray->H) задаются в метрах в системе координат векторной карты. Размер массива в байтах должен быть не менее pointcount ``*`` sizeof(``XYHDOUBLE``), в противном случае возможны ошибки работы с памятью
        
        :param _pointcount: число точек в массиве pointarray
        
        :param _areaextension: положительное число, задающее величину расширения габаритов области в метрах
        
        :param _mindepth: положительное число, задающее минимальную глубину зоны затопления в метрах (глубины, меньшие minDepth в матрицу качеств не заносятся)
        
        :param _isfloodzoneabs: тип высоты во входных данных: !``= 0`` - во входных данных заданы абсолютные высоты ``0`` - во входных данных заданы относительные высоты (функции ``*ZoneAbs````*`` используют абсолютные высоты на входе)
        
        :param _fcallback: функция обратного вызова для сообщения статуса выполнения (процентов), это функция типа ``EVENTCALL`` (описание в maptype.h) первым параметром в нее будет возвращено значение eventparam, вторым - код сообщения (``0x0581``), в третьем параметре  - процент выполненной обработки, в чевертом параметре - адрес строки с названием выполняемого этапа
        
        :param _eventparam: параметр, передаваемый в функцию обратного вызова для идентификации отклика на вызывающей стороне При отправке сообщения ``WM_ERROR`` в первом параметре содержится целочисленный код ошибки, во втором параметре передается указатель на текст описания ошибки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если процесс должен быть принудительно завершен, в ответ должно вернуться значение ``0x0581``
           Если fcallback равно нулю - сообщения не посылаются
           Текст передается в кодировке Unicode (UTF16)
           В результате построения формируется матрица качеств, элементы
           которой содержат глубины в зоне затопления
           Габариты матрицы качеств определяются координатами точек с отметками уровня воды
           (массив pointarray) и величиной расширения габаритов области (areaextension)
        """
        return mtrBuildFloodZoneCallback_t (_hmap, _isfloodzoneabs, _mtqname.buffer(), _pointarray, _pointcount, _areaextension, _mindepth, _fcallback, _eventparam)

    mtrFloodZoneByObjectCallBack_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrFloodZoneByObjectCallBack', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(BUILDZONEFLOODPARM), maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p), maptype.HPAINT)
    def mtrFloodZoneByObjectCallBack(_hmap: maptype.HMAP, _mtqname: mapsyst.WTEXT, _sitename: mapsyst.WTEXT, _parm: ctypes.POINTER(BUILDZONEFLOODPARM), _fcallback: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p), _hpaint: maptype.HPAINT) -> int:
        """
        Построить зону затопления по объекту методом створов
        
        :param _hmap: идентификатор открытых данных (документа) Исходная карта должна содержать данные о рельефе
        
        :param _parm: параметры построения зоны затопления
        
        :param _mtqname: полное имя создаваемой матрицы качеств
        
        :param _sitename: имя пользовательской карты для записи объектов - зон затопления
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций Создается функцией mapCreatePaintControl, освобождается - mapFreePaintControl
        
        :param _fcallback: функция обратного вызова для сообщения статуса выполнения (процентов) Это функция типа ``EVENTCALL`` (описание в maptype.h), первым параметром в нее будет возвращено значение eventparam, вторым - тип сообщения (``WM_PROGRESSBARUN`` или ``WM_ERROR`` - описание в maptype.h), третий и четвертый параметры - в зависимости от типа сообщения Только для ОС Windows: В случаях, когда функция обратного вызова не задается, значение параметра parm.Handle задает идентификатор окна (``HWND``), которому, если он указан (!=``0``), будет оправлятся сообщение ``WM_PROGRESSBARUN`` (описание в maptype.h). Отправка уведомлений ``WM_PROGRESSBARUN``, ``WM_ERROR`` и прочих с помощью функции обратного вызова и с помощью SendMessage (в ОС Windows) полностью аналогичны. При этом параметры ``WPARAM`` и ``LPARAM`` сообщения Windows являются соответственно аналогами параметров value2 и value3 функции обратного вызова При отправке ``WM_PROGRESSBARUN`` со значением первого параметра -``1``, во втором параметре передается указатель на текст названия выполняемой задачи. Для остановки процесса выполнения в обработчике сообщения ``WM_PROGRESSBARUN`` следует установить результат (возвращаемое значение) равным значению ``WM_PROGRESSBARUN``. При отправке ``WM_ERROR`` в первом параметре содержится целочисленный код ошибки, во втором параметре передается указатель на текст описания ошибки Текст передается в кодировке Unicode (``UTF16``) В результате построения формируется матрица качеств, элементы которой содержат глубины в зоне затопления. В памяти создается пользовательская карта sitename с классификатором service.rsc Классификатор service.rsc должен находиться в одном каталоге с приложением или с hmap
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если задано sitename и  Active ``> 0`` (параметр Active из ``BUILDZONEFLOODPARM`` - флаг
           создания объектов), пользовательская карта будет записана на диск
        """
        return mtrFloodZoneByObjectCallBack_t (_hmap, _mtqname.buffer(), _sitename.buffer(), _parm, _fcallback, _eventparam, _hpaint)

    mtrFloodZoneByFairwayEx_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrFloodZoneByFairwayEx', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.POINTER(FLOOD_ZONE_BY_FAIRWAY), maptype.HMESSAGE)
    def mtrFloodZoneByFairwayEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _mtqname: mapsyst.WTEXT, _floodlineparm: ctypes.POINTER(FLOOD_ZONE_BY_FAIRWAY), _handle: maptype.HMESSAGE) -> int:
        """
        Построить зону затопления по фарватеру
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор открытой пользовательской карты
        
        :param _mtqname: имя создаваемой матрицы качеств
        
        :param _floodlineparm: параметры построения зоны затопления по фарватеру
        
        :param _handle: в Linux - адрес функции обратного вызова, в Windows - идентификатор окна диалога для приёма сообщений ``WM_PROGRESSBARUN`` - сообщение с процентом выполнения (``WPARAM``) и названием процесса (``LPARAM``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если процесс должен быть принудительно завершен, в ответ
           должно вернуться значение WM_PROGRESSBARUN
        """
        return mtrFloodZoneByFairwayEx_t (_hmap, _hsite, _mtqname.buffer(), _floodlineparm, _handle)

    mtrCoordinateHydrography_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrCoordinateHydrography', maptype.HMAP, maptype.HSITE, ctypes.POINTER(HYDRO_LAY_PARM), maptype.HMESSAGE)
    def mtrCoordinateHydrography(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hydrolayparm: ctypes.POINTER(HYDRO_LAY_PARM), _handle: maptype.HMESSAGE) -> int:
        """
        Согласовать объекты гидрографии и матрицы высот
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор открытой пользовательской карты
        
        :param _hydrolayparm: структура параметров задачи
        
        :param _handle: в Linux - адрес функции обратного вызова, в Windows - идентификатор окна диалога для приёма сообщений ``WM_PROGRESSBARUN`` - сообщение с процентом выполнения (``WPARAM``) и названием этапа (``LPARAM``) При согласовании объектов гидрографии друг с другом матрицы высот не используются При согласовании объектов гидрографии с матрицами высот, используются все матрицы высот, которые открыты в исходной карте
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrCoordinateHydrography_t (_hmap, _hsite, _hydrolayparm, _handle)

    mtrWaterZoneUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrWaterZoneUn', maptype.PWCHAR, ctypes.POINTER(WZONEPARM))
    def mtrWaterZoneUn(_mtqname: mapsyst.WTEXT, _parm: ctypes.POINTER(WZONEPARM)) -> int:
        """
        Cоздать матрицу водно-балансных бассейнов
        
        :param _mtqname: имя создаваемой матрицы водно-балансных бассейнов
        
        :param _parm: параметры вызова Элемент матрицы качеств содержит ключ объекта, к которому относится бассейн
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrWaterZoneUn_t (_mtqname.buffer(), _parm)

    mtrBuildDepthMtqCallBack_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrBuildDepthMtqCallBack', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(DEPTHMTQPARM), ctypes.POINTER(maptype.COLORREF), ctypes.c_long, maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p))
    def mtrBuildDepthMtqCallBack(_hmap: maptype.HMAP, _depthmtqname: mapsyst.WTEXT, _depthmtqparm: ctypes.POINTER(DEPTHMTQPARM), _palette: ctypes.POINTER(maptype.COLORREF), _palettecount: int, _fcallback: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Построить матрицу глубин (матрицу качеств mtq)
        
        :param _hmap: идентификатор открытых данных (документа) (карта обеспеченная данными о рельефе дна)
        
        :param _depthmtqname: полное имя создаваемой матрицы
        
        :param _depthmtqparm: параметры построения
        
        :param _palette: адрес палитры создаваемой матрицы (если равен нулю, используется палитра по умолчанию)
        
        :param _palettecount: число цветов палитры
        
        :param _fcallback: функция обратного вызова для сообщения статуса выполнения (процентов), это функция типа ``EVENTCALL`` (описание в maptype.h), первым параметром в нее будет возвращено значение eventparam, вторым - тип сообщения (``AM_MTRNOTIFY`` (``0x0581``) или ``WM_ERROR`` - описание в maptype.h), третий и четвертый параметры - в зависимости от типа сообщения. Только для ОС Windows: В случаях, когда функция обратного вызова не задается значение параметра depthmtqparm.Handle задает идентификатор окна (``HWND``), которому, если он указан (!=``0``), будет оправлятся сообщение ``AM_MTRNOTIFY`` (``0x0581``). Отправка уведомлений ``WM_PROGRESSBARUN``, ``WM_ERROR`` и прочих с помощью функции обратного вызова и с помощью SendMessage (в ОС Windows) полностью аналогичны. При этом параметры ``WPARAM`` и ``LPARAM`` сообщения Windows являются соответственно аналогами параметров value2 и value3 функции обратного вызова. Для остановки процесса выполнения в обработчике сообщения ``AM_MTRNOTIFY`` следует установить результат (возвращаемое значение) равным значению ``AM_MTRNOTIFY``. При отправке ``WM_ERROR`` в первом параметре содержится целочисленный код ошибки, во втором параметре передается указатель на текст описания ошибки. Текст передается в кодировке Unicode (``UTF16``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrBuildDepthMtqCallBack_t (_hmap, _depthmtqname.buffer(), _depthmtqparm, _palette, _palettecount, _fcallback, _eventparam)

    mtrBuildFlowMtq_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrBuildFlowMtq', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(BUILDFLOWPARM), maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p), maptype.HPAINT)
    def mtrBuildFlowMtq(_hmap: maptype.HMAP, _mtqname: mapsyst.WTEXT, _parm: ctypes.POINTER(BUILDFLOWPARM), _fcallback: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p), _hpaint: maptype.HPAINT) -> int:
        """
        Построить матрицу давлений селевого потока
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _mtqname: имя матрицы давлений
        
        :param _parm: параметры построения матрицы давлений
        
        :param _fcallback: функция обратного вызова для сообщения процентов выполнения
        
        :param _eventparam: параметры функции обратного вызова
        
        :param _hpaint: контекст отображения для многопоточного вызова Значения кода ошибки приведены в описании структуры ``BUILDFLOWPARM``
        
        :returns: При ошибке возвращает ноль и заносит код ошибки в parm->ErrorCode
        :rtype: int
        """
        return mtrBuildFlowMtq_t (_hmap, _mtqname.buffer(), _parm, _fcallback, _eventparam, _hpaint)

    mtrMakeFlowTrace_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrMakeFlowTrace', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(ctypes.c_long), maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p), maptype.HPAINT)
    def mtrMakeFlowTrace(_hmap: maptype.HMAP, _flowtrace: maptype.HOBJ, _p1: ctypes.POINTER(maptype.DOUBLEPOINT), _p2: ctypes.POINTER(maptype.DOUBLEPOINT), _errorcode: ctypes.POINTER(ctypes.c_long), _fcallback: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p), _hpaint: maptype.HPAINT) -> int:
        """
        Построить линейный объект русла потока
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _flowtrace: объект-контейнер для занесения метрики русла, созданный функцией mapCreateObject (для сохранения объекта русла вызвать mapCommitObjectAsNew)
        
        :param _p1: точка начала русла
        
        :param _p2: точка конца русла Высота рельефа в точке p1 должна быть больше высоты в точке p2
        
        :param _errorcode: код ошибки Значения кода ошибки: ``1`` - Ошибка входных параметров ``2`` - Заданные точки начала и конца русла не обеспечены высотами рельефа ``3`` - Расстояние между заданными точками начала и конца русла меньше элемента матрицы высот ``4`` - Высота в точке начала русла меньше высоты в точке конца русла ``5`` - Расстояние между точками начала и конца русла недостаточно для профилирования матрицы высот
        
        :param _fcallback: функция обратного вызова для сообщения процентов выполнения
        
        :param _eventparam: параметры функции обратного вызова
        
        :param _hpaint: контекст отображения для многопоточного вызова
        
        :returns: В случае ошибки возвращает 0 и заносит код ошибки в errorcode
        :rtype: int
        """
        return mtrMakeFlowTrace_t (_hmap, _flowtrace, _p1, _p2, _errorcode, _fcallback, _eventparam, _hpaint)

    mtrCalcInclineInPoint_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrCalcInclineInPoint', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mtrCalcInclineInPoint(_hmap: maptype.HMAP, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _incline: ctypes.POINTER(ctypes.c_double), _azimuth: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Вычислить значение максимального уклона и направления максимального уклона (азимут) в заданной точке
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _point: точка на карте в метрах в системе координат документа
        
        :param _incline: рассчитанное значение уклона в радианах
        
        :param _azimuth: рассчитанное значение азимута радианах Для вычислений в заданной точке в составе документа должна быть матрица высот в заданной области
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrCalcInclineInPoint_t (_hmap, _point, _incline, _azimuth)

    mtrBuildRasterUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrBuildRasterUn', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(maptype.BUILDMTW), maptype.HMESSAGE)
    def mtrBuildRasterUn(_hmap: maptype.HMAP, _rstname: mapsyst.WTEXT, _filtername: mapsyst.WTEXT, _rstparm: ctypes.POINTER(maptype.BUILDMTW), _handle: maptype.HMESSAGE) -> int:
        """
        Построить растр качеств по векторной карте на заданный участок района работ
        
        :param _hmap: идентификатор открытых данных (документа) по которым строится растр качеств
        
        :param _rstname: полное имя создаваемого растра
        
        :param _filtername: полное имя служебного текстового файла Вместе с картой должен располагаться фильтр объектов - служебный текстовый файл map2rsw.ini, содержащий перечень кодов объектов, используемых при построении растра
        
        :param _rstparm: параметры создаваемого растра
        
        :param _handle: идентификатор окна диалога, которому посылаются сообщения о ходе процесса: ``0x0581`` - сообщение о проценте выполненных работ (в ``WPARAM``),  если процесс должен быть принудительно завершен, в ответ должно вернуться значение ``0x0581``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если handle равно нулю - сообщения не посылаются
        """
        return mtrBuildRasterUn_t (_hmap, _rstname.buffer(), _filtername.buffer(), _rstparm, _handle)

    mtrBuildMtq_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrBuildMtq', maptype.HMAP, ctypes.c_char_p, ctypes.POINTER(maptype.COLORREF), ctypes.c_long, ctypes.POINTER(maptype.XYHDOUBLE), ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_double, maptype.HMESSAGE)
    def mtrBuildMtq(_hmap: maptype.HMAP, _mtqname: ctypes.c_char_p, _palette: ctypes.POINTER(maptype.COLORREF), _countpalette: int, _pointarray: ctypes.POINTER(maptype.XYHDOUBLE), _pointcount: int, _elemsizemeters: float, _minvalue: float, _maxvalue: float, _handle: maptype.HMESSAGE) -> int:
        """
        Построить матрицу качеств по массиву значений характеристики качества
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _mtqname: полное имя создаваемой матрицы качеств
        
        :param _palette: адрес палитры создаваемой матрицы качеств
        
        :param _countpalette: количество цветов в палитре
        
        :param _pointarray: адрес массива значений характеристики качества Координаты точек (pointarray->X, pointarray->Y) задаются в метрах в системе координат векторной карты Размер массива в байтах должен быть не менее pointcount ``*`` sizeof(``XYHDOUBLE``), в противном случае возможны ошибки работы с памятью
        
        :param _pointcount: число точек в массиве pointarray
        
        :param _elemsizemeters: размер стороны элементарного участка в метрах на местности (дискрет матрицы)
        
        :param _minvalue: минимальное значение диапазона значений характеристики качества создаваемой матрицы
        
        :param _maxvalue: максимальное значение диапазона значений характеристики качества создаваемой матрицы
        
        :param _handle: идентификатор окна диалога, которому посылаются сообщения о ходе процесса: ``0x0581`` - сообщение о проценте выполненных работ (в ``WPARAM``), если процесс должен быть принудительно завершен, в ответ должно вернуться значение ``0x0581``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если minvalue >= maxvalue, то в матрицу заносится фактический диапазон значений из
           массива pointarray
           Если handle равно нулю - сообщения не посылаются
        """
        return mtrBuildMtq_t (_hmap, _mtqname, _palette, _countpalette, _pointarray, _pointcount, _elemsizemeters, _minvalue, _maxvalue, _handle)

    mtrBuildMatrixSurfaceUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrBuildMatrixSurfaceUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.BUILDSURFACE))
    def mtrBuildMatrixSurfaceUn(_hmap: maptype.HMAP, _mtrname: mapsyst.WTEXT, _mtrparm: ctypes.POINTER(maptype.BUILDSURFACE)) -> int:
        """
        Построить матрицу поверхности (матрицу качеств или матрицу высот) по данным векторной карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _mtrname: полное имя создаваемой матрицы
        
        :param _mtrparm: параметры создаваемой матрицы (структура ``BUILDSURFACE`` описана в maptype.h)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если mtrparm->FileMtw равно 1, то строится матрица высот (``*.mtw``),
           иначе строится матрица качеств (``*.mtq``)
        """
        return mtrBuildMatrixSurfaceUn_t (_hmap, _mtrname.buffer(), _mtrparm)

    mtrPutMtqLineZone_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrPutMtqLineZone', maptype.HMAP, ctypes.c_long, maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mtrPutMtqLineZone(_hmap: maptype.HMAP, _number: int, _linehobj: maptype.HOBJ, _width: float, _value: float, _regime: int) -> int:
        """
        Занести в матрицу качеств зону вдоль линейного объекта
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: номер матрицы качеств в цепочке
        
        :param _linehobj: линейный объект
        
        :param _width: ширина зоны в метрах
        
        :param _value: значение, заносимое в элементы зоны
        
        :param _regime: режим занесения значения (``0`` - без учёта ранее занесённого значения)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrPutMtqLineZone_t (_hmap, _number, _linehobj, _width, _value, _regime)

    mtrPutMtqLineZoneForPolygon_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrPutMtqLineZoneForPolygon', maptype.HMAP, ctypes.c_long, maptype.HOBJ, maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mtrPutMtqLineZoneForPolygon(_hmap: maptype.HMAP, _number: int, _linehobj: maptype.HOBJ, _polygonhobj: maptype.HOBJ, _width: float, _zonevalue: float, _polygonvalue: float, _regime: int) -> int:
        """
        Занести в матрицу качеств зону вдоль линейного объекта в границах площадного объекта
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: номер матрицы качеств в цепочке
        
        :param _linehobj: линейный объект
        
        :param _polygonhobj: площадной объект
        
        :param _width: ширина зоны в метрах
        
        :param _zonevalue: значение, заносимое в элементы зоны
        
        :param _polygonvalue: значение, заносимое в элементы площадного объекта
        
        :param _regime: режим занесения значения (``0`` - без учёта ранее занесённого значения)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrPutMtqLineZoneForPolygon_t (_hmap, _number, _linehobj, _polygonhobj, _width, _zonevalue, _polygonvalue, _regime)

    mtrLiquidSpreadingCallBack_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrLiquidSpreadingCallBack', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(SPREADPARM), maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p), ctypes.c_int, maptype.HPAINT)
    def mtrLiquidSpreadingCallBack(_hmap: maptype.HMAP, _mtqname: mapsyst.WTEXT, _parm: ctypes.POINTER(SPREADPARM), _fcallback: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p), _append: int, _hpaint: maptype.HPAINT) -> int:
        """
        Создать матрицу качеств растекания жидкости
        
        :param _hmap: идентификатор открытых данных (должна быть открыта хотя бы одна матрица высот)
        
        :param _mtqname: имя создаваемой матрицы качеств растекания, если матрицы создаются на каждой итерации,
        
        :param _parm: параметры вызова
        
        :param _fcallback: функция обратного вызова для сообщения статуса выполнения (процентов)
        
        :param _eventparam: параметры функции обратного вызова
        
        :param _append: признак необходимости добавить созданную матрицу к карте
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций, создается функцией mapCreatePaintControl, освобождается - mapFreePaintControl Функция обратного вызова fcallback - это функция типа ``EVENTCALL`` (описание в maptype.h), первым параметром в нее будет возвращено значение eventparam, вторым - код сообщения ``0x0581``, третий - процент выполнения Только для ОС Windows: В случаях, когда функция обратного вызова не задается, значение параметра parm.Handle задает идентификатор окна (``HWND``), которому, если он указан (!=``0``), будет оправлятся сообщение ``0x0581`` со значением процента выполнения в WParam Заполненные элементы матрицы содержат толщину слоя растекшейся жидкости
        
        :returns: При успешном выполнении возвращает номер файла в цепочке матриц (или 1, если append ``= 0``) При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           то в конце имени добавляется номер итерации (для первой = mtqname_1.mtq)
        """
        return mtrLiquidSpreadingCallBack_t (_hmap, _mtqname.buffer(), _parm, _fcallback, _eventparam, _append, _hpaint)

    mtrCalcMtqZoneSquare_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrCalcMtqZoneSquare', maptype.HMAP, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double))
    def mtrCalcMtqZoneSquare(_hmap: maptype.HMAP, _number: int, _minvalue: float, _maxvalue: float, _zonesquare: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Вычислить площадь зоны по матрице качеств
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: номер матрицы качеств в цепочке
        
        :param _minvalue: минимальное значение диапазона значений элементов, участвующих в вычислении площади
        
        :param _maxvalue: максимальное значение диапазона значений элементов, участвующих в вычислении площади
        
        :param _zonesquare: вычисленное значение площади
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если minvalue > maxvalue, то площадь вычисляется по всем заполненым элементам матрицы
        """
        return mtrCalcMtqZoneSquare_t (_hmap, _number, _minvalue, _maxvalue, _zonesquare)

    MtwProjectionReformingEvent_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'MtwProjectionReformingEvent', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_long, ctypes.POINTER(mapcreat.LOCALTRANSFORM), maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p))
    def MtwProjectionReformingEvent(_handle: maptype.HMESSAGE, _namein: mapsyst.WTEXT, _nameout: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM), _hevent: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Преобразовать матрицу высот (MTW) или матрицу качеств (MTQ) к заданной проекции
        
        :param _handle: диалог визуального сопровождения процесса обработки
        
        :param _namein: имя исходной матрицы
        
        :param _nameout: имя выходной матрицы
        
        :param _mapreg: адрес структуры с данными о заданной проекции
        
        :param _datum: параметры пересчета геодезических координат с заданного эллипсоида на эллипсоид ``WGS``-``84`` (может быть ноль)
        
        :param _ellparam: параметры пользовательского эллипсоида (может быть ноль)
        
        :param _ttype: тип локального преобразования координат (описание ``TRANSFORMTYPE`` в mapcreat.h) или ``0``
        
        :param _tparm: параметры локального преобразования координат (описание в mapcreat.h)
        
        :param _hevent: адрес функции обратного вызова для уведомлении о процессе
        
        :param _eventparam: параметры функции обратного вызова Диалогу визуального сопровождения процесса обработки посылаются сообщения ``WM_PROGRESSBAR``/``WM_PROGRESSBARUN``: Извещение об изменении состояния процесса, ``WPARAM`` - текущее состояние процесса в процентах (``0````%`` - ``100````%``)
        
        :returns: Если функция-отклик возвращает WM_PROGRESSBAR/WM_PROGRESSBARUN, то процесс завершается Описание структур MAPREGISTEREX, DATUMPARAM, ``ELLIPSOIDPARAM`` - mapcreat.h При ошибке возвращает ноль
        :rtype: int
        """
        return MtwProjectionReformingEvent_t (_handle, _namein.buffer(), _nameout.buffer(), _mapreg, _datum, _ellparam, _ttype, _tparm, _hevent, _eventparam)

    mtrCalcByMatrix_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrCalcByMatrix', maptype.HMAP, ctypes.POINTER(CALCMATRIXPARM))
    def mtrCalcByMatrix(_hmap: maptype.HMAP, _calcmatrixparm: ctypes.POINTER(CALCMATRIXPARM)) -> int:
        """
        Вычислить статистику по матрице высот (mtw) или матрице качеств (mtq)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _calcmatrixparm: параметры и результаты вычислений При наличии данных (значений качества) для вычисления статистики в области,
        
        :returns: заданной параметрами calcmatrixparm, возвращает 1 При отсутствии данных (значений качества) в заданной области возвращает 0
        :rtype: int
        """
        return mtrCalcByMatrix_t (_hmap, _calcmatrixparm)

    mtrSmoothMtrUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrSmoothMtrUn', maptype.PWCHAR, ctypes.c_double, maptype.HMESSAGE, ctypes.c_long)
    def mtrSmoothMtrUn(_mtrname: mapsyst.WTEXT, _smoothfactor: float, _handle: maptype.HMESSAGE, _messageid: int) -> int:
        """
        Построить сплайн сглаживания матрицы высот
        
        :param _mtrname: полное имя сглаживаемой матрицы
        
        :param _smoothfactor: уровень сглаживания от ``0`` до ``1: 0`` - прямая линия, ``1`` - кубический сплайн
        
        :param _handle: идентификатор окна диалога, которому посылаются сообщения о ходе процесса (процент обработки)
        
        :param _messageid: идентификатор сообщения с процентом обработки Для сглаживания матрицы запрашивается оперативная память в размере (RowCount``*``ColCount``*````16``) байт, где RowCount - количество строк матрицы, ColCount - количество столбцов матрицы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если handle ``= 0``, то сообщения не посылаются
        """
        return mtrSmoothMtrUn_t (_mtrname.buffer(), _smoothfactor, _handle, _messageid)

    mtrBuildDifferenceMatrix_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrBuildDifferenceMatrix', maptype.HMESSAGE, maptype.HMAP, maptype.HOBJ, maptype.PWCHAR, ctypes.POINTER(maptype.BUILDMTW), ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mtrBuildDifferenceMatrix(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP, _hobj: maptype.HOBJ, _mtwname: mapsyst.WTEXT, _mtwparam: ctypes.POINTER(maptype.BUILDMTW), _number1: int, _number2: int, _modulus: int) -> int:
        """
        Построить разницу двух матриц и сохранить в новую матрицу относительных высот
        
        :param _handle: идентификатор окна диалога, которому посылаются сообщения о ходе процесса (процент обработки) ``WM_PROGRESSBAR``
        
        :param _hmap: идентификатор документа с открытыми матрицами
        
        :param _hobj: рамка области для отображения результирующей матрицы
        
        :param _mtwname: имя создаваемой матрицы
        
        :param _mtwparam: параметры создаваемой матрицы
        
        :param _number1: номер первой матрицы в документе
        
        :param _number2: номер второй матрицы в документе
        
        :param _modulus: признак записи разницы высот в матрицах по модулю
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если handle ``= 0``, то сообщения не посылаются
        """
        return mtrBuildDifferenceMatrix_t (_handle, _hmap, _hobj, _mtwname.buffer(), _mtwparam, _number1, _number2, _modulus)

    mtrKrigingCreate_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_void_p,'mtrKrigingCreate', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.BUILDSURFACE), ctypes.POINTER(ctypes.c_double))
    def mtrKrigingCreate(_hmap: maptype.HMAP, _hsit: maptype.HSITE, _mtrparm: ctypes.POINTER(maptype.BUILDSURFACE), _ranges: ctypes.POINTER(ctypes.c_double)) -> ctypes.c_void_p:
        """
        Создать класс кригинга
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsit: идентификатор открытой пользовательской карты
        
        :param _mtrparm: параметры построения матрицы
        
        :param _ranges: для матриц качеств диапазон значений для палитры (при ``0`` не устанавливается)
        
        :returns: При ошибке возвращает ноль
        """
        return mtrKrigingCreate_t (_hmap, _hsit, _mtrparm, _ranges)

    mtrKrigingFree_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_void_p,'mtrKrigingFree', ctypes.c_void_p)
    def mtrKrigingFree(_kriging: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Освободить класса кригинга
        
        :param _kriging: идентификатор созданного класса кригинга
        """
        return mtrKrigingFree_t (_kriging)

    mtrKrigingGetMinMaxDistance_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrKrigingGetMinMaxDistance', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mtrKrigingGetMinMaxDistance(_kriging: ctypes.c_void_p, _min: ctypes.POINTER(ctypes.c_double), _max: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить минимальное и максимальное расстояние между точками
        
        :param _kriging: идентификатор созданного класса кригинга
        
        :param _min: возвращаемое минимальное расстояние между точками (только узловыми)
        
        :param _max: возвращаемое максимальное расстояние между точками
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrKrigingGetMinMaxDistance_t (_kriging, _min, _max)

    mtrKrigingSetEmpiricalVariograms_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrKrigingSetEmpiricalVariograms', ctypes.c_void_p, ctypes.c_double, ctypes.c_int)
    def mtrKrigingSetEmpiricalVariograms(_kriging: ctypes.c_void_p, _lagsize: float, _lagcount: int) -> int:
        """
        Вычислить эмпирическую вариограмму для лагов
        
        :param _kriging: идентификатор созданного класса кригинга
        
        :param _lagsize: размер лага в метрах (для всего диапазона LagSize = MaxDist / LagCount)
        
        :param _lagcount: количество лагов Лаг - диапазон расстояний между парами точек, для которых вычисляется эмпирическая вариограмма
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrKrigingSetEmpiricalVariograms_t (_kriging, _lagsize, _lagcount)

    mtrKrigingGetEmpiricalVariogram_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrKrigingGetEmpiricalVariogram', ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_int))
    def mtrKrigingGetEmpiricalVariogram(_kriging: ctypes.c_void_p, _lagnum: int, _variogram: ctypes.POINTER(ctypes.c_double), _dist: ctypes.POINTER(ctypes.c_double), _pointcount: ctypes.POINTER(ctypes.c_int)) -> int:
        """
        Запросить параметры эмпирической вариограммы для лага
        
        :param _kriging: идентификатор созданного класса кригинга
        
        :param _lagnum: номер лага, для которого возвращаются параметры
        
        :param _variogram: эмпирическая вариограмма = sum(dH ``*`` dH) / ``2``
        
        :param _dist: центр лага по оси расстояний между парами точек = lagnum ``*`` lagsize + lagszie / ``2``
        
        :param _pointcount: количество пар точек, попавших в диапазон лага
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrKrigingGetEmpiricalVariogram_t (_kriging, _lagnum, _variogram, _dist, _pointcount)

    mtrKrigingSetTeoreticalVariograms_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrKrigingSetTeoreticalVariograms', ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mtrKrigingSetTeoreticalVariograms(_kriging: ctypes.c_void_p, _modeltype: int, _range: ctypes.POINTER(ctypes.c_double), _sill: ctypes.POINTER(ctypes.c_double), _nugget: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Вычислить параметры модели, применяемой для вычисления теоретичекой вариограммы
        
        :param _kriging: идентификатор созданного класса кригинга
        
        :param _modeltype: тип модели
        
        :param _range: радиус модели (метры) - точка на оси расстояний между точками после которой кривая становится горизонтальной
        
        :param _sill: порог - значение, которое принимает теоретическая вариограмма в точке радиуса модели, из которого вычтено значение самородка
        
        :param _nugget: самородок - точка в которой кривая пересекает ось вариограммы Теоретически для нулевого расстояния между точками, изменение функции должно быть равно ``0``. Однако при бесконечно малых расстояниях разница между измерениями зачастую не стремится к нулю.
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если ``= -1`` - то значение вычисляется, если ``> 0``, то устанавливается
           Если ``= -1`` - то значение вычисляется, если ``> 0``, то устанавливается
           Если ``= -1`` - то значение вычисляется, если >``= 0``, то устанавливается
        """
        return mtrKrigingSetTeoreticalVariograms_t (_kriging, _modeltype, _range, _sill, _nugget)

    mtrKrigingGetTeoreticalVariogram_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrKrigingGetTeoreticalVariogram', ctypes.c_void_p, ctypes.c_double, ctypes.POINTER(ctypes.c_double))
    def mtrKrigingGetTeoreticalVariogram(_kriging: ctypes.c_void_p, _dist: float, _var: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Вычислить значение теоретической вариограммы по расстоянию между двумя точками
        
        :param _kriging: идентификатор созданного класса кригинга
        
        :param _dist: расстояние от начала
        
        :param _var: значение теоретической вариограммы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrKrigingGetTeoreticalVariogram_t (_kriging, _dist, _var)

    mtrKrigingBuildUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrKrigingBuildUn', ctypes.c_void_p, maptype.PWCHAR)
    def mtrKrigingBuildUn(_kriging: ctypes.c_void_p, _mtrname: mapsyst.WTEXT) -> int:
        """
        Построить матрицу
        
        :param _kriging: идентификатор созданного класса кригинга
        
        :param _mtrname: имя создаваемой маррицы высот или качеств
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrKrigingBuildUn_t (_kriging, _mtrname.buffer())

    mtrCokrigingCreate_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_void_p,'mtrCokrigingCreate', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.BUILDSURFACE), ctypes.POINTER(ctypes.c_double))
    def mtrCokrigingCreate(_hmap: maptype.HMAP, _hsit: maptype.HSITE, _mtrparm: ctypes.POINTER(maptype.BUILDSURFACE), _ranges: ctypes.POINTER(ctypes.c_double)) -> ctypes.c_void_p:
        """
        Создание класса кокригинга
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsit: идентификатор открытой пользовательской карты
        
        :param _mtrparm: параметры построения матрицы
        
        :param _ranges: для матриц качеств диапазон значений для палитры (при ``0`` не устанавливается)
        
        :returns: При ошибке возвращает ноль
        """
        return mtrCokrigingCreate_t (_hmap, _hsit, _mtrparm, _ranges)

    mtrCokrigingFree_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_void_p,'mtrCokrigingFree', ctypes.c_void_p)
    def mtrCokrigingFree(_cokriging: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Освобождение класса кокригинга
        
        :param _cokriging: идентификатор созданного класса кокригинга
        """
        return mtrCokrigingFree_t (_cokriging)

    mtrCokrigingGetMinMaxDistance_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrCokrigingGetMinMaxDistance', ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mtrCokrigingGetMinMaxDistance(_cokriging: ctypes.c_void_p, _feature: int, _min: ctypes.POINTER(ctypes.c_double), _max: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить минимальное и максимальное расстояние между точками
        
        :param _cokriging: идентификатор созданного класса кокригинга
        
        :param _feature: признак для вычисления ковариация в кокригинге
        
        :param _min: возвращаемое минимальное расстояние между точками (только узловыми)
        
        :param _max: возвращаемое максимальное расстояние между точками
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrCokrigingGetMinMaxDistance_t (_cokriging, _feature, _min, _max)

    mtrCokrigingSetEmpiricalCovariance_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrCokrigingSetEmpiricalCovariance', ctypes.c_void_p, ctypes.c_int, ctypes.c_double, ctypes.c_int)
    def mtrCokrigingSetEmpiricalCovariance(_cokriging: ctypes.c_void_p, _feature: int, _lagsize: float, _lagcount: int) -> int:
        """
        Вычислить эмпирическую вариограмму
        
        :param _cokriging: идентификатор созданного класса кокригинга
        
        :param _feature: признак для вычисления ковариация в кокригинге
        
        :param _lagsize: размер лага в метрах (для всего диапазона LagSize = MaxDist / LagCount)
        
        :param _lagcount: количество лагов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrCokrigingSetEmpiricalCovariance_t (_cokriging, _feature, _lagsize, _lagcount)

    mtrCokrigingGetEmpiricalCovariance_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrCokrigingGetEmpiricalCovariance', ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_int))
    def mtrCokrigingGetEmpiricalCovariance(_cokriging: ctypes.c_void_p, _feature: int, _lagnum: int, _variogram: ctypes.POINTER(ctypes.c_double), _dist: ctypes.POINTER(ctypes.c_double), _pointcount: ctypes.POINTER(ctypes.c_int)) -> int:
        """
        Запросить значение эмпирической вариограммы для лага
        
        :param _cokriging: идентификатор созданного класса кокригинга
        
        :param _feature: признак для вычисления ковариация в кокригинге
        
        :param _lagnum: номер лага, для которого возвращаются параметры
        
        :param _variogram: эмпирическая вариограмма = sum(dH ``*`` dH) / ``2``
        
        :param _dist: центр лага по оси расстояний между парами точек = lagnum ``*`` lagsize + lagszie / ``2``
        
        :param _pointcount: количество пар точек, попавших в диапазон лага
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrCokrigingGetEmpiricalCovariance_t (_cokriging, _feature, _lagnum, _variogram, _dist, _pointcount)

    mtrCokrigingGetVariance_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrCokrigingGetVariance', ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_double))
    def mtrCokrigingGetVariance(_cokriging: ctypes.c_void_p, _feature: int, _variance: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить значение дисперсии
        
        :param _cokriging: идентификатор созданного класса кокригинга
        
        :param _feature: признак для вычисления ковариация в кокригинге
        
        :param _variance: значение дисперсии
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrCokrigingGetVariance_t (_cokriging, _feature, _variance)

    mtrCokrigingGetVariancePointCount_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrCokrigingGetVariancePointCount', ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    def mtrCokrigingGetVariancePointCount(_cokriging: ctypes.c_void_p, _feature: int, _variancepointcount: ctypes.POINTER(ctypes.c_int)) -> int:
        """
        Запросить количество точек, по которым считалась дисперсия
        
        :param _cokriging: идентификатор созданного класса кокригинга
        
        :param _feature: признак для вычисления ковариация в кокригинге
        
        :param _variancepointcount: количество точек, по которым считалась дисперсия Для признаков - количество реальных исходных точек Для кросс - количество точек на которых одновременно выполнялись оба измерения
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrCokrigingGetVariancePointCount_t (_cokriging, _feature, _variancepointcount)

    mtrCokrigingSetTeoreticalCovariance_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrCokrigingSetTeoreticalCovariance', ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mtrCokrigingSetTeoreticalCovariance(_cokriging: ctypes.c_void_p, _feature: int, _modeltype: int, _range: ctypes.POINTER(ctypes.c_double), _sill: ctypes.POINTER(ctypes.c_double), _nugget: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Вычислить теоретическую вариограмму
        
        :param _cokriging: идентификатор созданного класса кокригинга
        
        :param _feature: признак для вычисления ковариация в кокригинге
        
        :param _modeltype: тип модели
        
        :param _range: радиус модели (метры) - точка на оси расстояний между точками после которой кривая становится горизонтальной
        
        :param _sill: порог - значение, которое принимает теоретическая вариограмма в точке радиуса модели, из которого вычтено значение самородка
        
        :param _nugget: самородок - точка в которой кривая пересекает ось вариограммы Теоретически для нулевого расстояния между точками, изменение функции должно быть равно ``0``. Однако при бесконечно малых расстояниях разница между измерениями зачастую не стремится к нулю.
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если ``= -1`` - то значение вычисляется, если ``> 0``, то устанавливается
           Если ``= -1`` - то значение вычисляется, если ``> 0``, то устанавливается
           Если ``= -1`` - то значение вычисляется, если >``= 0``, то устанавливается
        """
        return mtrCokrigingSetTeoreticalCovariance_t (_cokriging, _feature, _modeltype, _range, _sill, _nugget)

    mtrCokrigingGetTeoreticalCovariance_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrCokrigingGetTeoreticalCovariance', ctypes.c_void_p, ctypes.c_int, ctypes.c_double, ctypes.POINTER(ctypes.c_double))
    def mtrCokrigingGetTeoreticalCovariance(_cokriging: ctypes.c_void_p, _feature: int, _dist: float, _var: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Вычислить значение теоретической вариограммы по расстоянию между двумя точками
        
        :param _cokriging: идентификатор созданного класса кокригинга
        
        :param _feature: признак для вычисления ковариация в кокригинге
        
        :param _dist: расстояние от начала
        
        :param _var: значение теоретической вариограммы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrCokrigingGetTeoreticalCovariance_t (_cokriging, _feature, _dist, _var)

    mtrCokrigingBuildUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrCokrigingBuildUn', ctypes.c_void_p, maptype.PWCHAR)
    def mtrCokrigingBuildUn(_cokriging: ctypes.c_void_p, _mtrname: mapsyst.WTEXT) -> int:
        """
        Построить матрицу
        
        :param _cokriging: идентификатор созданного класса кокригинга
        
        :param _mtrname: имя создаваемой маррицы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrCokrigingBuildUn_t (_cokriging, _mtrname.buffer())

    mtrLogarithmBuildUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrLogarithmBuildUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.POINTER(maptype.BUILDSURFACE), ctypes.POINTER(ctypes.c_double))
    def mtrLogarithmBuildUn(_hmap: maptype.HMAP, _hsit: maptype.HSITE, _mtrname: mapsyst.WTEXT, _mtrparm: ctypes.POINTER(maptype.BUILDSURFACE), _ranges: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Создать класс логарифмической интерполяции
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsit: идентификатор открытой пользовательской карты
        
        :param _mtrparm: параметры построения матрицы
        
        :param _ranges: для матриц качеств диапазон значений для палитры (при ``0`` не устанавливается)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrLogarithmBuildUn_t (_hmap, _hsit, _mtrname.buffer(), _mtrparm, _ranges)

    mtrMtwToVectorCallBack_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrMtwToVectorCallBack', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long, maptype.HSELECT, ctypes.POINTER(MTRCLASS), ctypes.c_long, maptype.HOBJ, ctypes.c_long, maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p))
    def mtrMtwToVectorCallBack(_hmap: maptype.HMAP, _hsit: maptype.HSITE, _mtrnum: int, _isfilter: int, _hselect: maptype.HSELECT, _classes: ctypes.POINTER(MTRCLASS), _classcount: int, _border: maptype.HOBJ, _iscuthole: int, _fcallback: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Преобразовать матрицу высот в вектор
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsit: векторная карта в которую пишутся объекты
        
        :param _mtrnum: номер оконтуриваемой матрицы высот, добавленной к карте
        
        :param _isfilter: признак фильтрации точек, лежащих на одной прямой
        
        :param _hselect: содержит созданные объекты если ``= 0``, то не заполняется, ненулевое значение сильно замедляет обработку
        
        :param _classes: распознаваемые классы
        
        :param _classcount: количество классов
        
        :param _border: объект, ограничивающий область преобразования матрицы в вектор
        
        :param _iscuthole: признак вырезания подобъектов если ``= 0``, то внутренний объект всегда имеет больший номер (Key), чем внешний
        
        :param _fcallback: функция обратного вызова для сообщения статуса выполнения (процентов), это функция типа ``EVENTCALL`` (описание в maptype.h), первым параметром в нее будет возвращено значение eventparam, вторым - код сообщения (``0x0581``), в третьем параметре  - процент выполненной обработки, в чевертом параметре - адрес строки с названием выполняемого этапа
        
        :param _eventparam: параметр, передаваемый в функцию обратного вызова для идентификации отклика на вызывающей стороне
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если процесс должен быть принудительно завершен, в ответ
           должно вернуться значение ``0x0581``
           Если fcallback равно нулю - сообщения не посылаются
           Текст передается в кодировке Unicode (UTF16)
        """
        return mtrMtwToVectorCallBack_t (_hmap, _hsit, _mtrnum, _isfilter, _hselect, _classes, _classcount, _border, _iscuthole, _fcallback, _eventparam)

    mtrMtqToVectorCallBack_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrMtqToVectorCallBack', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long, maptype.HSELECT, ctypes.POINTER(MTRCLASS), ctypes.c_long, maptype.HOBJ, ctypes.c_long, maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p))
    def mtrMtqToVectorCallBack(_hmap: maptype.HMAP, _hsit: maptype.HSITE, _mtqnum: int, _isfilter: int, _hselect: maptype.HSELECT, _classes: ctypes.POINTER(MTRCLASS), _classcount: int, _border: maptype.HOBJ, _iscuthole: int, _fcallback: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Преобразовать матрицу качеств в вектор
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsit: векторная карта в которую пишутся объекты
        
        :param _mtqnum: номер исходной матрицы качеств, добавленной к карте
        
        :param _isfilter: признак фильтрации точек, лежащих на одной прямой (``0``..``1``)
        
        :param _hselect: содержит созданные объекты (если ``= 0``, то не заполняется)
        
        :param _classes: распознаваемые классы
        
        :param _classcount: количество классов
        
        :param _border: объект, ограничивающий область преобразования матрицы в вектор
        
        :param _iscuthole: признак вырезания подобъектов если ``= 0``, то внутренний объект всегда имеет больший номер (Key), чем внешний
        
        :param _fcallback: функция обратного вызова для сообщения статуса выполнения (процентов), это функция типа ``EVENTCALL`` (описание в maptype.h), первым параметром в нее будет возвращено значение eventparam, вторым - код сообщения (``0x0581``), в третьем параметре  - процент выполненной обработки, в чевертом параметре - адрес строки с названием выполняемого этапа
        
        :param _eventparam: параметр, передаваемый в функцию обратного вызова для идентификации отклика на вызывающей стороне
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если процесс должен быть принудительно завершен, в ответ
           должно вернуться значение ``0x0581``
           Если fcallback равно нулю - сообщения не посылаются
           Текст передается в кодировке Unicode (UTF16)
        """
        return mtrMtqToVectorCallBack_t (_hmap, _hsit, _mtqnum, _isfilter, _hselect, _classes, _classcount, _border, _iscuthole, _fcallback, _eventparam)

    mtrRstToVectorCallBack_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrRstToVectorCallBack', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long, maptype.HSELECT, ctypes.POINTER(MTRCLASS), ctypes.c_long, maptype.HOBJ, ctypes.c_long, maptype.EVENTCALL, ctypes.POINTER(ctypes.c_void_p))
    def mtrRstToVectorCallBack(_hmap: maptype.HMAP, _hsit: maptype.HSITE, _rstnum: int, _isfilter: int, _hselect: maptype.HSELECT, _classes: ctypes.POINTER(MTRCLASS), _classcount: int, _border: maptype.HOBJ, _iscuthole: int, _fcallback: maptype.EVENTCALL, _eventparam: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Преобразовать растр в вектор
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsit: векторная карта в которую пишутся объекты
        
        :param _rstnum: номер исходного растра, добавленного к карте
        
        :param _isfilter: признак фильтрации точек, лежащих на одной прямой (``0``..``1``)
        
        :param _hselect: содержит созданные объекты (если ``= 0``, то не заполняется)
        
        :param _classes: распознаваемые классы
        
        :param _classcount: количество классов
        
        :param _border: объект, ограничивающий область преобразования растра в вектор
        
        :param _iscuthole: признак вырезания подобъектов если ``= 0``, то внутренний объект всегда имеет больший номер (Key), чем внешний
        
        :param _fcallback: функция обратного вызова для сообщения статуса выполнения (процентов), это функция типа ``EVENTCALL`` (описание в maptype.h), первым параметром в нее будет возвращено значение eventparam, вторым - код сообщения (``0x0581``), в третьем параметре  - процент выполненной обработки, в чевертом параметре - адрес строки с названием выполняемого этапа
        
        :param _eventparam: параметр, передаваемый в функцию обратного вызова для идентификации отклика на вызывающей стороне
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если процесс должен быть принудительно завершен, в ответ
           должно вернуться значение ``0x0581``
           Если fcallback равно нулю - сообщения не посылаются
           Текст передается в кодировке Unicode (UTF16)
        """
        return mtrRstToVectorCallBack_t (_hmap, _hsit, _rstnum, _isfilter, _hselect, _classes, _classcount, _border, _iscuthole, _fcallback, _eventparam)

    mtrBuildDensityMtq_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrBuildDensityMtq', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, maptype.HSELECT, ctypes.POINTER(BUILDDENSITY), maptype.HMESSAGE)
    def mtrBuildDensityMtq(_hmap: maptype.HMAP, _hsit: maptype.HSITE, _mtqname: mapsyst.WTEXT, _hselect: maptype.HSELECT, _parm: ctypes.POINTER(BUILDDENSITY), _hwnd: maptype.HMESSAGE) -> int:
        """
        Построить матрицу плотности
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsit: векторная карта с объектами, по которым строится матрица плотности
        
        :param _mtqname: имя создаваемой матрицы
        
        :param _hselect: объекты, по которым строится матрица (если ``= 0``, то все объекты карты)
        
        :param _parm: параметры построения
        
        :param _hwnd: окно, которому посылаются сообщения ``WM_PROGRESSBAR`` с процентом обработки в ``WPARAM`` (если ``= 0``, то сообщения не посылаются) Элемент матрицы содержит количество точек, попавших в заданный радиус
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrBuildDensityMtq_t (_hmap, _hsit, _mtqname.buffer(), _hselect, _parm, _hwnd)

    mtrBuildVisibleMtq_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrBuildVisibleMtq', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, maptype.HSELECT, ctypes.POINTER(BUILDVISIBLE), maptype.HMESSAGE)
    def mtrBuildVisibleMtq(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _mtqname: mapsyst.WTEXT, _hselect: maptype.HSELECT, _parm: ctypes.POINTER(BUILDVISIBLE), _hwnd: maptype.HMESSAGE) -> int:
        """
        Построить матрицу видимости
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: векторная карта с объектами, по которым строится матрица плотности
        
        :param _mtqname: имя создаваемой матрицы
        
        :param _hselect: объекты, по которым строится матрица (если ``= 0``, то все объекты карты)
        
        :param _parm: параметры построения
        
        :param _hwnd: окно, которому посылаются сообщения ``WM_PROGRESSBAR`` с процентом обработки в ``WPARAM`` (если ``= 0``, то сообщения не посылаются) Элемент матрицы имеет значение ``1``, в случае если с него видна хотя бы одна заданная точка, в противном случае - ``0``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrBuildVisibleMtq_t (_hmap, _hsite, _mtqname.buffer(), _hselect, _parm, _hwnd)

    mtrexGetMatrixCount_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrexGetMatrixCount', maptype.HMAP, ctypes.c_long)
    def mtrexGetMatrixCount(_hmap: maptype.HMAP, _matrixtype: int) -> int:
        """
        Запросить число открытых файлов матричных данных
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _matrixtype: тип матрицы (``FILE_MTW``, ``FILE_MTL``, ``FILE_MTQ``)
        
        :returns: Если matrixtype =``= 0``, функция возвращает количество всех матриц документа При ошибке возвращает ноль
        :rtype: int
        """
        return mtrexGetMatrixCount_t (_hmap, _matrixtype)

    mtrexGetMatrixNumberByNameUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrexGetMatrixNumberByNameUn', maptype.HMAP, ctypes.c_long, maptype.PWCHAR)
    def mtrexGetMatrixNumberByNameUn(_hmap: maptype.HMAP, _matrixtype: int, _name: mapsyst.WTEXT) -> int:
        """
        Запросить номер матрицы в цепочке по имени файла
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _matrixtype: тип матрицы (``FILE_MTW``, ``FILE_MTL``, ``FILE_MTQ``)
        
        :param _name: имя файла матрицы В цепочке номера матриц начинаются с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrexGetMatrixNumberByNameUn_t (_hmap, _matrixtype, _name.buffer())

    mtrexGetMatrixNameUn_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrexGetMatrixNameUn', maptype.HMAP, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mtrexGetMatrixNameUn(_hmap: maptype.HMAP, _number: int, _matrixtype: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить имя файла матричных данных
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: номер файла в цепочке
        
        :param _matrixtype: тип матрицы (``FILE_MTW``, ``FILE_MTL``, ``FILE_MTQ``)
        
        :param _name: адрес строки для размещения результата
        
        :param _size: размер строки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrexGetMatrixNameUn_t (_hmap, _number, _matrixtype, _name.buffer(), _size)

    mtrexGetMatrixLocation_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrexGetMatrixLocation', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mtrexGetMatrixLocation(_hmap: maptype.HMAP, _number: int, _matrixtype: int, _location: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Запросить привязку матрицы в метрах в районе работ
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _matrixtype: тип матрицы (``FILE_MTW``, ``FILE_MTL``, ``FILE_MTQ``)
        
        :param _location: координаты юго-западного угла матрицы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrexGetMatrixLocation_t (_hmap, _number, _matrixtype, _location)

    mtrexSetMatrixLocation_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrexSetMatrixLocation', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mtrexSetMatrixLocation(_hmap: maptype.HMAP, _number: int, _matrixtype: int, _location: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Установить привязку матрицы в метрах в районе работ
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _matrixtype: тип матрицы (``FILE_MTW``, ``FILE_MTL``, ``FILE_MTQ``)
        
        :param _location: координаты юго-западного угла матрицы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrexSetMatrixLocation_t (_hmap, _number, _matrixtype, _location)

    mtrexGetMatrixView_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrexGetMatrixView', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mtrexGetMatrixView(_hmap: maptype.HMAP, _number: int, _matrixtype: int) -> int:
        """
        Запросить степень видимости матрицы
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _matrixtype: тип матрицы (``FILE_MTW``, ``FILE_MTL``, ``FILE_MTQ``)
        
        :returns: Возвращает установленное значение степени видимости матрицы: view ``= 0`` - не виден view ``= 1`` - полная view ``= 2`` - насыщенная view ``= 3`` - полупрозрачная view ``= 4`` - средняя view ``= 5`` - прозрачная При ошибке возвращает ноль
        :rtype: int
        """
        return mtrexGetMatrixView_t (_hmap, _number, _matrixtype)

    mtrexSetMatrixView_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrexSetMatrixView', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mtrexSetMatrixView(_hmap: maptype.HMAP, _number: int, _matrixtype: int, _view: int) -> int:
        """
        Установить степень видимости матрицы
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _matrixtype: тип матрицы (``FILE_MTW``, ``FILE_MTL``, ``FILE_MTQ``)
        
        :param _view: степень видимости матрицы: view ``= 0`` - не виден view ``= 1`` - полная view ``= 2`` - насыщенная view ``= 3`` - полупрозрачная view ``= 4`` - средняя view ``= 5`` - прозрачная
        
        :returns: Возвращает установленное значение При ошибке возвращает ноль
        :rtype: int
        """
        return mtrexSetMatrixView_t (_hmap, _number, _matrixtype, _view)

    mtrexGetMatrixEdit_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrexGetMatrixEdit', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mtrexGetMatrixEdit(_hmap: maptype.HMAP, _number: int, _matrixtype: int) -> int:
        """
        Запросить флаг редактируемости матрицы
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _matrixtype: тип матрицы (``FILE_MTW``, ``FILE_MTL``, ``FILE_MTQ``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrexGetMatrixEdit_t (_hmap, _number, _matrixtype)

    mtrexGetMatrixTransparent_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrexGetMatrixTransparent', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mtrexGetMatrixTransparent(_hmap: maptype.HMAP, _number: int, _matrixtype: int) -> int:
        """
        Запросить прозрачность палитры матрицы
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _matrixtype: тип матрицы (``FILE_MTW``, ``FILE_MTL``, ``FILE_MTQ``)
        
        :returns: Возвращает степень прозрачности в процентах от 0 до 100
        :rtype: int
        """
        return mtrexGetMatrixTransparent_t (_hmap, _number, _matrixtype)

    mtrexSetMatrixTransparent_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrexSetMatrixTransparent', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mtrexSetMatrixTransparent(_hmap: maptype.HMAP, _number: int, _matrixtype: int, _transparent: int) -> int:
        """
        Установить прозрачность палитры матрицы
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _matrixtype: тип матрицы (``FILE_MTW``, ``FILE_MTL``, ``FILE_MTQ``)
        
        :param _transparent: прозрачность в процентах от ``0`` до ``100``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrexSetMatrixTransparent_t (_hmap, _number, _matrixtype, _transparent)

    mtrexGetMatrixViewOrder_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrexGetMatrixViewOrder', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mtrexGetMatrixViewOrder(_hmap: maptype.HMAP, _number: int, _matrixtype: int) -> int:
        """
        Запросить порядок отображения матрицы
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _matrixtype: тип матрицы (``FILE_MTW``, ``FILE_MTL``, ``FILE_MTQ``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrexGetMatrixViewOrder_t (_hmap, _number, _matrixtype)

    mtrexSetMatrixViewOrder_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrexSetMatrixViewOrder', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mtrexSetMatrixViewOrder(_hmap: maptype.HMAP, _number: int, _matrixtype: int, _order: int) -> int:
        """
        Установить порядок отображения матрицы
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _matrixtype: тип матрицы (``FILE_MTW``, ``FILE_MTL``, ``FILE_MTQ``)
        
        :param _order: порядок (``0`` - под картой, ``1`` - над картой)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrexSetMatrixViewOrder_t (_hmap, _number, _matrixtype, _order)

    mtrexChangeOrderMatrixShow_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrexChangeOrderMatrixShow', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mtrexChangeOrderMatrixShow(_hmap: maptype.HMAP, _matrixtype: int, _oldnumber: int, _newnumber: int) -> int:
        """
        Поменять очередность отображения матриц в цепочке
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _matrixtype: тип матрицы (``FILE_MTW``, ``FILE_MTL``, ``FILE_MTQ``)
        
        :param _oldnumber: номер файла в цепочке
        
        :param _newnumber: устанавливаемый номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrexChangeOrderMatrixShow_t (_hmap, _matrixtype, _oldnumber, _newnumber)

    mtrexCloseMatrix_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrexCloseMatrix', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mtrexCloseMatrix(_hmap: maptype.HMAP, _number: int, _matrixtype: int) -> int:
        """
        Закрыть матричные данные
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _matrixtype: тип матрицы (``FILE_MTW``, ``FILE_MTL``, ``FILE_MTQ``) Чтобы освободить все ресурсы - нужно ВЫЗВАТЬ mapCloseData(hmap)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если number =``= 0``, закрываются все матрицы в окне
        """
        return mtrexCloseMatrix_t (_hmap, _number, _matrixtype)

    mtdIsLasColor_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtdIsLasColor', maptype.PWCHAR)
    def mtdIsLasColor(_lasname: mapsyst.WTEXT) -> int:
        """
        Запросить наличие цвета в данных облака точек формата LAS
        
        :param _lasname: имя файла формата ``LAS``
        
        :returns: При наличии цвета возвращает 1, при отсутствии 0 При ошибке возвращает ноль
        :rtype: int
        """
        return mtdIsLasColor_t (_lasname.buffer())

    mtdGetLasPointCount_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtdGetLasPointCount', maptype.PWCHAR)
    def mtdGetLasPointCount(_lasname: mapsyst.WTEXT) -> int:
        """
        Запросить количество записей точек в файле формата LAS
        
        :param _lasname: имя файла формата ``LAS``
        
        :returns: Возвращает значение поля NumberOfPointRecords заголовка файла LAS При ошибке возвращает ноль
        :rtype: int
        """
        return mtdGetLasPointCount_t (_lasname.buffer())

    mtdImportLasToMtd_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtdImportLasToMtd', maptype.PWCHAR, maptype.PWCHAR, maptype.HMESSAGE)
    def mtdImportLasToMtd(_lasname: mapsyst.WTEXT, _mtdname: mapsyst.WTEXT, _handle: maptype.HMESSAGE) -> int:
        """
        Импорт данных облака точек формата LAS в MTD-модель
        
        :param _lasname: имя файла формата ``LAS``
        
        :param _mtdname: имя файла ``MTD``-модели
        
        :param _handle: идентификатор окна диалога, которому посылается cообщение
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtdImportLasToMtd_t (_lasname.buffer(), _mtdname.buffer(), _handle)

    mtrCreateIsolinesBySurface_t = mapsyst.GetProcAddress(mtrexlib,ctypes.c_long,'mtrCreateIsolinesBySurface', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(CREATEISOLINES))
    def mtrCreateIsolinesBySurface(_hmap: maptype.HMAP, _matrixname: mapsyst.WTEXT, _sitename: mapsyst.WTEXT, _parm: ctypes.POINTER(CREATEISOLINES)) -> int:
        """
        Создание изолиний по матрице поверхности
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _matrixname: имя файла исходной матрицы (``*.mtw`` ``*.mtq`` ``*.mtl``) или ``MTD``-модели (``*.mtd``)
        
        :param _sitename: имя файла результирующей карты изолиний
        
        :param _parm: параметры создания изолиний
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mtrCreateIsolinesBySurface_t (_hmap, _matrixname.buffer(), _sitename.buffer(), _parm)



def mtrexapi_healthcheck():
    return 1
