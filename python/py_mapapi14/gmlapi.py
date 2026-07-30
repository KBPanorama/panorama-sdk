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
    *       Интерфейс обработки запросов OGC WFS-T (gis64acces.dll)    *
    *              Чтение файлов GML, GeoJSON, KML                     *
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

#-----------------------------
class FEATURELIST(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_uint),
                ("Xmlns",ctypes.c_int),
                ("Hmap",maptype.HMAP),
                ("Hsite",maptype.HSITE),
                ("Hselect",maptype.HSELECT),
                ("Hwnd",maptype.HMESSAGE),
                ("Hobj",maptype.HOBJ),
                ("SemCodeList",ctypes.POINTER(ctypes.c_int)),
                ("Statistic",ctypes.c_void_p),
                ("Dframe",maptype.DFRAME),
                ("Extend",maptype.DFRAME),
                ("Scale",ctypes.c_double),
                ("Flags",ctypes.c_int),
                ("List",ctypes.c_int),
                ("Completed",ctypes.c_int),
                ("Force",ctypes.c_int),
                ("Number",ctypes.c_uint),
                ("Count",ctypes.c_uint),
                ("Epsgcode",ctypes.c_int),
                ("Format",ctypes.c_uint),
                ("ObjectCreateLastStep",ctypes.c_uint),
                ("MathMetod",ctypes.c_uint),
                ("ServiceVersion",ctypes.c_int),
                ("TransactionType",ctypes.c_int),
                ("FindDirection",ctypes.c_int),
                ("SemCodeListCount",ctypes.c_uint),
                ("PrintEpsg",ctypes.c_int),
                ("Test",ctypes.c_int),
                ("ClickPoint",maptype.DOUBLEPOINT),
                ("SortList",ctypes.c_void_p),
                ("SemSortCode",ctypes.c_int),
                ("MultyLevelScale",ctypes.c_int),
                ("ClickPointFrame",maptype.DFRAME),
                ("ExtFlags",ctypes.c_int),
                ("PreviewClusterSize",ctypes.c_int),
                ("StringForSearchInResult",maptype.PWCHAR),
                ("PreviewClusterSavedPath",maptype.PWCHAR),
                ("MaxFileSize",ctypes.c_uint),
                ("IsFirstObject",ctypes.c_uint),
                ("UserPropertiesBlock",ctypes.c_char_p),
                ("SemNameList",ctypes.c_char_p),
                ("SemBlocName",ctypes.c_char_p),
                ("Reserve",ctypes.c_char*(96))]
#-----------------------------


#-----------------------------
class GMLPARAMS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Hwnd",maptype.HMESSAGE),
                ("SquareCode",ctypes.c_int),
                ("PointCode",ctypes.c_int),
                ("LineCode",ctypes.c_int),
                ("TextCode",ctypes.c_int),
                ("Protocol",ctypes.c_int),
                ("SavedObjectNumber",ctypes.c_int),
                ("TurnCoordinate",ctypes.c_int),
                ("CutObjects",ctypes.c_int),
                ("LoadServiceSem",ctypes.c_int),
                ("IsExcode",ctypes.c_int),
                ("SemanticTableFileName",maptype.WCHAR1*(2048)),
                ("Reserve",ctypes.c_char*(68))]
#-----------------------------


#-----------------------------
class CSV_SEMANTIC_TABLE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("FileKey",maptype.WCHAR1*(256)),
                ("SemanticKey",maptype.WCHAR1*(256))]
#-----------------------------




try:
    if os.environ['gisaccesdll']:
        gisaccesname = os.environ['gisaccesdll']
except KeyError:
    gisaccesname = 'gis64acces.dll'

try:
    acceslib = mapsyst.LoadLibrary(gisaccesname)
except Exception as e:
    print(e)
    acceslib = 0

if acceslib == 0:
    print(gisaccesname)
