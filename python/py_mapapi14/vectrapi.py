#!/usr/bin/env python3

"""
.. code-block:: none

    ********************************************************************
    *                                                                  *
    *              Copyright (c) PANORAMA Group 1991-2026              *
    *                     All Rights Reserved                          *
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



try:
    if os.environ['gisvectrdll']:
        gisvectrname = os.environ['gisvectrdll']
except KeyError:
    gisvectrname = 'gis64vectr.dll'

try:
    vectrlib = mapsyst.LoadLibrary(gisvectrname)
except Exception as e:
    print(e)
    vectrlib = 0

if vectrlib == 0:
    print(gisvectrname)
else:
    MapSort_t = mapsyst.GetProcAddress(vectrlib,ctypes.c_long,'MapSort', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def MapSort(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог сортировки векторных карт
        
        :param _hmap: идентификатор открытых данных
        
        :param _parm: параметры задачи, описание структуры в maptype.h поле Handle должно содержать идентификатор главного окна Вызов справки выполняется из раздела ``MAPSORTS``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return MapSort_t (_hmap, _parm)

    LoadSxf2MapUn_t = mapsyst.GetProcAddress(vectrlib,ctypes.c_long,'LoadSxf2MapUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.TASKPARMEX))
    def LoadSxf2MapUn(_lpszsource: mapsyst.WTEXT, _lpsztarget: mapsyst.WTEXT, _size: int, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог импорта векторных карт из формата SXF или TXF
        
        :param _lpszsource: адрес строки с именем импортируемого файла
        
        :param _lpsztarget: адрес строки для размещения имени создаваемой карты строка может иметь начальное значение
        
        :param _size: длина строки lpsztarget в байтах
        
        :param _parm: параметры задачи, описание структуры в maptype.h поле Handle должно содержать идентификатор главного окна Вызов справки выполняется из раздела ``IMPORTSXF``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return LoadSxf2MapUn_t (_lpszsource.buffer(), _lpsztarget.buffer(), _size, _parm)

    vctLoadDir2MapUn_t = mapsyst.GetProcAddress(vectrlib,ctypes.c_long,'vctLoadDir2MapUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.TASKPARMEX))
    def vctLoadDir2MapUn(_lpszsource: mapsyst.WTEXT, _lpsztarget: mapsyst.WTEXT, _size: int, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог импорта векторных карт из формата DIR
        
        :param _lpszsource: адрес строки с именем импортируемого файла ``DIR``
        
        :param _lpsztarget: адрес строки для размещения имени создаваемой карты строка может иметь начальное значение
        
        :param _size: длина строки lpsztarget в байтах
        
        :param _parm: параметры задачи, описание структуры в maptype.h поле Handle должно содержать идентификатор главного окна Вызов справки выполняется из раздела ``IMPORTSXF``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return vctLoadDir2MapUn_t (_lpszsource.buffer(), _lpsztarget.buffer(), _size, _parm)

    UpdateMapFromSxfUn_t = mapsyst.GetProcAddress(vectrlib,ctypes.c_long,'UpdateMapFromSxfUn', maptype.PWCHAR, ctypes.c_long, maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def UpdateMapFromSxfUn(_lpszsource: mapsyst.WTEXT, _size: int, _hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог обновления векторных карт из формата SXF, TXF или DIR
        
        :param _lpszsource: адрес строки с именем импортируемого файла, используемого для обновления векторной карты
        
        :param _size: длина строки lpszsource для записи имени файла ``SXF``, если в диалоге выбрано другое имя ``SXF``
        
        :param _hmap: идентификатор открытых данных
        
        :param _parm: параметры задачи, описание структуры в maptype.h поле Handle должно содержать идентификатор главного окна Вызов справки выполняется из раздела ``UPDATESXF``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return UpdateMapFromSxfUn_t (_lpszsource.buffer(), _size, _hmap, _parm)

    SaveMap2SxfUn_t = mapsyst.GetProcAddress(vectrlib,ctypes.c_long,'SaveMap2SxfUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.TASKPARMEX))
    def SaveMap2SxfUn(_hmap: maptype.HMAP, _lpsztarget: mapsyst.WTEXT, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Сохранить векторную карту в формат SXF
        
        :param _hmap: идентификатор открытых данных
        
        :param _lpsztarget: имя выходного файла
        
        :param _parm: параметры задачи, описание структуры в maptype.h поле Handle должно содержать идентификатор главного окна Вызов справки выполняется из раздела ``EXPORTSXF``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return SaveMap2SxfUn_t (_hmap, _lpsztarget.buffer(), _parm)

    SaveMap2TxtUn_t = mapsyst.GetProcAddress(vectrlib,ctypes.c_long,'SaveMap2TxtUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.TASKPARMEX))
    def SaveMap2TxtUn(_hmap: maptype.HMAP, _lpsztarget: mapsyst.WTEXT, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Сохранить векторную карту в формат TXF
        
        :param _hmap: идентификатор открытых данных
        
        :param _lpsztarget: имя выходного файла
        
        :param _parm: параметры задачи, описание структуры в maptype.h поле Handle должно содержать идентификатор главного окна Вызов справки выполняется из раздела ``EXPORTSXF``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return SaveMap2TxtUn_t (_hmap, _lpsztarget.buffer(), _parm)

    SaveMap2DirUn_t = mapsyst.GetProcAddress(vectrlib,ctypes.c_long,'SaveMap2DirUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.TASKPARMEX))
    def SaveMap2DirUn(_hmap: maptype.HMAP, _lpsztarget: mapsyst.WTEXT, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Сохранить одну или все векторные карты в формат DIR
        
        :param _hmap: идентификатор открытых данных
        
        :param _lpsztarget: имя файла сохраняемой карты
        
        :param _parm: параметры задачи, описание структуры в maptype.h поле Handle должно содержать идентификатор главного окна Вызов справки выполняется из раздела ``EXPORTSXF``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return SaveMap2DirUn_t (_hmap, _lpsztarget.buffer(), _parm)

    CallImportShp_t = mapsyst.GetProcAddress(vectrlib,ctypes.c_long,'CallImportShp', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def CallImportShp(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог импорта данных Shape
        
        :param _hmap: идентификатор открытых данных
        
        :param _parm: параметры задачи, описание структуры в maptype.h Исходные данные выбираются из диалогового окна открытия файла
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return CallImportShp_t (_hmap, _parm)

    ImportShpSet_t = mapsyst.GetProcAddress(vectrlib,ctypes.c_long,'ImportShpSet', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def ImportShpSet(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог импорта данных Shape с выбором исходной папки
        
        :param _hmap: идентификатор открытых данных
        
        :param _parm: параметры задачи, описание структуры ``TASKPARM`` в maptype.h Исходные данные выбираются из диалогового окна выбора директории
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return ImportShpSet_t (_hmap, _parm)

    CallExportShp_t = mapsyst.GetProcAddress(vectrlib,ctypes.c_long,'CallExportShp', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def CallExportShp(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог экспорта данных в Shape
        
        :param _hmap: идентификатор открытых данных
        
        :param _parm: параметры задачи, описание структуры в maptype.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return CallExportShp_t (_hmap, _parm)

    LoadS57ToMapUn_t = mapsyst.GetProcAddress(vectrlib,ctypes.c_long,'LoadS57ToMapUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.TASKPARMEX))
    def LoadS57ToMapUn(_s57name: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _mapnamesize: int, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог импорта морской карты из формата S57 в формат MAP c классификатором s57navy.rsc
        
        :param _s57name: полное имя файла формата ``S57``
        
        :param _mapname: полное имя создаваемой карты
        
        :param _mapnamesize: размер буфера с именем создаваемой карты в байтах
        
        :param _parm: параметры задачи, описание структуры в maptype.h Для работы программы требуется классификатор s57navy.rsc Для отображения карт нужна библиотека отображения знаков s57navy.iml (s57navy.iml64)
        
        :returns: При ошибке в параметрах возвращает ноль
        :rtype: int
        """
        return LoadS57ToMapUn_t (_s57name.buffer(), _mapname.buffer(), _mapnamesize, _parm)

    LoadS57ToMapForRscUn_t = mapsyst.GetProcAddress(vectrlib,ctypes.c_long,'LoadS57ToMapForRscUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.TASKPARMEX))
    def LoadS57ToMapForRscUn(_s57name: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _mapnamesize: int, _rscname: mapsyst.WTEXT, _rscnamesize: int, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог импорта морской карты из формата S57 в формат MAP с заданным классификатором
        
        :param _s57name: полное имя (путь) файла формата ``S57``
        
        :param _mapname: полное имя файла создаваемой карты
        
        :param _mapnamesize: размер буфера с именем создаваемой карты в байтах
        
        :param _rscname: полное имя файла классификатора (путь к файлу s57navy.rsc)
        
        :param _rscnamesize: размер буфера с именем файла ``RSC`` в байтах
        
        :param _parm: параметры задачи, описание структуры ``TASKPARM`` в maptype.h
        
        :returns: При ошибке в параметрах возвращает ноль
        :rtype: int
        """
        return LoadS57ToMapForRscUn_t (_s57name.buffer(), _mapname.buffer(), _mapnamesize, _rscname.buffer(), _rscnamesize, _parm)

    SaveMap2S57_t = mapsyst.GetProcAddress(vectrlib,ctypes.c_long,'SaveMap2S57', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def SaveMap2S57(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог экспорта морской карты из формата MAP или SIT в формат S57
        
        :param _hmap: идентификатор открытых данных
        
        :param _parm: параметры задачи, описание структуры в maptype.h Для работы программы требуется классификатор s57navy.rsc Для отображения карт нужна библиотека отображения знаков s57navy.iml (s57navy.iml64)
        
        :returns: При ошибке в параметрах возвращает ноль
        :rtype: int
        """
        return SaveMap2S57_t (_hmap, _parm)

    LoadMifToMapUn_t = mapsyst.GetProcAddress(vectrlib,ctypes.c_long,'LoadMifToMapUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.TASKPARMEX))
    def LoadMifToMapUn(_mifname: mapsyst.WTEXT, _mapname: mapsyst.WTEXT, _size: int, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызвать диалог импорта данных из формата MIF/MID
        
        :param _mifname: имя загружаемого файла формата ``MIF``
        
        :param _mapname: имя создаваемой карты
        
        :param _size: длина буфера для размещения имени файла выходной карты
        
        :param _parm: параметры задачи, описание структуры в maptype.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return LoadMifToMapUn_t (_mifname.buffer(), _mapname.buffer(), _size, _parm)



def vectrapi_healthcheck():
    return 1
