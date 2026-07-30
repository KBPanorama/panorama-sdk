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
    *               Описание функций для работы с растрами             *
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
    mapOpenRstUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapOpenRstUn', maptype.PWCHAR, ctypes.c_long)
    def mapOpenRstUn(_rstname: mapsyst.WTEXT, _mode: int) -> maptype.HMAP:
        """
        Открыть растровые данные
        
        :param _rstname: имя файла растровой карты
        
        :param _mode: режим чтения/записи (``GENERIC_READ``, ``GENERIC_WRITE`` или ``0``) ``GENERIC_READ`` - все данные только на чтение
        
        :returns: Возвращает идентификатор открытой растровой карты При ошибке возвращает ноль
        :rtype: maptype.HMAP
        """
        return mapOpenRstUn_t (_rstname.buffer(), _mode)

    mapOpenRstForMapUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapOpenRstForMapUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapOpenRstForMapUn(_hmap: maptype.HMAP, _rstname: mapsyst.WTEXT, _mode: int) -> int:
        """
        Открыть растровые данные в заданном районе работ (добавить в цепочку растров)
        
        :param _hmap: идентификатор открытых данных
        
        :param _rstname: имя файла растровой карты
        
        :param _mode: режим чтения/записи (``GENERIC_READ``, ``GENERIC_WRITE`` или ``0``) ``GENERIC_READ`` - все данные только на чтение
        
        :returns: Возвращает номер файла в цепочке растров При ошибке возвращает ноль
        :rtype: int
        """
        return mapOpenRstForMapUn_t (_hmap, _rstname.buffer(), _mode)

    mapCreateRstUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateRstUn', maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.COLORREF), ctypes.c_long, ctypes.c_double, ctypes.c_double)
    def mapCreateRstUn(_rstname: mapsyst.WTEXT, _width: int, _height: int, _nbits: int, _palette: ctypes.POINTER(maptype.COLORREF), _colorcount: int, _scale: float, _precision: float) -> maptype.HMAP:
        """
        Создать файл растрового изображения
        
        :param _rstname: имя создаваемого файла
        
        :param _width: ширина растрового изображения в элементах
        
        :param _height: высота растрового изображения в элементах
        
        :param _nbits: размер элемента (бит на пиксел)
        
        :param _palette: адрес устанавливаемой палитры
        
        :param _colorcount: число элементов в новой палитре
        
        :param _scale: масштаб
        
        :param _precision: разрешение растра При успешном завершении функция создает файл rstname с заполненным паспортом и палитрой растра
        
        :returns: При ошибке возвращает 0
        :rtype: maptype.HMAP
        """
        return mapCreateRstUn_t (_rstname.buffer(), _width, _height, _nbits, _palette, _colorcount, _scale, _precision)

    mapCreateRstExUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateRstExUn', maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.COLORREF), ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def mapCreateRstExUn(_rstname: mapsyst.WTEXT, _width: int, _height: int, _nbits: int, _palette: ctypes.POINTER(maptype.COLORREF), _colorcount: int, _scale: float, _precisionmet: float, _meterinelementx: float, _meterinelementy: float, _location: ctypes.POINTER(maptype.DOUBLEPOINT), _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> maptype.HMAP:
        """
        Создать файл растровой карты
        
        :param _rstname: полное имя растра
        
        :param _width: ширина изображения в пикселях
        
        :param _height: высота изображения в пикселях
        
        :param _nbits: количество бит на пиксель (``1``,``4``,``8``,``24``)
        
        :param _palette: указатель на палитру растра (справедливо для ``1``,``4``,``8`` бит на пиксель)
        
        :param _colorcount: число элементов в новой палитре
        
        :param _scale: мастаб растра
        
        :param _precisionmet: разрешения растра (точек на метр)
        
        :param _meterinelementx: размер пикселя растра в метрах на местности по оси X (по вертикали)
        
        :param _meterinelementy: размер пикселя растра в метрах на местности по оси Y (по горизонтали) meterinelementx и meterinelementy могут иметь разные значения
        
        :param _location: координаты юго-западного угла растра в метрах, соответствующие СК в mapregister
        
        :param _mapregister: проекции исходного материала Для корректного открытия растров в ``10``-ой и более ранних версиях необходимо выполнить условие: meterinelementx = scale/precisionmet Иначе масштаб и разрешение будут пересчитаны
        
        :returns: При ошибке возвращает 0
        :rtype: maptype.HMAP
        """
        return mapCreateRstExUn_t (_rstname.buffer(), _width, _height, _nbits, _palette, _colorcount, _scale, _precisionmet, _meterinelementx, _meterinelementy, _location, _mapregister)

    mapCreateRasterUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateRasterUn', maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.COLORREF), ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapCreateRasterUn(_rstname: mapsyst.WTEXT, _width: int, _height: int, _nbits: int, _palette: ctypes.POINTER(maptype.COLORREF), _colorcount: int, _meterinelementx: float, _meterinelementy: float, _location: ctypes.POINTER(maptype.DOUBLEPOINT), _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> maptype.HMAP:
        """
        Создать файл растровой карты
        
        :param _rstname: полное имя растра
        
        :param _width: ширина изображения в пикселях
        
        :param _height: высота изображения в пикселях
        
        :param _nbits: количество бит на пиксель (``1``,``4``,``8``,``24``)
        
        :param _palette: указатель на палитру растра (справедливо для ``1``,``4``,``8`` бит на пиксель)
        
        :param _colorcount: число элементов в новой палитре
        
        :param _meterinelementx: размер пикселя растра в метрах на местности по оси X (по вертикали)
        
        :param _meterinelementy: размер пикселя растра в метрах на местности по оси Y (по горизонтали) meterinelementx и meterinelementy могут иметь разные значения
        
        :param _location: координаты юго-западного угла растра в метрах, соответствующие СК в mapregister
        
        :param _mapregister: адрес структуры, содержащей параметры проекции исходного материала datumparam      - адрес структуры, содержащей коэффициенты трансформирования геодезических координат ellipsoidparam  - адрес структуры, содержащей параметры эллипсоида Структуры ``MAPREGISTEREX``, ``DATUMPARAM``, ``ELLIPSOIDPARAM`` описаны в mapcreat.h
        
        :returns: При ошибке возвращает 0
        :rtype: maptype.HMAP
        """
        return mapCreateRasterUn_t (_rstname.buffer(), _width, _height, _nbits, _palette, _colorcount, _meterinelementx, _meterinelementy, _location, _mapregister, _datum, _ellipsoid)

    mapCreateAndAppendRasterUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateAndAppendRasterUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.COLORREF), ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapCreateAndAppendRasterUn(_hmap: maptype.HMAP, _rstname: mapsyst.WTEXT, _width: int, _height: int, _nbits: int, _palette: ctypes.POINTER(maptype.COLORREF), _colorcount: int, _meterinelementx: float, _meterinelementy: float, _location: ctypes.POINTER(maptype.DOUBLEPOINT), _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        """
        Создать файл растрового изображения
        
        :param _hmap: идентификатор открытых данных
        
        :param _rstname: имя создаваемого файла
        
        :param _width: ширина растрового изображения в элементах
        
        :param _height: высота растрового изображения в элементах
        
        :param _nbits: размер элемента (бит на пиксел)
        
        :param _palette: адрес устанавливаемой палитры
        
        :param _colorcount: число элементов в новой палитре scale      - масштаб precision  - разрешение растра (точек на метр)
        
        :param _meterinelementx: размер пикселя растра в метрах на местности по оси X (по вертикали)
        
        :param _meterinelementy: размер пикселя растра в метрах на местности по оси Y (по горизонтали) meterinelementx и meterinelementy могут иметь разные значения
        
        :param _location: координаты юго-западного угла растра в метрах, соответствующие СК в mapregister
        
        :param _mapregister: адрес структуры, содержащей параметры проекции исходного материала
        
        :param _datumparam: адрес структуры, содержащей коэффициенты трансформирования геодезических координат
        
        :param _ellipsoidparam: адрес структуры, содержащей параметры эллипсоида Структуры ``MAPREGISTEREX``, ``DATUMPARAM``, ``ELLIPSOIDPARAM`` описаны в mapcreat.h Для корректного открытия растров в ``10``-ой и более ранних версиях необходимо выполнить условие: meterinelementx = scale/precision Иначе масштаб и разрешение будут пересчитаны При успешном завершении функция создает файл rstname с заполненным паспортом и палитрой растра и добавляет его в цепочку растров открытой векторной карты hmap
        
        :returns: Возвращает номер файла (начиная с 1) в цепочке растров открытой векторной карты При ошибке возвращает ноль
        :rtype: int
        """
        return mapCreateAndAppendRasterUn_t (_hmap, _rstname.buffer(), _width, _height, _nbits, _palette, _colorcount, _meterinelementx, _meterinelementy, _location, _mapregister, _datumparam, _ellipsoidparam)

    mapCreateAndAppendRstUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateAndAppendRstUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.COLORREF), ctypes.c_long, ctypes.c_double, ctypes.c_double, maptype.DOUBLEPOINT)
    def mapCreateAndAppendRstUn(_hmap: maptype.HMAP, _rstname: mapsyst.WTEXT, _width: int, _height: int, _nbits: int, _palette: ctypes.POINTER(maptype.COLORREF), _colorcount: int, _scale: float, _precision: float, _location: maptype.DOUBLEPOINT) -> int:
        """
        Создать файл растрового изображения
        
        :param _rstname: имя создаваемого файла
        
        :param _width: ширина растрового изображения в элементах
        
        :param _height: высота растрового изображения в элементах
        
        :param _nbits: размер элемента (бит на пиксел)
        
        :param _palette: адрес устанавливаемой палитры
        
        :param _colorcount: число элементов в новой палитре
        
        :param _scale: масштаб
        
        :param _precision: разрешение растра
        
        :param _location: привязка юго-западного угла растра в районе в метрах При успешном завершении функция создает файл rstname с заполненным паспортом и палитрой растра и добавляет его в цепочку растров открытой векторной карты hmap
        
        :returns: Возвращает номер файла в цепочке растров открытой векторной карты При ошибке возвращает ноль
        :rtype: int
        """
        return mapCreateAndAppendRstUn_t (_hmap, _rstname.buffer(), _width, _height, _nbits, _palette, _colorcount, _scale, _precision, _location)

    mapRstFileLengthCalculation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapRstFileLengthCalculation', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapRstFileLengthCalculation(_hmap: maptype.HMAP, _width: int, _height: int, _nbits: int) -> float:
        """
        Оценить теорeтическую длину файла растровой карты до ее создания
        
        :param _hmap: идентификатор открытых данных
        
        :param _width: ширина растрового изображения в элементах
        
        :param _height: высота растрового изображения в элементах
        
        :param _nbits: размер элемента (бит на пиксел)
        
        :returns: Возвращает теорeтическую длину файла растровой карты (байт) При ошибке возвращает ноль
        :rtype: float
        """
        return mapRstFileLengthCalculation_t (_hmap, _width, _height, _nbits)

    mapRstFileLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int64,'mapRstFileLength', maptype.HMAP, ctypes.c_long)
    def mapRstFileLength(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить длину в байтах файла растровой карты
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер растрового файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapRstFileLength_t (_hmap, _number)

    mapGetRstNumberByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstNumberByNameUn', maptype.HMAP, maptype.PWCHAR)
    def mapGetRstNumberByNameUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT) -> int:
        """
        Запросить номер растра в цепочке по имени файла
        
        :param _hmap: идентификатор открытых данных
        
        :param _name: имя файла растра В цепочке номера растров начинаются с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstNumberByNameUn_t (_hmap, _name.buffer())

    mapCloseRstForMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCloseRstForMap', maptype.HMAP, ctypes.c_long)
    def mapCloseRstForMap(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Закрыть растровые данные в заданном районе работ
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер растрового файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если number равен 0, закрываются все растровые данные
        """
        return mapCloseRstForMap_t (_hmap, _number)

    mapDeleteRst_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRst', maptype.HMAP, ctypes.c_long)
    def mapDeleteRst(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Закрыть растровые данные и удалить файл
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер растрового файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если number равен 0, закрываются и удаляются все растровые данные
        """
        return mapDeleteRst_t (_hmap, _number)

    mapGetRstNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstNameUn', maptype.HMAP, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetRstNameUn(_hmap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить имя файла растровых данных
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _name: адрес строки для размещения результата
        
        :param _size: размер строки
        
        :returns: При ошибке возвращает пустую строку
        :rtype: int
        """
        return mapGetRstNameUn_t (_hmap, _number, _name.buffer(), _size)

    mapGetRstCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstCount', maptype.HMAP)
    def mapGetRstCount(_hmap: maptype.HMAP) -> int:
        """
        Запросить число открытых файлов растровых данных
        
        :param _hmap: идентификатор открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstCount_t (_hmap)

    mapGetRstIdent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstIdent', maptype.HMAP, ctypes.c_long)
    def mapGetRstIdent(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить идентификатор растровых данных
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstIdent_t (_hmap, _number)

    mapGetRstNumberByIdent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstNumberByIdent', maptype.HMAP, ctypes.c_long)
    def mapGetRstNumberByIdent(_hmap: maptype.HMAP, _ident: int) -> int:
        """
        Запросить номер растра по идентификатору
        
        :param _hmap: идентификатор открытых данных
        
        :param _ident: идентификатор растровых данных
        
        :returns: При ошибке возвращается ноль
        :rtype: int
        """
        return mapGetRstNumberByIdent_t (_hmap, _ident)

    mapGetRstCurrentNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstCurrentNumber', maptype.HMAP)
    def mapGetRstCurrentNumber(_hmap: maptype.HMAP) -> int:
        """
        Запросить текущий номер растра
        
        :param _hmap: идентификатор открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstCurrentNumber_t (_hmap)

    mapSetRstCurrentNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstCurrentNumber', maptype.HMAP, ctypes.c_long)
    def mapSetRstCurrentNumber(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Установить текущий номер растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер растра
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstCurrentNumber_t (_hmap, _number)

    mapIsOpenRst_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsOpenRst', maptype.HMAP, ctypes.c_int)
    def mapIsOpenRst(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить oткрыт ли растр с номером number
        
        :returns: Функция возвращает признак открытия указанного растра в документе (1/0). При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsOpenRst_t (_hmap, _number)

    mapClearRstCache_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapClearRstCache', maptype.HMAP, ctypes.c_long)
    def mapClearRstCache(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Очистить кэш растровых данных, открытых на ГИС Сервере
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер растра, для которого нужно очистить кэш, или -``1`` (все растры)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapClearRstCache_t (_hmap, _number)

    mapGetRstSystemTime_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstSystemTime', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.SYSTEMTIME))
    def mapGetRstSystemTime(_hmap: maptype.HMAP, _number: int, _time: ctypes.POINTER(maptype.SYSTEMTIME)) -> int:
        """
        Запросить время крайнего редактирования растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер растра
        
        :param _time: системное время редактирования
        
        :returns: Возвращает системное время редактирования (создания) по Гринвичу При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstSystemTime_t (_hmap, _number, _time)

    mapGetRstView_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstView', maptype.HMAP, ctypes.c_long)
    def mapGetRstView(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить степень видимости растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Возвращает: ``0`` - не виден, ``1`` - полная видимость, ``2`` - насыщенная ``3`` - полупрозрачная, ``4`` - средняя, ``5`` - прозрачная При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstView_t (_hmap, _number)

    mapSetRstView_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstView', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetRstView(_hmap: maptype.HMAP, _number: int, _view: int) -> int:
        """
        Установить степень видимости растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _view: степень видимости растра: ``0`` - не виден ``1`` - полная видимость ``2`` - насыщенная ``3`` - полупрозрачная ``4`` - средняя ``5`` - прозрачная
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstView_t (_hmap, _number, _view)

    mapGetRstTransparent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstTransparent', maptype.HMAP, ctypes.c_long)
    def mapGetRstTransparent(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить прозрачность растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstTransparent_t (_hmap, _number)

    mapSetRstTransparent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstTransparent', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetRstTransparent(_hmap: maptype.HMAP, _number: int, _transparent: int) -> int:
        """
        Установить прозрачность растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _transparent: прозрачность в процентах от ``0`` до ``100``, где ``0`` - полностью прозрачный, ``100`` - нет прозрачности
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstTransparent_t (_hmap, _number, _transparent)

    mapGetRstSaturation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstSaturation', maptype.HMAP, ctypes.c_long)
    def mapGetRstSaturation(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить насыщенность палитры растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstSaturation_t (_hmap, _number)

    mapSetRstSaturation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstSaturation', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetRstSaturation(_hmap: maptype.HMAP, _number: int, _saturation: int) -> int:
        """
        Установить насыщенность палитры растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _saturation: насыщенность от -``16`` до ``16``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstSaturation_t (_hmap, _number, _saturation)

    mapSetRstGroupView_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstGroupView', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetRstGroupView(_hmap: maptype.HMAP, _userlabel: int, _view: int) -> int:
        """
        Установить степень видимости группы растров
        
        :param _hmap: идентификатор открытых данных
        
        :param _userlabel: пользовательская метка растра: -``1`` - все растры ``RSW_QUALITY`` - растры качеств (создаются mtrBuildRasterUn) ``RSW_VISIBILITY`` - растры зон видимости (создаются mapVisibilityZoneUn)
        
        :param _view: степень видимости: ``0`` - не виден ``1`` - полная ``2`` - насыщенная ``3`` - полупрозрачная ``4`` - средняя ``5`` - прозрачная
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstGroupView_t (_hmap, _userlabel, _view)

    mapGetRstViewOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstViewOrder', maptype.HMAP, ctypes.c_long)
    def mapGetRstViewOrder(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить порядок отображения растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер растрового файла в цепочке
        
        :returns: Возвращает: ``0`` - под картой, ``1`` - над картой При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstViewOrder_t (_hmap, _number)

    mapSetRstViewOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstViewOrder', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetRstViewOrder(_hmap: maptype.HMAP, _number: int, _order: int) -> int:
        """
        Установить порядок отображения растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер растрового файла в цепочке
        
        :param _order: порядок отображения растра: ``0`` - под картой, ``1`` - над картой
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstViewOrder_t (_hmap, _number, _order)

    mapChangeOrderRstShow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapChangeOrderRstShow', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapChangeOrderRstShow(_hmap: maptype.HMAP, _oldnumber: int, _newnumber: int) -> int:
        """
        Поменять очередность отображения растров (rst) в цепочке
        
        :param _hmap: идентификатор открытых данных
        
        :param _oldnumber: номер файла в цепочке
        
        :param _newnumber: устанавливаемый номер файла в цепочке Последний растр в цепочке отображается в последнюю очередь Нумерация растров в цепочке начинается с ``1`` и заканчивается номером mapGetRstCount(..)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapChangeOrderRstShow_t (_hmap, _oldnumber, _newnumber)

    mapChangeOrderRstShowByName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapChangeOrderRstShowByName', maptype.HMAP)
    def mapChangeOrderRstShowByName(_hmap: maptype.HMAP) -> int:
        """
        Поменять очередность отображения растров документа по отсотрированному списку имен файлов
        
        :param _hmap: идентификатор открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapChangeOrderRstShowByName_t (_hmap)

    mapTurnRstViewOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapTurnRstViewOrder', maptype.HMAP)
    def mapTurnRstViewOrder(_hmap: maptype.HMAP) -> int:
        """
        Просмотреть последовательно растры над картой
        
        :param _hmap: идентификатор открытых данных
        
        :returns: Возвращает номер растра отображаемого над картой или ноль При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если все растры отображаются под картой, то первый растр будет отображен над картой
           При следующем вызове второй растр будет отображен над картой, остальные - под картой
           После последнего растра в списке над картой - все растры под картой
           Далее - опять первый растр над картой
           Для получения результата на экране - карту нужно перерисовать
        """
        return mapTurnRstViewOrder_t (_hmap)

    mapGetPaintControlRasterSmoothing_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetPaintControlRasterSmoothing', maptype.HPAINT)
    def mapGetPaintControlRasterSmoothing(_hpaint: maptype.HPAINT) -> int:
        """
        Запросить режим сглаживания растровых данных при увеличении изображения 2 и более раз
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова, создается функцией mapCreatePaintControl()
        
        :returns: Возвращает установленный режим сглаживания
        :rtype: int
        """
        return mapGetPaintControlRasterSmoothing_t (_hpaint)

    mapSetPaintControlRasterSmoothing_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetPaintControlRasterSmoothing', maptype.HPAINT, ctypes.c_long)
    def mapSetPaintControlRasterSmoothing(_hpaint: maptype.HPAINT, _mode: int) -> int:
        """
        Установить режим сглаживания растровых данных при увеличении изображения 2 и более раз
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова, создается функцией mapCreatePaintControl()
        
        :param _mode: режим отображения: ``0`` - быстрое, ``1`` - со сглаживанием
        
        :returns: Возвращает установленный режим сглаживания
        :rtype: int
        """
        return mapSetPaintControlRasterSmoothing_t (_hpaint, _mode)

    mapGetRstColorCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstColorCount', maptype.HMAP, ctypes.c_long)
    def mapGetRstColorCount(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить количество цветов в палитре растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstColorCount_t (_hmap, _number)

    mapGetRstPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstPalette', maptype.HMAP, ctypes.POINTER(maptype.COLORREF), ctypes.c_long, ctypes.c_long)
    def mapGetRstPalette(_hmap: maptype.HMAP, _palette: ctypes.POINTER(maptype.COLORREF), _count: int, _number: int) -> int:
        """
        Запросить описание палитры растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _palette: адрес области для размещения палитры
        
        :param _count: число считываемых элементов палитры
        
        :param _number: номер файла в цепочке Размер области в байтах / ``4``
        
        :returns: если count ``> 256``, то возвращается ноль При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstPalette_t (_hmap, _palette, _count, _number)

    mapSetRstPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstPalette', maptype.HMAP, ctypes.POINTER(maptype.COLORREF), ctypes.c_long, ctypes.c_long)
    def mapSetRstPalette(_hmap: maptype.HMAP, _palette: ctypes.POINTER(maptype.COLORREF), _count: int, _number: int) -> int:
        """
        Установить описание палитры растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _palette: адрес устанавливаемой палитры
        
        :param _count: число элементов в новой палитре, не более ``256``
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если palette равно 0, устанавливается палитра из заголовка
        """
        return mapSetRstPalette_t (_hmap, _palette, _count, _number)

    mapGetRstStandardPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstStandardPalette', maptype.HMAP, ctypes.POINTER(maptype.COLORREF), ctypes.c_long, ctypes.c_long)
    def mapGetRstStandardPalette(_hmap: maptype.HMAP, _palette: ctypes.POINTER(maptype.COLORREF), _count: int, _number: int) -> int:
        """
        Запросить описание эталонной палитры растра без учета яркости и контрасности
        
        :param _hmap: идентификатор открытых данных
        
        :param _palette: адрес области для размещения палитры
        
        :param _count: число считываемых элементов палитры
        
        :param _number: номер файла в цепочке Размер области в байтах / ``4``
        
        :returns: если count ``> 256``, то возвращается ноль При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstStandardPalette_t (_hmap, _palette, _count, _number)

    mapGetRstPaletteFromHeader_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstPaletteFromHeader', maptype.HMAP, ctypes.POINTER(maptype.COLORREF), ctypes.c_long, ctypes.c_long)
    def mapGetRstPaletteFromHeader(_hmap: maptype.HMAP, _palette: ctypes.POINTER(maptype.COLORREF), _count: int, _number: int) -> int:
        """
        Запросить описание палитры из заголовка растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _palette: адрес области для размещения палитры
        
        :param _count: число считываемых элементов палитры
        
        :param _number: номер файла в цепочке Размер области в байтах / ``4``
        
        :returns: если count ``> 256``, то возвращается ноль При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstPaletteFromHeader_t (_hmap, _palette, _count, _number)

    mapSetRstPaletteToHeader_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstPaletteToHeader', maptype.HMAP, ctypes.POINTER(maptype.COLORREF), ctypes.c_long, ctypes.c_long)
    def mapSetRstPaletteToHeader(_hmap: maptype.HMAP, _palette: ctypes.POINTER(maptype.COLORREF), _count: int, _number: int) -> int:
        """
        Скопировать описание палитры в заголовок растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _palette: адрес области для размещения палитры
        
        :param _count: число считываемых элементов палитры
        
        :param _number: номер файла в цепочке размер области в байтах / ``4``
        
        :returns: если count ``> 256``, то возвращается ноль При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstPaletteToHeader_t (_hmap, _palette, _count, _number)

    mapGetRstBright_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBright', maptype.HMAP, ctypes.c_long)
    def mapGetRstBright(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить яркость палитры растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstBright_t (_hmap, _number)

    mapGetRstContrast_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstContrast', maptype.HMAP, ctypes.c_long)
    def mapGetRstContrast(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить контрастность палитры растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstContrast_t (_hmap, _number)

    mapGetRstGamma_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstGamma', maptype.HMAP, ctypes.c_long)
    def mapGetRstGamma(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить параболическую яркость растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstGamma_t (_hmap, _number)

    mapSetRstBright_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstBright', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetRstBright(_hmap: maptype.HMAP, _bright: int, _number: int) -> int:
        """
        Установить яркость палитры растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _bright: яркость
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstBright_t (_hmap, _bright, _number)

    mapSetRstContrast_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstContrast', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetRstContrast(_hmap: maptype.HMAP, _contrast: int, _number: int) -> int:
        """
        Установить контрастность палитры растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _contrast: контраст
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstContrast_t (_hmap, _contrast, _number)

    mapSetRstGamma_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstGamma', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetRstGamma(_hmap: maptype.HMAP, _gamma: int, _number: int) -> int:
        """
        Установить параболическую яркость растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _gamma: параболическая яркость
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstGamma_t (_hmap, _gamma, _number)

    mapRestoreRstPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRestoreRstPalette', maptype.HMAP, ctypes.c_long)
    def mapRestoreRstPalette(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Обновить активную палитру с нулевой яркостью и контрастностью
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapRestoreRstPalette_t (_hmap, _number)

    mapCheckInversionRst_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckInversionRst', maptype.HMAP, ctypes.c_long)
    def mapCheckInversionRst(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить значение инверсии растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Если изображение растра позитивное - возвращает ноль Если изображение растра негативное - возвращает 1 При ошибке возвращает -1
        :rtype: int
        """
        return mapCheckInversionRst_t (_hmap, _number)

    mapInvertRst_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapInvertRst', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapInvertRst(_hmap: maptype.HMAP, _number: int, _value: int) -> int:
        """
        Инвертировать растровую карту
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке value: ``0`` - установить изображение растра позитивным ``1`` - установить изображение растра негативным
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapInvertRst_t (_hmap, _number, _value)

    mapCheckVisibilityColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckVisibilityColor', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapCheckVisibilityColor(_hmap: maptype.HMAP, _number: int, _index: int) -> int:
        """
        Запросить видимость цвета для 16- и 256-цветных растров
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _index: индекс цвета в палитре растра, начиная с ``0``
        
        :returns: Возвращает: ``1`` - цвет с данным индексом отображается ``0`` - цвет с данным индексом не отображается При ошибке возвращает -1
        :rtype: int
        """
        return mapCheckVisibilityColor_t (_hmap, _number, _index)

    mapSetVisibilityColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetVisibilityColor', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSetVisibilityColor(_hmap: maptype.HMAP, _number: int, _index: int, _value: int) -> int:
        """
        Установить видимость цвета для 16- и 256-цветных растров
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _index: индекс цвета в палитре растра, начиная с ``0`` value: ``1`` - включить отображение цвета с данным индексом ``0`` - отключить отображение цвета с данным индексом Сохранение видимости цветов в ini-файле, не заносится в заголовок файла растра
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetVisibilityColor_t (_hmap, _number, _index, _value)

    mapSetVisibilityColorInRstFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetVisibilityColorInRstFile', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSetVisibilityColorInRstFile(_hmap: maptype.HMAP, _number: int, _index: int, _value: int) -> int:
        """
        Установить видимость цвета для 16- и 256-цветных растров
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _index: индекс цвета в палитре растра,начиная с ``0`` value: ``1`` - включить отображение цвета с данным индексом ``0`` - отключить отображение цвета с данным индексом Сохранение видимости цветов в заголовке файла растра, а также в ini-файле
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetVisibilityColorInRstFile_t (_hmap, _number, _index, _value)

    mapSetRstTransparentColor_t = mapsyst.GetProcAddress(acceslib,maptype.COLORREF,'mapSetRstTransparentColor', maptype.HMAP, ctypes.c_long, maptype.COLORREF)
    def mapSetRstTransparentColor(_hmap: maptype.HMAP, _number: int, _color: maptype.COLORREF) -> maptype.COLORREF:
        """
        Установить прозрачный цвет растра для 16-, 24-, 32-битных растров
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _color: значение прозрачного цвета в формате ``RGB`` - от ``0`` до ``0x00FFFFFF`` При установке ``IMGC_TRANSPARENT`` (``0xFFFFFFFF``) прозрачный цвет не используется
        
        :returns: При ошибке возвращает IMGC_TRANSPARENT
        :rtype: maptype.COLORREF
        """
        return mapSetRstTransparentColor_t (_hmap, _number, _color)

    mapGetRstTransparentColor_t = mapsyst.GetProcAddress(acceslib,maptype.COLORREF,'mapGetRstTransparentColor', maptype.HMAP, ctypes.c_long)
    def mapGetRstTransparentColor(_hmap: maptype.HMAP, _number: int) -> maptype.COLORREF:
        """
        Запросить прозрачный цвет растра для 16-, 24-, 32-битных растров
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Возвращает цвет в формате ``RGB`` - от 0 до ``0x00FFFFFF`` При возврате IMGC_TRANSPARENT (``0xFFFFFFFF``) прозрачный цвет не используется При ошибке возвращает IMGC_TRANSPARENT
        :rtype: maptype.COLORREF
        """
        return mapGetRstTransparentColor_t (_hmap, _number)

    mapGetRstMaskType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstMaskType', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapGetRstMaskType(_hmap: maptype.HMAP, _number: int, _masktype: ctypes.POINTER(ctypes.c_long), _maskstep: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить тип и шаг маски растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _masktype: тип маски (``0`` - маска отсутствует): ``HATCH_HORIZ``     ``1``  Штриховка горизонтальная ``HATCH_VERT``      ``2``  Штриховка вертикальная ``HATCH_GRID``      ``3``  Решетка прямая ``HATCH_QUAD``      ``4``  Квадратики ``HATCH_DIAG``      ``5``  Штриховка диагоналями ``HATCH_DIAGTURN``  ``6``  Штриховка обратными диагоналями ``HATCH_DIAGGRID``  ``7``  Решетка диагональная ``HATCH_QUADTURN``  ``8``  Квадратики повернутые
        
        :param _maskstep: шаг маски
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstMaskType_t (_hmap, _number, _masktype, _maskstep)

    mapSetRstMaskType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstMaskType', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSetRstMaskType(_hmap: maptype.HMAP, _number: int, _masktype: int, _maskstep: int) -> int:
        """
        Установить тип и шаг маски растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _masktype: тип маски(``0`` - маска отсутствует)
        
        :param _maskstep: шаг маски
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstMaskType_t (_hmap, _number, _masktype, _maskstep)

    mapSetRstParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstParameters', maptype.HMAP, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    def mapSetRstParameters(_hmap: maptype.HMAP, _number: int, _scale: float, _precision: float, _meterinelementx: float, _meterinelementy: float) -> int:
        """
        Установить взаимосвязанные параметры растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _scale: знаменатель масштаба
        
        :param _precision: разрешение (точек на метр)
        
        :param _meterinelementx: количество метров на элемент по оси X
        
        :param _meterinelementy: количество метров на элемент по оси Y meterinelementx и meterinelementy могут отличаться Для правильного отображения растров в ``10``-ой и более ранних версиях необходимо: meterinelementx = scale / precision
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если условие не выполняется, то meterinelementx и meterinelementy игнорируются и расчитываются по формуле
        """
        return mapSetRstParameters_t (_hmap, _number, _scale, _precision, _meterinelementx, _meterinelementy)

    mapSetRstScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstScale', maptype.HMAP, ctypes.c_long, ctypes.c_double)
    def mapSetRstScale(_hmap: maptype.HMAP, _number: int, _scale: float) -> int:
        """
        Установить масштаб растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _scale: знаменатель масштаба
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstScale_t (_hmap, _number, _scale)

    mapGetRstScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstScale', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def mapGetRstScale(_hmap: maptype.HMAP, _number: int, _scale: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить масштаб растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _scale: указатель переменной, куда вносится значение масштаба
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstScale_t (_hmap, _number, _scale)

    mapGetRstRangeScaleVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstRangeScaleVisible', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapGetRstRangeScaleVisible(_hmap: maptype.HMAP, _number: int, _bottomscale: ctypes.POINTER(ctypes.c_long), _topscale: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить значения масштаба нижней и верхней границ видимости растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _bottomscale: адрес для записи знаменателя масштаба нижней границы видимости растра
        
        :param _topscale: адрес для записи знаменателя масштаба верхней границы видимости растра
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstRangeScaleVisible_t (_hmap, _number, _bottomscale, _topscale)

    mapSetRstRangeScaleVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstRangeScaleVisible', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSetRstRangeScaleVisible(_hmap: maptype.HMAP, _number: int, _bottomscale: int, _topscale: int) -> int:
        """
        Установить значения масштаба нижней и верхней границ видимости растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _bottomscale: знаменатель масштаба нижней границы видимости растра
        
        :param _topscale: знаменатель масштаба верхней границы видимости растра
        
        :returns: bottomscale <= topscale, иначе возвращает 0 При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstRangeScaleVisible_t (_hmap, _number, _bottomscale, _topscale)

    mapSetRstPrecision_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstPrecision', maptype.HMAP, ctypes.c_long, ctypes.c_double)
    def mapSetRstPrecision(_hmap: maptype.HMAP, _number: int, _precision: float) -> int:
        """
        Установить разрешение растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _precision: разрешение растра, полученное при сканировании (точек на метр)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstPrecision_t (_hmap, _number, _precision)

    mapGetRstPrecision_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstPrecision', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def mapGetRstPrecision(_hmap: maptype.HMAP, _number: int, _precision: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить разрешение растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _precision: разрешение растра (точек на метр)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstPrecision_t (_hmap, _number, _precision)

    mapSetRstBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstBorder', maptype.HMAP, ctypes.c_long, maptype.HOBJ)
    def mapSetRstBorder(_hmap: maptype.HMAP, _number: int, _hobj: maptype.HOBJ) -> int:
        """
        Установить рамку растра по метрике замкнутого объекта
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _hobj: замкнутый объект карты Замкнутый объект должен иметь не менее ``4``-х точек
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           После выполнения функции отображение растра ограничится заданной областью
        """
        return mapSetRstBorder_t (_hmap, _number, _hobj)

    mapSetRstBorderEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstBorderEx', maptype.HMAP, ctypes.c_long, maptype.HOBJ, ctypes.c_long)
    def mapSetRstBorderEx(_hmap: maptype.HMAP, _number: int, _hobj: maptype.HOBJ, _flagsubject: int) -> int:
        """
        Установить рамку растра по метрике замкнутого объекта
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _hobj: замкнутый объект карты
        
        :param _flagsubject: флаг использования подобъектов объекта при установке рамки растра (``0``/``1``): ``0`` - в качестве рамки растра устанавливается контур объекта ``1`` - в качестве рамки растра устанавливается контур объекта с подобъектами Замкнутый объект должен иметь не менее ``4``-х точек
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           После выполнения функции отображение растра ограничится заданной областью
        """
        return mapSetRstBorderEx_t (_hmap, _number, _hobj, _flagsubject)

    mapGetRstBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBorder', maptype.HMAP, ctypes.c_long, maptype.HOBJ)
    def mapGetRstBorder(_hmap: maptype.HMAP, _number: int, _hobj: maptype.HOBJ) -> int:
        """
        Запросить объект рамки растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _hobj: идентификатор объекта рамки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstBorder_t (_hmap, _number, _hobj)

    mapDeleteRstBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRstBorder', maptype.HMAP, ctypes.c_long)
    def mapDeleteRstBorder(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Удалить рамку растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           После выполнения функции отображение растра будет полным
        """
        return mapDeleteRstBorder_t (_hmap, _number)

    mapDeleteRstBlocks_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRstBlocks', maptype.HMAP, ctypes.c_long)
    def mapDeleteRstBlocks(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Удалить блоки данных растра - очистка растра зон видимости и других
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapDeleteRstBlocks_t (_hmap, _number)

    mapGetRstMask_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstMask', maptype.HMAP, ctypes.c_long)
    def mapGetRstMask(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Определить существование маски растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstMask_t (_hmap, _number)

    mapGetShowRstByMask_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetShowRstByMask', maptype.HMAP, ctypes.c_long)
    def mapGetShowRstByMask(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Определить способ отображения растра относительно маски
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Возвращает: ``1`` - при отображении растра по маске ``0`` - при отображении растра без учета маски При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetShowRstByMask_t (_hmap, _number)

    mapSetShowRstByMask_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetShowRstByMask', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetShowRstByMask(_hmap: maptype.HMAP, _number: int, _value: int) -> int:
        """
        Установить отображение растра по маске
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке value  ``= 1`` - отобразить растр по маске ``= 0`` - отобразить растр без учета маски
        """
        return mapSetShowRstByMask_t (_hmap, _number, _value)

    mapCheckExistenceRstBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckExistenceRstBorder', maptype.HMAP, ctypes.c_long)
    def mapCheckExistenceRstBorder(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Определить существование рамки растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCheckExistenceRstBorder_t (_hmap, _number)

    mapShowRstByBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapShowRstByBorder', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapShowRstByBorder(_hmap: maptype.HMAP, _number: int, _value: int) -> int:
        """
        Установить отображение растра по рамке
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке value  ``= 1`` - отобразить растр по рамке ``= 0`` - отобразить растр без учета рамки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapShowRstByBorder_t (_hmap, _number, _value)

    mapCheckShowRstByBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckShowRstByBorder', maptype.HMAP, ctypes.c_long)
    def mapCheckShowRstByBorder(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Определить способ отображения растра относительно рамки
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Возвращает: ``1`` - при отображении растра по рамке ``0`` - при отображении растра без учета рамки При ошибке возвращает -1
        :rtype: int
        """
        return mapCheckShowRstByBorder_t (_hmap, _number)

    mapGetImmediatePointOfRstBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetImmediatePointOfRstBorder', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetImmediatePointOfRstBorder(_hmap: maptype.HMAP, _number: int, _pointin: ctypes.POINTER(maptype.DOUBLEPOINT), _pointout: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Определить координаты точки рамки ближайшей к pointin
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _pointin: координаты точки в метрах
        
        :param _pointout: адрес для записи координат найденной точки в метрах Найденная точка входит в прямоугольник габариты растра и имеет наименьшее удаление от точки pointin
        
        :returns: При ошибке или отсутствии рамки возвращает ноль
        :rtype: int
        """
        return mapGetImmediatePointOfRstBorder_t (_hmap, _number, _pointin, _pointout)

    mapIsRstGeoSupported_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsRstGeoSupported', maptype.HMAP, ctypes.c_long)
    def mapIsRstGeoSupported(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить поддерживается ли пересчет к геодезическим координатам из плоских прямоугольных и обратно
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер растра
        
        :returns: Если нет - возвращает ноль
        :rtype: int
        """
        return mapIsRstGeoSupported_t (_hmap, _number)

    mapGetRstProjectionDataPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstProjectionDataPro', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapGetRstProjectionDataPro(_hmap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: ctypes.POINTER(ctypes.c_long), _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        """
        Запросить данные о проекции растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _mapregister: адрес структуры, в которой будут размещены параметры проекции исходного материала
        
        :param _datumparam: адрес структуры, в которой будут размещены коэффициенты трансформирования геодезических координат
        
        :param _ellipsoidparam: адрес структуры, в которой будут размещены параметры эллипсоида
        
        :param _ttype: тип локального преобразования координат (``TRANSFORMTYPE`` в mapcreat.h) или ``0``
        
        :param _tparm: параметры локального преобразования координат Структуры ``MAPREGISTEREX``, ``DATUMPARAM``, ``ELLIPSOIDPARAM``, ``LOCALTRANSFORM`` описаны в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstProjectionDataPro_t (_hmap, _number, _mapregister, _datumparam, _ellipsoidparam, _ttype, _tparm)

    mapGetRstProjectionDataByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstProjectionDataByNameUn', maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def mapGetRstProjectionDataByNameUn(_name: mapsyst.WTEXT, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> int:
        """
        Запросить данные о проекции растра по имени файла
        
        :param _name: имя файла растра
        
        :param _mapregister: адрес структуры, в которой будут размещены данные о проекции
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstProjectionDataByNameUn_t (_name.buffer(), _mapregister)

    mapSetRstProjectionDataPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstProjectionDataPro', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_long, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapSetRstProjectionDataPro(_hmap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        """
        Установить данные о проекции растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _mapregister: адрес структуры, содержащей параметры проекции исходного материала
        
        :param _datumparam: адрес структуры, содержащей коэффициенты трансформирования геодезических координат
        
        :param _ellipsoidparam: адрес структуры, содержащей параметры эллипсоида
        
        :param _ttype: тип локального преобразования координат (``TRANSFORMTYPE`` в mapcreat.h) или ``0``
        
        :param _tparm: параметры локального преобразования координат Структуры ``MAPREGISTEREX``, ``DATUMPARAM``, ``ELLIPSOIDPARAM``, ``LOCALTRANSFORM`` описаны в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstProjectionDataPro_t (_hmap, _number, _mapregister, _datumparam, _ellipsoidparam, _ttype, _tparm)

    mapSetRstProjectionDataFromDoc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstProjectionDataFromDoc', maptype.HMAP, ctypes.c_long)
    def mapSetRstProjectionDataFromDoc(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Установить параметры проекции документа в растр
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstProjectionDataFromDoc_t (_hmap, _number)

    mapGetRstEllipsoidParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstEllipsoidParam', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapGetRstEllipsoidParam(_hmap: maptype.HMAP, _number: int, _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        """
        Запросить параметры эллипсоида растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла растра в цепочке
        
        :param _ellipsoidparam: адрес структуры, в которой будут размещены параметры эллипсоида Структурa ``ELLIPSOIDPARAM`` описанa в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstEllipsoidParam_t (_hmap, _number, _ellipsoidparam)

    mapSetRstEllipsoidParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstEllipsoidParam', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapSetRstEllipsoidParam(_hmap: maptype.HMAP, _number: int, _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        """
        Установить параметры эллипсоида растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла растра в цепочке.
        
        :param _ellipsoidparam: адрес структуры, содержащей параметры эллипсоида Структурa ``ELLIPSOIDPARAM`` описанa в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstEllipsoidParam_t (_hmap, _number, _ellipsoidparam)

    mapGetRstDatumParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstDatumParam', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapGetRstDatumParam(_hmap: maptype.HMAP, _number: int, _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        """
        Запросить коэффициенты трансформирования геодезических координат растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла растра в цепочке
        
        :param _datumparam: адрес структуры, в которой будут размещены коэффициенты трансформирования геодезических координат Структурa ``DATUMPARAM`` описанa в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstDatumParam_t (_hmap, _number, _datumparam)

    mapSetRstDatumParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstDatumParam', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapSetRstDatumParam(_hmap: maptype.HMAP, _number: int, _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        """
        Установить коэффициенты трансформирования геодезических координат растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла растра в цепочке.
        
        :param _datumparam: адрес структуры, содержащей коэффициенты трансформирования геодезических координат Структурa ``DATUMPARAM`` описанa в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstDatumParam_t (_hmap, _number, _datumparam)

    mapGetRstFrameMeters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstFrameMeters', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.c_long)
    def mapGetRstFrameMeters(_hmap: maptype.HMAP, _frame: ctypes.POINTER(maptype.DFRAME), _number: int) -> int:
        """
        Запросить габариты растра в метрах в районе работ
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _frame: возвращаемые габариты растра
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstFrameMeters_t (_hmap, _frame, _number)

    mapGetRstFrameDocMeters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstFrameDocMeters', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.c_long)
    def mapGetRstFrameDocMeters(_hmap: maptype.HMAP, _frame: ctypes.POINTER(maptype.DFRAME), _number: int) -> int:
        """
        Запросить габариты растра в метрах в текущей проекции
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _frame: возвращаемые габариты растра
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstFrameDocMeters_t (_hmap, _frame, _number)

    mapGetActualRstFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetActualRstFrame', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.c_long)
    def mapGetActualRstFrame(_hmap: maptype.HMAP, _frame: ctypes.POINTER(maptype.DFRAME), _number: int) -> int:
        """
        Запросить фактические габариты отображаемого растра в метрах в районе работ
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _frame: возвращаемые габариты растра При отображение растра по рамке возвращаются габариты рамки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetActualRstFrame_t (_hmap, _frame, _number)

    mapGetActualRstFrameDoc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetActualRstFrameDoc', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.c_long)
    def mapGetActualRstFrameDoc(_hmap: maptype.HMAP, _frame: ctypes.POINTER(maptype.DFRAME), _number: int) -> int:
        """
        Запросить фактические габариты отображаемого растра в метрах в текущей проекции
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _frame: возвращаемые габариты растра При отображение растра по рамке возвращаются габариты рамки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetActualRstFrameDoc_t (_hmap, _frame, _number)

    mapSetRstLocation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstLocation', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSetRstLocation(_hmap: maptype.HMAP, _number: int, _location: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Установить привязку растра в районе работ
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _location: координаты юго-западного угла растра в метрах документа
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstLocation_t (_hmap, _number, _location)

    mapGetRstLocation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstLocation', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetRstLocation(_hmap: maptype.HMAP, _number: int, _location: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Запросить привязку растра в районе работ
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _location: координаты юго-западного угла растра в метрах документа
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstLocation_t (_hmap, _number, _location)

    mapSetRstLocationEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstLocationEx', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSetRstLocationEx(_hmap: maptype.HMAP, _number: int, _source: ctypes.POINTER(maptype.DOUBLEPOINT), _target: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Установить привязку растра по двум точкам
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _source: исходная точка на растре по которой устанавливаются координаты в метрах документа
        
        :param _target: новые координаты выбранной точки в метрах документа
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstLocationEx_t (_hmap, _number, _source, _target)

    mapCheckExistenceRstLocation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckExistenceRstLocation', maptype.HMAP, ctypes.c_long)
    def mapCheckExistenceRstLocation(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить флаг существования привязки растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCheckExistenceRstLocation_t (_hmap, _number)

    mapGetRstCopyFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstCopyFlag', maptype.HMAP, ctypes.c_long)
    def mapGetRstCopyFlag(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить - может ли растр копироваться или экспортироваться
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Если нет - возвращает ноль
        :rtype: int
        """
        return mapGetRstCopyFlag_t (_hmap, _number)

    mapGetRstPrintFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstPrintFlag', maptype.HMAP, ctypes.c_long)
    def mapGetRstPrintFlag(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить - может ли растр выводиться на печать
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке Для данных, открытых на ГИС Сервере, может устанавливаться запрет вывода изображения на печать
        
        :returns: Если нет - возвращает ноль
        :rtype: int
        """
        return mapGetRstPrintFlag_t (_hmap, _number)

    mapGetRstHidePassportFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstHidePassportFlag', maptype.HMAP, ctypes.c_long)
    def mapGetRstHidePassportFlag(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить - можно ли показывать параметры паспорта
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке Для данных, открытых на ГИС Сервере, может устанавливаться запрет отображения параметров системы координат
        
        :returns: Если нет - возвращает ноль
        :rtype: int
        """
        return mapGetRstHidePassportFlag_t (_hmap, _number)

    mapGetRstHideCacheFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstHideCacheFlag', maptype.HMAP, ctypes.c_long)
    def mapGetRstHideCacheFlag(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить признак запрета кэширования данных с ГИС Сервера
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstHideCacheFlag_t (_hmap, _number)

    mapSetRstHideCacheFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstHideCacheFlag', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetRstHideCacheFlag(_hmap: maptype.HMAP, _number: int, _hideflag: int) -> int:
        """
        Установить признак запрета кэширования данных с ГИС Сервера
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _hideflag: признак запрета кэширования данных с ГИС Сервера
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstHideCacheFlag_t (_hmap, _number, _hideflag)

    mapIsRstFromServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsRstFromServer', maptype.HMAP, ctypes.c_long)
    def mapIsRstFromServer(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить открыт ли растр на сервере или локально
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Если растр открыт на сервере возвращает ненулевое значение
        :rtype: int
        """
        return mapIsRstFromServer_t (_hmap, _number)

    mapGetRstMeterInElementX_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstMeterInElementX', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def mapGetRstMeterInElementX(_hmap: maptype.HMAP, _number: int, _metinelemx: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить размер элемента растра в метрах по оси X
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _metinelemx: размер элемента растра в метрах на местности по оси X
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstMeterInElementX_t (_hmap, _number, _metinelemx)

    mapGetRstMeterInElementY_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstMeterInElementY', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def mapGetRstMeterInElementY(_hmap: maptype.HMAP, _number: int, _metinelemy: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить размер элемента растра в метрах по оси Y
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _metinelemy: размер элемента растра в метрах на местности по оси Y
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstMeterInElementY_t (_hmap, _number, _metinelemy)

    mapGetSizeRstElemXInPix_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSizeRstElemXInPix', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def mapGetSizeRstElemXInPix(_hmap: maptype.HMAP, _number: int, _eleminpix: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить размер элемента растра в пикселах экрана по оси X
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _eleminpix: размер точки экрана в элементах растра
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSizeRstElemXInPix_t (_hmap, _number, _eleminpix)

    mapGetSizeRstElemYInPix_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSizeRstElemYInPix', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def mapGetSizeRstElemYInPix(_hmap: maptype.HMAP, _number: int, _eleminpix: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить размер элемента растра в пикселах экрана по оси Y
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _eleminpix: размер точки экрана в элементах растра
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSizeRstElemYInPix_t (_hmap, _number, _eleminpix)

    mapGetRstWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstWidth', maptype.HMAP, ctypes.c_long)
    def mapGetRstWidth(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить ширину растра в элементах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstWidth_t (_hmap, _number)

    mapGetRstHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstHeight', maptype.HMAP, ctypes.c_long)
    def mapGetRstHeight(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить высоту растра в элементах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstHeight_t (_hmap, _number)

    mapGetRstLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_ulong,'mapGetRstLength', maptype.HMAP, ctypes.c_long)
    def mapGetRstLength(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить объем растра в байтах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstLength_t (_hmap, _number)

    mapGetRstElementSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstElementSize', maptype.HMAP, ctypes.c_long)
    def mapGetRstElementSize(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить размер элемента растра в битах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstElementSize_t (_hmap, _number)

    mapGetRstEdit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstEdit', maptype.HMAP, ctypes.c_long)
    def mapGetRstEdit(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить флаг редактируемости растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstEdit_t (_hmap, _number)

    mapGetRstCompressNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstCompressNumber', maptype.HMAP, ctypes.c_long)
    def mapGetRstCompressNumber(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить номер алгоритма сжатия растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Возвращает: ``0`` - растр не сжат, ``1`` - LZW, ``2`` - JPEG При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstCompressNumber_t (_hmap, _number)

    mapSetRstCompressNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstCompressNumber', maptype.HMAP, ctypes.c_long, ctypes.c_int)
    def mapSetRstCompressNumber(_hmap: maptype.HMAP, _number: int, _value: int) -> int:
        """
        Установить в заголовок растра номер алгоритма сжатия
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _value: номер алгоритма сжатия: ``0`` - растр не сжат, ``1`` - ``LZW``, ``2`` - ``JPEG`` ВНИМАНИЕ: Функция не выполняет сжатие изображения Для сжатия изображения по методу ``LZW`` воспользуйтесь функцией mapCompressLZW(), объявленной в mapapi.h Для сжатия изображения по методу ``JPEG`` воспользуйтесь функцией mapCompressJPEG(), объявленной в mapapi.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstCompressNumber_t (_hmap, _number, _value)

    mapGetRstCompressJpegQuality_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstCompressJpegQuality', maptype.HMAP, ctypes.c_long)
    def mapGetRstCompressJpegQuality(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить степень сжатия блока растра по алгоритму JPEG
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Возвращает степень сжатия изображения блока растра по алгоритму JPEG: 1-100, 1-максимальное сжатие, 100-сжатие без потери качества, рекомендуемое значение 60 При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstCompressJpegQuality_t (_hmap, _number)

    mapSetRstCompressJpegQuality_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstCompressJpegQuality', maptype.HMAP, ctypes.c_long, ctypes.c_int)
    def mapSetRstCompressJpegQuality(_hmap: maptype.HMAP, _number: int, _value: int) -> int:
        """
        Установить в заголовок растра степень сжатия блока растра по алгоритму JPEG
        
        :param _hmap: идентификатор открытой карты
        
        :param _number: номер файла в цепочке
        
        :param _value: степень сжатия изображения блока растра по алгоритму ``JPEG``: ``1````-100``, ``1``-максимальное сжатие, ``100``-сжатие без потери качества, рекомендуемое значение ``60`` Используйте для установки в заголовок растра номера алгоритма сжатия функцию mapSetRstCompressNumber() ВНИМАНИЕ: Функция не выполняет сжатие изображения Для сжатия изображения по методу ``JPEG`` воспользуйтесь функцией mapCompressJPEG(), объявленной в mapapi.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstCompressJpegQuality_t (_hmap, _number, _value)

    mapRstOptimizationPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRstOptimizationPro', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def mapRstOptimizationPro(_handle: maptype.HMESSAGE, _name: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _compressnumber: int, _borderflag: int, _quality: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Сжать растр RSW по заданному алгоритму
        
        :param _handle: идентификатор диалога для передачи сообщений о проценте выполнения ``WM_PROGRESSBAR``
        
        :param _name: имя сжимаемого файла RSW
        
        :param _newname: имя сжатого файла RSW
        
        :param _compressnumber: номер алгоритма сжатия (``RMF_COMPR_LZW``, ``RMF_COMPR_JPEG``, ``2416``)
        
        :param _borderflag: флаг удаления неотображаемых блоков (не попадающих в заданную рамку растра)
        
        :param _quality: степень сжатия растра по алгоритму ``RMF_COMPR_JPEG`` (рекомендуется ``60``) от ``0`` до ``100``
        
        :param _callevent: адрес функции оборатного вызова для уведомления о проценте обработанных наборов данных (maptype.h)
        
        :param _parm: адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы) вторым параметром в вызываемой функции передается процент от ``0`` до ``100``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapRstOptimizationPro_t (_handle, _name.buffer(), _newname.buffer(), _compressnumber, _borderflag, _quality, _callevent, _parm)

    mapGetRstPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstPoint', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.c_long, ctypes.c_long)
    def mapGetRstPoint(_hmap: maptype.HMAP, _number: int, _value: ctypes.POINTER(ctypes.c_long), _string: int, _column: int) -> int:
        """
        Прочитать элемент по абсолютным индексам
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _value: значение элемента
        
        :param _string: строка элемента
        
        :param _column: столбец элемента
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstPoint_t (_hmap, _number, _value, _string, _column)

    mapPutRstPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPutRstPoint', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapPutRstPoint(_hmap: maptype.HMAP, _number: int, _value: int, _string: int, _column: int) -> int:
        """
        Записать элемент по абсолютным индексам
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _value: значение элемента
        
        :param _string: строка элемента
        
        :param _column: столбец элемента
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPutRstPoint_t (_hmap, _number, _value, _string, _column)

    mapGetRstPlanePoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstPlanePoint', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.c_double, ctypes.c_double)
    def mapGetRstPlanePoint(_hmap: maptype.HMAP, _number: int, _value: ctypes.POINTER(ctypes.c_long), _x: float, _y: float) -> int:
        """
        Прочитать элемент по его плоским прямоугольным координатам в метрах из буфера
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _value: значение элемента
        
        :param _x: координата X элемента в метрах в системе координат растра
        
        :param _y: координата Y элемента в метрах в системе координат растра
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstPlanePoint_t (_hmap, _number, _value, _x, _y)

    mapGetRstPlanePointTriangle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstPlanePointTriangle', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.c_double, ctypes.c_double)
    def mapGetRstPlanePointTriangle(_hmap: maptype.HMAP, _number: int, _value: ctypes.POINTER(ctypes.c_long), _x: float, _y: float) -> int:
        """
        Прочитать элемент по его плоским прямоугольным координатам по методу треугольников
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _value: значение элемента
        
        :param _x: координата X точки в метрах в системе координат растра
        
        :param _y: координата Y точки в метрах в системе координат растра
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstPlanePointTriangle_t (_hmap, _number, _value, _x, _y)

    mapGetRstPlanePointColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstPlanePointColor', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.COLORREF), ctypes.c_double, ctypes.c_double)
    def mapGetRstPlanePointColor(_hmap: maptype.HMAP, _number: int, _color: ctypes.POINTER(maptype.COLORREF), _x: float, _y: float) -> int:
        """
        Определить цвет точки растра по прямоугольным координатам точки в метрах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _color: цвет элемента
        
        :param _x: координата X точки в метрах в системе координат растра
        
        :param _y: координата Y точки в метрах в системе координат растра
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstPlanePointColor_t (_hmap, _number, _color, _x, _y)

    mapGetRstBilinearInterpolationColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBilinearInterpolationColor', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.COLORREF), ctypes.POINTER(ctypes.c_long), ctypes.c_double, ctypes.c_double)
    def mapGetRstBilinearInterpolationColor(_hmap: maptype.HMAP, _number: int, _color: ctypes.POINTER(maptype.COLORREF), _indexcolor: ctypes.POINTER(ctypes.c_long), _x: float, _y: float) -> int:
        """
        Определить цвет точки по 4 соседним пикселям растра - билинейная интерполяция
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _color: заполняется вычисленным цветом indexсolor - заполняется индексом ближайшего цвета к вычисленному из палитры растра (для ``1``,``4`` и ``8`` бит на пиксель)
        
        :param _x: прямоугольная координата X точки в системе координат растра в метрах на местности
        
        :param _y: прямоугольная координата Y точки в системе координат растра в метрах на местности
        
        :returns: При попадании в крайние пиксели растра возвращается цвет ближайшего пикселя При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstBilinearInterpolationColor_t (_hmap, _number, _color, _indexcolor, _x, _y)

    mapGetRstBicubicInterpolationColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBicubicInterpolationColor', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.COLORREF), ctypes.POINTER(ctypes.c_long), ctypes.c_double, ctypes.c_double)
    def mapGetRstBicubicInterpolationColor(_hmap: maptype.HMAP, _number: int, _color: ctypes.POINTER(maptype.COLORREF), _indexcolor: ctypes.POINTER(ctypes.c_long), _x: float, _y: float) -> int:
        """
        Определить цвет точки по 16 соседним пикселям растра - бикубическая интерполяция
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _color: заполняется вычисленным цветом indexсolor - заполняется индексом ближайшего цвета к вычисленному из палитры растра (для ``1``,``4`` и ``8`` бит на пиксель)
        
        :param _x: прямоугольная координата X точки в системе координат растра в метрах на местности
        
        :param _y: прямоугольная координата Y точки в системе координат растра в метрах на местности
        
        :returns: При попадании в крайних 2 пикселя растра возвращается цвет ближайшего пикселя При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstBicubicInterpolationColor_t (_hmap, _number, _color, _indexcolor, _x, _y)

    mapPutRstPlanePoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPutRstPlanePoint', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.c_double)
    def mapPutRstPlanePoint(_hmap: maptype.HMAP, _number: int, _value: int, _x: float, _y: float) -> int:
        """
        Записать элемент по его прямоугольным координатам в метрах в буфер
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _value: значение элемента
        
        :param _x: координата X элемента
        
        :param _y: координата Y элемента
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPutRstPlanePoint_t (_hmap, _number, _value, _x, _y)

    mapPutRstPlaneLine_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPutRstPlaneLine', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapPutRstPlaneLine(_hmap: maptype.HMAP, _number: int, _color: int, _point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Записать отрезок в изображение основного растра по прямоугольным координатам в метрах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _color: цвет отрезка типа ``COLORREF`` для растров с ``16``,``24``,``32`` точек на пиксель, индекс цвета в палитре для растров с ``1``,``4``,``8`` точек на пиксель
        
        :param _point1: координаты начальной точки отрезка
        
        :param _point2: координаты конечной точки отрезка
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPutRstPlaneLine_t (_hmap, _number, _color, _point1, _point2)

    mapGetRstBlockCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBlockCount', maptype.HMAP, ctypes.c_long)
    def mapGetRstBlockCount(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить количество блоков растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstBlockCount_t (_hmap, _number)

    mapGetRstBlockRow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBlockRow', maptype.HMAP, ctypes.c_long)
    def mapGetRstBlockRow(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить число строк блоков растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstBlockRow_t (_hmap, _number)

    mapGetRstBlockColumn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBlockColumn', maptype.HMAP, ctypes.c_long)
    def mapGetRstBlockColumn(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить число столбцов блоков растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstBlockColumn_t (_hmap, _number)

    mapGetRstBlockSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBlockSize', maptype.HMAP, ctypes.c_long)
    def mapGetRstBlockSize(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить размер неусеченного блока растра в байтах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstBlockSize_t (_hmap, _number)

    mapGetRstCurrentBlockSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstCurrentBlockSize', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapGetRstCurrentBlockSize(_hmap: maptype.HMAP, _number: int, _string: int, _column: int) -> int:
        """
        Запросить размер текущего блока растра в байтах с учетом усеченных блоков
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _string: строка блока
        
        :param _column: столбец блока
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstCurrentBlockSize_t (_hmap, _number, _string, _column)

    mapGetRstBlockWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBlockWidth', maptype.HMAP, ctypes.c_long)
    def mapGetRstBlockWidth(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить ширину неусеченного блока растра в элементах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstBlockWidth_t (_hmap, _number)

    mapGetRstBlockHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBlockHeight', maptype.HMAP, ctypes.c_long)
    def mapGetRstBlockHeight(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить высоту неусеченного блока растра в элементах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstBlockHeight_t (_hmap, _number)

    mapGetRstCurrentBlockWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstCurrentBlockWidth', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapGetRstCurrentBlockWidth(_hmap: maptype.HMAP, _number: int, _column: int) -> int:
        """
        Запросить ширину текущего блока растра в элементах с учетом усеченных блоков
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _column: столбец блока
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstCurrentBlockWidth_t (_hmap, _number, _column)

    mapGetRstCurrentBlockHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstCurrentBlockHeight', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapGetRstCurrentBlockHeight(_hmap: maptype.HMAP, _number: int, _string: int) -> int:
        """
        Запросить высоту текущего блока растра в элементах с учетом усеченных блоков
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _string: строка блока
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstCurrentBlockHeight_t (_hmap, _number, _string)

    mapGetRstBlock_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetRstBlock', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapGetRstBlock(_hmap: maptype.HMAP, _number: int, _string: int, _column: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить адрес блока растра по номеру строки и столбца
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _string: строка блока
        
        :param _column: столбец блока Блоки последнего ряда могут иметь усеченный размер При запросе следующего блока может вернуть прежний адрес
        
        :returns: При ошибке возвращает ноль, иначе - адрес считанного блока
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetRstBlock_t (_hmap, _number, _string, _column)

    mapGetRstBlockAndCreate_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetRstBlockAndCreate', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapGetRstBlockAndCreate(_hmap: maptype.HMAP, _number: int, _string: int, _column: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить адрес блока растра по номеру строки и столбца
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _string: строка блока
        
        :param _column: столбец блока При отсутствии в файле - создается При запросе следующего блока может вернуть прежний адрес
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetRstBlockAndCreate_t (_hmap, _number, _string, _column)

    mapCheckRstBlockExistence_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckRstBlockExistence', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapCheckRstBlockExistence(_hmap: maptype.HMAP, _number: int, _blocknumber: int) -> int:
        """
        Запросить наличие блока растра в файле
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _blocknumber: порядковый номер блока
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCheckRstBlockExistence_t (_hmap, _number, _blocknumber)

    mapCheckRstBlockVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckRstBlockVisible', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapCheckRstBlockVisible(_hmap: maptype.HMAP, _number: int, _blocknumber: int) -> int:
        """
        Вернуть флаг отображения блока
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _blocknumber: порядковый номер блока
        
        :returns: Возвращает: ``0`` - не отображается, ``1`` - отображается, ``2`` - разделен рамкой При ошибке возвращает ноль
        :rtype: int
        """
        return mapCheckRstBlockVisible_t (_hmap, _number, _blocknumber)

    mapWriteRstBlock_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapWriteRstBlock', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_char_p, ctypes.c_long)
    def mapWriteRstBlock(_hmap: maptype.HMAP, _number: int, _string: int, _column: int, _bits: ctypes.c_char_p, _bitssize: int) -> int:
        """
        Записать блок в файл растрового изображения из памяти bits
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _string: строка блока
        
        :param _column: столбец блока
        
        :param _bits: указатель на начало изображения битовой области
        
        :param _bitssize: размер области bits в байтах
        
        :returns: Возвращает количество записанных байт При ошибке возвращает ноль.
        :rtype: int
        """
        return mapWriteRstBlock_t (_hmap, _number, _string, _column, _bits, _bitssize)

    mapPutRstBlockByMask_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPutRstBlockByMask', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_char_p, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapPutRstBlockByMask(_hmap: maptype.HMAP, _number: int, _string: int, _column: int, _mask: ctypes.c_char_p, _size: int, _width: int, _height: int, _value: int) -> int:
        """
        Записать блок размером size по DIB-маске mask индексом value
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _string: строка блока
        
        :param _column: столбец блока
        
        :param _mask: указатель на начало маски
        
        :param _size: размер области mask в байтах
        
        :param _width: ширина маски в байтах (``1`` байт соответствует элементу - ``0``/``1``)
        
        :param _height: число строк маски
        
        :param _value: значение, которое устанавливается в блок, если элемент маски равен ``0``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPutRstBlockByMask_t (_hmap, _number, _string, _column, _mask, _size, _width, _height, _value)

    mapSaveRst_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSaveRst', maptype.HMAP, ctypes.c_long)
    def mapSaveRst(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Записать изменения растра в файл
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSaveRst_t (_hmap, _number)

    mapPutRstFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPutRstFrame', maptype.HMAP, ctypes.c_long, ctypes.c_char_p, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapPutRstFrame(_hmap: maptype.HMAP, _number: int, _bits: ctypes.c_char_p, _left: int, _top: int, _width: int, _height: int, _begining: int, _widthinbyte: int) -> int:
        """
        Записать прямоугольный участок растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _bits: указатель на начало изображения битовой области
        
        :param _left: смещение слева в элементах (выравнено на границу байта)
        
        :param _top: смещение сверху в элементах
        
        :param _width: ширина в элементах (выравнено на границу байта)
        
        :param _height: высота в элементах
        
        :param _begining: начало изображения: ``1`` - (bits - указатель на первую строку битовой области) -``1`` - (bits - указатель на последнюю строку битовой области, в ``BMP`` изображение хранится снизу - вверх)
        
        :param _widthinbyte: ширина прямоугольного участка растра в байтах Принцип выравнивания: при ElementSize() ``= 1`` (бит) - left,width кратны ``8``, ``= 4`` (бит) - left,width кратны ``2``
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapPutRstFrame_t (_hmap, _number, _bits, _left, _top, _width, _height, _begining, _widthinbyte)

    mapGetRstFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstFrame', maptype.HMAP, ctypes.c_long, ctypes.c_char_p, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapGetRstFrame(_hmap: maptype.HMAP, _number: int, _bits: ctypes.c_char_p, _left: int, _top: int, _width: int, _height: int, _widthinbyte: int) -> int:
        """
        Прочитать прямоугольный участок растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _bits: указатель на начало изображения битовой области
        
        :param _left: смещение слева в элементах (выравнено на границу байта)
        
        :param _top: смещение сверху в элементах
        
        :param _width: ширина в элементах (выравнено на границу байта)
        
        :param _height: высота в элементах
        
        :param _widthinbyte: ширина прямоугольного участка растра в байтах Принцип выравнивания: при ElementSize() ``= 1`` (бит) - left,width кратны ``8``, ``= 4`` (бит) - left,width кратны ``2``
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstFrame_t (_hmap, _number, _bits, _left, _top, _width, _height, _widthinbyte)

    mapGetRstFrameRGB_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstFrameRGB', maptype.HMAP, ctypes.c_long, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapGetRstFrameRGB(_hmap: maptype.HMAP, _number: int, _bitsR: ctypes.c_char_p, _bitsG: ctypes.c_char_p, _bitsB: ctypes.c_char_p, _left: int, _top: int, _width: int, _height: int) -> int:
        """
        Прочитать цветовую плоскость прямоугольного участка растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _bitsR: указатель на начало изображения байтовой области красной плоскости
        
        :param _bitsG: указатель на начало изображения байтовой области зеленой плоскости
        
        :param _bitsB: указатель на начало изображения байтовой области синей плоскости
        
        :param _left: смещение слева в элементах
        
        :param _top: смещение сверху в элементах
        
        :param _width: ширина в элементах
        
        :param _height: высота в элементах Поддерживает только ``8``-битные растры (пока)
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstFrameRGB_t (_hmap, _number, _bitsR, _bitsG, _bitsB, _left, _top, _width, _height)

    mapGetRstFrameTurn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstFrameTurn', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.COLORREF), ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    def mapGetRstFrameTurn(_hmap: maptype.HMAP, _number: int, _bits: ctypes.POINTER(maptype.COLORREF), _width: int, _height: int, _strl: float, _coll: float, _strr: float, _colr: float) -> int:
        """
        Отобразить прямоугольный участок исходного растра в результирующем растре, расположенном в области памяти
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _bits: указатель на начало области памяти
        
        :param _width: ширина области памяти в элементах ``COLORREF``, количество столбцов результирующего растра
        
        :param _height: высота области памяти в элементах, количество строк результирующего растра
        
        :param _strl: координата левого элемента исходного растра
        
        :param _coll: координата левого элемента исходного растра
        
        :param _strr: координата правого элемента исходного растра
        
        :param _colr: координата правого элемента исходного растра Координаты strl,coll,strr,colr левого и правого элементов исходного растра в элементах растра определяют верхний граничный отрезок считываемого прямоугольного наклонного участка
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstFrameTurn_t (_hmap, _number, _bits, _width, _height, _strl, _coll, _strr, _colr)

    mapRstElementToPixel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRstElementToPixel', maptype.HMAP, ctypes.c_long, ctypes.c_double, ctypes.POINTER(ctypes.c_double))
    def mapRstElementToPixel(_hmap: maptype.HMAP, _number: int, _element: float, _pixel: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Пересчитать элементы растра в пикселы для текущего масштаба отображения
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _element: элементы растра
        
        :param _pixel: результат в пикселах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapRstElementToPixel_t (_hmap, _number, _element, _pixel)

    mapPixelToRstElement_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPixelToRstElement', maptype.HMAP, ctypes.c_long, ctypes.c_double, ctypes.POINTER(ctypes.c_double))
    def mapPixelToRstElement(_hmap: maptype.HMAP, _number: int, _pixel: float, _element: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Пересчитать пикселы в элементы растра для текущего масштаба отображения
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _pixel: пикселы
        
        :param _element: результат в элементах растра
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPixelToRstElement_t (_hmap, _number, _pixel, _element)

    mapBuildRstBlockMask_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBuildRstBlockMask', maptype.HMAP, ctypes.c_long, ctypes.c_char_p, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapBuildRstBlockMask(_hmap: maptype.HMAP, _number: int, _bits: ctypes.c_char_p, _size: int, _string: int, _column: int) -> int:
        """
        Сформировать битовую маску текущего блока с учетом рамки растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _bits: область битовой маски
        
        :param _size: размер области битовой маски в байтах
        
        :param _string: строка блока для заполнения маской
        
        :param _column: столбец блока
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapBuildRstBlockMask_t (_hmap, _number, _bits, _size, _string, _column)

    mapSetRstMask_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstMask', maptype.HMAP, ctypes.c_long, maptype.HOBJ)
    def mapSetRstMask(_hmap: maptype.HMAP, _number: int, _hobj: maptype.HOBJ) -> int:
        """
        Установить маску изображения растра по метрике объекта
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _hobj: объект карты с подобъектами
        
        :returns: При ошибке возвращает 0
        :rtype: int
        
        .. note::

           После выполнения функции отображение растра ограничится заданной областью
        """
        return mapSetRstMask_t (_hmap, _number, _hobj)

    mapFillRstVisiblePart_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapFillRstVisiblePart', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapFillRstVisiblePart(_hmap: maptype.HMAP, _number: int, _color: int) -> int:
        """
        Залить цветом часть растра, ограниченной рамкой
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _color: цвет
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapFillRstVisiblePart_t (_hmap, _number, _color)

    mapGetRstProcessingState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstProcessingState', maptype.HMAP, ctypes.c_long)
    def mapGetRstProcessingState(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить состояние растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке Возвращаемые значения: ``0`` - нет данных; или создание уменьшенных копий и сжатие не выполнялись ``1`` - создание всех уровней уменьшенных копий, сжатие ``JPEG`` растра ``2`` - создание всех уровней уменьшенных копий, сжатие ``LZW`` растра ``4`` - создание всех уровней уменьшенных копий
        """
        return mapGetRstProcessingState_t (_hmap, _number)

    mapSetRstProcessingState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstProcessingState', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetRstProcessingState(_hmap: maptype.HMAP, _number: int, _state: int) -> int:
        """
        Установить состояние растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _state: состояние растра Возможные значения состояния растра state: ``0`` - нет данных; или создание уменьшенных копий и сжатие не выполнялись ``1`` - создание всех уровней уменьшенных копий, сжатие ``JPEG`` растра ``2`` - создание всех уровней уменьшенных копий, сжатие ``LZW`` растра ``4`` - создание всех уровней уменьшенных копий
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapSetRstProcessingState_t (_hmap, _number, _state)

    mapOptimizationRstByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapOptimizationRstByNameUn', maptype.PWCHAR, maptype.HWND)
    def mapOptimizationRstByNameUn(_rswname: mapsyst.WTEXT, _handle: maptype.HWND) -> int:
        """
        Оптимизировать растр для открытия в ГИС Сервере
        
        :param _rswname: имя файла растра
        
        :param _handle: идентификатор окна, которое будет извещаться о ходе процесса (``0x585`` - ``0x588``) Функция проверяет состояние растра и при необходимости выполняет для растра оптимизацию со сжатием (``JPEG`` - для ``24``-х битных растров, ``LZW`` - для всех остальных) и создание всех уровней уменьшенной копии Необходимо закрыть растр из всех документов перед вызовом функции
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapOptimizationRstByNameUn_t (_rswname.buffer(), _handle)

    mapGetRstDuplicatesCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstDuplicatesCount', maptype.HMAP, ctypes.c_long)
    def mapGetRstDuplicatesCount(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить количество созданных уменьшенных копий в растре
        
        :param _hmap: идентификатор открытой основной векторной карты
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstDuplicatesCount_t (_hmap, _number)

    mapUpdateRstDuplicates_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateRstDuplicates', maptype.HMAP, ctypes.c_long)
    def mapUpdateRstDuplicates(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Обновить уменьшенную копию
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает 0
        :rtype: int
        
        .. note::

           Если уменьшенные копии не существуют, создаются ТРИ копии
        """
        return mapUpdateRstDuplicates_t (_hmap, _number)

    mapUpdateRstDuplicatesEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateRstDuplicatesEx', maptype.HMAP, ctypes.c_long, maptype.HPAINT)
    def mapUpdateRstDuplicatesEx(_hmap: maptype.HMAP, _number: int, _hpaint: maptype.HPAINT) -> int:
        """
        Обновить уменьшенную копию
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла растра в списке растров (в цепочке)
        
        :param _hpaint: контекст поддержки многопоточного вызова (mapCreatePaintControl)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если уменьшенные копии не существуют, создаются ДВЕ копии
        """
        return mapUpdateRstDuplicatesEx_t (_hmap, _number, _hpaint)

    mapUpdateRstDuplicateOfBlock_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateRstDuplicateOfBlock', maptype.HMAP, ctypes.c_long, ctypes.c_int, ctypes.c_int)
    def mapUpdateRstDuplicateOfBlock(_hmap: maptype.HMAP, _number: int, _string: int, _column: int) -> int:
        """
        Обновить уменьшенную копию блока растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке value  - значение элемента
        
        :param _string: строка элемента
        
        :param _column: столбец элемента
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdateRstDuplicateOfBlock_t (_hmap, _number, _string, _column)

    mapGetRstUserLabel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstUserLabel', maptype.HMAP, ctypes.c_long)
    def mapGetRstUserLabel(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить пользовательский идентификатор растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstUserLabel_t (_hmap, _number)

    mapSetRstUserLabel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstUserLabel', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetRstUserLabel(_hmap: maptype.HMAP, _number: int, _userlabel: int) -> int:
        """
        Установить пользовательский идентификатор растра
        
        :param _number: номер файла в цепочке
        
        :param _userlabel: идентификатор модели
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstUserLabel_t (_hmap, _number, _userlabel)

    mapWhereSouthWestRstPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapWhereSouthWestRstPlane', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapWhereSouthWestRstPlane(_hmap: maptype.HMAP, _number: int, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить координаты юго-западного угла растра в метрах
        
        :param _hmap: идентификатор открытой основной векторной карты
        
        :param _number: номер файла в цепочке
        
        :param _x: адрес для записи координаты X найденной точки в метрах
        
        :param _y: адрес для записи координаты Y найденной точки в метрах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapWhereSouthWestRstPlane_t (_hmap, _number, _x, _y)

    mapDeleteRstFileUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRstFileUn', maptype.PWCHAR)
    def mapDeleteRstFileUn(_name: mapsyst.WTEXT) -> int:
        """
        Удалить файл RSW
        
        :param _name: имя файла Функция предназначена для удаления растра и его составных частей Растровая карта размером более 4Gb состоит из ``2``-х файлов: ``*.rsw`` и ``*.rsw.01`` Аналог функции DeleteTheFile()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteRstFileUn_t (_name.buffer())

    mapMoveRstFileUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapMoveRstFileUn', maptype.PWCHAR, maptype.PWCHAR)
    def mapMoveRstFileUn(_oldname: mapsyst.WTEXT, _newname: mapsyst.WTEXT) -> int:
        """
        Переименовать имя файла RSW
        
        :param _oldname: старое имя файла
        
        :param _newname: новое имя файла Функция предназначена для переименования растра и его составных частей Растровая карта размером более 4Gb состоит из ``2``-х файлов: ``*.rsw`` и ``*.rsw.01`` Аналог функции MoveTheFile()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapMoveRstFileUn_t (_oldname.buffer(), _newname.buffer())

    mapCopyRstFileUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCopyRstFileUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapCopyRstFileUn(_oldname: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _exist: int) -> int:
        """
        Скопировать файл RSW
        
        :param _oldname: старое имя файла
        
        :param _newname: новое имя файла
        
        :param _exist: флаг наличия файла Функция предназначена для копирования растра и его составных частей Растровая карта размером более 4Gb состоит из ``2``-х файлов: ``*.rsw`` и ``*.rsw.01`` Аналог функции CopyTheFile()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCopyRstFileUn_t (_oldname.buffer(), _newname.buffer(), _exist)

    mapRstIsAccessTiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRstIsAccessTiff', maptype.HMAP, ctypes.c_long)
    def mapRstIsAccessTiff(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить тип растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Возвращает: ``0`` - обычный растр ``1`` - растр-пустышка с прямым доступом к файлу TIFF
        :rtype: int
        """
        return mapRstIsAccessTiff_t (_hmap, _number)

    mapGetRstFileName_TiffUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstFileName_TiffUn', maptype.HMAP, ctypes.c_long, maptype.PWCHAR, ctypes.c_int)
    def mapGetRstFileName_TiffUn(_hmap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _namesize: int) -> int:
        """
        Запросить имя TIFF-файла для растра с номером  number
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _name: возвращаемое имя
        
        :param _namesize: размер строки в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstFileName_TiffUn_t (_hmap, _number, _name.buffer(), _namesize)

    mapGetRstAffinCoef_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstAffinCoef_Tiff', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.AFFINCOEF))
    def mapGetRstAffinCoef_Tiff(_hmap: maptype.HMAP, _number: int, _affincoef: ctypes.POINTER(maptype.AFFINCOEF)) -> int:
        """
        Запросить матрицу аффинных коэффициентов привязки TIFF-файла
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _affincoef: возвращаемая матрица аффинных коэффициентов привязки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstAffinCoef_Tiff_t (_hmap, _number, _affincoef)

    mapSetRstAffinCoef_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstAffinCoef_Tiff', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.AFFINCOEF))
    def mapSetRstAffinCoef_Tiff(_hmap: maptype.HMAP, _number: int, _affincoef: ctypes.POINTER(maptype.AFFINCOEF)) -> int:
        """
        Установить матрицу аффинных коэффициентов привязки TIFF-файла
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _affincoef: устанавливаемая матрица аффинных коэффициентов привязки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstAffinCoef_Tiff_t (_hmap, _number, _affincoef)

    mapGetRstBandCount_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBandCount_Tiff', maptype.HMAP, ctypes.c_long)
    def mapGetRstBandCount_Tiff(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить количество каналов TIFF-растра с номером  number
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstBandCount_Tiff_t (_hmap, _number)

    mapGetRstRedBand_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstRedBand_Tiff', maptype.HMAP, ctypes.c_long)
    def mapGetRstRedBand_Tiff(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить номер канала TIFF-растра с номером number, отображаемого красным
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstRedBand_Tiff_t (_hmap, _number)

    mapGetRstGreenBand_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstGreenBand_Tiff', maptype.HMAP, ctypes.c_long)
    def mapGetRstGreenBand_Tiff(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить номер канала TIFF-растра с номером number, отображаемого зеленым
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstGreenBand_Tiff_t (_hmap, _number)

    mapGetRstBlueBand_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBlueBand_Tiff', maptype.HMAP, ctypes.c_long)
    def mapGetRstBlueBand_Tiff(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить номер канала TIFF-растра с номером number, отображаемого синим
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstBlueBand_Tiff_t (_hmap, _number)

    mapSetRstRedBand_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstRedBand_Tiff', maptype.HMAP, ctypes.c_long, ctypes.c_int)
    def mapSetRstRedBand_Tiff(_hmap: maptype.HMAP, _number: int, _redband: int) -> int:
        """
        Установить номер канала TIFF-растра с номером  number, отображаемого красным
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _redband: номер канала
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если установить -1, то такой канал не используется
        """
        return mapSetRstRedBand_Tiff_t (_hmap, _number, _redband)

    mapSetRstGreenBand_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstGreenBand_Tiff', maptype.HMAP, ctypes.c_long, ctypes.c_int)
    def mapSetRstGreenBand_Tiff(_hmap: maptype.HMAP, _number: int, _greenband: int) -> int:
        """
        Установить номер канала TIFF-растра с номером  number, отображаемого зеленым
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _greenband: номер канала
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если установить -1, то такой канал не используется
        """
        return mapSetRstGreenBand_Tiff_t (_hmap, _number, _greenband)

    mapSetRstBlueBand_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstBlueBand_Tiff', maptype.HMAP, ctypes.c_long, ctypes.c_int)
    def mapSetRstBlueBand_Tiff(_hmap: maptype.HMAP, _number: int, _blueband: int) -> int:
        """
        Установить номер канала TIFF-растра с номером  number, отображаемого синим
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _blueband: номер канала
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если установить -1, то такой канал не используется
        """
        return mapSetRstBlueBand_Tiff_t (_hmap, _number, _blueband)

    mapSetRstVegIndex_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstVegIndex_Tiff', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.VEGINDEX))
    def mapSetRstVegIndex_Tiff(_hmap: maptype.HMAP, _number: int, _vegindex: ctypes.POINTER(maptype.VEGINDEX)) -> int:
        """
        Установить отображение мультиспектрального растра по вегетационному индексу
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _vegindex: параметры отображения вегетационного индекса Перед вызовом необходимо убедиться при помощи функции mapRstIsAccessTiff, что для растра с номером number осуществляется прямой доступ к файлу ``TIFF`` Функция справедлива для мультиспектральных изображений (mapGetRstBandCount_Tiff() >``= 3``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstVegIndex_Tiff_t (_hmap, _number, _vegindex)

    mapGetRstVegIndex_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstVegIndex_Tiff', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.VEGINDEX))
    def mapGetRstVegIndex_Tiff(_hmap: maptype.HMAP, _number: int, _vegindex: ctypes.POINTER(maptype.VEGINDEX)) -> int:
        """
        Запросить параметры отображения вегетационного индекса
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _vegindex: возвращаемые параметры отображения вегетационного индекса Перед вызовом необходимо убедиться при помощи функции mapRstIsAccessTiff, что для растра с номером number осуществляется прямой доступ к файлу ``TIFF`` Функция справедлива для мультиспектральных изображений (mapGetRstBandCount_Tiff() >``= 3``)
        
        :returns: Возвращает параметры отображения вегетационного индекса Если отображение по вегетационному индексу не установлено возвращает 0
        :rtype: int
        """
        return mapGetRstVegIndex_Tiff_t (_hmap, _number, _vegindex)

    mapBeginRstPixelReading_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBeginRstPixelReading_Tiff', maptype.HMAP, ctypes.c_long)
    def mapBeginRstPixelReading_Tiff(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Начинает буферизированное чтение пикселей функцией mapGetRstBandPixel_Tiff
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           После завершения чтения пикселей необходимо вызвать mapEndRstPixelReading_Tiff
        """
        return mapBeginRstPixelReading_Tiff_t (_hmap, _number)

    mapEndRstPixelReading_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapEndRstPixelReading_Tiff', maptype.HMAP, ctypes.c_long)
    def mapEndRstPixelReading_Tiff(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Заканчивает буферизированное чтение пикселей функцией mapGetRstBandPixel_Tiff
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapEndRstPixelReading_Tiff_t (_hmap, _number)

    mapGetRstBandPixel_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBandPixel_Tiff', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapGetRstBandPixel_Tiff(_hmap: maptype.HMAP, _number: int, _x: int, _y: int, _bandnum: int, _color: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить яркость пиксела изображения на канал bandnum
        
        :param _x: координата X пикселя в системе координат растра (в пикселях)
        
        :param _y: координата Y пикселя в системе координат растра (в пикселях)
        
        :param _bandnum: номер канала (от ``0`` до mapGetRstBandCount_Tiff - ``1``)
        
        :param _color: возвращаемое значение реально записанное в растре (может быть ``1``,``4``,``8``,``16`` бит)
        
        :returns: Возвращает яркость пиксела изображения на канал bandnum При ошибке возвращает 0
        :rtype: int
        
        .. note::

           Если вызвается не внутри блока mapBeginRstPixelReading_Tiff -
           mapEndRstPixelReading_Tiff, то чтение выполняется очень медленно
        """
        return mapGetRstBandPixel_Tiff_t (_hmap, _number, _x, _y, _bandnum, _color)

    mapSetRstPaintCellRadius_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstPaintCellRadius_Tiff', ctypes.c_long)
    def mapSetRstPaintCellRadius_Tiff(_radius: int) -> int:
        """
        Установить радиус клетки в пикселях
        
        :param _radius: устанавливаемый радиус клетки в пикселях (не может быть меньше ``0``)
        
        :returns: При ошибке возвращает 0
        :rtype: int
        
        .. note::

           Если равен 0, то все пикселы вычисляются по строгим формулам
           Значение по умолчанию 3
           Устанавливает радиус клетки в узлах которой пересчет координат выполняется
           по строгим формулам при отрисовке растра в системе координат, отличной от
           системы координат растра
           Между узлами пересчет координат выполняется линейной интерполяцией. Коэффициенты
           линейного пересчета внутри клетки вычисляются по двум верхним узлам клетки
           При увеличении радиуса увеличивается скорость отрисовки, но ухудшается качество
           изображения при значительной деформации системы координат отрисовки относительно
           системы координат растра (изображение сегментируется по размеру клетки)
           Этот параметр является глобальным, т.е. с момента установки все растры
           отрисовываются с использовнаием этого параметра
        """
        return mapSetRstPaintCellRadius_Tiff_t (_radius)

    mapGetRstPaintCellRadius_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstPaintCellRadius_Tiff')
    def mapGetRstPaintCellRadius_Tiff() -> int:
        """
        Запросить радиус клетки в пикселях
        
        :returns: Возвращает радиус клетки в узлах которой пересчет координат выполняется по строгим формулам при отрисовке растра в системе координат, отличной от системы координат растра При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstPaintCellRadius_Tiff_t ()

    mapGetRstBitInBand_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBitInBand_Tiff', maptype.HMAP, ctypes.c_long)
    def mapGetRstBitInBand_Tiff(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить глубину цвета на канал
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Возвращает глубину цвета на канал (1, 4, 8, 16) При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstBitInBand_Tiff_t (_hmap, _number)

    mapGetRstHistogram_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstHistogram_Tiff', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.DWORD))
    def mapGetRstHistogram_Tiff(_hmap: maptype.HMAP, _number: int, _count: int, _histogram: ctypes.POINTER(maptype.DWORD)) -> int:
        """
        Запросить гистограмму
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _count: количество элементов в массиве histogram количество элементов вычисляется по формуле count = BandCount ``*`` (``1`` << BitInBand) Для палитровых растров BandCount ``= 1`` для ``1`` битных растров (палитровых) count ``= 2`` для ``4`` битных растров (палитровых) count ``= 16`` для ``8`` битных растров (палитровых) count ``= 256`` для ``RGB``                           count = ``3 *`` ``256`` ``= 768`` для ``8``  битных мультиспектральных  count = BandCount ``* 256`` для ``16`` битных мультиспектральных  count = BandCount ``* 65536``
        
        :param _histogram: возвращаемая гистограмма Гистограмма - поканальный массив количества пикселей, присутствующих в растре
        
        :returns: Возвращает гистограмму При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstHistogram_Tiff_t (_hmap, _number, _count, _histogram)

    mapGetRstLookupTable_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstLookupTable_Tiff', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_byte), ctypes.c_long)
    def mapGetRstLookupTable_Tiff(_hmap: maptype.HMAP, _number: int, _bandnum: int, _table: ctypes.POINTER(ctypes.c_byte), _tablesize: int) -> int:
        """
        Запросить таблицу преобразования цвета
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _bandnum: номер канала (от ``0`` до mapGetRstBandCount_Tiff - ``1``)
        
        :param _table: возвращаемая таблица преобразования
        
        :param _tablesize: размер таблицы table (для ``8`` бит должно быть ``256``, для ``16`` бит - ``65536``)
        
        :returns: Возвращает таблицу преобразования цвета для отображения панхроматических, RGB и мультиспектральных растров с глубиной цвета 8 или 16 бит При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstLookupTable_Tiff_t (_hmap, _number, _bandnum, _table, _tablesize)

    mapSetRstLookupTable_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstLookupTable_Tiff', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_byte), ctypes.c_long)
    def mapSetRstLookupTable_Tiff(_hmap: maptype.HMAP, _number: int, _bandnum: int, _table: ctypes.POINTER(ctypes.c_byte), _tablesize: int) -> int:
        """
        Установить таблицу преобразования цвета
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _bandnum: номер канала (от ``0`` до mapGetRstBandCount_Tiff - ``1``)
        
        :param _table: таблица преобразования
        
        :param _tablesize: размер таблицы table (для ``8`` бит должно быть не меньше ``256``, для ``16`` бит - не меньше ``65536``) Устанавливает таблицу преобразования цвета для отображения панхроматических, ``RGB`` и мультиспектральных растров с глубиной цвета ``8`` или ``16`` бит
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapSetRstLookupTable_Tiff_t (_hmap, _number, _bandnum, _table, _tablesize)

    mapGetRstBlockWidth_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBlockWidth_Tiff', maptype.HMAP, ctypes.c_long)
    def mapGetRstBlockWidth_Tiff(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить ширину блока
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Возвращает ширину блока в пикселях При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstBlockWidth_Tiff_t (_hmap, _number)

    mapGetRstBlockHeight_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBlockHeight_Tiff', maptype.HMAP, ctypes.c_long)
    def mapGetRstBlockHeight_Tiff(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить высоту блока
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Возвращает высоту блока в пикселях При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstBlockHeight_Tiff_t (_hmap, _number)

    mapGetRstBlockPixelType_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBlockPixelType_Tiff', maptype.HMAP, ctypes.c_long)
    def mapGetRstBlockPixelType_Tiff(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить способ расположения цветовых составляющих пикселя
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Возвращает способ расположения цветовых составляющих пикселя в блоке Возвращаемые значения: ``0`` - ошибка выполнения ``1`` - последовательно RGB RGB ... ``2`` - по цветовым плоскостям  RRR... GGG... BBB...
        :rtype: int
        """
        return mapGetRstBlockPixelType_Tiff_t (_hmap, _number)

    mapGetRstBlockRowCount_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBlockRowCount_Tiff', maptype.HMAP, ctypes.c_long)
    def mapGetRstBlockRowCount_Tiff(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить количество строк блоков
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Возвращает количество строк блоков При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstBlockRowCount_Tiff_t (_hmap, _number)

    mapGetRstBlockColCount_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBlockColCount_Tiff', maptype.HMAP, ctypes.c_long)
    def mapGetRstBlockColCount_Tiff(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить количество столбцов блоков
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Возвращает количество столбцов блоков При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstBlockColCount_Tiff_t (_hmap, _number)

    mapGetRstBlockSize_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBlockSize_Tiff', maptype.HMAP, ctypes.c_long)
    def mapGetRstBlockSize_Tiff(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить размер блока в байтах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке Для ``1`` и ``4`` битных растров в блок записывается ``1`` байт на пиксель
        
        :returns: Возвращает размер блока в байтах При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstBlockSize_Tiff_t (_hmap, _number)

    mapGetRstBlock_Tiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBlock_Tiff', maptype.HMAP, ctypes.c_long, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapGetRstBlock_Tiff(_hmap: maptype.HMAP, _number: int, _blockrow: int, _blockcol: int, _buf: ctypes.c_char_p, _bufsize: int) -> int:
        """
        Прочитать блок из растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _blockrow: номер строки блоков
        
        :param _blockcol: номер столбца блоков
        
        :param _buf: буфер, в который записывается изображение блока bifsize  - размер блока, должен быть равен mapGetRstBlockSize_Tiff Для ``1`` и ``4`` битных растров в блок записывается ``1`` байт на пиксель
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstBlock_Tiff_t (_hmap, _number, _blockrow, _blockcol, _buf, _bufsize)

    mapIsTiffOpenWithoutConvertUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsTiffOpenWithoutConvertUn', maptype.PWCHAR)
    def mapIsTiffOpenWithoutConvertUn(_name: mapsyst.WTEXT) -> int:
        """
        Проверить файл TIF на возможность открытия без преобразования в формат RSW
        
        :param _name: номер файла в цепочке
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapIsTiffOpenWithoutConvertUn_t (_name.buffer())

    mapCreateTiffExUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCreateTiffExUn', maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.CREATETIFPARMEX))
    def mapCreateTiffExUn(_filename: mapsyst.WTEXT, _width: int, _height: int, _parm: ctypes.POINTER(maptype.CREATETIFPARMEX)) -> ctypes.c_void_p:
        """
        Создать TIFF файл
        
        :param _filename: имя создаваемого ``TIFF`` файла
        
        :param _width: ширина растра в пикселях
        
        :param _height: высота растра в пикселях
        
        :param _parm: параметры создания растра
        
        :returns: Возвращает идентификатор созданного растра При ошибке возвращает 0
        """
        return mapCreateTiffExUn_t (_filename.buffer(), _width, _height, _parm)

    mapFreeTiff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeTiff', ctypes.c_void_p)
    def mapFreeTiff(_tiff: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Освободить идентификатор создания TIFF файла
        
        :param _tiff: идентификатор, полученный при создании ``TIFF`` файла функцией mapCreateTiffEx
        
        :returns: При ошибке возвращает 0
        """
        return mapFreeTiff_t (_tiff)

    mapGetTiffBlockWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetTiffBlockWidth', ctypes.c_void_p)
    def mapGetTiffBlockWidth(_tiff: ctypes.c_void_p) -> int:
        """
        Запросить ширину блока
        
        :param _tiff: идентификатор, полученный при создании ``TIFF`` файла функцией mapCreateTiffEx
        
        :returns: Возвращает ширину блока в пикселях При ошибке возвращает 0
        :rtype: int
        """
        return mapGetTiffBlockWidth_t (_tiff)

    mapGetTiffBlockHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetTiffBlockHeight', ctypes.c_void_p)
    def mapGetTiffBlockHeight(_tiff: ctypes.c_void_p) -> int:
        """
        Запросить высоту блока
        
        :param _tiff: идентификатор, полученный при создании ``TIFF`` файла функцией mapCreateTiffEx
        
        :returns: Возвращает высоту блока в пикселях При ошибке возвращает 0
        :rtype: int
        """
        return mapGetTiffBlockHeight_t (_tiff)

    mapGetTiffBlockRowCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetTiffBlockRowCount', ctypes.c_void_p)
    def mapGetTiffBlockRowCount(_tiff: ctypes.c_void_p) -> int:
        """
        Запросить количество строк блоков
        
        :param _tiff: идентификатор, полученный при создании ``TIFF`` файла функцией mapCreateTiffEx
        
        :returns: Возвращает количество строк блоков При ошибке возвращает 0
        :rtype: int
        """
        return mapGetTiffBlockRowCount_t (_tiff)

    mapGetTiffBlockColCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetTiffBlockColCount', ctypes.c_void_p)
    def mapGetTiffBlockColCount(_tiff: ctypes.c_void_p) -> int:
        """
        Запросить количество столбцов блоков
        
        :param _tiff: идентификатор, полученный при создании ``TIFF`` файла функцией mapCreateTiffEx
        
        :returns: Возвращает количество столбцов блоков При ошибке возвращает 0
        :rtype: int
        """
        return mapGetTiffBlockColCount_t (_tiff)

    mapGetTiffBandPixelType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetTiffBandPixelType', ctypes.c_void_p)
    def mapGetTiffBandPixelType(_tiff: ctypes.c_void_p) -> int:
        """
        Запросить тип пикселя на канал
        
        :param _tiff: идентификатор, полученный при создании ``TIFF`` файла функцией mapCreateTiffEx
        
        :returns: Возвращает тип пикселя на канал (PT_BYTE и другие) При ошибке возвращает 0
        :rtype: int
        """
        return mapGetTiffBandPixelType_t (_tiff)

    mapWriteTiffBlock_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapWriteTiffBlock', ctypes.c_void_p, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_void_p))
    def mapWriteTiffBlock(_tiff: ctypes.c_void_p, _bandnum: int, _col: int, _row: int, _image: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Записать блок в файл
        
        :param _tiff: идентификатор, полученный при создании ``TIFF`` файла функцией mapCreateTiffEx
        
        :param _bandnum: номер канала
        
        :param _col: номер столбца тайла
        
        :param _row: номер строки тайла
        
        :param _image: изображение тайла Ширина, высота тайла запрашивается через mapGetTiffBlockWidth, mapGetTiffBlockHeight Размер пикселя в байтах зависит от типа пикселя, определяемый через GetTiffBandPixelType В последних строках и столбцах размер тайла не усеченный
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapWriteTiffBlock_t (_tiff, _bandnum, _col, _row, _image)

    mapSetTiffLocation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetTiffLocation', ctypes.c_void_p, ctypes.POINTER(maptype.AFFINCOEF))
    def mapSetTiffLocation(_tiff: ctypes.c_void_p, _coef: ctypes.POINTER(maptype.AFFINCOEF)) -> int:
        """
        Установить матрицу привязки растра
        
        :param _tiff: идентификатор, полученный при создании ``TIFF`` файла функцией mapCreateTiffEx
        
        :param _coef: матрица, связывающая систему координат растра в пикселях с системой координат местности в метрах Xmeter = coef->``A0`` + coef->``A1`` ``*`` Xpix + coef->``A2`` ``*`` Ypix Ymeter = coef->``B0`` + coef->``B1`` ``*`` Xpix + coef->``B2`` ``*`` Ypix Направление осей -------------Xrst |    Ymeter |      | Yrst   | ---------- Xmeter
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapSetTiffLocation_t (_tiff, _coef)

    mapSetTiffProjection_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetTiffProjection', ctypes.c_void_p, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapSetTiffProjection(_tiff: ctypes.c_void_p, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        """
        Установить параметры системы координат растра
        
        :param _tiff: идентификатор, полученный при создании ``TIFF`` файла функцией mapCreateTiffEx
        
        :param _mapregister: адрес структуры, содержащей параметры проекции исходного материала
        
        :param _ellipsoidparam: адрес структуры, содержащей параметры эллипсоида
        
        :param _datumparam: адрес структуры, содержащей коэффициенты трансформирования геодезических координат Структуры ``MAPREGISTEREX``, ``DATUMPARAM``, ``ELLIPSOIDPARAM`` описаны в mapcreat.h
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapSetTiffProjection_t (_tiff, _mapregister, _ellipsoidparam, _datumparam)

    mapSetTiffProjection3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetTiffProjection3D', ctypes.c_void_p, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapSetTiffProjection3D(_tiff: ctypes.c_void_p, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        """
        Установить параметры системы координат матрицы высот
        
        :param _tiff: идентификатор, полученный при создании ``TIFF`` файла функцией mapCreateTiff
        
        :param _mapregister: адрес структуры, содержащей параметры проекции исходного материала
        
        :param _ellipsoidparam: адрес структуры, содержащей параметры эллипсоида
        
        :param _datumparam: адрес структуры, содержащей коэффициенты трансформирования геодезических координат Структуры ``MAPREGISTEREX``, ``DATUMPARAM``, ``ELLIPSOIDPARAM`` описаны в mapcreat.h Добавляется вертикальная СК, соответствующая значению поля ``MAPREGISTEREX``::HeightSystem (Система высот)
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapSetTiffProjection3D_t (_tiff, _mapregister, _ellipsoidparam, _datumparam)

    mapTiffIsGeographic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapTiffIsGeographic', ctypes.c_void_p)
    def mapTiffIsGeographic(_tiff: ctypes.c_void_p) -> int:
        """
        Запросить - соответствует ли тип системы координат геодезической СК
        
        :param _tiff: идентификатор, полученный при создании ``TIFF`` файла функцией mapCreateTiffEx
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapTiffIsGeographic_t (_tiff)

    mapSetTiffNoDataValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetTiffNoDataValue', ctypes.c_void_p, ctypes.c_long, ctypes.c_double)
    def mapSetTiffNoDataValue(_tiff: ctypes.c_void_p, _bandnum: int, _value: float) -> int:
        """
        Установить значение NoData для канала
        
        :param _tiff: идентификатор, полученный при создании ``TIFF`` файла функцией mapCreateTiffEx
        
        :param _bandnum: номер канала
        
        :param _value: значение NoData
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapSetTiffNoDataValue_t (_tiff, _bandnum, _value)

    mapRstIsAccessGraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRstIsAccessGraphicFile', maptype.HMAP, ctypes.c_long)
    def mapRstIsAccessGraphicFile(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить тип растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Возвращает: ``0`` - обычный растр ``1`` - растр-пустышка с прямым доступом к графическому файлу (TIFF, GeoTIFF, IMG, JPEG, PNG, GIF, BMP) При ошибке возвращает 0
        :rtype: int
        """
        return mapRstIsAccessGraphicFile_t (_hmap, _number)

    mapGetRstGraphicFileNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstGraphicFileNameUn', maptype.HMAP, ctypes.c_long, maptype.PWCHAR, ctypes.c_int)
    def mapGetRstGraphicFileNameUn(_hmap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить имя графического файла для растра с номером  number
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _name: возвращаемое имя
        
        :param _size: размер строки в байтах Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile, что для растра с номером number осуществляется прямой доступ к графическому файлу
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstGraphicFileNameUn_t (_hmap, _number, _name.buffer(), _size)

    mapGetRstGraphicBandFileNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstGraphicBandFileNameUn', maptype.HMAP, ctypes.c_long, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def mapGetRstGraphicBandFileNameUn(_hmap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _namesize: int, _numberband: int) -> int:
        """
        Запросить имя файла, применяемого для хранения канала изображения numberband, для растра с номером number
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _name: возвращаемое имя графического файла
        
        :param _namesize: размер строки в байтах
        
        :param _numberband: номер канала изображения, начиная с ``1`` Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile, что для растра с номером number осуществляется прямой доступ к графическому файлу Количество графических файлов, применяемых для хранения каналов изображения, запрашивается вызом функции mapGetRstBandFilesCount_GraphicFile
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstGraphicBandFileNameUn_t (_hmap, _number, _name.buffer(), _namesize, _numberband)

    mapGetRstAffinCoef_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstAffinCoef_GraphicFile', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.AFFINCOEF))
    def mapGetRstAffinCoef_GraphicFile(_hmap: maptype.HMAP, _number: int, _affincoef: ctypes.POINTER(maptype.AFFINCOEF)) -> int:
        """
        Запросить матрицу аффинных коэффициентов привязки графического файла
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _affincoef: возвращаемая матрица аффинных коэффициентов привязки Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile, что для растра с номером number осуществляется прямой доступ к графическому файлу
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstAffinCoef_GraphicFile_t (_hmap, _number, _affincoef)

    mapSetRstAffinCoef_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstAffinCoef_GraphicFile', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.AFFINCOEF))
    def mapSetRstAffinCoef_GraphicFile(_hmap: maptype.HMAP, _number: int, _affincoef: ctypes.POINTER(maptype.AFFINCOEF)) -> int:
        """
        Установить матрицу аффинных коэффициентов привязки графического файла
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _affincoef: устанавливаемая матрица аффинных коэффициентов привязки Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile, что для растра с номером number осуществляется прямой доступ к графическому файлу
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRstAffinCoef_GraphicFile_t (_hmap, _number, _affincoef)

    mapGetRstBandCount_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBandCount_GraphicFile', maptype.HMAP, ctypes.c_long)
    def mapGetRstBandCount_GraphicFile(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить количество каналов графического файла с номером  number
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile, что для растра с номером number осуществляется прямой доступ к графическому файлу
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstBandCount_GraphicFile_t (_hmap, _number)

    mapGetRstBandFilesCount_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBandFilesCount_GraphicFile', maptype.HMAP, ctypes.c_long)
    def mapGetRstBandFilesCount_GraphicFile(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить количество графических файлов, применяемых для хранения каналов изображения
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile, что для растра с номером number осуществляется прямой доступ к графическому файлу
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstBandFilesCount_GraphicFile_t (_hmap, _number)

    mapGetRstRedBand_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstRedBand_GraphicFile', maptype.HMAP, ctypes.c_long)
    def mapGetRstRedBand_GraphicFile(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить номер канала графического файла с номером  number, отображаемого красным
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile, что для растра с номером number осуществляется прямой доступ к графическому файлу
        """
        return mapGetRstRedBand_GraphicFile_t (_hmap, _number)

    mapGetRstGreenBand_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstGreenBand_GraphicFile', maptype.HMAP, ctypes.c_long)
    def mapGetRstGreenBand_GraphicFile(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить номер канала графического файла с номером  number, отображаемого зеленым
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile, что для растра с номером number осуществляется прямой доступ к графическому файлу
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstGreenBand_GraphicFile_t (_hmap, _number)

    mapGetRstBlueBand_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBlueBand_GraphicFile', maptype.HMAP, ctypes.c_long)
    def mapGetRstBlueBand_GraphicFile(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить номер канала графического файла с номером  number, отображаемого синим
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile, что для растра с номером number осуществляется прямой доступ к графическому файлу
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRstBlueBand_GraphicFile_t (_hmap, _number)

    mapSetRstRedBand_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstRedBand_GraphicFile', maptype.HMAP, ctypes.c_long, ctypes.c_int)
    def mapSetRstRedBand_GraphicFile(_hmap: maptype.HMAP, _number: int, _redband: int) -> int:
        """
        Установить номер канала графического файла с номером number, отображаемого красным
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _redband: номер канала графического файла
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если установить -1, то такой канал не используется
           Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
           что для растра с номером number осуществляется прямой доступ к графическому файлу
        """
        return mapSetRstRedBand_GraphicFile_t (_hmap, _number, _redband)

    mapSetRstGreenBand_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstGreenBand_GraphicFile', maptype.HMAP, ctypes.c_long, ctypes.c_int)
    def mapSetRstGreenBand_GraphicFile(_hmap: maptype.HMAP, _number: int, _greenband: int) -> int:
        """
        Установить номер канала графического файла с номером  number, отображаемого зеленым
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _greenband: номер канала графического файла
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если установить -1, то такой канал не используется
           Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
           что для растра с номером number осуществляется прямой доступ к графическому файлу
        """
        return mapSetRstGreenBand_GraphicFile_t (_hmap, _number, _greenband)

    mapSetRstBlueBand_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstBlueBand_GraphicFile', maptype.HMAP, ctypes.c_long, ctypes.c_int)
    def mapSetRstBlueBand_GraphicFile(_hmap: maptype.HMAP, _number: int, _blueband: int) -> int:
        """
        Установить номер канала графического файла с номером  number, отображаемого синим
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _blueband: номер канала графического файла
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если установить -1, то такой канал не используется
           Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile,
           что для растра с номером number осуществляется прямой доступ к графическому файлу
        """
        return mapSetRstBlueBand_GraphicFile_t (_hmap, _number, _blueband)

    mapSetRstVegIndex_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstVegIndex_GraphicFile', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.VEGINDEX))
    def mapSetRstVegIndex_GraphicFile(_hmap: maptype.HMAP, _number: int, _vegindex: ctypes.POINTER(maptype.VEGINDEX)) -> int:
        """
        Установить параметры отображения мультиспектрального растра по вегетационному индексу
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _vegindex: параметры отображения Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile, что для растра с номером number осуществляется прямой доступ к графическому файлу Функция справедлива для мультиспектральных изображений (mapGetRstBandCount_GraphicFile() >``= 3``)
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapSetRstVegIndex_GraphicFile_t (_hmap, _number, _vegindex)

    mapGetRstVegIndex_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstVegIndex_GraphicFile', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.VEGINDEX))
    def mapGetRstVegIndex_GraphicFile(_hmap: maptype.HMAP, _number: int, _vegindex: ctypes.POINTER(maptype.VEGINDEX)) -> int:
        """
        Запросить параметры отображения мультиспектрального растра по вегетационному индексу
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _vegindex: возвращаемые параметры отображения Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile, что для растра с номером number осуществляется прямой доступ к графическому файлу Функция справедлива для мультиспектральных изображений (mapGetRstBandCount_GraphicFile() >``= 3``)
        
        :returns: Возвращает параметры отображения вегетационного индекса Если отображение по вегетационному индексу не установлено возвращает 0 При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstVegIndex_GraphicFile_t (_hmap, _number, _vegindex)

    mapGetRstBandPixel_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBandPixel_GraphicFile', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapGetRstBandPixel_GraphicFile(_hmap: maptype.HMAP, _number: int, _x: int, _y: int, _bandnum: int, _color: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить яркость пиксела изображения на канал
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _x: координата пикселя в системе координат растра в пикселях
        
        :param _y: координата пикселя в системе координат растра в пикселях
        
        :param _bandnum: номер канала (от ``0`` до mapGetRstBandCount_GraphicFile - ``1``)
        
        :param _color: возвращаемое значение реально записанное в растре, может быть ``1``,``4``,``8``,``16`` бит Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile, что для растра с номером number осуществляется прямой доступ к графическому файлу
        
        :returns: Возвращает яркость пиксела изображения на канал bandnum При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstBandPixel_GraphicFile_t (_hmap, _number, _x, _y, _bandnum, _color)

    mapSetRstPaintCellRadius_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstPaintCellRadius_GraphicFile', ctypes.c_long)
    def mapSetRstPaintCellRadius_GraphicFile(_radius: int) -> int:
        """
        Установить радиус клетки
        
        :param _radius: устанавливаемый радиус клетки в пикселях (не может быть меньше ``0``)
        
        :returns: При ошибке возвращает 0
        :rtype: int
        
        .. note::

           Если равен 0, то все пикселы вычисляются по строгим формулам
           Значение по умолчанию 3
           Устанавливает радиус клетки в узлах которой пересчет координат выполняется
           по строгим формулам при отрисовке растра в системе координат, отличной от
           системы координат растра
           Между узлами пересчет координат выполняется линейной интерполяцией. Коэффициенты
           линейного пересчета внутри клетки вычисляются по двум верхним узлам клетки
           При увеличении радиуса увеличивается скорость отрисовки, но ухудшается качество
           изображения при значительной деформации системы координат отрисовки относительно
           системы координат растра (изображение сегментируется по размеру клетки)
           Этот параметр является глобальным, т.е. с момента установки все растры
           отрисовываются с использованием этого параметра
        """
        return mapSetRstPaintCellRadius_GraphicFile_t (_radius)

    mapGetRstPaintCellRadius_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstPaintCellRadius_GraphicFile')
    def mapGetRstPaintCellRadius_GraphicFile() -> int:
        """
        Запросить радиус клетки
        
        :returns: Возвращает радиус клетки в узлах которой пересчет координат выполняется по строгим формулам при отрисовке растра в системе координат, отличной от системы координат растра При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstPaintCellRadius_GraphicFile_t ()

    mapGetRstBitInBand_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBitInBand_GraphicFile', maptype.HMAP, ctypes.c_long)
    def mapGetRstBitInBand_GraphicFile(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить глубину цвета на канал
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile, что для растра с номером number осуществляется прямой доступ к графическому файлу
        
        :returns: Возвращает глубину цвета на канал (1, 4, 8, 16) При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstBitInBand_GraphicFile_t (_hmap, _number)

    mapGetRstHistogram_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstHistogram_GraphicFile', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.DWORD))
    def mapGetRstHistogram_GraphicFile(_hmap: maptype.HMAP, _number: int, _count: int, _histogram: ctypes.POINTER(maptype.DWORD)) -> int:
        """
        Запросить гистограмму
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _count: количество элементов в массиве histogram количество элементов вычисляется по формуле count = BandCount ``*`` (``1`` << BitInBand) для палитровых растров BandCount ``= 1`` для ``1`` битных растров (палитровых) count ``= 2`` для ``4`` битных растров (палитровых) count ``= 16`` для ``8`` битных растров (палитровых) count ``= 256`` для ``RGB``                           count = ``3 *`` ``256`` ``= 768`` для ``8``  битных мультиспектральных  count = BandCount ``* 256`` для ``16`` битных мультиспектральных  count = BandCount ``* 65536``
        
        :param _histogram: возвращаемая гистограмма Гистограмма - поканальный массив количества пикселей, присутствующих в растре Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile, что для растра с номером number осуществляется прямой доступ к графическому файлу
        
        :returns: Возвращает гистограмму При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstHistogram_GraphicFile_t (_hmap, _number, _count, _histogram)

    mapGetRstLookupTable_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstLookupTable_GraphicFile', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_byte), ctypes.c_long)
    def mapGetRstLookupTable_GraphicFile(_hmap: maptype.HMAP, _number: int, _bandnum: int, _table: ctypes.POINTER(ctypes.c_byte), _tablesize: int) -> int:
        """
        Запросить таблицу преобразования цвета
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _bandnum: номер канала (от ``0`` до mapGetRstBandCount_GraphicFile - ``1``)
        
        :param _table: возвращаемая таблица преобразования
        
        :param _tablesize: размер таблицы table (для ``8`` бит должно быть ``256``, для ``16`` бит - ``65536``) Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile, что для растра с номером number осуществляется прямой доступ к графическому файлу
        
        :returns: Возвращает таблицу преобразования цвета для отображения панхроматических, RGB и мультиспектральных растров с глубиной цвета 8 или 16 бит При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstLookupTable_GraphicFile_t (_hmap, _number, _bandnum, _table, _tablesize)

    mapSetRstLookupTable_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRstLookupTable_GraphicFile', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_byte), ctypes.c_long)
    def mapSetRstLookupTable_GraphicFile(_hmap: maptype.HMAP, _number: int, _bandnum: int, _table: ctypes.POINTER(ctypes.c_byte), _tablesize: int) -> int:
        """
        Установить таблицу преобразования цвета
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _bandnum: номер канала (от ``0`` до mapGetRstBandCount_GraphicFile - ``1``)
        
        :param _table: таблица преобразования
        
        :param _tablesize: размер таблицы table (для ``8`` бит должно быть не меньше ``256``, для ``16`` бит - не меньше ``65536``) Устанавливает таблицу преобразования цвета для отображения панхроматических, ``RGB`` и мультиспектральных растров с глубиной цвета ``8`` или ``16`` бит Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile, что для растра с номером number осуществляется прямой доступ к графическому файлу
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapSetRstLookupTable_GraphicFile_t (_hmap, _number, _bandnum, _table, _tablesize)

    mapGetRstBlockWidth_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBlockWidth_GraphicFile', maptype.HMAP, ctypes.c_long)
    def mapGetRstBlockWidth_GraphicFile(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить ширину блока в пикселях
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile, что для растра с номером number осуществляется прямой доступ к графическому файлу
        
        :returns: Возвращает ширину блока в пикселях При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstBlockWidth_GraphicFile_t (_hmap, _number)

    mapGetRstBlockHeight_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBlockHeight_GraphicFile', maptype.HMAP, ctypes.c_long)
    def mapGetRstBlockHeight_GraphicFile(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить высоту блока в пикселях
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile, что для растра с номером number осуществляется прямой доступ к графическому файлу
        
        :returns: Возвращает высоту блока в пикселях При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstBlockHeight_GraphicFile_t (_hmap, _number)

    mapGetRstBlockPixelType_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBlockPixelType_GraphicFile', maptype.HMAP, ctypes.c_long)
    def mapGetRstBlockPixelType_GraphicFile(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить способ расположения цветовых составляющих пикселя в блоке
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile, что для растра с номером number осуществляется прямой доступ к графическому файлу
        
        :returns: Возвращает способ расположения цветовых составляющих пикселя в блоке Возвращаемые значения: ``0`` - ошибка выполнения ``1`` - последовательно RGB RGB ... ``2`` - по цветовым плоскостям  RRR... GGG... BBB...
        :rtype: int
        """
        return mapGetRstBlockPixelType_GraphicFile_t (_hmap, _number)

    mapGetRstBlockRowCount_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBlockRowCount_GraphicFile', maptype.HMAP, ctypes.c_long)
    def mapGetRstBlockRowCount_GraphicFile(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить количество строк блоков
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile, что для растра с номером number осуществляется прямой доступ к графическому файлу
        
        :returns: Возвращает количество строк блоков При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstBlockRowCount_GraphicFile_t (_hmap, _number)

    mapGetRstBlockColCount_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBlockColCount_GraphicFile', maptype.HMAP, ctypes.c_long)
    def mapGetRstBlockColCount_GraphicFile(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить количество столбцов блоков
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile, что для растра с номером number осуществляется прямой доступ к графическому файлу
        
        :returns: Возвращает количество столбцов блоков При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstBlockColCount_GraphicFile_t (_hmap, _number)

    mapGetRstBlockSize_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBlockSize_GraphicFile', maptype.HMAP, ctypes.c_long)
    def mapGetRstBlockSize_GraphicFile(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить размер блока в байтах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке Для ``1`` и ``4`` битных растров в блок записывается ``1`` байт на пиксель Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile, что для растра с номером number осуществляется прямой доступ к графическому файлу
        
        :returns: Возвращает размер блока в байтах При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstBlockSize_GraphicFile_t (_hmap, _number)

    mapGetRstBlock_GraphicFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRstBlock_GraphicFile', maptype.HMAP, ctypes.c_long, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    def mapGetRstBlock_GraphicFile(_hmap: maptype.HMAP, _number: int, _blockrow: int, _blockcol: int, _buf: ctypes.c_char_p, _bufsize: int) -> int:
        """
        Прочитать блок из растра
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _blockrow: номер строки блоков
        
        :param _blockcol: номер столбца блоков
        
        :param _buf: буфер, в который записывается изображение блока bifsize  - размер блока, должен быть равен mapGetRstBlockSize_GraphicFile Для ``1`` и ``4`` битных растров в блок записывается ``1`` байт на пиксель Перед вызовом необходимо убедиться, используя функцию mapRstIsAccessGraphicFile, что для растра с номером number осуществляется прямой доступ к графическому файлу
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRstBlock_GraphicFile_t (_hmap, _number, _blockrow, _blockcol, _buf, _bufsize)

    mapIsGraphicFileOpenWithoutConvertUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsGraphicFileOpenWithoutConvertUn', maptype.PWCHAR)
    def mapIsGraphicFileOpenWithoutConvertUn(_name: mapsyst.WTEXT) -> int:
        """
        Проверить графический файл на возможность открытия без преобразования в формат RSW
        
        :param _name: имя файла
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsGraphicFileOpenWithoutConvertUn_t (_name.buffer())

    mapGetRmfDataFiles_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapGetRmfDataFiles', maptype.PWCHAR, ctypes.POINTER(ctypes.c_long))
    def mapGetRmfDataFiles(_name: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_long)) -> ctypes.c_void_p:
        """
        Запросить список файлов данных, относящихся к растру/матрице
        
        :param _name: имя файла данных формата RSW, MTW или MTQ
        
        :param _error: указатель на поле для записи кода ошибки (описаны в maperr.rh)
        
        :returns: Если файл данных один - возвращает ноль Если список файлов сформирован - возвращает идентификатор списка, который нужно освободить после чтения списка - mapFreeRmfDataFiles При ошибке возвращает ноль
        """
        return mapGetRmfDataFiles_t (_name.buffer(), _error)

    mapGetRmfDataFilesCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRmfDataFilesCount', ctypes.c_void_p)
    def mapGetRmfDataFilesCount(_handle: ctypes.c_void_p) -> int:
        """
        Запросить число элементов списка файлов данных, относящихся к растру/матрице
        
        :param _handle: идентификатор списка, полученный в функции mapGetRmfDataFiles
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRmfDataFilesCount_t (_handle)

    mapGetRmfDataFilesItem_t = mapsyst.GetProcAddress(acceslib,maptype.PWCHAR,'mapGetRmfDataFilesItem', ctypes.c_void_p, ctypes.c_long)
    def mapGetRmfDataFilesItem(_handle: ctypes.c_void_p, _number: int) -> mapsyst.WTEXT:
        """
        Запросить элемент списка файлов данных, относящихся к растру или матрице
        
        :param _handle: идентификатор списка, полученный в функции mapGetRmfDataFiles
        
        :param _number: номер элемента в списке с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: mapsyst.WTEXT
        """
        return mapGetRmfDataFilesItem_t (_handle, _number)

    mapFreeRmfDataFiles_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeRmfDataFiles', ctypes.c_void_p)
    def mapFreeRmfDataFiles(_handle: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Освободить память под список файлов данных, относящихся к растру или матрице
        
        :param _handle: идентификатор списка, полученный в функции mapGetRmfDataFiles
        """
        return mapFreeRmfDataFiles_t (_handle)

    mapCreateOutputFileName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateOutputFileName', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def mapCreateOutputFileName(_hmap: maptype.HMAP, _inputfilename: mapsyst.WTEXT, _postfix: mapsyst.WTEXT, _ext: mapsyst.WTEXT, _outputname: mapsyst.WTEXT, _sizeoutputname: int) -> int:
        """
        Сформировать имя выходного файла растровых данных
        
        :param _inputfilename: имя исходного файла RSW
        
        :param _postfix: добавляемый суффикс к имени файла
        
        :param _ext: расширение выходного файла
        
        :param _outputname: указатель для размещения имени выходного файла
        
        :param _sizeoutputname: размер выходного файла
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCreateOutputFileName_t (_hmap, _inputfilename.buffer(), _postfix.buffer(), _ext.buffer(), _outputname.buffer(), _sizeoutputname)

    mapGenerateLogFileName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGenerateLogFileName', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapGenerateLogFileName(_outputfilename: mapsyst.WTEXT, _logfilename: mapsyst.WTEXT, _size: int, _flagcreatedir: int) -> int:
        """
        Сформировать имя лог-файла по имени выходного растра
        
        :param _outputfilename: имя выходного файла RSW
        
        :param _logfilename: указатель для размещения имени лог-файла
        
        :param _size: размер памяти по указателю logfilename
        
        :param _flagcreatedir: флаг создания папки LOG Функция по имени выходного растра outputfilename формирует в папке LOG имя лог-файла
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если flagcreatedir равен 1, то в папке выходного растра создается папка LOG
        """
        return mapGenerateLogFileName_t (_outputfilename.buffer(), _logfilename.buffer(), _size, _flagcreatedir)



def rstapi_healthcheck():
    return 1
