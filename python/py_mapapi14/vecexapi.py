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
    *  Функции импорта и экспорта векторных данных различных форматов  *
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
# Импорт векторных данных из csv и текстовых форматов

LABEL_ECSV = 0x56534345


#-----------------------------
class ORDERCELL(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Layer",ctypes.c_int),
                ("Local",ctypes.c_int)]
#-----------------------------


#-----------------------------
class SETTING(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("IsUpdate",ctypes.c_int),
                ("Code",ctypes.c_int),
                ("Charset",ctypes.c_int),
                ("Isdirect",ctypes.c_int),
                ("Isdivision",ctypes.c_int),
                ("Isosm",ctypes.c_int),
                ("IsBL",ctypes.c_int),
                ("IsSorted",ctypes.c_int),
                ("Scale",ctypes.c_int),
                ("IsFolder",ctypes.c_int),
                ("MapType",ctypes.c_int),
                ("Reserve",ctypes.c_int),
                ("NumberField",maptype.WCHAR1*(32)),
                ("LabelField",maptype.WCHAR1*(32)),
                ("AngleField",maptype.WCHAR1*(32)),
                ("CodeField",maptype.WCHAR1*(32)),
                ("RscName",maptype.WCHAR1*(520)),
                ("Prefix",maptype.WCHAR1*(512)),
                ("Postfix",maptype.WCHAR1*(512))]
#-----------------------------


#-----------------------------
class RECORDLIST(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("DbfField",maptype.WCHAR1*(32)),
                ("FieldName",maptype.WCHAR1*(512)),
                ("FieldKey",maptype.WCHAR1*(512)),
                ("LayerName",maptype.WCHAR1*(512)),
                ("ObjectCode",ctypes.c_int),
                ("Reserve",ctypes.c_int)]
#-----------------------------


#-----------------------------
class SEMFIELDS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("name",maptype.WCHAR1*(2048)),
                ("code",ctypes.c_int),
                ("zero",ctypes.c_int)]
#-----------------------------


#-----------------------------
class RECORDHEAD(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Number",ctypes.c_int),
                ("Length",ctypes.c_int)]
#-----------------------------


#-----------------------------
class MAPTOSHPPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("hMap",maptype.HMAP),
                ("hSite",maptype.HSITE),
                ("hSelect",maptype.HSELECT),
                ("DBCode",ctypes.c_int),
                ("Isbl",ctypes.c_int),
                ("IsService",ctypes.c_int),
                ("IsDecode",ctypes.c_int),
                ("IsFolder",ctypes.c_int),
                ("IsLaeyrInShp",ctypes.c_char),
                ("Reserve",ctypes.c_char*(3))]
#-----------------------------


#-----------------------------
class DXF2MAPPARMS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Scale",ctypes.c_int),
                ("Image",ctypes.c_int),
                ("fSemantic",ctypes.c_int),
                ("Unit",ctypes.c_int),
                ("fLayerName",ctypes.c_int),
                ("fMapCreate",ctypes.c_int),
                ("fBaseType",ctypes.c_int),
                ("f3DMetric",ctypes.c_int),
                ("fXAxis",ctypes.c_int),
                ("fGraphic",ctypes.c_int)]
#-----------------------------


#-----------------------------
class PARMDXF(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("ImageType",ctypes.c_int),
                ("Semantic",ctypes.c_int),
                ("LayerType",ctypes.c_int),
                ("Precision",ctypes.c_int),
                ("Unicode",ctypes.c_int),
                ("RGBColor",ctypes.c_int),
                ("LineType",ctypes.c_int),
                ("Reserve",ctypes.c_int)]
#-----------------------------


#-----------------------------
class TXTTRANSLATEPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("InHuser",ctypes.c_void_p),
                ("OutHuser",ctypes.c_void_p),
                ("InDelimiter",ctypes.c_char),
                ("OutDelimiter",ctypes.c_char),
                ("InUnit",ctypes.c_char),
                ("OutUnit",ctypes.c_char),
                ("InFormat",ctypes.c_char),
                ("OutFormat",ctypes.c_char),
                ("IsSaveH",ctypes.c_char),
                ("Reserve",ctypes.c_char*(9))]
#-----------------------------


#-----------------------------
class TXTTOMAPPARMS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("HMap",maptype.HMAP),
                ("HSite",maptype.HSITE),
                ("RscObjectIncode",ctypes.c_long),
                ("XColumnNumber",ctypes.c_int),
                ("YColumnNumber",ctypes.c_int),
                ("HColumnNumber",ctypes.c_int),
                ("MColumnNumber",ctypes.c_int),
                ("CoordinateSystem",ctypes.c_int),
                ("LineNumberToStartReading",ctypes.c_int),
                ("DelimiterSymbol",ctypes.c_char)]
#-----------------------------


#-----------------------------
class CREATESHEETSPARMEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("hFrame",maptype.HOBJ),
                ("SourceMapType",ctypes.c_long),
                ("EpsgCode",ctypes.c_long),
                ("Scale",ctypes.c_long),
                ("IsDelimeter",ctypes.c_long),
                ("Error",ctypes.c_long),
                ("ValueEntryPercent",ctypes.c_long),
                ("MainName",maptype.WCHAR1*(512)),
                ("Prefix",maptype.WCHAR1*(128))]
#-----------------------------


#-----------------------------
class COMPARELISTPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("OperatorName",maptype.WCHAR1*(520)),
                ("DestMapName",maptype.WCHAR1*(2048)),
                ("StandardPath",maptype.WCHAR1*(2048)),
                ("Comment",maptype.WCHAR1*(2048)),
                ("SelectFrame",maptype.DFRAME),
                ("WorkDuration",ctypes.c_int),
                ("SelectRegime",ctypes.c_int),
                ("Reserve",ctypes.c_int*(10))]
#-----------------------------


#-----------------------------
class CREATETITLEPARAM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("SourceTextType",ctypes.c_int),
                ("CurrentSemanticCode",ctypes.c_int),
                ("CurrentRscObjectNumber",ctypes.c_int),
                ("TitleLocation",ctypes.c_int),
                ("IsNoSignCheck",ctypes.c_int),
                ("SetSemanticLink",ctypes.c_int),
                ("IsRectangleXYCheck",ctypes.c_int),
                ("IsGeodeticBLCheck",ctypes.c_int),
                ("TypeUnitCoordinateXY",ctypes.c_int),
                ("TypeGeodeticBL",ctypes.c_int),
                ("IsHeightCheck",ctypes.c_int),
                ("IsHeightFromMtr",ctypes.c_int),
                ("IsHeightInterpolate",ctypes.c_int),
                ("IsSphereCheck",ctypes.c_int),
                ("IsChangeDotCheck",ctypes.c_int),
                ("IsTextDirectCheck",ctypes.c_int),
                ("IsAfterNumberDecimal",ctypes.c_int),
                ("AfterNumberDecimal",ctypes.c_int),
                ("IsBeforeDecimalPlaces",ctypes.c_int),
                ("BeforeDecimalPlaces",ctypes.c_int),
                ("TitleLocationByLine",ctypes.c_int),
                ("TitleLocationSide",ctypes.c_int),
                ("IsTitleSplineCheck",ctypes.c_int),
                ("IsTitleNoRepeatCheck",ctypes.c_int),
                ("IsLabelAllObjectsMulti",ctypes.c_int),
                ("TypeTitlePolygon",ctypes.c_int),
                ("TitleAlignHorizontal",ctypes.c_int),
                ("TitleAlignVertical",ctypes.c_int),
                ("TypeAngle",ctypes.c_int),
                ("AngleSemanticNumber",ctypes.c_int),
                ("LeftIndentValue",ctypes.c_int),
                ("TopIndentValue",ctypes.c_int),
                ("TitleStep",ctypes.c_double),
                ("AngleValue",ctypes.c_double),
                ("TextRatherSemantics",maptype.WCHAR1*(520)),
                ("CustomText",maptype.WCHAR1*(520)),
                ("PrefixText",maptype.WCHAR1*(520)),
                ("PostfixText",maptype.WCHAR1*(520)),
                ("FontName",maptype.WCHAR1*(520)),
                ("InputRscObjectKey",maptype.WCHAR1*(520)),
                ("DrawObject",maptype.HOBJ)]
#-----------------------------


#-----------------------------
class COLUMNSEMANTIC(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("FieldNumber",ctypes.c_int),
                ("SemanticCode",ctypes.c_int)]
#-----------------------------


#-----------------------------
class CSVTITLE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("RscIncode",ctypes.c_int),
                ("Zero",ctypes.c_int),
                ("DistanceX",ctypes.c_int),
                ("DistanceY",ctypes.c_int),
                ("ColumnNumber1",ctypes.c_int),
                ("ColumnNumber2",ctypes.c_int),
                ("ColumnNumber3",ctypes.c_int),
                ("ColumnNumber4",ctypes.c_int)]
#-----------------------------


#-----------------------------
class CSVLOADPARAMS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("ShiftX",ctypes.c_double),
                ("ShiftY",ctypes.c_double),
                ("ShiftH",ctypes.c_double),
                ("Semantic",COLUMNSEMANTIC*(96)),
                ("Title",CSVTITLE*(2)),
                ("SemanticCount",ctypes.c_int),
                ("TitleCount",ctypes.c_int),
                ("ColumnNumberLinkSemantic",ctypes.c_int),
                ("DelimiterSymbol",ctypes.c_int),
                ("Precision",ctypes.c_int),
                ("UseTransactionLog",ctypes.c_int),
                ("ColumnNumberXorWKT",ctypes.c_int),
                ("ColumnNumberY",ctypes.c_int),
                ("ColumnNumberHeight",ctypes.c_int),
                ("ColumnNumberMeasure",ctypes.c_int),
                ("ColumnNumberObjectKey",ctypes.c_int),
                ("ColumnNumberMultiObject",ctypes.c_int),
                ("ColumnNumberObject",ctypes.c_int),
                ("ColumnNumberSubject",ctypes.c_int),
                ("RowNumberToStartReading",ctypes.c_int),
                ("RscIncodeForPoint",ctypes.c_int),
                ("RscIncodeForLine",ctypes.c_int),
                ("RscIncodeForSquare",ctypes.c_int),
                ("SemanticCodeX",ctypes.c_int),
                ("SemanticCodeY",ctypes.c_int),
                ("SemanticCodeH",ctypes.c_int),
                ("SemanticCodeM",ctypes.c_int),
                ("TryToAutoFillStructByFirstRow",ctypes.c_int),
                ("Units",ctypes.c_int),
                ("EpsgCode",ctypes.c_int),
                ("NumericSemanticsMode",ctypes.c_int),
                ("RowNumberToEndReading",ctypes.c_int),
                ("Zero",ctypes.c_int),
                ("Reserve",ctypes.c_char*(120))]
