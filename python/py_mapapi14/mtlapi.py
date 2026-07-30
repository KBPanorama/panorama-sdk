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
    *            Описание функций доступа к матрице слоев              *
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
class BUILDMTL(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("StructSize",ctypes.c_uint),
                ("MtwNumber",ctypes.c_int),
                ("BeginX",ctypes.c_double),
                ("BeginY",ctypes.c_double),
                ("EndX",ctypes.c_double),
                ("EndY",ctypes.c_double),
                ("ElemSizeMeters",ctypes.c_double),
                ("LayerCount",ctypes.c_int),
                ("LayerForm",ctypes.c_int),
                ("HeightSizeBytes",ctypes.c_int),
                ("LayerSizeBytes",ctypes.c_int),
                ("HeightMeasure",ctypes.c_int),
                ("LayerMeasure",ctypes.c_int),
                ("UserType",ctypes.c_int),
                ("Scale",ctypes.c_int),
                ("BlockSide",ctypes.c_int),
                ("CodeCount",ctypes.c_int),
                ("MtdPointFormat",ctypes.c_int),
                ("BigFormat",ctypes.c_int),
                ("Reserve",ctypes.c_char*(64))]
#-----------------------------


#-----------------------------
class MTLDESCRIBEUN(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Name",maptype.WCHAR1*(2048)),
                ("MaterialFileName",maptype.WCHAR1*(2048)),
                ("FrameMeters",maptype.DFRAME),
                ("ElementInPlane",ctypes.c_double),
                ("MinHeightValue",ctypes.c_double),
                ("MaxHeightValue",ctypes.c_double),
                ("BotLevelHeight",ctypes.c_double),
                ("MaxSummaryPower",ctypes.c_double),
                ("LayerCount",ctypes.c_int),
                ("MaterialCount",ctypes.c_int),
                ("UserType",ctypes.c_int),
                ("View",ctypes.c_int),
                ("UserLabel",ctypes.c_int),
                ("ReliefPresence",ctypes.c_int),
                ("Reserve",ctypes.c_char*(64))]
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
    mapOpenMtlUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapOpenMtlUn', maptype.PWCHAR, ctypes.c_long)
    def mapOpenMtlUn(_mtrname: mapsyst.WTEXT, _mode: int) -> maptype.HMAP:
        """
        Открыть матричные данные
        
        :param _mtrname: имя открываемого файла
        
        :param _mode: режим чтения/записи (``GENERIC_READ``, ``GENERIC_WRITE`` или ``0``) ``GENERIC_READ`` - все данные только на чтение
        
        :returns: Возвращает идентификатор открытой матричной карты При ошибке возвращает ноль
        :rtype: maptype.HMAP
        """
        return mapOpenMtlUn_t (_mtrname.buffer(), _mode)

    mapOpenMtlForMapUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapOpenMtlForMapUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapOpenMtlForMapUn(_hmap: maptype.HMAP, _mtrname: mapsyst.WTEXT, _mode: int) -> int:
        """
        Открыть матричные данные в заданном районе работ, добавить в цепочку матриц
        
        :param _hmap: идентификатор открытых данных
        
        :param _mtrname: имя открываемого файла
        
        :param _mode: режим чтения/записи (``GENERIC_READ``, ``GENERIC_WRITE`` или ``0``) ``GENERIC_READ`` - все данные только на чтение
        
        :returns: Возвращает номер файла в цепочке матриц При ошибке возвращает ноль
        :rtype: int
        """
        return mapOpenMtlForMapUn_t (_hmap, _mtrname.buffer(), _mode)

    mapCloseMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseMtl', maptype.HMAP, ctypes.c_long)
    def mapCloseMtl(_hmap: maptype.HMAP, _number: int) -> ctypes.c_void_p:
        """
        Закрыть матричные данные
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер закрываемой матрицы в цепочке матриц
        
        .. note::

           Если number ``= 0``, закрываются все матричные данные
        """
        return mapCloseMtl_t (_hmap, _number)

    mapCloseMtlForMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCloseMtlForMap', maptype.HMAP, ctypes.c_long)
    def mapCloseMtlForMap(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Закрыть матричные данные в заданном районе работ
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матричного файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если number ``= 0``, закрываются все матричные данные
        """
        return mapCloseMtlForMap_t (_hmap, _number)

    mapBuildMtlUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBuildMtlUn', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(BUILDMTL), maptype.HSELECT, maptype.HMESSAGE)
    def mapBuildMtlUn(_hmap: maptype.HMAP, _mtrname: mapsyst.WTEXT, _ininame: mapsyst.WTEXT, _mtrparm: ctypes.POINTER(BUILDMTL), _hselect: maptype.HSELECT, _handle: maptype.HMESSAGE) -> int:
        """
        Построить матрицу на заданный участок района работ
        
        :param _hmap: идентификатор исходной карты для построения матрицы
        
        :param _mtrname: полное имя файла создаваемой матрицы
        
        :param _ininame: полное имя файла легенды создаваемой матрицы
        
        :param _mtrparm: параметры создаваемой матрицы, структурa ``BUILDMTL`` описанa в mtlapi.h
        
        :param _hselect: идентификатор контекста отбора объектов карты
        
        :param _handle: идентификатор окна диалога, которому посылаются сообщения о ходе процесса: ``0x0378`` - сообщение о проценте выполненных работ (в ``WPARAM``) если процесс должен быть принудительно завершен, в ответ должно вернуться значение ``0x0378`` если handle равно нулю - сообщения не посылаются
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapBuildMtlUn_t (_hmap, _mtrname.buffer(), _ininame.buffer(), _mtrparm, _hselect, _handle)

    mapGetMtlDescribeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlDescribeUn', maptype.HMAP, ctypes.c_long, ctypes.POINTER(MTLDESCRIBEUN))
    def mapGetMtlDescribeUn(_hmap: maptype.HMAP, _number: int, _describe: ctypes.POINTER(MTLDESCRIBEUN)) -> int:
        """
        Запросить описание файла матричных данных
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _describe: адрес структуры, в которой будет размещено описание матрицы Структурa ``MTLDESCRIBEUN`` описанa в mtlapi.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlDescribeUn_t (_hmap, _number, _describe)

    mapGetMtlNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlNameUn', maptype.HMAP, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetMtlNameUn(_hmap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить имя файла матричных данных
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _name: адрес строки для размещения результата
        
        :param _size: размер строки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlNameUn_t (_hmap, _number, _name.buffer(), _size)

    mapGetMtlCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlCount', maptype.HMAP)
    def mapGetMtlCount(_hmap: maptype.HMAP) -> int:
        """
        Запросить число открытых файлов матричных данных
        
        :param _hmap: идентификатор открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlCount_t (_hmap)

    mapGetMtlNumberByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlNumberByNameUn', maptype.HMAP, maptype.PWCHAR)
    def mapGetMtlNumberByNameUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT) -> int:
        """
        Запросить номер матрицы в цепочке по имени файла
        
        :param _hmap: идентификатор открытых данных
        
        :param _name: имя файла матрицы В цепочке номера матриц начинаются с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlNumberByNameUn_t (_hmap, _name.buffer())

    mapGetMaxLayerCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMaxLayerCount', maptype.HMAP)
    def mapGetMaxLayerCount(_hmap: maptype.HMAP) -> int:
        """
        Запросить максимальное количество слоев всех матриц MTL-цепочки
        
        :param _hmap: идентификатор открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMaxLayerCount_t (_hmap)

    mapGetLayerCountOfMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetLayerCountOfMtl', maptype.HMAP, ctypes.c_long)
    def mapGetLayerCountOfMtl(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить количество слоев матрицы с номером number в цепочке
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetLayerCountOfMtl_t (_hmap, _number)

    mapGetMinBotLevelHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetMinBotLevelHeight', maptype.HMAP)
    def mapGetMinBotLevelHeight(_hmap: maptype.HMAP) -> float:
        """
        Запросить минимальную высоту нижнего уровня
        
        :param _hmap: идентификатор открытых данных
        
        :returns: При ошибке возвращает ERRORHEIGHT
        :rtype: float
        """
        return mapGetMinBotLevelHeight_t (_hmap)

    mapGetMaxSummaryPower_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetMaxSummaryPower', maptype.HMAP)
    def mapGetMaxSummaryPower(_hmap: maptype.HMAP) -> float:
        """
        Запросить максимальную суммарную мощность слоев
        
        :param _hmap: идентификатор открытых данных
        
        :returns: При ошибке возвращает ERRORPOWER
        :rtype: float
        """
        return mapGetMaxSummaryPower_t (_hmap)

    mapGetElementHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetElementHeight', maptype.HMAP, ctypes.c_double, ctypes.c_double)
    def mapGetElementHeight(_hmap: maptype.HMAP, _x: float, _y: float) -> float:
        """
        Запросить значение абсолютной высоты в заданной точке
        
        :param _hmap: идентификатор открытых данных
        
        :param _x: координата X точки, задаётся в метрах в системе координат векторной карты
        
        :param _y: координата Y точки, задаётся в метрах в системе координат векторной карты
        
        :returns: Возвращает значение высоты в метрах В случае ошибки при выборе высоты и в случае необеспеченности заданной точки матричными данными возвращает ERRORHEIGHT
        :rtype: float
        """
        return mapGetElementHeight_t (_hmap, _x, _y)

    mapGetElementHeightOfMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetElementHeightOfMtl', maptype.HMAP, ctypes.c_long, ctypes.c_double, ctypes.c_double)
    def mapGetElementHeightOfMtl(_hmap: maptype.HMAP, _number: int, _x: float, _y: float) -> float:
        """
        Запросить значение абсолютной высоты в заданной точке из матрицы с номером number в цепочке
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _x: координата X точки, задаётся в метрах в системе координат векторной карты
        
        :param _y: координата Y точки, задаётся в метрах в системе координат векторной карты
        
        :returns: Возвращает значение высоты в метрах В случае ошибки при выборе высоты и в случае необеспеченности заданной точки матричными данными возвращает ERRORHEIGHT
        :rtype: float
        """
        return mapGetElementHeightOfMtl_t (_hmap, _number, _x, _y)

    mapGetElementPower_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetElementPower', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapGetElementPower(_hmap: maptype.HMAP, _x: float, _y: float, _layernumber: int) -> float:
        """
        Запросить значение мощности слоя в заданной точке
        
        :param _hmap: идентификатор открытых данных
        
        :param _x: координата X точки, задаётся в метрах в системе координат векторной карты
        
        :param _y: координата Y точки, задаётся в метрах в системе координат векторной карты
        
        :param _layernumber: номер слоя
        
        :returns: Возвращает значение мощности слоя в метрах В случае ошибки и в случае необеспеченности заданной точки матричными данными возвращает ERRORPOWER
        :rtype: float
        """
        return mapGetElementPower_t (_hmap, _x, _y, _layernumber)

    mapGetElementPowerOfMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetElementPowerOfMtl', maptype.HMAP, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapGetElementPowerOfMtl(_hmap: maptype.HMAP, _number: int, _x: float, _y: float, _layernumber: int) -> float:
        """
        Запросить значение мощности слоя в заданной точке из матрицы с номером number в цепочке
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _x: координата X точки, задаётся в метрах в системе координат векторной карты
        
        :param _y: координата Y точки, задаётся в метрах в системе координат векторной карты
        
        :param _layernumber: номер слоя
        
        :returns: Возвращает значение мощности слоя в метрах В случае ошибки и в случае необеспеченности заданной точки матричными данными возвращает ERRORPOWER
        :rtype: float
        """
        return mapGetElementPowerOfMtl_t (_hmap, _number, _x, _y, _layernumber)

    mapGetElementPowersTriangleOfMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetElementPowersTriangleOfMtl', maptype.HMAP, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.c_long)
    def mapGetElementPowersTriangleOfMtl(_hmap: maptype.HMAP, _number: int, _x: float, _y: float, _powers: ctypes.POINTER(ctypes.c_double), _count: int) -> int:
        """
        Вычислить значения мощностей слоев в заданной точке методом треугольников по матрице с номером number
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _x: координата X точки, задаётся в метрах в системе координат векторной карты
        
        :param _y: координата Y точки, задаётся в метрах в системе координат векторной карты
        
        :param _powers: адрес массива для записи вычисленных значений мощностей (в метрах)
        
        :param _count: размер массива, должен быть не менее mapGetLayerCountOfMtl()
        
        :returns: Возвращает количество заполненных элементов массива powers При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetElementPowersTriangleOfMtl_t (_hmap, _number, _x, _y, _powers, _count)

    mapGetElementPowerTriangleOfMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetElementPowerTriangleOfMtl', maptype.HMAP, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapGetElementPowerTriangleOfMtl(_hmap: maptype.HMAP, _number: int, _x: float, _y: float, _layernumber: int) -> float:
        """
        Вычислить значение мощности слоя в заданной точке методом треугольников по матрице с номером number
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _x: координата X точки, задаётся в метрах в системе координат векторной карты
        
        :param _y: координата Y точки, задаётся в метрах в системе координат векторной карты
        
        :param _layernumber: номер слоя
        
        :returns: Возвращает значение мощности слоя в метрах При ошибке возвращает ERRORPOWER
        :rtype: float
        """
        return mapGetElementPowerTriangleOfMtl_t (_hmap, _number, _x, _y, _layernumber)

    mapPutElementHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPutElementHeight', maptype.HMAP, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    def mapPutElementHeight(_hmap: maptype.HMAP, _number: int, _x: float, _y: float, _h: float) -> int:
        """
        Установить значение абсолютной высоты в элемент матрицы, соответствующий заданной точке
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _x: координата X точки, задаётся в метрах в системе координат векторной карты
        
        :param _y: координата Y точки, задаётся в метрах в системе координат векторной карты
        
        :param _h: высота, задаётся в метрах в системе координат векторной карты
        
        :returns: В случае ошибки возвращает ноль
        :rtype: int
        """
        return mapPutElementHeight_t (_hmap, _number, _x, _y, _h)

    mapPutElementPower_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPutElementPower', maptype.HMAP, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapPutElementPower(_hmap: maptype.HMAP, _number: int, _x: float, _y: float, _power: float, _layernumber: int) -> int:
        """
        Установить значение мощности слоя layernumber в элемент, соответствующий заданной точке
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _x: координата X точки, задаётся в метрах в системе координат векторной карты
        
        :param _y: координата Y точки, задаётся в метрах в системе координат векторной карты
        
        :param _power: мощность, задаётся в метрах в системе координат векторной карты
        
        :param _layernumber: номер слоя
        
        :returns: В случае ошибки возвращает ноль
        :rtype: int
        """
        return mapPutElementPower_t (_hmap, _number, _x, _y, _power, _layernumber)

    mapGetMtlNumberInPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlNumberInPoint', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapGetMtlNumberInPoint(_hmap: maptype.HMAP, _x: float, _y: float, _number: int) -> int:
        """
        Запросить номер в цепочке для матрицы, расположенной в заданной точке
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: порядковый номер, найденной матрицы в точке (``1`` - первая в данной точке, ``2`` - вторая ...)
        
        :returns: В случае ошибки возвращает ноль
        :rtype: int
        """
        return mapGetMtlNumberInPoint_t (_hmap, _x, _y, _number)

    mapGetMtlNumberLastVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlNumberLastVisible', maptype.HMAP)
    def mapGetMtlNumberLastVisible(_hmap: maptype.HMAP) -> int:
        """
        Запросить номер в цепочке последней открытой матрицы с установленным в 1 признаком видимости
        
        :param _hmap: идентификатор открытых данных
        
        :returns: В случае ошибки возвращает ноль
        :rtype: int
        """
        return mapGetMtlNumberLastVisible_t (_hmap)

    mapGetMtlBlockSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlBlockSize', maptype.HMAP, ctypes.c_long)
    def mapGetMtlBlockSize(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить размер полного блока матрицы в байтах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlBlockSize_t (_hmap, _number)

    mapGetMtlBlockSide_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlBlockSide', maptype.HMAP, ctypes.c_long)
    def mapGetMtlBlockSide(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить вертикальный размер блока матрицы в элементах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlBlockSide_t (_hmap, _number)

    mapGetMtlBlockAddress_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetMtlBlockAddress', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapGetMtlBlockAddress(_hmap: maptype.HMAP, _number: int, _row: int, _column: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить адрес блока матрицы по номеру строки и столбца
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке При запросе следующего блока может вернуть прежний адрес Блоки последнего ряда могут иметь усеченный размер
        
        :returns: Возвращает адрес считанного блока При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetMtlBlockAddress_t (_hmap, _number, _row, _column)

    mapGetMtlBlockRow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlBlockRow', maptype.HMAP, ctypes.c_long)
    def mapGetMtlBlockRow(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить число строк блоков матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlBlockRow_t (_hmap, _number)

    mapGetMtlBlockColumn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlBlockColumn', maptype.HMAP, ctypes.c_long)
    def mapGetMtlBlockColumn(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить число столбцов блоков матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlBlockColumn_t (_hmap, _number)

    mapGetMtlElementRow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlElementRow', maptype.HMAP, ctypes.c_long)
    def mapGetMtlElementRow(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить число строк элементов в матрице
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlElementRow_t (_hmap, _number)

    mapGetMtlElementColumn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlElementColumn', maptype.HMAP, ctypes.c_long)
    def mapGetMtlElementColumn(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить число столбцов элементов в матрице
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlElementColumn_t (_hmap, _number)

    mapGetHeightArrayFromMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetHeightArrayFromMtl', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetHeightArrayFromMtl(_hmap: maptype.HMAP, _heightarray: ctypes.POINTER(ctypes.c_double), _heightcount: int, _firstpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _secondpoint: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Запросить массив значений абсолютных высот, соответствующих логическим элементам, лежащим на заданном отрезке
        
        :param _hmap: идентификатор открытых данных
        
        :param _heightarray: адрес массива высот
        
        :param _heightcount: количество высот
        
        :param _firstpoint: координаты точки (начало отрезка), задаются в метрах в системе координат векторной карты
        
        :param _secondpoint: координаты точки (конец отрезка), задаются в метрах в системе координат векторной карты Размер массива высот, заданного адресом heightarray, должен соответствовать запрашиваемому количеству высот (heightcount), в противном случае возможны ошибки работы с памятью В случае необеспеченности логического элемента матричными данными его значение равно ``ERRORHEIGHT`` (``-111111.0`` м)
        
        :returns: В случае ошибки при выборе высот возвращает ноль
        :rtype: int
        """
        return mapGetHeightArrayFromMtl_t (_hmap, _heightarray, _heightcount, _firstpoint, _secondpoint)

    mapGetLayerColor_t = mapsyst.GetProcAddress(acceslib,maptype.COLORREF,'mapGetLayerColor', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapGetLayerColor(_hmap: maptype.HMAP, _number: int, _layernumber: int) -> maptype.COLORREF:
        """
        Запросить значение цвета слоя layernumber
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _layernumber: номер слоя
        
        :returns: В случае ошибки возвращает ноль
        :rtype: maptype.COLORREF
        """
        return mapGetLayerColor_t (_hmap, _number, _layernumber)

    mapSetLayerColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetLayerColor', maptype.HMAP, ctypes.c_long, ctypes.c_long, maptype.COLORREF)
    def mapSetLayerColor(_hmap: maptype.HMAP, _number: int, _layernumber: int, _layercolor: maptype.COLORREF) -> int:
        """
        Установить значение цвета слоя layernumber
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _layernumber: номер слоя
        
        :param _layercolor: цвет слоя
        
        :returns: В случае ошибки возвращает ноль
        :rtype: int
        """
        return mapSetLayerColor_t (_hmap, _number, _layernumber, _layercolor)

    mapGetLayerShortName_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetLayerShortName', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapGetLayerShortName(_hmap: maptype.HMAP, _number: int, _layernumber: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить короткое имя слоя layernumber
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _layernumber: номер слоя
        
        :returns: В случае ошибки возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetLayerShortName_t (_hmap, _number, _layernumber)

    mapSetLayerShortName_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapSetLayerShortName', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_char_p)
    def mapSetLayerShortName(_hmap: maptype.HMAP, _number: int, _layernumber: int, _layername: ctypes.c_char_p) -> ctypes.POINTER(ctypes.c_char):
        """
        Установить короткое имя слоя layernumber
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _layernumber: номер слоя
        
        :param _layername: короткое имя
        
        :returns: В случае ошибки возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapSetLayerShortName_t (_hmap, _number, _layernumber, _layername)

    mapGetLayerLongNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapGetLayerLongNameUn', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapGetLayerLongNameUn(_hmap: maptype.HMAP, _number: int, _layernumber: int) -> ctypes.POINTER(maptype.WCHAR):
        """
        Запросить имя слоя layernumber
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _layernumber: номер слоя
        
        :returns: В случае ошибки возвращает ноль
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapGetLayerLongNameUn_t (_hmap, _number, _layernumber)

    mapSetLayerLongNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapSetLayerLongNameUn', maptype.HMAP, ctypes.c_long, ctypes.c_long, maptype.PWCHAR)
    def mapSetLayerLongNameUn(_hmap: maptype.HMAP, _number: int, _layernumber: int, _layername: mapsyst.WTEXT) -> ctypes.POINTER(maptype.WCHAR):
        """
        Установить имя слоя layernumber
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _layernumber: номер слоя
        
        :param _layername: название слоя
        
        :returns: В случае ошибки возвращает ноль
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapSetLayerLongNameUn_t (_hmap, _number, _layernumber, _layername.buffer())

    mapGetMaxLayerHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMaxLayerHeight', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapGetMaxLayerHeight(_hmap: maptype.HMAP, _number: int, _layernumber: int) -> int:
        """
        Запросить максимальную мощность слоя в метрах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _layernumber: номер слоя
        
        :returns: В случае ошибки возвращает ноль
        :rtype: int
        """
        return mapGetMaxLayerHeight_t (_hmap, _number, _layernumber)

    mapSetMaxLayerHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMaxLayerHeight', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSetMaxLayerHeight(_hmap: maptype.HMAP, _number: int, _layernumber: int, _maxlayerheight: int) -> int:
        """
        Установить максимальную мощность слоя в метрах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _layernumber: номер слоя
        
        :returns: В случае ошибки возвращает ноль.
        :rtype: int
        """
        return mapSetMaxLayerHeight_t (_hmap, _number, _layernumber, _maxlayerheight)

    mapGetMtlProjectionData_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlProjectionData', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.MTRPROJECTIONDATA))
    def mapGetMtlProjectionData(_hmap: maptype.HMAP, _number: int, _projectiondata: ctypes.POINTER(maptype.MTRPROJECTIONDATA)) -> int:
        """
        Запросить данные о проекции матричных данных
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _projectiondata: адрес структуры, в которой будут размещены данные о проекции Структурa ``MTRPROJECTIONDATA`` описанa в maptype.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlProjectionData_t (_hmap, _number, _projectiondata)

    mapCreateMtlUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateMtlUn', maptype.PWCHAR, ctypes.POINTER(BUILDMTL))
    def mapCreateMtlUn(_mtrname: mapsyst.WTEXT, _mtrparm: ctypes.POINTER(BUILDMTL)) -> maptype.HMAP:
        """
        Создать матричную карту
        
        :param _mtrname: полное имя файла матрицы
        
        :param _mtrparm: параметры создаваемой матрицы Структурa ``BUILDMTL`` описанa в mtlapi.h
        
        :returns: Возвращает идентификатор открытой матричной карты При ошибке возвращает ноль
        :rtype: maptype.HMAP
        """
        return mapCreateMtlUn_t (_mtrname.buffer(), _mtrparm)

    mapCreateAndAppendMtlUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateAndAppendMtlUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(BUILDMTL), ctypes.POINTER(maptype.MTRPROJECTIONDATA))
    def mapCreateAndAppendMtlUn(_hmap: maptype.HMAP, _mtrname: mapsyst.WTEXT, _mtrparm: ctypes.POINTER(BUILDMTL), _mtrprojectiondata: ctypes.POINTER(maptype.MTRPROJECTIONDATA)) -> int:
        """
        Создать файл матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _mtrname: полное имя файла матрицы
        
        :param _mtrparm: параметры создаваемой матрицы
        
        :param _mtrprojectiondata: параметры проекции создаваемой матрицы Структурa ``BUILDMTL`` описанa в mtlapi.h Структурa ``MTRPROJECTIONDATA`` описанa в maptype.h
        
        :returns: Возвращает номер файла в цепочке матриц При ошибке возвращает ноль
        :rtype: int
        """
        return mapCreateAndAppendMtlUn_t (_hmap, _mtrname.buffer(), _mtrparm, _mtrprojectiondata)

    mapSaveMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSaveMtl', maptype.HMAP, ctypes.c_long)
    def mapSaveMtl(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Записать изменения матрицы в файл
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSaveMtl_t (_hmap, _number)

    mapSetMtlShowRange_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtlShowRange', maptype.HMAP, ctypes.c_long, ctypes.c_double, ctypes.c_double)
    def mapSetMtlShowRange(_hmap: maptype.HMAP, _number: int, _minvalue: float, _maxvalue: float) -> int:
        """
        Установить диапазон отображаемых элементов матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _minvalue: минимальное значение отображаемого элемента в единицах матрицы
        
        :param _maxvalue: максимальное значение отображаемого элемента в единицах матрицы
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapSetMtlShowRange_t (_hmap, _number, _minvalue, _maxvalue)

    mapSetMtlBotLevel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtlBotLevel', maptype.HMAP, ctypes.c_long, ctypes.c_double)
    def mapSetMtlBotLevel(_hmap: maptype.HMAP, _number: int, _botlevel: float) -> int:
        """
        Установить нижний уровень слоев матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _botlevel: нижний уровень слоев в метрах
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapSetMtlBotLevel_t (_hmap, _number, _botlevel)

    mapSetMtlMaxSummaryPower_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtlMaxSummaryPower', maptype.HMAP, ctypes.c_long, ctypes.c_double)
    def mapSetMtlMaxSummaryPower(_hmap: maptype.HMAP, _number: int, _maxsummarypower: float) -> int:
        """
        Установить максимальную суммарную мощность слоев матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _maxsummarypower: максимальная суммарная мощность в метрах
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapSetMtlMaxSummaryPower_t (_hmap, _number, _maxsummarypower)

    mapSetMtlProjectionDataPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtlProjectionDataPro', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_long, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapSetMtlProjectionDataPro(_hmap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        """
        Установить данные о проекции матричных данных
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _mapregister: адрес структуры, содержащей данные о проекции
        
        :param _datumparam: адрес структуры, в которой будут размещены коэффициенты трансформирования геодезических координат
        
        :param _ellipsoidparam: адрес структуры, в которой будут размещены параметры эллипсоида
        
        :param _ttype: тип локального преобразования координат (``TRANSFORMTYPE`` в mapcreat.h) или ``0``
        
        :param _tparm: параметры локального преобразования координат Структуры ``MAPREGISTEREX``, ``DATUMPARAM``, ``ELLIPSOIDPARAM``, ``LOCALTRANSFORM`` описаны в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtlProjectionDataPro_t (_hmap, _number, _mapregister, _datumparam, _ellipsoidparam, _ttype, _tparm)

    mapGetMtlProjectionDataPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlProjectionDataPro', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapGetMtlProjectionDataPro(_hmap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: ctypes.POINTER(ctypes.c_long), _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        """
        Запросить данные о проекции матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _mapregister: адрес структуры, в которой будут размещены данные о проекции
        
        :param _datumparam: адрес структуры, в которой будут размещены коэффициенты трансформирования геодезических координат
        
        :param _ellipsoidparam: адрес структуры, в которой будут размещены параметры эллипсоида
        
        :param _ttype: тип локального преобразования координат (``TRANSFORMTYPE`` в mapcreat.h) или ``0``
        
        :param _tparm: параметры локального преобразования координат Структуры ``MAPREGISTEREX``, ``DATUMPARAM``, ``ELLIPSOIDPARAM``, ``LOCALTRANSFORM`` описаны в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlProjectionDataPro_t (_hmap, _number, _mapregister, _datumparam, _ellipsoidparam, _ttype, _tparm)

    mapIsMtlGeoSupported_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsMtlGeoSupported', maptype.HMAP, ctypes.c_long)
    def mapIsMtlGeoSupported(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить - поддерживается ли пересчет к геодезическим координатам из плоских прямоугольных и обратно
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Если нет - возвращает ноль
        :rtype: int
        """
        return mapIsMtlGeoSupported_t (_hmap, _number)

    mapGetMtlEllipsoidParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlEllipsoidParam', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapGetMtlEllipsoidParam(_hmap: maptype.HMAP, _number: int, _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        """
        Запросить параметры эллипсоида матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла матрицы в цепочке
        
        :param _ellipsoidparam: адрес структуры, в которой будут размещены параметры эллипсоида Структурa ``ELLIPSOIDPARAM`` описанa в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlEllipsoidParam_t (_hmap, _number, _ellipsoidparam)

    mapSetMtlEllipsoidParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtlEllipsoidParam', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapSetMtlEllipsoidParam(_hmap: maptype.HMAP, _number: int, _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        """
        Установить параметры эллипсоида матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла матрицы в цепочке
        
        :param _ellipsoidparam: адрес структуры, содержащей параметры эллипсоида Структурa ``ELLIPSOIDPARAM`` описанa в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtlEllipsoidParam_t (_hmap, _number, _ellipsoidparam)

    mapGetMtlDatumParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlDatumParam', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapGetMtlDatumParam(_hmap: maptype.HMAP, _number: int, _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        """
        Запросить коэффициенты трансформирования геодезических координат матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла матрицы в цепочке
        
        :param _datumparam: адрес структуры, в которой будут размещены коэффициенты трансформирования геодезических координат Структурa ``DATUMPARAM`` описанa в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlDatumParam_t (_hmap, _number, _datumparam)

    mapSetMtlDatumParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtlDatumParam', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapSetMtlDatumParam(_hmap: maptype.HMAP, _number: int, _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        """
        Установить коэффициенты трансформирования геодезических координат матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла матрицы в цепочке.
        
        :param _datumparam: адрес структуры, содержащей коэффициенты трансформирования геодезических координат Структурa ``DATUMPARAM`` описанa в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtlDatumParam_t (_hmap, _number, _datumparam)

    mapSetMtlBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtlBorder', maptype.HMAP, ctypes.c_long, maptype.HOBJ)
    def mapSetMtlBorder(_hmap: maptype.HMAP, _number: int, _hobj: maptype.HOBJ) -> int:
        """
        Установить рамку матрицы по метрике замкнутого объекта
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _number: номер файла в цепочке
        
        :param _hobj: замкнутый объект карты Замкнутый объект должен иметь не менее ``4``-х точек
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           После выполнения функции отображение матрицы ограничится заданной областью
        """
        return mapSetMtlBorder_t (_hmap, _number, _hobj)

    mapSetMtlBorderEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtlBorderEx', maptype.HMAP, ctypes.c_long, maptype.HOBJ, ctypes.c_long)
    def mapSetMtlBorderEx(_hmap: maptype.HMAP, _number: int, _hobj: maptype.HOBJ, _flagsubject: int) -> int:
        """
        Установить рамку матрицы по метрике замкнутого объекта
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _hobj: замкнутый объект карты
        
        :param _flagsubject: флаг использования подобъектов объекта при установке рамки растра: ``0`` - в качестве рамки устанавливается контур объекта ``1`` - в качестве рамки устанавливается контур объекта с подобъектами Замкнутый объект должен иметь не менее ``4``-х точек
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           После выполнения функции отображение матрицы ограничится заданной областью
        """
        return mapSetMtlBorderEx_t (_hmap, _number, _hobj, _flagsubject)

    mapGetMtlBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlBorder', maptype.HMAP, ctypes.c_long, maptype.HOBJ)
    def mapGetMtlBorder(_hmap: maptype.HMAP, _number: int, _hobj: maptype.HOBJ) -> int:
        """
        Запросить объект рамки матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlBorder_t (_hmap, _number, _hobj)

    mapDeleteMtlBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteMtlBorder', maptype.HMAP, ctypes.c_long)
    def mapDeleteMtlBorder(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Удалить рамку матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           После выполнения функции отображение матрицы будет полным
        """
        return mapDeleteMtlBorder_t (_hmap, _number)

    mapCheckExistenceMtlBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckExistenceMtlBorder', maptype.HMAP, ctypes.c_long)
    def mapCheckExistenceMtlBorder(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Определить существование рамки матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :returns: Если рамка матрицы существует возвращает 1, иначе возвращает 0
        :rtype: int
        """
        return mapCheckExistenceMtlBorder_t (_hmap, _number)

    mapCheckShowMtlByBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckShowMtlByBorder', maptype.HMAP, ctypes.c_long)
    def mapCheckShowMtlByBorder(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Определить способ отображения матрицы относительно рамки
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :returns: Возвращает: ``1`` - при отображении матрицы по рамке ``0`` - при отображении матрицы без учета рамки При ошибке возвращает -1
        :rtype: int
        """
        return mapCheckShowMtlByBorder_t (_hmap, _number)

    mapShowMtlByBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapShowMtlByBorder', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapShowMtlByBorder(_hmap: maptype.HMAP, _number: int, _value: int) -> int:
        """
        Установить отображение матрицы по рамке
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _value: ``1`` - отобразить матрицу по рамке ``0`` - отобразить матрицу без учета рамки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapShowMtlByBorder_t (_hmap, _number, _value)

    mapGetImmediatePointOfMtlBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetImmediatePointOfMtlBorder', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetImmediatePointOfMtlBorder(_hmap: maptype.HMAP, _number: int, _pointin: ctypes.POINTER(maptype.DOUBLEPOINT), _pointout: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Определить координаты и порядковый номер точки рамки ближайшей к pointin
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _pointin: координаты точки в метрах
        
        :param _pointout: адрес для записи координат найденной точки в метрах Найденная точка входит в прямоугольник габариты матрицы и имеет наименьшее удаление от точки pointin
        
        :returns: При ошибке или отсутствии рамки возвращает ноль
        :rtype: int
        """
        return mapGetImmediatePointOfMtlBorder_t (_hmap, _number, _pointin, _pointout)

    mapWhereSouthWestMtlPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapWhereSouthWestMtlPlane', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapWhereSouthWestMtlPlane(_hmap: maptype.HMAP, _number: int, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить координаты юго-западного угла матрицы в метрах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _x: адрес для записи координаты X найденной точки в метрах
        
        :param _y: адрес для записи координаты Y найденной точки в метрах
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapWhereSouthWestMtlPlane_t (_hmap, _number, _x, _y)

    mapGetActualMtlFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetActualMtlFrame', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.c_long)
    def mapGetActualMtlFrame(_hmap: maptype.HMAP, _frame: ctypes.POINTER(maptype.DFRAME), _number: int) -> int:
        """
        Запросить фактические габариты отображаемой матрицы в метрах в районе работ
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _frame: возвращаемые габариты матрицы При отображение матрицы по рамке возвращаются габариты рамки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetActualMtlFrame_t (_hmap, _frame, _number)

    mapGetMtlScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlScale', maptype.HMAP, ctypes.c_long)
    def mapGetMtlScale(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить масштаб матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlScale_t (_hmap, _number)

    mapGetMtlRangeScaleVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlRangeScaleVisible', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapGetMtlRangeScaleVisible(_hmap: maptype.HMAP, _number: int, _bottomscale: ctypes.POINTER(ctypes.c_long), _topscale: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить значения масштаба нижней и верхней границ видимости матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _bottomscale: адрес для записи знаменателя масштаба нижней границы видимости матрицы
        
        :param _topscale: адрес для записи знаменателя масштаба верхней границы видимости матрицы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlRangeScaleVisible_t (_hmap, _number, _bottomscale, _topscale)

    mapSetMtlRangeScaleVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtlRangeScaleVisible', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSetMtlRangeScaleVisible(_hmap: maptype.HMAP, _number: int, _bottomscale: int, _topscale: int) -> int:
        """
        Установить значения масштаба нижней и верхней границ видимости матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _bottomscale: знаменатель масштаба нижней границы видимости матрицы
        
        :param _topscale: знаменатель масштаба верхней границы видимости матрицы
        
        :returns: при невыполнении условия bottomscale <= topscale возвращает ноль При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtlRangeScaleVisible_t (_hmap, _number, _bottomscale, _topscale)

    mapGetActiveMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetActiveMtl', maptype.HMAP)
    def mapGetActiveMtl(_hmap: maptype.HMAP) -> int:
        """
        Запросить активную матрицу
        
        :param _hmap: идентификатор открытых данных Устанавливается приложением по своему усмотрению
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetActiveMtl_t (_hmap)

    mapSetActiveMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetActiveMtl', maptype.HMAP, ctypes.c_long)
    def mapSetActiveMtl(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Установить активную матрицу
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке Устанавливается приложением по своему усмотрению
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetActiveMtl_t (_hmap, _number)

    mapIsOpenMtl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsOpenMtl', maptype.HMAP, ctypes.c_long)
    def mapIsOpenMtl(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить открыта ли матрица с номером number
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Функция возвращает признак открытия указанной матрицы в документе - (1/0) При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsOpenMtl_t (_hmap, _number)

    mapGetMtlEdit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlEdit', maptype.HMAP, ctypes.c_long)
    def mapGetMtlEdit(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить флаг редактируемости матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlEdit_t (_hmap, _number)

    mapGetMtlFileSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlFileSize', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_int64))
    def mapGetMtlFileSize(_hmap: maptype.HMAP, _number: int, _filesize: ctypes.POINTER(ctypes.c_int64)) -> int:
        """
        Запросить размер файла
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _filesize: адрес для записи размера файла
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlFileSize_t (_hmap, _number, _filesize)

    mapGetMtlWidthInElement_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlWidthInElement', maptype.HMAP, ctypes.c_long)
    def mapGetMtlWidthInElement(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить ширину матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Возвращает ширину матрицы в элементах При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlWidthInElement_t (_hmap, _number)

    mapGetMtlHeightInElement_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlHeightInElement', maptype.HMAP, ctypes.c_long)
    def mapGetMtlHeightInElement(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить высоту матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Возвращает высоту матрицы в элементах При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlHeightInElement_t (_hmap, _number)

    mapGetMtlAccuracy_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetMtlAccuracy', maptype.HMAP, ctypes.c_long)
    def mapGetMtlAccuracy(_hmap: maptype.HMAP, _number: int) -> float:
        """
        Запросить точность матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Возвращает точность матрицы в метрах на элемент При ошибке возвращает ноль
        :rtype: float
        """
        return mapGetMtlAccuracy_t (_hmap, _number)

    mapGetMtlFlagLocationChanged_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlFlagLocationChanged', maptype.HMAP, ctypes.c_long)
    def mapGetMtlFlagLocationChanged(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить флаг изменения привязки матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlFlagLocationChanged_t (_hmap, _number)

    mapGetMtlLocation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlLocation', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetMtlLocation(_hmap: maptype.HMAP, _number: int, _location: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Запросить привязку матрицы в метрах в районе работ
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _location: координаты юго-западного угла матрицы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlLocation_t (_hmap, _number, _location)

    mapSetMtlLocation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtlLocation', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSetMtlLocation(_hmap: maptype.HMAP, _number: int, _location: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Установить привязку матрицы в метрах в районе работ
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _location: координаты юго-западного угла матрицы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtlLocation_t (_hmap, _number, _location)

    mapGetMtlCopyFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlCopyFlag', maptype.HMAP, ctypes.c_long)
    def mapGetMtlCopyFlag(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить - может ли матрица копироваться или экспортироваться
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlCopyFlag_t (_hmap, _number)

    mapGetMtlPrintFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlPrintFlag', maptype.HMAP, ctypes.c_long)
    def mapGetMtlPrintFlag(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить - может ли матрица выводиться на печать
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц Для данных, открытых на ГИС Сервере, может устанавливаться запрет вывода изображения на печать
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlPrintFlag_t (_hmap, _number)

    mapGetMtlMeasure_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlMeasure', maptype.HMAP, ctypes.c_long)
    def mapGetMtlMeasure(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить единицу измерения значений высот матрицы с номером number в цепочке
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц Возвращаемые значения: ``0``-метры, ``1``-дециметры, ``2``-сантиметры, ``3``-миллиметры
        
        :returns: При ошибке возвращает -1
        :rtype: int
        """
        return mapGetMtlMeasure_t (_hmap, _number)

    mapGetMtlLayerMeasure_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlLayerMeasure', maptype.HMAP, ctypes.c_long)
    def mapGetMtlLayerMeasure(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить единицу измерения мощности слоя матрицы с номером number в цепочке
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц Возвращаемые значения: ``0``-метры, ``1``-дециметры, ``2``-сантиметры, ``3``-миллиметры
        
        :returns: При ошибке возвращает -1
        :rtype: int
        """
        return mapGetMtlLayerMeasure_t (_hmap, _number)

    mapGetMtlView_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlView', maptype.HMAP, ctypes.c_long)
    def mapGetMtlView(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить степень видимости матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :returns: Возвращает: ``0`` - нет видимости, ``1`` - полная видимость, ``2`` - насыщенная ``3`` - полупрозрачная, ``4`` - средняя, ``5`` - прозрачная При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtlView_t (_hmap, _number)

    mapSetMtlView_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtlView', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetMtlView(_hmap: maptype.HMAP, _number: int, _view: int) -> int:
        """
        Установить степень видимости матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _view: степень видимости матрицы: ``0`` - нет видимости ``1`` - полная видимость ``2`` - насыщенная ``3`` - полупрозрачная ``4`` - средняя ``5`` - прозрачная
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtlView_t (_hmap, _number, _view)

    mapSetMtlViewOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtlViewOrder', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetMtlViewOrder(_hmap: maptype.HMAP, _number: int, _order: int) -> int:
        """
        Установить порядок отображения матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _order: порядок отображения: ``0`` - под картой, ``1`` - над картой
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapSetMtlViewOrder_t (_hmap, _number, _order)

    mapGetMtlViewOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlViewOrder', maptype.HMAP, ctypes.c_long)
    def mapGetMtlViewOrder(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить порядок отображения матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :returns: Возвращает: ``0`` - под картой, ``1`` - над картой При ошибке возвращает 0
        :rtype: int
        """
        return mapGetMtlViewOrder_t (_hmap, _number)

    mapChangeOrderMtlShow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapChangeOrderMtlShow', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapChangeOrderMtlShow(_hmap: maptype.HMAP, _oldnumber: int, _newnumber: int) -> int:
        """
        Поменять очередность отображения матриц слоев в цепочке
        
        :param _hmap: идентификатор открытых данных
        
        :param _oldnumber: номер файла в цепочке
        
        :param _newnumber: устанавливаемый номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapChangeOrderMtlShow_t (_hmap, _oldnumber, _newnumber)

    mapGetMtlTransparent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtlTransparent', maptype.HMAP, ctypes.c_long)
    def mapGetMtlTransparent(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить прозрачность палитры матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Возвращает степень прозрачности в процентах от 0 до 100
        :rtype: int
        """
        return mapGetMtlTransparent_t (_hmap, _number)

    mapSetMtlTransparent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtlTransparent', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetMtlTransparent(_hmap: maptype.HMAP, _number: int, _transparent: int) -> int:
        """
        Установить прозрачность палитры матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _transparent: прозрачность в процентах от ``0`` до ``100``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtlTransparent_t (_hmap, _number, _transparent)

    mapCreateMtl3D_t = mapsyst.GetProcAddress(acceslib,maptype.HMTL3D,'mapCreateMtl3D', maptype.HMAP)
    def mapCreateMtl3D(_hmap: maptype.HMAP) -> maptype.HMTL3D:
        """
        Создать объект отображения матрицы слоев в 3D
        
        :param _hmap: идентификатор открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HMTL3D
        """
        return mapCreateMtl3D_t (_hmap)

    mapDeleteMtl3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapDeleteMtl3D', maptype.HMTL3D)
    def mapDeleteMtl3D(_hmtl3d: maptype.HMTL3D) -> ctypes.c_void_p:
        """
        Удалить объект отображения матрицы слоев в 3D
        
        :param _hmtl3d: идентификатор объекта отображения
        """
        return mapDeleteMtl3D_t (_hmtl3d)

    mapPaintMtl3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPaintMtl3D', maptype.HMTL3D, maptype.HDC, ctypes.POINTER(maptype.MTL3DVIEWUN))
    def mapPaintMtl3D(_hmtl3d: maptype.HMTL3D, _hdc: maptype.HDC, _parm: ctypes.POINTER(maptype.MTL3DVIEWUN)) -> int:
        """
        Отобразить матрицу слоев в 3D
        
        :param _hmtl3d: идентификатор объекта отображения
        
        :param _hdc: контекст отображения
        
        :param _parm: параметры 3D-отображения матриц (описаны в maptype.h)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPaintMtl3D_t (_hmtl3d, _hdc, _parm)



def mtlapi_healthcheck():
    return 1
