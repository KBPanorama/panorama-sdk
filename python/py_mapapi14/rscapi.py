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
    *       Описание функций доступа к объекту "Классификатор карт"    *
    *        Интерфейс для программ на языках C, PASCAL, BASIC         *
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
    mapGetRscIdent_t = mapsyst.GetProcAddress(acceslib,maptype.HRSC,'mapGetRscIdent', maptype.HMAP, maptype.HSITE)
    def mapGetRscIdent(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> maptype.HRSC:
        """
        Запросить идентификатор классификатора карты
        
        :param _hmap: идентификатор открытой карты
        
        :param _hsite: идентификатор открытой пользовательской карты
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HRSC
        """
        return mapGetRscIdent_t (_hmap, _hsite)

    mapGetRscFileNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscFileNameUn', maptype.HRSC, maptype.PWCHAR, ctypes.c_long)
    def mapGetRscFileNameUn(_hrsc: maptype.HRSC, _target: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить имя файла классификатора
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _target: строка для размещения полного имени файла
        
        :param _size: размер строки в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscFileNameUn_t (_hrsc, _target.buffer(), _size)

    mapGetRscNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscNameUn', maptype.HRSC, maptype.PWCHAR, ctypes.c_long)
    def mapGetRscNameUn(_hrsc: maptype.HRSC, _rscname: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить имя файла классификатора
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _rscname: строка для размещения имени файла и расширения без пути
        
        :param _size: размер строки в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscNameUn_t (_hrsc, _rscname.buffer(), _size)

    mapGetRscUserName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscUserName', maptype.HRSC, ctypes.c_char_p, ctypes.c_long)
    def mapGetRscUserName(_hrsc: maptype.HRSC, _name: ctypes.c_char_p, _size: int) -> int:
        """
        Запросить условное название классификатора
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _name: строка для размещения условного названия классификатора
        
        :param _size: размер строки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscUserName_t (_hrsc, _name, _size)

    mapSetRscUserName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscUserName', maptype.HRSC, ctypes.c_char_p)
    def mapSetRscUserName(_hrsc: maptype.HRSC, _name: ctypes.c_char_p) -> int:
        """
        Установить условное название классификатора
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _name: условное название классификатора
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscUserName_t (_hrsc, _name)

    mapGetRscDescriptionUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscDescriptionUn', maptype.HRSC, maptype.PWCHAR, ctypes.c_long)
    def mapGetRscDescriptionUn(_hrsc: maptype.HRSC, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить описание классификатора
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _name: строка для размещения условного названия классификатора
        
        :param _size: размер строки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscDescriptionUn_t (_hrsc, _name.buffer(), _size)

    mapSetRscDescriptionUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscDescriptionUn', maptype.HRSC, maptype.PWCHAR)
    def mapSetRscDescriptionUn(_hrsc: maptype.HRSC, _str: mapsyst.WTEXT) -> int:
        """
        Установить описание классификатора
        
        :param _hrsc: идентификатор классификатора карты,
        
        :param _str: описание классификатора
        """
        return mapSetRscDescriptionUn_t (_hrsc, _str.buffer())

    mapGetRscTypeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscTypeUn', maptype.HRSC, maptype.PWCHAR, ctypes.c_long)
    def mapGetRscTypeUn(_hrsc: maptype.HRSC, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить тип классификатора
        
        :param _hrsc: идентификатор классификатора карты,
        
        :param _name: строка для размещения условного названия классификатора
        
        :param _size: размер строки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscTypeUn_t (_hrsc, _name.buffer(), _size)

    mapSetRscTypeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscTypeUn', maptype.HRSC, maptype.PWCHAR)
    def mapSetRscTypeUn(_hrsc: maptype.HRSC, _str: mapsyst.WTEXT) -> int:
        """
        Установить тип классификатора
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _str: тип классификатора
        """
        return mapSetRscTypeUn_t (_hrsc, _str.buffer())

    mapGetRscCorrectDate_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetRscCorrectDate', maptype.HRSC)
    def mapGetRscCorrectDate(_hrsc: maptype.HRSC) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить дату последнего изменения классификатора в формате YYYYMMDD
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает пустую строку
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetRscCorrectDate_t (_hrsc)

    mapGetRscUpdateDateTime_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetRscUpdateDateTime', maptype.HRSC, ctypes.c_char_p, ctypes.c_int)
    def mapGetRscUpdateDateTime(_hrsc: maptype.HRSC, _datetime: ctypes.c_char_p, _size: int) -> int:
        """
        Запросить дату и время последнего изменения классификатора в локальном времени с часовым поясом
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _datetime: строка-буфер для заполнения даты-времени
        
        :param _size: размер строки для заполнения Формат даты и времени:  ``DD``/``MM``/``YYYY`` ``HH``:``MM``:``SS`` +N
        
        :returns: При ошибке возвращает 0 и пустую строку datetimestr
        :rtype: int
        """
        return mapGetRscUpdateDateTime_t (_hrsc, _datetime, _size)

    mapGetRscComputerNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscComputerNameUn', maptype.HRSC, maptype.PWCHAR, ctypes.c_long)
    def mapGetRscComputerNameUn(_hrsc: maptype.HRSC, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить имя компьютера, с которого делали последние изменения
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _name: строка для размещения типа классификатора
        
        :param _size: размер строки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscComputerNameUn_t (_hrsc, _name.buffer(), _size)

    mapGetRscError_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscError', maptype.HRSC)
    def mapGetRscError(_hrsc: maptype.HRSC) -> int:
        """
        Запросить код ошибки последней операции с классификатором карты
        
        :param _hrsc: идентификатор классификатора карты Коды ошибок перечислены в maperr.rh
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscError_t (_hrsc)

    mapGetRscMode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscMode', maptype.HRSC)
    def mapGetRscMode(_hrsc: maptype.HRSC) -> int:
        """
        Запросить номер любых изменений классификатора карты
        
        :param _hrsc: идентификатор классификатора карты Пример любых изменений классификатора карты: параметры условных знаков, названия характеристик При изменении флага внутренние коды объектов сохраняются
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscMode_t (_hrsc)

    mapGetRscModify_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscModify', maptype.HRSC)
    def mapGetRscModify(_hrsc: maptype.HRSC) -> int:
        """
        Запросить наличие изменений классификатора карты, которые еще не сохранены в файле
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: Возвращает: ``0`` - изменений нет, ``1`` - классификатор изменен
        :rtype: int
        """
        return mapGetRscModify_t (_hrsc)

    mapGetRscStyle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscStyle', maptype.HRSC)
    def mapGetRscStyle(_hrsc: maptype.HRSC) -> int:
        """
        Запросить номер структурных изменений - стиля классификатора карты
        
        :param _hrsc: идентификатор классификатора карты Пример структурных изменений: изменения кодов/ключей объектов При изменении стиля могут измениться внутренние коды объектов - требуется перекодировка объектов карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscStyle_t (_hrsc)

    mapGetRscIsWrite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscIsWrite', maptype.HRSC)
    def mapGetRscIsWrite(_hrsc: maptype.HRSC) -> int:
        """
        Запросить возможность редактирования классификатора карты
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: Если классификатор открыт только для чтения, то возвращает ноль
        :rtype: int
        """
        return mapGetRscIsWrite_t (_hrsc)

    mapGetRscIsLocalPlace_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscIsLocalPlace', maptype.HRSC)
    def mapGetRscIsLocalPlace(_hrsc: maptype.HRSC) -> int:
        """
        Запросить локально ли размещен классификатор
        
        :returns: Если классификатор открыт на ГИС Сервере, то возвращает ноль
        :rtype: int
        """
        return mapGetRscIsLocalPlace_t (_hrsc)

    mapGetRscScaleTableNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscScaleTableNumber', maptype.HRSC)
    def mapGetRscScaleTableNumber(_hrsc: maptype.HRSC) -> int:
        """
        Запросить номера таблицы масштабов
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: Возвращает номер таблицы масштабов с ``1`` - общий список масштабов ``2`` - таблица масштабов для крупномасштабных карт
        :rtype: int
        """
        return mapGetRscScaleTableNumber_t (_hrsc)

    mapSetRscScaleTableNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscScaleTableNumber', maptype.HRSC, ctypes.c_long)
    def mapSetRscScaleTableNumber(_hrsc: maptype.HRSC, _number: int) -> int:
        """
        Установить номер таблицы масштабов
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер таблицы масштабов: ``1`` - таблица с общим списком масштабов ``2`` - таблица масштабов для крупномасштабных карт
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscScaleTableNumber_t (_hrsc, _number)

    mapGetRscScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscScale', maptype.HRSC)
    def mapGetRscScale(_hrsc: maptype.HRSC) -> int:
        """
        Запросить масштаб карты для классификатора
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscScale_t (_hrsc)

    mapSetRscScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscScale', maptype.HRSC, ctypes.c_long)
    def mapSetRscScale(_hrsc: maptype.HRSC, _scale: int) -> int:
        """
        Установить масштаб карты для классификатора
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _scale: знаменатель масштаба
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscScale_t (_hrsc, _scale)

    mapGetRscDate_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetRscDate', maptype.HRSC)
    def mapGetRscDate(_hrsc: maptype.HRSC) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить дату создания файла классификатора
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: Возвращает дату в виде ГГГГММДД
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetRscDate_t (_hrsc)

    mapGetRscClassificatorCode_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetRscClassificatorCode', maptype.HRSC)
    def mapGetRscClassificatorCode(_hrsc: maptype.HRSC) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить код классификатора
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetRscClassificatorCode_t (_hrsc)

    mapSetRscClassificatorCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscClassificatorCode', maptype.HRSC, ctypes.c_char_p)
    def mapSetRscClassificatorCode(_hrsc: maptype.HRSC, _code: ctypes.c_char_p) -> int:
        """
        Установить код классификатора
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код классификатора ``7`` символов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscClassificatorCode_t (_hrsc, _code)

    mapGetRscObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectCount', maptype.HRSC)
    def mapGetRscObjectCount(_hrsc: maptype.HRSC) -> int:
        """
        Запросить число объектов описанных в классификаторе
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectCount_t (_hrsc)

    mapGetRscObjectCountInLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectCountInLayer', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectCountInLayer(_hrsc: maptype.HRSC, _layer: int) -> int:
        """
        Запросить число объектов описанных в классификаторе в заданном слое
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectCountInLayer_t (_hrsc, _layer)

    mapGetRscObjectNameInLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetRscObjectNameInLayer', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapGetRscObjectNameInLayer(_hrsc: maptype.HRSC, _layer: int, _number: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить название объекта по порядковому номеру в заданном слое
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :param _number: номер объекта в слое
        
        :returns: При ошибке возвращает ноль или пустую строку
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetRscObjectNameInLayer_t (_hrsc, _layer, _number)

    mapGetRscObjectNameInLayerUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectNameInLayerUn', maptype.HRSC, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetRscObjectNameInLayerUn(_hrsc: maptype.HRSC, _layer: int, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить название объекта по порядковому номеру в заданном слое
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :param _number: номер объекта в слое
        
        :param _name: адрес строки для размещения результата
        
        :param _size: размер строки (не меньше ``32`` байт)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectNameInLayerUn_t (_hrsc, _layer, _number, _name.buffer(), _size)

    mapGetRscObjectExcodeInLayerPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_ulong,'mapGetRscObjectExcodeInLayerPro', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapGetRscObjectExcodeInLayerPro(_hrsc: maptype.HRSC, _layer: int, _number: int) -> int:
        """
        Запросить классификационный код объекта по порядковому номеру в заданном слое
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :param _number: номер объекта в слое
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectExcodeInLayerPro_t (_hrsc, _layer, _number)

    mapGetRscObjectLocalInLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectLocalInLayer', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapGetRscObjectLocalInLayer(_hrsc: maptype.HRSC, _layer: int, _number: int) -> int:
        """
        Запросить код локализации объекта по порядковому номеру в заданном слое
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :param _number: номер объекта в слое
        
        :returns: При ошибке возвращает ноль (ноль допустим)
        :rtype: int
        """
        return mapGetRscObjectLocalInLayer_t (_hrsc, _layer, _number)

    mapGetRscObjectCodeInLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectCodeInLayer', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapGetRscObjectCodeInLayer(_hrsc: maptype.HRSC, _layer: int, _number: int) -> int:
        """
        Запросить внутренний код (порядковый номер) объекта по порядковому номеру в заданном слое
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :param _number: номер объекта в слое
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectCodeInLayer_t (_hrsc, _layer, _number)

    mapGetRscScaleCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscScaleCount', maptype.HRSC)
    def mapGetRscScaleCount(_hrsc: maptype.HRSC) -> int:
        """
        Запросить размер текущей таблицы масштабов классификатора
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscScaleCount_t (_hrsc)

    mapGetRscScaleItem_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscScaleItem', maptype.HRSC, ctypes.c_long)
    def mapGetRscScaleItem(_hrsc: maptype.HRSC, _number: int) -> int:
        """
        Запросить значение из текущей таблицы масштабов классификатора по порядковому номеру
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: порядковый номер с ``1``
        
        :returns: Возвращает знаменатель масштаба из текущей таблицы масштабов классификатора При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscScaleItem_t (_hrsc, _number)

    mapSetRscExampleScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscExampleScale', maptype.HRSC, ctypes.c_long)
    def mapSetRscExampleScale(_hrsc: maptype.HRSC, _scale: int) -> int:
        """
        Установить процент масштаба отображения знака в окнах - примерах
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _scale: масштаб отображения в ``%`` от ``10`` до ``100`` уменьшение, более ``100`` увеличение
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscExampleScale_t (_hrsc, _scale)

    mapGetRscExampleScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscExampleScale', maptype.HRSC)
    def mapGetRscExampleScale(_hrsc: maptype.HRSC) -> int:
        """
        Запросить процент масштаба отображения знака в окнах - примерах
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: Возвращает масштаб отображения в %: от 10 до 100 уменьшение, более 100 увеличение При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscExampleScale_t (_hrsc)

    mapGetRscSeekObjectCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSeekObjectCode', maptype.HRSC, ctypes.c_long, ctypes.c_long, ctypes.c_char_p)
    def mapGetRscSeekObjectCode(_hrsc: maptype.HRSC, _oldnumber: int, _seektype: int, _example: ctypes.c_char_p) -> int:
        """
        Найти объект классификатора
        
        :param _oldnumber: номер объекта при предыдущем поиске, ``0`` - поиск с первого
        
        :param _seektype: условия поиска  ``SEEK_RSCOBJECT`` (maptype.h)
        
        :param _example: шаблон для поиска
        
        :returns: Возвращает порядковый номер объекта или 0, если такого нет
        :rtype: int
        """
        return mapGetRscSeekObjectCode_t (_hrsc, _oldnumber, _seektype, _example)

    mapGetP3DNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetP3DNameUn', maptype.HRSC, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetP3DNameUn(_hrsc: maptype.HRSC, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить полное имя P3D файла по коду библиотеки по порядковому номеру
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _name: строка для размещения полного (с путем) имени файла
        
        :param _size: размер строки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetP3DNameUn_t (_hrsc, _number, _name.buffer(), _size)

    mapCreateRscUn_t = mapsyst.GetProcAddress(acceslib,maptype.HRSC,'mapCreateRscUn', maptype.PWCHAR, ctypes.POINTER(maptype.RSCCREATEUN), ctypes.POINTER(maptype.PALETTE256))
    def mapCreateRscUn(_name: mapsyst.WTEXT, _rsccreate: ctypes.POINTER(maptype.RSCCREATEUN), _palette: ctypes.POINTER(maptype.PALETTE256)) -> maptype.HRSC:
        """
        Создать классификатор векторной карты
        
        :param _name: полный путь к файлу создаваемого классификатора
        
        :param _rsccreate: входные данные
        
        :param _palette: при необходимости задается палитра, не более ``32`` цветов Структуры ``RSCCREATEUN``, ``PALETTE256`` описаны в maptype.h
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HRSC
        """
        return mapCreateRscUn_t (_name.buffer(), _rsccreate, _palette)

    mapCreateKeyObjectRsc_t = mapsyst.GetProcAddress(acceslib,maptype.HRSC,'mapCreateKeyObjectRsc', ctypes.c_char_p, ctypes.POINTER(maptype.RSCCREATE), ctypes.POINTER(maptype.PALETTE256))
    def mapCreateKeyObjectRsc(_name: ctypes.c_char_p, _rsccreate: ctypes.POINTER(maptype.RSCCREATE), _palette: ctypes.POINTER(maptype.PALETTE256)) -> maptype.HRSC:
        """
        Создать классификатор векторной карты c идентификацией кодов объекта по ключу - короткому имени объекта
        
        :param _name: имя создаваемого файла классификатора
        
        :param _rsccreate: входные данные
        
        :param _palette: при необходимости задается палитра, не более ``32`` цветов Структуры ``RSCCREATEUN``, ``PALETTE256`` описаны в maptype.h
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HRSC
        """
        return mapCreateKeyObjectRsc_t (_name, _rsccreate, _palette)

    mapCreateRscFromXsdEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateRscFromXsdEx', maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long))
    def mapCreateRscFromXsdEx(_rscpath: mapsyst.WTEXT, _xsdpath: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Создать классификатор по XSD схеме из файла
        
        :param _rscpath: путь для сохранения классификатора
        
        :param _xsdpath: путь к схеме
        
        :param _error: адрес поля для записи кода ошибки или ноль
        
        :returns: При ошибке возвращает ноль, в противном случае количество добавленных слоев
        :rtype: int
        """
        return mapCreateRscFromXsdEx_t (_rscpath.buffer(), _xsdpath.buffer(), _error)

    mapCreateRscFromXsdStreamEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateRscFromXsdStreamEx', maptype.PWCHAR, ctypes.c_char_p, ctypes.c_ulong, ctypes.POINTER(ctypes.c_long))
    def mapCreateRscFromXsdStreamEx(_rscpath: mapsyst.WTEXT, _memory: ctypes.c_char_p, _size: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Создать классификатор по XSD схеме из потока
        
        :param _rscpath: путь для сохранения классификатора
        
        :param _memory: данные, содержащие схему
        
        :param _size: размер данных со схемой
        
        :param _error: адрес поля для записи кода ошибки или ноль
        
        :returns: При ошибке возвращает ноль, в противном случае количество добавленных слоев
        :rtype: int
        """
        return mapCreateRscFromXsdStreamEx_t (_rscpath.buffer(), _memory, _size, _error)

    mapGetRscDescribe_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscDescribe', maptype.HRSC, ctypes.POINTER(maptype.RSCCREATE), ctypes.POINTER(maptype.PALETTE256))
    def mapGetRscDescribe(_hrsc: maptype.HRSC, _rsccreate: ctypes.POINTER(maptype.RSCCREATE), _palette: ctypes.POINTER(maptype.PALETTE256)) -> int:
        """
        Запросить данные по классификатору векторной карты
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _rsccreate: входные данные
        
        :param _palette: при необходимости задается палитра, не более ``32`` цветов Структуры ``RSCCREATEUN``, ``PALETTE256`` описаны в maptype.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscDescribe_t (_hrsc, _rsccreate, _palette)

    mapOpenRscEx_t = mapsyst.GetProcAddress(acceslib,maptype.HRSC,'mapOpenRscEx', maptype.PWCHAR, ctypes.c_long)
    def mapOpenRscEx(_name: mapsyst.WTEXT, _mode: int) -> maptype.HRSC:
        """
        Открыть классификатор
        
        :param _name: имя  файла классификатора
        
        :param _mode: ``GENERIC_READ`` или ``GENERIC_WRITE`` (``0`` обрабатывается как ``GENERIC_WRITE``)
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HRSC
        """
        return mapOpenRscEx_t (_name.buffer(), _mode)

    mapOpenCommonRscUn_t = mapsyst.GetProcAddress(acceslib,maptype.HRSC,'mapOpenCommonRscUn', maptype.PWCHAR)
    def mapOpenCommonRscUn(_name: mapsyst.WTEXT) -> maptype.HRSC:
        """
        Открыть классификатор в общем списке классификаторов
        
        :param _name: имя  файла классификатора Для ускорения последующего открытия или закрытия карт с этим классификатором при потоковой обработке
        
        :returns: При ошибке возвращает ноль, иначе идентификатор классификатора карты
        :rtype: maptype.HRSC
        """
        return mapOpenCommonRscUn_t (_name.buffer())

    mapCloseRsc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCloseRsc', maptype.HRSC)
    def mapCloseRsc(_hrsc: maptype.HRSC) -> int:
        """
        Закрыть классификатор
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCloseRsc_t (_hrsc)

    mapCommitRsc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCommitRsc', maptype.HRSC)
    def mapCommitRsc(_hrsc: maptype.HRSC) -> int:
        """
        Сохранить классификатор на диск или на сервер после обновления
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCommitRsc_t (_hrsc)

    mapSaveRscAs_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSaveRscAs', maptype.HRSC, maptype.PWCHAR)
    def mapSaveRscAs(_hrsc: maptype.HRSC, _path: mapsyst.WTEXT) -> int:
        """
        Сохранить классификатор по указанному пути, включая имя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _path: путь к создаваемому файлу в UTF-16
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSaveRscAs_t (_hrsc, _path.buffer())

    mapFindRscEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapFindRscEx', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def mapFindRscEx(_srcname: mapsyst.WTEXT, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Найти классификатор в текущей папке, папке приложения или общей папке классификаторов
        
        :param _srcname: имя или полный путь классификатора, автоматически ищутся файлы rsc и rscz
        
        :param _name: поле для записи найденного файла rsc с заданным именем
        
        :param _size: размер буфера в байтах для записи полного пути найденного классификатора, если размер равен нулю, то имя классификатора не перезаписывается найденным путем
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapFindRscEx_t (_srcname.buffer(), _name.buffer(), _size)

    mapLoadRscFrom_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLoadRscFrom', maptype.HRSC, maptype.PWCHAR)
    def mapLoadRscFrom(_hrsc: maptype.HRSC, _path: mapsyst.WTEXT) -> int:
        """
        Считать классификатор по указанному пути
        
        :param _hrsc: идентификатор обновляемого классификатора карты
        
        :param _path: путь к считываемому файлу в UTF-16 Чтобы сразу сохранить считанный классификатор в тот, что был открыт изначально, необходимо вызвать mapCommitRsc Чтобы отменить результаты считывания нужно вызвать mapRevertRsc
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapLoadRscFrom_t (_hrsc, _path.buffer())

    mapRevertRsc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRevertRsc', maptype.HRSC)
    def mapRevertRsc(_hrsc: maptype.HRSC) -> int:
        """
        Восстановить классификатор с диска
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapRevertRsc_t (_hrsc)

    mapPressRsc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPressRsc', maptype.HRSC)
    def mapPressRsc(_hrsc: maptype.HRSC) -> int:
        """
        Сжать классификатор в памяти, удалить из таблиц удаленные записи
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPressRsc_t (_hrsc)

    mapRscGetXSDName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRscGetXSDName', maptype.HRSC, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def mapRscGetXSDName(_hrsc: maptype.HRSC, _path: mapsyst.WTEXT, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Сформировать имя XSD-схемы по заданному пути
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _path: путь для размещения схемы
        
        :param _name: буфер для записи полного пути к схеме
        
        :param _size: длина буфера в байтах К имени папки дописывается имя классификатора с расширением ``".xsd"`` Например: ...\\schemas\\map5000m\\map5000m.xsd
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapRscGetXSDName_t (_hrsc, _path.buffer(), _name.buffer(), _size)

    mapRscUpdateXSD_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRscUpdateXSD', maptype.HRSC, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapRscUpdateXSD(_hrsc: maptype.HRSC, _path: mapsyst.WTEXT, _name: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Создать или обновить XSD-схему для RSC
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _path: путь для размещения схемы
        
        :param _name: буфер для записи полного пути к схеме
        
        :param _size: длина буфера в байтах
        
        :param _error: поле для записи кода ошибки (maperr.rh) По заданному пути создается папка с именем классификатора без расширения К имени папки дописывается имя классификатора с расширением ``".xsd"`` Например: ...\\schemas\\map5000m\\map5000m.xsd
        
        :returns: Если схема не требует обновления, то возвращает -1 При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если такого файла нет или он старее файла RSC, то выполняется создание файла схемы функцией mapRscSaveToXSD
        """
        return mapRscUpdateXSD_t (_hrsc, _path.buffer(), _name.buffer(), _size, _error)

    mapRscSaveToXSDPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRscSaveToXSDPro', maptype.HRSC, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, maptype.PWCHAR)
    def mapRscSaveToXSDPro(_hrsc: maptype.HRSC, _name: mapsyst.WTEXT, _layers: mapsyst.WTEXT, _comment: mapsyst.WTEXT, _isselectonly: int, _prefix: mapsyst.WTEXT) -> int:
        """
        Сохранить описание классификатора в виде прикладной XSD схемы
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _name: имя создаваемой ``XSD`` схемы
        
        :param _layers: имя ``XML`` файла, содержащего указания на переименование и обобщение слоев в прикладной схеме
        
        :param _comment: текст комментария для размещения в прикладной схеме
        
        :param _isselectonly: признак вывода в схему только тех слоев, что заданы в файле слоев (layers)
        
        :param _prefix: префикс идентификатора схемы (targetnamespace), если значение равно нулю, то в качества идентификатора присваивается имя классификатора ``RSC`` без расширения
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Например, для operator.rsc в схеме будут сгенерированы строки:
           ``"<xsd:schema "``xmlns:operator=\\``"http://www.gisinfo.net/bsd/operator"``
           targetNamespace=``"http://www.gisinfo.net/bsd/operator"``>"
           Имена прикладных элементов в данной схеме будут начинаться с префикса ``"operator:"``
           Подробнее о содержании прикладной схемы можно прочитать
           в документе ``"Спецификация GML для ЦТК"``
        """
        return mapRscSaveToXSDPro_t (_hrsc, _name.buffer(), _layers.buffer(), _comment.buffer(), _isselectonly, _prefix.buffer())

    mapTurnRsc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapTurnRsc', maptype.PWCHAR, ctypes.c_long)
    def mapTurnRsc(_name: mapsyst.WTEXT, _tomips: int) -> int:
        """
        Преобразовать формат двоичных числовых полей файла RSC к заданной платформе
        
        :param _name: полный путь к файлу преобразуемого классификатора
        
        :param _tomips: признак платформы: ``0`` - ``"Intel\\Little endian"``, ``1`` - ``"Mips\\Sparc\\Big endian"`` Преобразование классификатора к той платформе, на которой его открывают, выполняется автоматически
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapTurnRsc_t (_name.buffer(), _tomips)

    mapGetRscLocalCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscLocalCount', maptype.HRSC)
    def mapGetRscLocalCount(_hrsc: maptype.HRSC) -> int:
        """
        Запросить количество локализаций
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscLocalCount_t (_hrsc)

    mapGetRscLocalNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscLocalNameUn', maptype.HRSC, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapGetRscLocalNameUn(_hrsc: maptype.HRSC, _local: int, _name: mapsyst.WTEXT, _size: int, _language: int) -> int:
        """
        Запросить название локализации по ее номеру
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _local: тип локализации (``0`` - линейный, ...)
        
        :param _name: адрес строки для размещения результата
        
        :param _size: размер строки
        
        :param _language: код языка (``ML_RUSSIAN``, ``ML_ENGLISH``, ...) или ``0`` (тот, что установлен в ядре)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscLocalNameUn_t (_hrsc, _local, _name.buffer(), _size, _language)

    mapGetRscLocalNameSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscLocalNameSize', maptype.HRSC)
    def mapGetRscLocalNameSize(_hrsc: maptype.HRSC) -> int:
        """
        Запросить длину имени локализации
        
        :param _hrsc: идентификатор классификатора карты Обычно все названия до ``32`` символов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscLocalNameSize_t (_hrsc)

    mapGetRscLocalName_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetRscLocalName', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapGetRscLocalName(_hrsc: maptype.HRSC, _local: int, _language: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить название локализации по ее номеру
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _local: тип локализации  (``0`` - линейный, ...)
        
        :param _language: язык Названия хранятся на двух языках ...
        """
        return mapGetRscLocalName_t (_hrsc, _local, _language)

    mapGetRscSegmentCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSegmentCount', maptype.HRSC)
    def mapGetRscSegmentCount(_hrsc: maptype.HRSC) -> int:
        """
        Запросить количество слоев
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSegmentCount_t (_hrsc)

    mapGetRscSegmentName_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetRscSegmentName', maptype.HRSC, ctypes.c_long)
    def mapGetRscSegmentName(_hrsc: maptype.HRSC, _layer: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить имя слоя по порядковому номеру слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :returns: При ошибке возвращает пустую строку
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetRscSegmentName_t (_hrsc, _layer)

    mapGetRscSegmentNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSegmentNameUn', maptype.HRSC, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetRscSegmentNameUn(_hrsc: maptype.HRSC, _layer: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить имя слоя по порядковому номеру слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :param _name: адрес строки для размещения результата
        
        :param _size: размер строки (может быть до ``2048`` байт)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSegmentNameUn_t (_hrsc, _layer, _name.buffer(), _size)

    mapGetSegmentByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSegmentByNameUn', maptype.HRSC, maptype.PWCHAR)
    def mapGetSegmentByNameUn(_hrsc: maptype.HRSC, _name: mapsyst.WTEXT) -> int:
        """
        Запросить порядковый номер слоя по имени
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _name: имя слоя Номера слоев начинаются с ``0``
        
        :returns: При отсутствии слоя возвращает -1
        :rtype: int
        """
        return mapGetSegmentByNameUn_t (_hrsc, _name.buffer())

    mapGetRscSegmentNameSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSegmentNameSize', maptype.HRSC)
    def mapGetRscSegmentNameSize(_hrsc: maptype.HRSC) -> int:
        """
        Запросить максимальную длину имени слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSegmentNameSize_t (_hrsc)

    mapGetRscSegmentOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSegmentOrder', maptype.HRSC, ctypes.c_long)
    def mapGetRscSegmentOrder(_hrsc: maptype.HRSC, _layer: int) -> int:
        """
        Запросить порядок вывода слоя на экран по порядковому номеру
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSegmentOrder_t (_hrsc, _layer)

    mapGetRscSegmentObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSegmentObjectCount', maptype.HRSC, ctypes.c_long)
    def mapGetRscSegmentObjectCount(_hrsc: maptype.HRSC, _layer: int) -> int:
        """
        Запросить количество объектов слоя по порядковому номеру слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSegmentObjectCount_t (_hrsc, _layer)

    mapSetRscSegmentName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscSegmentName', maptype.HRSC, ctypes.c_long, ctypes.c_char_p)
    def mapSetRscSegmentName(_hrsc: maptype.HRSC, _layer: int, _name: ctypes.c_char_p) -> int:
        """
        Установить имя слоя по порядковому номеру слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :param _name: имя слоя
        
        :returns: При ошибке возвращает ноль, иначе порядковый номер слоя. Если вернулся 0, проверьте код последней ошибки функцией mapGetRscError При установке уже имеющегося имени слоя функция mapGetRscError возвращает IDS_RSCEXITSEGMENTERROR (maperr.rh)
        :rtype: int
        """
        return mapSetRscSegmentName_t (_hrsc, _layer, _name)

    mapSetRscSegmentOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscSegmentOrder', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapSetRscSegmentOrder(_hrsc: maptype.HRSC, _layer: int, _order: int) -> int:
        """
        Установить порядок вывода слоя по порядковому номеру слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :param _order: порядок вывода
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscSegmentOrder_t (_hrsc, _layer, _order)

    mapDeleteRscSegment_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRscSegment', maptype.HRSC, ctypes.c_long)
    def mapDeleteRscSegment(_hrsc: maptype.HRSC, _layer: int) -> int:
        """
        Удалить слой по порядковому номеру слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0`` Слой удаляется вместе с объектами
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteRscSegment_t (_hrsc, _layer)

    mapMoveRscSegmentObjects_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapMoveRscSegmentObjects', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapMoveRscSegmentObjects(_hrsc: maptype.HRSC, _oldcode: int, _newcode: int) -> int:
        """
        Перенести объекты из одного слоя в другой
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _oldcode: номер слоя
        
        :param _newcode: номер слоя
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapMoveRscSegmentObjects_t (_hrsc, _oldcode, _newcode)

    mapAppendRscSegment_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendRscSegment', maptype.HRSC, ctypes.POINTER(maptype.RSCSEGMENT))
    def mapAppendRscSegment(_hrsc: maptype.HRSC, _segment: ctypes.POINTER(maptype.RSCSEGMENT)) -> int:
        """
        Создать слой в классификаторе карты
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _segment: структура входных данных (описана в maptype.h)
        
        :returns: При ошибке возвращает ноль, иначе порядковый номер слоя с 0 Если вернулся 0, проверьте код последней ошибки функцией mapGetRscError При установке уже имеющегося имени слоя функция mapGetRscError возвращает IDS_RSCEXITSEGMENTERROR (maperr.rh)
        :rtype: int
        """
        return mapAppendRscSegment_t (_hrsc, _segment)

    mapGetRscSegment_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSegment', maptype.HRSC, ctypes.POINTER(maptype.RSCSEGMENT), ctypes.c_long)
    def mapGetRscSegment(_hrsc: maptype.HRSC, _segment: ctypes.POINTER(maptype.RSCSEGMENT), _layer: int) -> int:
        """
        Заполнить структуру описания слоев
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _segment: структура входных данных (``RSCSEGMENT`` описана в maptype.h)
        
        :param _layer: номер слоя c ``0``
        
        :returns: При ошибке возвращает ноль, иначе - порядковый номер слоя с 0
        :rtype: int
        """
        return mapGetRscSegment_t (_hrsc, _segment, _layer)

    mapGetRscSegmentShortNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSegmentShortNameUn', maptype.HRSC, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetRscSegmentShortNameUn(_hrsc: maptype.HRSC, _layer: int, _shortname: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить короткое имя слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :param _shortname: короткое имя (ключ) слоя
        
        :param _size: размер строки
        
        :returns: При ошибке возвращает пустую строку
        :rtype: int
        """
        return mapGetRscSegmentShortNameUn_t (_hrsc, _layer, _shortname.buffer(), _size)

    mapSetRscSegmentShortName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscSegmentShortName', maptype.HRSC, ctypes.c_long, ctypes.c_char_p)
    def mapSetRscSegmentShortName(_hrsc: maptype.HRSC, _layer: int, _shortname: ctypes.c_char_p) -> int:
        """
        Установить короткое имя(ключ) слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscSegmentShortName_t (_hrsc, _layer, _shortname)

    mapGetRscSegmentByShortNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSegmentByShortNameUn', maptype.HRSC, maptype.PWCHAR)
    def mapGetRscSegmentByShortNameUn(_hrsc: maptype.HRSC, _shortname: mapsyst.WTEXT) -> int:
        """
        Запросить порядковый номер слоя по короткому имени слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _shortname: короткое имя (ключ) слоя
        
        :returns: При ошибке возвращает -1
        :rtype: int
        """
        return mapGetRscSegmentByShortNameUn_t (_hrsc, _shortname.buffer())

    mapGetRscSegmentSemanticCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSegmentSemanticCount', maptype.HRSC, ctypes.c_long)
    def mapGetRscSegmentSemanticCount(_hrsc: maptype.HRSC, _layer: int) -> int:
        """
        Запросить количество семантик слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSegmentSemanticCount_t (_hrsc, _layer)

    mapGetRscSegmentSemanticCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSegmentSemanticCode', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapGetRscSegmentSemanticCode(_hrsc: maptype.HRSC, _layer: int, _number: int) -> int:
        """
        Запросить код семантики слоя по порядковому номеру
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :param _number: порядковый номер семантики в списке с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSegmentSemanticCode_t (_hrsc, _layer, _number)

    mapAppendRscSegmentSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendRscSegmentSemantic', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapAppendRscSegmentSemantic(_hrsc: maptype.HRSC, _layer: int, _semanticcode: int) -> int:
        """
        Добавить семантику слою
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :param _semanticcode: код добавляемой семантики
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendRscSegmentSemantic_t (_hrsc, _layer, _semanticcode)

    mapDeleteRscSegmentSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRscSegmentSemantic', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapDeleteRscSegmentSemantic(_hrsc: maptype.HRSC, _layer: int, _semanticcode: int) -> int:
        """
        Удалить семантику из слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :param _semanticcode: код удаляемой семантики
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteRscSegmentSemantic_t (_hrsc, _layer, _semanticcode)

    mapBuildRscSegmentSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBuildRscSegmentSemantic', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapBuildRscSegmentSemantic(_hrsc: maptype.HRSC, _layer: int, _type: int) -> int:
        """
        Установить семантику для слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :param _type: ``0`` - собрать всю семантику объектов (обязательную и возможную) ``1`` - только обязательную ``2`` - собрать всю семантику объектов + общую семантику
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapBuildRscSegmentSemantic_t (_hrsc, _layer, _type)

    mapSetRscSegmentNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscSegmentNameUn', maptype.HRSC, ctypes.c_long, maptype.PWCHAR)
    def mapSetRscSegmentNameUn(_hrsc: maptype.HRSC, _layer: int, _name: mapsyst.WTEXT) -> int:
        """
        Установить имя слоя по порядковому номеру слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :param _name: имя слоя
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscSegmentNameUn_t (_hrsc, _layer, _name.buffer())

    mapGetRscClassCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscClassCount', maptype.HRSC)
    def mapGetRscClassCount(_hrsc: maptype.HRSC) -> int:
        """
        Запросить количество классов слоев
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscClassCount_t (_hrsc)

    mapGetRscClassIdent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscClassIdent', maptype.HRSC, ctypes.c_long)
    def mapGetRscClassIdent(_hrsc: maptype.HRSC, _number: int) -> int:
        """
        Запросить идентификатор класса слоя по порядковому номеру среди классов слоев
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: порядковый номер класса c ``1``
        
        :returns: При ошибке возвращает ноль, иначе - идентификатор класса слоя (более 255)
        :rtype: int
        """
        return mapGetRscClassIdent_t (_hrsc, _number)

    mapGetRscClassLevel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscClassLevel', maptype.HRSC, ctypes.c_long)
    def mapGetRscClassLevel(_hrsc: maptype.HRSC, _ident: int) -> int:
        """
        Запросить уровень класса слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _ident: идентификатор класса (более ``255``)
        
        :returns: Возвращает уровень класса слоя (больше или равен 1) При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscClassLevel_t (_hrsc, _ident)

    mapGetRscClassParent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscClassParent', maptype.HRSC, ctypes.c_long)
    def mapGetRscClassParent(_hrsc: maptype.HRSC, _ident: int) -> int:
        """
        Запросить идентификатор родителя класса слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _ident: идентификатор класса (более ``255``)
        
        :returns: Возвращает идентификатор класса или порядковый номер слоя (если класс 1 уровня) При ошибке возвращает ноль (для класса 1 уровня 0 допустим)
        :rtype: int
        """
        return mapGetRscClassParent_t (_hrsc, _ident)

    mapGetRscClassNameUnicode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscClassNameUnicode', maptype.HRSC, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetRscClassNameUnicode(_hrsc: maptype.HRSC, _ident: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить имя класса слоя по идентификатору класса
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _ident: идентификатор класса (более ``255``)
        
        :param _name: адрес строки для размещения результата
        
        :param _size: размер строки (может быть до ``2048`` байт)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscClassNameUnicode_t (_hrsc, _ident, _name.buffer(), _size)

    mapSetRscClassNameUnicode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscClassNameUnicode', maptype.HRSC, ctypes.c_long, maptype.PWCHAR)
    def mapSetRscClassNameUnicode(_hrsc: maptype.HRSC, _ident: int, _name: mapsyst.WTEXT) -> int:
        """
        Установить имя класса слоя по идентификатору класса
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _ident: идентификатор класса (более ``255``)
        
        :param _name: полное имя класса
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscClassNameUnicode_t (_hrsc, _ident, _name.buffer())

    mapAppendRscClass_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendRscClass', maptype.HRSC, ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR)
    def mapAppendRscClass(_hrsc: maptype.HRSC, _parent: int, _key: mapsyst.WTEXT, _name: mapsyst.WTEXT) -> int:
        """
        Создать новый класс слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _parent: идентификатор класса - родителя или порядковый номер основного слоя
        
        :param _key: ключ, короткое имя класса (сохраняется как char[``32``] c завершающим нулем - уникальное)
        
        :param _name: имя класса
        
        :returns: Возвращает идентификатор класса При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendRscClass_t (_hrsc, _parent, _key.buffer(), _name.buffer())

    mapDeleteRscClass_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRscClass', maptype.HRSC, ctypes.c_long)
    def mapDeleteRscClass(_hrsc: maptype.HRSC, _ident: int) -> int:
        """
        Удалить класс слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _ident: идентификатор класса (более ``255``) Класс удаляется со всеми классами - потомками, объекты переносятся в класс - родитель или в слой - родитель
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteRscClass_t (_hrsc, _ident)

    mapGetRscClassGenericSegment_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscClassGenericSegment', maptype.HRSC, ctypes.c_long)
    def mapGetRscClassGenericSegment(_hrsc: maptype.HRSC, _ident: int) -> int:
        """
        Запросить слой для класса слоя по идентификатору класса
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _ident: идентификатор класса (более ``255``)
        
        :returns: Возвращает номер слоя (может быть 0)
        :rtype: int
        """
        return mapGetRscClassGenericSegment_t (_hrsc, _ident)

    mapGetRscClassKeyUnicode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscClassKeyUnicode', maptype.HRSC, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetRscClassKeyUnicode(_hrsc: maptype.HRSC, _ident: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить ключ класса слоя по идентификатору класса
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _ident: идентификатор класса (более ``255``)
        
        :param _name: адрес строки для размещения результата
        
        :param _size: размер строки (не менее ``64`` байта)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscClassKeyUnicode_t (_hrsc, _ident, _name.buffer(), _size)

    mapGetRscClassIdentbyKeyUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscClassIdentbyKeyUn', maptype.HRSC, maptype.PWCHAR)
    def mapGetRscClassIdentbyKeyUn(_hrsc: maptype.HRSC, _name: mapsyst.WTEXT) -> int:
        """
        Запросить идентификатор класса по ключу класса
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _name: уникальный ключ слоя
        
        :returns: Возвращает идентификатор класса или 0
        :rtype: int
        """
        return mapGetRscClassIdentbyKeyUn_t (_hrsc, _name.buffer())

    mapSetRscClassKeyUnicode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscClassKeyUnicode', maptype.HRSC, ctypes.c_long, maptype.PWCHAR)
    def mapSetRscClassKeyUnicode(_hrsc: maptype.HRSC, _ident: int, _name: mapsyst.WTEXT) -> int:
        """
        Записать ключ класса по идентификатору класса
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _ident: идентификатор класса (более ``255``)
        
        :param _name: уникальный ключ слоя не более ``31`` символа (записывается в char[``32``])
        
        :returns: Возвращает длину ключа в байтах или 0
        :rtype: int
        """
        return mapSetRscClassKeyUnicode_t (_hrsc, _ident, _name.buffer())

    mapGetRscSegmentClassCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSegmentClassCount', maptype.HRSC, ctypes.c_long)
    def mapGetRscSegmentClassCount(_hrsc: maptype.HRSC, _layer: int) -> int:
        """
        Запросить количество дочерних классов слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :returns: Возвращает количество дочерних классов слоя
        :rtype: int
        """
        return mapGetRscSegmentClassCount_t (_hrsc, _layer)

    mapGetRscSegmentSeekIdentCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSegmentSeekIdentCount', maptype.HRSC, ctypes.c_long)
    def mapGetRscSegmentSeekIdentCount(_hrsc: maptype.HRSC, _layer: int) -> int:
        """
        Запросить количество семантик - идентификаторов поиска для слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :returns: Возвращает количество семантик - идентификаторов поиска
        :rtype: int
        """
        return mapGetRscSegmentSeekIdentCount_t (_hrsc, _layer)

    mapGetRscSegmentSeekIdentCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSegmentSeekIdentCode', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapGetRscSegmentSeekIdentCode(_hrsc: maptype.HRSC, _layer: int, _semnumber: int) -> int:
        """
        Запросить код семантик - идентификаторов поиска для слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :param _semnumber: порядковый номер семантики ( от ``1`` до ``4``)
        
        :returns: Возвращает код семантики - идентификатора поиска или 0
        :rtype: int
        """
        return mapGetRscSegmentSeekIdentCode_t (_hrsc, _layer, _semnumber)

    mapGetRscSegmentSeekIdentFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSegmentSeekIdentFlag', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapGetRscSegmentSeekIdentFlag(_hrsc: maptype.HRSC, _layer: int, _semcode: int) -> int:
        """
        Запросить - является ли семантика идентификатором поиска для слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :param _semcode: код семантики
        
        :returns: Возвращает: ``1`` - является, ``0`` - не является
        :rtype: int
        """
        return mapGetRscSegmentSeekIdentFlag_t (_hrsc, _layer, _semcode)

    mapSetRscSegmentSeekIdentFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscSegmentSeekIdentFlag', maptype.HRSC, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSetRscSegmentSeekIdentFlag(_hrsc: maptype.HRSC, _layer: int, _semcode: int, _flag: int) -> int:
        """
        Установить семантику как идентификатор поиска для слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _layer: номер слоя c ``0``
        
        :param _semcode: код семантики
        
        :param _flag: ``1`` назначить семантику идентификатором поиска для слоя - ``0`` удалить семантику из списка семантик - идентификаторов поиска
        
        :returns: Если у слоя уже 4 семантики - идентификатора, семантика не устанавливается и возвращается 0 Если семантика не входит в список семантик слоя - семантика будет добавлена в список семантик слоя При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscSegmentSeekIdentFlag_t (_hrsc, _layer, _semcode, _flag)

    mapAppendRscObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendRscObject', maptype.HRSC, ctypes.POINTER(maptype.RSCOBJECT))
    def mapAppendRscObject(_hrsc: maptype.HRSC, _object: ctypes.POINTER(maptype.RSCOBJECT)) -> int:
        """
        Создать объект
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _object: описание объекта (структура ``RSCOBJECT`` описана в maptype.h)
        
        :returns: При ошибке возвращает ноль, иначе - порядковый номер объекта с 1
        :rtype: int
        """
        return mapAppendRscObject_t (_hrsc, _object)

    mapCopyRscObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCopyRscObject', maptype.HRSC, ctypes.c_long)
    def mapCopyRscObject(_hrsc: maptype.HRSC, _oldcode: int) -> int:
        """
        Скопировать объект
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _oldcode: порядковый номер объекта с которого копируют Копируется заголовок объекта, вид изображения, семантика объекта, код ``FIRSTSERVEXCODE`` Для того, чтобы данный объект сохранился, пользователь должен переопределить внешний код
        
        :returns: При ошибке возвращает ноль, иначе - порядковый номер нового объекта с 1
        :rtype: int
        """
        return mapCopyRscObject_t (_hrsc, _oldcode)

    mapUpdateRscObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateRscObject', maptype.HRSC, ctypes.c_long, ctypes.POINTER(maptype.RSCOBJECT))
    def mapUpdateRscObject(_hrsc: maptype.HRSC, _code: int, _object: ctypes.POINTER(maptype.RSCOBJECT)) -> int:
        """
        Обновить объект
        
        :param _hrsc: идентификатор классификатора карты сode   - порядковый номер объекта с ``1``
        
        :param _object: описание объекта (структура ``RSCOBJECT`` описана в maptype.h)
        
        :returns: При ошибке возвращает ноль , иначе порядковый номер объекта с 1 При наличии серии внешний код, локализация и слой - не меняются Если внешний вид объекта не соответствует локализации - записывается умалчиваемый внешний вид
        :rtype: int
        """
        return mapUpdateRscObject_t (_hrsc, _code, _object)

    mapDeleteRscObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRscObject', maptype.HRSC, ctypes.c_long)
    def mapDeleteRscObject(_hrsc: maptype.HRSC, _code: int) -> int:
        """
        Удалить объект
        
        :param _hrsc: идентификатор классификатора карты сode - порядковый номер объекта который удаляют с ``1``
        
        :returns: При ошибке возвращает ноль, иначе порядковый номер удаленного объекта Если объект входит в серию - удаление не делается
        :rtype: int
        """
        return mapDeleteRscObject_t (_hrsc, _code)

    mapGetRscObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObject', maptype.HRSC, ctypes.c_long, ctypes.POINTER(maptype.RSCOBJECT))
    def mapGetRscObject(_hrsc: maptype.HRSC, _incode: int, _object: ctypes.POINTER(maptype.RSCOBJECT)) -> int:
        """
        Заполнить структуру описания объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: порядковый номер объекта с ``1``
        
        :param _object: описание объекта (структура ``RSCOBJECT`` описана в maptype.h)
        
        :returns: При ошибке возвращает ноль , иначе порядковый номер объекта
        :rtype: int
        """
        return mapGetRscObject_t (_hrsc, _incode, _object)

    mapGetRscObjectNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectNumber', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectNumber(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить порядковый номер объекта в серии однотипных объектов по внутреннему коду объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: порядковый номер объекта с ``1`` Однотипные объекты имеют общий классификационный код и локализацию Противоположная функция - mapGetRscObjectCodeByNumber
        
        :returns: При ошибке или отсутствии серии возвращает ноль, иначе номер объекта в серии
        :rtype: int
        """
        return mapGetRscObjectNumber_t (_hrsc, _incode)

    mapGetRscImageSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscImageSize', maptype.HRSC, ctypes.c_long, ctypes.POINTER(maptype.IMAGESIZE), ctypes.c_long, ctypes.c_char_p)
    def mapGetRscImageSize(_hrsc: maptype.HRSC, _incode: int, _imagesize: ctypes.POINTER(maptype.IMAGESIZE), _length: int, _string: ctypes.c_char_p) -> int:
        """
        Запросить размеры в микронах и свойства экранного вида объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: порядковый номер объекта с ``1``
        
        :param _imagesize: структура размеров и свойств изображения объектов (``IMAGESIZE`` описана maptype.h)
        
        :param _string: строка длиной length задается для определения горизонтального размера подписи
        
        :param _length: длина строки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscImageSize_t (_hrsc, _incode, _imagesize, _length, _string)

    mapGetRscPrnImageSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscPrnImageSize', maptype.HRSC, ctypes.c_long, ctypes.POINTER(maptype.IMAGESIZE), ctypes.c_long, ctypes.c_char_p)
    def mapGetRscPrnImageSize(_hrsc: maptype.HRSC, _incode: int, _imagesize: ctypes.POINTER(maptype.IMAGESIZE), _length: int, _string: ctypes.c_char_p) -> int:
        """
        Запросить размеры в микронах и свойства принтерного вида объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: порядковый номер объекта с ``1``
        
        :param _imagesize: структура размеров и свойств изображения объектов (``IMAGESIZE`` описана maptype.h)
        
        :param _string: строка длиной length задается для определения горизонтального размера подписи
        
        :param _length: длина строки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscPrnImageSize_t (_hrsc, _incode, _imagesize, _length, _string)

    mapGetRscMarkFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscMarkFrame', maptype.HRSC, ctypes.c_long, ctypes.c_char_p, ctypes.c_double, ctypes.POINTER(maptype.IMAGEFRAME))
    def mapGetRscMarkFrame(_hrsc: maptype.HRSC, _number: int, _param: ctypes.c_char_p, _angle: float, _imageframe: ctypes.POINTER(maptype.IMAGEFRAME)) -> int:
        """
        Запросить габаритную рамку изображения объекта с учетом поворота объекта
        
        :param _number: номер функции отображения (mapgdi.h)
        
        :param _param: параметры отображения (mapgdi.h)
        
        :param _angle: угол поворота объекта в радианах по часовой стрелке
        
        :param _imageframe: габаритная рамка изображения объекта (точечный, векторный) Cтруктура ``IMAGEFRAME`` описана в maptype.h Все размеры в микронах на ``"бумажном"`` изображении (в базовом масштабе) относительно первой точки метрики объекта в картографической системе Для пересчета полученных координат в метры на местности нужно их поделить на ``1 000 000``, умножить на базовый масштаб карты и добавить координаты первой точки метрики
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscMarkFrame_t (_hrsc, _number, _param, _angle, _imageframe)

    mapGetRscObjectCodeByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectCodeByNumber', maptype.HRSC, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapGetRscObjectCodeByNumber(_hrsc: maptype.HRSC, _excode: int, _local: int, _number: int) -> int:
        """
        Запросить внутренний код объекта по внешнему коду, локализации и порядковому номеру
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _excode: внешний код объекта
        
        :param _local: тип локализации
        
        :param _number: порядковый номер среди аналогичных объектов
        
        :returns: Возвращает внутренний код (порядковый номер) с 1 При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectCodeByNumber_t (_hrsc, _excode, _local, _number)

    mapGetRscObjectsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectsCount', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapGetRscObjectsCount(_hrsc: maptype.HRSC, _excode: int, _local: int) -> int:
        """
        Запросить количество объектов с заданным внешним кодом и локализацией
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _excode: внешний код объекта
        
        :param _local: тип локализации
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectsCount_t (_hrsc, _excode, _local)

    mapGetRscObjectName_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetRscObjectName', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectName(_hrsc: maptype.HRSC, _incode: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить имя объекта по внутреннему коду объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта (номер по порядку) с ``1``
        
        :returns: При ошибке возвращает пустую строку
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetRscObjectName_t (_hrsc, _incode)

    mapGetRscObjectNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectNameUn', maptype.HRSC, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetRscObjectNameUn(_hrsc: maptype.HRSC, _incode: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить имя объекта по внутреннему коду объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта (номер по порядку) с ``1``
        
        :param _name: адрес строки для размещения результата
        
        :param _size: зарезервированный размер строки (может быть до ``2048`` байт)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectNameUn_t (_hrsc, _incode, _name.buffer(), _size)

    mapGetRscObjectKeyUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectKeyUn', maptype.HRSC, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetRscObjectKeyUn(_hrsc: maptype.HRSC, _incode: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить ключ объекта по внутреннему коду объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта (номер по порядку) с ``1``
        
        :param _name: адрес строки для размещения результата
        
        :param _size: зарезервированный размер строки
        
        :returns: При ошибке возвращает пустую строку
        :rtype: int
        """
        return mapGetRscObjectKeyUn_t (_hrsc, _incode, _name.buffer(), _size)

    mapSetRscObjectKey_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapSetRscObjectKey', maptype.HRSC, ctypes.c_long, ctypes.c_char_p)
    def mapSetRscObjectKey(_hrsc: maptype.HRSC, _incode: int, _key: ctypes.c_char_p) -> ctypes.POINTER(ctypes.c_char):
        """
        Установить ключ объекта по внутреннему коду объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта (номер по порядку)
        
        :param _key: ключ объекта Короткое имя должно быть уникально
        
        :returns: При ошибке возвращает пустую строку
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapSetRscObjectKey_t (_hrsc, _incode, _key)

    mapGetRscObjectLocal_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectLocal', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectLocal(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить код локализации объекта по внутреннему коду объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта (номер по порядку) с ``1``
        
        :returns: При ошибке возвращает ноль (ноль допустим)
        :rtype: int
        """
        return mapGetRscObjectLocal_t (_hrsc, _incode)

    mapGetRscObjectSegment_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectSegment', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectSegment(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить номер слоя объекта по внутреннему коду объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта (номер по порядку) с ``1``
        
        :returns: При ошибке возвращает ноль (ноль допустим)
        :rtype: int
        """
        return mapGetRscObjectSegment_t (_hrsc, _incode)

    mapSetRscObjectSegment_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscObjectSegment', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapSetRscObjectSegment(_hrsc: maptype.HRSC, _incode: int, _segment: int) -> int:
        """
        Установить номер слоя объекта по внутреннему коду объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта (номер по порядку) с ``1``
        
        :param _segment: номер слоя с ``0``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscObjectSegment_t (_hrsc, _incode, _segment)

    mapGetRscObjectClass_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectClass', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectClass(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить идентификатор класса слоя объекта по внутреннему коду объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта (номер по порядку) с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectClass_t (_hrsc, _incode)

    mapSetRscObjectClass_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscObjectClass', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapSetRscObjectClass(_hrsc: maptype.HRSC, _incode: int, _ident: int) -> int:
        """
        Установить идентификатор класса слоя объекта по внутреннему коду
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _ident: идентификатор класса
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscObjectClass_t (_hrsc, _incode, _ident)

    mapGetRscObjectIdent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectIdent', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectIdent(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить идентификатор объекта по внутреннему коду
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта Идентификатор объекта - постоянное уникальное значение в пределах данного классификатора
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectIdent_t (_hrsc, _incode)

    mapGetRscObjectIdentIncode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectIdentIncode', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectIdentIncode(_hrsc: maptype.HRSC, _ident: int) -> int:
        """
        Запросить внутренний код объекта по идентификатору
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _ident: идентификатор объекта
        
        :returns: Возвращает внутренний код (порядковый номер) При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectIdentIncode_t (_hrsc, _ident)

    mapGetRscObjectCodeByKeyUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectCodeByKeyUn', maptype.HRSC, maptype.PWCHAR)
    def mapGetRscObjectCodeByKeyUn(_hrsc: maptype.HRSC, _key: mapsyst.WTEXT) -> int:
        """
        Запросить внутренний код объекта по ключу
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _key: ключ объекта
        
        :returns: Возвращает внутренний код (порядковый номер) При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectCodeByKeyUn_t (_hrsc, _key.buffer())

    mapGetRscObjectCodeByName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectCodeByName', maptype.HRSC, ctypes.c_char_p)
    def mapGetRscObjectCodeByName(_hrsc: maptype.HRSC, _name: ctypes.c_char_p) -> int:
        """
        Запросить внутренний код объекта по имени
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _name: имя объекта
        
        :returns: Возвращает внутренний код (порядковый номер) При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectCodeByName_t (_hrsc, _name)

    mapGetRscObjectCodeByNameAfterCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectCodeByNameAfterCode', maptype.HRSC, ctypes.c_char_p, ctypes.c_long)
    def mapGetRscObjectCodeByNameAfterCode(_hrsc: maptype.HRSC, _name: ctypes.c_char_p, _code: int) -> int:
        """
        Запросить внутренний код объекта по имени
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _name: имя объекта
        
        :param _code: внутренний код объекта, за которым нужно продолжить поиск объекта по имени
        
        :returns: Возвращает внутренний код (порядковый номер) При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectCodeByNameAfterCode_t (_hrsc, _name, _code)

    mapGetRscImageSemanticCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscImageSemanticCount', maptype.HRSC, ctypes.c_long)
    def mapGetRscImageSemanticCount(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить число семантик, влияющих на внещний вид объекта, по внутреннему коду
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscImageSemanticCount_t (_hrsc, _incode)

    mapGetRscImageSemanticCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscImageSemanticCode', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapGetRscImageSemanticCode(_hrsc: maptype.HRSC, _incode: int, _number: int) -> int:
        """
        Запросить код семантики, влияющей на изображение, по внутреннему коду объекта и порядковому номеру семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _number: номер семантики c ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscImageSemanticCode_t (_hrsc, _incode, _number)

    mapGetRscObjectRelateCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectRelateCount', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectRelateCount(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запpосить количество связанных подписей объекта по внутреннему коду объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectRelateCount_t (_hrsc, _incode)

    mapGetRscObjectRelateOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectRelateOrder', maptype.HRSC, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.RSCRELATION))
    def mapGetRscObjectRelateOrder(_hrsc: maptype.HRSC, _incode: int, _order: int, _relate: ctypes.POINTER(maptype.RSCRELATION)) -> int:
        """
        Запpосить описание связанной подписи по внутреннему коду объекта и по порядковому номеру связанной подписи
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта оrder  - порядковый номер связанной подписи с ``1``
        
        :param _relate: описание связанной подписи (описание в maptype.h)
        
        :returns: Возвращает идентификатор подписи При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectRelateOrder_t (_hrsc, _incode, _order, _relate)

    mapGetRscObjectSemanticFont_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectSemanticFont', maptype.HRSC, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.LOGFONTW), ctypes.c_long)
    def mapGetRscObjectSemanticFont(_hrsc: maptype.HRSC, _incode: int, _semanticcode: int, _font: ctypes.POINTER(maptype.LOGFONTW), _viewtype: int) -> int:
        """
        Запросить параметры шрифта для подписи семантики объекта по внутреннему коду объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _semanticcode: код семантики объекта
        
        :param _font: описание шрифта, структура ``LOGFONTW`` описана в mapsyst.h
        
        :param _viewtype: вид отображения объекта: ``0`` - экранный, ``1`` - принтерный
        
        :returns: При ошибке или, если в параметрах объекта нет подписи, возвращает  0
        :rtype: int
        """
        return mapGetRscObjectSemanticFont_t (_hrsc, _incode, _semanticcode, _font, _viewtype)

    mapDeleteRscObjectRelate_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRscObjectRelate', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapDeleteRscObjectRelate(_hrsc: maptype.HRSC, _incode: int, _semanticcode: int) -> int:
        """
        Удалить описание связанной подписи по внутреннему коду объекта и коду семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _semanticcode: код семантики объекта
        
        :returns: Возвращает внутренний код объекта При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteRscObjectRelate_t (_hrsc, _incode, _semanticcode)

    mapSetRscObjectNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscObjectNameUn', maptype.HRSC, ctypes.c_long, maptype.PWCHAR)
    def mapSetRscObjectNameUn(_hrsc: maptype.HRSC, _incode: int, _name: mapsyst.WTEXT) -> int:
        """
        Установить имя объекта по внутреннему коду объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _name: имя объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscObjectNameUn_t (_hrsc, _incode, _name.buffer())

    mapGetRscObjectWCodeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectWCodeUn', maptype.HRSC, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetRscObjectWCodeUn(_hrsc: maptype.HRSC, _incode: int, _wcode: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить буквенно-цифровой код объекта по внутреннему коду
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _wcode: указатель на поле для записи буквенно-цифрового кода объекта
        
        :param _size: указатель на поле для записи длины запрошенных данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectWCodeUn_t (_hrsc, _incode, _wcode.buffer(), _size)

    mapGetRscObjectIncodeByWCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectIncodeByWCode', maptype.HRSC, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapGetRscObjectIncodeByWCode(_hrsc: maptype.HRSC, _wcode: mapsyst.WTEXT, _local: int, _number: int) -> int:
        """
        Запросить внутренний код объекта по буквенно-цифровому коду объекта, локализации и порядковому номеру
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _wcode: буквенно-цифровой код объекта
        
        :param _local: тип локализации
        
        :param _number: порядковый номер среди аналогичных объектов Количество объектов можно получить функцией mapGetRscObjectsCount
        
        :returns: При ошибке возвращает ноль, иначе incode объекта
        :rtype: int
        """
        return mapGetRscObjectIncodeByWCode_t (_hrsc, _wcode.buffer(), _local, _number)

    mapGetRscObjectExcodeBySymbolicCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_ulong,'mapGetRscObjectExcodeBySymbolicCode', maptype.HRSC, maptype.PWCHAR)
    def mapGetRscObjectExcodeBySymbolicCode(_hrsc: maptype.HRSC, _wcode: mapsyst.WTEXT) -> int:
        """
        Запросить внешний код объекта по его буквенно-цифровому коду
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _wcode: буквенно-цифровой код объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectExcodeBySymbolicCode_t (_hrsc, _wcode.buffer())

    mapSetRscObjectWCodeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscObjectWCodeUn', maptype.HRSC, ctypes.c_long, maptype.PWCHAR)
    def mapSetRscObjectWCodeUn(_hrsc: maptype.HRSC, _incode: int, _wcode: mapsyst.WTEXT) -> int:
        """
        Установить буквенно-цифровой код объекта по внутреннему коду
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта wname  - буквенно-цифровой код
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscObjectWCodeUn_t (_hrsc, _incode, _wcode.buffer())

    mapGetRscObjectExcodePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_ulong,'mapGetRscObjectExcodePro', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectExcodePro(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить внешний код объекта по внутреннему коду
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectExcodePro_t (_hrsc, _incode)

    mapGetRscObjectOnePointFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectOnePointFlag', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectOnePointFlag(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить признак векторного объекта с одной точкой метрики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта Возвращаемое значение: ``0`` - признак не установлен, ``1`` - признак установлен (при создании векторного объекта сохранять после первой точки)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectOnePointFlag_t (_hrsc, _incode)

    mapSetRscObjectOnePointFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscObjectOnePointFlag', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapSetRscObjectOnePointFlag(_hrsc: maptype.HRSC, _incode: int, _flag: int) -> int:
        """
        Установить признак векторного объекта с одной точкой метрики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _flag: признак векторного объекта с одной точкой метрики: ``0`` - признак не установлен, ``1`` - признак установлен (при создании векторного объекта сохранять после первой точки)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscObjectOnePointFlag_t (_hrsc, _incode, _flag)

    mapGetRscObjOldFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjOldFlag', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjOldFlag(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить признак устаревшего объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта Возвращаемое значение: ``0`` - обычный объект, ``1`` - объект устарел и не должен отображаться в диалоге выбора создаваемого объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjOldFlag_t (_hrsc, _incode)

    mapSetRscObjOldFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscObjOldFlag', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapSetRscObjOldFlag(_hrsc: maptype.HRSC, _incode: int, _flag: int) -> int:
        """
        Установить флаг устаревшего объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _flag: признак устаревшего объекта: ``0`` - обычный объект, ``1`` - объект устарел и не должен отображаться в диалоге выбора создаваемого объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscObjOldFlag_t (_hrsc, _incode, _flag)

    mapGetRscObjectOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectOrder', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectOrder(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить порядoк вывода объекта в слое, в данной локализации
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectOrder_t (_hrsc, _incode)

    mapGetRscObjectOrderIndex_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectOrderIndex', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectOrderIndex(_hRsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить индекс порядка отображения объекта в слое
        
        :param _hRsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectOrderIndex_t (_hRsc, _incode)

    mapSetRscObjectOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscObjectOrder', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapSetRscObjectOrder(_hrsc: maptype.HRSC, _incode: int, _order: int) -> int:
        """
        Записать порядок вывода объекта в слое
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _order: порядок вывода с ``0`` до ``255``, где ``0`` - вывод в стандартном порядке Устанавливает порядок вывода объекта в слое, в данной локализации
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscObjectOrder_t (_hrsc, _incode, _order)

    mapGetRscObjectDirect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectDirect', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectDirect(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить направление цифрования объекта по внутреннему коду
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectDirect_t (_hrsc, _incode)

    mapGetRscObjDesignFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjDesignFlag', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjDesignFlag(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить признак объекта оформления
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :returns: Возвращает: ``0`` - обычный объект, ``1`` - объект оформления
        :rtype: int
        """
        return mapGetRscObjDesignFlag_t (_hrsc, _incode)

    mapSetRscObjDesignFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscObjDesignFlag', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapSetRscObjDesignFlag(_hrsc: maptype.HRSC, _incode: int, _flag: int) -> int:
        """
        Установить признак объекта оформления
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _flag: признак объекта оформления (``0`` или ``1``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscObjDesignFlag_t (_hrsc, _incode, _flag)

    mapGetRscObjectMultiContourFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectMultiContourFlag', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectMultiContourFlag(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить признак мультиконтурного объекта для полигонов или линейных объектов
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :returns: Возвращает признак мультиконтурного объекта: 0/1 При сортировке могут формироваться упрощенные контура для отображения в мелких масштабах При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectMultiContourFlag_t (_hrsc, _incode)

    mapSetRscObjectMultiContourFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscObjectMultiContourFlag', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapSetRscObjectMultiContourFlag(_hrsc: maptype.HRSC, _incode: int, _flag: int) -> int:
        """
        Установить признак мультиконтурного объекта для полигонов или линейных объектов
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _flag: признак мультиконтурного объекта: ``0``/``1`` (при сортировке могут формироваться упрощенные контура для отображения в мелких масштабах)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscObjectMultiContourFlag_t (_hrsc, _incode, _flag)

    mapGetRscObjectPolygonPointFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectPolygonPointFlag', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectPolygonPointFlag(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить признак Полигон с подобъектом-точкой для отображения точечного знака
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :returns: Возвращает признак полигона с подобъектом-точкой (0/1) При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectPolygonPointFlag_t (_hrsc, _incode)

    mapSetRscObjectPolygonPointFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscObjectPolygonPointFlag', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapSetRscObjectPolygonPointFlag(_hrsc: maptype.HRSC, _incode: int, _flag: int) -> int:
        """
        Установить признак Полигон с подобъектом-точкой для отображения точечного знака
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _flag: признак полигона с подобъектом-точкой (``0``/``1``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscObjectPolygonPointFlag_t (_hrsc, _incode, _flag)

    mapGetMetaObjectFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMetaObjectFlag', maptype.HRSC, ctypes.c_long)
    def mapGetMetaObjectFlag(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить признак метаобъекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: порядковый номер объекта с ``1``
        
        :returns: Возвращает признак метаобъекта (0/1) При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMetaObjectFlag_t (_hrsc, _incode)

    mapSetMetaObjectFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMetaObjectFlag', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapSetMetaObjectFlag(_hrsc: maptype.HRSC, _incode: int, _flag: int) -> int:
        """
        Установить признак метаобъекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: порядковый номер объекта с ``1``
        
        :param _flag: признак метаобъекта (``0``/``1``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMetaObjectFlag_t (_hrsc, _incode, _flag)

    mapGetMetaObjectFlagWithoutMetric_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMetaObjectFlagWithoutMetric', maptype.HRSC, ctypes.c_long)
    def mapGetMetaObjectFlagWithoutMetric(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить признак метаобъекта без метрики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: порядковый номер объекта с ``1``
        
        :returns: Возвращает признак метаобъекта без метрики (0/1) При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMetaObjectFlagWithoutMetric_t (_hrsc, _incode)

    mapSetMetaObjectFlagWithoutMetric_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMetaObjectFlagWithoutMetric', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapSetMetaObjectFlagWithoutMetric(_hrsc: maptype.HRSC, _incode: int, _flag: int) -> int:
        """
        Установить признак метаобъекта без метрики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: порядковый номер объекта с ``1``
        
        :param _flag: признак метаобъекта без метрики (``0``/``1``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMetaObjectFlagWithoutMetric_t (_hrsc, _incode, _flag)

    mapGetRscObjectFunction_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectFunction', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectFunction(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить номер функции отображения объекта по внутреннему коду
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectFunction_t (_hrsc, _incode)

    mapGetRscObjectParametersSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectParametersSize', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectParametersSize(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить длину параметров отображения объекта по внутреннему коду
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectParametersSize_t (_hrsc, _incode)

    mapGetRscObjectParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetRscObjectParameters', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectParameters(_hrsc: maptype.HRSC, _incode: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить параметры отображения объекта по внутреннему коду
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetRscObjectParameters_t (_hrsc, _incode)

    mapGetRscObjectMarkView_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetRscObjectMarkView', maptype.HRSC, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapGetRscObjectMarkView(_hrsc: maptype.HRSC, _identnumber: int, _size: ctypes.POINTER(ctypes.c_long)) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить внешний вид объекта - ссылка на файл в памяти
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _identnumber: идентификатор графического файла в памяти, полученный из структуры ``IMGGRAPHICFILE``
        
        :param _size: возвращаемый размер файла в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetRscObjectMarkView_t (_hrsc, _identnumber, _size)

    mapGetRscPrimitiveCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscPrimitiveCount', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapGetRscPrimitiveCount(_hrsc: maptype.HRSC, _incode: int, _viewtype: int) -> int:
        """
        Запросить количество примитивов в параметрах отображения объекта по внутреннему коду и виду отображения
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _viewtype: вид отображения: ``0`` - экранный, ``1`` - принтерный
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscPrimitiveCount_t (_hrsc, _incode, _viewtype)

    mapGetRscPrimitiveFunction_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscPrimitiveFunction', maptype.HRSC, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapGetRscPrimitiveFunction(_hrsc: maptype.HRSC, _incode: int, _number: int, _viewtype: int) -> int:
        """
        Запросить номер функции отображения примитива по порядковому номеру примитива, внутреннему коду и виду отображения
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта (номер по порядку)
        
        :param _number: номер примитива в параметрах отображения объекта
        
        :param _viewtype: вид отображения: ``0`` - экранный, ``1`` - принтерный
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscPrimitiveFunction_t (_hrsc, _incode, _number, _viewtype)

    mapGetRscPrimitiveLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscPrimitiveLength', maptype.HRSC, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapGetRscPrimitiveLength(_hrsc: maptype.HRSC, _incode: int, _number: int, _viewtype: int) -> int:
        """
        Запросить длину параметров примитива по порядковому номеру примитива, внутреннему коду и виду отображения
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта (номер по порядку)
        
        :param _number: номер примитива в параметрах отображения объекта
        
        :param _viewtype: вид отображения: ``0`` - экранный, ``1`` - принтерный
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscPrimitiveLength_t (_hrsc, _incode, _number, _viewtype)

    mapGetRscPrimitiveParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetRscPrimitiveParameters', maptype.HRSC, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapGetRscPrimitiveParameters(_hrsc: maptype.HRSC, _incode: int, _number: int, _viewtype: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить адрес параметров примитива по порядковому номеру примитива, внутреннему коду и виду отображения
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта (номер по порядку)
        
        :param _number: номер примитива в параметрах отображения объекта
        
        :param _viewtype: вид отображения: ``0`` - экранный, ``1`` - принтерный
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetRscPrimitiveParameters_t (_hrsc, _incode, _number, _viewtype)

    mapGetRscImageSuitable_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscImageSuitable', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapGetRscImageSuitable(_hrsc: maptype.HRSC, _local: int, _incode: int) -> int:
        """
        Проверить соответствие локализации и вида отображения объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _local: тип локализации
        
        :param _incode: внутренний код объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscImageSuitable_t (_hrsc, _local, _incode)

    mapSetRscObjectImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscObjectImage', maptype.HRSC, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_char_p)
    def mapSetRscObjectImage(_hrsc: maptype.HRSC, _incode: int, _length: int, _number: int, _param: ctypes.c_char_p) -> int:
        """
        Установить внешний вид объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _length: длина параметров
        
        :param _number: номер функции отображения
        
        :param _param: указатель на параметры функции
        
        :returns: При ошибке возвращает ноль, иначе порядковый номер объекта
        :rtype: int
        """
        return mapSetRscObjectImage_t (_hrsc, _incode, _length, _number, _param)

    mapGetRscPrintObjectFunction_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscPrintObjectFunction', maptype.HRSC, ctypes.c_long)
    def mapGetRscPrintObjectFunction(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить номер функции принтерного отображения объекта по внутреннему коду
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscPrintObjectFunction_t (_hrsc, _incode)

    mapGetRscPrintObjectParametersSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscPrintObjectParametersSize', maptype.HRSC, ctypes.c_long)
    def mapGetRscPrintObjectParametersSize(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить длину параметров принтерного отображения объекта по внутреннему  коду
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscPrintObjectParametersSize_t (_hrsc, _incode)

    mapGetRscPrintObjectParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetRscPrintObjectParameters', maptype.HRSC, ctypes.c_long)
    def mapGetRscPrintObjectParameters(_hrsc: maptype.HRSC, _incode: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить параметры принтерного отображения объекта по внутреннему коду объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetRscPrintObjectParameters_t (_hrsc, _incode)

    mapSetRscPrintObjectImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscPrintObjectImage', maptype.HRSC, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_char_p)
    def mapSetRscPrintObjectImage(_hrsc: maptype.HRSC, _incode: int, _length: int, _number: int, _param: ctypes.c_char_p) -> int:
        """
        Установить принтерный вид объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _length: длина параметров
        
        :param _number: номер функции отображения
        
        :param _param: указатель на параметры функции
        
        :returns: При ошибке возвращает ноль, иначе порядковый номер объекта
        :rtype: int
        """
        return mapSetRscPrintObjectImage_t (_hrsc, _incode, _length, _number, _param)

    mapGetRscObjectBaseColor_t = mapsyst.GetProcAddress(acceslib,maptype.COLORREF,'mapGetRscObjectBaseColor', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapGetRscObjectBaseColor(_hrsc: maptype.HRSC, _incode: int, _viewtype: int) -> maptype.COLORREF:
        """
        Найти "основной" цвет изображения объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _viewtype: вид отображения:  ``0`` - экранный, ``1`` - принтерный
        
        :returns: При отсутствии цвета возвращает ``0xFF000000`` При ошибке возвращает 0
        :rtype: maptype.COLORREF
        """
        return mapGetRscObjectBaseColor_t (_hrsc, _incode, _viewtype)

    mapGetRscObjectFont_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectFont', maptype.HRSC, ctypes.c_long, ctypes.POINTER(maptype.LOGFONTW), ctypes.c_long)
    def mapGetRscObjectFont(_hrsc: maptype.HRSC, _incode: int, _font: ctypes.POINTER(maptype.LOGFONTW), _viewtype: int) -> int:
        """
        Запросить параметры шрифта объекта по внутреннему коду
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _font: описание шрифта, структура ``LOGFONTW`` описана в mapsyst.h
        
        :param _viewtype: вид отображения:  ``0`` - экранный, ``1`` - принтерный
        
        :returns: При ошибке или если в параметрах объекта нет подписи возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectFont_t (_hrsc, _incode, _font, _viewtype)

    mapGetRscTextFont_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscTextFont', maptype.HRSC, ctypes.POINTER(mapgdi.IMGTEXT), ctypes.POINTER(maptype.LOGFONTW))
    def mapGetRscTextFont(_hrsc: maptype.HRSC, _text: ctypes.POINTER(mapgdi.IMGTEXT), _font: ctypes.POINTER(maptype.LOGFONTW)) -> int:
        """
        Заполнить параметры шрифта по параметрам текста
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _text: параметры функции отображения текста
        
        :param _font: возвращаемые параметры шрифта Параметры шрифта заполняются корректно, если среди открытых карт есть карта с переданным идентификатором классификатора Размер шрифта вычисляется для базового масштаба карты с текущим разрешением экрана
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscTextFont_t (_hrsc, _text, _font)

    mapGetRscTemplateTable_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscTemplateTable', maptype.HRSC, ctypes.c_long, ctypes.POINTER(mapgdi.TABLETEMPLATE))
    def mapGetRscTemplateTable(_hrsc: maptype.HRSC, _incode: int, _table: ctypes.POINTER(mapgdi.TABLETEMPLATE)) -> int:
        """
        Запросить таблицу отображения шаблонов по внутреннему коду объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _table: указатель на структуру ``TABLETEMPLATE`` (определено в mapgdi.h)
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRscTemplateTable_t (_hrsc, _incode, _table)

    mapGetRscObjectLabelSemantics_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectLabelSemantics', maptype.HRSC, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_int))
    def mapGetRscObjectLabelSemantics(_hrsc: maptype.HRSC, _incode: int, _viewtype: int, _size: int, _code: ctypes.POINTER(ctypes.c_int)) -> int:
        """
        Запросить список кодов семантик, формирующих подписи в векторных знаках, являющихся частью вида объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _viewtype: вид отображения: ``0`` - экранный, ``1`` - принтерный, ``2`` - все
        
        :param _size: размерность массива (количество элементов)
        
        :param _code: адрес массива кодов семантики
        
        :returns: Возвращает число семантик, от которых зависят подписи Если размер массива меньше, чем число семантик ``"лишние"`` семантики не пишутся
        :rtype: int
        """
        return mapGetRscObjectLabelSemantics_t (_hrsc, _incode, _viewtype, _size, _code)

    mapDeleteRscPrintObjectParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRscPrintObjectParameters', maptype.HRSC, ctypes.c_long)
    def mapDeleteRscPrintObjectParameters(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Удалить принтерный вид объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteRscPrintObjectParameters_t (_hrsc, _incode)

    mapCheckRscTextFlagHorizontal_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckRscTextFlagHorizontal', maptype.HRSC, ctypes.c_long)
    def mapCheckRscTextFlagHorizontal(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Проверить в параметрах объекта наличие флага горизонтальности шрифта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :returns: возвращает 1, иначе ноль
        :rtype: int
        
        .. note::

           Если в параметрах есть текст или векторный с признаком горизонтальности
        """
        return mapCheckRscTextFlagHorizontal_t (_hrsc, _incode)

    mapFillRscTextSemanticBuff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapFillRscTextSemanticBuff', maptype.HRSC, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.c_long)
    def mapFillRscTextSemanticBuff(_hrsc: maptype.HRSC, _incode: int, _semcode: ctypes.POINTER(ctypes.c_long), _buffsize: int) -> int:
        """
        Заполнить массив семантик, влияющих на подписи у объектов с функцией отображения IMG_VECTOREX, по внутреннему коду объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _semcode: буфер для записи внешних кодов семантик для текстов (желательно выделять место не менее ``16 *`` sizeof(int)
        
        :param _buffsize: размер буфера в байтах
        
        :returns: Если в параметрах нет векторных или в них нет текстов по семантике возвращает 0 Возвращает общее количество семантик влияющих на подписи, заполняет semcode Если возвращаемое количество больше, чем входит в буфер - увеличьте буфер, сделайте повторный вызов
        :rtype: int
        """
        return mapFillRscTextSemanticBuff_t (_hrsc, _incode, _semcode, _buffsize)

    mapFillRscSemanticBuff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapFillRscSemanticBuff', maptype.HRSC, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.c_long)
    def mapFillRscSemanticBuff(_hrsc: maptype.HRSC, _incode: int, _flag: int, _semcode: ctypes.POINTER(ctypes.c_long), _buffsize: int) -> int:
        """
        Заполннить массив семантик по внутреннему коду объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _flag: тип семантики (из maptype.h ``SEMANTIC_FOR_OBJECT``)
        
        :param _semcode: буфер для записи внешних кодов семантик (желательно выделять место не менее ``16 *`` sizeof(int)
        
        :param _buffsize: размер буфера в байтах
        
        :returns: Если нет семантик возвращает 0 Возвращает общее количество семантик с учетом флага, заполняет semcode Если возвращаемое количество больше, чем входит в буфер - увеличьте буфер, сделайте повторный вызов
        :rtype: int
        """
        return mapFillRscSemanticBuff_t (_hrsc, _incode, _flag, _semcode, _buffsize)

    mapGetRscObjectPressure_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectPressure', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectPressure(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить флаг сжатия изображения объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :returns: Возвращает: ``0`` - изображение сжимается, ``1`` - нет.
        :rtype: int
        """
        return mapGetRscObjectPressure_t (_hrsc, _incode)

    mapSetRscObjectPressure_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscObjectPressure', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapSetRscObjectPressure(_hrsc: maptype.HRSC, _incode: int, _flag: int) -> int:
        """
        Установить флаг сжатия изображения объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _flag: флаг сжатия изображения: ``0`` - сжимается, ``1`` - нет
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscObjectPressure_t (_hrsc, _incode, _flag)

    mapGetRscObjectPressLimit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectPressLimit', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectPressLimit(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить размер максимального сжатия изображения объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :returns: Возвращает коэффициент максимального сжатия, умноженный на 10
        :rtype: int
        """
        return mapGetRscObjectPressLimit_t (_hrsc, _incode)

    mapSetRscObjectPressLimit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscObjectPressLimit', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapSetRscObjectPressLimit(_hrsc: maptype.HRSC, _incode: int, _presslimit: int) -> int:
        """
        Установить размер максимального сжатия изображения объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _presslimit: коэффициент максимального сжатия, умноженный на ``10`` (в интервале от ``10`` до ``250``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscObjectPressLimit_t (_hrsc, _incode, _presslimit)

    mapGetRscObjectScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectScale', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectScale(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить флаг масштабирования изображения объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :returns: Возвращает: ``1`` - изображение масштабируется, ``0`` - нет
        :rtype: int
        """
        return mapGetRscObjectScale_t (_hrsc, _incode)

    mapSetRscObjectScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscObjectScale', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapSetRscObjectScale(_hrsc: maptype.HRSC, _incode: int, _flag: int) -> int:
        """
        Установить флаг масштабирования изображения объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _flag: флаг масштабирования изображения: ``1`` - масштабируется, ``0`` - нет
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscObjectScale_t (_hrsc, _incode, _flag)

    mapGetRscObjectScaleLimit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectScaleLimit', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectScaleLimit(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить размер максимального увеличения изображения объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :returns: Возвращает коэффициент максимального увеличения, умноженный на 10
        :rtype: int
        """
        return mapGetRscObjectScaleLimit_t (_hrsc, _incode)

    mapSetRscObjectScaleLimit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscObjectScaleLimit', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapSetRscObjectScaleLimit(_hrsc: maptype.HRSC, _incode: int, _scalelimit: int) -> int:
        """
        Установить размер максимального увеличения изображения объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _scalelimit: коэффициент максимального сжатия, умноженный на ``10`` (в интервале от ``10`` до ``250``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscObjectScaleLimit_t (_hrsc, _incode, _scalelimit)

    mapSetRscObjectScaleBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscObjectScaleBorder', maptype.HRSC, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSetRscObjectScaleBorder(_hrsc: maptype.HRSC, _incode: int, _bottom: int, _top: int) -> int:
        """
        Установить границы видимости объекта на карте - диапазон масштабов видимости объекта на карте
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: порядковый номер объекта (внутренний код в классификаторе)
        
        :param _bottom: минимальное значение знаменателя масштаба при котором виден объект
        
        :param _top: максимальное значение знаменателя масштаба при котором виден объект Например: объект виден в диапазоне от ``1:300 000`` (top) до ``1:15 000`` (bottom)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscObjectScaleBorder_t (_hrsc, _incode, _bottom, _top)

    mapGetRscObjectScaleBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectScaleBorder', maptype.HRSC, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapGetRscObjectScaleBorder(_hrsc: maptype.HRSC, _incode: int, _bottom: ctypes.POINTER(ctypes.c_long), _top: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить границы видимости объекта на карте - диапазон масштабов видимости объекта на карте
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _bottom: минимальное значение знаменателя масштаба при котором виден объект
        
        :param _top: максимальное значение знаменателя масштаба при котором виден объект
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscObjectScaleBorder_t (_hrsc, _incode, _bottom, _top)

    mapGetRscObjectBotScaleInclude_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectBotScaleInclude', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectBotScaleInclude(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить вхождение верхней границы видимости объекта на карте в диапазон видимости
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :returns: Если входит возвращает 1, иначе 0
        :rtype: int
        """
        return mapGetRscObjectBotScaleInclude_t (_hrsc, _incode)

    mapGetRscObjectTopScaleInclude_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscObjectTopScaleInclude', maptype.HRSC, ctypes.c_long)
    def mapGetRscObjectTopScaleInclude(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить вхождение нижней границы видимости объекта на карте в диапазон видимости
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :returns: Если входит возвращает 1, иначе 0
        :rtype: int
        """
        return mapGetRscObjectTopScaleInclude_t (_hrsc, _incode)

    mapAppendRscSemanticEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendRscSemanticEx', maptype.HRSC, ctypes.POINTER(maptype.RSCSEMANTICEX))
    def mapAppendRscSemanticEx(_hrsc: maptype.HRSC, _rsem: ctypes.POINTER(maptype.RSCSEMANTICEX)) -> int:
        """
        Создать новую семантику
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _rsem: описание семантики объекта, структура ``RSCSEMANTICEX`` описана в maptype.h
        
        :returns: Возвращает код созданной семантики При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendRscSemanticEx_t (_hrsc, _rsem)

    mapUpdateRscSemanticEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateRscSemanticEx', maptype.HRSC, ctypes.c_long, ctypes.POINTER(maptype.RSCSEMANTICEX), ctypes.c_long)
    def mapUpdateRscSemanticEx(_hrsc: maptype.HRSC, _code: int, _rsem: ctypes.POINTER(maptype.RSCSEMANTICEX), _classupdate: int) -> int:
        """
        Обновить семантику
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код обновляемой семантики
        
        :param _rsem: описание семантики объекта, структура ``RSCSEMANTICEX`` описана в maptype.h
        
        :param _classupdate: флаг обновления: ``1`` - классификатор семантики удаляется для последующего обновления (например при смене типа семантики) ``0`` - тип семантики остается прежний и обновления классификатора данной семантики не нужно
        
        :returns: Возвращает код обновленной семантики При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdateRscSemanticEx_t (_hrsc, _code, _rsem, _classupdate)

    mapDeleteRscSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRscSemantic', maptype.HRSC, ctypes.c_long)
    def mapDeleteRscSemantic(_hrsc: maptype.HRSC, _code: int) -> int:
        """
        Удалить семантику
        
        :param _code: код удаляемой семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteRscSemantic_t (_hrsc, _code)

    mapGetRscApplySemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscApplySemantic', maptype.HRSC, ctypes.c_long, ctypes.POINTER(maptype.APPLYSEMANTIC))
    def mapGetRscApplySemantic(_hrsc: maptype.HRSC, _code: int, _applysemantic: ctypes.POINTER(maptype.APPLYSEMANTIC)) -> int:
        """
        Запросить информацию о применении семантики для объектов карты
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _applysemantic: структура для информации (``APPLYSEMANTIC`` описана в maptype.h)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscApplySemantic_t (_hrsc, _code, _applysemantic)

    mapEnableRscSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapEnableRscSemantic', maptype.HRSC, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapEnableRscSemantic(_hrsc: maptype.HRSC, _incode: int, _code: int, _enable: int) -> int:
        """
        Объявить принадлежность семантики объекту
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта
        
        :param _code: код семантики
        
        :param _enable: код доступа к семантике: ``2`` - обязательная, ``1`` - возможная
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapEnableRscSemantic_t (_hrsc, _incode, _code, _enable)

    mapGetRscSemanticCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticCount', maptype.HRSC)
    def mapGetRscSemanticCount(_hrsc: maptype.HRSC) -> int:
        """
        Запросить количество семантик в классификаторе
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSemanticCount_t (_hrsc)

    mapGetRscSemanticCodeByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticCodeByNumber', maptype.HRSC, ctypes.c_long)
    def mapGetRscSemanticCodeByNumber(_hrsc: maptype.HRSC, _number: int) -> int:
        """
        Запросить код семантики по порядковому номеру
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: порядковый номер семантики с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSemanticCodeByNumber_t (_hrsc, _number)

    mapGetRscSemanticCodeByKeyUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticCodeByKeyUn', maptype.HRSC, maptype.PWCHAR)
    def mapGetRscSemanticCodeByKeyUn(_hrsc: maptype.HRSC, _key: mapsyst.WTEXT) -> int:
        """
        Запросить код семантики по короткому имени семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _key: короткое имя семантики (ключ)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSemanticCodeByKeyUn_t (_hrsc, _key.buffer())

    mapGetRscSemanticByShortNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticByShortNameUn', maptype.HRSC, maptype.PWCHAR)
    def mapGetRscSemanticByShortNameUn(_hrsc: maptype.HRSC, _shortname: mapsyst.WTEXT) -> int:
        """
        Запросить порядковый номер семантики по короткому имени семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _shortname: короткое имя семантики (ключ)
        
        :returns: При ошибке возвращает ноль, иначе - порядковый номер семантики с 1
        :rtype: int
        """
        return mapGetRscSemanticByShortNameUn_t (_hrsc, _shortname.buffer())

    mapGetRscSemanticByKeyUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticByKeyUn', maptype.HRSC, maptype.PWCHAR)
    def mapGetRscSemanticByKeyUn(_hrsc: maptype.HRSC, _key: mapsyst.WTEXT) -> int:
        """
        Запросить порядковый номер семантики по короткому имени семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _key: короткое имя семантики (ключ)
        
        :returns: При ошибке возвращает ноль, иначе - порядковый номер семантики с 1
        :rtype: int
        """
        return mapGetRscSemanticByKeyUn_t (_hrsc, _key.buffer())

    mapGetRscSemanticNameByNumberUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticNameByNumberUn', maptype.HRSC, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetRscSemanticNameByNumberUn(_hrsc: maptype.HRSC, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить название семантики по порядковому номеру
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер семантики
        
        :param _name: адрес строки для размещения результата
        
        :param _size: максимальный размер выходной строки
        
        :returns: При ошибке возвращает пустую строку
        :rtype: int
        """
        return mapGetRscSemanticNameByNumberUn_t (_hrsc, _number, _name.buffer(), _size)

    mapGetRscSemanticNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticNameUn', maptype.HRSC, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetRscSemanticNameUn(_hrsc: maptype.HRSC, _code: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить название семантики по коду в кодировке UTF-16
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _name: адрес строки для размещения результата
        
        :param _size: максимальный размер выходной строки в байтах (может быть до ``2048`` байт)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSemanticNameUn_t (_hrsc, _code, _name.buffer(), _size)

    mapSetRscSemanticNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscSemanticNameUn', maptype.HRSC, ctypes.c_long, maptype.PWCHAR)
    def mapSetRscSemanticNameUn(_hrsc: maptype.HRSC, _code: int, _name: mapsyst.WTEXT) -> int:
        """
        Установить название семантики по коду в кодировке UTF-16
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _name: адрес строки с новым названием
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscSemanticNameUn_t (_hrsc, _code, _name.buffer())

    mapGetRscSemanticTypeByCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticTypeByCode', maptype.HRSC, ctypes.c_long)
    def mapGetRscSemanticTypeByCode(_hrsc: maptype.HRSC, _code: int) -> int:
        """
        Запросить тип семантики по ее внешнему коду
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: внешний код семантики Коды типов семантик ``SEMTYPE`` описаны maptype.h
        
        :returns: При ошибке возвращает ноль (символьная семантика имеет тип ноль!)
        :rtype: int
        """
        return mapGetRscSemanticTypeByCode_t (_hrsc, _code)

    mapGetRscSemanticKeyUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticKeyUn', maptype.HRSC, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetRscSemanticKeyUn(_hrsc: maptype.HRSC, _code: int, _shortname: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить короткое имя (ключ) семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _shortname: короткое имя семантики (ключ)
        
        :param _size: размер выходной строки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSemanticKeyUn_t (_hrsc, _code, _shortname.buffer(), _size)

    mapGetRscSemanticShortNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticShortNameUn', maptype.HRSC, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetRscSemanticShortNameUn(_hrsc: maptype.HRSC, _code: int, _shortname: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить короткое имя (ключ) семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _shortname: короткое имя семантики (ключ)
        
        :param _size: размер выходной строки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSemanticShortNameUn_t (_hrsc, _code, _shortname.buffer(), _size)

    mapSetRscSemanticShortNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscSemanticShortNameUn', maptype.HRSC, ctypes.c_long, maptype.PWCHAR)
    def mapSetRscSemanticShortNameUn(_hrsc: maptype.HRSC, _code: int, _shortname: mapsyst.WTEXT) -> int:
        """
        Установить короткое имя (ключ) семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _shortname: короткое имя семантики (ключ)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscSemanticShortNameUn_t (_hrsc, _code, _shortname.buffer())

    mapSetRscSemanticDecimal_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscSemanticDecimal', maptype.HRSC, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSetRscSemanticDecimal(_hrsc: maptype.HRSC, _code: int, _size: int, _decimal: int) -> int:
        """
        Установить размер и точность значения семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _size: размер значения семантики, включая десятичную точку
        
        :param _decimal: количество знаков после запятой (у символьных - ``0``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscSemanticDecimal_t (_hrsc, _code, _size, _decimal)

    mapGetRscSemanticForObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticForObject', maptype.HRSC, ctypes.POINTER(maptype.RSCSEMANTICEX), ctypes.c_long, ctypes.c_long)
    def mapGetRscSemanticForObject(_hrsc: maptype.HRSC, _semtype: ctypes.POINTER(maptype.RSCSEMANTICEX), _semcode: int, _objectcode: int) -> int:
        """
        Заполнить расширенную структуру описания семантической характеристики по коду семантики и коду объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _semtype: описание семантики объекта, структура ``RSCSEMANTICEX`` описана в maptype.h
        
        :param _semcode: внешний код семантики
        
        :param _objectcode: внутренний код объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSemanticForObject_t (_hrsc, _semtype, _semcode, _objectcode)

    mapGetRscSemanticExByCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticExByCode', maptype.HRSC, ctypes.POINTER(maptype.RSCSEMANTICEX), ctypes.c_long)
    def mapGetRscSemanticExByCode(_hrsc: maptype.HRSC, _semtype: ctypes.POINTER(maptype.RSCSEMANTICEX), _code: int) -> int:
        """
        Заполнить структуру описания семантической характеристики по коду семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _semtype: описание семантики объекта, структура ``RSCSEMANTICEX`` описана в maptype.h
        
        :param _code: внешний код семантики
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSemanticExByCode_t (_hrsc, _semtype, _code)

    mapGetRscSemanticClassificatorCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticClassificatorCount', maptype.HRSC, ctypes.c_long)
    def mapGetRscSemanticClassificatorCount(_hrsc: maptype.HRSC, _code: int) -> int:
        """
        Запросить количество значений классификатора семантической характеристики по коду семантики, если ее тип TCODE
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSemanticClassificatorCount_t (_hrsc, _code)

    mapGetRscSemanticClassificatorNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticClassificatorNameUn', maptype.HRSC, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetRscSemanticClassificatorNameUn(_hrsc: maptype.HRSC, _code: int, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить название значения характеристики из классификатора семантики по коду семантики и номеру в классификаторе
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _number: последовательный номер в классификаторе(``1``,``2``,``3``...)
        
        :param _name: адрес строки для размещения результата
        
        :param _size: максимальный размер строки (может быть до ``2048`` байт)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSemanticClassificatorNameUn_t (_hrsc, _code, _number, _name.buffer(), _size)

    mapGetRscSemanticClassificatorCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticClassificatorCode', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapGetRscSemanticClassificatorCode(_hrsc: maptype.HRSC, _code: int, _number: int) -> int:
        """
        Запросить код значения характеристики из классификатора семантики по коду семантики и номеру в классификаторе
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _number: последовательный номер в классификаторе(``1``,``2``,``3``...)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSemanticClassificatorCode_t (_hrsc, _code, _number)

    mapAppendRscClassificatorUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendRscClassificatorUn', maptype.HRSC, ctypes.c_long, ctypes.c_long, maptype.PWCHAR)
    def mapAppendRscClassificatorUn(_hrsc: maptype.HRSC, _code: int, _value: int, _name: mapsyst.WTEXT) -> int:
        """
        Записать новую "строчку" классификатора - числовое значение и символьное
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантической характеристики
        
        :param _value: числовое значение
        
        :param _name: символьное значение семантической характеристики
        
        :returns: Возвращает номер записанной строки с 1 При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendRscClassificatorUn_t (_hrsc, _code, _value, _name.buffer())

    mapUpdateRscClassificatorNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateRscClassificatorNameUn', maptype.HRSC, ctypes.c_long, ctypes.c_long, maptype.PWCHAR)
    def mapUpdateRscClassificatorNameUn(_hrsc: maptype.HRSC, _code: int, _index: int, _name: mapsyst.WTEXT) -> int:
        """
        Обновить символьное значение классификатора по номеру строки
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантической характеристики
        
        :param _index: номер строки с ``1``
        
        :param _name: символьное значение семантической характеристики
        
        :returns: Возвращает номер исправленной строки с 1 При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdateRscClassificatorNameUn_t (_hrsc, _code, _index, _name.buffer())

    mapGetRscClsAbbreviationUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscClsAbbreviationUn', maptype.HRSC, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetRscClsAbbreviationUn(_hrsc: maptype.HRSC, _code: int, _value: int, _buffer: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить сокращенное имя перечислимой семантики по коду семантики и значению перечислимой семантики
        
        :param _code: код семантики
        
        :param _value: код перечислимой семантики (``"Код из классификатора (список)"``)
        
        :param _size: размер буфера для размещения строки (``64`` байта)
        
        :param _buffer: буфер для размещения выходной строки - сокращенного имени (Псевдонима)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscClsAbbreviationUn_t (_hrsc, _code, _value, _buffer.buffer(), _size)

    mapSetRscClsAbbreviationUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscClsAbbreviationUn', maptype.HRSC, ctypes.c_long, ctypes.c_long, maptype.PWCHAR)
    def mapSetRscClsAbbreviationUn(_hrsc: maptype.HRSC, _code: int, _value: int, _buffer: mapsyst.WTEXT) -> int:
        """
        Записать сокращенное имя  перечислимой семантики в UTF-16 по коду семантики и значению перечислимой семантики
        
        :param _code: код семантики
        
        :param _value: код перечислимой семантики (``"Код из классификатора (список)"``)
        
        :param _buffer: сокращенное значение классификатора (Псевдоним), не более ``31`` символа в UNICODE
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscClsAbbreviationUn_t (_hrsc, _code, _value, _buffer.buffer())

    mapDeleteRscClsAbbreviationUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRscClsAbbreviationUn', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapDeleteRscClsAbbreviationUn(_hrsc: maptype.HRSC, _code: int, _value: int) -> int:
        """
        Удалить сокращенное имя перечислимой семантики в UTF-16 по коду семантики и значению перечислимой семантики
        
        :param _code: код семантики
        
        :param _value: код перечислимой семантики (``"Код из классификатора (список)"``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteRscClsAbbreviationUn_t (_hrsc, _code, _value)

    mapFindRscClassificatorCodePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapFindRscClassificatorCodePro', maptype.HRSC, ctypes.c_long, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long))
    def mapFindRscClassificatorCodePro(_hrsc: maptype.HRSC, _code: int, _name: mapsyst.WTEXT, _errorcode: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Найти код записи семантики-классификатора по строковому значению
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантической характеристики типа классификатор
        
        :param _name: символьное значение семантической характеристики, которое нужно найти
        
        :param _errorcode: при ошибке записывает код ошибки (``IDS_NOTFOUND``, ...) Поиск осуществляется по совпадению заданной строки с коротким (Псевдоним) и полным именем в семантике-классификаторе
        
        :returns: Если не нашли возвращает ноль, иначе - числовое значение классификатора семантики
        :rtype: int
        
        .. note::

           Если код записи по именам не найден, то еще выполняет поиск по ключу
        """
        return mapFindRscClassificatorCodePro_t (_hrsc, _code, _name.buffer(), _errorcode)

    mapGetRscClsKeyUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscClsKeyUn', maptype.HRSC, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetRscClsKeyUn(_hrsc: maptype.HRSC, _code: int, _value: int, _key: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить ключ строки классификатора семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _value: значение классификатора
        
        :param _key: поле для записи значения
        
        :param _size: длина поля в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscClsKeyUn_t (_hrsc, _code, _value, _key.buffer(), _size)

    mapSetRscClsKeyUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscClsKeyUn', maptype.HRSC, ctypes.c_long, ctypes.c_long, maptype.PWCHAR)
    def mapSetRscClsKeyUn(_hrsc: maptype.HRSC, _code: int, _value: int, _key: mapsyst.WTEXT) -> int:
        """
        Записать ключ классификатора семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _value: значение классификатора
        
        :param _key: новое значение ключа (должно быть уникальным для данного кода семантики) Для одной семантики ключ классификатора должен быть уникален
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscClsKeyUn_t (_hrsc, _code, _value, _key.buffer())

    mapGetRscSemanticClassificatorFullNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticClassificatorFullNameUn', maptype.HRSC, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_int)
    def mapGetRscSemanticClassificatorFullNameUn(_hrsc: maptype.HRSC, _code: int, _value: int, _buffer: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить полное имя классификатора семантики в UTF-16 по коду семантики и значению классификатора
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _value: значение классификатора
        
        :param _size: размер буфера для размещения строки
        
        :param _buffer: буфер для размещения строки
        
        :returns: Возвращает длину полного имени При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSemanticClassificatorFullNameUn_t (_hrsc, _code, _value, _buffer.buffer(), _size)

    mapSetRscClsFullNameEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscClsFullNameEx', maptype.HRSC, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR)
    def mapSetRscClsFullNameEx(_hrsc: maptype.HRSC, _code: int, _value: int, _name: mapsyst.WTEXT, _shortname: mapsyst.WTEXT) -> int:
        """
        Записать полное имя значения классификатора семантики UTF-16 по коду семантики и значению классификатора
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _value: значение классификатора
        
        :param _name: полное имя записи
        
        :param _shortname: короткое имя записи
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscClsFullNameEx_t (_hrsc, _code, _value, _name.buffer(), _shortname.buffer())

    mapRscSemanticClassificatorShortName_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapRscSemanticClassificatorShortName', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapRscSemanticClassificatorShortName(_hrsc: maptype.HRSC, _code: int, _value: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить короткое имя классификатора семантики по коду семантики и числовому значению классификатора
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _value: значение классификатора
        
        :returns: При ошибке возвращает адрес пустой строки, при успешном выполнении - адрес строки
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapRscSemanticClassificatorShortName_t (_hrsc, _code, _value)

    mapGetRscClsKeyValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscClsKeyValue', maptype.HRSC, ctypes.c_long, ctypes.c_char_p)
    def mapGetRscClsKeyValue(_hrsc: maptype.HRSC, _code: int, _key: ctypes.c_char_p) -> int:
        """
        Запросить значение классификатора семантики по ключу
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _key: ключ
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscClsKeyValue_t (_hrsc, _code, _key)

    mapGetRscSemantic3DListFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemantic3DListFlag', maptype.HRSC, ctypes.c_long)
    def mapGetRscSemantic3DListFlag(_hrsc: maptype.HRSC, _code: int) -> int:
        """
        Запросить является ли семантика списком 3D изображений по коду
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :returns: Если семантика - список 3D изображений возвращает 1 При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSemantic3DListFlag_t (_hrsc, _code)

    mapSetRscSemantic3DListFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscSemantic3DListFlag', maptype.HRSC, ctypes.c_long)
    def mapSetRscSemantic3DListFlag(_hrsc: maptype.HRSC, _code: int) -> int:
        """
        Установить признак семантики - список 3D изображений
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscSemantic3DListFlag_t (_hrsc, _code)

    mapGetRscSemanticRoundUpFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticRoundUpFlag', maptype.HRSC, ctypes.c_long)
    def mapGetRscSemanticRoundUpFlag(_hrsc: maptype.HRSC, _code: int) -> int:
        """
        Запросить округляется ли числовая семантика в большую сторону
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код проверяемой семантики
        
        :returns: Если семантика числовая и округляется в большую сторону, возвращает ненулевое значение При ошибке возвращает 0
        :rtype: int
        """
        return mapGetRscSemanticRoundUpFlag_t (_hrsc, _code)

    mapSetRscSemanticRoundUpFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscSemanticRoundUpFlag', maptype.HRSC, ctypes.c_long, ctypes.c_int)
    def mapSetRscSemanticRoundUpFlag(_hrsc: maptype.HRSC, _code: int, _flag: int) -> int:
        """
        Установить признак семантики - числовая семантика округляется в большую сторону
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики (должна быть числовой)
        
        :param _flag: признак округления значения в большую сторону (``0`` или не ``0``)
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapSetRscSemanticRoundUpFlag_t (_hrsc, _code, _flag)

    mapGetRscSemanticNotEditFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticNotEditFlag', maptype.HRSC, ctypes.c_long)
    def mapGetRscSemanticNotEditFlag(_hrsc: maptype.HRSC, _code: int) -> int:
        """
        Запросить флаг запрета редактирования семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :returns: Возвращает флаг запрета редактирования семантики (ноль или не ноль) При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSemanticNotEditFlag_t (_hrsc, _code)

    mapSetRscSemanticNotEditFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscSemanticNotEditFlag', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapSetRscSemanticNotEditFlag(_hrsc: maptype.HRSC, _code: int, _flag: int) -> int:
        """
        Установить флаг запрета редактирования семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _flag: флаг запрета редактирования семантики: ``1`` - установить запрет, ``0`` - снять
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscSemanticNotEditFlag_t (_hrsc, _code, _flag)

    mapGetRscSemantic3DListCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemantic3DListCount', maptype.HRSC, ctypes.c_long)
    def mapGetRscSemantic3DListCount(_hrsc: maptype.HRSC, _libcode: int) -> int:
        """
        Запросить количество семантик - списков 3D изображений  в данной библиотеке
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _libcode: код библиотеки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSemantic3DListCount_t (_hrsc, _libcode)

    mapGetRscSemantic3DList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemantic3DList', maptype.HRSC, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.c_long)
    def mapGetRscSemantic3DList(_hrsc: maptype.HRSC, _libcode: int, _code: ctypes.POINTER(ctypes.c_long), _countlimit: int) -> int:
        """
        Запросить список кодов семантик - списков 3D изображений в данной библиотеке
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _libcode: код библиотеки
        
        :param _code: адрес массива кодов семантик
        
        :param _countlimit: размер массива
        
        :returns: Возвращает число записанных кодов семантики При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSemantic3DList_t (_hrsc, _libcode, _code, _countlimit)

    mapGetSemanticUniqueValueFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSemanticUniqueValueFlag', maptype.HRSC, ctypes.c_long)
    def mapGetSemanticUniqueValueFlag(_hrsc: maptype.HRSC, _code: int) -> int:
        """
        Запросить флаг уникальности значения семантики в листе карты
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSemanticUniqueValueFlag_t (_hrsc, _code)

    mapSetSemanticUniqueValueFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSemanticUniqueValueFlag', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapSetSemanticUniqueValueFlag(_hrsc: maptype.HRSC, _code: int, _flag: int) -> int:
        """
        Установить флаг уникальности значения семантики в листе карты
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _flag: флаг уникальности значения семантики (ноль или не ноль)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetSemanticUniqueValueFlag_t (_hrsc, _code, _flag)

    mapGetSemanticRepeatValueFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSemanticRepeatValueFlag', maptype.HRSC, ctypes.c_long)
    def mapGetSemanticRepeatValueFlag(_hrsc: maptype.HRSC, _code: int) -> int:
        """
        Запросить флаг повторяемости значения семантики у объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSemanticRepeatValueFlag_t (_hrsc, _code)

    mapSetSemanticRepeatValueFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSemanticRepeatValueFlag', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapSetSemanticRepeatValueFlag(_hrsc: maptype.HRSC, _code: int, _flag: int) -> int:
        """
        Установить флаг повторяемости значения семантики у объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _flag: флаг повторяемости значения семантики у объекта (ноль или не ноль)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetSemanticRepeatValueFlag_t (_hrsc, _code, _flag)

    mapGetSemanticRecodeFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSemanticRecodeFlag', maptype.HRSC, ctypes.c_long)
    def mapGetSemanticRecodeFlag(_hrsc: maptype.HRSC, _code: int) -> int:
        """
        Запросить флаг заполнения по другой семантике
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSemanticRecodeFlag_t (_hrsc, _code)

    mapSetSemanticRecodeFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSemanticRecodeFlag', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapSetSemanticRecodeFlag(_hrsc: maptype.HRSC, _code: int, _flag: int) -> int:
        """
        Установить флаг заполнения по другой семантике
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _flag: флаг заполнения по другой семантике (ноль или не ноль)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetSemanticRecodeFlag_t (_hrsc, _code, _flag)

    mapGetSemanticIndexFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSemanticIndexFlag', maptype.HRSC, ctypes.c_long)
    def mapGetSemanticIndexFlag(_hrsc: maptype.HRSC, _code: int) -> int:
        """
        Запросить флаг индексируемой семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSemanticIndexFlag_t (_hrsc, _code)

    mapSetSemanticIndexFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSemanticIndexFlag', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapSetSemanticIndexFlag(_hrsc: maptype.HRSC, _code: int, _flag: int) -> int:
        """
        Установить флаг индексируемой семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _flag: флаг индексируемой семантики (ноль или не ноль)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetSemanticIndexFlag_t (_hrsc, _code, _flag)

    mapGetRscSemanticUnitUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticUnitUn', maptype.HRSC, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetRscSemanticUnitUn(_hrsc: maptype.HRSC, _code: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить название единиц измерения семантики по коду в кодировке UTF-16
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _name: адрес строки для размещения результата
        
        :param _size: максимальный размер выходной строки в байтах (может быть до ``2048`` байт)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSemanticUnitUn_t (_hrsc, _code, _name.buffer(), _size)

    mapSetRscSemanticUnitUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscSemanticUnitUn', maptype.HRSC, ctypes.c_long, maptype.PWCHAR)
    def mapSetRscSemanticUnitUn(_hrsc: maptype.HRSC, _code: int, _name: mapsyst.WTEXT) -> int:
        """
        Установить название единиц измерения семантики по коду в кодировке UTF-16
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _name: адрес строки с новым названием
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscSemanticUnitUn_t (_hrsc, _code, _name.buffer())

    mapDeleteRscSemanticUnitUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRscSemanticUnitUn', maptype.HRSC, ctypes.c_long)
    def mapDeleteRscSemanticUnitUn(_hrsc: maptype.HRSC, _code: int) -> int:
        """
        Удалить название единиц измерения семантики по коду в кодировке UTF-16
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteRscSemanticUnitUn_t (_hrsc, _code)

    mapAppendRscDef_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendRscDef', maptype.HRSC, ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    def mapAppendRscDef(_hrsc: maptype.HRSC, _code: int, _semcode: int, _objmin: float, _objdef: float, _objmax: float) -> int:
        """
        Добавить умолчания для семантики для объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код объекта или ``0`` (для общих умолчаний семантики)
        
        :param _semcode: код семантики
        
        :param _objmin: умолчание на объект или общее на семантику
        
        :param _objdef: умолчание на объект или общее на семантику
        
        :param _objmax: умолчание на объект или общее на семантику
        
        :returns: Возвращает код семантики При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendRscDef_t (_hrsc, _code, _semcode, _objmin, _objdef, _objmax)

    mapUpdateRscDef_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateRscDef', maptype.HRSC, ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    def mapUpdateRscDef(_hrsc: maptype.HRSC, _code: int, _semcode: int, _objmin: float, _objdef: float, _objmax: float) -> int:
        """
        Заменить умолчания для семантики для объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код объекта или ``0`` (для общих умолчаний семантики)
        
        :param _semcode: код семантики
        
        :param _objmin: умолчание на объект или общее на семантику
        
        :param _objdef: умолчание на объект или общее на семантику
        
        :param _objmax: умолчание на объект или общее на семантику
        
        :returns: Возвращает код семантики При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdateRscDef_t (_hrsc, _code, _semcode, _objmin, _objdef, _objmax)

    mapDeleteRscDef_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRscDef', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapDeleteRscDef(_hrsc: maptype.HRSC, _code: int, _semcode: int) -> int:
        """
        Удалить умолчания для семантики для объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код объекта или ``0`` (для общих умолчаний семантики)
        
        :param _semcode: код семантики
        
        :returns: Возвращает код семантики При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteRscDef_t (_hrsc, _code, _semcode)

    mapGetRscSemanticHint_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapGetRscSemanticHint', maptype.HRSC, ctypes.c_long)
    def mapGetRscSemanticHint(_hrsc: maptype.HRSC, _code: int) -> ctypes.POINTER(maptype.WCHAR):
        """
        Запросить комментарий к семантике по коду
        
        :param _hrsc: идентификатор классификатора карты semcode - код семантики
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapGetRscSemanticHint_t (_hrsc, _code)

    mapAppendRscSemanticHint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendRscSemanticHint', maptype.HRSC, ctypes.c_long, maptype.PWCHAR)
    def mapAppendRscSemanticHint(_hrsc: maptype.HRSC, _semcode: int, _text: mapsyst.WTEXT) -> int:
        """
        Добавить запись в таблицу описания семантик
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _semcode: код семантики
        
        :param _text: многострочное описание порядка заполнения и назначения семантики
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendRscSemanticHint_t (_hrsc, _semcode, _text.buffer())

    mapDeleteRscSemanticHint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRscSemanticHint', maptype.HRSC, ctypes.c_long)
    def mapDeleteRscSemanticHint(_hrsc: maptype.HRSC, _semcode: int) -> int:
        """
        Удалить запись в таблице описания семантик
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _semcode: код семантики
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteRscSemanticHint_t (_hrsc, _semcode)

    mapUpdateRscSemanticHint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateRscSemanticHint', maptype.HRSC, ctypes.c_long, maptype.PWCHAR)
    def mapUpdateRscSemanticHint(_hrsc: maptype.HRSC, _semcode: int, _text: mapsyst.WTEXT) -> int:
        """
        Обновить запись в таблице описания семантик
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _semcode: код семантики
        
        :param _text: многострочное описание порядка заполнения и назначения семантики
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdateRscSemanticHint_t (_hrsc, _semcode, _text.buffer())

    mapGetRscSemanticObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticObjectCount', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapGetRscSemanticObjectCount(_hrsc: maptype.HRSC, _incode: int, _importance: int) -> int:
        """
        Запросить количество семантик для данного объекта по значимости семантики и внутреннему коду
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код (порядковый номер) объекта c ``1``
        
        :param _importance: значимость семантики - в maptype.h ``SEMANTIC_FOR_OBJECT``
        
        :returns: Возвращает количество семантик требуемой значимости При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSemanticObjectCount_t (_hrsc, _incode, _importance)

    mapGetRscSemanticObjectUsed_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticObjectUsed', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapGetRscSemanticObjectUsed(_hrsc: maptype.HRSC, _incode: int, _semanticcode: int) -> int:
        """
        Запросить использование семантики для данного объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код (порядковый номер)объекта
        
        :param _semanticcode: код семантики
        
        :returns: Возвращает значимость семантики (в maptype.h SEMANTIC_FOR_OBJECT)
        :rtype: int
        """
        return mapGetRscSemanticObjectUsed_t (_hrsc, _incode, _semanticcode)

    mapGetRscSemanticOnlyObjectUsed_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticOnlyObjectUsed', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapGetRscSemanticOnlyObjectUsed(_hrsc: maptype.HRSC, _incode: int, _semanticcode: int) -> int:
        """
        Запросить использование семантики для данного объекта - без учета общих семантик и семантик слоя
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код(индекс)объекта
        
        :param _semanticcode: код семантики
        
        :returns: Возвращает значимость семантики (в maptype.h SEMANTIC_FOR_OBJECT)
        :rtype: int
        """
        return mapGetRscSemanticOnlyObjectUsed_t (_hrsc, _incode, _semanticcode)

    mapGetRscSemanticObjectCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticObjectCode', maptype.HRSC, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapGetRscSemanticObjectCode(_hrsc: maptype.HRSC, _incode: int, _number: int, _importance: int) -> int:
        """
        Запросить код семантики для данного объекта по порядковому номеру семантики и значимости семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код (порядковый номер) объекта с ``1``
        
        :param _number: порядковый номер семантики
        
        :param _importance: значимость семантики (в maptype.h ``SEMANTIC_FOR_OBJECT``)
        
        :returns: При значимости семантики ``ALL_SEMANTIC`` - возвращает семантику в порядке сортировки Возвращает код семантики При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSemanticObjectCode_t (_hrsc, _incode, _number, _importance)

    mapGetRscSemanticObjectCodeList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemanticObjectCodeList', maptype.HRSC, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.c_long)
    def mapGetRscSemanticObjectCodeList(_hrsc: maptype.HRSC, _incode: int, _code: ctypes.POINTER(ctypes.c_long), _countlimit: int) -> int:
        """
        Запросить список всех кодов семантики для данного объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код (порядковый номер) объекта с ``1``
        
        :param _code: адрес массива семантик
        
        :param _countlimit: размер массива
        
        :returns: Возвращает число считанных кодов семантики При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSemanticObjectCodeList_t (_hrsc, _incode, _code, _countlimit)

    mapAppendRscSemanticObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendRscSemanticObject', maptype.HRSC, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapAppendRscSemanticObject(_hrsc: maptype.HRSC, _incode: int, _semanticcode: int, _importance: int) -> int:
        """
        Добавить код семантики для данного объекта по значимости семантики (POSSIBLE_SEMANTIC или MUST_SEMANTIC)
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код (порядковый номер) объекта
        
        :param _semanticcode: код семантики
        
        :param _importance: значимость семантики (``POSSIBLE_SEMANTIC`` или ``MUST_SEMANTIC``)
        
        :returns: Возвращает номер добавленной семантики в семантиках данного типа При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendRscSemanticObject_t (_hrsc, _incode, _semanticcode, _importance)

    mapUpdateRscSemanticObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateRscSemanticObject', maptype.HRSC, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapUpdateRscSemanticObject(_hrsc: maptype.HRSC, _incode: int, _semanticcode: int, _importance: int) -> int:
        """
        Изменить значимость семантики для данного объекта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код (порядковый номер) объекта
        
        :param _semanticcode: код семантики
        
        :param _importance: значимость семантики (``POSSIBLE_SEMANTIC`` или ``MUST_SEMANTIC``)
        
        :returns: Возвращает число семантик требуемой значимости При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdateRscSemanticObject_t (_hrsc, _incode, _semanticcode, _importance)

    mapDeleteRscSemanticObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRscSemanticObject', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapDeleteRscSemanticObject(_hrsc: maptype.HRSC, _incode: int, _semanticcode: int) -> int:
        """
        Удалить семантику для данного объекта - POSSIBLE_SEMANTIC или MUST_SEMANTIC
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код (порядковый номер) объекта
        
        :param _semanticcode: код семантики
        
        :returns: Возвращает общее число семантик объекта При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteRscSemanticObject_t (_hrsc, _incode, _semanticcode)

    mapSetRscObjSemanticOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscObjSemanticOrder', maptype.HRSC, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_int))
    def mapSetRscObjSemanticOrder(_hrsc: maptype.HRSC, _incode: int, _count: int, _semantics: ctypes.POINTER(ctypes.c_int)) -> int:
        """
        Записать порядок семантик для объекта в соответствии с входным списком
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код (порядковый номер) объекта
        
        :param _count: размер массива семантик объекта
        
        :param _semantics: указатель на сортированный список семантик объекта Семантики которые не назначены объекту - пишутся в конец списка
        
        :returns: Возвращает количество семантик объекта При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscObjSemanticOrder_t (_hrsc, _incode, _count, _semantics)

    mapGetRscAll3DSemObjects_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscAll3DSemObjects', maptype.HRSC, ctypes.c_char_p, ctypes.c_long)
    def mapGetRscAll3DSemObjects(_hrsc: maptype.HRSC, _buffer: ctypes.c_char_p, _count: int) -> int:
        """
        Составить список всех объектов классификатора, использующих семантики с признаком - список 3D вида
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _buffer: указатель на массив байтов
        
        :param _count: размер буфера в байтах (не менее количества объектов классификатора)
        
        :returns: Возвращает количество объектов, для которых могут использоваться семантики - списки 3D видов
        :rtype: int
        
        .. note::

           Если для объекта разрешена семантика - список 3D видов, в буфер
           на место, определяемое внутренним кодом объекта заносится 1, иначе 0
        """
        return mapGetRscAll3DSemObjects_t (_hrsc, _buffer, _count)

    mapGetRscColor_t = mapsyst.GetProcAddress(acceslib,maptype.COLORREF,'mapGetRscColor', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapGetRscColor(_hrsc: maptype.HRSC, _index: int, _number: int) -> maptype.COLORREF:
        """
        Запросить цвет из палитры
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _index: порядковый номер цвета в палитре с ``1``
        
        :param _number: порядковый номер палитры с ``1``
        
        :returns: Возвращает цвет в COLORREF При ошибке возвращает ноль
        :rtype: maptype.COLORREF
        """
        return mapGetRscColor_t (_hrsc, _index, _number)

    mapSetRscColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscColor', maptype.HRSC, maptype.COLORREF, ctypes.c_long, ctypes.c_long)
    def mapSetRscColor(_hrsc: maptype.HRSC, _color: maptype.COLORREF, _index: int, _number: int) -> int:
        """
        Установить цвет в данную палитру
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _color: цвет в ``COLORREF``
        
        :param _index: порядковый номер цвета в палитре с ``1``
        
        :param _number: порядковый номер палитры с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscColor_t (_hrsc, _color, _index, _number)

    mapGetRscColorCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscColorCount', maptype.HRSC)
    def mapGetRscColorCount(_hrsc: maptype.HRSC) -> int:
        """
        Запросить количество цветов в палитре классификатора
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscColorCount_t (_hrsc)

    mapGetRscPaletteCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscPaletteCount', maptype.HRSC)
    def mapGetRscPaletteCount(_hrsc: maptype.HRSC) -> int:
        """
        Запросить количество палитр классификатора
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscPaletteCount_t (_hrsc)

    mapGetRscPaletteNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscPaletteNameUn', maptype.HRSC, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetRscPaletteNameUn(_hrsc: maptype.HRSC, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запрос имени палитры по ее номеру
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: порядковый номер палитры с ``1``
        
        :param _name: строка для размещения имени палитры
        
        :param _size: размер строки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscPaletteNameUn_t (_hrsc, _number, _name.buffer(), _size)

    mapGetRscCMYKColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_uint,'mapGetRscCMYKColor', maptype.HRSC, ctypes.c_long)
    def mapGetRscCMYKColor(_hrsc: maptype.HRSC, _index: int) -> int:
        """
        Запросить цвет из CMYK - палитры
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _index: порядковый номер цвета в палитре с ``1``
        
        :returns: Возвращает цвет из 4 составляющих (С,M,Y,K), каждая в интервале от 0 до 255 При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscCMYKColor_t (_hrsc, _index)

    mapSetRscCMYKColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscCMYKColor', maptype.HRSC, ctypes.c_uint, ctypes.c_long)
    def mapSetRscCMYKColor(_hrsc: maptype.HRSC, _color: int, _index: int) -> int:
        """
        Установить цвет в CMYK - палитру
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _color: ``4`` составляющих (С,M,Y,K), каждая в интервале от ``0`` до ``255``
        
        :param _index: порядковый номер цвета в палитре с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscCMYKColor_t (_hrsc, _color, _index)

    mapDeleteRscPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRscPalette', maptype.HRSC, ctypes.c_long)
    def mapDeleteRscPalette(_hrsc: maptype.HRSC, _number: int) -> int:
        """
        Удалить палитру по порядковому номеру
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: порядковый номер палитры с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если палитра одна, она не удаляется
        """
        return mapDeleteRscPalette_t (_hrsc, _number)

    mapGetRGBColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRGBColor', maptype.HRSC, maptype.COLORREF, ctypes.c_long, ctypes.POINTER(maptype.COLORREF))
    def mapGetRGBColor(_hrsc: maptype.HRSC, _parmcolor: maptype.COLORREF, _palettenumber: int, _palettecolor: ctypes.POINTER(maptype.COLORREF)) -> int:
        """
        Преобразовать цвет из палитры классификатора или именованный в формат RGB
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _parmcolor: цвет из палитры, именованный, ``RGB`` или ``IMGC_TRANSPARENT``
        
        :param _palettenumber: порядковый номер палитры с ``1``, если цвет из палитры
        
        :param _palettecolor: адрес переменной для возврата цвета в формате ``COLORREF``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRGBColor_t (_hrsc, _parmcolor, _palettenumber, _palettecolor)

    mapGetFontCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetFontCount', maptype.HRSC)
    def mapGetFontCount(_hrsc: maptype.HRSC) -> int:
        """
        Запрос количества шрифтов
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetFontCount_t (_hrsc)

    mapAppendFont_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendFont', maptype.HRSC, ctypes.POINTER(maptype.RSCFONT))
    def mapAppendFont(_hrsc: maptype.HRSC, _font: ctypes.POINTER(maptype.RSCFONT)) -> int:
        """
        Добавить шрифт
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _font: описание шрифта, структура ``RSCFONT`` описана maptype.h
        
        :returns: Возвращает код шрифта При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendFont_t (_hrsc, _font)

    mapReplaceFont_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapReplaceFont', maptype.HRSC, ctypes.c_long, ctypes.POINTER(maptype.RSCFONT))
    def mapReplaceFont(_hrsc: maptype.HRSC, _index: int, _font: ctypes.POINTER(maptype.RSCFONT)) -> int:
        """
        Заменить шрифт
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _index: порядковый номер шрифта с ``1``
        
        :param _font: описание шрифта, структура ``RSCFONT`` описана maptype.h
        
        :returns: Возвращает код шрифта При ошибке возвращает ноль
        :rtype: int
        """
        return mapReplaceFont_t (_hrsc, _index, _font)

    mapGetFontCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetFontCode', maptype.HRSC, ctypes.c_long)
    def mapGetFontCode(_hrsc: maptype.HRSC, _number: int) -> int:
        """
        Запросить код шрифта по порядковому номеру
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер шрифта c ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetFontCode_t (_hrsc, _number)

    mapGetFontNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetFontNumber', maptype.HRSC, ctypes.POINTER(mapgdi.IMGTEXT))
    def mapGetFontNumber(_hrsc: maptype.HRSC, _parm: ctypes.POINTER(mapgdi.IMGTEXT)) -> int:
        """
        Запросить порядковый номер шрифта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _parm: параметры функции отображения текста
        
        :returns: Возвращает порядковый номер шрифта c 1 При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetFontNumber_t (_hrsc, _parm)

    mapGetFontName_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetFontName', maptype.HRSC, ctypes.c_long)
    def mapGetFontName(_hrsc: maptype.HRSC, _number: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить условное имя шрифта по порядковому номеру
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер шрифта c ``1``
        
        :returns: При ошибке возвращает указатель на пустую строку
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetFontName_t (_hrsc, _number)

    mapGetFont_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetFont', maptype.HRSC, ctypes.c_long, ctypes.POINTER(maptype.RSCFONT))
    def mapGetFont(_hrsc: maptype.HRSC, _number: int, _font: ctypes.POINTER(maptype.RSCFONT)) -> int:
        """
        Запросить шрифт по порядковому номеру c 1
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер шрифта
        
        :param _font: описание шрифта, структура ``RSCFONT`` описана maptype.h
        
        :returns: Возвращает код шрифта При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetFont_t (_hrsc, _number, _font)

    mapGetFontByCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetFontByCode', maptype.HRSC, ctypes.c_long, ctypes.POINTER(maptype.RSCFONT))
    def mapGetFontByCode(_hrsc: maptype.HRSC, _code: int, _font: ctypes.POINTER(maptype.RSCFONT)) -> int:
        """
        Запросить шрифт по коду
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код шрифта
        
        :param _font: описание шрифта, структура ``RSCFONT`` описана maptype.h
        
        :returns: Возвращает порядковый номер шрифта (с 1) При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetFontByCode_t (_hrsc, _code, _font)

    mapSetFontByCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetFontByCode', maptype.HRSC, ctypes.c_long)
    def mapSetFontByCode(_hrsc: maptype.HRSC, _code: int) -> int:
        """
        Дополнить параметры шрифта
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код шрифта
        
        :returns: Возвращает порядковый номер шрифта в таблице шрифтов При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetFontByCode_t (_hrsc, _code)

    mapDeleteFontByKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteFontByKey', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapDeleteFontByKey(_hrsc: maptype.HRSC, _key: int, _newkey: int) -> int:
        """
        Удалить шрифт по ключу, если нужно переназначить шрифт во внешнем виде объектов
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _key: ключ шрифта
        
        :param _newkey: ключ другого шрифта или ``0``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если newkey ``= 0``, будет назначен шрифт по умолчанию
        """
        return mapDeleteFontByKey_t (_hrsc, _key, _newkey)

    mapOpenFormula_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapOpenFormula', ctypes.c_char_p, ctypes.POINTER(ctypes.c_long))
    def mapOpenFormula(_formula: ctypes.c_char_p, _errorcode: ctypes.POINTER(ctypes.c_long)) -> ctypes.c_void_p:
        """
        Открыть формулу для выполнения множества вычислений по объектам
        
        hrsc      - идентификатор цифрового классификатора карты (RSC)
        
        :param _formula: строка, содержащая формулу
        
        :param _errorcode: код ошибки
        
        :returns: При ошибке возвращает ноль
        
        .. note::

           После завершения вычислений необходимо закрыть формулу функцией mapCloseFormula
        """
        return mapOpenFormula_t (_formula, _errorcode)

    mapCalculateFormula_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCalculateFormula', maptype.HOBJ, ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_long))
    def mapCalculateFormula(_hobj: maptype.HOBJ, _hformula: ctypes.c_void_p, _value: ctypes.POINTER(ctypes.c_double), _errorcode: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Вычислить значение открытой формулы для объекта
        
        :param _hobj: идентификатор объекта карты, для которого выполняется вычисление
        
        :param _hformula: идентификатор формулы, открытой в mapOpenFormula
        
        :param _value: поле для записи вычисленного значения
        
        :param _errorcode: поле для записи кода ошибки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCalculateFormula_t (_hobj, _hformula, _value, _errorcode)

    mapCloseFormula_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseFormula', ctypes.c_void_p)
    def mapCloseFormula(_hformula: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Закрыть формулу после выполнения вычислений
        
        :param _hformula: идентификкатор формулы, открытой в mapOpenFormula
        """
        return mapCloseFormula_t (_hformula)

    GetFormulaValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'GetFormulaValue', maptype.HOBJ, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_long))
    def GetFormulaValue(_hobj: maptype.HOBJ, _formula: ctypes.c_char_p, _value: ctypes.POINTER(ctypes.c_double), _errorcode: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Вычисление формулы
        
        :param _hobj: идентификатор объекта карты, для которого выполняется вычисление
        
        :param _formula: строка, содержащая формулу
        
        :param _value: поле для записи вычисленного значения
        
        :param _errorcode: поле для записи кода ошибки
        
        :returns: Возвращает 0 при ошибке, и в переменной errno - код ошибки
        :rtype: int
        """
        return GetFormulaValue_t (_hobj, _formula, _value, _errorcode)

    CheckFormula_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'CheckFormula', maptype.HRSC, ctypes.c_char_p, ctypes.POINTER(ctypes.c_long))
    def CheckFormula(_hrsc: maptype.HRSC, _formula: ctypes.c_char_p, _errorcode: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Проверить синтаксис формулы
        
        rsc       - идентификатор классификатора карты
        
        :param _formula: строка, содержащая формулу
        
        :param _errorcode: поле для записи кода ошибки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return CheckFormula_t (_hrsc, _formula, _errorcode)

    mapGetFormulaItemCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetFormulaItemCount')
    def mapGetFormulaItemCount() -> int:
        """
        Запросить число поддерживаемых элементов (операций) формулы ("ABS", "ARM", "COS", ... "()")
        """
        return mapGetFormulaItemCount_t ()

    mapGetFormulaItemName_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetFormulaItemName', ctypes.c_long)
    def mapGetFormulaItemName(_number: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить название элемента формулы по порядковому номеру с 1 ("ABS", "ARM", "COS", ... "()")
        
        :param _number: порядковый номер формулы
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetFormulaItemName_t (_number)

    mapGetFormulaItemComment_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapGetFormulaItemComment', ctypes.c_long)
    def mapGetFormulaItemComment(_number: int) -> ctypes.POINTER(maptype.WCHAR):
        """
        Запросить комментарий к элементу формулы по порядковому номеру с 1
        
        :param _number: порядковый номер формулы
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapGetFormulaItemComment_t (_number)

    AgregateStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'AgregateStringUn', maptype.HRSC, maptype.HOBJ, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def AgregateStringUn(_hrsc: maptype.HRSC, _hobj: maptype.HOBJ, _formula: mapsyst.WTEXT, _dest: mapsyst.WTEXT, _destlength: int, _errorcode: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Создать символьную строку со вставками по значениям семантики
        
        :param _formula: символьная строка любого содержания, в которой указаны места для вставки семантики
        
        :param _dest: указатель на буфер для размещения строки размер буфера - размер строки + ``256*`` количество вставок
        
        :param _destlength: размер строки
        
        :param _errorcode: поле для записи кода ошибки Вставка семантики: ``#`` - Указывает, что дальше идет ключевое слово или код семантики, в которой лежит значение любого типа, далее в () значение по умолчанию Пример: ``#9``(без названия) - взять значение семантики ``9``, при отсутствии вставить строчку ``"без названия"``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return AgregateStringUn_t (_hrsc, _hobj, _formula.buffer(), _dest.buffer(), _destlength, _errorcode)

    mapGetRscFormulaCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscFormulaCount', maptype.HRSC)
    def mapGetRscFormulaCount(_hrsc: maptype.HRSC) -> int:
        """
        Запросить количество формул в классификаторе
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscFormulaCount_t (_hrsc)

    mapGetRscFormulaCodeByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscFormulaCodeByNumber', maptype.HRSC, ctypes.c_long)
    def mapGetRscFormulaCodeByNumber(_hrsc: maptype.HRSC, _number: int) -> int:
        """
        Запросить код формулы в классификаторе по порядковому номеру с 1
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: порядковый номер формулы
        
        :returns: При ошибке и для удаленной формулы возвращает ноль
        :rtype: int
        """
        return mapGetRscFormulaCodeByNumber_t (_hrsc, _number)

    mapGetRscDescribeFormulaByCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscDescribeFormulaByCode', maptype.HRSC, ctypes.POINTER(maptype.RSCFORMULA), ctypes.c_long)
    def mapGetRscDescribeFormulaByCode(_hrsc: maptype.HRSC, _form: ctypes.POINTER(maptype.RSCFORMULA), _formulacode: int) -> int:
        """
        Заполнить структуру описания формулы по коду формулы
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _form: описание формулы, структура ``RSCFORMULA`` описана в maptype.h
        
        :param _formulacode: код формулы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscDescribeFormulaByCode_t (_hrsc, _form, _formulacode)

    mapReplaceRscFormulaText_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapReplaceRscFormulaText', maptype.HRSC, ctypes.c_long, ctypes.c_long, maptype.PWCHAR)
    def mapReplaceRscFormulaText(_hrsc: maptype.HRSC, _formulacode: int, _textlength: int, _text: mapsyst.WTEXT) -> int:
        """
        Заменить текст формулы по коду формулы
        
        :param _hrsc: идентификатор классификатора карты fcode       - код формулы
        
        :param _formulacode: код формулы
        
        :param _textlength: длина формулы в байтах
        
        :param _text: текст формулы Проверка на синтактическую правильность не делается
        
        :returns: При ошибке возвращает ноль, иначе - код формулы
        :rtype: int
        """
        return mapReplaceRscFormulaText_t (_hrsc, _formulacode, _textlength, _text.buffer())

    mapSetRscFormulaToSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscFormulaToSemantic', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapSetRscFormulaToSemantic(_hrsc: maptype.HRSC, _formulacode: int, _semanticcode: int) -> int:
        """
        Назначить семантике формулу для расчетов
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _formulacode: код формулы
        
        :param _semanticcode: код семантики
        
        :returns: Возвращает код формулы или ноль
        :rtype: int
        """
        return mapSetRscFormulaToSemantic_t (_hrsc, _formulacode, _semanticcode)

    mapDeleteRscFormula_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRscFormula', maptype.HRSC, ctypes.c_long)
    def mapDeleteRscFormula(_hrsc: maptype.HRSC, _formulacode: int) -> int:
        """
        Удалить формулу для расчетов по коду формулы
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _formulacode: код формулы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteRscFormula_t (_hrsc, _formulacode)

    mapGetRscTextFormulaByCode_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapGetRscTextFormulaByCode', maptype.HRSC, ctypes.c_long)
    def mapGetRscTextFormulaByCode(_hrsc: maptype.HRSC, _formulacode: int) -> ctypes.POINTER(maptype.WCHAR):
        """
        Запросить текст формулы по коду формулы
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _formulacode: код формулы
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapGetRscTextFormulaByCode_t (_hrsc, _formulacode)

    mapGetRscTextFormulaBySemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapGetRscTextFormulaBySemantic', maptype.HRSC, ctypes.c_long)
    def mapGetRscTextFormulaBySemantic(_hrsc: maptype.HRSC, _semanticcode: int) -> ctypes.POINTER(maptype.WCHAR):
        """
        Запросить текст формулы по коду семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _semanticcode: код семантики
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapGetRscTextFormulaBySemantic_t (_hrsc, _semanticcode)

    mapGetRscFormulaSemanticArray_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscFormulaSemanticArray', maptype.HRSC, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.c_int)
    def mapGetRscFormulaSemanticArray(_hrsc: maptype.HRSC, _semanticcode: int, _codearray: ctypes.POINTER(ctypes.c_long), _arraycount: int) -> int:
        """
        Запросить список кодов семантик в тексте формулы по коду семантики - формулы
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _semanticcode: код семантики - формулы
        
        :param _codearray: указатель на заполняемый массив кодов семантик
        
        :param _arraycount: число зарезервированных элементов массива для заполнения
        
        :returns: Возвращает число заполненных элементов При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscFormulaSemanticArray_t (_hrsc, _semanticcode, _codearray, _arraycount)

    mapAppendRscFormula_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendRscFormula', maptype.HRSC, ctypes.POINTER(maptype.RSCFORMULA), maptype.PWCHAR, ctypes.POINTER(ctypes.c_long))
    def mapAppendRscFormula(_hrsc: maptype.HRSC, _form: ctypes.POINTER(maptype.RSCFORMULA), _text: mapsyst.WTEXT, _errcode: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Записать новую формулу
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _form: описание формулы
        
        :param _text: текст формулы
        
        :param _errcode: код ошибки при проверке формулы (maperr.rh)
        
        :returns: Возвращает код формулы (можно назначить семантике в mapSetRscFormulaToSemantic) При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendRscFormula_t (_hrsc, _form, _text.buffer(), _errcode)

    mapCountRscFormulaLibraries_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCountRscFormulaLibraries', maptype.HRSC)
    def mapCountRscFormulaLibraries(_hrsc: maptype.HRSC) -> int:
        """
        Запросить количество библиотек формул для семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCountRscFormulaLibraries_t (_hrsc)

    mapOpenRscFormulaLibrary_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapOpenRscFormulaLibrary', maptype.HRSC, maptype.PWCHAR, ctypes.c_long)
    def mapOpenRscFormulaLibrary(_hrsc: maptype.HRSC, _name: mapsyst.WTEXT, _message: int) -> int:
        """
        Добавить библиотеку в список для вычисления значений семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _name: имя библиотеки
        
        :param _message: ``0`` - не выдавать сообщений
        
        :returns: Возвращает номер библиотеки в списке (1,...) При ошибке возвращает ноль
        :rtype: int
        """
        return mapOpenRscFormulaLibrary_t (_hrsc, _name.buffer(), _message)

    mapGetRscFormulaLibraryFunction_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.SEMLIBLIST),'mapGetRscFormulaLibraryFunction', maptype.HRSC, ctypes.c_long)
    def mapGetRscFormulaLibraryFunction(_hrsc: maptype.HRSC, _number: int) -> ctypes.POINTER(maptype.SEMLIBLIST):
        """
        Запросить описание формул для семантики по номеру библиотеки в списке
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер библиотеки в списке  (``1``,...)
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(maptype.SEMLIBLIST)
        """
        return mapGetRscFormulaLibraryFunction_t (_hrsc, _number)

    mapGetRscFormulaLibraryName_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapGetRscFormulaLibraryName', maptype.HRSC, ctypes.c_long)
    def mapGetRscFormulaLibraryName(_hrsc: maptype.HRSC, _number: int) -> ctypes.POINTER(maptype.WCHAR):
        """
        Запросить по номеру библиотеки в списке имя библиотеки
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер библиотеки в списке с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapGetRscFormulaLibraryName_t (_hrsc, _number)

    mapGetRscTabCtrCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscTabCtrCount', maptype.HRSC)
    def mapGetRscTabCtrCount(_hrsc: maptype.HRSC) -> int:
        """
        Запросить число записей в таблице кластеров
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscTabCtrCount_t (_hrsc)

    mapGetRscTabCtrLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscTabCtrLength', maptype.HRSC)
    def mapGetRscTabCtrLength(_hrsc: maptype.HRSC) -> int:
        """
        Запросить размер всех записей в таблице кластеров
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscTabCtrLength_t (_hrsc)

    mapGetRscTabCtr_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(mapgdi.TABCTR),'mapGetRscTabCtr', maptype.HRSC, ctypes.c_long)
    def mapGetRscTabCtr(_hrsc: maptype.HRSC, _number: int) -> ctypes.POINTER(mapgdi.TABCTR):
        """
        Запросить запись в таблице кластеров по порядковому номеру
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: порядковый номер записи в таблице кластеров
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(mapgdi.TABCTR)
        """
        return mapGetRscTabCtr_t (_hrsc, _number)

    mapAppendRscTabCtr_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendRscTabCtr', maptype.HRSC, ctypes.POINTER(mapgdi.TABCTR))
    def mapAppendRscTabCtr(_hrsc: maptype.HRSC, _tabctr: ctypes.POINTER(mapgdi.TABCTR)) -> int:
        """
        Добавить запись в таблицу кластеров
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _tabctr: описание записи таблицы кластеров
        
        :returns: При ошибке возвращает ноль, иначе количество кластеров
        :rtype: int
        """
        return mapAppendRscTabCtr_t (_hrsc, _tabctr)

    mapDeleteRscTabCtr_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRscTabCtr', maptype.HRSC, ctypes.c_long)
    def mapDeleteRscTabCtr(_hrsc: maptype.HRSC, _number: int) -> int:
        """
        Удалить запись в таблице кластеров
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: порядковый номер записи в таблице кластеров
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteRscTabCtr_t (_hrsc, _number)

    mapUpdateRscTabCtr_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateRscTabCtr', maptype.HRSC, ctypes.c_long, ctypes.POINTER(mapgdi.TABCTR))
    def mapUpdateRscTabCtr(_hrsc: maptype.HRSC, _number: int, _tabctr: ctypes.POINTER(mapgdi.TABCTR)) -> int:
        """
        Обновить запись в таблице кластеров
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: порядковый номер записи в таблице кластеров
        
        :param _tabctr: описание записи таблицы кластеров
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdateRscTabCtr_t (_hrsc, _number, _tabctr)

    mapGetRscTabRecCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscTabRecCount', maptype.HRSC)
    def mapGetRscTabRecCount(_hrsc: maptype.HRSC) -> int:
        """
        Запросить число записей в таблице перекодировки семантик
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscTabRecCount_t (_hrsc)

    mapGetRscTabRecLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscTabRecLength', maptype.HRSC)
    def mapGetRscTabRecLength(_hrsc: maptype.HRSC) -> int:
        """
        Запросить размер всех записей в таблице перекодировки семантик
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscTabRecLength_t (_hrsc)

    mapGetRscRecCtr_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetRscRecCtr', maptype.HRSC, ctypes.c_long)
    def mapGetRscRecCtr(_hrsc: maptype.HRSC, _number: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить запись в таблице перекодировки семантик по порядковому номеру
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер записи с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetRscRecCtr_t (_hrsc, _number)

    mapAppendRscTabRec_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendRscTabRec', maptype.HRSC, ctypes.c_char_p, ctypes.c_long)
    def mapAppendRscTabRec(_hrsc: maptype.HRSC, _tabrec: ctypes.c_char_p, _length: int) -> int:
        """
        Добавить запись в таблицу перекодировки семантик
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _tabrec: добавляемая запись
        
        :param _length: длина записи
        
        :returns: При ошибке возвращает ноль, иначе количество записей
        :rtype: int
        """
        return mapAppendRscTabRec_t (_hrsc, _tabrec, _length)

    mapDeleteRscTabRec_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRscTabRec', maptype.HRSC, ctypes.c_long)
    def mapDeleteRscTabRec(_hrsc: maptype.HRSC, _number: int) -> int:
        """
        Удалить запись в таблице перекодировки семантик
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер удаляемой записи с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteRscTabRec_t (_hrsc, _number)

    mapUpdateRscTabRec_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateRscTabRec', maptype.HRSC, ctypes.c_long, ctypes.c_char_p, ctypes.c_long)
    def mapUpdateRscTabRec(_hrsc: maptype.HRSC, _number: int, _tabrec: ctypes.c_char_p, _length: int) -> int:
        """
        Обновить запись в таблице перекодировки семантик
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер записи с ``1``
        
        :param _tabrec: обновляемая запись
        
        :param _length: длина записи
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdateRscTabRec_t (_hrsc, _number, _tabrec, _length)

    mapGetRscTabSemDbCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscTabSemDbCount', maptype.HRSC)
    def mapGetRscTabSemDbCount(_hrsc: maptype.HRSC) -> int:
        """
        Запросить число записей в таблице семантик - ссылок на БД
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscTabSemDbCount_t (_hrsc)

    mapGetRscTabSemDbLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscTabSemDbLength', maptype.HRSC)
    def mapGetRscTabSemDbLength(_hrsc: maptype.HRSC) -> int:
        """
        Запросить размер всех записей в таблице семантик - ссылок на БД
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscTabSemDbLength_t (_hrsc)

    mapGetRscTabSemDb_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetRscTabSemDb', maptype.HRSC, ctypes.c_long)
    def mapGetRscTabSemDb(_hrsc: maptype.HRSC, _number: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить запись в таблице семантик - ссылок на БД по порядковому номеру
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер записи с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetRscTabSemDb_t (_hrsc, _number)

    mapGetRscTabSemDbByCode_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapGetRscTabSemDbByCode', maptype.HRSC, ctypes.c_long, ctypes.POINTER(ctypes.POINTER(maptype.WCHAR)), ctypes.POINTER(ctypes.POINTER(maptype.WCHAR)))
    def mapGetRscTabSemDbByCode(_hrsc: maptype.HRSC, _code: int, _dbname: ctypes.POINTER(ctypes.POINTER(maptype.WCHAR)), _table: ctypes.POINTER(ctypes.POINTER(maptype.WCHAR))) -> ctypes.POINTER(maptype.WCHAR):
        """
        Запросить описание семантики - ссылки на БД по коду
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _dbname: имя поля для записи указателя на имя базы данных
        
        :param _table: имя поля для записи указателя на имя таблицы
        
        :returns: Возвращает указатель на имя поля в таблице При ошибке возвращает ноль
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapGetRscTabSemDbByCode_t (_hrsc, _code, _dbname, _table)

    mapAppendRscTabSemDb_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendRscTabSemDb', maptype.HRSC, ctypes.c_char_p, ctypes.c_long)
    def mapAppendRscTabSemDb(_hrsc: maptype.HRSC, _tab: ctypes.c_char_p, _length: int) -> int:
        """
        Добавить запись в таблицу семантик - ссылок на БД
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _tab: адрес добавляемой записи ``TABSEMDB``
        
        :param _length: длина записи в байтах
        
        :returns: При ошибке возвращает ноль, иначе количество записей
        :rtype: int
        """
        return mapAppendRscTabSemDb_t (_hrsc, _tab, _length)

    mapDeleteRscTabSemDb_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRscTabSemDb', maptype.HRSC, ctypes.c_long)
    def mapDeleteRscTabSemDb(_hrsc: maptype.HRSC, _number: int) -> int:
        """
        Удалить запись в таблице семантик - ссылок на БД
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер удаляемой записи с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteRscTabSemDb_t (_hrsc, _number)

    mapUpdateRscTabSemDb_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateRscTabSemDb', maptype.HRSC, ctypes.c_long, ctypes.c_char_p, ctypes.c_long)
    def mapUpdateRscTabSemDb(_hrsc: maptype.HRSC, _number: int, _tab: ctypes.c_char_p, _length: int) -> int:
        """
        Обновить запись в таблице семантик - ссылок на БД
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер обновляемой записи с ``1``
        
        :param _tab: адрес обновляемой записи
        
        :param _length: длина записи
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdateRscTabSemDb_t (_hrsc, _number, _tab, _length)

    mapGetRscTabSemTmpCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscTabSemTmpCount', maptype.HRSC)
    def mapGetRscTabSemTmpCount(_hrsc: maptype.HRSC) -> int:
        """
        Запросить число записей в таблице семантик - шаблонов строк
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscTabSemTmpCount_t (_hrsc)

    mapGetRscTabSemTmpLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscTabSemTmpLength', maptype.HRSC)
    def mapGetRscTabSemTmpLength(_hrsc: maptype.HRSC) -> int:
        """
        Запросить размер всех записей в таблице семантик - шаблонов строк
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscTabSemTmpLength_t (_hrsc)

    mapGetRscTabSemTmp_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetRscTabSemTmp', maptype.HRSC, ctypes.c_long)
    def mapGetRscTabSemTmp(_hrsc: maptype.HRSC, _number: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить запись в таблице семантик - шаблонов строк по порядковому номеру
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер записи с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetRscTabSemTmp_t (_hrsc, _number)

    mapGetRscTabSemTmpNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscTabSemTmpNumber', maptype.HRSC, ctypes.c_long)
    def mapGetRscTabSemTmpNumber(_hrsc: maptype.HRSC, _code: int) -> int:
        """
        Запросить порядковый номер записи в таблице семантик - шаблонов строк по коду семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscTabSemTmpNumber_t (_hrsc, _code)

    mapGetRscTabSemTmpTextByCode_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapGetRscTabSemTmpTextByCode', maptype.HRSC, ctypes.c_long)
    def mapGetRscTabSemTmpTextByCode(_hrsc: maptype.HRSC, _code: int) -> ctypes.POINTER(maptype.WCHAR):
        """
        Запросить текст шаблона текстовой строки по коду семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapGetRscTabSemTmpTextByCode_t (_hrsc, _code)

    mapSetRscTabSemTmpTextByCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscTabSemTmpTextByCode', maptype.HRSC, ctypes.c_long, maptype.PWCHAR)
    def mapSetRscTabSemTmpTextByCode(_hrsc: maptype.HRSC, _code: int, _text: mapsyst.WTEXT) -> int:
        """
        Установить текст шаблона текстовой строки по коду семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _text: текст шаблона текстовой строки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если для кода не было шаблона, то он будет добавлен
        """
        return mapSetRscTabSemTmpTextByCode_t (_hrsc, _code, _text.buffer())

    mapDeleteRscTabSemTmp_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRscTabSemTmp', maptype.HRSC, ctypes.c_long)
    def mapDeleteRscTabSemTmp(_hrsc: maptype.HRSC, _number: int) -> int:
        """
        Удалить запись в таблице семантик - шаблонов строк
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер записи с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteRscTabSemTmp_t (_hrsc, _number)

    mapCheckSemanticTemplate_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckSemanticTemplate', maptype.HRSC, ctypes.c_long, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long))
    def mapCheckSemanticTemplate(_hrsc: maptype.HRSC, _code: int, _value: mapsyst.WTEXT, _position: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Проверить соответствие строки и шаблона строки
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _value: строка значения семантики для проверки
        
        :param _position: поле для записи номера символа c ``1``, не соответствующего шаблону
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCheckSemanticTemplate_t (_hrsc, _code, _value.buffer(), _position)

    mapTestSemanticTemplate_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapTestSemanticTemplate', maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long))
    def mapTestSemanticTemplate(_value: mapsyst.WTEXT, _test: mapsyst.WTEXT, _position: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Проверить соответствие строки и шаблона строки до записи шаблона строки
        
        :param _value: строка значения семантики для проверки
        
        :param _test: строка шаблона, может содержать несколько шаблонов, разделенных символом \\n
        
        :param _position: номер символа с ``1``, который не соответствует шаблону
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapTestSemanticTemplate_t (_value.buffer(), _test.buffer(), _position)

    mapGetRscSemFileFormatByCode_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapGetRscSemFileFormatByCode', maptype.HRSC, ctypes.c_long)
    def mapGetRscSemFileFormatByCode(_hrsc: maptype.HRSC, _code: int) -> ctypes.POINTER(maptype.WCHAR):
        """
        Запросить текст списка форматов для семантики - ссылки на файл по коду семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики Пример строки: ``"jpg,tiff,bmp,rsw"``
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapGetRscSemFileFormatByCode_t (_hrsc, _code)

    mapSetRscSemFileFormatByCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRscSemFileFormatByCode', maptype.HRSC, ctypes.c_long, maptype.PWCHAR)
    def mapSetRscSemFileFormatByCode(_hrsc: maptype.HRSC, _code: int, _text: mapsyst.WTEXT) -> int:
        """
        Установить текст списка форматов для семантики - ссылки на файл по коду семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _text: список форматов через запятую (``"jpg,tiff,bmp,rsw"``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRscSemFileFormatByCode_t (_hrsc, _code, _text.buffer())

    mapDeleteRscSemFileFormatByCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRscSemFileFormatByCode', maptype.HRSC, ctypes.c_long)
    def mapDeleteRscSemFileFormatByCode(_hrsc: maptype.HRSC, _code: int) -> int:
        """
        Удалить запись списка форматов по коду семантики - ссылки на файл
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteRscSemFileFormatByCode_t (_hrsc, _code)

    mapGetRscSemFileFormatForDialogByCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRscSemFileFormatForDialogByCode', maptype.HRSC, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetRscSemFileFormatForDialogByCode(_hrsc: maptype.HRSC, _code: int, _filter: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить строку с фильтром для диалога выбора файла с учетом OC
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _code: код семантики
        
        :param _filter: строка для размещения фильтра
        
        :param _size: размер строки Пример строки: ``"SXF SITX (*.sxf; *.sitx), *.sxf; *.sitx"`` или ``"SXF SITX (*.sxf *.sitx)"``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRscSemFileFormatForDialogByCode_t (_hrsc, _code, _filter.buffer(), _size)

    mapGetColorsGroupCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetColorsGroupCount', maptype.HRSC)
    def mapGetColorsGroupCount(_hrsc: maptype.HRSC) -> int:
        """
        Запросить число групп в таблице именованных цветов
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetColorsGroupCount_t (_hrsc)

    mapGetColorsGroupName_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapGetColorsGroupName', maptype.HRSC, ctypes.c_long)
    def mapGetColorsGroupName(_hrsc: maptype.HRSC, _number: int) -> ctypes.POINTER(maptype.WCHAR):
        """
        Запросить название группы по номеру группы
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер группы с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapGetColorsGroupName_t (_hrsc, _number)

    mapSetColorsGroupName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetColorsGroupName', maptype.HRSC, ctypes.c_long, maptype.PWCHAR)
    def mapSetColorsGroupName(_hrsc: maptype.HRSC, _number: int, _name: mapsyst.WTEXT) -> int:
        """
        Установить название группы по номеру группы
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер группы с ``1``
        
        :param _name: новое название группы цветов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetColorsGroupName_t (_hrsc, _number, _name.buffer())

    mapGetColorsGroupLevel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetColorsGroupLevel', maptype.HRSC, ctypes.c_long)
    def mapGetColorsGroupLevel(_hrsc: maptype.HRSC, _number: int) -> int:
        """
        Запросить уровень группы по номеру группы
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер группы с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetColorsGroupLevel_t (_hrsc, _number)

    mapSetColorsGroupLevel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetColorsGroupLevel', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapSetColorsGroupLevel(_hrsc: maptype.HRSC, _number: int, _level: int) -> int:
        """
        Изменить уровень группы по номеру группы
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер группы с ``1``
        
        :param _level: номер уровня вложенности группы от ``0`` до ``31``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetColorsGroupLevel_t (_hrsc, _number, _level)

    mapGetColorsGroupIdent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetColorsGroupIdent', maptype.HRSC, ctypes.c_long)
    def mapGetColorsGroupIdent(_hrsc: maptype.HRSC, _number: int) -> int:
        """
        Запросить идентификатор группы по номеру группы
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер группы с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetColorsGroupIdent_t (_hrsc, _number)

    mapAppendColorsGroup_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendColorsGroup', maptype.HRSC, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapAppendColorsGroup(_hrsc: maptype.HRSC, _name: mapsyst.WTEXT, _level: int, _number: int) -> int:
        """
        Добавить группу в таблицу цветов
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _name: название новой группы цветов
        
        :param _level: номер уровня вложенности группы от ``0`` до ``31``
        
        :param _number: порядковый номер в списке групп с ``1``, под которым будет создана группа (вставлена в список)
        
        :returns: Возвращает порядковый номер созданной группы с 1 При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если номер равен нулю, то группа создается в конце списка
        """
        return mapAppendColorsGroup_t (_hrsc, _name.buffer(), _level, _number)

    mapChangeColorsGroupOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapChangeColorsGroupOrder', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapChangeColorsGroupOrder(_hrsc: maptype.HRSC, _number: int, _newnumber: int) -> int:
        """
        Изменить расположение группы в списке групп
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: текущий порядковый номер перемещаемой группы в списке групп с ``1``
        
        :param _newnumber: новый порядковый номер элемента в текущем списке групп с ``1``, перед которым нужно вставить группу
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapChangeColorsGroupOrder_t (_hrsc, _number, _newnumber)

    mapDeleteColorsGroup_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteColorsGroup', maptype.HRSC, ctypes.c_long)
    def mapDeleteColorsGroup(_hrsc: maptype.HRSC, _number: int) -> int:
        """
        Удалить группу в таблице цветов
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер группы с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteColorsGroup_t (_hrsc, _number)

    mapGetColorsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetColorsCount', maptype.HRSC)
    def mapGetColorsCount(_hrsc: maptype.HRSC) -> int:
        """
        Запросить число цветов в таблице цветов
        
        :param _hrsc: идентификатор классификатора карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetColorsCount_t (_hrsc)

    mapGetColorsRecord_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.TABCOLORSITEM),'mapGetColorsRecord', maptype.HRSC, ctypes.c_long)
    def mapGetColorsRecord(_hrsc: maptype.HRSC, _number: int) -> ctypes.POINTER(maptype.TABCOLORSITEM):
        """
        Запросить описание цвета по номеру цвета
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер цвета с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(maptype.TABCOLORSITEM)
        """
        return mapGetColorsRecord_t (_hrsc, _number)

    mapSetColorsRecord_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetColorsRecord', maptype.HRSC, ctypes.c_long, ctypes.POINTER(maptype.TABCOLORSITEM))
    def mapSetColorsRecord(_hrsc: maptype.HRSC, _number: int, _item: ctypes.POINTER(maptype.TABCOLORSITEM)) -> int:
        """
        Установить описание цвета по номеру цвета
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер цвета с ``1``
        
        :param _item: запись описания именованного цвета (``TABCOLORSITEM`` описана в maptype.h)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetColorsRecord_t (_hrsc, _number, _item)

    mapAppendColors_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendColors', maptype.HRSC, ctypes.POINTER(maptype.TABCOLORSITEM))
    def mapAppendColors(_hrsc: maptype.HRSC, _item: ctypes.POINTER(maptype.TABCOLORSITEM)) -> int:
        """
        Добавить описание цвета в таблицу цветов
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _item: запись описания именованного цвета (``TABCOLORSITEM`` описана в maptype.h)
        
        :returns: Возвращает порядковый номер созданного цвета с 1 При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendColors_t (_hrsc, _item)

    mapDeleteColors_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteColors', maptype.HRSC, ctypes.c_long)
    def mapDeleteColors(_hrsc: maptype.HRSC, _number: int) -> int:
        """
        Удалить описание цвета в таблице цветов
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _number: номер цвета с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteColors_t (_hrsc, _number)

    mapGetObjectListForColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapGetObjectListForColor', maptype.HRSC, ctypes.c_long)
    def mapGetObjectListForColor(_hrsc: maptype.HRSC, _color: int) -> ctypes.c_void_p:
        """
        Запросить список внутренних кодов объектов, в которых используется заданный именованный цвет
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _color: проверяемый цвет вместе с маской (``IMGC_INDEX``, ``IMGC_COLORINDEX``, ...)
        
        :returns: Возвращает идентификатор списка объектов При отсутствии заданного цвета возвращает ноль
        """
        return mapGetObjectListForColor_t (_hrsc, _color)

    mapGetObjectListForColorPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_int),'mapGetObjectListForColorPoint', ctypes.c_void_p, ctypes.POINTER(ctypes.c_long))
    def mapGetObjectListForColorPoint(_list: ctypes.c_void_p, _count: ctypes.POINTER(ctypes.c_long)) -> ctypes.POINTER(ctypes.c_int):
        """
        Получить адрес списка кодов объектов, в которых используется заданный именованный цвет
        
        :param _list: идентификатор списка объектов, созданный функцией mapGetObjectListForColor
        
        :param _count: поле для записи числа объектов в списке
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_int)
        """
        return mapGetObjectListForColorPoint_t (_list, _count)

    mapFreeObjectListForColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeObjectListForColor', ctypes.c_void_p)
    def mapFreeObjectListForColor(_list: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Удалить список объектов из памяти
        
        :param _list: идентификатор списка объектов, созданный функцией mapGetObjectListForColor
        """
        return mapFreeObjectListForColor_t (_list)

    mapGetFirstAdjObjects_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_int),'mapGetFirstAdjObjects', maptype.HRSC, ctypes.c_long, ctypes.POINTER(ctypes.c_int))
    def mapGetFirstAdjObjects(_hrsc: maptype.HRSC, _incode: int, _count: ctypes.POINTER(ctypes.c_int)) -> ctypes.POINTER(ctypes.c_int):
        """
        Запросить список допустимых кодов объектов для первой точки контура
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта, для которого запрашивается список допустимых соседей
        
        :param _count: поле для записи числа кодов объектов в списке
        
        :returns: Возвращает указатель на первый внутренний код в списке кодов При ошибке или отсутствии списка крайних объектов возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_int)
        """
        return mapGetFirstAdjObjects_t (_hrsc, _incode, _count)

    mapGetLastAdjObjects_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_int),'mapGetLastAdjObjects', maptype.HRSC, ctypes.c_long, ctypes.POINTER(ctypes.c_int))
    def mapGetLastAdjObjects(_hrsc: maptype.HRSC, _incode: int, _count: ctypes.POINTER(ctypes.c_int)) -> ctypes.POINTER(ctypes.c_int):
        """
        Запросить список допустимых кодов объектов для последней точки контура
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта, для которого запрашивается список допустимых соседей
        
        :param _count: поле для записи числа кодов объектов в списке
        
        :returns: Возвращает указатель на первый внутренний код в списке кодов При ошибке или отсутствии списка крайних объектов возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_int)
        """
        return mapGetLastAdjObjects_t (_hrsc, _incode, _count)

    mapGetAdjObjectsSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_int),'mapGetAdjObjectsSemantic', maptype.HRSC, ctypes.c_long, ctypes.POINTER(ctypes.c_int))
    def mapGetAdjObjectsSemantic(_hrsc: maptype.HRSC, _incode: int, _count: ctypes.POINTER(ctypes.c_int)) -> ctypes.POINTER(ctypes.c_int):
        """
        Запросить список кодов семантик для проверки совпадения значений
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта, для которого запрашивается список семантик
        
        :param _count: поле для записи числа кодов семантик в списке
        
        :returns: Возвращает указатель на первый код семантики в списке кодов При ошибке или отсутствии списка кодов семантик возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_int)
        """
        return mapGetAdjObjectsSemantic_t (_hrsc, _incode, _count)

    mapGetAdjObjectsFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetAdjObjectsFlag', maptype.HRSC, ctypes.c_long)
    def mapGetAdjObjectsFlag(_hrsc: maptype.HRSC, _incode: int) -> int:
        """
        Запросить флаг видов контроля соседей в виде суммы значений
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта, для которого запрашивается флаг Сумма возвращаемых значений: ``1`` - Объекты начала и конца контура должны быть на одной карте с базовым объектом ``2`` - Объект может быть создан только после выбора начального и/или конечного объекта из списков ``4`` - Выбираемые объекты начала и конца должны иметь совпадающие значения заданных семантик
        
        :returns: При ошибке или отсутствии установленных значений возвращает ноль
        :rtype: int
        """
        return mapGetAdjObjectsFlag_t (_hrsc, _incode)

    mapUpdateAdjObjects_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateAdjObjects', maptype.HRSC, ctypes.c_long, ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def mapUpdateAdjObjects(_hrsc: maptype.HRSC, _incode: int, _firstlist: ctypes.POINTER(ctypes.c_int), _firstcount: int, _lastlist: ctypes.POINTER(ctypes.c_int), _lastcount: int) -> int:
        """
        Обновить или добавить коды объектов в записи таблицы соседей
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта, для которого устанавливается флаг
        
        :param _firstlist: указатель на массив кодов объектов, допустимых в первой точке объекта
        
        :param _firstcount: число кодов объектов в массиве для первой точки
        
        :param _lastlist: указатель на массив кодов объектов, допустимых в последней точке объекта
        
        :param _lastcount: число кодов объектов в массиве для последней точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если для incode не было записи в таблице соседей, то она будет создана
        """
        return mapUpdateAdjObjects_t (_hrsc, _incode, _firstlist, _firstcount, _lastlist, _lastcount)

    mapUpdateAdjObjectsSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateAdjObjectsSemantic', maptype.HRSC, ctypes.c_long, ctypes.POINTER(ctypes.c_int), ctypes.c_int)
    def mapUpdateAdjObjectsSemantic(_hrsc: maptype.HRSC, _incode: int, _semlist: ctypes.POINTER(ctypes.c_int), _semcount: int) -> int:
        """
        Обновить или добавить коды семантик в записи таблицы соседей
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта, для которого устанавливается флаг
        
        :param _semlist: указатель на массив кодов семантик, для которых будет выполнено сравнение значений объекта и его соседей
        
        :param _semcount: число кодов семантик в массиве
        
        :returns: При ошибке или отсутствии записи в таблице соседей возвращает ноль
        :rtype: int
        
        .. note::

           Если для incode не было записи в таблице соседей, то она не будет создана
        """
        return mapUpdateAdjObjectsSemantic_t (_hrsc, _incode, _semlist, _semcount)

    mapSetAdjObjectsFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetAdjObjectsFlag', maptype.HRSC, ctypes.c_long, ctypes.c_long)
    def mapSetAdjObjectsFlag(_hrsc: maptype.HRSC, _incode: int, _flag: int) -> int:
        """
        Установить флаг видов контроля соседей
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _incode: внутренний код объекта, для которого устанавливается флаг
        
        :param _flag: новое значение флага в виде суммы всех требуемых значений
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetAdjObjectsFlag_t (_hrsc, _incode, _flag)

    mapGetLinkObjects_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_uint),'mapGetLinkObjects', maptype.HRSC, ctypes.c_long, ctypes.POINTER(ctypes.c_int))
    def mapGetLinkObjects(_hrsc: maptype.HRSC, _semcode: int, _count: ctypes.POINTER(ctypes.c_int)) -> ctypes.POINTER(ctypes.c_uint):
        """
        Запросить список внешних кодов связанных объектов для заданного кода семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _semcode: код семантики, для которого запрашивается список допустимых связанных объектов
        
        :param _count: поле для записи числа кодов объектов в списке
        
        :returns: Возвращает указатель на первый внешний код в списке кодов
        :rtype: ctypes.POINTER(ctypes.c_uint)
        """
        return mapGetLinkObjects_t (_hrsc, _semcode, _count)

    mapGetLinkObjectsForObject_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_uint),'mapGetLinkObjectsForObject', maptype.HOBJ, ctypes.c_long, ctypes.POINTER(ctypes.c_int))
    def mapGetLinkObjectsForObject(_hobj: maptype.HOBJ, _semcode: int, _count: ctypes.POINTER(ctypes.c_int)) -> ctypes.POINTER(ctypes.c_uint):
        """
        Запросить список внешних кодов связанных объектов для семантики объекта
        
        :param _hobj: идентификатор объекта
        
        :param _semcode: код семантики объекта, для которого запрашивается список допустимых связанных объектов
        
        :param _count: поле для записи числа кодов объектов в списке
        
        :returns: Возвращает указатель на первый внешний код в списке кодов
        :rtype: ctypes.POINTER(ctypes.c_uint)
        """
        return mapGetLinkObjectsForObject_t (_hobj, _semcode, _count)

    mapUpdateLinkObjects_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateLinkObjects', maptype.HRSC, ctypes.c_long, ctypes.POINTER(ctypes.c_uint), ctypes.c_int)
    def mapUpdateLinkObjects(_hrsc: maptype.HRSC, _semcode: int, _objlist: ctypes.POINTER(ctypes.c_uint), _count: int) -> int:
        """
        Обновить или добавить внешние коды объектов в записи таблицы связанных объектов
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _semcode: код семантики типа ``GUID``
        
        :param _objlist: указатель на массив внешних кодов объектов, которые могут быть связаны по заданной семантике
        
        :param _count: поле для записи числа кодов объектов в массиве
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если для semcode не было записи в таблице связанных объектов, то она будет создана
        """
        return mapUpdateLinkObjects_t (_hrsc, _semcode, _objlist, _count)

    mapDeleteLinkObjects_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteLinkObjects', maptype.HRSC, ctypes.c_long)
    def mapDeleteLinkObjects(_hrsc: maptype.HRSC, _semcode: int) -> int:
        """
        Удалить запись о связанных объектах по коду семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _semcode: код семантики типа ``GUID``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteLinkObjects_t (_hrsc, _semcode)

    mapGetRscGroupSemList_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.TGROUPSEMITEM),'mapGetRscGroupSemList', maptype.HRSC, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapGetRscGroupSemList(_hrsc: maptype.HRSC, _semcode: int, _count: ctypes.POINTER(ctypes.c_long)) -> ctypes.POINTER(maptype.TGROUPSEMITEM):
        """
        Запросить список кодов семантик в составе групповой семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _semcode: код групповой семантики
        
        :param _count: поле для записи числа семантик в списке
        
        :returns: Возвращает указатель на список кодов семантик, входящих в состав групповой семантики При ошибке возвращает ноль
        :rtype: ctypes.POINTER(maptype.TGROUPSEMITEM)
        """
        return mapGetRscGroupSemList_t (_hrsc, _semcode, _count)

    mapUpdateRscGroupSem_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateRscGroupSem', maptype.HRSC, ctypes.c_long, ctypes.POINTER(maptype.TGROUPSEMITEM), ctypes.c_long)
    def mapUpdateRscGroupSem(_hrsc: maptype.HRSC, _semcode: int, _list: ctypes.POINTER(maptype.TGROUPSEMITEM), _count: int) -> int:
        """
        Добавить или обновить запись в таблице
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _semcode: код групповой семантики
        
        :param _list: список кодов семантик, входящих в состав групповой семантики
        
        :param _count: число семантик в списке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если в классификаторе нет таблицы групповой семантики с заданным кодом семантики, то она будет создана
           Если таблица есть, то она будет обновлена
        """
        return mapUpdateRscGroupSem_t (_hrsc, _semcode, _list, _count)

    mapDeleteRscGroupSem_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteRscGroupSem', maptype.HRSC, ctypes.c_long)
    def mapDeleteRscGroupSem(_hrsc: maptype.HRSC, _semcode: int) -> int:
        """
        Удалить старый список
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _semcode: код групповой семантики
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если таблица есть, то она будет удалена
        """
        return mapDeleteRscGroupSem_t (_hrsc, _semcode)



def rscapi_healthcheck():
    return 1
