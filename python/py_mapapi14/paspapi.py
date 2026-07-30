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
    *            Описание функций работы с паспортом карты             *
    *         Стандартные диалоги для приложений НА GIS ToolKit        *
    *                 Пример вызова диалога:                           *
    *                                                                  *
    *   HINSTANCE libInst = ::LoadLibrary("gis64pasp.dll");            *
    *                                                                  *
    *   typedef long int (WINAPI * CREATEPLAN)(char * mapname,         *
    *                                          int size,               *
    *                                    const TASKPARMEX* parm);      *
    *                                                                  *
    *   CREATEPLAN pcreateplan = (CREATEPLAN)                          *
    *                   GetProcAddress(libInst, "paspCreatePlan");     *
    *                                                                  *
    *   long int rezult = (*pcreateplan)(mapname, size, parm);         *
    *                                                                  *
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

#-----------------------------
class REFERENCESYSTEM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("NameSystem",ctypes.c_char*(512)),
                ("Comment",ctypes.c_char*(512)),
                ("Ident",ctypes.c_char*(64)),
                ("CodeEpsg",ctypes.c_int),
                ("Reserve",ctypes.c_int)]
#-----------------------------


#-----------------------------
class REFERENCESYSTEMUN(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("NameSystem",maptype.WCHAR1*(1024)),
                ("Comment",maptype.WCHAR1*(1024)),
                ("Ident",maptype.WCHAR1*(128)),
                ("CodeEpsg",ctypes.c_int),
                ("Reserve",ctypes.c_int)]
#-----------------------------


#-----------------------------
class ORGANIZATION(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Name",ctypes.c_char*(256)),
                ("Phone",ctypes.c_char*(32)),
                ("Facsimile",ctypes.c_char*(32)),
                ("City",ctypes.c_char*(32)),
                ("Adminarea",ctypes.c_char*(32)),
                ("Postalcode",ctypes.c_char*(32)),
                ("Country",ctypes.c_char*(32)),
                ("Email",ctypes.c_char*(64)),
                ("Reserve",ctypes.c_char*(256))]
#-----------------------------


#-----------------------------
class AGENT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Fio",ctypes.c_char*(256)),
                ("NameOrg",ctypes.c_char*(256)),
                ("Phone",ctypes.c_char*(32)),
                ("Facsimile",ctypes.c_char*(32)),
                ("Email",ctypes.c_char*(64))]
#-----------------------------


#-----------------------------
class AGENTEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Fio",maptype.WCHAR1*(512)),
                ("NameOrg",maptype.WCHAR1*(512)),
                ("Position",maptype.WCHAR1*(512)),
                ("Phone",maptype.WCHAR1*(64)),
                ("Facsimile",maptype.WCHAR1*(64)),
                ("Email",maptype.WCHAR1*(128)),
                ("Reserve",maptype.WCHAR1*(512))]
#-----------------------------


#-----------------------------
class ORGANIZATIONEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Name",maptype.WCHAR1*(512)),
                ("Phone",maptype.WCHAR1*(64)),
                ("Facsimile",maptype.WCHAR1*(64)),
                ("City",maptype.WCHAR1*(64)),
                ("Adminarea",maptype.WCHAR1*(64)),
                ("Postalcode",maptype.WCHAR1*(64)),
                ("Country",maptype.WCHAR1*(64)),
                ("Email",maptype.WCHAR1*(128)),
                ("Reserve",maptype.WCHAR1*(512))]
#-----------------------------