else:
    gmlOpenProEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlOpenProEx', maptype.PWCHAR, maptype.HRSC)
    def gmlOpenProEx(_schemafilename: mapsyst.WTEXT, _hrsc: maptype.HRSC) -> ctypes.c_void_p:
        """
        Открыть доступ к схеме для потокового формирования GML\\JSON
        
        :param _schemafilename: локальный путь к файлу ``XSD``-схемы
        
        :param _hrsc: идентификатор классификатора (может быть получен в mapGetRscIdent, mapGetRscIdentByObject)
        
        :returns: Возвращает идентификатор доступа к GML данным При ошибке возвращает ноль
        
        .. note::

           Если классификатор размещен на ГИС Сервере, то схема открывается через
           идентификатор карты (gmlOpen, gmlOpenEx, gmlOpenUn)
        """
        return gmlOpenProEx_t (_schemafilename.buffer(), _hrsc)

    gmlOpenUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlOpenUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, maptype.PWCHAR)
    def gmlOpenUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _schemafilename: mapsyst.WTEXT, _schemaurl: mapsyst.WTEXT) -> ctypes.c_void_p:
        """
        Открыть доступ к прикладной схеме для заданной карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор открытой пользовательской карты в документе
        
        :param _schemafilename: локальный путь к файлу ``XSD``-схемы ``GML`` данных
        
        :param _schemaurl: ``URL`` к файлу ``XSD``-схемы ``GML`` данных например: ``"http://www.gisinfo.net/bsd/topomap.xsd"`` Для записи набора (dataset) функцией gmlGetFeaturiesDataset доступ к схеме открывается gmlOpenEx По завершении работы необходимо освободить ресурсы вызовом gmlClose
        
        :returns: Возвращает идентификатор доступа к прикладной схеме При ошибке возвращает ноль
        """
        return gmlOpenUn_t (_hmap, _hsite, _schemafilename.buffer(), _schemaurl.buffer())

    gmlSetSchemaLocation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlSetSchemaLocation', ctypes.c_void_p, maptype.PWCHAR)
    def gmlSetSchemaLocation(_hgml: ctypes.c_void_p, _schemalocation: mapsyst.WTEXT) -> int:
        """
        Установить адрес схемы
        
        :param _hgml: идентификатор ``GML`` данных
        
        :param _schemalocation: новый адрес схемы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return gmlSetSchemaLocation_t (_hgml, _schemalocation.buffer())

    gmlClose_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlClose', ctypes.c_void_p)
    def gmlClose(_hgml: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Закрыть доступ к схеме и освободить ресурсы
        
        :param _hgml: идентификатор ``GML`` данных
        """
        return gmlClose_t (_hgml)

    gmlFeatureTypeCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlFeatureTypeCount', ctypes.c_void_p)
    def gmlFeatureTypeCount(_hgml: ctypes.c_void_p) -> int:
        """
        Запросить число типов объектов GML данных (слоев)
        
        :param _hgml: идентификатор ``GML`` данных
        
        :returns: Возвращает число типов объектов GML, содержащихся в схеме При ошибке возвращает ноль
        :rtype: int
        """
        return gmlFeatureTypeCount_t (_hgml)

    gmlFeatureTypeName_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'gmlFeatureTypeName', ctypes.c_void_p, ctypes.c_long)
    def gmlFeatureTypeName(_hgml: ctypes.c_void_p, _number: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить имя типа объекта GML данных по порядковому номеру
        
        :param _hgml: идентификатор ``GML`` данных
        
        :param _number: порядковый номер
        
        :returns: Возвращает имя типа объекта При ошибке возвращает пустую строку
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return gmlFeatureTypeName_t (_hgml, _number)

    gmlFeatureTypeDescription_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'gmlFeatureTypeDescription', ctypes.c_void_p, ctypes.c_long)
    def gmlFeatureTypeDescription(_hGml: ctypes.c_void_p, _number: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить описание типа объекта GML данных по порядковому номеру
        
        :param _hGml: идентификатор ``GML`` данных
        
        :param _number: порядковый номер
        
        :returns: Возвращает описание типа объекта При ошибке возвращает 0
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return gmlFeatureTypeDescription_t (_hGml, _number)

    gmlFeatureTypeNameNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlFeatureTypeNameNumber', ctypes.c_void_p, ctypes.c_char_p)
    def gmlFeatureTypeNameNumber(_hgml: ctypes.c_void_p, _featuretypename: ctypes.c_char_p) -> int:
        """
        Запросить порядковый номер типа объекта по имени типа
        
        :param _hgml: идентификатор открытой схемы для записи ``GML``
        
        :param _featuretypename: имя типа объекта ``GML`` данных
        
        :returns: Возвращает порядковый номер типа объекта в схеме При ошибке возвращает ноль
        :rtype: int
        """
        return gmlFeatureTypeNameNumber_t (_hgml, _featuretypename)

    gmlFeaturiesBoundsPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlFeaturiesBoundsPro', ctypes.c_void_p, maptype.HMAP, maptype.HSITE, ctypes.c_long, maptype.HSELECT, ctypes.c_long, ctypes.POINTER(maptype.DFRAME))
    def gmlFeaturiesBoundsPro(_hgml: ctypes.c_void_p, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _hselect: maptype.HSELECT, _epsgcode: int, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Запросить габариты объектов карты по списку номеров типов объектов
        
        :param _hgml: идентификатор ``GML`` данных
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор открытой пользовательской карты в документе
        
        :param _list: номер обрабатываемого листа на многолистовой карте или ``0`` (все листы)
        
        :param _hselect: идентификатор условий отбора объектов или ``0``
        
        :param _epsgcode: код геодезической системы координат в базе данных ``EPSG``, для ``GML`` по умолчанию - ``4326``
        
        :param _dframe: габариты объектов карты в указанной системе координат
        
        :returns: При ошибке возвращает ноль.
        :rtype: int
        """
        return gmlFeaturiesBoundsPro_t (_hgml, _hmap, _hsite, _list, _hselect, _epsgcode, _dframe)

    gmlGetFeaturiesProEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlGetFeaturiesProEx', ctypes.c_void_p, maptype.HMAP, maptype.HSITE, ctypes.c_long, maptype.HSELECT, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.DFRAME), ctypes.c_long, ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, maptype.HMESSAGE, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.DFRAME))
    def gmlGetFeaturiesProEx(_hgml: ctypes.c_void_p, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _hselect: maptype.HSELECT, _metadata: mapsyst.WTEXT, _number: int, _count: int, _epsgcode: int, _dframe: ctypes.POINTER(maptype.DFRAME), _flags: int, _format: int, _targetfilename: mapsyst.WTEXT, _mapid: mapsyst.WTEXT, _completed: int, _force: int, _hwnd: maptype.HMESSAGE, _requestid: mapsyst.WTEXT, _xmlns: int, _secondframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Запросить данные объектов карты по заданным условиям в файле формата GML или JSON
        
        :param _hgml: идентификатор открытой схемы для записи ``GML``
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор открытой пользовательской карты в документе
        
        :param _list: номер листа для многолистовой карты или ``1``, для конвертирования в один ``GML``-файл сразу всех листов необходимо указать ``"-1"`` или ``0``
        
        :param _hselect: идентификатор условий отбора объектов или ``0``
        
        :param _metadata: метаданные
        
        :param _number: порядковый номер объекта, с которого начинать вывод в файл (с ``1``)
        
        :param _count: число объектов, выводимых в файл, если равно ``0``, то выводятся все объекты
        
        :param _epsgcode: код системы координат в базе данных ``EPSG``, для ``GML`` по умолчанию - ``4326``, или -``1`` (выводить текущую систему координат, как местную)
        
        :param _dframe: область отбора объектов карты в указанной системе координат или ``0`` (левый нижний и правый верхний угол области)
        
        :param _flags: флажки вывода расширенных метаданных об объекте (описание в ``OGCSERVICEFLAG``)
        
        :param _format: тип разметки или формат файла: ``GML``, ``GML``/``WFS``, ``JSON``  (описание в ``OGCSERVICETYPE``)
        
        :param _targetfilename: имя выходного файла
        
        :param _mapid: указатель на идентификатор карты, который записывается в каждый объект карты или ``0``
        
        :param _completed: признак необходимости записи элементов начала и конца файла (``0`` - не формировать, ``1`` - только закрывающий, ``2`` - только начальные теги, -``1`` - начало и конец данных) при значении ``0`` и ``1`` файл для записи должен существовать, при значении ``2`` и -``1`` файл создается автоматически
        
        :param _force: признак принудительной записи объектов, которые не описаны в прикладной схеме, если равен нулю, то записываются только объекты, виды (коды) которых описаны в схеме
        
        :param _hwnd: идентификатор окна для приема сообщений или ноль, посылаются сообщения ``WM_OBJECT`` (``%``, число объектов)
        
        :param _requestid: идентификатор запроса
        
        :param _xmlns: признак записи пространства имен в тег member для gml/wfs
        
        :param _secondframe: дополнительные точки для области отбора объектов карты в указанной системе координат
        
        :returns: Возвращает число записанных объектов Если заданы слои, содержащие объекты, которых нет на карте, то возвращает -1 Если условиям поиска не соответствует ни один объект, то возвращает -2 Если выходной файл не может быть открыт, то возвращает -3 Если произошел сбой при работе программы, то возвращает -4 Если для карты запрещено копирование, то возвращает -5
        :rtype: int
        """
        return gmlGetFeaturiesProEx_t (_hgml, _hmap, _hsite, _list, _hselect, _metadata.buffer(), _number, _count, _epsgcode, _dframe, _flags, _format, _targetfilename.buffer(), _mapid.buffer(), _completed, _force, _hwnd, _requestid.buffer(), _xmlns, _secondframe)

    gmlGetFeaturiesProInMemory_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlGetFeaturiesProInMemory', ctypes.c_void_p, maptype.HMAP, maptype.HSITE, ctypes.c_long, maptype.HSELECT, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.DFRAME), ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_long), maptype.PWCHAR, ctypes.c_long)
    def gmlGetFeaturiesProInMemory(_hgml: ctypes.c_void_p, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _hselect: maptype.HSELECT, _metadata: mapsyst.WTEXT, _number: int, _count: int, _epsgcode: int, _dframe: ctypes.POINTER(maptype.DFRAME), _flags: int, _format: int, _mapid: mapsyst.WTEXT, _completed: int, _force: int, _retcode: ctypes.POINTER(ctypes.c_long), _requestid: mapsyst.WTEXT, _xmlns: int) -> ctypes.c_void_p:
        """
        Запросить данные объектов карты по заданным условиям в памяти в формате GML или JSON
        
        :param _hgml: идентификатор открытой схемы для записи ``GML``
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор открытой пользовательской карты в документе
        
        :param _list: номер листа для многолистовой карты или ``1``, для конвертирования в один ``GML``-файл сразу всех листов необходимо указать ``"-1"`` или ``0``
        
        :param _hselect: идентификатор условий отбора объектов или ``0``
        
        :param _metadata: метаданные
        
        :param _number: порядковый номер объекта, с которого начинать вывод в файл (с ``1``)
        
        :param _count: число объектов, выводимых в файл, если равно ``0``, то выводятся все объекты
        
        :param _epsgcode: код системы координат в базе данных ``EPSG``, для ``GML`` по умолчанию - ``4326``, или -``1`` (выводить текущую систему координат, как местную)
        
        :param _dframe: бласть отбора объектов карты в указанной системе координат или ``0`` (левый нижний и правый верхний угол области)
        
        :param _flags: флажки вывода расширенных метаданных об объекте (описание в ``OGCSERVICEFLAG``)
        
        :param _format: тип разметки или формат файла: ``GML``, ``GML``/``WFS``, ``JSON``  (описание в ``OGCSERVICETYPE``) targetfilename - имя выходного файла
        
        :param _mapid: указатель на идентификатор карты, который записывается в каждый объект карты или ``0``
        
        :param _completed: признак необходимости записи элементов начала и конца файла (``0`` - не формировать, ``1`` - только закрывающий, ``2`` - только начальные теги, -``1`` - начало и конец данных) при значении ``0`` и ``1`` файл для записи должен существовать, при значении ``2`` и -``1`` файл создается автоматически
        
        :param _force: признак принудительной записи объектов, которые не описаны в прикладной схеме, если равен нулю, то записываются только объекты, виды (коды) которых описаны в схеме
        
        :param _retcode: адрес, по которому пишут число записанных объектов или код ошибки
        
        :param _requestid: идентификатор запроса
        
        :param _xmlns: признак записи пространства имен в тег member для gml/wfs flagsext    - дополнительные флажки вывода метаданных об объекте (описание в ``OGC_SERVICE_FLAG_EXTENDED``) (подается дополнительно к dframe, левый верхний и правый нижний угол области) Для чтения из памяти результата необходимо вызвать gmlGetFeaturiesPoint
        
        :returns: Возвращает в параметре retcode число записанных объектов или код ошибки Если заданы слои, содержащие объекты, которых нет на карте, то записывает -1 Если условиям поиска не соответствует ни один объект, то записывает -2 Если произошел сбой при работе программы, то записывает -4 Если для карты запрещено копирование, то записывает -5 При ошибке возвращает ноль иначе идентификатор данных в памяти
        
        .. note::

           После завершения чтения необходимо освободить память вызовом gmlFreeFeaturiesPoint
           Если объем данных слишком большой, то функция может занять всю память в системе
        """
        return gmlGetFeaturiesProInMemory_t (_hgml, _hmap, _hsite, _list, _hselect, _metadata.buffer(), _number, _count, _epsgcode, _dframe, _flags, _format, _mapid.buffer(), _completed, _force, _retcode, _requestid.buffer(), _xmlns)

    gmlGetFeaturiesPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'gmlGetFeaturiesPoint', ctypes.c_void_p, ctypes.POINTER(ctypes.c_long))
    def gmlGetFeaturiesPoint(_handle: ctypes.c_void_p, _size: ctypes.POINTER(ctypes.c_long)) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить указатель на данные в памяти по идентификатору данных
        
        :param _handle: идентификатор данных
        
        :param _size: указатель на поле для записи длины запрошенных данных Идентификатор данных может быть получен в gmlGetFeaturiesProInMemory или gmlGetObjectFeatureProInMemory
        
        :returns: При ошибке возвращает ноль иначе указатель на данные в памяти
        :rtype: ctypes.POINTER(ctypes.c_char)
        
        .. note::

           После завершения чтения необходимо освободить память вызовом gmlFreeFeaturiesPoint
        """
        return gmlGetFeaturiesPoint_t (_handle, _size)

    gmlFreeFeaturiesPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlFreeFeaturiesPoint', ctypes.c_void_p)
    def gmlFreeFeaturiesPoint(_handle: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Освободить память под данные по идентификатору данных
        
        :param _handle: идентификатор данных Идентификатор данных может быть получен в gmlGetFeaturiesProInMemory или gmlGetObjectFeatureProInMemory
        """
        return gmlFreeFeaturiesPoint_t (_handle)

    gmlGetObjectFeaturePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlGetObjectFeaturePro', ctypes.c_void_p, maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def gmlGetObjectFeaturePro(_hgml: ctypes.c_void_p, _hobj: maptype.HOBJ, _epsgcode: int, _flags: int, _format: int, _targetfilename: mapsyst.WTEXT, _mapid: mapsyst.WTEXT, _completed: int, _requestid: mapsyst.WTEXT, _xmlns: int) -> int:
        """
        Запросить данные объекта карты в файле формата GML или JSON
        
        :param _hgml: идентификатор открытой схемы для записи ``GML`` (может быть равен нулю)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _epsgcode: код геодезической системы координат в базе данных ``EPSG``
        
        :param _flags: флажки вывода расширенных метаданных об объекте (описание в ``OGCSERVICEFLAG``)
        
        :param _format: формат вывода данных: ``GML``, ``JSON`` (описание в ``OGCSERVICETYPE``)
        
        :param _targetfilename: имя выходного ``GML`` или ``JSON`` файла
        
        :param _mapid: указатель на идентификатор карты, который записывается в каждый объект карты или ``0``
        
        :param _completed: признак необходимости записи элементов начала и конца файла (``0`` - не формировать, ``1`` - только закрывающий, ``2`` - только начальные теги, -``1`` - начало и конец данных) при значении ``0`` и ``1`` файл для записи должен существовать, при значении ``2`` и -``1`` файл создается автоматически
        
        :param _requestid: идентификатор запроса для записи в метаданные
        
        :param _xmlns: признак записи пространства имен в тег member для gml/wfs
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return gmlGetObjectFeaturePro_t (_hgml, _hobj, _epsgcode, _flags, _format, _targetfilename.buffer(), _mapid.buffer(), _completed, _requestid.buffer(), _xmlns)

    gmlGetObjectFeatureProInMemory_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlGetObjectFeatureProInMemory', ctypes.c_void_p, maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_void_p, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long), maptype.PWCHAR, ctypes.c_long)
    def gmlGetObjectFeatureProInMemory(_hgml: ctypes.c_void_p, _hobj: maptype.HOBJ, _epsgcode: int, _flags: int, _format: int, _handle: ctypes.c_void_p, _mapid: mapsyst.WTEXT, _completed: int, _retcode: ctypes.POINTER(ctypes.c_long), _requestid: mapsyst.WTEXT, _xmlns: int) -> ctypes.c_void_p:
        """
        Запросить данные объекта карты в памяти в формате GML или JSON
        
        :param _hgml: идентификатор открытой схемы для записи ``GML`` (может быть равен нулю)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _epsgcode: код геодезической системы координат в базе данных ``EPSG``
        
        :param _flags: флажки вывода расширенных метаданных об объекте (описание в ``OGCSERVICEFLAG``)
        
        :param _handle: при первом вызове ``0``; значение, которое вернула функция при первом вызове, когда параметр был равен ``0`` (параметр handle должен содержать ненулевое значение для дозаписи в память новых объектов)
        
        :param _format: формат вывода данных: ``GML``, ``JSON`` (описание в ``OGCSERVICETYPE``)
        
        :param _mapid: указатель на идентификатор карты, который записывается в каждый объект карты или ``0``
        
        :param _completed: признак необходимости записи элементов начала и конца файла (``0`` - не формировать, ``1`` - только закрывающий, ``2`` - только начальные теги, -``1`` - начало и конец данных) при значении ``0`` и ``1`` файл для записи должен существовать, при значении ``2`` и -``1`` файл создается автоматически
        
        :param _retcode: адрес, по которому пишут число записанных объектов или код ошибки
        
        :param _requestid: идентификатор запроса для записи в метаданные
        
        :param _xmlns: признак записи пространства имен в тег member для gml/wfs Для чтения из памяти результата необходимо вызвать gmlGetFeaturiesPoint
        
        :returns: Возвращает в параметре retcode число записанных объектов или код ошибки Если заданы слои, содержащие объекты, которых нет на карте, то записывает -1 Если условиям поиска не соответствует ни один объект, то записывает -2 Если произошел сбой при работе программы, то записывает -4 Если для карты запрещено копирование, то записывает -5 При ошибке возвращает ноль иначе идентификатор данных в памяти
        
        .. note::

           После завершения чтения необходимо освободить память вызовом gmlFreeFeaturiesPoint
        """
        return gmlGetObjectFeatureProInMemory_t (_hgml, _hobj, _epsgcode, _flags, _format, _handle, _mapid.buffer(), _completed, _retcode, _requestid.buffer(), _xmlns)

    gmlGetFeatureByIdPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlGetFeatureByIdPro', ctypes.c_void_p, maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long, ctypes.c_char_p, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, maptype.PWCHAR)
    def gmlGetFeatureByIdPro(_hgml: ctypes.c_void_p, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _epsgcode: int, _id: ctypes.c_char_p, _flags: int, _format: int, _targetfilename: mapsyst.WTEXT, _mapid: mapsyst.WTEXT, _completed: int, _requestid: mapsyst.WTEXT) -> int:
        """
        Запросить данные объекта карты по GML-идентификатору
        
        :param _hgml: идентификатор открытой схемы для записи ``GML``
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор открытой пользовательской карты в документе
        
        :param _list: номер листа для многолистовой карты или ``1``
        
        :param _epsgcode: код геодезической системы координат в базе данных ``EPSG``
        
        :param _id: ``GML``-идентификатор объекта
        
        :param _flags: флажки вывода расширенных метаданных об объекте (описание в ``OGCSERVICEFLAG``)
        
        :param _format: формат вывода данных: ``GML``, ``JSON`` (описание в ``OGCSERVICETYPE``)
        
        :param _targetfilename: имя выходного файла
        
        :param _mapid: указатель на идентификатор карты, который записывается в каждый объект карты или ``0``
        
        :param _completed: признак необходимости записи элементов начала и конца файла (``0`` - не формировать, ``1`` - только закрывающий, ``2`` - только начальные теги, -``1`` - начало и конец данных)
        
        :param _requestid: идентификатор запроса для записи в метаданные
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return gmlGetFeatureByIdPro_t (_hgml, _hmap, _hsite, _list, _epsgcode, _id, _flags, _format, _targetfilename.buffer(), _mapid.buffer(), _completed, _requestid.buffer())

    gmlGeoToGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlGeoToGeo', ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.DFRAME))
    def gmlGeoToGeo(_epsgcodesource: int, _epsgcodedest: int, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Преобразовать координаты рамки из одной геодезической системы координат в другую геодезическую систему координат
        
        :param _epsgcodesource: код исходной геодезической системы координат в базе данных ``EPSG``
        
        :param _epsgcodedest: код выходной геодезической системы координат в базе данных ``EPSG``
        
        :param _dframe: координаты рамки в исходной системе координат в радианах Коды могут быть в диапазоне ``4326`` - ``4937``
        
        :returns: Возвращает по адресу dframe значения координат в СК epsgcodedest При ошибке возвращает ноль.
        :rtype: int
        """
        return gmlGeoToGeo_t (_epsgcodesource, _epsgcodedest, _dframe)

    gmlSetSelectByFeaturieType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlSetSelectByFeaturieType', ctypes.c_void_p, maptype.HSELECT, ctypes.c_char_p)
    def gmlSetSelectByFeaturieType(_hgml: ctypes.c_void_p, _hselect: maptype.HSELECT, _featuretype: ctypes.c_char_p) -> int:
        """
        Установить отбор объектов по идентификатору слоя
        
        :param _hgml: идентификатор открытой схемы для записи ``GML``
        
        :param _hselect: идентификатор условий отбора объектов
        
        :param _featuretype: идентификатор слоя в кодировке ``UTF``-``8``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return gmlSetSelectByFeaturieType_t (_hgml, _hselect, _featuretype)

    gmlCreateObjectsFromJSONPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlCreateObjectsFromJSONPro', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.HMESSAGE, ctypes.c_long)
    def gmlCreateObjectsFromJSONPro(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _jsonname: mapsyst.WTEXT, _squarecode: int, _pointcode: int, _linecode: int, _textcode: int, _hwnd: maptype.HMESSAGE, _charset: int) -> int:
        """
        Cоздание объектов из файла формата geoJSON
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор открытой пользовательской карты
        
        :param _jsonname: имя файла формата GeoJSON
        
        :param _squarecode: код создаваемых площадных объектов или ``0``
        
        :param _pointcode: код создаваемых точечных объектов или ``0``
        
        :param _linecode: код создаваемых линейных объектов или ``0``
        
        :param _textcode: код создаваемых подписей или ``0``
        
        :param _hwnd: идентификатор окна для приема сообщений или ноль, посылаются сообщения ``WM_PROGRESSBAR``
        
        :param _charset: кодировка текста (``0`` - ``UTF``-``8`` или ``1`` - ``ANSI``) Код создаваемого объекта ищется в поле code (``"code"``: ``115001010``,)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если код не задан в объекте, то он выбирается из входных параметров
        """
        return gmlCreateObjectsFromJSONPro_t (_hmap, _hsite, _jsonname.buffer(), _squarecode, _pointcode, _linecode, _textcode, _hwnd, _charset)

    gmlCreateObjectsFromJSONStreamByParams_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlCreateObjectsFromJSONStreamByParams', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.c_long, ctypes.POINTER(GMLPARAMS))
    def gmlCreateObjectsFromJSONStreamByParams(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _stream: ctypes.c_char_p, _streamlength: int, _gmlparam: ctypes.POINTER(GMLPARAMS)) -> int:
        """
        Cоздание объектов из файла формата geoJSON
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор открытой пользовательской карты
        
        :param _stream: указатель на данные, в котором находится транзакции
        
        :param _streamlength: длина потока
        
        :param _gmlparam: параметры для создания карты из gml Код создаваемого объекта ищется в поле code (``"code"``: ``115001010``,)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если код не задан в объекте, то он выбирается из входных параметров
        """
        return gmlCreateObjectsFromJSONStreamByParams_t (_hmap, _hsite, _stream, _streamlength, _gmlparam)

    gmlFreeJsonHandle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlFreeJsonHandle', ctypes.c_void_p)
    def gmlFreeJsonHandle(_hjson: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Освободить идентификатор данных json
        
        :param _hjson: идентификатор данных, полученный в функциях gmlLoadJsonTransactionToMap
        """
        return gmlFreeJsonHandle_t (_hjson)

    gmlLoadJsonTransactionToMapBySelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlLoadJsonTransactionToMapBySelect', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.c_long, ctypes.c_long, maptype.HSELECT)
    def gmlLoadJsonTransactionToMapBySelect(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _stream: ctypes.c_char_p, _streamlength: int, _protocol: int, _hselect: maptype.HSELECT) -> ctypes.c_void_p:
        """
        Cоздать объекты из потока транзакций
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор открытой пользовательской карты
        
        :param _stream: указатель на данные, в котором находится транзакции
        
        :param _streamlength: длина потока
        
        :param _protocol: флаг формирования лога ошибок
        
        :param _hselect: идентификатор условий отбора объектов
        
        :returns: При ошибке возвращает 0, иначе идентификатор данных
        """
        return gmlLoadJsonTransactionToMapBySelect_t (_hmap, _hsite, _stream, _streamlength, _protocol, _hselect)

    gmlGetJsonObjectsNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_int),'gmlGetJsonObjectsNumber', ctypes.c_void_p)
    def gmlGetJsonObjectsNumber(_hjson: ctypes.c_void_p) -> ctypes.POINTER(ctypes.c_int):
        """
        Запросить массив уникальных номеров созданных объектов
        
        :param _hjson: идентификатор данных
        
        :returns: Возвращает массив номеров объектов int При ошибке возвращает 0
        :rtype: ctypes.POINTER(ctypes.c_int)
        """
        return gmlGetJsonObjectsNumber_t (_hjson)

    gmlGetJsonCreateObjectsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlGetJsonCreateObjectsCount', ctypes.c_void_p)
    def gmlGetJsonCreateObjectsCount(_hjson: ctypes.c_void_p) -> int:
        """
        Запросить количество созданных объектов
        
        :param _hjson: идентификатор данных
        
        :returns: Возвращает количество созданных объектов При ошибке возвращает 0
        :rtype: int
        """
        return gmlGetJsonCreateObjectsCount_t (_hjson)

    gmlGetJsonUpdateObjectsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlGetJsonUpdateObjectsCount', ctypes.c_void_p)
    def gmlGetJsonUpdateObjectsCount(_hjson: ctypes.c_void_p) -> int:
        """
        Запросить количество обновленных объектов при выполнении транзакций
        
        :param _hjson: идентификатор данных
        
        :returns: Возвращает количество обновленных объектов При ошибке возвращает 0
        :rtype: int
        """
        return gmlGetJsonUpdateObjectsCount_t (_hjson)

    gmlGetJsonDeleteObjectsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlGetJsonDeleteObjectsCount', ctypes.c_void_p)
    def gmlGetJsonDeleteObjectsCount(_hjson: ctypes.c_void_p) -> int:
        """
        Запросить количество удаленных объектов при выполнении транзакций
        
        :param _hjson: идентификатор данных
        
        :returns: Возвращает количество удаленных объектов При ошибке возвращает 0
        :rtype: int
        """
        return gmlGetJsonDeleteObjectsCount_t (_hjson)

    gmlGetJsonReplaceObjectsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlGetJsonReplaceObjectsCount', ctypes.c_void_p)
    def gmlGetJsonReplaceObjectsCount(_hjson: ctypes.c_void_p) -> int:
        """
        Запросить количество заменённых объектов при выполнении транзакций
        
        :param _hjson: идентификатор данных
        
        :returns: Возвращает количество заменённых объектов При ошибке возвращает 0
        :rtype: int
        """
        return gmlGetJsonReplaceObjectsCount_t (_hjson)

    gmlGetJsonTransactionObjectsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlGetJsonTransactionObjectsCount', ctypes.c_void_p)
    def gmlGetJsonTransactionObjectsCount(_hjson: ctypes.c_void_p) -> int:
        """
        Запросить количество объектов, присланных в транзакции
        
        :param _hjson: идентификатор данных
        
        :returns: При ошибке возвращает 0, иначе количество присланных объектов
        :rtype: int
        """
        return gmlGetJsonTransactionObjectsCount_t (_hjson)

    gmlGetJsonTransactionNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlGetJsonTransactionNumber', ctypes.c_void_p)
    def gmlGetJsonTransactionNumber(_hjson: ctypes.c_void_p) -> int:
        """
        Запросить номер сформированной транзакции
        
        :param _hjson: идентификатор данных
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return gmlGetJsonTransactionNumber_t (_hjson)

    gmlSaveFileEndPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlSaveFileEndPro', ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_char_p, ctypes.c_long, ctypes.c_long)
    def gmlSaveFileEndPro(_format: int, _targetfilename: mapsyst.WTEXT, _matched: int, _returned: int, _data: ctypes.c_char_p, _datasize: int, _saveclosedtag: int) -> int:
        """
        Записать завершающие теги
        
        :param _format: формат вывода данных: ``GML``, ``JSON`` (описание в ``OGCSERVICETYPE``)
        
        :param _targetfilename: имя выходного файла
        
        :param _matched: количество найденных объектов
        
        :param _data: данные которые необходимо дописать в конец файла
        
        :param _datasize: размер данных
        
        :param _saveclosedtag: сохранять закрывающий тэг
        
        :returns: returned       - количество объектов, записанных в GML При ошибке возвращает ноль
        :rtype: int
        """
        return gmlSaveFileEndPro_t (_format, _targetfilename.buffer(), _matched, _returned, _data, _datasize, _saveclosedtag)

    gmlSaveStatistic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlSaveStatistic', ctypes.c_long, maptype.PWCHAR, ctypes.c_void_p)
    def gmlSaveStatistic(_format: int, _targetfilename: mapsyst.WTEXT, _statistic: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Записать собранную статистику по запросу: количество объектов, семантик, слоёв
        
        :param _format: формат вывода данных: ``GML``, ``JSON`` (описание в ``OGCSERVICETYPE``)
        
        :param _targetfilename: имя выходного ``GML``-файла
        
        :param _statistic: указатель на собранную статистику по предыдущим запросам
        """
        return gmlSaveStatistic_t (_format, _targetfilename.buffer(), _statistic)

    gmlFreeStatistic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlFreeStatistic', ctypes.c_void_p)
    def gmlFreeStatistic(_statistic: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Освободить собранную статистику по запросу
        
        :param _statistic: указатель на собранную статистику по предыдущим запросам
        """
        return gmlFreeStatistic_t (_statistic)

    gmlSaveSortList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlSaveSortList', ctypes.c_void_p, ctypes.c_long, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def gmlSaveSortList(_sortlist: ctypes.c_void_p, _format: int, _targetfilename: mapsyst.WTEXT, _numberbegin: int, _count: int) -> int:
        """
        Записать отсортированный массив в файл
        
        :param _sortlist: указатель на массив объектов, собранный по предыдущим запросам
        
        :param _format: формат вывода данных: ``GML``, ``JSON`` (описание в ``OGCSERVICETYPE``)
        
        :param _targetfilename: имя выходного ``GML``-файла
        
        :param _numberbegin: номер начального объекта или ``0``
        
        :param _count: вывод определенного количества объектов
        """
        return gmlSaveSortList_t (_sortlist, _format, _targetfilename.buffer(), _numberbegin, _count)

    gmlFreeSortList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlFreeSortList', ctypes.c_void_p)
    def gmlFreeSortList(_sortlist: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Освободить массив
        
        :param _sortlist: указатель на массив объектов, собранный по предыдущим запросам
        """
        return gmlFreeSortList_t (_sortlist)

    gmlGetJSONBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlGetJSONBorder', maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME))
    def gmlGetJSONBorder(_name: mapsyst.WTEXT, _border: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Запросить габариты объектов файла geojson и числа объектов
        
        :param _name: имя файла geojson
        
        :param _border: габариты объектов в радианах в СК ``WGS``-``84``
        
        :returns: Если число объектов не может быть определено, то возвращает -1 При ошибке возвращает 0
        :rtype: int
        """
        return gmlGetJSONBorder_t (_name.buffer(), _border)

    gmlCheckJSON_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlCheckJSON', maptype.PWCHAR)
    def gmlCheckJSON(_name: mapsyst.WTEXT) -> int:
        """
        Проверить, что это geojson
        
        :param _name: имя файла geojson Функция ищет узел ``"type"``:``"FeatureCollection"``
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return gmlCheckJSON_t (_name.buffer())

    gmlCheckJSONFromStream_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlCheckJSONFromStream', ctypes.c_char_p, ctypes.c_long)
    def gmlCheckJSONFromStream(_stream: ctypes.c_char_p, _streamlength: int) -> int:
        """
        Проверить, что это geojson
        
        :param _stream: входной файл в памяти
        
        :param _streamlength: длина файла Функция ищет узел ``"type"``:``"FeatureCollection"``
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return gmlCheckJSONFromStream_t (_stream, _streamlength)

    mapLoadKmlToMapEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLoadKmlToMapEx', maptype.PWCHAR, maptype.HMAP, maptype.HSITE, maptype.HMESSAGE, ctypes.POINTER(ctypes.c_long))
    def mapLoadKmlToMapEx(_kmlname: mapsyst.WTEXT, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _hwnd: maptype.HMESSAGE, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Импортировать данные из файла KML/KMZ на карту (без настройки ключей из RSC)
        
        :param _kmlname: имя файла ``KML``/``KMLZ``
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор открытой пользовательской карты в документе
        
        :param _hwnd: идентификатор (окна или функции обратного вызова Linux) для сообщений о ходе процесса ``WM_PROGRESSBAR``
        
        :param _error: поле для записи кода ошибки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapLoadKmlToMapEx_t (_kmlname.buffer(), _hmap, _hsite, _hwnd, _error)

    mapOpenKml_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapOpenKml', maptype.PWCHAR, ctypes.POINTER(ctypes.c_long), ctypes.c_long)
    def mapOpenKml(_kmlname: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_long), _selectstyle: int) -> ctypes.c_void_p:
        """
        Открыть файл KML/KMZ
        
        :param _kmlname: имя файла ``KML``
        
        :param _error: поле для записи кода ошибки selectstyle
        
        :returns: При ошибке возвращает ноль, иначе - идентификатор открытого файла KML
        """
        return mapOpenKml_t (_kmlname.buffer(), _error, _selectstyle)

    mapCloseKml_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseKml', ctypes.c_void_p)
    def mapCloseKml(_hkml: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Закрыть доступ к файлу KML/KMZ и освободить ресурсы
        
        :param _hkml: идентификатор доступа к файлу kml, созданный функцией mapOpenKml
        """
        return mapCloseKml_t (_hkml)

    mapGetKmlStylesCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetKmlStylesCount', ctypes.c_void_p)
    def mapGetKmlStylesCount(_hkml: ctypes.c_void_p) -> int:
        """
        Запросить число стилей <Style>, найденных в файле
        
        :param _hkml: идентификатор доступа к файлу kml, созданный функцией mapOpenKml
        
        :returns: При ошибке возвращает ноль, иначе - число найденных стилей
        :rtype: int
        """
        return mapGetKmlStylesCount_t (_hkml)

    mapGetKmlStyleId_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetKmlStyleId', ctypes.c_void_p, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetKmlStyleId(_hkml: ctypes.c_void_p, _number: int, _styleid: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить идентификатор стиля по номеру
        
        :param _hkml: идентификатор доступа к файлу kml, созданный функцией mapOpenKml
        
        :param _number: номер стиля в списке от ``1`` до mapGetKmlStylesCount()
        
        :param _styleid: буфер для записи строки - идентификатора стиля
        
        :param _size: размер буфера в байтах
        
        :returns: При ошибке возвращает ноль, иначе - идентификатор стиля
        :rtype: int
        """
        return mapGetKmlStyleId_t (_hkml, _number, _styleid.buffer(), _size)

    mapGetKmlStyleImage_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(mapgdi.IMGDRAW),'mapGetKmlStyleImage', ctypes.c_void_p, ctypes.c_long)
    def mapGetKmlStyleImage(_hkml: ctypes.c_void_p, _number: int) -> ctypes.POINTER(mapgdi.IMGDRAW):
        """
        Запросить запись параметров стиля по номеру
        
        :param _hkml: идентификатор доступа к файлу kml, созданный функцией mapOpenKml
        
        :param _number: номер стиля в списке от ``1`` до mapGetKmlStylesCount()
        
        :returns: При ошибке возвращает ноль, иначе - указатель на запись параметров
        :rtype: ctypes.POINTER(mapgdi.IMGDRAW)
        """
        return mapGetKmlStyleImage_t (_hkml, _number)

    mapSetKmlStyleObjectKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetKmlStyleObjectKey', ctypes.c_void_p, ctypes.c_long, ctypes.c_char_p)
    def mapSetKmlStyleObjectKey(_hkml: ctypes.c_void_p, _number: int, _key: ctypes.c_char_p) -> int:
        """
        Установить ключ объекта для стиля по номеру
        
        :param _hkml: идентификатор доступа к файлу kml, созданный функцией mapOpenKml
        
        :param _number: номер стиля в списке от ``1`` до mapGetKmlStylesCount(), если номер равен -``1``, то устанавливается умалчиваемое значение для всех записей, кроме тех, которым назначено значение через номер стиля
        
        :param _key: ключ объекта из ``RSC``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetKmlStyleObjectKey_t (_hkml, _number, _key)

    mapSetKmlStyleObjectKeyForIdent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetKmlStyleObjectKeyForIdent', ctypes.c_void_p, maptype.PWCHAR, ctypes.c_char_p)
    def mapSetKmlStyleObjectKeyForIdent(_hkml: ctypes.c_void_p, _styleid: mapsyst.WTEXT, _key: ctypes.c_char_p) -> int:
        """
        Установить ключ объекта для стиля по идентификатору
        
        :param _hkml: идентификатор доступа к файлу kml, созданный функцией mapOpenKml
        
        :param _styleid: идентификатор стиля
        
        :param _key: ключ объекта из ``RSC``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetKmlStyleObjectKeyForIdent_t (_hkml, _styleid.buffer(), _key)

    mapGetKmlStyleObjectKey_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetKmlStyleObjectKey', ctypes.c_void_p, ctypes.c_long)
    def mapGetKmlStyleObjectKey(_hkml: ctypes.c_void_p, _number: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить ключ объекта для стиля по номеру
        
        :param _hkml: идентификатор доступа к файлу kml, созданный функцией mapOpenKml
        
        :param _number: номер стиля в списке от ``1`` до mapGetKmlStylesCount(), если номер равен -``1``, то запрашивается умалчиваемое значение для всех записей, кроме тех, которым назначено значение через номер стиля
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetKmlStyleObjectKey_t (_hkml, _number)

    mapLoadKmlToMapPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLoadKmlToMapPro', ctypes.c_void_p, maptype.HMAP, maptype.HSITE, maptype.HMESSAGE, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long), maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def mapLoadKmlToMapPro(_hkml: ctypes.c_void_p, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _hwnd: maptype.HMESSAGE, _errorcount: ctypes.POINTER(ctypes.c_long), _objectcount: ctypes.POINTER(ctypes.c_long), _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Импортировать данные из файла KML/KMZ на карту с учетом настроенных ключей объектов
        
        :param _hkml: идентификатор доступа к файлу kml, созданный функцией mapOpenKml
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор открытой пользовательской карты в документе
        
        :param _hwnd: идентификатор (окна или функции обратного вызова Linux) для сообщений о ходе процесса ``WM_PROGRESSBAR``
        
        :param _errorcount: поле для записи числа ошибок при импорте файла ``KML``
        
        :param _objectcount: поле для записи числа созданных объектов
        
        :param _callevent: адрес функции обратного вызова для получения уведомлений о проценте загруженных данных (описание в  maptype.h)
        
        :param _parm: параметр, передаваемый в функцию обратного вызова (например, адрес класса обработки сообщений)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapLoadKmlToMapPro_t (_hkml, _hmap, _hsite, _hwnd, _errorcount, _objectcount, _callevent, _parm)

    mapSaveMapToKmlEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSaveMapToKmlEx', maptype.HMAP, maptype.HSITE, maptype.HSELECT, maptype.HMESSAGE, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_int), ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapSaveMapToKmlEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT, _hwnd: maptype.HMESSAGE, _kmlname: mapsyst.WTEXT, _imgsize: int, _semcodelist: ctypes.POINTER(ctypes.c_int), _semcodecount: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Экспортировать карту в файл формата KML/KMZ
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор открытой пользовательской карты в документе
        
        :param _hselect: условия отбора объектов или ``0`` (вся карта)
        
        :param _hwnd: идентификатор (окна или функции обратного вызова Linux) для сообщений о ходе процесса ``WM_OBJECT``
        
        :param _kmlname: полный путь к файлу ``KML`` или ``KMZ``
        
        :param _imgsize: размер иконок в пикселах (например: ``32``, ``48``, ``64``, ...)
        
        :param _semcodelist: указатель на список кодов семантик, которые нужно сохранить в ``KML``, или ``0``
        
        :param _semcodecount: число кодов семантик в списке или ``0``
        
        :param _error: поле для записи кода ошибки (описание в maperr.rh) При формировании файла kml иконки сохраняются в формате png в папку ``"имя_файла.icons/"`` рядом с файлом kml Файл kmz содержит файл kml и все иконки в одном архиве
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSaveMapToKmlEx_t (_hmap, _hsite, _hselect, _hwnd, _kmlname.buffer(), _imgsize, _semcodelist, _semcodecount, _error)

    gmlLoadGmlTransactionToMapEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlLoadGmlTransactionToMapEx', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def gmlLoadGmlTransactionToMapEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _stream: ctypes.c_char_p, _streamlength: int, _flag: int, _squarecode: int, _pointcode: int, _linecode: int, _textcode: int) -> ctypes.c_void_p:
        """
        Cоздать объекты из потока транзакций по стандарту OGC WFS-T
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор открытой пользовательской карты
        
        :param _stream: указатель на данные, в котором находится xml файл транзакции ``OGC`` ``WFS``-T
        
        :param _streamlength: длина потока
        
        :param _squarecode: код создаваемых площадей
        
        :param _pointcode: код создаваемых точечных объектов
        
        :param _linecode: код создаваемых линий
        
        :param _textcode: код создаваемых подписей
        
        :param _flag: флаг формирования лога ошибок hselect      - идентификатор условий отбора объектов
        
        :returns: Возвращает идентификатор данных HGMLCLASS, который должен быть освобожден функцией mapFreeGmlClassHandle При ошибке возвращает 0
        """
        return gmlLoadGmlTransactionToMapEx_t (_hmap, _hsite, _stream, _streamlength, _flag, _squarecode, _pointcode, _linecode, _textcode)

    gmlCreateObjectsFromXmlStreamPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlCreateObjectsFromXmlStreamPro', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.HMESSAGE)
    def gmlCreateObjectsFromXmlStreamPro(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _stream: ctypes.c_char_p, _streamlength: int, _protocol: int, _squarecode: int, _pointcode: int, _linecode: int, _textcode: int, _hwnd: maptype.HMESSAGE) -> ctypes.c_void_p:
        """
        Cоздать объекты из потока gml/xml файла
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор открытой пользовательской карты в документе
        
        :param _stream: указатель на данные, в котором находится gml/xml файл или файл gml ``OGC`` ``WFS``
        
        :param _streamlength: длина потока
        
        :param _protocol: признак ведения протокола ошибок
        
        :param _squarecode: код создаваемых площадей
        
        :param _pointcode: код создаваемых точечных объектов
        
        :param _linecode: код создаваемых линий
        
        :param _textcode: код создаваемых подписей
        
        :param _hwnd: идентификатор окна для приема сообщений или ноль, посылаются сообщения ``WM_PROGRESSBAR``
        
        :returns: Возвращает идентификатор данных HGMLCLASS, который должен быть освобожден функцией mapFreeGmlClassHandle При ошибке возвращает 0
        """
        return gmlCreateObjectsFromXmlStreamPro_t (_hmap, _hsite, _stream, _streamlength, _protocol, _squarecode, _pointcode, _linecode, _textcode, _hwnd)

    gmlCreateObjectsFromXmlPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlCreateObjectsFromXmlPro', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.HMESSAGE)
    def gmlCreateObjectsFromXmlPro(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _xmlname: mapsyst.WTEXT, _protocol: int, _squarecode: int, _pointcode: int, _linecode: int, _textcode: int, _hwnd: maptype.HMESSAGE) -> ctypes.c_void_p:
        """
        Cоздать объекты из файла gml/xml
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор открытой пользовательской карты в документе
        
        :param _xmlname: имя входного файла gml/xml или файла gml ``OGC`` ``WFS``
        
        :param _protocol: признак ведения протокола ошибок в формате ``JSON`` (запрашивается gmlGetGmlReport)
        
        :param _squarecode: код создаваемых площадей
        
        :param _pointcode: код создаваемых точечных объектов
        
        :param _linecode: код создаваемых линий
        
        :param _textcode: код создаваемых подписей
        
        :param _hwnd: идентификатор окна для приема сообщений или ноль, посылаются сообщения ``WM_PROGRESSBAR``
        
        :returns: Возвращает идентификатор данных HGMLCLASS, который должен быть освобожден функцией mapFreeGmlClassHandle При ошибке возвращает 0
        """
        return gmlCreateObjectsFromXmlPro_t (_hmap, _hsite, _xmlname.buffer(), _protocol, _squarecode, _pointcode, _linecode, _textcode, _hwnd)

    gmlFreeGmlClassHandle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlFreeGmlClassHandle', ctypes.c_void_p)
    def gmlFreeGmlClassHandle(_hgmlclass: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Освободить идентификатор данных gml/xml
        
        :param _hgmlclass: идентификатор данных, полученный в функциях mapCreateObjFromXml, mapCreateObjFromXmlStream, mapLoadGmlTransactionToMap
        """
        return gmlFreeGmlClassHandle_t (_hgmlclass)

    gmlGetGmlReport_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'gmlGetGmlReport', ctypes.c_void_p, ctypes.c_char_p, ctypes.c_long)
    def gmlGetGmlReport(_hgmlclass: ctypes.c_void_p, _buffer: ctypes.c_char_p, _size: int) -> int:
        """
        Запросить протокол ошибок в формате JSON при загрузке GML функцией gmlCreateObjectsFromXmlPro
        
        :param _hgmlclass: идентификатор данных, полученный в функциях mapCreateObjFromXml
        
        :param _buffer: адрес буфера для чтения протокола
        
        :param _size: размер буфера для чтения протокола Для запроса размера протокола параметр buffer должен быть равен нулю
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return gmlGetGmlReport_t (_hgmlclass, _buffer, _size)

    gmlGetGmlObjectsNumberEx_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_int),'gmlGetGmlObjectsNumberEx', ctypes.c_void_p)
    def gmlGetGmlObjectsNumberEx(_hgmlclass: ctypes.c_void_p) -> ctypes.POINTER(ctypes.c_int):
        """
        Запросить массив уникальных номеров созданных объектов
        
        :param _hgmlclass: идентификатор данных
        
        :returns: Возвращает массив номеров объектов int При ошибке возвращает 0
        :rtype: ctypes.POINTER(ctypes.c_int)
        """
        return gmlGetGmlObjectsNumberEx_t (_hgmlclass)

    gmlGetGmlCreateObjectsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlGetGmlCreateObjectsCount', ctypes.c_void_p)
    def gmlGetGmlCreateObjectsCount(_hgmlclass: ctypes.c_void_p) -> int:
        """
        Запросить количество созданных объектов
        
        :param _hgmlclass: идентификатор данных
        
        :returns: Возвращает количество созданных объектов При ошибке возвращает 0
        :rtype: int
        """
        return gmlGetGmlCreateObjectsCount_t (_hgmlclass)

    gmlGetGmlUpdateObjectsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlGetGmlUpdateObjectsCount', ctypes.c_void_p)
    def gmlGetGmlUpdateObjectsCount(_hgmlclass: ctypes.c_void_p) -> int:
        """
        Запросить количество обновленных объектов при выполнении транзакций
        
        :param _hgmlclass: идентификатор данных
        
        :returns: Возвращает количество обновленных объектов При ошибке возвращает 0
        :rtype: int
        """
        return gmlGetGmlUpdateObjectsCount_t (_hgmlclass)

    gmlGetGmlDeleteObjectsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlGetGmlDeleteObjectsCount', ctypes.c_void_p)
    def gmlGetGmlDeleteObjectsCount(_hgmlclass: ctypes.c_void_p) -> int:
        """
        Запросить количество удаленных объектов при выполнении транзакций
        
        :param _hgmlclass: идентификатор данных
        
        :returns: Возвращает количество удаленных объектов При ошибке возвращает 0
        :rtype: int
        """
        return gmlGetGmlDeleteObjectsCount_t (_hgmlclass)

    gmlGetGmlReplaceObjectsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlGetGmlReplaceObjectsCount', ctypes.c_void_p)
    def gmlGetGmlReplaceObjectsCount(_hgmlclass: ctypes.c_void_p) -> int:
        """
        Запросить количество заменённых объектов при выполнении транзакций
        
        :param _hgmlclass: идентификатор данных
        
        :returns: Возвращает количество заменённых объектов При ошибке возвращает 0
        :rtype: int
        """
        return gmlGetGmlReplaceObjectsCount_t (_hgmlclass)

    gmlGetGmlTransactionObjectsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlGetGmlTransactionObjectsCount', ctypes.c_void_p)
    def gmlGetGmlTransactionObjectsCount(_hgmlclass: ctypes.c_void_p) -> int:
        """
        Запросить количество объектов, присланных в транзакции
        
        :param _hgmlclass: идентификатор данных
        
        :returns: При ошибке возвращает 0, иначе количество присланных объектов
        :rtype: int
        """
        return gmlGetGmlTransactionObjectsCount_t (_hgmlclass)

    gmlGetTransactionNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlGetTransactionNumber', ctypes.c_void_p)
    def gmlGetTransactionNumber(_hgmlclass: ctypes.c_void_p) -> int:
        """
        Запросить номер сформированной транзакции
        
        hJson - идентификатор данных
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return gmlGetTransactionNumber_t (_hgmlclass)

    gmlGetGmlErrorCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlGetGmlErrorCount', ctypes.c_void_p)
    def gmlGetGmlErrorCount(_hgmlclass: ctypes.c_void_p) -> int:
        """
        Запросить количество ошибок при выполнении транзакции
        
        :param _hgmlclass: идентификатор данных
        """
        return gmlGetGmlErrorCount_t (_hgmlclass)

    gmlGetGmlRscName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlGetGmlRscName', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def gmlGetGmlRscName(_xmlname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить имя классификатора данных, по которому был создан gml
        
        :param _xmlname: имя входного файла gml/xml или файла gml ``OGC`` ``WFS``
        
        :param _rscname: возвращаемое значение имени классификатора, по которому создан gml
        
        :param _size: размер переменной rscname
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return gmlGetGmlRscName_t (_xmlname.buffer(), _rscname.buffer(), _size)

    gmlGetGmlBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlGetGmlBorder', maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME))
    def gmlGetGmlBorder(_name: mapsyst.WTEXT, _border: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Запросить габариты набора данных в формате GML и число объектов
        
        :param _name: имя gml-файла
        
        :param _border: габариты набора данных в радианах в системе ``WGS``-``84``
        
        :returns: Если число объектов не может быть определено, то возвращает -1 При ошибке возвращает 0, иначе идентификатор данных
        :rtype: int
        """
        return gmlGetGmlBorder_t (_name.buffer(), _border)

    gmlGetGmlBorderEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlGetGmlBorderEx', maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME), ctypes.POINTER(ctypes.c_long))
    def gmlGetGmlBorderEx(_xmlname: mapsyst.WTEXT, _border: ctypes.POINTER(maptype.DFRAME), _epsgcode: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить габариты объектов файла GML и кода EPSG
        
        :param _xmlname: имя входного файла gml/xml или файла gml ``OGC`` ``WFS``
        
        :param _border: габариты набора данных, заданные в наборе данных
        
        :param _epsgcode: код системы координат, в которой заданы габариты
        
        :returns: Если код системы координат не соответствует габаритам набора данных - возвращает -1 (для CК-42) При ошибке возвращает 0
        :rtype: int
        """
        return gmlGetGmlBorderEx_t (_xmlname.buffer(), _border, _epsgcode)

    gmlUpdateObjectFromGml_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlUpdateObjectFromGml', maptype.HOBJ, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def gmlUpdateObjectFromGml(_hobj: maptype.HOBJ, _filename: mapsyst.WTEXT, _onlypoints: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Обновить описание объекта из файла gml/geojson
        
        :param _hobj: идентификатор обновляемого объекта в памяти
        
        :param _filename: имя файла gml/geojson (полный путь)
        
        :param _onlypoints: признак обновления только координат объекта
        
        :param _error: коды ошибок выполнения программы (описание в  maperr.rh) Объект изменяется без записи на карту
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return gmlUpdateObjectFromGml_t (_hobj, _filename.buffer(), _onlypoints, _error)

    gmlCreateSld_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlCreateSld', maptype.PWCHAR)
    def gmlCreateSld(_path: mapsyst.WTEXT) -> ctypes.c_void_p:
        """
        Сформировать список стилей для рисования объектов по международным стандартам
        
        :param _path: путь к файлу стилей, если path ``= 0`` создает пустой список Международные стандарты -  ``OGC`` ``05``-078r4 v.``1``.``1``.``0`` и ``OGC`` ``02````-070`` v.``1``.``0``.``0`` - ``SLD`` (StyledLayerDescriptor) Каждый созданный список стилей должен быть удален функцией gmlFreeSld, когда он больше не используется
        
        :returns: При ошибке возвращает ноль
        """
        return gmlCreateSld_t (_path.buffer())

    gmlFreeSld_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlFreeSld', ctypes.c_void_p)
    def gmlFreeSld(_hsld: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Освободить список стилей
        
        :param _hsld: список стилей, созданный gmlCreateSld
        """
        return gmlFreeSld_t (_hsld)

    gmlAppendSldToSld_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlAppendSldToSld', ctypes.c_void_p, ctypes.c_void_p)
    def gmlAppendSldToSld(_hsld: ctypes.c_void_p, _addhsld: ctypes.c_void_p) -> int:
        """
        Добавить в список дополнительные SLD стили, которые будут учитываться при создании списка DRAWOBJECT
        
        :param _hsld: список стилей, созданный gmlCreateSld
        
        :param _addhsld: добавляемый список стилей
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return gmlAppendSldToSld_t (_hsld, _addhsld)

    gmlCreatePaintDrawListBySldStream_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlCreatePaintDrawListBySldStream', ctypes.c_char_p, ctypes.c_long, ctypes.c_void_p, maptype.HMAP, maptype.HSITE)
    def gmlCreatePaintDrawListBySldStream(_stream: ctypes.c_char_p, _size: int, _hsld: ctypes.c_void_p, _hmap: maptype.HMAP, _hsite: maptype.HSITE) -> ctypes.c_void_p:
        """
        Создать список (DRAWOBJECT) примитивов для рисования объектов на карте по стандарту OGC SLD
        
        :param _stream: xml файл стилей с фильтрами для объектов, загруженный в буфер
        
        :param _size: размер буфера stream
        
        :param _hsld: список стилей, созданный gmlCreateSld, или ``0``
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор открытой пользовательской карты в документе Каждый созданный список примитивов должен быть удален функцией mapFreePaintDrawList, когда он больше не используется.
        
        :returns: При ошибке возвращает 0
        """
        return gmlCreatePaintDrawListBySldStream_t (_stream, _size, _hsld, _hmap, _hsite)

    gmlCreatePaintDrawListBySld_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'gmlCreatePaintDrawListBySld', maptype.PWCHAR, ctypes.c_void_p, maptype.HMAP, maptype.HSITE)
    def gmlCreatePaintDrawListBySld(_path: mapsyst.WTEXT, _hsld: ctypes.c_void_p, _hmap: maptype.HMAP, _hsite: maptype.HSITE) -> ctypes.c_void_p:
        """
        Создать список (DRAWOBJECT) примитивов для рисования объектов на карте по стандарту OGC SLD
        
        :param _path: путь к файлу стилей с фильтрами для объектов
        
        :param _hsld: список стилей, созданный gmlCreateSld или ``0``
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор открытой пользовательской карты в документе Каждый созданный список примитивов должен быть удален функцией mapFreePaintDrawList, когда он больше не используется.
        
        :returns: При ошибке возвращает 0
        """
        return gmlCreatePaintDrawListBySld_t (_path.buffer(), _hsld, _hmap, _hsite)

    gmlGetDrawObjectByName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gmlGetDrawObjectByName', ctypes.c_void_p, ctypes.c_char_p, maptype.HDRAW)
    def gmlGetDrawObjectByName(_hsld: ctypes.c_void_p, _name: ctypes.c_char_p, _hdraw: maptype.HDRAW) -> int:
        """
        Запросить графическое описание в SLD схеме по имени стиля
        
        :param _hsld: список стилей, созданный gmlCreateSld
        
        :param _name: имя стиля в списке
        
        :param _hdraw: заполняемое описание
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return gmlGetDrawObjectByName_t (_hsld, _name, _hdraw)

    gmlCreateDrawByStyleInSite_t = mapsyst.GetProcAddress(acceslib,maptype.HDRAW,'gmlCreateDrawByStyleInSite', ctypes.c_char_p, ctypes.c_long, maptype.HMAP, maptype.HSITE)
    def gmlCreateDrawByStyleInSite(_stream: ctypes.c_char_p, _size: int, _hmap: maptype.HMAP, _hsite: maptype.HSITE) -> maptype.HDRAW:
        """
        Создать графическое описание по стилю
        
        :param _stream: файл стилей, загруженный в буфер
        
        :param _size: размер файла
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор открытой пользовательской карты в документе
        
        :returns: При ошибке возвращает 0, иначе примитив
        :rtype: maptype.HDRAW
        """
        return gmlCreateDrawByStyleInSite_t (_stream, _size, _hmap, _hsite)

    mapConvertImageToStream_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapConvertImageToStream', ctypes.c_char_p, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_char_p, ctypes.c_long)
    def mapConvertImageToStream(_data: ctypes.c_char_p, _width: int, _height: int, _type: int, _outstream: ctypes.c_char_p, _outsize: int) -> int:
        """
        Сконвертировать изображение в указанный формат и положить результат в буфер
        
        :param _data: входное изображение (``4`` байта на пиксель)
        
        :param _width: ширина изображения
        
        :param _height: высота изображения
        
        :param _type: формат картинки ``IMAGEFILE_TYPE`` (``IMAGEFILE_PNG``, ``IMAGEFILE_JPG`` ...)
        
        :param _outstream: буфер для результирующего сжатого изображения
        
        :param _outsize: размер выходного буфера или ``0`` - для определения необходимого размера
        
        :returns: При ошибке возвращает 0, или размер выходного буфера
        :rtype: int
        """
        return mapConvertImageToStream_t (_data, _width, _height, _type, _outstream, _outsize)

    mapCreateLegendFromXMLEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateLegendFromXMLEx', maptype.HMAP, maptype.HSITE, maptype.HSELECT, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapCreateLegendFromXMLEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT, _xmlname: mapsyst.WTEXT, _imgpath: mapsyst.WTEXT, _frsc: int, _imgsize: int, _transparentcolor: int) -> int:
        """
        Подготовить легенду карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор открытой пользовательской карты
        
        :param _hselect: контекст отбора слоев карты для формирования легенды (необязательный параметр)
        
        :param _xmlname: имя выходного xml-файла
        
        :param _imgpath: путь к изображениям формата png
        
        :param _frsc: флаг отбора объектов (``1`` - по всему классификатору; ``0`` - по hselect)
        
        :param _imgsize: нестандартный размер изображения (сторона квадрата)
        
        :param _transparentcolor: цвет прозрачного фона, если параметр не задан то фон непрозрачный белый
        
        :returns: При ошибке возвращает 0
        :rtype: int
        
        .. note::

           Если равен нулю, то будут созданы только изображения размеров 16x16, 24x24 и 32x32)
           При необходимости создания изображения нестандартного размера (отличного от 16x16, 24x24 и 32x32)
           необходимо указать размер в параметре imgsize
           Максимальный размер изображения 1024x1024
        """
        return mapCreateLegendFromXMLEx_t (_hmap, _hsite, _hselect, _xmlname.buffer(), _imgpath.buffer(), _frsc, _imgsize, _transparentcolor)



def gmlapi_healthcheck():
    return 1
