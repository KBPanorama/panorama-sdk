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
    *          Функции обработки растров - gis64picex.dll              *
    *                                                                  *
    *  Функции импорта графических файлов в RSW                        *
    *  Функции обработки файлов KMZ                                    *
    *  Функции экспорта RSW в графические форматы                      *
    *  Функции трансформирования, импорта и экспорта матриц из TIF     *
    *  Функции сохранения изображения карты (документа) в RSW, TIFF    *
    *  Функции оптимизации (сжатия) файлов растров и матриц            *
    *  Функции трансформирования растров                               *
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
    if os.environ['gispicexdll']:
        gispicexname = os.environ['gispicexdll']
except KeyError:
    gispicexname = 'gis64picex.dll'

try:
    picexlib = mapsyst.LoadLibrary(gispicexname)
except Exception as e:
    print(e)
    picexlib = 0

if picexlib == 0:
    print(gispicexname)
else:
    picexLoadRasterToRswUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'picexLoadRasterToRswUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long))
    def picexLoadRasterToRswUn(_handle: maptype.HMESSAGE, _srcname: mapsyst.WTEXT, _rswname: mapsyst.WTEXT, _retcode: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Выполнить импорт растровых данных в файл RSW
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки или ноль
        
        :param _srcname: имя входного файла (``TIF``, ``IMG``, ``PNG``, ``GIF``, ``JPG``, ``BMP``, ``PCX``)
        
        :param _rswname: имя выходного файла (``*.rsw``)
        
        :param _retcode: поле для записи кода ошибки (maperr.rh) Приоритет изъятия параметров привязки: ``1`` - cодержимое соответствующих тегов файлов ``TIF``, ``IMG`` ``2`` - файл привязки world.file ``3`` - файл привязки ``TAB`` (MapInfo) ``4`` - MAP (OziExplorer) ``5`` - ``PRJ`` Функция ищет файл привязки рядом с исходным файлом srcname, перебирая по приоритету типы файлов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return picexLoadRasterToRswUn_t (_handle, _srcname.buffer(), _rswname.buffer(), _retcode)

    picexLoadRasterToRswPro_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'picexLoadRasterToRswPro', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(maptype.IMPORTRASTERSPARAM), maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def picexLoadRasterToRswPro(_handle: maptype.HMESSAGE, _srcname: mapsyst.WTEXT, _rswname: mapsyst.WTEXT, _param: ctypes.POINTER(maptype.IMPORTRASTERSPARAM), _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Выполнить импорт графического файла в файл RSW с автоматической установкой привязки и параметров проекции
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки или ноль
        
        :param _srcname: имя входного файла (``TIF``, ``IMG``, ``PNG``, ``GIF``, ``JPG``, ``BMP``, ``PCX``)
        
        :param _rswname: имя выходного файла (``*.rsw``)
        
        :param _param: параметры импорта графических файлов или ``0`` (cтруктура ``IMPORTRASTERSPARAM`` объявлена в picexprm.h)
        
        :param _callevent: адрес функции обратного вызова для уведомления о проценте обработанных наборов данных (maptype.h)
        
        :param _parm: адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы) вторым параметром в вызываемой функции передается процент от ``0`` до ``100`` Привязка растра, параметры проекции и системы координат определяются функцией по тегам файлов GeoTIFF, ``IMG``, из файлов привязки ``WORLD`` ``FILE``, ``TAB`` (MapInfo), MAP (OziExplorer), из файлов параметров проекции ``PRJ``. Приоритет изъятия параметров привязки: ``1`` - содержимое соответствующих тегов файлов ``TIF``, ``IMG`` ``2`` - файл привязки world.file ``3`` - файл привязки ``TAB`` (MapInfo) ``4`` - MAP (OziExplorer) ``5`` - ``PRJ`` Функция ищет файл привязки рядом с исходным файлом srcname, перебирая по приоритету типы файлов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return picexLoadRasterToRswPro_t (_handle, _srcname.buffer(), _rswname.buffer(), _param, _callevent, _parm)

    picexLoadRastersListToRswPro_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'picexLoadRastersListToRswPro', maptype.HMESSAGE, ctypes.POINTER(ctypes.POINTER(maptype.WCHAR)), ctypes.c_int, maptype.PWCHAR, ctypes.POINTER(maptype.IMPORTRASTERSPARAM))
    def picexLoadRastersListToRswPro(_handle: maptype.HMESSAGE, _imagelist: ctypes.POINTER(ctypes.POINTER(maptype.WCHAR)), _imagecount: int, _outputfilename: mapsyst.WTEXT, _param: ctypes.POINTER(maptype.IMPORTRASTERSPARAM)) -> int:
        """
        Выполнить импорт списка файлов растровых данных в файлы формата RSW в многопоточном режиме
        
        :param _handle: идентификатор диалога визуального сопровождения процесса обработки
        
        :param _imagelist: список файлов растровых данных
        
        :param _imagecount: количество файлов в списке imageList
        
        :param _outputfilename: имя формируемого файла проекта MPT или путь к выходной папке
        
        :param _param: параметры импорта графических файлов (структура ``IMPORTRASTERSPARAM`` объявлена в picexprm.h) Функция при импорте нескольких графических файлов формирует растры RSW и файл проекта MPT в выходной папке Выходные растры создаются в папке файла MPT, указанного в аргументе outputFileName
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если в списке imageList несколько растров, то аргумент outputFileName должен содержать имя файла проекта MPT
           Если в списке imageList указан один растр, то аргумент outputFileName должен содержать полный путь к выходной папке
        """
        return picexLoadRastersListToRswPro_t (_handle, _imagelist, _imagecount, _outputfilename.buffer(), _param)

    picexLoadJpegToRswAndCompressJPEG_Un_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'picexLoadJpegToRswAndCompressJPEG_Un', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int, ctypes.c_int, ctypes.c_int)
    def picexLoadJpegToRswAndCompressJPEG_Un(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _inputname: mapsyst.WTEXT, _rstname: mapsyst.WTEXT, _meterinelementx: ctypes.POINTER(ctypes.c_double), _meterinelementy: ctypes.POINTER(ctypes.c_double), _point: ctypes.POINTER(maptype.DOUBLEPOINT), _compression: int, _compressjpegquality: int, _flagmessage: int) -> int:
        """
        Выполнить импорт растровых данных из файла JPEG в файл RSW
        
        :param _hmap: идентификатор открытых данных
        
        :param _handle: идентификатор диалога визуального сопровождения процесса обработки
        
        :param _inputname: имя ``JPEG``-файла
        
        :param _rstname: имя RSW-файла
        
        :param _meterinelementx: размер в метрах элемента по X
        
        :param _meterinelementy: размер в метрах элемента по Y
        
        :param _point: точка привязки растра (в метрах) - положение юго-западного угла растра в районе
        
        :param _compression: флаг использования сжатия при формировании ``RST``-файла: ``0`` - сжатие к блокам изображения не применено ``1`` - блоки должны быть сжаты по методу ``LZW`` ``2`` - блоки должны быть сжаты по методу ``JPEG`` (справедливо для ``24`` битных растров)
        
        :param _compressjpegquality: степень сжатия блока растра по алгоритму ``JPEG`` Возможные значения: ``1`` - ``100`` Рекомендуемое значение: ``60``
        
        :param _flagmessage: параметр не используется Управление диагностическими сообщениями осуществляется вызовом функции mapMessageEnable
        
        :returns: Если mapIsMessageEnable возвращает 0, то диагностические сообщения не выдаются При ошибке возвращает ноль
        :rtype: int
        """
        return picexLoadJpegToRswAndCompressJPEG_Un_t (_hmap, _handle, _inputname.buffer(), _rstname.buffer(), _meterinelementx, _meterinelementy, _point, _compression, _compressjpegquality, _flagmessage)

    picexGetAccessToGraphicFileUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'picexGetAccessToGraphicFileUn', maptype.HMESSAGE, ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.DOUBLEPOINT))
    def picexGetAccessToGraphicFileUn(_handle: maptype.HMESSAGE, _enablemessage: int, _sourcename: mapsyst.WTEXT, _outputname: mapsyst.WTEXT, _meterinelementx: ctypes.POINTER(ctypes.c_double), _meterinelementy: ctypes.POINTER(ctypes.c_double), _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Выполнить импорт растровой карты без копирования изображения в формат RSW
        
        :param _handle: идентификатор диалога визуального сопровождения процесса обработки
        
        :param _enablemessage: флаг выдачи сообщений: ``1``, сообщение выдает MessageBox ``0``, посылается сообщение диалогу ``WM_ERROR``
        
        :param _sourcename: имя исходного файла (``*.TIF``, ``*.IMG``, ``*.JPG``, ``*.PNG``, ``*.GIF``, ``*.BMP``)
        
        :param _outputname: имя выходного файла (``*.RSW``)
        
        :param _meterinelementx: размер в метрах элемента по X
        
        :param _meterinelementy: размер в метрах элемента по Y
        
        :param _point: привязка растра В качестве исходных данных в функцию могут передаваться имена файлов форматов: (``TIFF``, GeoTIFF, ``IMG``, ``JPEG``, ``PNG``, ``GIF``, ``BMP``) При успешном выполнении функции создается файл RSW с именем outputname В файл RSW записываются параметры загружаемого растра, при этом изображение в RSW не переносится Исходный и выходной (``*.RSW``) файлы должны находиться в одной папке Обзорное изображение растра записывается в файл ``*.TOF``, который создается в этой же папке Для доступа к изображению графического файла созданный файл outputname необходимо открыть вызовом функции mapOpenRstUn, или добавить в документ карты вызовом функции mapOpenRstForMapUn
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если в качестве исходного файла подается файл GeoTIFF, или файл IMG с геопривязанным изображением,
           то входные параметры meterinelementx, meterinelementy и point могут быть равны 0
        """
        return picexGetAccessToGraphicFileUn_t (_handle, _enablemessage, _sourcename.buffer(), _outputname.buffer(), _meterinelementx, _meterinelementy, _point)

    LoadTiffAccessToRswUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'LoadTiffAccessToRswUn', maptype.HMAP, maptype.HMESSAGE, ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.c_long, ctypes.c_long)
    def LoadTiffAccessToRswUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _enablemessage: int, _tiffname: mapsyst.WTEXT, _rstname: mapsyst.WTEXT, _scale: float, _precision: float, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _res: int, _rez1: int) -> int:
        """
        Выполнить импорт растровой карты из Tiff (GeoTiff) в RSW
        
        :param _hmap: идентификатор открытых данных
        
        :param _handle: идентификатор диалога визуального сопровождения процесса обработки
        
        :param _enablemessage: флаг выдачи сообщений: ``1``, сообщение выдает MessageBox ``0``, посылается сообщение диалогу ``WM_ERROR``
        
        :param _tiffname: имя ``TIF``-файла
        
        :param _rstname: имя ``RST``-файла
        
        :param _scale: знаменатель масштаба создаваемого растра, например ``1 000`` (``1 : 1 000``)
        
        :param _precision: разрешающая способность создаваемого растра (точек/метр), например ``12 000`` (примерно ``300`` dpi)
        
        :param _point: привязка растра
        
        :param _mapreg: параметры проекции
        
        :param _res: параметр не используется
        
        :param _rez1: параметр не используется Изображение в RSW не переносится, в RSW записываются заголовки, палитра, УК Управление диагностическими сообщениями осуществляется вызовом функции mapMessageEnable
        
        :returns: Если mapIsMessageEnable возвращает 0, то диагностические сообщения не выдаются При ошибке возвращает ноль
        :rtype: int
        """
        return LoadTiffAccessToRswUn_t (_hmap, _handle, _enablemessage, _tiffname.buffer(), _rstname.buffer(), _scale, _precision, _point, _mapreg, _res, _rez1)

    LoadTiffToRstAndCompressUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'LoadTiffToRstAndCompressUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_int)
    def LoadTiffToRstAndCompressUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _tiffname: mapsyst.WTEXT, _rstname: mapsyst.WTEXT, _scale: float, _precision: float, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _compression: int) -> int:
        """
        Выполнить импорт из формата TIFF в RSW
        
        :param _hmap: идентификатор открытых данных или ноль
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки или ноль
        
        :param _tiffname: имя читаемого ``TIF``-файла
        
        :param _rstname: имя создаваемого RSW-файла
        
        :param _scale: знаменатель масштаба создаваемого растра, например ``1 000`` (``1 : 1 000``)
        
        :param _precision: разрешающая способность создаваемого растра (точек/метр), например ``12 000`` (примерно ``300`` dpi)
        
        :param _point: точка привязки растра (в метрах), положение юго-западного угла растра в районе
        
        :param _compression: флаг выполнения сжатия при формировании ``RST``-файла (``0``/``1``)
        
        :returns: При ошибке функция возвращает ноль
        :rtype: int
        """
        return LoadTiffToRstAndCompressUn_t (_hmap, _handle, _tiffname.buffer(), _rstname.buffer(), _scale, _precision, _point, _compression)

    picexMultyChannelsTiffAccessToRswUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'picexMultyChannelsTiffAccessToRswUn', maptype.HMESSAGE, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.TAFPARM), maptype.PWCHAR, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.DOUBLEPOINT))
    def picexMultyChannelsTiffAccessToRswUn(_handle: maptype.HMESSAGE, _enablemessage: int, _tifffilenames: mapsyst.WTEXT, _sizetifffiles: int, _tafparm: ctypes.POINTER(maptype.TAFPARM), _rstname: mapsyst.WTEXT, _meterinpixelx: ctypes.POINTER(ctypes.c_double), _meterinpixely: ctypes.POINTER(ctypes.c_double), _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Выполнить импорт снимков Landsat, Kompsat и GeoEye, поставляемых в виде набора одноканальных TIF растров
        
        :param _handle: идентификатор диалога визуального сопровождения процесса обработки
        
        :param _enablemessage: флаг выдачи сообщений: ``1`` -  сообщение выдает MessageBox ``0`` -  посылается сообщение диалогу ``WM_ERROR``
        
        :param _tifffilenames: список имен одноканальных ``TIF`` растров, имена отделены друг от друга ``";"``
        
        :param _sizetifffiles: размер в байтах области памяти, выделенной для списка имен одноканальных ``TIF`` растров (включая завершающий ноль)
        
        :param _tafparm: параметры создания обзорного изображения графического файла, указатель на структуру ``TAFPARM``
        
        :param _rstname: имя выходного файла растровой карты RSW meterinelementx - размер в метрах элемента по X meterinelementy - размер в метрах элемента по Y
        
        :param _point: привязка растра Одноканальные ``TIF`` растры интерпретируются как разные каналы одного изображения Изображение в RSW не переносится, в RSW записывается служебная информация Для ускорения отображения растровых данных применяется произвольная схема создаваемых обзорных изображений: ``1:4``, ``1:16``, ``1:64``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если исходный снимок содержит обзорные изображения, то они используются напрямую при создании
           производных обзорных изображений
           Возможно применение сжатия обзорных изображений
        """
        return picexMultyChannelsTiffAccessToRswUn_t (_handle, _enablemessage, _tifffilenames.buffer(), _sizetifffiles, _tafparm, _rstname.buffer(), _meterinpixelx, _meterinpixely, _point)

    picGetWidthAndHeightImage_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'picGetWidthAndHeightImage', maptype.PWCHAR, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def picGetWidthAndHeightImage(_imgname: mapsyst.WTEXT, _maxwidth: float, _maxheight: float, _widthcm: ctypes.POINTER(ctypes.c_double), _heightcm: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Рассчитать ширину и высоту изображения в см по размерам графического файла
        
        :param _imgname: графический файл
        
        :param _maxwidth: ширина допустимой области в шаблоне в см
        
        :param _maxheight: высота допустимой области в шаблоне в см
        
        :param _widthcm: поле для записи ширины изображения в см
        
        :param _heightcm: поле для записи высоты изображения в см
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return picGetWidthAndHeightImage_t (_imgname.buffer(), _maxwidth, _maxheight, _widthcm, _heightcm)

    picexLoadKmzToRsw_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'picexLoadKmzToRsw', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_int)
    def picexLoadKmzToRsw(_handle: maptype.HMESSAGE, _inputfilename: mapsyst.WTEXT, _outputfilename: mapsyst.WTEXT, _compression: int, _compressjpegquality: int) -> int:
        """
        Выполнить импорт растровой карты из KMZ в RSW
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _inputfilename: имя ``KMZ`` файла
        
        :param _outputfilename: имя проекта MPT
        
        :param _compression: флаг сжатия выходного файла: ``0`` - сжатие к блокам изображения применяться не будет ``1`` - сжатие изображения по методу ``LZW`` ``2`` - сжатие изображения по методу ``JPEG`` (справедливо для ``24`` битных растров)
        
        :param _compressjpegquality: степень сжатия блока растра по алгоритму ``JPEG``: возможные значения: ``1`` - ``100`` рекомендуемое значение: ``60``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return picexLoadKmzToRsw_t (_handle, _inputfilename.buffer(), _outputfilename.buffer(), _compression, _compressjpegquality)

    picexLoadKmzToMtw_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'picexLoadKmzToMtw', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def picexLoadKmzToMtw(_handle: maptype.HMESSAGE, _inputfilename: mapsyst.WTEXT, _outputfilename: mapsyst.WTEXT, _compression: int) -> int:
        """
        Выполнить импорт матрицы высот рельефа из KMZ в MTW
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _inputfilename: имя ``KMZ`` файла
        
        :param _outputfilename: имя проекта MPT
        
        :param _compression: флаг сжатия выходного файла Диалогу визуального сопровождения процесса обработки посылаются сообщения
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return picexLoadKmzToMtw_t (_handle, _inputfilename.buffer(), _outputfilename.buffer(), _compression)

    picexSaveRswImageToKmz_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'picexSaveRswImageToKmz', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def picexSaveRswImageToKmz(_handle: maptype.HMESSAGE, _sourcename: mapsyst.WTEXT, _outputname: mapsyst.WTEXT, _compress: int) -> int:
        """
        Сохранить изображение растра в файл формата KMZ
        
        :param _handle: идентификатор окна диалога сопровождения процесса обработки
        
        :param _sourcename: имя исходного файла RSW
        
        :param _outputname: имя выходного файла ``KMZ``
        
        :param _compress: коэффициент качества (``0````-100``) изображения при сжатии по методу ``JPEG`` Файл ``KMZ`` представляет собой ``ZIP``-архив пирамиды растровых тайлов в форматах ``JPEG`` или ``PNG``
        
        :returns: При ошибке функция возвращает ноль
        :rtype: int
        """
        return picexSaveRswImageToKmz_t (_handle, _sourcename.buffer(), _outputname.buffer(), _compress)

    picexSaveMatrixToKmz_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'picexSaveMatrixToKmz', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def picexSaveMatrixToKmz(_handle: maptype.HMESSAGE, _sourcename: mapsyst.WTEXT, _outputname: mapsyst.WTEXT, _compress: int) -> int:
        """
        Сохранить матрицу высот в файл формата KMZ
        
        :param _handle: идентификатор окна диалога сопровождения процесса обработки
        
        :param _sourcename: имя исходного файла RSW
        
        :param _outputname: имя выходного файла ``KMZ``
        
        :param _compress: флаг сжатия Файл ``KMZ`` представляет собой ``ZIP``-архив пирамиды тайлов в формате ``TIFF``
        
        :returns: При ошибке функция возвращает ноль
        :rtype: int
        """
        return picexSaveMatrixToKmz_t (_handle, _sourcename.buffer(), _outputname.buffer(), _compress)

    picexExportRasterToGraphicFilePro_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'picexExportRasterToGraphicFilePro', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def picexExportRasterToGraphicFilePro(_handle: maptype.HMESSAGE, _rswname: mapsyst.WTEXT, _outpitfilename: mapsyst.WTEXT, _floctype: int, _compressmethod: int, _compressjpegquality: int, _flag_useborder: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Выполнить экспорт RSW в файл формата TIFF, JPEG, BMP, PCX
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _rswname: имя файла растровой карты RSW
        
        :param _outpitfilename: имя выходного графического файла (``TIFF``, ``JPEG``, ``BMP``, ``PCX``)
        
        :param _floctype: тип файла привязки: ``1`` - файл привязки world file ``2`` - ``TAB`` (MapInfo)
        
        :param _compressmethod: флаг применения сжатия
        
        :param _compressjpegquality: степень сжатия изображения по алгоритму ``JPEG``: возможные значения: ``10`` - ``100`` рекомендуемое значение: ``60`` flaguseborder       - флаг ``"Вырезать изображение по рамке"``(``0``/``1``)
        
        :param _callevent: адрес функции обратного вызова для уведомления о проценте обработанных наборов данных (maptype.h)
        
        :param _parm: адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы) вторым параметром в вызываемой функции передается процент от ``0`` до ``100``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return picexExportRasterToGraphicFilePro_t (_handle, _rswname.buffer(), _outpitfilename.buffer(), _floctype, _compressmethod, _compressjpegquality, _flag_useborder, _callevent, _parm)

    picexExportRastersToGraphicFilesEx_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'picexExportRastersToGraphicFilesEx', maptype.HMESSAGE, ctypes.POINTER(ctypes.POINTER(maptype.WCHAR)), ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def picexExportRastersToGraphicFilesEx(_handle: maptype.HMESSAGE, _filelist: ctypes.POINTER(ctypes.POINTER(maptype.WCHAR)), _count: int, _outputdir: mapsyst.WTEXT, _outputfileformat: mapsyst.WTEXT, _floctype: int, _compressmethod: int, _compressjpegquality: int, _flaguseborder: int) -> int:
        """
        Выполнить экспорт списка файлов RSW в файлы формата TIFF, JPEG, BMP, PCX
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _filelist: список указателей на имена файлов экспортируемых растров RSW
        
        :param _count: количество файлов в списке filelist
        
        :param _outputdir: папка для выходных файлов (``TIFF``, ``JPEG``, ``BMP``, ``PCX``)
        
        :param _outputfileformat: расширение выходного файла (``".TIF"``, ``".JPG"``, ``".BMP"``, ``".PCX"``), формат формируемых выходных файлов
        
        :param _floctype: тип файла привязки: ``1`` - файл привязки world file ``2`` - ``TAB`` (MapInfo)
        
        :param _compressmethod: флаг применения сжатия
        
        :param _compressjpegquality: степень сжатия изображения по алгоритму ``JPEG``: возможные значения: ``10`` - ``100`` рекомендуемое значение: ``60``
        
        :param _flaguseborder: флаг ``"Вырезать изображение по рамке"``(``0``/``1``)
        
        :returns: Функция возвращает количество успешно экспортируемых файлов При ошибке возвращает ноль
        :rtype: int
        """
        return picexExportRastersToGraphicFilesEx_t (_handle, _filelist, _count, _outputdir.buffer(), _outputfileformat.buffer(), _floctype, _compressmethod, _compressjpegquality, _flaguseborder)

    picexSaveRswToJpegUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'picexSaveRswToJpegUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def picexSaveRswToJpegUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _rswname: mapsyst.WTEXT, _jpegname: mapsyst.WTEXT, _compressjpegquality: int) -> int:
        """
        Выполнить экспорт 24-х битного растра RSW в файл JPEG
        
        :param _hmap: идентификатор открытых данных
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _rswname: имя файла ``24``-х битного растра RSW
        
        :param _jpegname: имя файла ``JPEG``
        
        :param _compressjpegquality: степень сжатия блока растра по алгоритму ``JPEG``: возможные значения: ``10`` - ``100`` рекомендуемое значение: ``60``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return picexSaveRswToJpegUn_t (_hmap, _handle, _rswname.buffer(), _jpegname.buffer(), _compressjpegquality)

    LoadRasterToTiffConverter_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'LoadRasterToTiffConverter', maptype.HMAP, maptype.HMESSAGE, ctypes.c_int, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.DFRAME))
    def LoadRasterToTiffConverter(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _rstnumber: int, _tiffname: mapsyst.WTEXT, _flagborder: int, _compressmethod: int, _flagcmyk: int, _flagintergraph: int, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Выполнить экспорт RSW в формат TIFF
        
        :param _hmap: идентификатор открытых данных
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _rstnumber: номер RSW файла
        
        :param _tiffname: имя ``TIFF`` файла
        
        :param _flagborder: флаг использования рамки растровой карты: ``0`` - включать в формируемый файл все блоки изображения (рекомендуемое значение) ``1`` - не включать в формируемый файл блоки изображения не входящие в область, ограниченную рамкой
        
        :param _compressmethod: флаг сжатия изображения (``0`` - не применять сжатие, ``1`` - сжатие PackBit), рекомендуемое значение - ``0``
        
        :param _flagcmyk: выбор цветовой модели: ``0`` - цветовая модель ``RGB`` ``24`` бит на пиксел ``1`` - цветовая модель ``CMYK`` ``32`` бит на пиксел режим поддерживается только для  растров ``24``,``32`` бит на пиксел
        
        :param _flagintergraph: флаг записи матрицы трансформирования с помощью которой Intergraph определяет привязку растра
        
        :param _dframe: габариты изображения в районе в метрах, параметр обязателен для записи матрицы трансформирования, если flagIntergraph ``= 1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return LoadRasterToTiffConverter_t (_hmap, _handle, _rstnumber, _tiffname.buffer(), _flagborder, _compressmethod, _flagcmyk, _flagintergraph, _dframe)

    MtwTransformingBySquareMethodUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'MtwTransformingBySquareMethodUn', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def MtwTransformingBySquareMethodUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _parm: ctypes.POINTER(maptype.TASKPARMEX), _sourcename: mapsyst.WTEXT, _outputname: mapsyst.WTEXT, _sizenameout: int, _count: int, _fact: ctypes.POINTER(maptype.DOUBLEPOINT), _teor: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Трансформировать матрицу (вычисление коэффициентов пересчета координат методом наименьших квадратов)
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _hmap: идентификатор открытых данных
        
        :param _parm: параметры прикладной задачи
        
        :param _sourcename: имя исходного растра (``MAX_PATH_LONG``)
        
        :param _outputname: имя выходного растра (размер выделенной памяти не менее ``MAX_PATH_LONG`` символов), в случае незаданного или совпадающего с исходным выходного имени, будет создана копия исходной матрицы - <имя_исходной_матрицы>~.mtw результат будет записан в исходный файл
        
        :param _sizenameout: размер выделенной памяти для outputname в байтах
        
        :param _count: количество опорных точек
        
        :param _fact: исходные координаты опоры
        
        :param _teor: желаемые координаты опоры
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return MtwTransformingBySquareMethodUn_t (_hmap, _handle, _parm, _sourcename.buffer(), _outputname.buffer(), _sizenameout, _count, _fact, _teor)

    picexMatrixParametersChange_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'picexMatrixParametersChange', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(maptype.BUILDMTW), ctypes.c_long)
    def picexMatrixParametersChange(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _sourcemtwname: mapsyst.WTEXT, _outputmtwname: mapsyst.WTEXT, _newparam: ctypes.POINTER(maptype.BUILDMTW), _flagsmoothing: int) -> int:
        """
        Сформировать матрицу высот с измененными параметрами из исходной
        
        :param _hmap: идентификатор открытых данных
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _sourcemtwname: имя исходной матрицы высот
        
        :param _outputmtwname: имя выходной матрицы высот
        
        :param _newparam: указатель на структуру новых параметров выходной матрицы
        
        :param _flagsmoothing: флаг cглаживания высот
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return picexMatrixParametersChange_t (_hmap, _handle, _sourcemtwname.buffer(), _outputmtwname.buffer(), _newparam, _flagsmoothing)

    LoadMtwToTiff_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'LoadMtwToTiff', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(maptype.EXPORTMATRIXPARAM))
    def LoadMtwToTiff(_handle: maptype.HMESSAGE, _mtwname: mapsyst.WTEXT, _tiffname: mapsyst.WTEXT, _filename: mapsyst.WTEXT, _param: ctypes.POINTER(maptype.EXPORTMATRIXPARAM)) -> int:
        """
        Сохранить матрицу в формате TIFF (BigTIFF)
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _mtwname: имя файла матрицы
        
        :param _tiffname: имя ``TIFF``-файла
        
        :param _filename: имя файла параметров геопривязки (``TFW``, ``TAB``)
        
        :param _param: параметры экспорта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return LoadMtwToTiff_t (_handle, _mtwname.buffer(), _tiffname.buffer(), _filename.buffer(), _param)

    LoadMtwToTiffConverterExUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'LoadMtwToTiffConverterExUn', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.DFRAME))
    def LoadMtwToTiffConverterExUn(_handle: maptype.HMESSAGE, _mtwname: mapsyst.WTEXT, _tiffname: mapsyst.WTEXT, _filename: mapsyst.WTEXT, _flagborder: int, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Сохранить матрицу в формате TIFF
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _mtwname: имя файла матрицы
        
        :param _tiffname: имя ``TIFF``-файла
        
        :param _filename: имя файла параметров (``TFW``, ``TAB``)
        
        :param _flagborder: флаг использования рамки: ``0`` - включать в формируемый файл все элементы матрицы ``1`` - не включать в формируемый файл элементы матрицы не входящие в область, ограниченную рамкой
        
        :param _dframe: прямоугольная область сохраняемых элементов матрицы или ``0``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return LoadMtwToTiffConverterExUn_t (_handle, _mtwname.buffer(), _tiffname.buffer(), _filename.buffer(), _flagborder, _dframe)

    LoadMtwToBigTiffConverter_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'LoadMtwToBigTiffConverter', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.DFRAME))
    def LoadMtwToBigTiffConverter(_handle: maptype.HMESSAGE, _mtwname: mapsyst.WTEXT, _tiffname: mapsyst.WTEXT, _filename: mapsyst.WTEXT, _flagborder: int, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Сохранить матрицу в формате BigTIFF
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _mtwname: имя файла матрицы
        
        :param _tiffname: имя ``TIFF``-файла
        
        :param _filename: имя файла параметров (``TFW``, ``TAB``)
        
        :param _flagborder: флаг использования рамки: ``0`` - включать в формируемый файл все элементы матрицы ``1`` - не включать в формируемый файл элементы матрицы не входящие в область, ограниченную рамкой
        
        :param _dframe: прямоугольная область сохраняемых элементов матрицы или ``0``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return LoadMtwToBigTiffConverter_t (_handle, _mtwname.buffer(), _tiffname.buffer(), _filename.buffer(), _flagborder, _dframe)

    LoadGeoTiffToMtwPro_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'LoadGeoTiffToMtwPro', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_double, ctypes.c_long, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def LoadGeoTiffToMtwPro(_handle: maptype.HMESSAGE, _tiffname: mapsyst.WTEXT, _mtwname: mapsyst.WTEXT, _scale: float, _flagcompress: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Загрузить матрицу из формата SRTM (GeoTIFF)
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _tiffname: имя исходного файла формата ``SRTM`` (GeoTIFF)
        
        :param _mtwname: имя файла формируемой матрицы
        
        :param _scale: масштаб формируемой матрицы
        
        :param _flagcompress: параметр не используется, равен ``0``
        
        :param _callevent: адрес функции обратного вызова для уведомления о проценте обработанных наборов данных (maptype.h)
        
        :param _parm: адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы) вторым параметром в вызываемой функции передается процент от ``0`` до ``100``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return LoadGeoTiffToMtwPro_t (_handle, _tiffname.buffer(), _mtwname.buffer(), _scale, _flagcompress, _callevent, _parm)

    MtqTransformingBySquareMethodUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'MtqTransformingBySquareMethodUn', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def MtqTransformingBySquareMethodUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _parm: ctypes.POINTER(maptype.TASKPARMEX), _sourcename: mapsyst.WTEXT, _outputname: mapsyst.WTEXT, _sizenameout: int, _count: int, _fact: ctypes.POINTER(maptype.DOUBLEPOINT), _teor: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Трансформировать матрицу качеств (вычисление коэффициентов пересчета координат методом наименьших квадратов)
        
        :param _hmap: идентификатор открытых данных
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _parm: параметры прикладной задачи
        
        :param _sourcename: имя исходноЙ матрицы качеств(``MAX_PATH_LONG``)
        
        :param _outputname: имя выходной матрицы качеств в случае незаданного или совпадающего с исходным выходного имени, будет создана копия исходной матрицы - <имя_исходной_матрицы>~.mtq результат будет записан в исходный файл
        
        :param _sizenameout: размер выделенной памяти для outputname
        
        :param _count: количество опорных точек
        
        :param _fact: исходные координаты опоры
        
        :param _teor: желаемые координаты опоры
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return MtqTransformingBySquareMethodUn_t (_hmap, _handle, _parm, _sourcename.buffer(), _outputname.buffer(), _sizenameout, _count, _fact, _teor)

    LoadDocumentImageToRswFile_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'LoadDocumentImageToRswFile', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_double, ctypes.c_int)
    def LoadDocumentImageToRswFile(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _filename: mapsyst.WTEXT, _dframe: ctypes.POINTER(maptype.DFRAME), _bitcount: int, _meterinelement: float, _flagcompress: int) -> int:
        """
        Сохранить карту в формате RSW
        
        :param _hmap: идентификатор открытых данных
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _filename: имя файла сохраняемого изображения RSW
        
        :param _dframe: фрагмент сохраняемой карты (в метрах на местности)
        
        :param _bitcount: количество бит на пиксель сохраняемого изображения
        
        :param _meterinelement: размер пикселя сохраняемого изображения в метрах
        
        :param _flagcompress: флаг сжатия изображения
        
        :returns: При ошибке функция возвращает ноль
        :rtype: int
        """
        return LoadDocumentImageToRswFile_t (_hmap, _handle, _filename.buffer(), _dframe, _bitcount, _meterinelement, _flagcompress)

    LoadDocumentImageToPictureFile_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'LoadDocumentImageToPictureFile', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_double, ctypes.c_int)
    def LoadDocumentImageToPictureFile(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _filename: mapsyst.WTEXT, _dframe: ctypes.POINTER(maptype.DFRAME), _bitcount: int, _meterinelement: float, _flagcompress: int) -> int:
        """
        Сохранить карту в формате BMP, JPEG, PNG
        
        :param _hmap: идентификатор открытых данных
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _filename: имя файла сохраняемого изображения
        
        :param _dframe: фрагмент сохраняемой карты(в метрах на местности)
        
        :param _bitcount: количество бит на пиксель сохраняемого изображения
        
        :param _meterinelement: размер пикселя сохраняемого изображения в метрах
        
        :param _flagcompress: флаг сжатия изображения при сохранении файла ``TIFF``: (``0`` - не сжимать, ``1`` - сжатие PackBit) - коэффициент качества изображения при сжатии ``JPEG`` (``0````-100``) при сохранении файла ``JPG``
        
        :returns: При ошибке функция возвращает ноль
        :rtype: int
        """
        return LoadDocumentImageToPictureFile_t (_hmap, _handle, _filename.buffer(), _dframe, _bitcount, _meterinelement, _flagcompress)

    LoadDocumentImageToTiffFile_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'LoadDocumentImageToTiffFile', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_double, ctypes.c_int, ctypes.c_int)
    def LoadDocumentImageToTiffFile(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _filename: mapsyst.WTEXT, _dframe: ctypes.POINTER(maptype.DFRAME), _bitcount: int, _meterinelement: float, _flagcompress: int, _flagintergraph: int) -> int:
        """
        Сохранить карту в формате TIFF
        
        :param _hmap: идентификатор открытых данных
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _filename: имя файла сохраняемого изображения
        
        :param _dframe: фрагмент сохраняемой карты (в метрах на местности)
        
        :param _bitcount: количество бит на пиксель сохраняемого изображения
        
        :param _meterinelement: размер пикселя сохраняемого изображения в метрах
        
        :param _flagcompress: флаг сжатия изображения при сохранении файла ``TIFF``: (``0`` - не сжимать, ``1`` - сжатие PackBit) - коэффициент качества изображения при сжатии ``JPEG`` (``0````-100``) при сохранении файла ``JPG``
        
        :param _flagintergraph: флаг записи матрицы трансформирования для использования в программе Intergraph
        
        :returns: При ошибке функция возвращает ноль
        :rtype: int
        """
        return LoadDocumentImageToTiffFile_t (_hmap, _handle, _filename.buffer(), _dframe, _bitcount, _meterinelement, _flagcompress, _flagintergraph)

    LoadDocumentImageToGrayScaleTiffFile_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'LoadDocumentImageToGrayScaleTiffFile', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME), ctypes.c_double)
    def LoadDocumentImageToGrayScaleTiffFile(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _filename: mapsyst.WTEXT, _dframe: ctypes.POINTER(maptype.DFRAME), _meterinelement: float) -> int:
        """
        Сохранить карту в формате TIFF GrayScale (8 бит на пиксель)
        
        :param _hmap: идентификатор открытых данных
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _filename: имя файла сохраняемого изображения
        
        :param _dframe: фрагмент сохраняемой карты(в метрах на местности)
        
        :param _meterinelement: размер пикселя сохраняемого изображения в метрах
        
        :returns: При ошибке функция возвращает ноль
        :rtype: int
        """
        return LoadDocumentImageToGrayScaleTiffFile_t (_hmap, _handle, _filename.buffer(), _dframe, _meterinelement)

    picexSaveRswImageToKmz_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'picexSaveRswImageToKmz', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def picexSaveRswImageToKmz(_handle: maptype.HMESSAGE, _inputfilename: mapsyst.WTEXT, _outputfilename: mapsyst.WTEXT, _compress: int) -> int:
        """
        Сохранить изображение растра в файл формата KMZ
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _inputfilename: имя входного файла
        
        :param _outputfilename: имя выходного файла
        
        :param _compress: коэффициент качества (``0````-100``) ``JPEG``-изображения при сжатии по ``JPEG`` методу Файл ``KMZ`` представляет собой ``ZIP``-архив пирамиды растровых тайлов в форматах ``JPEG`` или ``PNG``
        
        :returns: При ошибке функция возвращает ноль
        :rtype: int
        """
        return picexSaveRswImageToKmz_t (_handle, _inputfilename.buffer(), _outputfilename.buffer(), _compress)

    LoadMapToPictureFileUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'LoadMapToPictureFileUn', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(maptype.DFRAME), ctypes.c_int, ctypes.c_int, ctypes.c_int, maptype.PWCHAR, ctypes.c_int, ctypes.c_int, maptype.HMESSAGE, ctypes.c_int)
    def LoadMapToPictureFileUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _dframe: ctypes.POINTER(maptype.DFRAME), _bitcount: int, _scale: int, _resolution: int, _filename: mapsyst.WTEXT, _flagintergraph: int, _flagcompress: int, _handlemainwin: maptype.HMESSAGE, _flafadjustmode: int) -> int:
        """
        Сохранить изображение карты в формате BMP, Tiff, JPG, RSW
        
        :param _hmap: идентификатор открытых данных
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _dframe: фрагмент сохраняемой карты(в метрах на местности)
        
        :param _bitcount: кол-во бит на пиксел сохраняемого изображения (``16``, ``24``-рекомендуемое значение, ``32``)
        
        :param _scale: масштаб сохраняемого изображения
        
        :param _resolution: разрешающая способность сохраняемого изображения (точек на дюйм)
        
        :param _filename: имя файла сохраняемого изображения (``*.bmp``, ``*.tif``)
        
        :param _flagintergraph: флаг записи матрицы трансформирования для использования в программе Intergraph, аргумент flagintergraph применим при сохранении файла ``TIFF``
        
        :param _flagcompress: флаг сжатия изображения при сохранении файла ``TIFF``: (``0`` - не сжимать, ``1`` - сжатие PackBit) - коэффициент качества изображения при сжатии ``JPEG`` (``0````-100``) при сохранении файла ``JPG``
        
        :param _handlemainwin: должен быть равен нулю
        
        :param _flafadjustmode: флаг установки доступности для выполнения команды Adjust: ``0`` - adjustmode не устанавливался ``1`` - adjustmode уже установлен до вызова функции
        
        :returns: При ошибке функция возвращает ноль
        :rtype: int
        """
        return LoadMapToPictureFileUn_t (_hmap, _handle, _dframe, _bitcount, _scale, _resolution, _filename.buffer(), _flagintergraph, _flagcompress, _handlemainwin, _flafadjustmode)

    LoadRstOptimizationPro_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'LoadRstOptimizationPro', maptype.HMESSAGE, maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def LoadRstOptimizationPro(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP, _name: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _compressnumber: int, _jpegcompressvalue: int, _flagborder: int, _flagsavecopy: int, _flagduplicate: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Оптимизировать файл растровой карты с возможным сжатием изображения и созданием уменьшенной копии растра
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _hmap: идентификатор открытых данных
        
        :param _name: имя файла растровой карты
        
        :param _newname: имя файла оптимизированной растровой карты
        
        :param _compressnumber: номер алгоритма сжатия блоков изображения: ``0`` - не использовать сжатие ``1`` - алгоритм сжатия ``LZW`` ``2`` - алгоритм сжатия ``JPEG`` (для ``24`` битных растров)
        
        :param _jpegcompressvalue: степень сжатия изображения растра по алгоритму ``JPEG``, если compressnumber ``= 2`` (``1````-100``, ``1``-максимальное сжатие, ``100``-сжатие без потери качества), рекомендуется значение ``60``.
        
        :param _flagborder: флаг использования рамки растровой карты: ``0`` - включать в формируемый файл все блоки изображения ``1`` - не включать в формируемый файл блоки изображения не входящие в область, ограниченную рамкой
        
        :param _flagsavecopy: флаг сохранения копии исходного файла с именем ``*``.~rw: ``0`` - не создавать копию исходного файла ``1`` - создать копию исходного файла
        
        :param _flagduplicate: флаг создания уменьшенной копии растра: ``0`` - не создавать уменьшенную копию растра ``1`` - создавать уменьшенную копию растра
        
        :param _callevent: адрес функции обратного вызова для уведомления о проценте обработанных наборов данных (maptype.h)
        
        :param _parm: адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы) вторым параметром в вызываемой функции передается процент от ``0`` до ``100`` Добавлен пересчет габаритов растра при обрезке изображения по рамке растра (когда flagborder ``= 1``).
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return LoadRstOptimizationPro_t (_handle, _hmap, _name.buffer(), _newname.buffer(), _compressnumber, _jpegcompressvalue, _flagborder, _flagsavecopy, _flagduplicate, _callevent, _parm)

    LoadMtrOptimizationPro_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'LoadMtrOptimizationPro', maptype.HMESSAGE, maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def LoadMtrOptimizationPro(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP, _name: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _compressnumber: int, _flagborder: int, _flagsavecopy: int, _flagduplicate: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Оптимизировать файл матрицы высот с возможным сжатием изображения и созданием уменьшенной копии изображения
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _hmap: идентификатор открытых данных
        
        :param _name: имя файла матрицы высот
        
        :param _newname: имя файла оптимизированной матрицы высот
        
        :param _compressnumber: номер алгоритма сжатия блоков: ``0`` - не использовать сжатие ``32`` - алгоритм сжатия матрицы
        
        :param _flagborder: флаг использования рамки матрицы высот: ``0`` - включать в формируемый файл все блоки изображения ``1`` - не включать в формируемый файл блоки изображения не входящие в область, ограниченную рамкой
        
        :param _flagsavecopy: флаг сохранения копии исходного файла: ``0`` - не создавать копию исходного файла ``1`` - создать копию исходного файла
        
        :param _flagduplicate: флаг создания уменьшенной копии: ``0`` - не создавать уменьшенную копию ``1`` - создавать уменьшенную копию
        
        :param _callevent: адрес функции обратного вызова для уведомления о проценте обработанных наборов данных (maptype.h)
        
        :param _parm: адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы) вторым параметром в вызываемой функции передается процент от ``0`` до ``100`` Добавлен пересчет габаритов матрицы высот при обрезке изображения по рамке матрицы высот (когда flagborder =``= 1``).
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return LoadMtrOptimizationPro_t (_handle, _hmap, _name.buffer(), _newname.buffer(), _compressnumber, _flagborder, _flagsavecopy, _flagduplicate, _callevent, _parm)

    picexMtqOptimizationPro_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'picexMtqOptimizationPro', maptype.HMESSAGE, maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def picexMtqOptimizationPro(_handle: maptype.HMESSAGE, _hmap: maptype.HMAP, _name: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _compressnumber: int, _flagborder: int, _flagsavecopy: int, _flagduplicate: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Оптимизировать файл матрицы качества MTQ с возможным сжатием изображения и созданием уменьшенной копии изображения
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _hmap: идентификатор открытых данных
        
        :param _name: имя файла матрицы качества MTQ
        
        :param _newname: имя файла оптимизированной матрицы качества MTQ
        
        :param _compressnumber: номер алгоритма сжатия блоков: ``0`` - не использовать сжатие ``32`` - алгоритм сжатия матрицы
        
        :param _flagborder: флаг использования рамки матрицы качества MTQ ``0`` - включать в формируемый файл все блоки изображения ``1`` - не включать в формируемый файл блоки изображения не входящие в область, ограниченную рамкой
        
        :param _flagsavecopy: флаг сохранения копии исходного файла: ``0`` - не создавать копию исходного файла ``1`` - создать копию исходного файла
        
        :param _flagduplicate: флаг создания уменьшенной копии: ``0`` - не создавать уменьшенную копию ``1`` - создавать уменьшенную копию
        
        :param _callevent: адрес функции обратного вызова для уведомления о проценте обработанных наборов данных (maptype.h)
        
        :param _parm: адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы) вторым параметром в вызываемой функции передается процент от ``0`` до ``100`` Внимание: сжатие может быть применено к матрицам с размером элемента в ``4`` байта Добавлен пересчет габаритов матрицы качества MTQ при обрезке изображения по рамке матрицы качества MTQ (когда flagborder =``= 1``).
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return picexMtqOptimizationPro_t (_handle, _hmap, _name.buffer(), _newname.buffer(), _compressnumber, _flagborder, _flagsavecopy, _flagduplicate, _callevent, _parm)

    AttachRswWithScalingAndRotationExUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'AttachRswWithScalingAndRotationExUn', maptype.HMAP, maptype.HMESSAGE, maptype.PWCHAR, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long)
    def AttachRswWithScalingAndRotationExUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _rswnamein: mapsyst.WTEXT, _sizenamein: int, _rswnameout: mapsyst.WTEXT, _sizenameout: int, _pointmet1: ctypes.POINTER(maptype.DOUBLEPOINT), _pointmetnew1: ctypes.POINTER(maptype.DOUBLEPOINT), _pointmet2: ctypes.POINTER(maptype.DOUBLEPOINT), _pointmetnew2: ctypes.POINTER(maptype.DOUBLEPOINT), _message: int) -> int:
        """
        Выполнить привязку растра с масштабированием и поворотом по двум точкам
        
        :param _hmap: идентификатор открытых данных
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _rswnamein: имя исходного файла растра
        
        :param _sizenamein: размер строки rswnamein в байтах
        
        :param _rswnameout: имя выходного файла растра (размер строки не менее ``MAX_PATH_LONG`` байт) в случае не заданного или совпадающего с исходным выходного имени, будет создана копия исходного растра с именем вида - <имя_исходного_растра>~.rsw результат будет записан вместо исходного файла
        
        :param _sizenameout: размер строки rswnameout в байтах
        
        :param _pointmet1: исходные координаты первой точки  в метрах
        
        :param _pointmetnew1: устанавливаемые координаты первой точки в метрах
        
        :param _pointmet2: исходные координаты второй точки  в метрах
        
        :param _pointmetnew2: устанавливаемые координаты второй точки в метрах
        
        :param _message: флаг на выдачу сообщений (``0``/``1``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return AttachRswWithScalingAndRotationExUn_t (_hmap, _handle, _rswnamein.buffer(), _sizenamein, _rswnameout.buffer(), _sizenameout, _pointmet1, _pointmetnew1, _pointmet2, _pointmetnew2, _message)

    RswTransformingBySquareMethodUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'RswTransformingBySquareMethodUn', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def RswTransformingBySquareMethodUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _parm: ctypes.POINTER(maptype.TASKPARMEX), _sourcename: mapsyst.WTEXT, _outputname: mapsyst.WTEXT, _sizenameout: int, _count: int, _fact: ctypes.POINTER(maptype.DOUBLEPOINT), _teor: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Трансформировать растр (вычисление коэффициентов пересчета координат методом наименьших квадратов)
        
        :param _hmap: идентификатор открытых данных
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки map         - карта,содержащая векторные данные
        
        :param _parm: параметры прикладной задачи
        
        :param _sourcename: имя исходного растра (``MAX_PATH_LONG``)
        
        :param _outputname: имя выходного растра (размер выделенной памяти не менее ``MAX_PATH_LONG`` символов) в случае не заданного или совпадающего с исходным выходного имени, будет создана копия исходного растра - <имя_исходного_растра>~.rsw результат будет записан в исходный файл
        
        :param _sizenameout: размер выделенной памяти для outputname в байтах
        
        :param _count: количество опорных точек (не меньше ``4``-х)
        
        :param _fact: исходные координаты опоры
        
        :param _teor: желаемые координаты опоры
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return RswTransformingBySquareMethodUn_t (_hmap, _handle, _parm, _sourcename.buffer(), _outputname.buffer(), _sizenameout, _count, _fact, _teor)

    RswTransformingByBorderMethodUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'RswTransformingByBorderMethodUn', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def RswTransformingByBorderMethodUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _parm: ctypes.POINTER(maptype.TASKPARMEX), _sourcename: mapsyst.WTEXT, _outputname: mapsyst.WTEXT, _count: int, _fact: ctypes.POINTER(maptype.DOUBLEPOINT), _teor: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Трансформировать растр по рамке листа карты
        
        :param _hmap: идентификатор открытых данных
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _parm: параметры прикладной задачи
        
        :param _sourcename: имя исходного растра
        
        :param _outputname: имя выходного растра
        
        :param _count: количество опорных точек (не меньше ``4``-х)
        
        :param _fact: исходные координаты опоры
        
        :param _teor: желаемые координаты опоры
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return RswTransformingByBorderMethodUn_t (_hmap, _handle, _parm, _sourcename.buffer(), _outputname.buffer(), _count, _fact, _teor)

    RswTransformingWithBorderSettingUn_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'RswTransformingWithBorderSettingUn', maptype.HMAP, maptype.HMESSAGE, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.COLORREF), ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def RswTransformingWithBorderSettingUn(_hmap: maptype.HMAP, _handle: maptype.HMESSAGE, _parm: ctypes.POINTER(maptype.TASKPARMEX), _sourcename: mapsyst.WTEXT, _outputname: mapsyst.WTEXT, _count: int, _fact: ctypes.POINTER(maptype.DOUBLEPOINT), _teor: ctypes.POINTER(maptype.DOUBLEPOINT), _colortransparent: ctypes.POINTER(maptype.COLORREF), _flagcutting: int, _flagduplicate: int, _flagbordernew: int) -> int:
        """
        Трансформировать растр по рамке листа карты (нелинейное трансформирование)
        
        :param _hmap: идентификатор открытых данных
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _parm: параметры прикладной задачи
        
        :param _sourcename: имя исходного растра
        
        :param _outputname: имя выходного растра
        
        :param _count: количество опорных точек (не меньше ``4``-х)
        
        :param _fact: исходные координаты опоры
        
        :param _teor: желаемые координаты опоры
        
        :param _colortransparent: указатель на неотображаемый цвет (если colortransparent !``= 0``,
        
        :param _flagcutting: флаг обрезки изображения выходного растра по рамке растра значение флага принимается во внимание при установленной рамке в растр (flagbordernew)
        
        :param _flagduplicate: флаг создания уменьшенной копии изображения выходного растра (``0``/``1``)
        
        :param _flagbordernew: ``0`` - не устанавливать рамку выходного растра ``1`` - установить рамку выходного растра по теоретическим координатам (например - по объекту Рамка номенклатурного листа карты) ``2`` - установить рамку выходного растра по рамке исходного растра если в исходном растре рамка не установлена, то будет установлена рамка растра по пересчитанным габаритам исходного растра ``3`` - установить рамку выходного растра по пересчитанным габаритам исходного растра
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           то в качестве цвета фона используется цвет из colortransparent
           отображение цвета colortransparent отключается)
        """
        return RswTransformingWithBorderSettingUn_t (_hmap, _handle, _parm, _sourcename.buffer(), _outputname.buffer(), _count, _fact, _teor, _colortransparent, _flagcutting, _flagduplicate, _flagbordernew)

    RswProjectionReformingPro_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'RswProjectionReformingPro', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_long, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def RswProjectionReformingPro(_handle: maptype.HMESSAGE, _sourcename: mapsyst.WTEXT, _outputname: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        """
        Преобразовать растр к заданной проекции
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки
        
        :param _sourcename: имя исходного растра
        
        :param _outputname: имя выходного растра
        
        :param _mapreg: адрес структуры с данными о заданной проекции
        
        :param _datum: параметры пересчета геодезических координат с заданного эллипсоида на эллипсоид ``WGS``-``84`` или ``0``
        
        :param _ellparam: параметры пользовательского эллипсоида или ``0``
        
        :param _ttype: тип локального преобразования координат или ``0``
        
        :param _tparm: параметры локального преобразования координат Структуры ``MAPREGISTEREX``, ``DATUMPARAM``, ``ELLIPSOIDPARAM``, ``LOCALTRANSFORM`` описаны в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return RswProjectionReformingPro_t (_handle, _sourcename.buffer(), _outputname.buffer(), _mapreg, _datum, _ellparam, _ttype, _tparm)

    picexGetLastError_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'picexGetLastError')
    def picexGetLastError() -> int:
        """
        Вернуть код последней ошибки (коды ошибок в maperr.rh)
        
        :returns: В случае отсутствия ошибки возвращает ноль
        :rtype: int
        """
        return picexGetLastError_t ()

    picexSetRstProjectionByPrj_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'picexSetRstProjectionByPrj', maptype.PWCHAR, maptype.PWCHAR)
    def picexSetRstProjectionByPrj(_prjfilename: mapsyst.WTEXT, _rswfilename: mapsyst.WTEXT) -> int:
        """
        Установить параметры проекции растра по файлу PRJ
        
        :param _prjfilename: имя файла ``PRJ``
        
        :param _rswfilename: имя файла RSW
        
        :returns: При ошибке функция возвращает 0
        :rtype: int
        """
        return picexSetRstProjectionByPrj_t (_prjfilename.buffer(), _rswfilename.buffer())

    picexSetRstProjectionFromPrj_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'picexSetRstProjectionFromPrj', maptype.PWCHAR, maptype.PWCHAR)
    def picexSetRstProjectionFromPrj(_graphicfilename: mapsyst.WTEXT, _rswfilename: mapsyst.WTEXT) -> int:
        """
        Установить параметры проекции растра из PRJ-файла по имени графического файла
        
        :param _graphicfilename: имя графического файла, рядом с которым находится ``PRJ``-файл имена графического и ``PRJ`` - файлов соответствуют
        
        :param _rswfilename: имя файла RSW
        
        :returns: При ошибке функция возвращает 0
        :rtype: int
        """
        return picexSetRstProjectionFromPrj_t (_graphicfilename.buffer(), _rswfilename.buffer())

    picexIsRasterGeoSupported_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'picexIsRasterGeoSupported', maptype.PWCHAR, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def picexIsRasterGeoSupported(_rswfilename: mapsyst.WTEXT, _isgeosupported: ctypes.POINTER(ctypes.c_long), _islocation: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить наличие привязки в растре и поддержку пересчета к геодезическим координатам
        
        :param _rswfilename: имя файла растра
        
        :param _isgeosupported: флаг поддержки пересчета к геодезическим координатам из плоских прямоугольных и обратно
        
        :param _islocation: флаг наличия привязки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return picexIsRasterGeoSupported_t (_rswfilename.buffer(), _isgeosupported, _islocation)

    picexUpdateRasterDuplicates_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'picexUpdateRasterDuplicates', maptype.HMESSAGE, maptype.PWCHAR)
    def picexUpdateRasterDuplicates(_handle: maptype.HMESSAGE, _rswfilename: mapsyst.WTEXT) -> int:
        """
        Обновить пирамиду обзорных изображений растра
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки или ноль
        
        :param _rswfilename: имя файла растра
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return picexUpdateRasterDuplicates_t (_handle, _rswfilename.buffer())

    picexRasterCompressPro_t = mapsyst.GetProcAddress(picexlib,ctypes.c_long,'picexRasterCompressPro', maptype.HMESSAGE, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def picexRasterCompressPro(_handle: maptype.HMESSAGE, _rswfilename: mapsyst.WTEXT, _compressmethod: int, _compressvalue: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Выполнить сжатие растра
        
        :param _handle: идентификатор окна диалога визуального сопровождения процесса обработки или ноль
        
        :param _rswfilename: имя файла растра
        
        :param _compressmethod: метод сжатия (``RMF_COMPR_LZW``, ``RMF_COMPR_JPEG``)
        
        :param _compressvalue: степень сжатия изображения по алгоритму ``JPEG``: возможные значения: ``10`` - ``100`` рекомендуемое значение: ``60``
        
        :param _callevent: адрес функции обратного вызова для уведомления о проценте обработанных наборов данных (maptype.h)
        
        :param _parm: адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы) вторым параметром в вызываемой функции передается процент от ``0`` до ``100``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return picexRasterCompressPro_t (_handle, _rswfilename.buffer(), _compressmethod, _compressvalue, _callevent, _parm)



def mappicex_healthcheck():
    return 1