#-----------------------------
class RMF_METADATA(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Totalsize",ctypes.c_double),
                ("Ident",maptype.WCHAR1*(128)),
                ("WestLongitude",maptype.WCHAR1*(64)),
                ("EastLongitude",maptype.WCHAR1*(64)),
                ("SouthLatitude",maptype.WCHAR1*(64)),
                ("NorthLatitude",maptype.WCHAR1*(64)),
                ("Scale",maptype.WCHAR1*(64)),
                ("Nomenclature",maptype.WCHAR1*(512)),
                ("Createdate",maptype.WCHAR1*(64)),
                ("Format",maptype.WCHAR1*(32)),
                ("Filename",maptype.WCHAR1*(2048)),
                ("Comment",maptype.WCHAR1*(512)),
                ("Lineage",maptype.WCHAR1*(1024)),
                ("Areadate",maptype.WCHAR1*(64)),
                ("Security",maptype.WCHAR1*(256)),
                ("Datatype",maptype.WCHAR1*(256)),
                ("SatName",maptype.WCHAR1*(128)),
                ("CloudState",maptype.WCHAR1*(64)),
                ("SunAngle",maptype.WCHAR1*(64)),
                ("ScanAngle",maptype.WCHAR1*(64)),
                ("Epsgcode",ctypes.c_int),
                ("MinScale",ctypes.c_int),
                ("MaxScale",ctypes.c_int),
                ("Reserve",maptype.WCHAR1*(456))]
#-----------------------------


#-----------------------------
class PROJECTIONDLG_OPTIONS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("DataType",ctypes.c_int),
                ("Editable",ctypes.c_int),
                ("PassportFlag",ctypes.c_int),
                ("ShowMapList",ctypes.c_int)]
#-----------------------------




try:
    if os.environ['gispaspdll']:
        gispaspname = os.environ['gispaspdll']
except KeyError:
    gispaspname = 'gis64pasp.dll'

try:
    pasplib = mapsyst.LoadLibrary(gispaspname)
except Exception as e:
    print(e)
    pasplib = 0

if pasplib == 0:
    print(gispaspname)