#-----------------------------


#-----------------------------
class CSVSAVEPARAMS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Label",ctypes.c_int),
                ("Length",ctypes.c_int),
                ("Semantic",ctypes.POINTER(COLUMNSEMANTIC)),
                ("SemanticCount",ctypes.c_int),
                ("DecodeSemantics",ctypes.c_int),
                ("DelimiterSymbol",ctypes.c_int),
                ("Precision",ctypes.c_int),
                ("EpsgCode",ctypes.c_int),
                ("SaveObjectKey",ctypes.c_int),
                ("Units",ctypes.c_int),
                ("FileEncoding",ctypes.c_int),
                ("SaveObjectHeight",ctypes.c_int),
                ("SaveObjectMeasure",ctypes.c_int),
                ("SaveObjectNumber",ctypes.c_int),
                ("SaveObjectName",ctypes.c_int),
                ("SaveObjectLength",ctypes.c_int),
                ("SaveObjectSquare",ctypes.c_int),
                ("SaveMapName",ctypes.c_int),
                ("SaveLayerName",ctypes.c_int),
                ("SaveObjectLocal",ctypes.c_int),
                ("SaveCenterCoordinates",ctypes.c_int),
                ("ExportType",ctypes.c_int),
                ("SemCodeForName",ctypes.c_int),
                ("LengthUnits",ctypes.c_int),
                ("SquareUnits",ctypes.c_int),
                ("Reserve",ctypes.c_char*(56))]
#-----------------------------




try:
    if os.environ['gisvecexdll']:
        gisvecexname = os.environ['gisvecexdll']
except KeyError:
    gisvecexname = 'gis64vecex.dll'

try:
    vecexlib = mapsyst.LoadLibrary(gisvecexname)
except Exception as e:
    print(e)
    vecexlib = 0

if vecexlib == 0:
    print(gisvecexname)