else:
    paspCreateMapUn_t = mapsyst.GetProcAddress(pasplib,ctypes.c_long,'paspCreateMapUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.TASKPARMEX))
    def paspCreateMapUn(_hmap: maptype.HMAP, _mapname: mapsyst.WTEXT, _size: int, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог создания карты
        
        :param _hmap: идентификатор открытой карты или ``0``
        
        :param _mapname: указатель на строку, содержащую имя карты (файла паспорта)
        
        :param _size: длина строки имени карты в байтах
        
        :param _parm: параметры задачи (описание в maptype.h) Help вызывается по топику ``CREATE_MAP``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           После вызова функции значение строки может измениться
           Рекомендуется 1024 символа, то есть 2048 байт в WCHAR
        """
        return paspCreateMapUn_t (_hmap, _mapname.buffer(), _size, _parm)

    paspCreateMapProEx_t = mapsyst.GetProcAddress(pasplib,ctypes.c_long,'paspCreateMapProEx', maptype.HMAP, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def paspCreateMapProEx(_hmap: maptype.HMAP, _mapname: mapsyst.WTEXT, _size: int, _parm: ctypes.POINTER(maptype.TASKPARMEX), _password: mapsyst.WTEXT, _passwsize: int, _rscname: mapsyst.WTEXT, _rscsize: int, _epsgcode: int) -> int:
        """
        Вызвать диалог создания защищенной карты с заданными классификатором и кодом EPSG
        
        :param _hmap: идентификатор открытой карты или ``0``
        
        :param _mapname: указатель на строку, содержащую имя карты (файла паспорта)
        
        :param _size: длина строки имени карты в байтах
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _password: пароль доступа к данным из которого формируется ``256``-битный код для шифрования данных (при утрате данные не восстанавливаются)
        
        :param _passwsize: длина поля пароля в байтах
        
        :param _rscname: имя классификатора, с которым создана карта
        
        :param _rscsize: длина поля имени классификатора в байтах
        
        :param _epsgcode: код ``EPSG`` для начальной инициализации полей диалога или ``0`` при epsgcode ``= -1`` устанавливается тип карты ``"Крупномасштабный план"`` Help вызывается по топику ``CREATE_MAP``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           После вызова функции значение строки может измениться
        """
        return paspCreateMapProEx_t (_hmap, _mapname.buffer(), _size, _parm, _password.buffer(), _passwsize, _rscname.buffer(), _rscsize, _epsgcode)

    paspCreatePlanUn_t = mapsyst.GetProcAddress(pasplib,ctypes.c_long,'paspCreatePlanUn', maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.TASKPARMEX))
    def paspCreatePlanUn(_mapname: mapsyst.WTEXT, _size: int, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог создания крупномасштабного плана
        
        :param _mapname: указатель на строку, содержащую имя карты (файла паспорта)
        
        :param _size: длина строки имени карты в байтах
        
        :param _parm: параметры задачи (описание в maptype.h) Help вызывается по топику ``CREATE_PLAN``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           После вызова функции значение строки может измениться
        """
        return paspCreatePlanUn_t (_mapname.buffer(), _size, _parm)

    paspCreateSite_t = mapsyst.GetProcAddress(pasplib,ctypes.c_long,'paspCreateSite', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def paspCreateSite(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог создания пользовательской карты по открытой карте
        
        :param _hmap: идентификатор открытых данных
        
        :param _parm: параметры задачи (описание в maptype.h) Help вызывается по топику ``CREATE_SITE``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return paspCreateSite_t (_hmap, _parm)

    MapPaspSitDocUn_t = mapsyst.GetProcAddress(pasplib,ctypes.c_long,'MapPaspSitDocUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long, maptype.PWCHAR, ctypes.POINTER(maptype.TASKPARMEX))
    def MapPaspSitDocUn(_hmap: maptype.HMAP, _mapname: mapsyst.WTEXT, _size: int, _path: mapsyst.WTEXT, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог создания пользовательской карты с запросом имени файла
        
        :param _hmap: идентификатор открытых данных
        
        :param _mapname: буфер для записи имени созданной карты
        
        :param _size: длина буфера в байтах
        
        :param _path: директория в которой будет предложено создать файл Пользователь может выбрать другую директорию
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return MapPaspSitDocUn_t (_hmap, _mapname.buffer(), _size, _path.buffer(), _parm)

    paspViewPasp_t = mapsyst.GetProcAddress(pasplib,ctypes.c_long,'paspViewPasp', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.TASKPARMEX))
    def paspViewPasp(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог просмотра и редактирования паспорта
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _parm: параметры задачи (описание в maptype.h) Help вызывается по топику ``PASP_EDID``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return paspViewPasp_t (_hmap, _hsite, _parm)

    paspSetWorkSystemParameters_t = mapsyst.GetProcAddress(pasplib,ctypes.c_long,'paspSetWorkSystemParameters', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def paspSetWorkSystemParameters(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог для изменения параметров местной системы координат
        
        :param _hmap: идентификатор открытых данных
        
        :param _parm: параметры задачи (описание в maptype.h) Устанавливает параметры МСК для документа (``HMAP``), которые затем могут использоваться при пересчетах координат в функциях mapPlaneToWorkSystemPlane, mapWorkSystemPlaneToGeo и подобных Help вызывается по топику ``MCK_PARAM``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return paspSetWorkSystemParameters_t (_hmap, _parm)

    paspSetCurrentProjectionParameters_t = mapsyst.GetProcAddress(pasplib,ctypes.c_long,'paspSetCurrentProjectionParameters', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def paspSetCurrentProjectionParameters(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Отобразить и установить текущие параметры проекции документа для просмотра, печати и расчета координат
        
        :param _hmap: идентификатор открытых данных
        
        :param _parm: параметры задачи (описание в maptype.h) Устанавливать общие параметры проекции можно для документа, поддерживающего пересчет геодезических координат (mapIsGeoSupported() !``= 0``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           После установки общих параметров проекции изображение карты формируется
           в заданной проекции. Векторные карты, имеющие другие параметры
           проекции, трансформируются в процессе отображения.
           Все операции с координатами (mapPlaneToGeo, mapGeoToPlane,
           mapPlaneToGeoWGS84, mapAppendPointPlane, mapInsertPointPlane,
           mapUpdatePointPlane, mapAppendPointGeo и другие) выполняются
           в системе координат документа, определяемой общими параметрами проекции
           При чтении\\записи координат в конкретной карте выполняется пересчет
           из системы координат документа
           Новые параметры устанавливаются функцией mapSetDocProjection(...)(описание в mapapi.h)
           Help вызывается по топику DOCPROJECTION
        """
        return paspSetCurrentProjectionParameters_t (_hmap, _parm)

    paspSetProjectionParametersUn_t = mapsyst.GetProcAddress(pasplib,ctypes.c_long,'paspSetProjectionParametersUn', maptype.HMAP, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, ctypes.c_long)
    def paspSetProjectionParametersUn(_hmap: maptype.HMAP, _mapregisterex: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _spheroidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _parm: ctypes.POINTER(maptype.TASKPARMEX), _title: mapsyst.WTEXT, _iswrite: int) -> int:
        """
        Отобразить и установить параметры проекции
        
        :param _hmap: идентификатор открытых данных (или ``0``)
        
        :param _mapregisterex: параметры проекции (описание в mapcreat.h)
        
        :param _datum: параметры датума (описание в mapcreat.h)
        
        :param _spheroidparam: параметры эллипсоида (описание в mapcreat.h)
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _title: заголовок диалога
        
        :param _iswrite: флаг допустимости редактирования параметров проекции ``0`` - не редактировать, ``1`` - редактировать Исходные значения параметров проекции заданы в mapregisterex, datum, spheroidparam Выход: установленные в карту ``MAPREGISTEREX``, ``DATUMPARAM``, ``ELLIPSOIDPARAM``
        
        :returns: При изменении значений параметров возвращает 1 При отсутствии изменений и при ошибке возвращает ноль
        :rtype: int
        """
        return paspSetProjectionParametersUn_t (_hmap, _mapregisterex, _datum, _spheroidparam, _parm, _title.buffer(), _iswrite)

    paspSetProjectionParametersPro_t = mapsyst.GetProcAddress(pasplib,ctypes.c_long,'paspSetProjectionParametersPro', maptype.HMAP, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(mapcreat.LOCALTRANSFORM), ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, ctypes.c_long)
    def paspSetProjectionParametersPro(_hmap: maptype.HMAP, _mapregisterex: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _spheroidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: ctypes.POINTER(ctypes.c_long), _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM), _parm: ctypes.POINTER(maptype.TASKPARMEX), _title: mapsyst.WTEXT, _iswrite: int) -> int:
        """
        Отобразить и установить параметры проекции с преобразованием координат
        
        :param _hmap: идентификатор открытых данных (или ``0``)
        
        :param _mapregisterex: параметры проекции (описание в mapcreat.h)
        
        :param _datum: параметры датума (описание в mapcreat.h)
        
        :param _spheroidparam: параметры эллипсоида (описание в mapcreat.h)
        
        :param _ttype: тип преобразования координат (описание ``TRANSFORMTYPE`` в mapcreat.h) или ``0``
        
        :param _tparm: параметры преобразования (описание ``LOCALTRANSFORM`` в mapcreat.h)
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _title: заголовок диалога
        
        :param _iswrite: флаг допустимости редактирования параметров проекции ``0`` - не редактировать, ``1`` - редактировать Исходные значения параметров проекции заданы в mapregisterex, datum, spheroidparam Выход: установленные  в карту ``MAPREGISTEREX``, ``DATUMPARAM``, ``ELLIPSOIDPARAM``
        
        :returns: При изменении значений параметров возвращает 1 При отсутствии изменений и при ошибке возвращает ноль
        :rtype: int
        """
        return paspSetProjectionParametersPro_t (_hmap, _mapregisterex, _datum, _spheroidparam, _ttype, _tparm, _parm, _title.buffer(), _iswrite)

    paspSetRmfProjectionParametersUn_t = mapsyst.GetProcAddress(pasplib,ctypes.c_long,'paspSetRmfProjectionParametersUn', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR)
    def paspSetRmfProjectionParametersUn(_hmap: maptype.HMAP, _datatype: int, _chainnumber: int, _parm: ctypes.POINTER(maptype.TASKPARMEX), _title: mapsyst.WTEXT) -> int:
        """
        Установить параметры проекции списка растров, матриц
        
        :param _hmap: идентификатор открытых данных
        
        :param _datatype: тип файла (растры, матрицы) (описание в maptype.h : ``FILE_RSW``, ``FILE_MTW``,...)
        
        :param _chainnumber: номер в цепочке
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _title: заголовок диалога
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return paspSetRmfProjectionParametersUn_t (_hmap, _datatype, _chainnumber, _parm, _title.buffer())

    paspSetProjectionData_t = mapsyst.GetProcAddress(pasplib,ctypes.c_long,'paspSetProjectionData', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR)
    def paspSetProjectionData(_hmap: maptype.HMAP, _datatype: int, _chainnumber: int, _parm: ctypes.POINTER(maptype.TASKPARMEX), _title: mapsyst.WTEXT) -> int:
        """
        Отобразить и установить параметры проекции для растра, матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _datatype: тип файла (растры, матрицы) (описание в maptype.h : ``FILE_RSW``, ``FILE_MTW``,...)
        
        :param _chainnumber: номер в цепочке
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _title: заголовок диалога
        
        :returns: При установке измененных значений параметров возвращает 1 При просмотре или при ошибке возвращает ноль
        :rtype: int
        """
        return paspSetProjectionData_t (_hmap, _datatype, _chainnumber, _parm, _title.buffer())

    paspReadFileXMLPro_t = mapsyst.GetProcAddress(pasplib,ctypes.c_long,'paspReadFileXMLPro', maptype.HMAP, ctypes.POINTER(REFERENCESYSTEMUN), ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(mapcreat.LOCALTRANSFORM), ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_long)
    def paspReadFileXMLPro(_hmap: maptype.HMAP, _referencesystem: ctypes.POINTER(REFERENCESYSTEMUN), _mapregisterex: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _spheroidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: ctypes.POINTER(ctypes.c_long), _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM), _parm: ctypes.POINTER(maptype.TASKPARMEX), _regime: int) -> int:
        """
        Прочитать XML-файл
        
        :param _hmap: идентификатор открытых данных (при создании карты hmap ``= 0``)
        
        :param _referencesystem: параметры системы отсчета
        
        :param _mapregisterex: параметры проекции (описание в mapcreat.h)
        
        :param _datum: параметры датума (описание в mapcreat.h)
        
        :param _spheroidparam: параметры эллипсоида (описание в mapcreat.h)
        
        :param _ttype: тип преобразования координат (описание ``TRANSFORMTYPE`` в mapcreat.h) или ``0``
        
        :param _tparm: параметры преобразования (описание ``LOCALTRANSFORM`` в mapcreat.h)
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _regime: режим работы с паспортом (создание, редактирование) Help вызывается по топику ``PARAMETERSXML``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return paspReadFileXMLPro_t (_hmap, _referencesystem, _mapregisterex, _datum, _spheroidparam, _ttype, _tparm, _parm, _regime)

    paspReadEPSGExUn_t = mapsyst.GetProcAddress(pasplib,ctypes.c_long,'paspReadEPSGExUn', maptype.HMAP, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(ctypes.c_long), maptype.PWCHAR, ctypes.c_long)
    def paspReadEPSGExUn(_hmap: maptype.HMAP, _mapregisterex: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _spheroidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _parm: ctypes.POINTER(maptype.TASKPARMEX), _epsgcode: ctypes.POINTER(ctypes.c_long), _namesystem: mapsyst.WTEXT, _size: int) -> int:
        """
        Прочитать параметры из базы данных EPSG
        
        :param _hmap: идентификатор открытых данных (при создании карты hmap ``= 0``)
        
        :param _mapregisterex: параметры проекции (описание в mapcreat.h)
        
        :param _datum: параметры датума (описание в mapcreat.h)
        
        :param _spheroidparam: параметры эллипсоида (описание в mapcreat.h)
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _size: длина строки Файлы базы данных ``EPSG``.``CSG``, ``EPSG``.``CSP``, ``EPSG``.``CSU`` должны находиться в каталоге приложения
        
        :returns: epsgcode      - код EPSG (в epsgcode возвращается код EPSG) systemname    - строка длиной не менее 64 символов для размещения названия системы координат (идентификатора) При ошибке возвращает ноль
        :rtype: int
        """
        return paspReadEPSGExUn_t (_hmap, _mapregisterex, _datum, _spheroidparam, _parm, _epsgcode, _namesystem.buffer(), _size)

    paspWriteXMLMDUn_t = mapsyst.GetProcAddress(pasplib,ctypes.c_long,'paspWriteXMLMDUn', maptype.PWCHAR, maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_long)
    def paspWriteXMLMDUn(_filename: mapsyst.WTEXT, _hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _regime: int) -> int:
        """
        Создать и редактировать файл метаданных в формате XML
        
        :param _filename: имя файла метаданных (``0``, если формировать для всех листов и всех карт)
        
        :param _hmap: идентификатор открытых данных
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _regime: режимы работы с файлом метаданных ``0`` - создание, ``1`` - редактирование
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return paspWriteXMLMDUn_t (_filename.buffer(), _hmap, _parm, _regime)

    paspEditXMLMDUn_t = mapsyst.GetProcAddress(pasplib,ctypes.c_long,'paspEditXMLMDUn', maptype.PWCHAR, ctypes.POINTER(maptype.TASKPARMEX))
    def paspEditXMLMDUn(_filename: mapsyst.WTEXT, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Просмотреть и редактировать файл метаданных
        
        :param _filename: имя файла метаданных
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return paspEditXMLMDUn_t (_filename.buffer(), _parm)

    paspSaveMetaDataUn_t = mapsyst.GetProcAddress(pasplib,ctypes.c_long,'paspSaveMetaDataUn', maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(ORGANIZATION), ctypes.POINTER(AGENT), maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def paspSaveMetaDataUn(_filename: mapsyst.WTEXT, _mapregisterex: ctypes.POINTER(mapcreat.MAPREGISTEREX), _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _organization: ctypes.POINTER(ORGANIZATION), _agent: ctypes.POINTER(AGENT), _rscname: mapsyst.WTEXT, _comment: mapsyst.WTEXT, _lineage: mapsyst.WTEXT, _security: int, _codeepsg: int) -> int:
        """
        Создать xml файл метаданных для одного листа (без вызова диалога)
        
        :param _filename: имя файла метаданных
        
        :param _mapregisterex: параметры проекции (описание в mapcreat.h)
        
        :param _listreg: параметры листа многолистовой карты (описание в mapcreat.h)
        
        :param _organization: сведения об организации
        
        :param _agent: ведения о сотруднике
        
        :param _rscname: имя файла классификатора (без пути)
        
        :param _comment: комментарий, содержит краткое описание набора данных (до ``256`` символов)
        
        :param _lineage: общие сведения об исходных данных и технологии их обработки (до ``512`` символов)
        
        :param _security: гриф секретности:  ``1`` - открытая информация ``2`` - информация с ограниченным доступом ``3`` - информация для служебного пользования ``4`` - секретная информация ``5`` - совершенно секретная информация
        
        :param _codeepsg: код ``EPSG`` Обязательные для заполнения параметры filename, mapregisterex, listreg
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return paspSaveMetaDataUn_t (_filename.buffer(), _mapregisterex, _listreg, _organization, _agent, _rscname.buffer(), _comment.buffer(), _lineage.buffer(), _security, _codeepsg)

    paspMetaDataMtwRsw_t = mapsyst.GetProcAddress(pasplib,ctypes.c_long,'paspMetaDataMtwRsw', maptype.PWCHAR, maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_long, ctypes.c_long)
    def paspMetaDataMtwRsw(_filename: mapsyst.WTEXT, _hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _datatype: int, _chainnumber: int) -> int:
        """
        Создать и редактировать файл метаданных матриц и растров в формате XML
        
        :param _filename: имя файла метаданных (или ``0``)
        
        :param _hmap: идентификатор открытых данных
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _datatype: тип файла (растры, матрицы) (описание в maptype.h : ``FILE_RSW``, ``FILE_MTW``,...)
        
        :param _chainnumber: номер в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return paspMetaDataMtwRsw_t (_filename.buffer(), _hmap, _parm, _datatype, _chainnumber)

    paspSaveMetaDataRmf_t = mapsyst.GetProcAddress(pasplib,ctypes.c_long,'paspSaveMetaDataRmf', maptype.PWCHAR, ctypes.POINTER(RMF_METADATA), ctypes.POINTER(ORGANIZATIONEX), ctypes.POINTER(AGENTEX), ctypes.c_long)
    def paspSaveMetaDataRmf(_filename: mapsyst.WTEXT, _metadata: ctypes.POINTER(RMF_METADATA), _organization: ctypes.POINTER(ORGANIZATIONEX), _agent: ctypes.POINTER(AGENTEX), _datatype: int) -> int:
        """
        Создать файл метаданных матриц и растров в формате XML (без вызова диалога)
        
        :param _filename: имя файла метаданных
        
        :param _metadata: метаданные матриц и растров
        
        :param _organization: сведения об организации
        
        :param _agent: сведения о сотруднике
        
        :param _datatype: тип файла (растры, матрицы) (описание в maptype.h : ``FILE_RSW``, ``FILE_MTW``,...)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return paspSaveMetaDataRmf_t (_filename.buffer(), _metadata, _organization, _agent, _datatype)

    paspGetMetaDataRmf_t = mapsyst.GetProcAddress(pasplib,ctypes.c_long,'paspGetMetaDataRmf', maptype.PWCHAR, maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(RMF_METADATA), ctypes.POINTER(ORGANIZATIONEX), ctypes.POINTER(AGENTEX), ctypes.c_long)
    def paspGetMetaDataRmf(_filename: mapsyst.WTEXT, _hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _metadata: ctypes.POINTER(RMF_METADATA), _organization: ctypes.POINTER(ORGANIZATIONEX), _agent: ctypes.POINTER(AGENTEX), _datatype: int) -> int:
        """
        Запросить метаданные для матриц и растров
        
        :param _filename: имя файла метаданных
        
        :param _hmap: идентификатор открытых данных
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _metadata: метаданные матриц и растров
        
        :param _organization: сведения об организации
        
        :param _agent: ведения о сотруднике
        
        :param _datatype: тип файла (растры, матрицы) (описание в maptype.h : ``FILE_RSW``, ``FILE_MTW``,...) Структуры ``ORGANIZATIONEX``, ``AGENTEX``  необязательны для заполнения
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return paspGetMetaDataRmf_t (_filename.buffer(), _hmap, _parm, _metadata, _organization, _agent, _datatype)

    paspSaveMetaDataMapFiles_t = mapsyst.GetProcAddress(pasplib,ctypes.c_long,'paspSaveMetaDataMapFiles', maptype.PWCHAR, maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(RMF_METADATA), ctypes.POINTER(ORGANIZATIONEX), ctypes.POINTER(AGENTEX), ctypes.c_long)
    def paspSaveMetaDataMapFiles(_filename: mapsyst.WTEXT, _hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _metadata: ctypes.POINTER(RMF_METADATA), _organization: ctypes.POINTER(ORGANIZATIONEX), _agent: ctypes.POINTER(AGENTEX), _datatype: int) -> int:
        """
        Создать файл метаданных матриц, растров, 3D моделей в формате XML
        
        :param _filename: имя файла метаданных
        
        :param _hmap: идентификатор открытых данных (или ``0``)
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _metadata: метаданные матриц и растров
        
        :param _datatype: тип данных (растры, матрицы: ``FILE_RSW``, ``FILE_MTW`` см. maptype.h )
        
        :param _organization: сведения об организации
        
        :param _agent: ведения о сотруднике
        
        :param _datatype: тип файла (растры, матрицы) (описание в maptype.h : ``FILE_RSW``, ``FILE_MTW``,...) При hmap ``= 0`` структура ``RMF_METADATA`` должна быть заполнена Структуры ``ORGANIZATIONEX``, ``AGENTEX`` могут быть ``0`` (заполнение в диалоге)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return paspSaveMetaDataMapFiles_t (_filename.buffer(), _hmap, _parm, _metadata, _organization, _agent, _datatype)

    pspGetPassword_t = mapsyst.GetProcAddress(pasplib,ctypes.c_long,'pspGetPassword', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def pspGetPassword(_mapname: mapsyst.WTEXT, _password: mapsyst.WTEXT, _size: int) -> int:
        """
        Ввести пароль для хранения закодированных данных SITX
        
        :param _mapname: путь к карте, для которой вводится пароль
        
        :param _password: адрес буфера для сохранения пароля
        
        :param _size: размер буфера в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return pspGetPassword_t (_mapname.buffer(), _password.buffer(), _size)



def paspapi_healthcheck():
    return 1