else:
    vecModifyMapEx_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'vecModifyMapEx', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_long, ctypes.POINTER(mapcreat.LOCALTRANSFORM), maptype.HMESSAGE, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_long))
    def vecModifyMapEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _outname: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _newnamesize: int, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM), _handle: maptype.HMESSAGE, _hevent: maptype.EVENTSTATE, _eventparm: ctypes.POINTER(ctypes.c_void_p), _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Трансформирование векторной карты в заданную систему координат
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор открытой пользовательской карты
        
        :param _outname: полный путь к паспорту трансформированной карты или путь к папке для размещения карты с тем же именем
        
        :param _newname: имя созданной карты
        
        :param _newnamesize: размер буфера для newname в байтах
        
        :param _mapreg: структура параметров системы координат, в которую трансформируется исходная карта
        
        :param _datum: параметры датума или ``0``
        
        :param _ellipsoid: параметры эллипсоида или ``0``
        
        :param _ttype: тип локального преобразования координат (описан в ``TRANSFORMTYPE`` в mapcreat.h) или ``0``
        
        :param _tparm: параметры локального преобразования координат
        
        :param _handle: идентификатор окна диалога процесса обработки (``HWND`` для Windows/функция обратного вызова для Linux) Окну диалога посылаются следующие сообщения ``WM_PROGRESSBARUN``
        
        :param _hevent: адрес функции обратного вызова для получения процента выполнения задачи eventparam  - первый параметр функции обратного вызова
        
        :param _error: поле для записи кода ошибки выполнения функции
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return vecModifyMapEx_t (_hmap, _hsite, _outname.buffer(), _newname.buffer(), _newnamesize, _mapreg, _datum, _ellipsoid, _ttype, _tparm, _handle, _hevent, _eventparm, _error)

    mapGetAnySxfInfoMeta_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'mapGetAnySxfInfoMeta', maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(mapcreat.METAINFO))
    def mapGetAnySxfInfoMeta(_name: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _metainfo: ctypes.POINTER(mapcreat.METAINFO)) -> int:
        """
        Запросить паспортные данные из файлов SXF, TXF, MAP, SIT, SITX по имени файла
        
        :param _name: имя файла карты форматов ``SXF``, ``TXF``, MAP, SIT, SITX
        
        :param _mapreg: структура параметров системы координат карты
        
        :param _listreg: параметры листа многолистовой карты или ``0``
        
        :param _metainfo: параметры метаданных карты
        
        :returns: Возвращает число объектов в карте, если число объектов равно 0, то возвращает -1 При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetAnySxfInfoMeta_t (_name.buffer(), _mapreg, _listreg, _metainfo)

    GetRscNameFromAnySxfUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'GetRscNameFromAnySxfUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def GetRscNameFromAnySxfUn(_name: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить имя классификатора (RSC) из файлов SXF, TXF, MAP (SIT)
        
        :param _name: имя файла карты форматов ``SXF``, ``TXF``, MAP, SIT, SITX
        
        :param _rscname: адрес буфера для записи имени классификатора
        
        :param _size: длина буфера в байтах В файлах ``SXF`` и ``TXF`` имя классификатора (``RSC``) может отсутствовать
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return GetRscNameFromAnySxfUn_t (_name.buffer(), _rscname.buffer(), _size)

    GetSxfCheckSumUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'GetSxfCheckSumUn', maptype.PWCHAR)
    def GetSxfCheckSumUn(_name: mapsyst.WTEXT) -> int:
        """
        Запросить контрольную сумму файла SXF
        
        :param _name: имя файла ``SXF``
        
        :returns: При ошибке возвращает ноль и выдает сообщение на экран Ноль - допустимое значение контрольной суммы
        :rtype: int
        """
        return GetSxfCheckSumUn_t (_name.buffer())

    SxfCheckSumUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'SxfCheckSumUn', maptype.PWCHAR)
    def SxfCheckSumUn(_name: mapsyst.WTEXT) -> int:
        """
        Проверить контрольную сумму файла SXF
        
        :param _name: имя файла ``SXF``
        
        :returns: При успешной проверке возвращает 1 При несовпадении контрольной суммы возвращает -1 При ошибке структуры файла возвращает -2 При устаревшей версии структуры файла возвращает -3 При ошибке доступа к данным возвращает ноль и выдает сообщение на экран (если выдача сообщений разрешена)
        :rtype: int
        """
        return SxfCheckSumUn_t (_name.buffer())

    GetBorderMetricsFromAnySxfEx_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'GetBorderMetricsFromAnySxfEx', maptype.PWCHAR, maptype.HOBJ, ctypes.c_long)
    def GetBorderMetricsFromAnySxfEx(_name: mapsyst.WTEXT, _hobj: maptype.HOBJ, _extend: int) -> int:
        """
        Заполнить метрику объекта координатами рамки листа карты из файлов SXF, TXF, MAP, SIT, SITX
        
        :param _name: имя файла карты в одном из вышеперечисленных форматов
        
        :param _hobj: идентификатор объекта, созданного на той карте, где будет сохранен объект
        
        :param _extend: признак вставки дополнительных точек на стороны рамки, если рамка состоит только из ``4`` угловых точек Координаты будут пересчитаны из системы координат файла к системе координат выходной карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если объекта-рамки нет в наборе данных, то запишутся координаты габаритов набора данных
           Если у исходного объекта имелись координаты, то они будут удалены
           Объект-рамка ищется по коду SHEETFRAMEEXCODE (91000000)
        """
        return GetBorderMetricsFromAnySxfEx_t (_name.buffer(), _hobj, _extend)

    BuildPreviewImageFromAnySxfPro_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'BuildPreviewImageFromAnySxfPro', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, maptype.EVENTLOG, ctypes.POINTER(ctypes.c_void_p))
    def BuildPreviewImageFromAnySxfPro(_dataname: mapsyst.WTEXT, _imagename: mapsyst.WTEXT, _width: int, _height: int, _rscname: mapsyst.WTEXT, _hevent: maptype.EVENTLOG, _eventparam: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Сформировать обзорное изображение карты в формате PNG из файлов SXF, TXF, MAP, SIT, SITX
        
        :param _dataname: имя файла карты в одном из вышеперечисленных форматов
        
        :param _imagename: имя файла ``PNG`` с обзорным изображением, если равно ``0``,
        
        :param _width: ширина изображения в пикселах (например, ``512``)
        
        :param _height: высота изображения в пикселах (например, ``512``)
        
        :param _rscname: имя цифрового классификатора для карт формата ``SXF`` и ``TXF``, если равно нулю, то ищется в ``SXF`` или ``TXF``
        
        :param _hevent: адрес функции обратного вызова для записи в протокол ошибок выполнени программы
        
        :param _eventparam: первый параметр функции обратного вызова Изображение строится из цетральной части карты в базовом масштабе карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           то к полному имени файла карты добавляется ``".preview.png"``
        """
        return BuildPreviewImageFromAnySxfPro_t (_dataname.buffer(), _imagename.buffer(), _width, _height, _rscname.buffer(), _hevent, _eventparam)

    mapStructControl_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'mapStructControl', maptype.HMAP, maptype.HSITE, ctypes.c_long, maptype.HMESSAGE)
    def mapStructControl(_hMap: maptype.HMAP, _hSite: maptype.HSITE, _mode: int, _handle: maptype.HMESSAGE) -> int:
        """
        Выполнить контроль структуры данных карты
        
        :param _hMap: идентификатор открытых данных (документа)
        
        :param _hSite: идентификатор векторной карты в документе, для фоновой карты равен hmap
        
        :param _mode: режим работы: ``0`` - контроль, ``1`` - редактирование
        
        :param _handle: идентификатор обработчика (окна диалога) процесса обработки или ``0`` Обработчику посылаются следующие сообщения: ``WM_LIST``   = ``0x586``   WParam - количество листов в районе LParam - номер текущего листа ``WM_OBJECT`` = ``0x585``   WParam - процент обработанных объектов ``WM_ERROR``  = ``0x587``   WParam - порядковый номер объекта или ``0`` LParam ``= 1`` - ошибка в карте ``= 2`` - ошибка в классификаторе ``= 3`` - ошибка в описании объекта ``= 4`` - ошибка в метрике ``= 5`` - ошибка в семантике ``= 6`` - ошибка в графике
        
        :returns: Возвращает количество ошибок в районе
        :rtype: int
        """
        return mapStructControl_t (_hMap, _hSite, _mode, _handle)

    mapCallSorting_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'mapCallSorting', maptype.HMAP, maptype.HSITE, maptype.HMESSAGE, ctypes.POINTER(ORDERCELL), ctypes.c_int)
    def mapCallSorting(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _handle: maptype.HMESSAGE, _ordercell: ctypes.POINTER(ORDERCELL), _ordercount: int) -> int:
        """
        Специальная сортировка отдельной карты документа
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в документе, для фоновой карты равен hmap
        
        :param _handle: идентификатор обработчика (окна диалога) процесса обработки или ``0``
        
        :param _ordercell: массив записей (слой, локализация) в котором должна быть отсортирована карта
        
        :param _ordercount: число записей в массиве
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCallSorting_t (_hmap, _hsite, _handle, _ordercell, _ordercount)

    ImportFromAnySxfProEx_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'ImportFromAnySxfProEx', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, maptype.HMESSAGE, maptype.HSELECT, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, maptype.EVENTLOG, ctypes.POINTER(ctypes.c_void_p))
    def ImportFromAnySxfProEx(_hmap: maptype.HMAP, _sxfname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _size: int, _handle: maptype.HMESSAGE, _hselect: maptype.HSELECT, _frscfromsxf: int, _sittype: int, _password: mapsyst.WTEXT, _psize: int, _transform: int, _hevent: maptype.EVENTLOG, _eventparam: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Импорт карты из файла SXF, TXF или DIR с преобразованием топокарты к зоне документа
        
        :param _hmap: идентификатор открытой карты (рекомендуется указывать для определения текущей зоны топокарты) или ``0``
        
        :param _sxfname: имя загружаемого файла типа ``SXF``, ``TXF`` или ``DIR``
        
        :param _rscname: имя файла классификатора, с которым загружается карта, имя классификатора можно запросить из ``SXF`` (``TXF``) функцией GetRscNameFromSxf или из карты; для файла ``DIR`` может быть ``0``
        
        :param _mapname: имя создаваемой карты (обычно совпадает с именем ``SXF`` (``TXF``)) или ноль или указатель на пустую строку или указатель на папку для размещения карты. Если имя карты не задано или задана только папка, то карта создается с именем ``SXF`` (``TXF``) и расширением ``".sit"``. Если namemap указывает на буфер достаточной длины (size), то в буфер записывается имя созданной карты. Для файла ``DIR`` тип общей карты - MPT (проект данных, включающий все открытые карты из ``DIR``) или MAP (многолистовая карта)
        
        :param _size: длина буфера в байтах, на который указывает переменная mapname, или ``0`` (если запись в поле запрещена). Обычно длина равна ``MAX_PATH_LONG`` (``1024``) ``*`` sizeof(``WCHAR``)
        
        :param _handle: идентификатор обработчика (в Windows - окна диалога) процесса обработки или ``0``
        
        :param _hselect: фильтр загружаемых объектов и слоев, если необходима выборочная обработка данных
        
        :param _frscfromsxf: значение флажка ``"разрешить использование имени классификатора, указанного в файле sxf"``
        
        :param _sittype: тип создаваемых карт в проекте MPT при импорте ``DIR`` (``1`` - SIT, -``1`` - SITX)
        
        :param _password: пароль для создания защищенного хранилища карты (SITX)
        
        :param _psize: длина пароля в байтах
        
        :param _transform: признак необходимости трансформировать загружаемую карту в систему координат hmap (если hmap и transform не равно ``0``)
        
        :param _hevent: адрес функции обратного вызова для записи в протокол ошибок выполнени программы
        
        :param _eventparam: первый параметр функции обратного вызова Файлы ``SXF`` и ``TXF`` могут хранить координаты в метрах, радианах или градусах Для добавления открытой карты в документ необходимо вызвать функцию mapAppendData(hmap, namemap). Если mapname содержит имя карты типа MAP и она содержит хотя бы один лист, то при импорте данных выполняется создание нового листа в карте MAP. В этом случае функция mapAppendData не должна вызываться
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return ImportFromAnySxfProEx_t (_hmap, _sxfname.buffer(), _rscname.buffer(), _mapname.buffer(), _size, _handle, _hselect, _frscfromsxf, _sittype, _password.buffer(), _psize, _transform, _hevent, _eventparam)

    vecLoadTxfFromBuffer_t = mapsyst.GetProcAddress(vecexlib,maptype.HMAP,'vecLoadTxfFromBuffer', ctypes.c_char_p, ctypes.c_long, maptype.PWCHAR)
    def vecLoadTxfFromBuffer(_buffer: ctypes.c_char_p, _size: int, _rscname: mapsyst.WTEXT) -> maptype.HMAP:
        """
        Загрузить временную карту из буфера в памяти в формате TXF
        
        :param _buffer: адрес буфера, содержащего данные в формате ``TXF``
        
        :param _size: размер буфера
        
        :param _rscname: имя классификатора для создания временной карты, если равно нулю, то используется service.rsc
        
        :returns: Возвращает идентификатор временной карты в памяти При закрытии карты все ее данные удаляются При ошибке возвращает ноль
        :rtype: maptype.HMAP
        """
        return vecLoadTxfFromBuffer_t (_buffer, _size, _rscname.buffer())

    UpdateFromAnySxfUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'UpdateFromAnySxfUn', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, maptype.HMESSAGE, maptype.HSELECT, ctypes.c_long)
    def UpdateFromAnySxfUn(_hmap: maptype.HMAP, _sxfname: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _size: int, _handle: maptype.HMESSAGE, _hselect: maptype.HSELECT, _mode: int) -> int:
        """
        Обновить карту из файла SXF, TXF или DIR с использованием Select
        
        с преобразованием топокарты к зоне документа
        Файлы SXF и TXF могут хранить координаты в метрах, радианах или градусах
        
        :param _hmap: идентификатор открытой карты (для определения текущей зоны топокарты) или ``0``;
        
        :param _sxfname: имя загружаемого файла типа ``SXF``, ``TXF`` или ``DIR``;
        
        :param _mapname: имя обновляемой карты; может быть ноль или указатель на пустую строку, в этом случае обновляемая карта в документе ищется по совпадению номенклатур.
        
        :param _size: длина буфера, на который указывает переменная namemap или ``0`` (если запись в буфер запрещена). Обычно длина равна ``MAX_PATH_LONG`` ``*`` sizeof(``WCHAR``)
        
        :param _handle: идентификатор обработчика (в Windows - окна диалога) процесса обработки или ``0``
        
        :param _hselect: фильтр загружаемых объектов и слоев, если необходима выборочная обработка данных
        
        :param _mode: режим обновления данных: ``0`` - поиск записей по совпадению уникального номера в карте и исходном файле и обновление, если объект не найден, то добавление объекта; ``1`` - добавление объектов с новыми уникальными номерами в те карты, номенклатуры которых совпадают с номенклатурой ``SXF`` (``TXF``), если - номенклатура не найдена, то добавляется новый лист (карта); ``2`` - добавление объектов с новыми уникальными номерами в заданную карту без учета номенклатур
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если namemap указывает на буфер достаточной длины (size),
           то в буфер записывается имя обновленной карты;
           Если карты не было в документе - она может быть создана (добавлена)
        """
        return UpdateFromAnySxfUn_t (_hmap, _sxfname.buffer(), _mapname.buffer(), _size, _handle, _hselect, _mode)

    ExportToSxfUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'ExportToSxfUn', maptype.PWCHAR, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, maptype.HMESSAGE, maptype.HSELECT, ctypes.c_long)
    def ExportToSxfUn(_mapname: mapsyst.WTEXT, _list: int, _sxfname: mapsyst.WTEXT, _flag: int, _handle: maptype.HMESSAGE, _select: maptype.HSELECT, _flserv: int) -> int:
        """
        Сохранить (экспортировать) карту в двоичный формат SXF
        
        :param _mapname: имя файла сохраняемой карты;
        
        :param _list: номер листа для многолистовой карты или ``1``;
        
        :param _sxfname: имя создаваемого файла ``SXF``, обычно совпадает с именем карты, но имеет расширение ``SXF``;
        
        :param _flag: вид хранимых координат (``0`` - метры, ``4`` - радианы, ``8`` - градусы, для карты, поддерживающей геодезические координаты, -``1`` - определить по виду координат на карте);
        
        :param _handle: идентификатор обработчика (в Windows - окна диалога) процесса обработки или ``0``
        
        :param _select: фильтр выгружаемых объектов и слоев, если необходима выборочная обработка данных;
        
        :param _flserv: записать служебный объект c датумом и эллипсоидом и имя классификатора (поддерживается с версии ``10.7`` и выше) Для топокарт, хранящих координаты в метрах, координаты всегда хранятся в зоне, указанной в паспорте карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если карты не было в документе - она может быть создана (добавлена)
        """
        return ExportToSxfUn_t (_mapname.buffer(), _list, _sxfname.buffer(), _flag, _handle, _select, _flserv)

    ExportToTxfPro_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'ExportToTxfPro', maptype.PWCHAR, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.HMESSAGE, maptype.HSELECT)
    def ExportToTxfPro(_mapname: mapsyst.WTEXT, _list: int, _txfname: mapsyst.WTEXT, _flag: int, _precision: int, _isutf8: int, _handle: maptype.HMESSAGE, _hselect: maptype.HSELECT) -> int:
        """
        Сохранить (экспортировать) карту в текстовый формат TXF
        
        :param _mapname: имя файла сохраняемой карты;
        
        :param _list: номер листа для многолистовой карты или ``1``;
        
        :param _txfname: имя создаваемого файла ``TXF``, обычно совпадает с именем карты, но имеет расширение ``SXF``;
        
        :param _flag: вид хранимых координат (``0`` - метры, ``4`` - радианы, ``8`` - градусы, для карты, поддерживающей геодезические координаты, -``1`` - определить по виду координат на карте);
        
        :param _precision: число знаков после запятой для координат в метрах или ``0``; если карта имеет паспортную точность в см (``2`` знака) или в мм (``3`` знака), то precision игнорируется;
        
        :param _isutf8: признак записи названий файлов, имени листа карты, текстов подписей и текстовых семантик в кодировке utf8 (если значение поля больше нуля, если ноль - в кодировке ``ANSI``)
        
        :param _handle: идентификатор обработчика (в Windows - окна диалога) процесса обработки или ``0``
        
        :param _hselect: фильтр выгружаемых объектов и слоев, если необходима выборочная обработка данных; Для топокарт, хранящих координаты в метрах, координаты всегда хранятся в зоне, указанной в паспорте карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если карты не было в документе - она может быть создана (добавлена)
        """
        return ExportToTxfPro_t (_mapname.buffer(), _list, _txfname.buffer(), _flag, _precision, _isutf8, _handle, _hselect)

    ExportToDirPro_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'ExportToDirPro', maptype.HMAP, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.HMESSAGE, maptype.HSELECT, ctypes.c_long, ctypes.c_long, maptype.PWCHAR)
    def ExportToDirPro(_hmap: maptype.HMAP, _dirname: mapsyst.WTEXT, _type: int, _flag: int, _total: int, _precision: int, _handle: maptype.HMESSAGE, _hselect: maptype.HSELECT, _frsc: int, _isutf8: int, _logname: mapsyst.WTEXT) -> int:
        """
        Сохранить (экспортировать) карту в формат DIR
        
        :param _hmap: идентификатор открытых данных
        
        :param _dirname: имя создаваемого файла ``DIR``, обычно совпадает с именем открытого проекта или главной карты, но имеет расширение ``DIR``;
        
        :param _type: тип создаваемых файлов (``0`` - ``SXF``, ``1`` - ``TXF``);
        
        :param _flag: вид хранимых координат (``0`` - метры, ``4`` - радианы, ``8`` - градусы, для карты, поддерживающей геодезические координаты, -``1`` - определить по виду координат на карте);
        
        :param _total: признак сохранения в ``DIR`` только главной карты (``0``) или всех карт документа (``1``);
        
        :param _precision: для файлов ``TXF`` число знаков после запятой для координат в метрах или ``0``; если карта имеет паспортную точность в см (``2`` знака) или в мм (``3`` знака), то precision игнорируется;
        
        :param _handle: идентификатор окна диалога, которому посылаются уведомительные сообщения (``HWND`` для Windows, ``CALLBACK``-Функция для Linux);
        
        :param _hselect: фильтр выгружаемых объектов и слоев, если необходима выборочная обработка данных;
        
        :param _frsc: записать имя классификатора в файл sxf (если не равно ``0``) utf8    - записать имена файлов и файлы ``TXF`` (если поле не равно нулю) в кодировке ``UTF8``
        
        :param _logname: имя файла-протокола результатов сохранения карты в ``DIR`` или ноль Для топокарт, хранящих координаты в метрах, координаты всегда хранятся в зоне, указанной в паспорте карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если карты не было в документе - она может быть создана (добавлена)
        """
        return ExportToDirPro_t (_hmap, _dirname.buffer(), _type, _flag, _total, _precision, _handle, _hselect, _frsc, _isutf8, _logname.buffer())

    vecCutSiteToSheets_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'vecCutSiteToSheets', maptype.HMESSAGE, maptype.HMAP, maptype.HSITE, maptype.HMAP, maptype.HSELECT)
    def vecCutSiteToSheets(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _hmapout: maptype.HMAP, _hselect: maptype.HSELECT) -> int:
        """
        Нарезать исходную карту по листам выходной карты
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор открытой пользовательской карты
        
        :param _hmapout: идентификатор выходной карты (для ускорения загрузки установить mapSetLoadState)
        
        :param _hselect: условия отбора объектов или ``0`` (обработать все объекты)
        
        :returns: Возвращает число обработанных объектов При прерывании задачи оператором возвращает -1 При ошибке возвращает ноль
        :rtype: int
        """
        return vecCutSiteToSheets_t (_handle, _hmap, _hsite, _hmapout, _hselect)

    shpCheckZipContents_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'shpCheckZipContents', maptype.PWCHAR)
    def shpCheckZipContents(_zipname: mapsyst.WTEXT) -> int:
        """
        Проверить, что файл zip содержит файлы SHP
        
        :param _zipname: имя файла ``ZIP``
        
        :returns: Возвращает число найденных файлов SHP в архиве При ошибке возвращает ноль
        :rtype: int
        """
        return shpCheckZipContents_t (_zipname.buffer())

    shpLoadSheetFromZip_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'shpLoadSheetFromZip', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def shpLoadSheetFromZip(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _shpzip: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _epsgcode: int, _iscreate: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Выполнить импорт наборов данных SHP из папки, запакованной в ZIP, в один лист карты
        
        :param _hmap: идентификатор карты, в которую дописываются листы или ``0`` (если hmap !``= 0``, то mapname, rscname, iscreate игнорируются)
        
        :param _handle: идентификатор обработчика сообщений о ходе выполнения импорта данных
        
        :param _shpzip: имя файла zip, содержащего слои листа карты в формате ``SHP`` (любой вложенности)
        
        :param _mapname: имя файла создаваемой/обновляемой карты
        
        :param _rscname: имя файла классификатора, с которым создается карта, или ``0`` (если карта существует)
        
        :param _epsgcode: код системы координат создаваемой карты или ``0`` (если карта существует или создается по ``PRJ``)
        
        :param _iscreate: признак создания карты или ``0`` (если карта существует)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return shpLoadSheetFromZip_t (_hmap, _handle, _shpzip.buffer(), _mapname.buffer(), _rscname.buffer(), _epsgcode, _iscreate, _error)

    shpLoadSheetFromFolder_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'shpLoadSheetFromFolder', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def shpLoadSheetFromFolder(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _shpfolder: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _epsgcode: int, _iscreate: int) -> int:
        """
        Выполнить импорт наборов данных SHP из папки в один лист карты
        
        :param _hmap: идентификатор карты, в которую дописываются листы или ``0`` (если hmap !``= 0``, то mapname, rscname, iscreate игнорируются)
        
        :param _handle: идентификатор обработчика сообщений о ходе выполнения импорта данных
        
        :param _shpfolder: имя папки, в которой размещены слои листа карты в формате ``SHP`` (любой вложенности)
        
        :param _mapname: имя файла создаваемой/обновляемой карты
        
        :param _rscname: имя файла классификатора, с которым создается карта, или ``0`` (если карта существует)
        
        :param _epsgcode: код системы координат создаваемой карты или ``0`` (если карта существует или создается по ``PRJ``)
        
        :param _iscreate: признак создания карты или ``0`` (если карта существует)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return shpLoadSheetFromFolder_t (_hmap, _handle, _shpfolder.buffer(), _mapname.buffer(), _rscname.buffer(), _epsgcode, _iscreate)

    shpLoadFromFolderByShi_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'shpLoadFromFolderByShi', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long))
    def shpLoadFromFolderByShi(_handle: maptype.HMESSAGE, _shpfolder: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _shiname: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Выполнить импорт наборов данных SHP из папки в один лист карты
        
        :param _handle: идентификатор обработчика сообщений о ходе выполнения импорта данных
        
        :param _shpfolder: имя папки, в которой размещены слои листа карты в формате ``SHP`` (любой вложенности)
        
        :param _mapname: имя файла создаваемой карты (sit/sitx), если карта уже существует, то будет выполнена ее очистка
        
        :param _shiname: имя файла настроек shi
        
        :param _error: код ошибки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return shpLoadFromFolderByShi_t (_handle, _shpfolder.buffer(), _mapname.buffer(), _shiname.buffer(), _error)

    shpShapeProcReadPrj_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'shpShapeProcReadPrj', maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), maptype.PWCHAR, ctypes.c_long)
    def shpShapeProcReadPrj(_prjname: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _csname: mapsyst.WTEXT, _size: int) -> int:
        """
        Считать параметры системы координат из файла PRJ
        
        :param _prjname: имя файла ``PRJ``
        
        :param _mapreg: параметры проекции создаваемой карты
        
        :param _ellipsoid: параметры эллипсоида
        
        :param _datum: параметры датума
        
        :param _csname: буфер для записи условного наименования системы координат
        
        :param _size: размер буфера в байтах
        
        :returns: Если задана геодезическая система координат в градусах, то возвращает 2 Для координат в метрах возвращает 1 Если параметры не были определены и координаты в метрах - возвращает -1 При ошибке возвращает ноль
        :rtype: int
        """
        return shpShapeProcReadPrj_t (_prjname.buffer(), _mapreg, _ellipsoid, _datum, _csname.buffer(), _size)

    shpShapeProcSheetInitEx_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_void_p,'shpShapeProcSheetInitEx', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), maptype.PWCHAR, ctypes.POINTER(SEMFIELDS), ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def shpShapeProcSheetInitEx(_handle: maptype.HMESSAGE, _mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _name: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _nomenclature: mapsyst.WTEXT, _semitem: ctypes.POINTER(SEMFIELDS), _semcount: int, _ismap: int, _epsgcode: int) -> ctypes.c_void_p:
        """
        Создать объект для импорта файлов SHP
        
        :param _handle: идентификатор получателя сообщений ``WM_ERROR`` и ``WM_OBJECT``
        
        :param _mapname: имя паспорта создаваемой\\обновляемой карты
        
        :param _rscname: имя классификатора создаваемой карты или ``0`` (если имя не задано, то карта обновляется)
        
        :param _name: имя района (листа) карты
        
        :param _mapreg: параметры проекции создаваемой карты
        
        :param _ellipsoid: параметры эллипсоида
        
        :param _datum: параметры датума
        
        :param _nomenclature: номенклатура листа или ``0`` (используется и для формирования имени файлов листов карт с рамкой)
        
        :param _semitem: список обрабатываемых полей атрибутов или ``0`` (если нужно обрабатывать не все поля ``DBF``)
        
        :param _semcount: число элементов в списке
        
        :param _ismap: признак создания карты (``1`` - многолистовая карта MAP, иначе ``0``)
        
        :param _epsgcode: код системы координат, в которой создается карта или ``0`` (если система совпадает с системой исходных данных) Для освобождения ресурсов объектов после загрузки необходимо вызвать функцию shpShapeProcClose
        
        :returns: При ошибке возвращает ноль
        """
        return shpShapeProcSheetInitEx_t (_handle, _mapname.buffer(), _rscname.buffer(), _name.buffer(), _mapreg, _ellipsoid, _datum, _nomenclature.buffer(), _semitem, _semcount, _ismap, _epsgcode)

    shpShapeProcSheetForMap_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_void_p,'shpShapeProcSheetForMap', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), maptype.PWCHAR, ctypes.POINTER(RECORDLIST), ctypes.c_long, ctypes.POINTER(SEMFIELDS), ctypes.c_long)
    def shpShapeProcSheetForMap(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellparm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datumparm: ctypes.POINTER(mapcreat.DATUMPARAM), _nomenclature: mapsyst.WTEXT, _recitem: ctypes.POINTER(RECORDLIST), _recount: int, _semitem: ctypes.POINTER(SEMFIELDS), _semcount: int) -> ctypes.c_void_p:
        """
        Создать объект для импорта файлов SHP
        
        :param _hmap: идентификатор карты, в которую дописываются листы
        
        :param _handle: идентификатор получателя сообщений ``WM_ERROR`` и ``WM_OBJECT``
        
        :param _mapreg: параметры проекции создаваемой карты ellipsoid - параметры эллипсоида datum - параметры датума
        
        :param _nomenclature: номенклатура листа или ``0`` (используется и для формирования имени файлов листов карт с рамкой)
        
        :param _recitem: список обрабатываемых файлов ``SHP``
        
        :param _recount: число файлов в списке
        
        :param _semitem: список обрабатываемых полей атрибутов
        
        :param _semcount: число полей в списке Для освобождения ресурсов объектов после загрузки необходимо вызвать функцию shpShapeProcClose
        
        :returns: При ошибке возвращает ноль
        """
        return shpShapeProcSheetForMap_t (_hmap, _handle, _mapreg, _ellparm, _datumparm, _nomenclature.buffer(), _recitem, _recount, _semitem, _semcount)

    shpShapeProcClose_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'shpShapeProcClose', ctypes.c_void_p)
    def shpShapeProcClose(_hshpload: ctypes.c_void_p) -> int:
        """
        Удалить объект для импорта файлов SHP
        
        :param _hshpload: объект, созданный в функции shpShapeProcSheetForMap или shpShapeProcSheetInitEx
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return shpShapeProcClose_t (_hshpload)

    shpGetShapeProcMapHandle_t = mapsyst.GetProcAddress(vecexlib,maptype.HMAP,'shpGetShapeProcMapHandle', ctypes.c_void_p)
    def shpGetShapeProcMapHandle(_hshpload: ctypes.c_void_p) -> maptype.HMAP:
        """
        Запросить идентификатор открытой карты
        
        :param _hshpload: идентификатор объекта загрузки ``SHP``
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HMAP
        """
        return shpGetShapeProcMapHandle_t (_hshpload)

    shpShapeProcLoad_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'shpShapeProcLoad', ctypes.c_void_p, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(SETTING), ctypes.POINTER(ctypes.c_long))
    def shpShapeProcLoad(_hshpload: ctypes.c_void_p, _shpfilename: mapsyst.WTEXT, _code: int, _setting: ctypes.POINTER(SETTING), _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Загрузить SHP-файл
        
        :param _hshpload: идентификатор объекта загрузки ``SHP`` shpname  - имя входного файла ``SHP``
        
        :param _code: код зарегистрированного объекта
        
        :param _setting: указатель на структуру настроек диалога ``SETTING``
        
        :param _error: код ошибки при создании объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return shpShapeProcLoad_t (_hshpload, _shpfilename.buffer(), _code, _setting, _error)

    shpShapeProcLoadList_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'shpShapeProcLoadList', ctypes.c_void_p, ctypes.POINTER(ctypes.POINTER(maptype.WCHAR)), ctypes.c_long, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(SETTING))
    def shpShapeProcLoadList(_hshpload: ctypes.c_void_p, _shplist: ctypes.POINTER(ctypes.POINTER(maptype.WCHAR)), _count: int, _code: ctypes.POINTER(ctypes.c_int), _setting: ctypes.POINTER(SETTING)) -> int:
        """
        Загрузить список Shape файлов
        
        :param _hshpload: идентификатор объекта загрузки ``SHP``
        
        :param _shplist: список указателей на имена shp-файлов
        
        :param _count: число файлов в списке
        
        :param _code: массив кодов объектов для списка shp-файлов
        
        :param _setting: указатель на структуру настроек диалога ``SETTING`` (myform.h)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return shpShapeProcLoadList_t (_hshpload, _shplist, _count, _code, _setting)

    shpCheckSheetProjectEquivalent_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'shpCheckSheetProjectEquivalent', maptype.PWCHAR)
    def shpCheckSheetProjectEquivalent(_name: mapsyst.WTEXT) -> int:
        """
        Проверить совпадение параметров систем координат (PRJ) в разных папках (листах) с наборами SHP
        
        :param _name: имя корневой папки с файлами ``SHP`` или с набором папок, содержащих отдельные листы карты
        
        :returns: При совпадении параметров возвращает 1, иначе - нулевое значение
        :rtype: int
        
        .. note::

           Если файлы SHP расположены в корневой папке, то сравнивает файлы PRJ в корневой папке,
           если есть набор папок, то сравнивает по одному файлу PRJ в каждой папке, чтобы найти
           разные параметры СК (например, разные зоны)
        """
        return shpCheckSheetProjectEquivalent_t (_name.buffer())

    shpGetShpBorderInFolder_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'shpGetShpBorderInFolder', maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME))
    def shpGetShpBorderInFolder(_folder: mapsyst.WTEXT, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Запросить общие габариты набора файлов SHP в заданной папке, включая вложенные папки
        
        :param _folder: путь к папке, содержащей файлы ``SHP``
        
        :param _frame: габариты, запрашиваются в радианах в системе ``WGS``-``84``
        
        :returns: Возвращает общее число объектов во всех файлах SHP Если для SHP не заданы параметры проекции (PRJ) - возвращает ноль При ошибке возвращает ноль
        :rtype: int
        """
        return shpGetShpBorderInFolder_t (_folder.buffer(), _frame)

    shpGetShpBorder_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'shpGetShpBorder', maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME))
    def shpGetShpBorder(_shpname: mapsyst.WTEXT, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Запросить габариты файла SHP
        
        :param _shpname: путь к файлу ``SHP``
        
        :param _frame: габариты, запрашиваются в радианах в системе ``WGS``-``84``
        
        :returns: Возвращает общее число объектов во всех файлах SHP Если для SHP не заданы параметры проекции (PRJ) - возвращает ноль При ошибке возвращает ноль
        :rtype: int
        """
        return shpGetShpBorder_t (_shpname.buffer(), _frame)

    shpLoadOneShape_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'shpLoadOneShape', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_long))
    def shpLoadOneShape(_hmap: maptype.HMAP, _shpname: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _epsgcode: int, _iscreate: int, _scale: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Выполнить импорт набора данных SHP в один лист карты
        
        :param _hmap: идентификатор карты, в которую дописываются листы или ``0`` (если hmap !``= 0``, то mapname, rscname, iscreate игнорируются)
        
        :param _shpname: имя файла в формате ``SHP``
        
        :param _mapname: имя файла создаваемой карты или ``0`` (если карта существует)
        
        :param _rscname: имя файла классификатора, с которым создается карта, или ``0`` (если карта существует)
        
        :param _epsgcode: код системы координат создаваемой карты или ``0`` (если карта существует или создается по ``PRJ``)
        
        :param _iscreate: признак создания карты или ``0`` (если карта существует)
        
        :param _scale: масштаб создаваемой карты или ``0`` (если карта существует)
        
        :param _error: поле для записи кода ошибки выполнения функции
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return shpLoadOneShape_t (_hmap, _shpname.buffer(), _mapname.buffer(), _rscname.buffer(), _epsgcode, _iscreate, _scale, _error)

    vecUpdateObjectFromShp_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'vecUpdateObjectFromShp', maptype.HOBJ, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def vecUpdateObjectFromShp(_info: maptype.HOBJ, _shpname: mapsyst.WTEXT, _onlypoints: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Обновить описание объекта из SHP
        
        :param _info: идентификатор обновляемого объекта в памяти
        
        :param _shpname: имя исходного файла ``SHP`` (полный путь)
        
        :param _onlypoints: признак обновления только координат объекта
        
        :param _error: коды ошибок выполнения программы (см. maperr.rh) Объект изменяется без записи на карту
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return vecUpdateObjectFromShp_t (_info, _shpname.buffer(), _onlypoints, _error)

    vecSaveMapToShpPro_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'vecSaveMapToShpPro', maptype.HMESSAGE, ctypes.POINTER(MAPTOSHPPARM), maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long), maptype.PWCHAR, maptype.PWCHAR)
    def vecSaveMapToShpPro(_handle: maptype.HMESSAGE, _parm: ctypes.POINTER(MAPTOSHPPARM), _shppath: mapsyst.WTEXT, _xmlparm: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_long), _ininame: mapsyst.WTEXT, _logname: mapsyst.WTEXT) -> int:
        """
        Экспорт векторной карты в формат SHP
        
        :param _handle: идентификатор обработчика (в Windows - окна диалога) процесса обработки или ``0`` Обработчику отправляются сообщения ``WM_OBJECT``, ``WM_ERROR``, ``WM_LIST``
        
        :param _parm: основные параметры для экспорта карты
        
        :param _shppath: путь к папке для записи файлов ``SHP``
        
        :param _xmlparm: путь к файлу схемы, описывающей структуру файлов ``SHP`` (если файл не задан, то структура слоев соответствует исходной карте)
        
        :param _error: коды ошибок выполнения программы (см. maperr.rh)
        
        :param _ininame: имя файлов параметров экспорта в ``SHP``
        
        :param _logname: имя файла с протоколом ошибок процедуры
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return vecSaveMapToShpPro_t (_handle, _parm, _shppath.buffer(), _xmlparm.buffer(), _error, _ininame.buffer(), _logname.buffer())

    vecSaveObjectToShp_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'vecSaveObjectToShp', maptype.HOBJ, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long))
    def vecSaveObjectToShp(_info: maptype.HOBJ, _shpname: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Сохранить описание объекта в SHP
        
        :param _info: идентификатор сохраняемого объекта в памяти
        
        :param _shpname: имя файла ``SHP`` (полный путь), в который будет сохранен объект
        
        :param _error: коды ошибок выполнения программы (maperr.rh)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return vecSaveObjectToShp_t (_info, _shpname.buffer(), _error)

    mifLoadSheetFromFolder_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'mifLoadSheetFromFolder', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mifLoadSheetFromFolder(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _folder: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _epsgcode: int, _iscreate: int) -> int:
        """
        Выполнить импорт наборов данных MIF\\MID из папки в один лист карты
        
        :param _hmap: идентификатор карты, в которую дописываются листы или ``0`` (если hmap !``= 0``, то mapname, rscname, iscreate игнорируются)
        
        :param _handle: идентификатор обработчика сообщений о ходе выполнения импорта данных
        
        :param _folder: имя папки, в которой размещены слои листа карты в формате ``MIF``\\``MID`` (любой вложенности)
        
        :param _mapname: имя файла создаваемой/обновляемой карты
        
        :param _rscname: имя файла классификатора, с которым создается карта, или ``0`` (если карта существует)
        
        :param _epsgcode: код системы координат создаваемой карты или ``0`` (если карта существует или создается по своим параметрам)
        
        :param _iscreate: признак создания карты или ``0`` (если карта существует)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mifLoadSheetFromFolder_t (_hmap, _handle, _folder.buffer(), _mapname.buffer(), _rscname.buffer(), _epsgcode, _iscreate)

    LoadS57FolderToMap_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'LoadS57FolderToMap', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_char_p, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, ctypes.POINTER(ctypes.c_long))
    def LoadS57FolderToMap(_handle: maptype.HMESSAGE, _folders57: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _size: int, _rscname: mapsyst.WTEXT, _sittype: int, _hw_id: ctypes.c_char_p, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _logfile: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Импорт файлов данных S57/S63 из заданной папки в формат MPT/SITX
        
        :param _handle: идентификатор окна, которому посылаются сообщения ``WM_OBJECT`` и ``WM_ERROR``
        
        :param _folders57: путь к папке для поиска файлов формата ``S57`` (файл ``PERMIT``.``TXT`` ищется внутри папки и на ``2`` уровня выше папки \\``ENC_ROOT``, если задан userpermit)
        
        :param _mapname: полное имя создаваемой карты
        
        :param _rscname: полное имя файла классификатора (обычно S57navy.rsc)
        
        :param _sittype: тип создаваемых карт в проекте MPT или MAP (для данных ``S63`` всегда MPT/SITX, ``1`` - MPT/SIT; -``1`` - MPT/SITX, ``0`` - MAP)
        
        :param _hw_id: ``OEM`` код инсталляции СПО на конкретном компьютере для работы с ``S63``, двоичное значение длиной ``6`` байт
        
        :param _callevent: адрес функции обратного вызова для получения уведомлений о проценте загруженных данных (см. maptype.h)
        
        :param _parm: параметр, передаваемый в функцию обратного вызова (например, адрес класса обработки сообщений)
        
        :param _logfile: путь к файлу журнала работы программы (может быть ``0``)
        
        :param _error: поле для записи кода ошибки выполнения Данные, закодированные по стандарту ``S63``, остаются закодированными в формате SITX, в качестве пароля используется двоичное значение hw_id Для работы программы требуется классификатор s57navy.rsc Для отображения карт нужна библиотека отображения знаков s57navy.iml (s57navy.iml64)
        
        :returns: При ошибке в параметрах возвращает ноль
        :rtype: int
        """
        return LoadS57FolderToMap_t (_handle, _folders57.buffer(), _mapname.buffer(), _size, _rscname.buffer(), _sittype, _hw_id, _callevent, _parm, _logfile.buffer(), _error)

    CreateUserPermit_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'CreateUserPermit', maptype.PWCHAR, ctypes.c_long, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
    def CreateUserPermit(_m_key: mapsyst.WTEXT, _m_keysize: int, _hw_id: ctypes.c_char_p, _m_id: ctypes.c_char_p, _userpermit: ctypes.c_char_p, _size: int) -> int:
        """
        Сформировать USERPERMIT (28 шестнадцатеричных символов)
        
        :param _m_key: пароль для доступа к данным ``S63`` - уникальный ключ ``M_KEY`` в виде hex-строки длиной ``10`` байт
        
        :param _m_keysize: длина строки m_key в байтах
        
        :param _hw_id: закрытый ``OEM`` код инсталляции СПО на конкретном компьютере для работы с ``S63``, двоичное число длиной ``5`` байт
        
        :param _m_id: id разработчика в виде hex-строки длиной ``4`` байта
        
        :param _userpermit: буфер для записи разрешения пользователя для инсталляции СПО
        
        :param _size: длина буфера в байтах (не менее ``28`` байт)
        
        :returns: При ошибке в параметрах возвращает ноль
        :rtype: int
        """
        return CreateUserPermit_t (_m_key.buffer(), _m_keysize, _hw_id, _m_id, _userpermit, _size)

    GetHWID_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'GetHWID', ctypes.c_char_p, maptype.PWCHAR, ctypes.c_long, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_long))
    def GetHWID(_userpermit: ctypes.c_char_p, _m_key: mapsyst.WTEXT, _m_keysize: int, _hw_id6: ctypes.c_char_p, _size: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Определить HW_ID по userpermit
        
        :param _userpermit: запись разрешения пользователя для инсталляции СПО
        
        :param _m_key: пароль для доступа к данным ``S63`` - уникальный ключ ``M_KEY`` в виде hex-строки длиной ``20`` байт в ``UTF16``
        
        :param _m_keysize: длина пароля в байтах hw_id - буфер для записи закрытого ``OEM`` кода инсталляции СПО на конкретном компьютере для работы с ``S63``, двоичное число длиной ``5`` байт
        
        :param _size: длина буфера в байтах
        
        :param _error: поле для записи кода ошибки
        
        :returns: При ошибке в параметрах возвращает ноль
        :rtype: int
        """
        return GetHWID_t (_userpermit, _m_key.buffer(), _m_keysize, _hw_id6, _size, _error)

    LoadS57FolderToMapPro_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'LoadS57FolderToMapPro', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, ctypes.POINTER(ctypes.c_long), ctypes.c_char_p)
    def LoadS57FolderToMapPro(_handle: maptype.HMESSAGE, _folders57: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _size: int, _rscname: mapsyst.WTEXT, _sittype: int, _m_key: mapsyst.WTEXT, _m_keysize: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _logfile: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_long), _userpermit: ctypes.c_char_p) -> int:
        """
        Импорт файлов данных S57/S63 из заданной папки в формат MPT/SITX
        
        :param _handle: идентификатор окна, которому посылаются сообщения ``WM_OBJECT`` и ``WM_ERROR``
        
        :param _folders57: путь к папке для поиска файлов формата ``S57`` (файл ``PERMIT``.``TXT`` ищется внутри папки и на ``2`` уровня выше папки \\``ENC_ROOT``, если задан userpermit)
        
        :param _mapname: полное имя создаваемой карты
        
        :param _rscname: полное имя файла классификатора (обычно S57navy.rsc)
        
        :param _sittype: тип создаваемых карт в проекте MPT или MAP (для данных ``S63`` всегда MPT/SITX, ``1`` - MPT/SIT; -``1`` - MPT/SITX, ``0`` - MAP)
        
        :param _m_key: пароль для доступа к данным ``S63`` - уникальный ключ ``M_KEY`` в виде hex-строки в UTF-16 или ноль
        
        :param _m_keysize: длина строки m_key в байтах
        
        :param _callevent: адрес функции обратного вызова для получения уведомлений о проценте загруженных данных (см. maptype.h)
        
        :param _parm: параметр, передаваемый в функцию обратного вызова (например, адрес класса обработки сообщений)
        
        :param _logfile: путь к файлу журнала работы программы (может быть ``0``)
        
        :param _error: поле для записи кода ошибки выполнения
        
        :param _userpermit: закодированное разрешение пользователя на обработку данных ``S63`` (шестнадцатеричная строка длиной ``28`` символов) или ``0``, например: ``"66B5CBFDF7E4139D5B6086C23130"`` Данные, закодированные по стандарту ``S63``, остаются закодированными в формате SITX, в качестве пароля используется двоичное значение hw_id6, закодированное в userpermit Для работы программы требуется классификатор s57navy.rsc Для отображения карт нужна библиотека отображения знаков s57navy.iml (s57navy.iml64)
        
        :returns: При ошибке в параметрах возвращает ноль
        :rtype: int
        """
        return LoadS57FolderToMapPro_t (_handle, _folders57.buffer(), _mapname.buffer(), _size, _rscname.buffer(), _sittype, _m_key.buffer(), _m_keysize, _callevent, _parm, _logfile.buffer(), _error, _userpermit)

    vecLoadS57ToMapUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'vecLoadS57ToMapUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def vecLoadS57ToMapUn(_handle: maptype.HMESSAGE, _s57name: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _size: int, _rscname: mapsyst.WTEXT, _regionname: mapsyst.WTEXT, _safelystate: int) -> int:
        """
        Импорт из формата S57 в формат MAP или SIT (без вызова диалога)
        
        :param _handle: идентификатор окна диалога, которому посылаются уведомительные сообщения ``WM_OBJECT`` и ``WM_ERROR`` (``HWND`` для Windows, ``CALLBACK``-Функция для Linux) или ``0``
        
        :param _s57name: полный путь к файлу формата ``S57`` (``*.000`` или ``*.030``)
        
        :param _mapname: полный путь к файлу создаваемой карты
        
        :param _size: размер буфера имени создаваемой карты, если имя может быть изменено в функции
        
        :param _rscname: полное имя файла классификатора (s57navy.rsc)
        
        :param _regionname: условное название создаваемой карты (``"Море Лаптевых"`` и т.п.)
        
        :param _safelystate: флаг создания границ зон безопасности (длительный процесс оверлейного анализа данных)
        
        :returns: При ошибке в параметрах возвращает ноль
        :rtype: int
        """
        return vecLoadS57ToMapUn_t (_handle, _s57name.buffer(), _mapname.buffer(), _size, _rscname.buffer(), _regionname.buffer(), _safelystate)

    FindPermitFile_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'FindPermitFile', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def FindPermitFile(_folders57: mapsyst.WTEXT, _folder: mapsyst.WTEXT, _size: int) -> int:
        """
        Найти файл PERMIT.TXT в заданной папке
        
        :param _folders57: папка, относительно которой выполняется поиск (ниже и выше на ``2`` уровня, если в пути есть ``ENC_ROOT``)
        
        :param _folder: адрес буфера для записи пути к папке, в которой найден файл ``PERMIT``.``TXT``
        
        :param _size: размер буфера в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return FindPermitFile_t (_folders57.buffer(), _folder.buffer(), _size)

    LoadS57FolderToMapEx_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'LoadS57FolderToMapEx', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR)
    def LoadS57FolderToMapEx(_handle: maptype.HMESSAGE, _folders57: mapsyst.WTEXT, _namemap: mapsyst.WTEXT, _size: int, _namersc: mapsyst.WTEXT, _sittype: int, _password: mapsyst.WTEXT, _psize: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _logfile: mapsyst.WTEXT) -> int:
        """
        Импорт всех файлов S57 из заданной папки в формат MAP/MPT
        
        :param _handle: идентификатор окна, которому посылаются сообщения ``WM_OBJECT`` и ``WM_ERROR``
        
        :param _folders57: путь к папке для поиска файлов формата ``S57``
        
        :param _namemap: полное имя создаваемой карты
        
        :param _size: размер буфера, содержащего имя создаваемой карты, если имя можно обновить при импорте, или ``0``
        
        :param _namersc: полное имя файла классификатора (обычно ``S57NAVY``.``RSC``)
        
        :param _sittype: тип создаваемых карт в проекте MPT или MAP (``1`` - SIT; -``1`` - SITX, ``0`` - MAP)
        
        :param _password: пароль доступа к данным, из которого формируется ``256``-битный код для шифрования данных (при утрате данные не восстанавливаются) или ``0``
        
        :param _psize: длина пароля в байтах или ``0``
        
        :param _callevent: адрес функции обратного вызова для получения уведомлений о проценте загруженных данных (см. maptype.h)
        
        :param _parm: параметр, передаваемый в функцию обратного вызова (например, адрес класса обработки сообщений)
        
        :param _logfile: путь к файлу журнала работы программы (может быть ``0``) Для работы программы требуется классификатор s57navy.rsc Для отображения карт нужна библиотека отображения знаков s57navy.iml (s57navy.iml64)
        
        :returns: При ошибке в параметрах возвращает ноль
        :rtype: int
        """
        return LoadS57FolderToMapEx_t (_handle, _folders57.buffer(), _namemap.buffer(), _size, _namersc.buffer(), _sittype, _password.buffer(), _psize, _callevent, _parm, _logfile.buffer())

    vecSaveMapToS57Un_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'vecSaveMapToS57Un', maptype.HMESSAGE, maptype.HMAP, maptype.HSELECT, maptype.HSELECT, maptype.PWCHAR)
    def vecSaveMapToS57Un(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP, _hselect: maptype.HSELECT, _hdepth: maptype.HSELECT, _s57name: mapsyst.WTEXT) -> int:
        """
        Экспорт карты в формата S57 из формата MAP или SIT для карт, которые были ранее импортированы из S57
        
        :param _handle: идентификатор окна диалога, которому посылаются уведомительные сообщения (``HWND`` для Windows, ``CALLBACK``-Функция для Linux)
        
        :param _hmap: идентификатор открытого документа, содержащего векторную карту
        
        :param _hselect: условия отбора листов карты, которые будут сохранены в ``S57``
        
        :param _hdepth: условия отбора отметок глубин (обычно все точечные объекты с кодом ``129``)
        
        :param _s57name: полное имя файла формата ``S57`` (``*.030`` или ``*.000``) Экспорт в ``S57`` выполняется только из главной карты (hsite = hmap), каждый лист карты сохраняется в отдельный набор
        
        :returns: При ошибке в параметрах возвращает ноль
        :rtype: int
        """
        return vecSaveMapToS57Un_t (_handle, _hmap, _hselect, _hdepth, _s57name.buffer())

    vecLoadDxfToMap_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'vecLoadDxfToMap', maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(DXF2MAPPARMS), maptype.PWCHAR, maptype.HMESSAGE, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def vecLoadDxfToMap(_dxfname: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _regionname: mapsyst.WTEXT, _parm: ctypes.POINTER(DXF2MAPPARMS), _customname: mapsyst.WTEXT, _handle: maptype.HMESSAGE, _isutf: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Импорт векторной карты из формата DXF
        
        :param _dxfname: имя текстового файла ``DXF``
        
        :param _mapname: имя создаваемой или обновляемой векторной карты
        
        :param _rscname: имя файла классификатора
        
        :param _regionname: условное название карты
        
        :param _customname: файл соответствия названий слоев ``DXF`` и видов объектов из ``RSC`` или ``0``
        
        :param _parm: параметры для процедуры импорта ``DXF``
        
        :param _handle: идентификатор окна диалога для посылки сообщений
        
        :param _isutf: признак кодировки текстовых данных в ``UTF``-``8``
        
        :param _error: поле для записи кода ошибки выполнения импорта или ``0``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return vecLoadDxfToMap_t (_dxfname.buffer(), _mapname.buffer(), _rscname.buffer(), _regionname.buffer(), _parm, _customname.buffer(), _handle, _isutf, _error)

    vecDxfReadUnits_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'vecDxfReadUnits', maptype.PWCHAR)
    def vecDxfReadUnits(_dxfname: mapsyst.WTEXT) -> int:
        """
        Определить единицу измерения координат в файле DXF
        
        :param _dxfname: путь к файлу dxf, в котором запрашивается единица измерения координат ``1`` - Inches, ``2`` - Feet, ``3`` - Miles, ``4`` - Millimeters, ``5`` - Centimeters, ``6`` - Meters, ``7`` - Kilometers ...
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return vecDxfReadUnits_t (_dxfname.buffer())

    vecCreateDxfLayerNamesList_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_void_p,'vecCreateDxfLayerNamesList', maptype.PWCHAR)
    def vecCreateDxfLayerNamesList(_dxfname: mapsyst.WTEXT) -> ctypes.c_void_p:
        """
        Запросить список слоёв в файле DXF
        
        :param _dxfname: путь к файлу ``DXF``
        
        :returns: Возвращает идентификатор списка слоёв После чтения необходимо освободить память функцией vecFreeDxfLayerNamesList При ошибке возвращает ноль
        """
        return vecCreateDxfLayerNamesList_t (_dxfname.buffer())

    vecFreeDxfLayerNamesList_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_void_p,'vecFreeDxfLayerNamesList', ctypes.c_void_p)
    def vecFreeDxfLayerNamesList(_hdxflayers: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Закрыть список и освободить память
        
        :param _hdxflayers: идентификатор списка слоёв ``DXF``, полученный из vecCreateDxfLayerNamesList
        """
        return vecFreeDxfLayerNamesList_t (_hdxflayers)

    vecGetDxfLayerNamesCount_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'vecGetDxfLayerNamesCount', ctypes.c_void_p)
    def vecGetDxfLayerNamesCount(_hdxflayers: ctypes.c_void_p) -> int:
        """
        Запросить число слоёв в файле DXF
        
        :param _hdxflayers: идентификатор списка слоёв ``DXF`` из функции vecCreateDxfLayerNamesList
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return vecGetDxfLayerNamesCount_t (_hdxflayers)

    vecGetDxfLayerNamesItem_t = mapsyst.GetProcAddress(vecexlib,ctypes.POINTER(maptype.WCHAR),'vecGetDxfLayerNamesItem', ctypes.c_void_p, ctypes.c_long)
    def vecGetDxfLayerNamesItem(_hdxflayers: ctypes.c_void_p, _layernumber: int) -> ctypes.POINTER(maptype.WCHAR):
        """
        Запросить имя слоя DXF из списка по номеру
        
        :param _hdxflayers: идентификатор списка слоёв ``DXF`` из функции vecCreateDxfLayerNamesList
        
        :param _layernumber: номер слоя в списке с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return vecGetDxfLayerNamesItem_t (_hdxflayers, _layernumber)

    vecSaveMapToDxfUn_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'vecSaveMapToDxfUn', maptype.HMAP, maptype.HSITE, ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, maptype.HMESSAGE, ctypes.POINTER(PARMDXF), maptype.HSELECT)
    def vecSaveMapToDxfUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _dxfname: mapsyst.WTEXT, _dxlname: mapsyst.WTEXT, _dxkname: mapsyst.WTEXT, _handle: maptype.HMESSAGE, _parm: ctypes.POINTER(PARMDXF), _hselect: maptype.HSELECT) -> int:
        """
        Экспорт в формат DXF
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор открытой пользовательской карты
        
        :param _list: номер листа карты с ``1``
        
        :param _dxfname: имя текстового файла ``DXF``
        
        :param _dxlname: имя файла знаков или ``0``
        
        :param _dxkname: имя файла кодов или ``0``
        
        :param _handle: идентификатор обработчика сообщений (окна диалога) для посылки сообщений ``WM_OBJECT`` и ``WM_ERROR``
        
        :param _parm: параметры формирования файла ``DXF``
        
        :param _hselect: условия отбора объектов карты или ``0``
        
        :returns: Возвращает число корректно обработанных объектов листа карты При ошибке возвращает ноль
        :rtype: int
        """
        return vecSaveMapToDxfUn_t (_hmap, _hsite, _list, _dxfname.buffer(), _dxlname.buffer(), _dxkname.buffer(), _handle, _parm, _hselect)

    vecTxtTranslate_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'vecTxtTranslate', maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(TXTTRANSLATEPARM), maptype.HMESSAGE, ctypes.POINTER(mapcreat.LOCALDATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def vecTxtTranslate(_inname: mapsyst.WTEXT, _outname: mapsyst.WTEXT, _parm: ctypes.POINTER(TXTTRANSLATEPARM), _handle: maptype.HMESSAGE, _directdatum: ctypes.POINTER(mapcreat.LOCALDATUMPARAM), _directellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        """
        Пересчёт координат в текстовых файлах
        
        :param _inname: входной текстовый файл
        
        :param _outname: выходной текстовый файл
        
        :param _parm: параметры пересчёта координат в текстовых файлах
        
        :param _handle: идентификатор обработчика сообщений (окна диалога)
        
        :param _directdatum: параметры перехода от пользовательской системы координат к геодезической системе на заданном эллипсоиде (обратное преобразование Гельмерта, или Coordinate Frame Rotation; ``EPSG`` dataset coordinate operation method code ``1032``) directoutellipsoid - параметры эллипсоида выходной системы координат (``0``, если не требуется пересчёт по прямому датуму) Структуры ``LOCALDATUMPARAM`` и ``ELLIPSOIDPARAM`` описаны в mapcreat.h
        
        :returns: Возвращает число обработанных строк входного файла При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если пересчет выполняется между пользовательскими системами координат (parm->InHuser и parm->OutHuser) через
           систему WGS84, то параметры directdatum и directoutellipsoid должны быть равны нулю
        """
        return vecTxtTranslate_t (_inname.buffer(), _outname.buffer(), _parm, _handle, _directdatum, _directellipsoid)

    vecLoadTxtToMap_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'vecLoadTxtToMap', maptype.PWCHAR, ctypes.POINTER(TXTTOMAPPARMS), maptype.HMESSAGE)
    def vecLoadTxtToMap(_inputTxtFileName: mapsyst.WTEXT, _parm: ctypes.POINTER(TXTTOMAPPARMS), _hmessage: maptype.HMESSAGE) -> int:
        """
        Импорт векторной карты из формата TXT
        
        :param _inputTxtFileName: имя текстового файла ``TXT``
        
        :param _parm: параметры для процедуры импорта ``TXT``
        
        :param _hmessage: идентификатор окна для посылки сообщений Окну диалога посылается сообщение ``WM_PROGRESSBARUN`` При выборе типа объекта с локализацией ``LOCAL_POINT`` создается столько объектов, сколько записей будет прочитано из файла При выборе типа объекта с локализацией ``LOCAL_LINE`` или ``LOCAL_SQUARE`` cоздается один объект, метрика которого состоит из точек, сформиро- ванных из прочитанных записей
        
        :returns: Возвращает число импортированных объектов При ошибке возвращает ноль
        :rtype: int
        """
        return vecLoadTxtToMap_t (_inputTxtFileName.buffer(), _parm, _hmessage)

    vecCreateMapForNomenclatureListEx_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'vecCreateMapForNomenclatureListEx', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.POINTER(maptype.WCHAR)), ctypes.c_long, ctypes.POINTER(CREATESHEETSPARMEX))
    def vecCreateMapForNomenclatureListEx(_handle: maptype.HMESSAGE, _mapfilename: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _sheetlist: ctypes.POINTER(ctypes.POINTER(maptype.WCHAR)), _sheetlistcount: int, _parm: ctypes.POINTER(CREATESHEETSPARMEX)) -> int:
        """
        Формирование района работ по списку номенклатур
        
        :param _handle: идентификатор диалога для приема сообщений ``WM_PROGRESSBARUN``
        
        :param _mapfilename: имя файла паспорта MAP создаваемой многолистовой карты
        
        :param _rscname: имя файла классификатора ``RSC``
        
        :param _sheetlist: адрес массива указателей на список номенклатур стандартной разграфки для топокарт
        
        :param _sheetlistcount: число номенклатур в списке
        
        :param _parm: параметры создаваемой многолистовой карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return vecCreateMapForNomenclatureListEx_t (_handle, _mapfilename.buffer(), _rscname.buffer(), _sheetlist, _sheetlistcount, _parm)

    vecCreateMapForUser_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'vecCreateMapForUser', maptype.HMESSAGE, maptype.HMAP, maptype.HSITE, ctypes.POINTER(COMPARELISTPARM))
    def vecCreateMapForUser(_handle: maptype.HMESSAGE, _hMap: maptype.HMAP, _hSite: maptype.HSITE, _userParm: ctypes.POINTER(COMPARELISTPARM)) -> int:
        """
        Создание копии фрагмента карты (открепление для автономной работы)
        
        :param _handle: идентификатор окна диалога, которому посылаются уведомительные сообщения (``HWND`` для Windows, ``CALLBACK``-Функция для Linux);
        
        :param _hMap: идентификатор открытых данных
        
        :param _hSite: идентификатор открытой пользовательской карты
        
        :param _userParm: параметры задачи ``"Сравнение двух версий листа карты"``
        """
        return vecCreateMapForUser_t (_handle, _hMap, _hSite, _userParm)

    vecCreateMapProtocol_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'vecCreateMapProtocol', maptype.HMESSAGE, maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR, ctypes.c_int)
    def vecCreateMapProtocol(_handle: maptype.HMESSAGE, _hMap: maptype.HMAP, _userMapName: mapsyst.WTEXT, _standardPath: mapsyst.WTEXT, _userProtocol: mapsyst.WTEXT, _userSize: int, _mapProtocol: mapsyst.WTEXT, _mapSize: int) -> int:
        """
        Формирование протоколов изменений для открепленной карты и базовой карты относительно эталонной
        
        :param _handle: идентификатор окна диалога, которому посылаются уведомительные сообщения (``HWND`` для Windows, ``CALLBACK``-Функция для Linux);
        
        :param _hMap: идентификатор открытых данных
        
        :param _userMapName: имя карты оператора
        
        :param _standardPath: каталог эталонов карт
        
        :param _userProtocol: адрес буфера для размещения пути к протоколу карты пользователя
        
        :param _userSize: размер буфера в байтах
        
        :param _mapProtocol: адрес буфера для размещения пути к протоколу базовой карты
        
        :param _mapSize: размер буфера в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return vecCreateMapProtocol_t (_handle, _hMap, _userMapName.buffer(), _standardPath.buffer(), _userProtocol.buffer(), _userSize, _mapProtocol.buffer(), _mapSize)

    vecCheckReadyForCreateObjectTitle_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'vecCheckReadyForCreateObjectTitle', maptype.HMAP)
    def vecCheckReadyForCreateObjectTitle(_hmap: maptype.HMAP) -> int:
        """
        Проверка возможности построения подписей по выделенным объектам
        
        :param _hmap: идентификатор открытых данных Проверяется наличие выделенных объектов и разрешение на редактирование карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return vecCheckReadyForCreateObjectTitle_t (_hmap)

    vecCreateObjectTitle_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'vecCreateObjectTitle', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(CREATETITLEPARAM))
    def vecCreateObjectTitle(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _param: ctypes.POINTER(CREATETITLEPARAM)) -> int:
        """
        Нанесение подписей на карту по заданным параметрам
        
        :param _hmap: идентификатор открытых данных
        
        :param _handle: идентификатор обработчика сообщений о ходе выполнения нанесения подписей
        
        :param _param: указатель на структуру настроек для подписывания
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return vecCreateObjectTitle_t (_hmap, _handle, _param)

    vecLoadCSVToMap_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'vecLoadCSVToMap', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.POINTER(CSVLOADPARAMS), maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def vecLoadCSVToMap(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _csvname: mapsyst.WTEXT, _csvparams: ctypes.POINTER(CSVLOADPARAMS), _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Загрузить данные на карту из CSV файла
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор карты в данных
        
        :param _csvname: путь к загружаемому файлу в формате ``CSV``
        
        :param _csvparams: параметры  зарузки
        
        :param _callevent: адрес функции оборатного вызова для уведомления о проценте обработанных записей (см. maptype.h)
        
        :param _parm: параметр, который будет передан при вызове функции первым (адрес класса диалога или ноль), вторым параметром в вызываемой функции передается процент от ``0`` до ``100``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return vecLoadCSVToMap_t (_hmap, _hsite, _csvname.buffer(), _csvparams, _callevent, _parm)

    vecSaveMapToCSV_t = mapsyst.GetProcAddress(vecexlib,ctypes.c_long,'vecSaveMapToCSV', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.POINTER(CSVSAVEPARAMS), maptype.HSELECT, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def vecSaveMapToCSV(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _csvname: mapsyst.WTEXT, _csvparams: ctypes.POINTER(CSVSAVEPARAMS), _select: maptype.HSELECT, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Сохранить данные из карты в файл CSV
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор карты в данных
        
        :param _csvname: путь к файлу в формате ``CSV``
        
        :param _csvparams: параметры сохранения
        
        :param _select: фильтр отбора объектов на карте или ``0``
        
        :param _callevent: адрес функции оборатного вызова для уведомления о проценте обработанных записей (см. maptype.h)
        
        :param _parm: параметр, который будет передан при вызове функции первым (адрес класса диалога или ноль), вторым параметром в вызываемой функции передается процент от ``0`` до ``100``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return vecSaveMapToCSV_t (_hmap, _hsite, _csvname.buffer(), _csvparams, _select, _callevent, _parm)



def vecexapi_healthcheck():
    return 1
