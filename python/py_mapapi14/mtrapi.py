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
    *               Описание функций по работе с матрицами             *
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
class CALC_ABSOLUTE_HEIGHT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("MethodMTW",ctypes.c_char),
                ("MethodMTL",ctypes.c_char),
                ("MethodMTD",ctypes.c_char),
                ("MethodTIN",ctypes.c_char),
                ("FilterMTD",ctypes.c_char),
                ("Reserve",ctypes.c_char*(51)),
                ("RadiusMTD",ctypes.c_double)]
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
    mapOpenMtrUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapOpenMtrUn', maptype.PWCHAR, ctypes.c_long)
    def mapOpenMtrUn(_mtrname: mapsyst.WTEXT, _mode: int) -> maptype.HMAP:
        """
        Открыть матричные данные
        
        :param _mtrname: имя открываемого файла
        
        :param _mode: режим чтения/записи (``GENERIC_READ``, ``GENERIC_WRITE`` или ``0``) ``GENERIC_READ`` - все данные только на чтение
        
        :returns: Возвращает идентификатор открытой матричной карты При ошибке возвращает ноль
        :rtype: maptype.HMAP
        """
        return mapOpenMtrUn_t (_mtrname.buffer(), _mode)

    mapOpenMtrForMapUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapOpenMtrForMapUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapOpenMtrForMapUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _mode: int) -> int:
        """
        Открыть матричные данные в заданном районе работ (добавляет набор в цепочку матриц)
        
        :param _hmap: идентификатор открытых данных mtrname - имя открываемого файла
        
        :param _mode: режим чтения/записи (``GENERIC_READ``, ``GENERIC_WRITE`` или ``0``) ``GENERIC_READ`` - все данные только на чтение
        
        :returns: Возвращает номер файла в цепочке матриц При ошибке возвращает ноль
        :rtype: int
        """
        return mapOpenMtrForMapUn_t (_hmap, _name.buffer(), _mode)

    mapCloseMtr_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseMtr', maptype.HMAP, ctypes.c_long)
    def mapCloseMtr(_hmap: maptype.HMAP, _number: int) -> ctypes.c_void_p:
        """
        Закрыть матричные данные (убирает набор из цепочки открытых матриц)
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц если number ``= 0``, закрываются все матрицы в окне Чтобы освободить все ресурсы - нужно вызвать mapCloseData(hmap)
        """
        return mapCloseMtr_t (_hmap, _number)

    mapCloseMtrForMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCloseMtrForMap', maptype.HMAP, ctypes.c_long)
    def mapCloseMtrForMap(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Закрыть матричные данные в заданном районе работ
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц если number ``= 0``, закрываются все матричные данные
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCloseMtrForMap_t (_hmap, _number)

    mapSetMtrMultiThreadFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrMultiThreadFlag', ctypes.c_long)
    def mapSetMtrMultiThreadFlag(_flag: int) -> int:
        """
        Установить признак обработки матриц в потоках
        
        :param _flag: признак обработки матрицы в потоках (``0`` / ``1``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если признак установлен, то при повторном открытии матрицы создается новый класс доступа
           со своим буфером чтения/записи матрицы. Это наиболее быстрый способ работы в потоках за счет дополнительной памяти
           Если нет, то доступ осуществляется через общий класс для всех идентификаторов одной матрицы в приложении
           Многопоточность будет также поддерживаться за счет локировок класса и вспомогательного класса HPAINT
        """
        return mapSetMtrMultiThreadFlag_t (_flag)

    mapGetMtrSystemTime_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrSystemTime', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.SYSTEMTIME))
    def mapGetMtrSystemTime(_hmap: maptype.HMAP, _number: int, _time: ctypes.POINTER(maptype.SYSTEMTIME)) -> int:
        """
        Запросить время крайнего редактирования матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _time: системное время редактирования
        
        :returns: Возвращает системное время редактирования (создания) по Гринвичу При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrSystemTime_t (_hmap, _number, _time)

    mapBuildMtwUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBuildMtwUn', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(maptype.BUILDMTW), maptype.HWND)
    def mapBuildMtwUn(_hmap: maptype.HMAP, _mtrname: mapsyst.WTEXT, _filtername: mapsyst.WTEXT, _mtrparm: ctypes.POINTER(maptype.BUILDMTW), _handle: maptype.HWND) -> int:
        """
        Построить матрицу по векторной карте на заданный участок района работ
        
        :param _hmap: исходная карта для построения матрицы
        
        :param _mtrname: полное имя создаваемой матрицы
        
        :param _filtername: полное имя фильтра объектов Вместе с картой может располагаться фильтр объектов - текстовый файл mtrcrea.imh, содержащий перечень кодов объектов, используемых при построении матрицы
        
        :param _mtrparm: параметры создаваемой матрицы
        
        :param _handle: идентификатор окна диалога, которому посылаются сообщения о ходе процесса: ``0x0581`` - сообщение о проценте выполненных работ (в ``WPARAM``) если процесс должен быть принудительно завершен, в ответ должно вернуться значение ``0x0581`` если handle равно нулю - сообщения не посылаются Параметр ``LPARAM`` (не равный ``0``) сообщения о ходе процесса содержит номер этапа построения матрицы: ``1`` - Заполнение матрицы абсолютными высотами объектов ``2`` - Обработка объектов гидрографии с постоянной высотой ``3`` - Обработка объектов гидрографии с переменной высотой ``4`` - Обработка точечных объектов с абсолютной высотой ``5`` - Определение минимальной и максимальной высоты ``6`` - Вычисление незаполненных элементов матрицы ``9`` - Заполнение матрицы относительными высотами объектов ``10`` - Создание матрицы выполнено ``11`` - Создание матрицы не выполнено ``13`` - Обработка пустых замкнутых горизонталей ``14`` - Вычисление элементов матрицы по сетке высотных точек ``15`` - Построение сетки треугольников по высотным точкам ``16`` - Сжатие матрицы ``17`` - Вычисление высот по трехмерной метрике площадных объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если filtername равно нулю - фильтр объектов не используется
        """
        return mapBuildMtwUn_t (_hmap, _mtrname.buffer(), _filtername.buffer(), _mtrparm, _handle)

    mapBuildMtwDepth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBuildMtwDepth', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.POINTER(maptype.BUILDMTW), maptype.HMESSAGE, ctypes.POINTER(ctypes.c_long))
    def mapBuildMtwDepth(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _mtrname: mapsyst.WTEXT, _mtrparm: ctypes.POINTER(maptype.BUILDMTW), _handle: maptype.HMESSAGE, _errorcode: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Построить матрицу глубин по морской карте, созданной по классификатору с именем s57navy.rsc
        
        :param _hmap: идентификатор открытой карты
        
        :param _hsite: идентификатор открытой пользовательской карты
        
        :param _mtrname: полное имя создаваемой матрицы
        
        :param _mtrparm: параметры создаваемой матрицы
        
        :param _handle: идентификатор окна диалога, которому посылаются сообщения о ходе процесса: ``0x0589`` - сообщение о проценте выполненных работ (в ``WPARAM``), если процесс должен быть принудительно завершен, в ответ должно вернуться значение ``0x0589``
        
        :param _errorcode: код ошибки: ``IDS_PARM`` - ошибка входных параметров функции ``IDS_NOMAP`` - нет открытых векторных карт ``IDS_MEMORY`` - ошибка выделения памяти ``IDS_RSCOPEN`` - ошибка открытия файла ``RSC`` ``IDS_LOADLIBRARY`` - ошибка загрузки библиотеки ``IDS_CREATE`` - ошибка создания файла ``7300`` - нет открытых морских карт Объекты для построения матрицы глубин: изобата (ключ ``DEPCNT_L``), отметка глубины (ключ ``SOUNDG_P``), область суши (``LNDARE_S``), затонувшее судно (``WRECKS_P1``), опасность (``OBSTRN_S1``), подводная осыхающая скала (``UWTROC_P``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapBuildMtwDepth_t (_hmap, _hsite, _mtrname.buffer(), _mtrparm, _handle, _errorcode)

    mapBuildRswUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBuildRswUn', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(maptype.BUILDMTW), maptype.HWND)
    def mapBuildRswUn(_hmap: maptype.HMAP, _rstname: mapsyst.WTEXT, _filtername: mapsyst.WTEXT, _mtrparm: ctypes.POINTER(maptype.BUILDMTW), _handle: maptype.HWND) -> int:
        """
        Построить растр качеств по векторной карте на заданный участок района работ
        
        :param _hmap: исходная карта для построения растра
        
        :param _rstname: полное имя создаваемого растра
        
        :param _filtername: полное имя служебного текстового файла вместе с картой должен располагаться фильтр объектов - служебный текстовый файл mаp2rsw.ini, содержащий перечень кодов объектов, используемых при построении растра
        
        :param _mtrparm: параметры создаваемого растра,
        
        :param _handle: идентификатор окна диалога, которому посылаются сообщения о ходе процесса: ``0x0581`` - сообщение о проценте выполненных работ (в ``WPARAM``) если процесс должен быть принудительно завершен, в ответ должно вернуться значение ``0x0581`` если handle равно нулю - сообщения не посылаются
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapBuildRswUn_t (_hmap, _rstname.buffer(), _filtername.buffer(), _mtrparm, _handle)

    mapClearMtrCache_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapClearMtrCache', maptype.HMAP, ctypes.c_long)
    def mapClearMtrCache(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Очистить кэш матричных данных, открытых на ГИС Сервере
        
        :param _hmap: идентификатор открытой векторной карты
        
        :param _number: номер матрицы, для которой нужно очистить кэш, или -``1`` (все матрицы)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapClearMtrCache_t (_hmap, _number)

    mapGetMtrDescribeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrDescribeUn', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.MTRDESCRIBEUN))
    def mapGetMtrDescribeUn(_hmap: maptype.HMAP, _number: int, _describe: ctypes.POINTER(maptype.MTRDESCRIBEUN)) -> int:
        """
        Запросить описание файла матричных данных
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _describe: адрес структуры, в которой будет размещено описание матрицы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrDescribeUn_t (_hmap, _number, _describe)

    mapGetMtrColorDescEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrColorDescEx', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.MTRCOLORDESCEX))
    def mapGetMtrColorDescEx(_hmap: maptype.HMAP, _number: int, _colornumber: int, _colordesc: ctypes.POINTER(maptype.MTRCOLORDESCEX)) -> int:
        """
        Запросить описание диапазона высот матрицы с номером
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _colornumber: номер диапазона высот
        
        :param _colordesc: адрес структуры, в которой будет размещено описание диапазона высот
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrColorDescEx_t (_hmap, _number, _colornumber, _colordesc)

    mapGetMtrNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrNameUn', maptype.HMAP, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetMtrNameUn(_hmap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить имя файла матричных данных
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _name: адрес строки для размещения результата
        
        :param _size: размер строки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrNameUn_t (_hmap, _number, _name.buffer(), _size)

    mapGetMtrCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrCount', maptype.HMAP)
    def mapGetMtrCount(_hmap: maptype.HMAP) -> int:
        """
        Запросить число открытых файлов матричных данных
        
        :param _hmap: идентификатор открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrCount_t (_hmap)

    mapGetMtwCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtwCount', maptype.HMAP, ctypes.c_long)
    def mapGetMtwCount(_hmap: maptype.HMAP, _userlabel: int) -> int:
        """
        Запросить число открытых файлов матричных данных
        
        :param _hmap: идентификатор открытых данных
        
        :param _userlabel: метка файла MTW: ``0`` - выполняется запрос для матриц высот ``LABEL_MTW_DEPTH`` - выполняется запрос для матриц глубин ``LABEL_MTW_EGM`` - выполняется запрос для матриц поправок высот геоида
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtwCount_t (_hmap, _userlabel)

    mapGetMtrNumberByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrNumberByNameUn', maptype.HMAP, maptype.PWCHAR)
    def mapGetMtrNumberByNameUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT) -> int:
        """
        Запросить номер матрицы в цепочке по имени файла
        
        :param _hmap: идентификатор открытых данных
        
        :param _name: имя файла матрицы В цепочке номера матриц начинаются с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrNumberByNameUn_t (_hmap, _name.buffer())

    mapGetActualMtrFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetActualMtrFrame', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.c_long)
    def mapGetActualMtrFrame(_hmap: maptype.HMAP, _frame: ctypes.POINTER(maptype.DFRAME), _number: int) -> int:
        """
        Запросить фактические габариты матрицы в метрах в системе координат документа
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _frame: адрес структуры, в которой будут размещены габариты матрицы в метрах При отображении матрицы по рамке возвращаются габариты рамки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetActualMtrFrame_t (_hmap, _frame, _number)

    mapGetMtrLocation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrLocation', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetMtrLocation(_hmap: maptype.HMAP, _number: int, _location: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Запросить привязку матрицы в метрах в районе работ
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _location: координаты юго-западного угла матрицы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrLocation_t (_hmap, _number, _location)

    mapSetMtrLocation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrLocation', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSetMtrLocation(_hmap: maptype.HMAP, _number: int, _location: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Установить привязку матрицы в метрах в районе работ
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _location: координаты юго-западного угла матрицы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtrLocation_t (_hmap, _number, _location)

    mapGetTotalMinHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetTotalMinHeight', maptype.HMAP)
    def mapGetTotalMinHeight(_hmap: maptype.HMAP) -> float:
        """
        Запросить минимальное значение высот всех матриц в метрах
        
        :param _hmap: идентификатор открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapGetTotalMinHeight_t (_hmap)

    mapGetTotalMaxHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetTotalMaxHeight', maptype.HMAP)
    def mapGetTotalMaxHeight(_hmap: maptype.HMAP) -> float:
        """
        Запросить максимальное значение высот всех матриц в метрах
        
        :param _hmap: идентификатор открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapGetTotalMaxHeight_t (_hmap)

    mapHeightValuePresence_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapHeightValuePresence', maptype.HMAP, ctypes.POINTER(maptype.DFRAME))
    def mapHeightValuePresence(_hmap: maptype.HMAP, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Запросить наличие высот рельефа на заданном участке
        
        :param _hmap: идентификатор открытой основной векторной карты
        
        :param _frame: адрес структуры, содержащей габариты заданного участка в метрах
        
        :returns: При наличии высот рельефа возвращает 1, при отсутствии возвращает 0
        :rtype: int
        
        .. note::

           Если frame равно нулю, то заданный участок определяется габаритами карты
        """
        return mapHeightValuePresence_t (_hmap, _frame)

    mapGetHeightValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetHeightValue', maptype.HMAP, ctypes.c_double, ctypes.c_double)
    def mapGetHeightValue(_hmap: maptype.HMAP, _x: float, _y: float) -> float:
        """
        Выбрать значение абсолютной высоты в заданной точке
        
        :param _hmap: идентификатор открытой основной векторной карты
        
        :param _x: координата Х точки в метрах в системе координат векторной карты
        
        :param _y: координата Y точки в метрах в системе координат векторной карты
        
        :returns: Возвращает значение высоты в метрах В случае ошибки при выборе высоты и в случае необеспеченности заданной точки матричными данными возвращает ERRORHEIGHT (``-111111.0``)
        :rtype: float
        """
        return mapGetHeightValue_t (_hmap, _x, _y)

    mapGetHeightValueOfMtrControl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetHeightValueOfMtrControl', maptype.HMAP, ctypes.c_long, ctypes.c_double, ctypes.c_double, maptype.HPAINT)
    def mapGetHeightValueOfMtrControl(_hmap: maptype.HMAP, _number: int, _x: float, _y: float, _hpaint: maptype.HPAINT) -> float:
        """
        Выбрать значение абсолютной высоты в заданной точке из матрицы с номером number в цепочке
        
        :param _hmap: идентификатор открытой основной векторной карты
        
        :param _number: номер матрицы в цепочке
        
        :param _hpaint: контекст поддержки многопоточного вызова (mapCreatePaintControl)
        
        :param _x: координата Х точки в метрах в системе координат векторной карты
        
        :param _y: координата Y точки в метрах в системе координат векторной карты
        
        :returns: Возвращает значение высоты в метрах В случае ошибки при выборе высоты и в случае необеспеченности заданной точки матричными данными возвращает ERRORHEIGHT (``-111111.0``)
        :rtype: float
        """
        return mapGetHeightValueOfMtrControl_t (_hmap, _number, _x, _y, _hpaint)

    mapGetHeightValueOfMtrEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetHeightValueOfMtrEx', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double))
    def mapGetHeightValueOfMtrEx(_hmap: maptype.HMAP, _number: int, _interptype: int, _x: float, _y: float, _h: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Вернуть интерполированную высоту в заданной точке
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _interptype: тип интерполяции ``1`` - ближайший сосед ``2`` - интерполяция по ближайшим ``3`` элементам ``3`` - билинейная интерполяция по ``4`` ближайшим элементам ``4`` - бикубическая интерполяция по ``16`` ближайшим элементам
        
        :param _x: координата Х точки в метрах
        
        :param _y: координата Y точки в метрах
        
        :param _h: возвращаемое значение в метрах, при ошибке устанавливается ``ERRORHEIGHT`` (``-111111.0``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetHeightValueOfMtrEx_t (_hmap, _number, _interptype, _x, _y, _h)

    mapGetMtrPointEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrPointEx', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_double), ctypes.c_long, ctypes.c_long, maptype.HPAINT)
    def mapGetMtrPointEx(_hmap: maptype.HMAP, _number: int, _value: ctypes.POINTER(ctypes.c_double), _row: int, _column: int, _hpaint: maptype.HPAINT) -> int:
        """
        Прочитать элемент матрицы высот по абсолютным индексам
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _value: полученное значение элемента в метрах (при отсутствии высоты равно ``ERRORHEIGHT``)
        
        :param _row: индекс строки матрицы (значение от ``0`` до height``-1``, где height - высота матрицы элементах, запрашиваемая функцией mapGetMtrHeightInElement)
        
        :param _column: индекс колонки матрицы (значение от ``0`` до width``-1``, где width - ширина матрицы элементах, запрашиваемая функцией mapGetMtrWidthInElement)
        
        :param _hpaint: контекст поддержки многопоточного вызова (mapCreatePaintControl) или ``0``
        
        :returns: При ошибке и при отсутствии высоты возвращает ноль
        :rtype: int
        """
        return mapGetMtrPointEx_t (_hmap, _number, _value, _row, _column, _hpaint)

    mapGetMtrMeterInElementX_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrMeterInElementX', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def mapGetMtrMeterInElementX(_hmap: maptype.HMAP, _number: int, _metinelemX: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить размер элемента матрицы в метрах по оси X
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _metinelemX: размер элемента матрицы в метрах на местности по оси X
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrMeterInElementX_t (_hmap, _number, _metinelemX)

    mapGetMtrMeterInElementY_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrMeterInElementY', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def mapGetMtrMeterInElementY(_hmap: maptype.HMAP, _number: int, _metinelemY: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить размер элемента матрицы в метрах по оси Y
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _metinelemY: размер элемента матрицы в метрах на местности по оси Y
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrMeterInElementY_t (_hmap, _number, _metinelemY)

    mapPutHeightValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPutHeightValue', maptype.HMAP, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    def mapPutHeightValue(_hmap: maptype.HMAP, _number: int, _x: float, _y: float, _h: float) -> int:
        """
        Занести значение абсолютной высоты в элемент матрицы, соответствующий заданной точке
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _x: координата Х точки в метрах в системе координат документа
        
        :param _y: координата Y точки в метрах в системе координат документа
        
        :param _h: значение высоты в метрах в системе координат документа
        
        :returns: В случае ошибки возвращает ноль
        :rtype: int
        """
        return mapPutHeightValue_t (_hmap, _number, _x, _y, _h)

    mapPutMtrPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPutMtrPoint', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_double)
    def mapPutMtrPoint(_hmap: maptype.HMAP, _number: int, _x: int, _y: int, _h: float) -> int:
        """
        Занести значение абсолютной высоты в элемент матрицы, соответствующий заданной точке
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _x: номер строки элементов в матрице
        
        :param _y: номер колонки элементов в матрице
        
        :param _h: значение высоты в метрах
        
        :returns: В случае ошибки возвращает ноль
        :rtype: int
        """
        return mapPutMtrPoint_t (_hmap, _number, _x, _y, _h)

    mapGetAbsoluteHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetAbsoluteHeight', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.POINTER(CALC_ABSOLUTE_HEIGHT), maptype.HPAINT)
    def mapGetAbsoluteHeight(_hmap: maptype.HMAP, _x: float, _y: float, _parm: ctypes.POINTER(CALC_ABSOLUTE_HEIGHT), _hpaint: maptype.HPAINT) -> float:
        """
        Вычислить абсолютную высоту в заданной точке по открытым данным, содержащим модели рельефа
        
        :param _hmap: идентификатор открытых данных
        
        :param _x: координата Х точки в метрах в системе координат документа
        
        :param _y: координата Y точки в метрах в системе координат документа
        
        :param _parm: параметры вычисления высоты (структура ``CALC_ABSOLUTE_HEIGHT``) Последовательность использования моделей рельефа: MTW, ``MTL``, ``MTD``, ``TIN`` Переход к использованию очередной модели рельефа выполняется в случае ошибки при вычислении высоты и в случае необеспеченности заданной точки данными модели. Использование модели рельефа можно отключить, задавая в структуре ``CALC_ABSOLUTE_HEIGHT`` метод вычисления высоты ``= -1``
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций, создается функцией mapCreatePaintControl, освобождается - mapFreePaintControl Модели рельефа: матрица высот MTW, матрица слоев ``MTL``, облако точек ``MTD``, триангуляционная нерегулярная сеть ``TIN``
        
        :returns: Возвращает значение высоты в метрах В случае ошибки при выборе высоты и в случае необеспеченности заданной точки данными моделей рельефа возвращает ERRORHEIGHT (``-111111.0``)
        :rtype: float
        
        .. note::

           Если parm ``= 0``, то считается, что задана структура CALC_ABSOLUTE_HEIGHT, содержащая элементы равные 0
        """
        return mapGetAbsoluteHeight_t (_hmap, _x, _y, _parm, _hpaint)

    mapGetPrecisionHeightValueEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetPrecisionHeightValueEx', maptype.HMAP, ctypes.c_double, ctypes.c_double, maptype.HPAINT)
    def mapGetPrecisionHeightValueEx(_hmap: maptype.HMAP, _x: float, _y: float, _hpaint: maptype.HPAINT) -> float:
        """
        Выбрать значение абсолютной высоты в заданной точке из матрицы с наименьшим размером элемента (более точной)
        
        :param _hmap: идентификатор открытой основной векторной карты
        
        :param _x: координата Х точки в метрах в системе координат документа
        
        :param _y: координата Y точки в метрах в системе координат документа
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций, создается функцией mapCreatePaintControl, освобождается - mapFreePaintControl
        
        :returns: Возвращает значение высоты в метрах В случае ошибки при выборе высоты и в случае необеспеченности заданной точки матричными данными возвращает ERRORHEIGHT (``-111111.0``)
        :rtype: float
        """
        return mapGetPrecisionHeightValueEx_t (_hmap, _x, _y, _hpaint)

    mapGetPrecisionHeightTriangleEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetPrecisionHeightTriangleEx', maptype.HMAP, ctypes.c_double, ctypes.c_double, maptype.HPAINT)
    def mapGetPrecisionHeightTriangleEx(_hmap: maptype.HMAP, _x: float, _y: float, _hpaint: maptype.HPAINT) -> float:
        """
        Рассчитать абсолютную высоту методом треугольников в заданной точке по матрице с наименьшим размером элемента
        
        :param _hmap: идентификатор открытой основной векторной карты
        
        :param _x: координата Х точки в метрах в системе координат документа
        
        :param _y: координата Y точки в метрах в системе координат документа
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций, создается функцией mapCreatePaintControl, освобождается - mapFreePaintControl В матрицах обрабатываются нормальные высоты Высота вычисляется по самой точной матрице высот,а в случае необеспеченности заданной точки данными матриц высот - по самой точной матрице слоев
        
        :returns: Возвращает значение высоты в метрах В случае ошибки при выборе высоты и в случае необеспеченности заданной точки матричными данными возвращает ERRORHEIGHT (``-111111.0``)
        :rtype: float
        """
        return mapGetPrecisionHeightTriangleEx_t (_hmap, _x, _y, _hpaint)

    mapGetHeightTriangleOfMtr_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetHeightTriangleOfMtr', maptype.HMAP, ctypes.c_long, ctypes.c_double, ctypes.c_double)
    def mapGetHeightTriangleOfMtr(_hmap: maptype.HMAP, _number: int, _x: float, _y: float) -> float:
        """
        Рассчитать абсолютную высоту методом треугольников в заданной точке по матрице с номером number
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _x: координата Х точки в метрах в системе координат документа
        
        :param _y: координата Y точки в метрах в системе координат документа
        
        :returns: Возвращает значение высоты в метрах В случае ошибки при выборе высоты и в случае необеспеченности заданной точки матричными данными возвращает ERRORHEIGHT (``-111111.0``)
        :rtype: float
        """
        return mapGetHeightTriangleOfMtr_t (_hmap, _number, _x, _y)

    mapGetGeneralHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetGeneralHeight', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    def mapGetGeneralHeight(_hmap: maptype.HMAP, _xcenter: float, _ycenter: float, _size: float) -> float:
        """
        Рассчитать среднее значение абсолютной высоты по высотам квадратной области
        
        :param _hmap: идентификатор открытых данных
        
        :param _xcenter: координата Х центра области в метрах в системе координат документа
        
        :param _ycenter: координата Y центра области в метрах в системе координат документа
        
        :param _size: размер стороны области в метрах (размер элемента матрицы обобщенного рельефа) Функция может использоваться для создания матрицы обобщенного рельефа
        
        :returns: Возвращает среднее значение высоты в метрах в системе координат документа В случае ошибки при выборе высот и в случае необеспеченности заданной области матричными данными возвращает ERRORHEIGHT (``-111111.0``)
        :rtype: float
        """
        return mapGetGeneralHeight_t (_hmap, _xcenter, _ycenter, _size)

    mapGetGeneralHeightOfMtr_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetGeneralHeightOfMtr', maptype.HMAP, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    def mapGetGeneralHeightOfMtr(_hmap: maptype.HMAP, _number: int, _xcenter: float, _ycenter: float, _size: float) -> float:
        """
        Рассчитать среднее значение абсолютной высоты по высотам квадратной области матрицы с номером number
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _xcenter: координата Х центра области в метрах в системе координат документа
        
        :param _ycenter: координата Y центра области в метрах в системе координат документа
        
        :param _size: размер стороны области в метрах (размер элемента матрицы обобщенного рельефа) Функция может использоваться для создания матрицы обобщенного рельефа
        
        :returns: Возвращает среднее значение высоты в метрах В случае ошибки при выборе высот и в случае необеспеченности заданной области матричными данными возвращает ERRORHEIGHT (``-111111.0``)
        :rtype: float
        """
        return mapGetGeneralHeightOfMtr_t (_hmap, _number, _xcenter, _ycenter, _size)

    mapGetMtrNumberInPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrNumberInPoint', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapGetMtrNumberInPoint(_hmap: maptype.HMAP, _x: float, _y: float, _number: int) -> int:
        """
        Запросить номер в цепочке для матрицы, расположенной в заданной точке
        
        :param _hmap: идентификатор открытых данных
        
        :param _x: координата Х точки в метрах в системе координат документа
        
        :param _y: координата Y точки в метрах в системе координат документа
        
        :param _number: порядковый номер, найденной матрицы в точке (``1`` - первая в данной точке, ``2`` - вторая ...)
        
        :returns: При ошибке возвращается ноль, иначе - порядковый номер открытой матрицы в цепочке с 1
        :rtype: int
        """
        return mapGetMtrNumberInPoint_t (_hmap, _x, _y, _number)

    mapGetPrecisionHeightFrameAndPoints_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetPrecisionHeightFrameAndPoints', maptype.HMAP, ctypes.POINTER(ctypes.c_int), ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.DFRAME), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), maptype.HPAINT)
    def mapGetPrecisionHeightFrameAndPoints(_hmap: maptype.HMAP, _matrix: ctypes.POINTER(ctypes.c_int), _width: int, _hight: int, _unit: int, _dframe: ctypes.POINTER(maptype.DFRAME), _minvalue: ctypes.POINTER(ctypes.c_long), _maxvalue: ctypes.POINTER(ctypes.c_long), _minPoint: ctypes.POINTER(maptype.DOUBLEPOINT), _maxPoint: ctypes.POINTER(maptype.DOUBLEPOINT), _hpaint: maptype.HPAINT) -> int:
        """
        Вычислить значения массива элементов с применением метода треугольников по матрицам высот
        
        :param _hmap: идентификатор документа, содержащего открытые матрицы высот (MTW)
        
        :param _matrix: указатель на буфер выходной матрицы ``4``-ех байтовых целочисленных элементов
        
        :param _width: ширина выходной матрицы (число элементов в строке)
        
        :param _hight: высота выходной матрицы (число строк)
        
        :param _unit: единица измерения высоты в матрице (``0`` - метры, ``1`` - дециметры, ``2`` - сантиметры, ``3`` - миллиметры)
        
        :param _dframe: габариты матрицы на местности в системе координат документа от юго-западного элемента матрицы до северо-восточного
        
        :param _minvalue: поле для записи минимального значения элемента в выходной матрице
        
        :param _maxvalue: поле для записи максимального значения элемента в выходной матрице
        
        :param _minPoint: поле для записи координат в системе координат документа точки минимума
        
        :param _maxPoint: поле для записи координат в системе координат документа точки максимума
        
        :param _hpaint: контекст поддержки многопоточного вызова (mapCreatePaintControl) Применяется для обработки ``OGC`` ``WCS``-запросов
        
        :returns: При ошибке возвращает ноль, если область полностью обеспечена данными возвращает 1, если данных недостаточно возвращает отррицательное количество незаполненных элементов области
        :rtype: int
        """
        return mapGetPrecisionHeightFrameAndPoints_t (_hmap, _matrix, _width, _hight, _unit, _dframe, _minvalue, _maxvalue, _minPoint, _maxPoint, _hpaint)

    mapGetHeightArrayEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetHeightArrayEx', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), maptype.HPAINT)
    def mapGetHeightArrayEx(_hmap: maptype.HMAP, _heightarray: ctypes.POINTER(ctypes.c_double), _count: int, _first: ctypes.POINTER(maptype.DOUBLEPOINT), _second: ctypes.POINTER(maptype.DOUBLEPOINT), _hpaint: maptype.HPAINT) -> int:
        """
        Выбрать массив значений абсолютных высот, соответствующих логическим элементам, лежащим на заданном отрезке
        
        :param _hmap: идентификатор открытой основной векторной карты
        
        :param _heightarray: адрес массива высот
        
        :param _count: количество высот
        
        :param _first: координаты точки, задающей начало отрезка, в метрах в системе координат документа
        
        :param _second: координаты точки, задающей конец отрезка, в метрах в системе координат документа
        
        :param _hpaint: контекст поддержки многопоточного вызова (mapCreatePaintControl) Размер массива высот, заданного адресом heightarray, должен соответствовать запрашиваемому количеству высот (count), в противном случае возможны ошибки работы с памятью Расчет абсолютной высоты в каждой промежуточной точке выполняется методом треугольников по матрице с наименьшим размером элемента (более точной) В случае необеспеченности логического элемента матричными данными его значение равно ``ERRORHEIGHT`` (``-111111.0``)
        
        :returns: В случае ошибки при выборе высот возвращает ноль
        :rtype: int
        """
        return mapGetHeightArrayEx_t (_hmap, _heightarray, _count, _first, _second, _hpaint)

    mapGetMtrBlockSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrBlockSize', maptype.HMAP, ctypes.c_long)
    def mapGetMtrBlockSize(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить размер полного блока матрицы в байтах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrBlockSize_t (_hmap, _number)

    mapGetMtrElementSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrElementSize', maptype.HMAP, ctypes.c_long)
    def mapGetMtrElementSize(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить размер (тип) элемента матрицы в байтах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц Возвращаемое значение ``1`` соответствует типу ``"unsigned char"`` Возвращаемое значение ``2`` соответствует типу ``"short int"`` Возвращаемое значение ``4`` соответствует типу ``"int"`` Возвращаемое значение ``8`` соответствует типу ``"double"``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrElementSize_t (_hmap, _number)

    mapGetMtrBlockSide_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrBlockSide', maptype.HMAP, ctypes.c_long)
    def mapGetMtrBlockSide(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить вертикальный размер блока матрицы в элементах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrBlockSide_t (_hmap, _number)

    mapGetMtrBlockWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrBlockWidth', maptype.HMAP, ctypes.c_long)
    def mapGetMtrBlockWidth(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить горизонтальный размер блока матрицы в элементах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrBlockWidth_t (_hmap, _number)

    mapGetMtrCurrentBlockWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrCurrentBlockWidth', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapGetMtrCurrentBlockWidth(_hmap: maptype.HMAP, _number: int, _column: int) -> int:
        """
        Запросить ширину текущего блока матрицы в элементах (с учетом усеченных блоков)
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrCurrentBlockWidth_t (_hmap, _number, _column)

    mapGetMtrCurrentBlockHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrCurrentBlockHeight', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapGetMtrCurrentBlockHeight(_hmap: maptype.HMAP, _number: int, _row: int) -> int:
        """
        Запросить высоту текущего блока матрицы в элементах (с учетом усеченных блоков)
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _row: строка блока
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrCurrentBlockHeight_t (_hmap, _number, _row)

    mapGetMtrCurrentBlockSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrCurrentBlockSize', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapGetMtrCurrentBlockSize(_hmap: maptype.HMAP, _number: int, _row: int, _column: int) -> int:
        """
        Запросить размер текущего блока матрицы в байтах (с учетом усеченных блоков)
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _row: строка блока
        
        :param _column: столбец блока
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrCurrentBlockSize_t (_hmap, _number, _row, _column)

    mapGetMtrBlockAndCreate_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetMtrBlockAndCreate', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapGetMtrBlockAndCreate(_hmap: maptype.HMAP, _number: int, _row: int, _column: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить адрес блока матрицы по номеру строки и столбца
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _row: строка блока
        
        :param _column: столбец блока При отсутствии в файле - создается При запросе следующего блока может вернуть прежний адрес
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetMtrBlockAndCreate_t (_hmap, _number, _row, _column)

    mapWriteMtrBlock_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapWriteMtrBlock', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_char_p, ctypes.c_long)
    def mapWriteMtrBlock(_hmap: maptype.HMAP, _number: int, _row: int, _column: int, _bits: ctypes.c_char_p, _sizebits: int) -> int:
        """
        Записать блок (row, column) в файл матрицы из памяти bits
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _row: строка блока
        
        :param _column: столбец блока
        
        :param _bits: указатель на начало изображения битовой области
        
        :param _sizebits: размер области bits в байтах
        
        :returns: Возвращает количество записанных байт При ошибке возвращает ноль
        :rtype: int
        """
        return mapWriteMtrBlock_t (_hmap, _number, _row, _column, _bits, _sizebits)

    mapCheckMtrBlockVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckMtrBlockVisible', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapCheckMtrBlockVisible(_hmap: maptype.HMAP, _number: int, _index: int) -> int:
        """
        Вернуть флаг отображения блока матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _index: порядковый номер (индекс) блока, index = row ``*`` blockColumnCount + col, где: row - индекс строки блоков, blockColumnCount - число столбцов блоков матрицы (функция mapGetMtrBlockColumn) col - индекс столбца блоков
        
        :returns: Возвращает: ``0`` - не отображается, ``1`` - отображается, ``2`` - разделен рамкой При ошибке возвращает ноль
        :rtype: int
        """
        return mapCheckMtrBlockVisible_t (_hmap, _number, _index)

    mapGetMtrBlockRow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrBlockRow', maptype.HMAP, ctypes.c_long)
    def mapGetMtrBlockRow(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить число строк блоков матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrBlockRow_t (_hmap, _number)

    mapGetMtrBlockColumn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrBlockColumn', maptype.HMAP, ctypes.c_long)
    def mapGetMtrBlockColumn(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить число столбцов блоков матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrBlockColumn_t (_hmap, _number)

    mapGetMtrElementRow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrElementRow', maptype.HMAP, ctypes.c_long)
    def mapGetMtrElementRow(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить число строк элементов в матрице
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrElementRow_t (_hmap, _number)

    mapGetMtrElementColumn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrElementColumn', maptype.HMAP, ctypes.c_long)
    def mapGetMtrElementColumn(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить число столбцов элементов в матрице
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrElementColumn_t (_hmap, _number)

    mapGetMtrScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrScale', maptype.HMAP, ctypes.c_long)
    def mapGetMtrScale(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить масштаб матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrScale_t (_hmap, _number)

    mapGetMtrRangeScaleVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrRangeScaleVisible', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapGetMtrRangeScaleVisible(_hmap: maptype.HMAP, _number: int, _bottomscale: ctypes.POINTER(ctypes.c_long), _topscale: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить значения масштаба нижней и верхней границ видимости матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _bottomscale: адрес для записи знаменателя масштаба нижней границы видимости матрицы
        
        :param _topscale: адрес для записи знаменателя масштаба верхней границы видимости матрицы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrRangeScaleVisible_t (_hmap, _number, _bottomscale, _topscale)

    mapSetMtrRangeScaleVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrRangeScaleVisible', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSetMtrRangeScaleVisible(_hmap: maptype.HMAP, _number: int, _bottomscale: int, _topscale: int) -> int:
        """
        Установить значения масштаба нижней и верхней границ видимости матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _bottomscale: знаменатель масштаба нижней границы видимости матрицы
        
        :param _topscale: знаменатель масштаба верхней границы видимости матрицы
        
        :returns: bottomScale <= topScale, иначе возвращает 0 При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtrRangeScaleVisible_t (_hmap, _number, _bottomscale, _topscale)

    mapGetMtrMapType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrMapType', maptype.HMAP, ctypes.c_long)
    def mapGetMtrMapType(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить тип исходной карты
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrMapType_t (_hmap, _number)

    mapGetMtrMeasure_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrMeasure', maptype.HMAP, ctypes.c_long)
    def mapGetMtrMeasure(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить единицу измерения значений высот матрицы с номером number в цепочке
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: Возвращает значение поля Unit структуры параметров создания матрицы BUILDMTW Возвращаемые значения: ``0`` - метры, ``1`` - дециметры, ``2`` - сантиметры, ``3`` - миллиметры При ошибке возвращает -1
        :rtype: int
        """
        return mapGetMtrMeasure_t (_hmap, _number)

    mapIsMtrGeoSupported_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsMtrGeoSupported', maptype.HMAP, ctypes.c_long)
    def mapIsMtrGeoSupported(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить поддерживается ли пересчет к геодезическим координатам из плоских прямоугольных и обратно
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц Выполняется запрос - заполнены ли параметры системы координат матрицы
        
        :returns: Если нет - возвращает ноль
        :rtype: int
        """
        return mapIsMtrGeoSupported_t (_hmap, _number)

    mapGetMtrProjectionDataPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrProjectionDataPro', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapGetMtrProjectionDataPro(_hmap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: ctypes.POINTER(ctypes.c_long), _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        """
        Запросить данные о системе координат (в том числе, проекции матрицы)
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _mapregister: адрес структуры, в которой будут размещены данные о системе координат
        
        :param _datumparam: адрес структуры, в которой будут размещены коэффициенты трансформирования геодезических координат
        
        :param _ellipsoidparam: адрес структуры, в которой будут размещены о параметрах эллипсоида
        
        :param _ttype: тип локального преобразования координат (``TRANSFORMTYPE`` в mapcreat.h) или ``0``
        
        :param _tparm: параметры локального преобразования координат Структуры ``MAPREGISTEREX``, ``DATUMPARAM``, ``ELLIPSOIDPARAM``, ``LOCALTRANSFORM`` описаны в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrProjectionDataPro_t (_hmap, _number, _mapregister, _datumparam, _ellipsoidparam, _ttype, _tparm)

    mapGetMtrProjectionDataByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrProjectionDataByNameUn', maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def mapGetMtrProjectionDataByNameUn(_name: mapsyst.WTEXT, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> int:
        """
        Запросить данные о системе координат матрицы по имени файла
        
        :param _name: имя файла матрицы
        
        :param _mapregister: адрес структуры, в которой будут размещены данные о системе координат Структурa ``MAPREGISTEREX`` описанa в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrProjectionDataByNameUn_t (_name.buffer(), _mapregister)

    mapSetMtrProjectionDataPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrProjectionDataPro', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_long, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapSetMtrProjectionDataPro(_hmap: maptype.HMAP, _number: int, _mapregisterex: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        """
        Установить данные о системе координат матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц mapregister    - адрес структуры, содержащей данные о системе координат
        
        :param _datumparam: адрес структуры, содержащей коэффициенты трансформирования геодезических координат
        
        :param _ellipsoidparam: адрес структуры, содержащей данные о параметрах эллипсоида
        
        :param _ttype: тип локального преобразования координат (``TRANSFORMTYPE`` в mapcreat.h) или ``0``
        
        :param _tparm: параметры локального преобразования координат Структуры ``MAPREGISTEREX``, ``DATUMPARAM``, ``ELLIPSOIDPARAM``, ``LOCALTRANSFORM`` описаны в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtrProjectionDataPro_t (_hmap, _number, _mapregisterex, _datumparam, _ellipsoidparam, _ttype, _tparm)

    mapSaveMtr_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSaveMtr', maptype.HMAP, ctypes.c_long)
    def mapSaveMtr(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Записать изменения матрицы в файл
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSaveMtr_t (_hmap, _number)

    mapGetMtrEllipsoidParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrEllipsoidParam', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapGetMtrEllipsoidParam(_hmap: maptype.HMAP, _number: int, _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        """
        Запросить параметры эллипсоида матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _ellipsoidparam: адрес структуры, в которой будут размещены параметры эллипсоида Структурa ``ELLIPSOIDPARAM`` описанa в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrEllipsoidParam_t (_hmap, _number, _ellipsoidparam)

    mapSetMtrEllipsoidParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrEllipsoidParam', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapSetMtrEllipsoidParam(_hmap: maptype.HMAP, _number: int, _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        """
        Установить параметры эллипсоида матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _ellipsoidparam: адрес структуры, содержащей параметры эллипсоида Структурa ``ELLIPSOIDPARAM`` описанa в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtrEllipsoidParam_t (_hmap, _number, _ellipsoidparam)

    mapGetMtrDatumParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrDatumParam', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapGetMtrDatumParam(_hmap: maptype.HMAP, _number: int, _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        """
        Запросить коэффициенты трансформирования геодезических координат матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _datumparam: адрес структуры, в которой будут размещены коэффициенты трансформирования Структурa ``DATUMPARAM`` описанa в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrDatumParam_t (_hmap, _number, _datumparam)

    mapSetMtrDatumParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrDatumParam', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapSetMtrDatumParam(_hmap: maptype.HMAP, _number: int, _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        """
        Установить коэффициенты трансформирования геодезических координат матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _datumparam: адрес структуры, содержащей коэффициенты трансформирования геодезических координат Структурa ``DATUMPARAM`` описанa в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtrDatumParam_t (_hmap, _number, _datumparam)

    mapCalcAbsoluteHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCalcAbsoluteHeight', maptype.HMAP, ctypes.POINTER(maptype.XYHDOUBLE))
    def mapCalcAbsoluteHeight(_hmap: maptype.HMAP, _point: ctypes.POINTER(maptype.XYHDOUBLE)) -> int:
        """
        Вычислить значение абсолютной высоты в заданной точке методом интерполяции
        
        :param _hmap: идентификатор открытых данных
        
        :param _point: координаты точки в метрах в системе координат документа Значение высоты вычисляется по точкам рельефа местности в виде горизонталей, отметок высот векторной карты Вычисленная высота записывается в поле point->H
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCalcAbsoluteHeight_t (_hmap, _point)

    mapCalcAbsoluteHeightBySectors_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapCalcAbsoluteHeightBySectors', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long)
    def mapCalcAbsoluteHeightBySectors(_hmap: maptype.HMAP, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _sectorcount: int) -> float:
        """
        Вычислить значение абсолютной высоты в заданной точке методом интерполяции
        
        :param _hmap: идентификатор открытых данных
        
        :param _point: координаты точки в метрах в системе координат документа
        
        :param _sectorcount: количество направлений для поиска окружающих высот кратно ``4``: минимальное количество направлений ``= 4``, максимальное ``= 256`` Значение высоты вычисляется по точкам рельефа местности в виде горизонталей, отметок высот векторной карты
        
        :returns: Возвращает значение высоты в метрах В случае ошибки при вычислении высоты возвращает ERRORHEIGHT (``-111111.0``)
        :rtype: float
        """
        return mapCalcAbsoluteHeightBySectors_t (_hmap, _point, _sectorcount)

    mapGetMtrView_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrView', maptype.HMAP, ctypes.c_long)
    def mapGetMtrView(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить степень видимости матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: Возвращает: ``0`` - не виден ``1`` - полная ``2`` - насыщенная ``3`` - полупрозрачная ``4`` - средняя ``5`` - прозрачная
        :rtype: int
        """
        return mapGetMtrView_t (_hmap, _number)

    mapSetMtrView_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrView', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetMtrView(_hmap: maptype.HMAP, _number: int, _view: int) -> int:
        """
        Установить степень видимости матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _view: степень видимости матрицы: ``0`` - не виден ``1`` - полная ``2`` - насыщенная ``3`` - полупрозрачная ``4`` - средняя ``5`` - прозрачная
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtrView_t (_hmap, _number, _view)

    mapGetMtrTransparent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrTransparent', maptype.HMAP, ctypes.c_long)
    def mapGetMtrTransparent(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить прозрачность палитры матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: Возвращает степень прозрачности в процентах от 0 до 100
        :rtype: int
        """
        return mapGetMtrTransparent_t (_hmap, _number)

    mapSetMtrTransparent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrTransparent', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetMtrTransparent(_hmap: maptype.HMAP, _number: int, _transparent: int) -> int:
        """
        Установить прозрачность палитры матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _transparent: прозрачность в процентах от ``0`` до ``100``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtrTransparent_t (_hmap, _number, _transparent)

    mapGetMtrViewOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrViewOrder', maptype.HMAP, ctypes.c_long)
    def mapGetMtrViewOrder(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить порядок отображения матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: Возвращает: ``0`` - под картой, ``1`` - над картой При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrViewOrder_t (_hmap, _number)

    mapSetMtrViewOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrViewOrder', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetMtrViewOrder(_hmap: maptype.HMAP, _number: int, _order: int) -> int:
        """
        Установить порядок отображения матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _order: порядок: ``0`` - под картой, ``1`` - над картой
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtrViewOrder_t (_hmap, _number, _order)

    mapChangeOrderMtrShow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapChangeOrderMtrShow', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapChangeOrderMtrShow(_hmap: maptype.HMAP, _oldnumber: int, _newnumber: int) -> int:
        """
        Поменять очередность отображения матриц (mtr) в цепочке
        
        :param _hmap: идентификатор открытых данных
        
        :param _oldnumber: номер файла в цепочке
        
        :param _newnumber: устанавливаемый номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapChangeOrderMtrShow_t (_hmap, _oldnumber, _newnumber)

    mapGetPaintControlMatrixSmoothing_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetPaintControlMatrixSmoothing', maptype.HPAINT)
    def mapGetPaintControlMatrixSmoothing(_hpaint: maptype.HPAINT) -> int:
        """
        Запросить режим сглаживания растрово-матричных данных
        
        :param _hpaint: контекст поддержки многопоточного вызова (mapCreatePaintControl) или ``0``
        
        :returns: Возвращает установленный режим сглаживания
        :rtype: int
        """
        return mapGetPaintControlMatrixSmoothing_t (_hpaint)

    mapSetPaintControlMatrixSmoothing_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetPaintControlMatrixSmoothing', maptype.HPAINT, ctypes.c_long)
    def mapSetPaintControlMatrixSmoothing(_hpaint: maptype.HPAINT, _mode: int) -> int:
        """
        Установить режим сглаживания растрово-матричных данных
        
        :param _mode: режим отображения (``0`` - быстрое, ``1`` - со сглаживанием)
        
        :param _hpaint: контекст поддержки многопоточного вызова (mapCreatePaintControl) или ``0``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetPaintControlMatrixSmoothing_t (_hpaint, _mode)

    mapGetMtrShadow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrShadow', maptype.HMAP)
    def mapGetMtrShadow(_hmap: maptype.HMAP) -> int:
        """
        Запросить глубину тени матрицы высот
        
        :param _hmap: идентификатор открытых данных
        
        :returns: Возвращает флаг наложения тени (от 0 до 16): MTRSHADOW_NONE   ``=  0``,   // Тень отсутствует MTRSHADOW_PALE   ``=  1``,   // Бледная MTRSHADOW_WEAK   ``=  2``,   // Слабая MTRSHADOW_MIDDLE ``=  4``,   // Средняя MTRSHADOW_HEAVY  ``=  8``,   // Сильная MTRSHADOW_DEEP   ``= 16``,   // Глубокая
        :rtype: int
        """
        return mapGetMtrShadow_t (_hmap)

    mapSetMtrShadow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrShadow', maptype.HMAP, ctypes.c_long)
    def mapSetMtrShadow(_hmap: maptype.HMAP, _value: int) -> int:
        """
        Установить глубину тени матрицы высот
        
        :param _hmap: идентификатор открытых данных
        
        :param _value: флаг наложения тени (от ``0`` до ``16``): ``MTRSHADOW_NONE``   ``=  0``,   // Тень отсутствует ``MTRSHADOW_PALE``   ``=  1``,   // Бледная ``MTRSHADOW_WEAK``   ``=  2``,   // Слабая ``MTRSHADOW_MIDDLE`` ``=  4``,   // Средняя ``MTRSHADOW_HEAVY``  ``=  8``,   // Сильная ``MTRSHADOW_DEEP``   ``= 16``,   // Глубокая
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtrShadow_t (_hmap, _value)

    mapGetMtrShadowIntensity_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrShadowIntensity', maptype.HMAP)
    def mapGetMtrShadowIntensity(_hmap: maptype.HMAP) -> int:
        """
        Запросить интенсивность тени матрицы высот
        
        :param _hmap: идентификатор открытых данных
        
        :returns: Возвращает интенсивность тени (от 0 до 100) При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrShadowIntensity_t (_hmap)

    mapSetMtrShadowIntensity_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrShadowIntensity', maptype.HMAP, ctypes.c_long)
    def mapSetMtrShadowIntensity(_hmap: maptype.HMAP, _value: int) -> int:
        """
        Установить интенсивность тени матрицы высот
        
        :param _hmap: идентификатор открытых данных
        
        :param _value: интенсивность тени (от ``0`` до ``100``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtrShadowIntensity_t (_hmap, _value)

    mapGetMtrPaletteCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrPaletteCount', maptype.HMAP)
    def mapGetMtrPaletteCount(_hmap: maptype.HMAP) -> int:
        """
        Запросить число цветов в палитре матриц высот
        
        :param _hmap: идентификатор открытых данных ВСЕ МАТРИЦЫ ВЫСОТ РАБОТАЮТ С ОДНОЙ ПАЛИТРОЙ
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrPaletteCount_t (_hmap)

    mapGetMtrPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrPalette', maptype.HMAP, ctypes.POINTER(maptype.COLORREF), ctypes.c_long)
    def mapGetMtrPalette(_hmap: maptype.HMAP, _palette: ctypes.POINTER(maptype.COLORREF), _count: int) -> int:
        """
        Запросить текущую палитру матрицы высот (с учетом яркости/контрастности)
        
        :param _hmap: идентификатор открытых данных
        
        :param _palette: адрес области для размещения палитры
        
        :param _count: число считываемых элементов палитры (размер области в байтах / ``4``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrPalette_t (_hmap, _palette, _count)

    mapGetMtrStandardPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrStandardPalette', maptype.HMAP, ctypes.POINTER(maptype.COLORREF), ctypes.c_long)
    def mapGetMtrStandardPalette(_hmap: maptype.HMAP, _palette: ctypes.POINTER(maptype.COLORREF), _count: int) -> int:
        """
        Запросить эталонную палитру матрицы высот (без учета яркости/контрасности)
        
        :param _hmap: идентификатор открытых данных
        
        :param _palette: адрес области для размещения палитры
        
        :param _count: число считываемых элементов палитры (размер области в байтах / ``4``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrStandardPalette_t (_hmap, _palette, _count)

    mapSetMtrPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrPalette', maptype.HMAP, ctypes.POINTER(maptype.COLORREF), ctypes.c_long)
    def mapSetMtrPalette(_hmap: maptype.HMAP, _palette: ctypes.POINTER(maptype.COLORREF), _count: int) -> int:
        """
        Установить описание палитры матрицы высот
        
        :param _hmap: идентификатор открытых данных
        
        :param _palette: адрес устанавливаемой палитры
        
        :param _count: число элементов в новой палитре
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtrPalette_t (_hmap, _palette, _count)

    mapGetMtrBright_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrBright', maptype.HMAP)
    def mapGetMtrBright(_hmap: maptype.HMAP) -> int:
        """
        Запросить яркость палитры матрицы высот
        
        :param _hmap: идентификатор открытых данных
        
        :returns: Возвращает значение яркости (-16..+16) При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrBright_t (_hmap)

    mapSetMtrBright_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrBright', maptype.HMAP, ctypes.c_long)
    def mapSetMtrBright(_hmap: maptype.HMAP, _bright: int) -> int:
        """
        Установить яркость палитры матрицы высот
        
        :param _hmap: идентификатор открытых данных
        
        :param _bright: значение яркости (-``16``..+``16``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtrBright_t (_hmap, _bright)

    mapGetMtrContrast_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrContrast', maptype.HMAP)
    def mapGetMtrContrast(_hmap: maptype.HMAP) -> int:
        """
        Запросить контрастность палитры матрицы высот
        
        :param _hmap: идентификатор открытых данных
        
        :returns: Возвращает значение контраста в диапазоне (-16..+16) При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrContrast_t (_hmap)

    mapSetMtrContrast_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrContrast', maptype.HMAP, ctypes.c_long)
    def mapSetMtrContrast(_hmap: maptype.HMAP, _contrast: int) -> int:
        """
        Установить контрастность палитры матрицы высот
        
        :param _hmap: идентификатор открытых данных
        
        :param _contrast: значение контраста (-``16``..+``16``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtrContrast_t (_hmap, _contrast)

    mapGetMtrGamma_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrGamma', maptype.HMAP)
    def mapGetMtrGamma(_hmap: maptype.HMAP) -> int:
        """
        Запросить параболическую яркость палитры матрицы высот
        
        :param _hmap: идентификатор открытых данных
        
        :returns: Возвращает значение параболической яркости При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrGamma_t (_hmap)

    mapSetMtrGamma_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrGamma', maptype.HMAP, ctypes.c_long)
    def mapSetMtrGamma(_hmap: maptype.HMAP, _gamma: int) -> int:
        """
        Установить параболическую яркость палитры матрицы высот
        
        :param _hmap: идентификатор открытых данных
        
        :param _gamma: параболическая яркость
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtrGamma_t (_hmap, _gamma)

    mapGetMtrColorStyle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrColorStyle', maptype.HMAP)
    def mapGetMtrColorStyle(_hmap: maptype.HMAP) -> int:
        """
        Запросить стиль палитры матрицы высот
        
        :param _hmap: идентификатор открытых данных Возвращаемое значение: ``0`` - полутоновая палитра ``1`` - цветная палитра -``1`` - отображаются только тени от рельефа
        """
        return mapGetMtrColorStyle_t (_hmap)

    mapSetMtrColorStyle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrColorStyle', maptype.HMAP, ctypes.c_long)
    def mapSetMtrColorStyle(_hmap: maptype.HMAP, _colorstyle: int) -> int:
        """
        Установить стиль палитры матрицы высот
        
        :param _hmap: идентификатор открытых данных
        
        :param _colorstyle: стиль отображения матрицы: ``0`` - полутоновая палитра ``1`` - цветная палитра -``1`` - отображаются только тени от рельефа
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtrColorStyle_t (_hmap, _colorstyle)

    mapSetMtrColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrColor', maptype.HMAP, ctypes.c_long, ctypes.c_long, maptype.COLORREF)
    def mapSetMtrColor(_hmap: maptype.HMAP, _number: int, _colornumber: int, _color: maptype.COLORREF) -> int:
        """
        Установить цвет диапазона высот матрицы с номером number в цепочке
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _colornumber: номер диапазона высот
        
        :param _color: цвет диапазона
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtrColor_t (_hmap, _number, _colornumber, _color)

    mapGetMtrUserDiapason_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrUserDiapason', maptype.HMAP)
    def mapGetMtrUserDiapason(_hmap: maptype.HMAP) -> int:
        """
        Запросить флаг пользовательского диапазона цепочки матриц высот
        
        :param _hmap: идентификатор открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrUserDiapason_t (_hmap)

    mapSetMtrUserDiapason_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrUserDiapason', maptype.HMAP, ctypes.c_long)
    def mapSetMtrUserDiapason(_hmap: maptype.HMAP, _value: int) -> int:
        """
        Установить флаг пользовательского диапазона цепочки матриц высот
        
        :param _hmap: идентификатор открытых данных
        
        :param _value: признак пользовательского диапазона (``0`` / ``1``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtrUserDiapason_t (_hmap, _value)

    mapGetMtrViewOutUserDiapason_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrViewOutUserDiapason', maptype.HMAP)
    def mapGetMtrViewOutUserDiapason(_hmap: maptype.HMAP) -> int:
        """
        Запросить флаг отображения высот вне пользовательского диапазона граничными цветами
        
        :param _hmap: идентификатор открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrViewOutUserDiapason_t (_hmap)

    mapSetMtrViewOutUserDiapason_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrViewOutUserDiapason', maptype.HMAP, ctypes.c_long)
    def mapSetMtrViewOutUserDiapason(_hmap: maptype.HMAP, _value: int) -> int:
        """
        Установить флаг отображения высот вне пользовательского диапазона граничными цветами
        
        :param _hmap: идентификатор открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtrViewOutUserDiapason_t (_hmap, _value)

    mapGetMtwPaletteCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtwPaletteCount', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapGetMtwPaletteCount(_hmap: maptype.HMAP, _number: int, _userlabel: int) -> int:
        """
        Запросить количество цветов в палитре матрицы number
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц: ``0`` - возращает общее количество цветов для всех открытых матриц с меткой userLabel
        
        :param _userlabel: метка файла MTW (определяется функцией mapGetMtwUserLabel): ``0`` - выполняется запрос для матриц высот ``LABEL_MTW_DEPTH`` - выполняется запрос для матриц глубин ``LABEL_MTW_EGM`` - выполняется запрос для матриц поправок высот геоида
        
        :returns: ``> 0`` - возвращает количество цветов матрицы с номером number и меткой userLabel -``1`` - возвращает максимальное количество цветов для всех матриц с меткой userLabel При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtwPaletteCount_t (_hmap, _number, _userlabel)

    mapGetMtwPaletteDiapason_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtwPaletteDiapason', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.COLORREF), ctypes.POINTER(ctypes.c_double))
    def mapGetMtwPaletteDiapason(_hmap: maptype.HMAP, _number: int, _userlabel: int, _count: int, _minimum: ctypes.POINTER(ctypes.c_double), _maximum: ctypes.POINTER(ctypes.c_double), _palette: ctypes.POINTER(maptype.COLORREF), _diapason: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить для матрицы массив цветов палитры и массив граничных значений диапазонов высот
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц: ``0`` - заполняет массивы цветов и диапазонов для всех открытых матриц с меткой userLabel ``> 0`` - заполняет массивы цветов и диапазонов для матрицы с номером number и меткой userLabel -``1`` - заполняет полные массивы цветов и диапазонов для всех матриц с меткой userLabel (полный массив диапазонов высот заполняется только для ``LABEL_MTW_DEPTH`` и ``LABEL_MTW_EGM``)
        
        :param _userlabel: метка файла MTW (определяется функцией mapGetMtwUserLabel): ``0`` - выполняется запрос для матриц высот ``LABEL_MTW_DEPTH`` - выполняется запрос для матриц глубин ``LABEL_MTW_EGM`` - выполняется запрос для матриц поправок высот геоида
        
        :param _count: количество элементов в массиве цветов и массиве диапазонов (определяется функцией mapGetMtwPaletteCount)
        
        :param _minimum: минимальное значение в метрах (если ``0``, то не заполняется)
        
        :param _maximum: максимальное значение в метрах (если ``0``, то не заполняется) если number ``= 0`` - minimum, maximum - общие для всех открытых матриц с меткой userlabel number ``> 0`` - minimum, maximum - для матрицы с номером number number ``= -1`` - minimum, maximum не заполняюся
        
        :param _palette: массив цветов палитры размером count ``*`` sizeof(``COLORREF``) или более если palette ``= 0``, то массив не заполняется
        
        :param _diapason: массив нижних граничных значений диапазонов в метрах размером count ``*`` sizeof(double) или более если diapason ``= 0``, то массив не заполняется
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtwPaletteDiapason_t (_hmap, _number, _userlabel, _count, _minimum, _maximum, _palette, _diapason)

    mapSetMtrBorderEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrBorderEx', maptype.HMAP, ctypes.c_long, maptype.HOBJ, ctypes.c_long)
    def mapSetMtrBorderEx(_hmap: maptype.HMAP, _number: int, _hobj: maptype.HOBJ, _flagsubject: int) -> int:
        """
        Установить рамку матрицы по метрике замкнутого объекта
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _hobj: замкнутый объект карты, должен иметь не менее ``4``-х точек
        
        :param _flagsubject: флаг использования подобъектов объекта при установке рамки матрицы (``0``/``1``) ``0`` - в качестве рамки матрицы устанавливается контур объекта ``1`` - в качестве рамки матрицы устанавливается контур объекта с подобъектами
        
        :returns: При ошибке возвращает 0
        :rtype: int
        
        .. note::

           После выполнения функции отображение растра ограничится заданной областью
        """
        return mapSetMtrBorderEx_t (_hmap, _number, _hobj, _flagsubject)

    mapGetMtrBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrBorder', maptype.HMAP, ctypes.c_long, maptype.HOBJ)
    def mapGetMtrBorder(_hmap: maptype.HMAP, _number: int, _hobj: maptype.HOBJ) -> int:
        """
        Запросить объект рамки матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _hobj: идентификатор объекта рамки матрицы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrBorder_t (_hmap, _number, _hobj)

    mapDeleteMtrBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteMtrBorder', maptype.HMAP, ctypes.c_long)
    def mapDeleteMtrBorder(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Удалить рамку матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           После выполнения функции отображение матрицы будет полным
        """
        return mapDeleteMtrBorder_t (_hmap, _number)

    mapCheckExistenceMtrBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckExistenceMtrBorder', maptype.HMAP, ctypes.c_long)
    def mapCheckExistenceMtrBorder(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Определить существование рамки матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCheckExistenceMtrBorder_t (_hmap, _number)

    mapCheckShowMtrByBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckShowMtrByBorder', maptype.HMAP, ctypes.c_long)
    def mapCheckShowMtrByBorder(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Определить способ отображения матрицы (относительно рамки)
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: Возвращает: ``1`` - при отображении матрицы по рамке ``0`` - при отображении матрицы без учета рамки При ошибке возвращает -1
        :rtype: int
        """
        return mapCheckShowMtrByBorder_t (_hmap, _number)

    mapShowMtrByBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapShowMtrByBorder', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapShowMtrByBorder(_hmap: maptype.HMAP, _number: int, _value: int) -> int:
        """
        Установить отображение матрицы по рамке
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц value  ``= 1`` - отобразить матрицу по рамке ``= 0`` - отобразить матрицу без учета рамки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapShowMtrByBorder_t (_hmap, _number, _value)

    mapGetImmediatePointOfMtrBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetImmediatePointOfMtrBorder', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetImmediatePointOfMtrBorder(_hmap: maptype.HMAP, _number: int, _pointin: ctypes.POINTER(maptype.DOUBLEPOINT), _pointout: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Определить координаты и порядковый номер точки рамки, которая входит в прямоугольник Габариты растра (матрицы)
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _pointin: координаты точки в метрах в системе документа
        
        :param _pointout: адрес для записи координат найденной точки в метрах в системе документа Определяется точка рамки, которая имеет наименьшее удаление от точки pointin
        
        :returns: При ошибке или отсутствии рамки возвращает ноль
        :rtype: int
        """
        return mapGetImmediatePointOfMtrBorder_t (_hmap, _number, _pointin, _pointout)

    mapGetMtrProcessingState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrProcessingState', maptype.HMAP, ctypes.c_long)
    def mapGetMtrProcessingState(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить состояние матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц Возвращаемые значения: ``0`` - нет данных или создание уменьшенных копий и сжатие не выполнялись ``3`` - создание всех уровней уменьшенных копий, сжатие ``RMF_COMPR_32`` матрицы ``4`` - создание всех уровней уменьшенных копий матрицы
        """
        return mapGetMtrProcessingState_t (_hmap, _number)

    mapSetMtrProcessingState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrProcessingState', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetMtrProcessingState(_hmap: maptype.HMAP, _number: int, _state: int) -> int:
        """
        Установить состояние матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _state: состояние матрицы. Возможные значения состояния матрицы state: ``0`` - нет данных; или создание уменьшенных копий и сжатие не выполнялись ``3`` - создание всех уровней уменьшенных копий, сжатие ``RMF_COMPR_32`` матрицы ``4`` - создание всех уровней уменьшенных копий матрицы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtrProcessingState_t (_hmap, _number, _state)

    mapOptimizationMtrByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapOptimizationMtrByNameUn', maptype.PWCHAR, maptype.HWND)
    def mapOptimizationMtrByNameUn(_mtrname: mapsyst.WTEXT, _handle: maptype.HWND) -> int:
        """
        Оптимизировать матрицу
        
        :param _mtrname: имя файла матрицы
        
        :param _handle: идентификатор окна, которое будет извещаться о ходе процесса (``0x585`` - ``0x588``) Функция проверяет состояние матрицы и при необходимости выполняет для неё оптимизацию со сжатием и создание всех уровней уменьшенной копии Необходимо закрыть матрицу из всех документов перед вызовом функции
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapOptimizationMtrByNameUn_t (_mtrname.buffer(), _handle)

    mapGetMtrDuplicatesCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrDuplicatesCount', maptype.HMAP, ctypes.c_long)
    def mapGetMtrDuplicatesCount(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить количество созданных уменьшенных копий в матрице
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц Каждый элемент уменьшенной копии формируется интерполяцией из ``16`` элементов предыдущего уровня (``4`` х ``4``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrDuplicatesCount_t (_hmap, _number)

    mapUpdateMtrDuplicates_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateMtrDuplicates', maptype.HMAP, ctypes.c_long)
    def mapUpdateMtrDuplicates(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Обновить уменьшенную копию
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdateMtrDuplicates_t (_hmap, _number)

    mapOpenMtr3D_t = mapsyst.GetProcAddress(acceslib,maptype.HMTR3D,'mapOpenMtr3D', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapOpenMtr3D(_hmap: maptype.HMAP, _width: int, _height: int) -> maptype.HMTR3D:
        """
        Открыть сеанс трехмерной визуализации местности, обеспеченной открытыми матрицами высот
        
        :param _hmap: идентификатор открытых данных
        
        :param _width: ширина изображения
        
        :param _height: высота изображения
        
        :returns: Возвращает идентификатор открытого сеанса (TMtr3D*) При ошибке возвращает ноль
        :rtype: maptype.HMTR3D
        """
        return mapOpenMtr3D_t (_hmap, _width, _height)

    mapCloseMtr3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseMtr3D', maptype.HMTR3D)
    def mapCloseMtr3D(_hmtr3d: maptype.HMTR3D) -> ctypes.c_void_p:
        """
        Закрыть сеанс трехмерной визуализации местности
        
        :param _hmtr3d: идентификатор открытого сеанса 3D визуализации
        """
        return mapCloseMtr3D_t (_hmtr3d)

    mapPaintMtr3DUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapPaintMtr3DUn', maptype.HMTR3D, maptype.HDC, ctypes.POINTER(maptype.MTR3DVIEWUN))
    def mapPaintMtr3DUn(_hmtr3d: maptype.HMTR3D, _hDC: maptype.HDC, _parm: ctypes.POINTER(maptype.MTR3DVIEWUN)) -> ctypes.c_void_p:
        """
        Отобразить фрагмент местности в трехмерном виде
        
        :param _hmtr3d: идентификатор открытого сеанса 3D визуализации
        
        :param _parm: параметры отображения (описаны в maptype.h)
        
        :param _hDC: контекст отображения
        """
        return mapPaintMtr3DUn_t (_hmtr3d, _hDC, _parm)

    mapSetMtr3DHeightWater_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetMtr3DHeightWater', maptype.HMTR3D, ctypes.c_double)
    def mapSetMtr3DHeightWater(_hmtr3d: maptype.HMTR3D, _height: float) -> ctypes.c_void_p:
        """
        Установить уровень затопления
        
        :param _hmtr3d: идентификатор открытого сеанса 3D визуализации
        
        :param _height: уровень затопления
        """
        return mapSetMtr3DHeightWater_t (_hmtr3d, _height)

    mapBuildMtr3DUn_t = mapsyst.GetProcAddress(acceslib,maptype.HBITMAP,'mapBuildMtr3DUn', maptype.HMTR3D, ctypes.POINTER(maptype.MTR3DVIEWUN))
    def mapBuildMtr3DUn(_hmtr3d: maptype.HMTR3D, _parm: ctypes.POINTER(maptype.MTR3DVIEWUN)) -> maptype.HBITMAP:
        """
        Построить BITMAP с изображением фрагмента местности в трехмерном виде
        
        :param _hmtr3d: идентификатор открытого сеанса 3D визуализации
        
        :param _parm: параметры отображения (описаны в maptype.h)
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HBITMAP
        """
        return mapBuildMtr3DUn_t (_hmtr3d, _parm)

    mapCreateMtwUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateMtwUn', maptype.PWCHAR, ctypes.POINTER(maptype.BUILDMTW), ctypes.POINTER(maptype.MTRPROJECTIONDATA))
    def mapCreateMtwUn(_mtrname: mapsyst.WTEXT, _mtrparm: ctypes.POINTER(maptype.BUILDMTW), _mtrprojectiondata: ctypes.POINTER(maptype.MTRPROJECTIONDATA)) -> maptype.HMAP:
        """
        Создать матричную карту
        
        :param _mtrname: имя файла создаваемой матрицы
        
        :param _mtrparm: параметры создания матрицы высот
        
        :param _mtrprojectiondata: параметры проекции
        
        :returns: Возвращает идентификатор открытой матричной карты Структуры BUILDMTW, MTRPROJECTIONDATA описаны в maptype.h При ошибке возвращает ноль
        :rtype: maptype.HMAP
        """
        return mapCreateMtwUn_t (_mtrname.buffer(), _mtrparm, _mtrprojectiondata)

    mapCreateMtwForSqlite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateMtwForSqlite', maptype.PWCHAR, ctypes.POINTER(maptype.BUILDMTW), ctypes.POINTER(maptype.MTRPROJECTIONDATA), ctypes.c_double, ctypes.c_double)
    def mapCreateMtwForSqlite(_mtrname: mapsyst.WTEXT, _mtrparm: ctypes.POINTER(maptype.BUILDMTW), _mtrprojectiondata: ctypes.POINTER(maptype.MTRPROJECTIONDATA), _minvalue: float, _maxvalue: float) -> int:
        """
        Создать матричную карту для БД SQLite
        
        :param _mtrname: имя создаваемой матрицы
        
        :param _mtrparm: параметры создания матрицы высот
        
        :param _mtrprojectiondata: параметры проекции
        
        :param _minvalue: минимальное значение данных в матрице
        
        :param _maxvalue: максимальное значение данных в матрице Структуры ``BUILDMTW``, ``MTRPROJECTIONDATA`` описаны в maptype.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCreateMtwForSqlite_t (_mtrname.buffer(), _mtrparm, _mtrprojectiondata, _minvalue, _maxvalue)

    mapPutMtrFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPutMtrFrame', maptype.HMAP, ctypes.c_long, ctypes.c_char_p, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapPutMtrFrame(_hmap: maptype.HMAP, _number: int, _bits: ctypes.c_char_p, _left: int, _top: int, _width: int, _height: int, _beginning: int) -> int:
        """
        Вывести прямоугольный участок матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _bits: адрес логического начала выводимого участка (смотреть параметр beginning)
        
        :param _left: смещение участка матрицы слева (в элементах)
        
        :param _top: смещение участка матрицы сверху (в элементах)
        
        :param _width: ширина участка матрицы (в элементах)
        
        :param _height: высота участка матрицы (в элементах)
        
        :param _beginning: определяет, на какую строку указывает bits : если beginning ``= 0``, то bits указывает на начало верхней строки выводимого участка если beginning ``= 1``, то bits указывает на начало нижней строки выводимого участка Размер участка, заданного адресом bits, должен быть не менее (width ``*`` height ``*`` размер элемента матрицы в байтах), в противном случае возможны ошибки работы с памятью Запрос размера элемента матрицы в байтах - функция mapGetMtrElementSize. Высоты выводимого участка должны быть записаны в области bits в единицах измерения высот данной матрицы Запрос единицы измерения высоты матрицы - функция mapGetMtrMeasure
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPutMtrFrame_t (_hmap, _number, _bits, _left, _top, _width, _height, _beginning)

    mapGetMtrFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrFrame', maptype.HMAP, ctypes.c_long, ctypes.c_char_p, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapGetMtrFrame(_hmap: maptype.HMAP, _number: int, _bits: ctypes.c_char_p, _left: int, _top: int, _width: int, _height: int, _widthinbyte: int) -> int:
        """
        Прочитать прямоугольный участок матрицы в заданную область памяти
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _bits: указатель на начало области памяти
        
        :param _left: смещение участка матрицы слева (в элементах)
        
        :param _top: смещение участка матрицы сверху (в элементах)
        
        :param _width: ширина участка матрицы (в элементах)
        
        :param _height: высота участка матрицы (в элементах)
        
        :param _widthinbyte: ширинa участка матрицы в байтах Размер участка, заданного адресом bits, должен быть не менее (width ``*`` height ``*`` размер элемента матрицы в байтах), в противном случае возможны ошибки работы с памятью Запрос размера элемента матрицы в байтах - функция mapGetMtrElementSize Высоты участка записываются в область bits в единицах измерения значений высот данной матрицы Запрос единицы измерения значений высот матрицы - функция mapGetMtrMeasure
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrFrame_t (_hmap, _number, _bits, _left, _top, _width, _height, _widthinbyte)

    mapGetReliefRange_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetReliefRange', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGetReliefRange(_hmap: maptype.HMAP, _minvalue: ctypes.POINTER(ctypes.c_double), _maxvalue: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить диапазон высот рельефа (суммарный диапазон всех матриц высот, слоев, TIN-моделей)
        
        :param _hmap: идентификатор открытых данных
        
        :param _minvalue: минимальная высота диапазона в метрах
        
        :param _maxvalue: максимальная высота диапазона в метрах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetReliefRange_t (_hmap, _minvalue, _maxvalue)

    mapSetMtrShowRange_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrShowRange', maptype.HMAP, ctypes.c_long, ctypes.c_double, ctypes.c_double)
    def mapSetMtrShowRange(_hmap: maptype.HMAP, _number: int, _minvalue: float, _maxvalue: float) -> int:
        """
        Занести в матрицу диапазон значений высот
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _minvalue: минимальная высота диапазона в метрах
        
        :param _maxvalue: максимальная высота диапазона в метрах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtrShowRange_t (_hmap, _number, _minvalue, _maxvalue)

    mapGetMtrShowRange_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrShowRange', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGetMtrShowRange(_hmap: maptype.HMAP, _number: int, _minvalue: ctypes.POINTER(ctypes.c_double), _maxvalue: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить диапазон значений высот матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _minvalue: минимальная высота диапазона в метрах
        
        :param _maxvalue: максимальная высота диапазона в метрах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrShowRange_t (_hmap, _number, _minvalue, _maxvalue)

    mapSetMtrHeightRangeEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrHeightRangeEx', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapSetMtrHeightRangeEx(_hmap: maptype.HMAP, _minvalue: float, _maxvalue: float, _viewOutRange: int) -> int:
        """
        Установить диапазон отображаемых высот всей цепочки матриц
        
        :param _hmap: идентификатор открытых данных
        
        :param _minvalue: минимальная высота диапазона в метрах
        
        :param _maxvalue: максимальная высота диапазона в метрах
        
        :param _viewOutRange: отображать элементы матрицы, значения которых вне диапазона (``0`` или ``1``): ``0`` - значения вне диапазона не отображаются ``1`` - элементы, имеющие значения высот < minvalue, отображаются первым цветом палитры матрицы элементы, имеющие значения высот > maxvalue, отображаются последним цветом палитры матрицы Установленный диапазон в матрицу не заносится (сохраняется в ``INI``-файл документа)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtrHeightRangeEx_t (_hmap, _minvalue, _maxvalue, _viewOutRange)

    mapGetMtrHeightRange_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrHeightRange', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGetMtrHeightRange(_hmap: maptype.HMAP, _minvalue: ctypes.POINTER(ctypes.c_double), _maxvalue: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить диапазон высот отображаемых элементов цепочки матриц
        
        :param _hmap: идентификатор открытых данных
        
        :param _minvalue: минимальная высота диапазона в метрах
        
        :param _maxvalue: максимальная высота диапазона в метрах
        
        :returns: При успешном завершении возвращает: ``1`` - диапазон высот был вычислен по матрицам цепочки ``2`` - диапазон высот установлен пользователем При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrHeightRange_t (_hmap, _minvalue, _maxvalue)

    mapResetMtrHeightRange_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapResetMtrHeightRange', maptype.HMAP)
    def mapResetMtrHeightRange(_hmap: maptype.HMAP) -> int:
        """
        Установить суммарный диапазон высот отображаемых элементов цепочки матриц
        
        :param _hmap: идентификатор открытых данных Суммарный диапазон включает в себя диапазоны всех открытых матриц высот в документе
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapResetMtrHeightRange_t (_hmap)

    mapSetMtrUserNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrUserNameUn', maptype.HMAP, ctypes.c_long, maptype.PWCHAR)
    def mapSetMtrUserNameUn(_hmap: maptype.HMAP, _number: int, _username: mapsyst.WTEXT) -> int:
        """
        Установить условное имя матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _username: условное имя матрицы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtrUserNameUn_t (_hmap, _number, _username.buffer())

    mapGetMtrUserNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrUserNameUn', maptype.HMAP, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetMtrUserNameUn(_hmap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _namesize: int) -> int:
        """
        Запросить условное имя матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _name: адрес строки в которую записывается условное имя матрицы
        
        :param _namesize: размер строки в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrUserNameUn_t (_hmap, _number, _name.buffer(), _namesize)

    mapGetMtwUserLabel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtwUserLabel', maptype.HMAP, ctypes.c_long)
    def mapGetMtwUserLabel(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить пользовательскую метку матрицы (MTW)
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: Возвращает: ``0`` - метка матрицы высот ``LABEL_MTW_DEPTH`` - метка матрицы глубин ``LABEL_MTW_EGM`` - метка матрицы поправок высот геоида При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtwUserLabel_t (_hmap, _number)

    mapGetSouthWestMtrPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSouthWestMtrPlane', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGetSouthWestMtrPlane(_hmap: maptype.HMAP, _number: int, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить координаты юго-западного угла матрицы в метрах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц x, y   - адреса для записи координат найденной точки в метрах в системе координат матрицы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSouthWestMtrPlane_t (_hmap, _number, _x, _y)

    mapGetActiveMtr_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetActiveMtr', maptype.HMAP)
    def mapGetActiveMtr(_hmap: maptype.HMAP) -> int:
        """
        Запросить активную матрицу (устанавливается приложением по своему усмотрению)
        
        :param _hmap: идентификатор открытой карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetActiveMtr_t (_hmap)

    mapSetActiveMtr_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetActiveMtr', maptype.HMAP, ctypes.c_long)
    def mapSetActiveMtr(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Установить активную матрицу (устанавливается приложением по своему усмотрению)
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetActiveMtr_t (_hmap, _number)

    mapGetMtrEdit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrEdit', maptype.HMAP, ctypes.c_long)
    def mapGetMtrEdit(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить флаг редактируемости матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrEdit_t (_hmap, _number)

    mapGetMtrCopyFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrCopyFlag', maptype.HMAP, ctypes.c_long)
    def mapGetMtrCopyFlag(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить может ли матрица копироваться или экспортироваться
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrCopyFlag_t (_hmap, _number)

    mapGetMtrPrintFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrPrintFlag', maptype.HMAP, ctypes.c_long)
    def mapGetMtrPrintFlag(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить может ли матрица выводиться на печать
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц Для данных, открытых на ГИС Сервере, может устанавливаться запрет вывода изображения на печать
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrPrintFlag_t (_hmap, _number)

    mapGetMtrHidePassportFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrHidePassportFlag', maptype.HMAP, ctypes.c_long)
    def mapGetMtrHidePassportFlag(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить можно ли показывать параметры паспорта
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц Для данных, открытых на ГИС Сервере, может устанавливаться запрет отображения параметров системы координат
        
        :returns: Если нет - возвращает ноль
        :rtype: int
        """
        return mapGetMtrHidePassportFlag_t (_hmap, _number)

    mapGetMtrFileSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrFileSize', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_int64))
    def mapGetMtrFileSize(_hmap: maptype.HMAP, _number: int, _filesize: ctypes.POINTER(ctypes.c_int64)) -> int:
        """
        Запросить размер файла
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _filesize: адрес для записи размера файла
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrFileSize_t (_hmap, _number, _filesize)

    mapGetMtrWidthInElement_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrWidthInElement', maptype.HMAP, ctypes.c_long)
    def mapGetMtrWidthInElement(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить ширину матрицы (элементы)
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrWidthInElement_t (_hmap, _number)

    mapGetMtrHeightInElement_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrHeightInElement', maptype.HMAP, ctypes.c_long)
    def mapGetMtrHeightInElement(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить высоту матрицы (элементы)
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrHeightInElement_t (_hmap, _number)

    mapGetMtrAccuracy_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrAccuracy', maptype.HMAP, ctypes.c_long)
    def mapGetMtrAccuracy(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить точность (метр/элемент) матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrAccuracy_t (_hmap, _number)

    mapSetAbsHeightDifference_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetAbsHeightDifference', maptype.HMAP, ctypes.c_long, ctypes.c_double)
    def mapSetAbsHeightDifference(_hmap: maptype.HMAP, _number: int, _difference: float) -> int:
        """
        Установить ошибку наложения высот (в единицах матрицы)
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _difference: ошибка наложения высот
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetAbsHeightDifference_t (_hmap, _number, _difference)

    mapGetMtrFlagLocationChanged_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrFlagLocationChanged', maptype.HMAP, ctypes.c_long)
    def mapGetMtrFlagLocationChanged(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить флаг изменения привязки (метры) матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrFlagLocationChanged_t (_hmap, _number)

    mapGetMtrType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrType', maptype.HMAP, ctypes.c_long)
    def mapGetMtrType(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить тип матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrType_t (_hmap, _number)

    maGetMtrPseudoCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'maGetMtrPseudoCode', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def maGetMtrPseudoCode(_hmap: maptype.HMAP, _number: int, _value: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить значения псевдокода матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _value: адрес для записи псевдокода матрицы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return maGetMtrPseudoCode_t (_hmap, _number, _value)

    mapGetMtrCompressNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtrCompressNumber', maptype.HMAP, ctypes.c_long)
    def mapGetMtrCompressNumber(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить флаг сжатия матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtrCompressNumber_t (_hmap, _number)

    mapSetMtrCompressNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtrCompressNumber', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetMtrCompressNumber(_hmap: maptype.HMAP, _number: int, _compressnumber: int) -> int:
        """
        Занести в матрицу высот номер алгоритма сжатия блоков
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _compressnumber: номер алгоритма сжатия блоков
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtrCompressNumber_t (_hmap, _number, _compressnumber)

    mapMtrOptimizationPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapMtrOptimizationPro', maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def mapMtrOptimizationPro(_handle: maptype.HMESSAGE, _name: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _compressnumber: int, _borderflag: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Сжать матрицу MTW по заданному алгоритму
        
        :param _handle: идентификатор диалога для передачи сообщений о проценте выполнения ``WM_PROGRESSBAR``
        
        :param _name: имя сжимаемого файла MTW
        
        :param _newname: имя сжатого файла MTW
        
        :param _compressnumber: номер алгоритма сжатия (``RMF_COMPR_32``)
        
        :param _borderflag: флаг удаления неотображаемых блоков (не попадающих в заданную рамку матрицы)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapMtrOptimizationPro_t (_handle, _name.buffer(), _newname.buffer(), _compressnumber, _borderflag, _callevent, _parm)

    mapDeleteMtrFileUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteMtrFileUn', maptype.PWCHAR)
    def mapDeleteMtrFileUn(_name: mapsyst.WTEXT) -> int:
        """
        Удалить файл матрицы высот
        
        :param _name: имя файла матрицы высот Функция предназначена для удаления матрицы высот и еe составных частей Матрица высот размером более 4Gb состоит из ``2``-х файлов: ``*.mtw`` и ``*.mtw.01`` Аналог функции DeleteTheFile()
        """
        return mapDeleteMtrFileUn_t (_name.buffer())

    mapMoveMtrFileUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapMoveMtrFileUn', maptype.PWCHAR, maptype.PWCHAR)
    def mapMoveMtrFileUn(_oldname: mapsyst.WTEXT, _newname: mapsyst.WTEXT) -> int:
        """
        Переименовать имя файла матрицы высот
        
        :param _oldname: старое имя файла матрицы высот
        
        :param _newname: новое имя файла матрицы высот Функция предназначена для переименовывания матрицы высот и её составных частей Матрица высот размером более 4Gb состоит из ``2``-х файлов: ``*.mtw`` и ``*.mtw.01`` Аналог функции MoveTheFile()
        """
        return mapMoveMtrFileUn_t (_oldname.buffer(), _newname.buffer())

    mapCopyMtrFileUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCopyMtrFileUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapCopyMtrFileUn(_oldname: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _exist: int) -> int:
        """
        Скопировать файл матрицы высот
        
        :param _oldname: старое имя файла матрицы высот
        
        :param _newname: новое имя файла матрицы высот
        
        :param _exist: флаг наличия файла Функция предназначена для копирования матрицы высот и её составных частей Матрица высот размером более 4Gb состоит из ``2``-х файлов: ``*.mtw`` и ``*.mtw.01`` Аналог функции CopyTheFile()
        """
        return mapCopyMtrFileUn_t (_oldname.buffer(), _newname.buffer(), _exist)

    mapCreateMtrLegendToXML_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateMtrLegendToXML', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def mapCreateMtrLegendToXML(_hmap: maptype.HMAP, _xmlname: mapsyst.WTEXT, _imgpath: mapsyst.WTEXT, _imgsize: int) -> int:
        """
        Подготовить легенду матрицы высот
        
        :param _hmap: идентификатор открытых данных
        
        :param _xmlname: имя выходного xml-файла
        
        :param _imgpath: путь к изображениям формата png
        
        :param _imgsize: нестандартный размер изображения (сторона квадрата), если равен нулю, то будут созданы только изображения размеров 16x16, 24x24 и 32x32 Максимальный размер изображения 1024x1024 При необходимости создания изображения нестандартного размера (отличного от 16x16, 24x24 и 32x32) указать размер в параметре imgsize
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCreateMtrLegendToXML_t (_hmap, _xmlname.buffer(), _imgpath.buffer(), _imgsize)

    mapSmoothMtrUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSmoothMtrUn', maptype.PWCHAR, ctypes.c_double, maptype.HMESSAGE, ctypes.c_long)
    def mapSmoothMtrUn(_mtrname: mapsyst.WTEXT, _smooth: float, _hwnd: maptype.HMESSAGE, _messageid: int) -> int:
        """
        Выполнить сплайн сглаживание матрицы высот
        
        :param _mtrname: имя сглаживаемой матрицы
        
        :param _smooth: уровень сглаживания (от ``0`` до ``1``)
        
        :param _hwnd: идентификатор окна в которое послыается сообщение с процентом обработки (если ``= 0``, то сообщение не посылается)
        
        :param _messageid: идентификатор сообщения с процентом обработки (``WM_OBJECT``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSmoothMtrUn_t (_mtrname.buffer(), _smooth, _hwnd, _messageid)

    mapOpenMtqUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapOpenMtqUn', maptype.PWCHAR, ctypes.c_long)
    def mapOpenMtqUn(_mtqname: mapsyst.WTEXT, _mode: int) -> maptype.HMAP:
        """
        Открыть матрицу качеств
        
        :param _mtqname: имя открываемого файла
        
        :param _mode: режим чтения/записи (``GENERIC_READ``, ``GENERIC_WRITE`` или ``0``) ``GENERIC_READ`` - все данные только на чтение
        
        :returns: Возвращает идентификатор открытой матричной карты При ошибке возвращает ноль
        :rtype: maptype.HMAP
        """
        return mapOpenMtqUn_t (_mtqname.buffer(), _mode)

    mapCloseMtq_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseMtq', maptype.HMAP, ctypes.c_long)
    def mapCloseMtq(_hmap: maptype.HMAP, _number: int) -> ctypes.c_void_p:
        """
        Закрыть матрицу качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер закрываемой матрицы ``0`` - закрываются все матрицы в окне Чтобы освободить все ресурсы - нужно вызвать mapCloseData(hmap)
        """
        return mapCloseMtq_t (_hmap, _number)

    mapOpenMtqForMapUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapOpenMtqForMapUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapOpenMtqForMapUn(_hmap: maptype.HMAP, _mtqname: mapsyst.WTEXT, _mode: int) -> int:
        """
        Открыть данные матрицы качеств в заданном районе работ (добавить в цепочку матриц качеств)
        
        :param _hmap: идентификатор открытых данных
        
        :param _mtqname: имя открываемого файла
        
        :param _mode: режим чтения/записи (``GENERIC_READ``, ``GENERIC_WRITE`` или ``0``) ``GENERIC_READ`` - все данные только на чтение
        
        :returns: Возвращает номер файла в цепочке матриц При ошибке возвращает ноль
        :rtype: int
        """
        return mapOpenMtqForMapUn_t (_hmap, _mtqname.buffer(), _mode)

    mapCloseMtqForMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCloseMtqForMap', maptype.HMAP, ctypes.c_long)
    def mapCloseMtqForMap(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Закрыть данные матрицы качеств в заданном районе работ
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц ``0`` - закрываются все матричные данные
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCloseMtqForMap_t (_hmap, _number)

    mapGetMtqNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqNameUn', maptype.HMAP, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetMtqNameUn(_hmap: maptype.HMAP, _number: int, _mtqname: mapsyst.WTEXT, _namesize: int) -> int:
        """
        Запросить имя файла данных матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _mtqname: адрес для записи имени файла
        
        :param _namesize: размер имени файла
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqNameUn_t (_hmap, _number, _mtqname.buffer(), _namesize)

    mapGetMtqNumberUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqNumberUn', maptype.HMAP, maptype.PWCHAR)
    def mapGetMtqNumberUn(_hmap: maptype.HMAP, _mtqname: mapsyst.WTEXT) -> int:
        """
        Запросить номер файла матрицы качеств в цепочке по имени файла
        
        :param _hmap: идентификатор открытых данных
        
        :param _mtqname: имя файла матрицы качеств В цепочке номера матриц качеств начинаются с ``1``
        
        :returns: При отсутствии файла матрицы качеств в цепочке возвращает ноль
        :rtype: int
        """
        return mapGetMtqNumberUn_t (_hmap, _mtqname.buffer())

    mapGetMtqCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqCount', maptype.HMAP)
    def mapGetMtqCount(_hmap: maptype.HMAP) -> int:
        """
        Запросить число открытых файлов матриц качеств
        
        :param _hmap: идентификатор открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqCount_t (_hmap)

    mapGetMtqSystemTime_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqSystemTime', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.SYSTEMTIME))
    def mapGetMtqSystemTime(_hmap: maptype.HMAP, _number: int, _time: ctypes.POINTER(maptype.SYSTEMTIME)) -> int:
        """
        Запросить время крайнего редактирования матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы
        
        :param _time: адрес для записи системного времени редактирования (создания) по Гринвичу
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqSystemTime_t (_hmap, _number, _time)

    mapGetMtqDescribeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqDescribeUn', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.MTRDESCRIBEUN))
    def mapGetMtqDescribeUn(_hmap: maptype.HMAP, _number: int, _describe: ctypes.POINTER(maptype.MTRDESCRIBEUN)) -> int:
        """
        Запросить описание файла матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _describe: адрес структуры, в которой будет размещено описание матрицы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqDescribeUn_t (_hmap, _number, _describe)

    mapGetMtqElementSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqElementSize', maptype.HMAP, ctypes.c_long)
    def mapGetMtqElementSize(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить размер элемента матрицы качеств в байтах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке Возвращаемое значение ``1`` соответствует типу ``"unsigned char"`` Возвращаемое значение ``2`` соответствует типу ``"short int"`` Возвращаемое значение ``4`` соответствует типу ``"int"`` Возвращаемое значение ``8`` соответствует типу ``"double"``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqElementSize_t (_hmap, _number)

    mapGetMtqMeterInElementX_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqMeterInElementX', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def mapGetMtqMeterInElementX(_hmap: maptype.HMAP, _number: int, _metinelemX: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить размер элемента матрицы в метрах по оси X
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _metinelemX: размер элемента матрицы в метрах на местности по оси X
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqMeterInElementX_t (_hmap, _number, _metinelemX)

    mapGetMtqMeterInElementY_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqMeterInElementY', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def mapGetMtqMeterInElementY(_hmap: maptype.HMAP, _number: int, _metinelemY: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить размер элемента матрицы в метрах по оси Y
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _metinelemY: размер элемента матрицы в метрах на местности по оси Y
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqMeterInElementY_t (_hmap, _number, _metinelemY)

    mapGetMtqView_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqView', maptype.HMAP, ctypes.c_long)
    def mapGetMtqView(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить отображение (степень видимости) матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Возвращает: ``0`` - не отображать ``1`` - полная ``2`` - насыщенная ``3`` - полупрозрачная ``4`` - средняя ``5`` - прозрачная
        :rtype: int
        """
        return mapGetMtqView_t (_hmap, _number)

    mapSetMtqView_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtqView', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetMtqView(_hmap: maptype.HMAP, _number: int, _view: int) -> int:
        """
        Установить отображение матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _view: степень видимости матрицы: ``0`` - не отображать ``1`` - полная ``2`` - насыщенная ``3`` - полупрозрачная ``4`` - средняя ``5`` - прозрачная
        """
        return mapSetMtqView_t (_hmap, _number, _view)

    mapGetMtqViewOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqViewOrder', maptype.HMAP, ctypes.c_long)
    def mapGetMtqViewOrder(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить порядок отображения матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqViewOrder_t (_hmap, _number)

    mapSetMtqViewOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtqViewOrder', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetMtqViewOrder(_hmap: maptype.HMAP, _number: int, _order: int) -> int:
        """
        Установить порядок отображения матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _order: порядок отображения: ``0`` - под картой, ``1`` - над картой
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtqViewOrder_t (_hmap, _number, _order)

    mapChangeOrderMtqShow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapChangeOrderMtqShow', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapChangeOrderMtqShow(_hmap: maptype.HMAP, _oldnumber: int, _newnumber: int) -> int:
        """
        Поменять очередность отображения матриц (mtq) в цепочке
        
        :param _hmap: идентификатор открытых данных
        
        :param _oldnumber: номер файла в цепочке
        
        :param _newnumber: устанавливаемый номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapChangeOrderMtqShow_t (_hmap, _oldnumber, _newnumber)

    mapGetMtqShadow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqShadow', maptype.HMAP, ctypes.c_long)
    def mapGetMtqShadow(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить тень матрицы качества
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Возвращает: ``1`` - тень есть, ``0`` - нет тени При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqShadow_t (_hmap, _number)

    mapSetMtqShadow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtqShadow', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetMtqShadow(_hmap: maptype.HMAP, _number: int, _value: int) -> int:
        """
        Установить тень матрицы качества
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _value: флаг наложения тени (``1`` - тень есть, ``0`` - нет тени)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtqShadow_t (_hmap, _number, _value)

    mapCreateMtqUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateMtqUn', maptype.PWCHAR, ctypes.POINTER(maptype.BUILDMTW), ctypes.POINTER(maptype.MTRPROJECTIONDATA), ctypes.POINTER(maptype.COLORREF), ctypes.c_int)
    def mapCreateMtqUn(_mtqname: mapsyst.WTEXT, _parm: ctypes.POINTER(maptype.BUILDMTW), _projectiondata: ctypes.POINTER(maptype.MTRPROJECTIONDATA), _palette: ctypes.POINTER(maptype.COLORREF), _countpalette: int) -> maptype.HMAP:
        """
        Создать матрицу качеств
        
        :param _mtqname: имя файла создаваемой матрицы
        
        :param _parm: параметры создания матрицы mtrprojectiondata - параметры проекции
        
        :param _palette: указатель на палитру
        
        :param _countpalette: количество цветов в палитре
        
        :returns: Возвращает идентификатор открытой матричной карты Структуры BUILDMTW, MTRPROJECTIONDATA описаны в maptype.h При ошибке возвращает ноль
        :rtype: maptype.HMAP
        """
        return mapCreateMtqUn_t (_mtqname.buffer(), _parm, _projectiondata, _palette, _countpalette)

    mapPutMtqFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPutMtqFrame', maptype.HMAP, ctypes.c_long, ctypes.c_char_p, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapPutMtqFrame(_hmap: maptype.HMAP, _number: int, _bits: ctypes.c_char_p, _left: int, _top: int, _width: int, _height: int, _beginning: int) -> int:
        """
        Записать прямоугольный участок матрицы качеств из памяти
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке.
        
        :param _bits: адрес логического начала записываемого участка (смотреть параметр  beginning)
        
        :param _left: смещение участка матрицы слева (в элементах)
        
        :param _top: смещение участка матрицы сверху (в элементах)
        
        :param _width: ширина участка матрицы (в элементах)
        
        :param _height: высота участка матрицы (в элементах)
        
        :param _beginning: определяет, на какую строку указывает bits : ``0`` - bits указывает на начало верхней строки выводимого участка ``1`` - bits указывает на начало нижней строки выводимого участка Размер участка, заданного адресом bits, должен быть не менее (width ``*`` height ``*`` размер элемента матрицы в байтах), в противном случае возможны ошибки работы с памятью Запрос размера элемента матрицы качеств в байтах - функция mapGetMtqElementSize Значения элементов участка матрицы в области bits должны быть записаны в единицах измерения значений данной матрицы качеств Запрос единицы измерения значений матрицы качеств - функция mapGetMtqMeasure
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPutMtqFrame_t (_hmap, _number, _bits, _left, _top, _width, _height, _beginning)

    mapSetMtqPseudoCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtqPseudoCode', maptype.HMAP, ctypes.c_long, ctypes.c_double)
    def mapSetMtqPseudoCode(_hmap: maptype.HMAP, _number: int, _value: float) -> int:
        """
        Установить значение псевдокода матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _value: значение псевдокода
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtqPseudoCode_t (_hmap, _number, _value)

    mapGetMtqCompressNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqCompressNumber', maptype.HMAP, ctypes.c_long)
    def mapGetMtqCompressNumber(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить флаг сжатия матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqCompressNumber_t (_hmap, _number)

    mapSetMtqCompressNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtqCompressNumber', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetMtqCompressNumber(_hmap: maptype.HMAP, _number: int, _compressnumber: int) -> int:
        """
        Занести в матрицу качеств номер алгоритма сжатия блоков
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _compressnumber: номер алгоритма сжатия блоков
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtqCompressNumber_t (_hmap, _number, _compressnumber)

    mapSetMtqShowRange_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtqShowRange', maptype.HMAP, ctypes.c_long, ctypes.c_double, ctypes.c_double)
    def mapSetMtqShowRange(_hmap: maptype.HMAP, _number: int, _minvalue: float, _maxvalue: float) -> int:
        """
        Установить диапазон отображаемых элементов матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы качеств в цепочке открытых матриц качеств
        
        :param _minvalue: минимальное включаемое значение границы диапазона отображаемых элементов матрицы качеств
        
        :param _maxvalue: максимальное включаемое значение границы диапазона отображаемых элементов матрицы качеств
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtqShowRange_t (_hmap, _number, _minvalue, _maxvalue)

    mapSetMtqViewOutRange_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtqViewOutRange', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSetMtqViewOutRange(_hmap: maptype.HMAP, _number: int, _viewup: int, _viewdown: int) -> int:
        """
        Установить флаги отображения элементов матрицы качеств вне границ диапазона, заданного в mapSetMtqShowRange
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы качеств в цепочке открытых матриц качеств
        
        :param _viewup: отображать элементы, значения которых больше верхней границы диапазона (параметр maxvalue функции mapSetMtqShowRange)
        
        :param _viewdown: отображать элементы, значения которых меньше нижней границы диапазона (параметр minvalue функции mapSetMtqShowRange)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtqViewOutRange_t (_hmap, _number, _viewup, _viewdown)

    mapGetMtqPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqPalette', maptype.HMAP, ctypes.POINTER(maptype.COLORREF), ctypes.c_long, ctypes.c_long)
    def mapGetMtqPalette(_hmap: maptype.HMAP, _palette: ctypes.POINTER(maptype.COLORREF), _count: int, _number: int) -> int:
        """
        Запросить описание палитры матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _palette: адрес области для размещения палитры
        
        :param _count: число считываемых элементов палитры (размер области в байтах / ``4``)
        
        :param _number: номер матрицы в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqPalette_t (_hmap, _palette, _count, _number)

    mapGetMtqStandardPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqStandardPalette', maptype.HMAP, ctypes.POINTER(maptype.COLORREF), ctypes.c_long, ctypes.c_long)
    def mapGetMtqStandardPalette(_hmap: maptype.HMAP, _palette: ctypes.POINTER(maptype.COLORREF), _count: int, _number: int) -> int:
        """
        Запросить эталонную палитру матрицы качеств (без учета яркости и контрастности)
        
        :param _hmap: идентификатор открытых данных
        
        :param _palette: адрес области для размещения палитры
        
        :param _count: число считываемых элементов палитры (размер области в байтах / ``4``)
        
        :param _number: номер матрицы в цепочке.
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqStandardPalette_t (_hmap, _palette, _count, _number)

    mapSetMtqPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtqPalette', maptype.HMAP, ctypes.POINTER(maptype.COLORREF), ctypes.c_long, ctypes.c_long)
    def mapSetMtqPalette(_hmap: maptype.HMAP, _palette: ctypes.POINTER(maptype.COLORREF), _count: int, _number: int) -> int:
        """
        Установить описание палитры матрицы качеств и сохранить в файле (синонимы)
        
        :param _hmap: идентификатор открытых данных
        
        :param _palette: адрес устанавливаемой палитры
        
        :param _count: число элементов в новой палитре
        
        :param _number: номер матрицы в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtqPalette_t (_hmap, _palette, _count, _number)

    mapSetMtqPaletteDiapason_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtqPaletteDiapason', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.c_long, ctypes.c_long)
    def mapSetMtqPaletteDiapason(_hmap: maptype.HMAP, _diapason: ctypes.POINTER(ctypes.c_double), _count: int, _number: int) -> int:
        """
        Установить верхние значения диапазонов неравномерной палитры матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _diapason: адрес массива устанавливаемых значений диапазонов
        
        :param _count: число элементов в массиве значений диапазонов
        
        :param _number: номер матрицы в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtqPaletteDiapason_t (_hmap, _diapason, _count, _number)

    mapUnsetMtqPaletteDiapason_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUnsetMtqPaletteDiapason', maptype.HMAP, ctypes.c_long)
    def mapUnsetMtqPaletteDiapason(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Удалить верхние значения диапазонов неравномерной палитры матрицы качеств (палитра становится равномерной)
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUnsetMtqPaletteDiapason_t (_hmap, _number)

    mapGetMtqPaletteDiapason_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqPaletteDiapason', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_long, ctypes.c_long)
    def mapGetMtqPaletteDiapason(_hmap: maptype.HMAP, _minimum: ctypes.POINTER(ctypes.c_double), _diapason: ctypes.POINTER(ctypes.c_double), _count: int, _number: int) -> int:
        """
        Запросить верхние значения диапазонов неравномерной палитры и минимальное значение элемента матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _minimum: минимальное значение элемента матрицы (результат запроса)
        
        :param _diapason: адрес массива верхних значений диапазонов (результат запроса)
        
        :param _count: число элементов в массиве значений диапазонов
        
        :param _number: номер матрицы в цепочке
        
        :returns: При ошибке и при неустановленных верхних значениях диапазонов возвращает ноль
        :rtype: int
        """
        return mapGetMtqPaletteDiapason_t (_hmap, _minimum, _diapason, _count, _number)

    mapSetMtqTwoIntervalPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtqTwoIntervalPalette', maptype.HMAP, maptype.COLORREF, maptype.COLORREF, maptype.COLORREF, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSetMtqTwoIntervalPalette(_hmap: maptype.HMAP, _firstcolor: maptype.COLORREF, _mediumcolor: maptype.COLORREF, _lastcolor: maptype.COLORREF, _count: int, _mediumposition: int, _number: int) -> int:
        """
        Установить и сохранить описание двухинтервальной палитры матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _firstcolor: адрес начального цвета первого интервала
        
        :param _mediumcolor: адрес промежуточного цвета (конечного первого интервала, начального второго интервала)
        
        :param _lastcolor: адрес конечного цвета второго интервала
        
        :param _count: число элементов в палитре
        
        :param _mediumposition: номер промежуточного цвета в палитре, (число от ``0`` до count``-1``)
        
        :param _number: номер матрицы в цепочке Двухинтервальная палитра формируется с использованием трёх цветов (начального, промежуточного, конечного), задающих границы двух интервалов Составляющие интенсивности цветов внутри интервала равномерно изменяются от начального цвета интервала к конечному
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtqTwoIntervalPalette_t (_hmap, _firstcolor, _mediumcolor, _lastcolor, _count, _mediumposition, _number)

    mapGetMtqBright_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqBright', maptype.HMAP, ctypes.c_long)
    def mapGetMtqBright(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить яркость палитры матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :returns: Возвращает значение яркости (-16..+16) При ошибке возвращает 0
        :rtype: int
        """
        return mapGetMtqBright_t (_hmap, _number)

    mapSetMtqBright_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtqBright', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetMtqBright(_hmap: maptype.HMAP, _number: int, _bright: int) -> int:
        """
        Установить яркость палитры матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _bright: яркость (-``16``..+``16``)
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapSetMtqBright_t (_hmap, _number, _bright)

    mapGetMtqContrast_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqContrast', maptype.HMAP, ctypes.c_long)
    def mapGetMtqContrast(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить контрастность палитры матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :returns: Возвращает значение контраста в диапазоне (-16..+16) При ошибке возвращает 0
        :rtype: int
        """
        return mapGetMtqContrast_t (_hmap, _number)

    mapSetMtqContrast_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtqContrast', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetMtqContrast(_hmap: maptype.HMAP, _number: int, _contrast: int) -> int:
        """
        Установить контрастность палитры матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _contrast: контраст (-``16``..+``16``)
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapSetMtqContrast_t (_hmap, _number, _contrast)

    mapGetMtqPaletteCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqPaletteCount', maptype.HMAP, ctypes.c_long)
    def mapGetMtqPaletteCount(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить число цветов в палитре матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapGetMtqPaletteCount_t (_hmap, _number)

    mapGetMtqColorDescEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqColorDescEx', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.MTRCOLORDESCEX))
    def mapGetMtqColorDescEx(_hmap: maptype.HMAP, _number: int, _colornumber: int, _colordesc: ctypes.POINTER(maptype.MTRCOLORDESCEX)) -> int:
        """
        Запросить описание диапазона значений матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _colornumber: номер диапазона значений
        
        :param _colordesc: адрес структуры, в которой будет размещено описание диапазона значений
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqColorDescEx_t (_hmap, _number, _colornumber, _colordesc)

    mapSetMtqColor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtqColor', maptype.HMAP, ctypes.c_long, ctypes.c_long, maptype.COLORREF)
    def mapSetMtqColor(_hmap: maptype.HMAP, _number: int, _colornumber: int, _color: maptype.COLORREF) -> int:
        """
        Установить цвет диапазона значений элементов матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _colornumber: номер диапазона значений
        
        :param _color: цвет для диапазона
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtqColor_t (_hmap, _number, _colornumber, _color)

    mapGetMtqValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetMtqValue', maptype.HMAP, ctypes.c_long, ctypes.c_double, ctypes.c_double)
    def mapGetMtqValue(_hmap: maptype.HMAP, _number: int, _x: float, _y: float) -> float:
        """
        Запросить значение в заданной точке из матрицы с номером number в цепочке
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _x: координата Х точки в метрах в системе координат документа
        
        :param _y: координата Y точки в метрах в системе координат документа
        
        :returns: Возвращает значение элемента с учётом единицы измерения Возвращаемое значение равно значению элемента из файла матрицы, делённому на 10 в степени n, где n = mapGetMtqMeasure() В случае ошибки при выборе значения и в случае необеспеченности заданной точки матричными данными возвращает ERRORHEIGHT  (``-111111.0``)
        :rtype: float
        """
        return mapGetMtqValue_t (_hmap, _number, _x, _y)

    mapGetMtqValuePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetMtqValuePro', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), maptype.HPAINT)
    def mapGetMtqValuePro(_hmap: maptype.HMAP, _number: int, _interptype: int, _x: float, _y: float, _value: ctypes.POINTER(ctypes.c_double), _hpaint: maptype.HPAINT) -> float:
        """
        Запросить интерполированное значение из матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы качеств в цепочке
        
        :param _interptype: тип интерполяции: ``1`` - ближайший сосед ``2`` - интерполяция по ближайшим ``3`` элементам ``3`` - билинейная интерполяция по ``4`` ближайшим элементам ``4`` - бикубическая интерполяция по ``16`` ближайшим элементам
        
        :param _x: координата Х точки в метрах в системе координат документа
        
        :param _y: координата Y точки в метрах в системе координат документа
        
        :param _value: возвращаемое значение, при ошибке устанавливается ``ERRORHEIGHT`` (``-111111.0``)
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций, создается функцией mapCreatePaintControl, освобождается - mapFreePaintControl
        
        :returns: При ошибке возвращает 0
        :rtype: float
        """
        return mapGetMtqValuePro_t (_hmap, _number, _interptype, _x, _y, _value, _hpaint)

    mapGetMtqPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqPoint', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_double), ctypes.c_long, ctypes.c_long)
    def mapGetMtqPoint(_hmap: maptype.HMAP, _number: int, _value: ctypes.POINTER(ctypes.c_double), _string: int, _column: int) -> int:
        """
        Запросить элемент матрицы качеств по абсолютным индексам
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _value: полученное значение элемента в метрах
        
        :param _string: индекс строки матрицы (значение от ``0`` до height``-1``, где height - высота матрицы элементах, запрашиваемая функцией mapGetMtqHeightInElement)
        
        :param _column: индекс колонки матрицы (значение от ``0`` до width``-1``, где width - ширина матрицы элементах, запрашиваемая функцией mapGetMtqWidthInElement)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqPoint_t (_hmap, _number, _value, _string, _column)

    mapPutMtqValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPutMtqValue', maptype.HMAP, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    def mapPutMtqValue(_hmap: maptype.HMAP, _number: int, _x: float, _y: float, _h: float) -> int:
        """
        Установить значение в элемент матрицы, соответствующий заданной точке
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке x, y   - координаты точки в метрах в системе документа
        
        :param _x: координата Х точки в метрах в системе координат документа
        
        :param _y: координата Y точки в метрах в системе координат документа В матрицу заносится значение элемента с учётом единицы измерения Заносимое значение равно h, умноженному на ``10`` в степени n, где n = mapGetMtqMeasure().
        
        :returns: В случае ошибки возвращает ноль
        :rtype: int
        """
        return mapPutMtqValue_t (_hmap, _number, _x, _y, _h)

    mapGetActualMtqFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetActualMtqFrame', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.c_long)
    def mapGetActualMtqFrame(_hmap: maptype.HMAP, _frame: ctypes.POINTER(maptype.DFRAME), _number: int) -> int:
        """
        Запросить фактические габариты матрицы в метрах в районе работ
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _frame: адрес для размещения результата При отображение матрицы по рамке возвращаются габариты рамки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetActualMtqFrame_t (_hmap, _frame, _number)

    mapGetMtqScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqScale', maptype.HMAP, ctypes.c_long)
    def mapGetMtqScale(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить масштаб матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqScale_t (_hmap, _number)

    mapIsMtqGeoSupported_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsMtqGeoSupported', maptype.HMAP, ctypes.c_long)
    def mapIsMtqGeoSupported(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить поддерживается ли пересчет к геодезическим координатам из плоских прямоугольных и обратно
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: Если нет - возвращает ноль
        :rtype: int
        """
        return mapIsMtqGeoSupported_t (_hmap, _number)

    mapGetMtqProjectionDataPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqProjectionDataPro', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapGetMtqProjectionDataPro(_hmap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: ctypes.POINTER(ctypes.c_long), _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        """
        Запросить данные о проекции матричных данных
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _mapregister: адрес структуры, в которой будут размещены данные о системе координат
        
        :param _datumparam: адрес структуры, в которой будут размещены коэффициенты трансформирования геодезических координат
        
        :param _ellipsoidparam: адрес структуры, в которой будут размещены данные о параметрах эллипсоида
        
        :param _ttype: тип локального преобразования координат (``TRANSFORMTYPE`` в mapcreat.h) или ``0``
        
        :param _tparm: параметры локального преобразования координат Структуры ``MAPREGISTEREX``, ``DATUMPARAM``, ``ELLIPSOIDPARAM``, ``LOCALTRANSFORM`` описаны в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqProjectionDataPro_t (_hmap, _number, _mapregister, _datumparam, _ellipsoidparam, _ttype, _tparm)

    mapSetMtqProjectionDataPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtqProjectionDataPro', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_long, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapSetMtqProjectionDataPro(_hmap: maptype.HMAP, _number: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        """
        Установить данные о системе координат матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _mapregister: адрес структуры, содержащей данные о системе координат
        
        :param _datumparam: адрес структуры, содержащей коэффициенты трансформирования геодезических координат
        
        :param _ellipsoidparam: адрес структуры, содержащей параметры эллипсоида
        
        :param _ttype: тип локального преобразования координат (``TRANSFORMTYPE`` в mapcreat.h) или ``0``
        
        :param _tparm: параметры локального преобразования координат Структуры ``MAPREGISTEREX``, ``DATUMPARAM``, ``ELLIPSOIDPARAM``, ``LOCALTRANSFORM`` описаны в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtqProjectionDataPro_t (_hmap, _number, _mapregister, _datumparam, _ellipsoidparam, _ttype, _tparm)

    mapGetMtqEllipsoidParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqEllipsoidParam', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapGetMtqEllipsoidParam(_hmap: maptype.HMAP, _number: int, _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        """
        Запросить параметры эллипсоида матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла матрицы в цепочке
        
        :param _ellipsoidparam: адрес структуры, в которой будут размещены параметры эллипсоида Структурa ``ELLIPSOIDPARAM`` описанa в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqEllipsoidParam_t (_hmap, _number, _ellipsoidparam)

    mapSetMtqEllipsoidParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtqEllipsoidParam', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapSetMtqEllipsoidParam(_hmap: maptype.HMAP, _number: int, _ellipsoidparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        """
        Установить параметры эллипсоида матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла матрицы в цепочке.
        
        :param _ellipsoidparam: адрес структуры, содержащей параметры эллипсоида Структурa ``ELLIPSOIDPARAM`` описанa в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtqEllipsoidParam_t (_hmap, _number, _ellipsoidparam)

    mapGetMtqDatumParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqDatumParam', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapGetMtqDatumParam(_hmap: maptype.HMAP, _number: int, _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        """
        Запросить коэффициенты трансформирования геодезических координат матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла матрицы в цепочке
        
        :param _datumparam: адрес структуры, в которой будут размещены коэффициенты трансформирования геодезических координат Структурa ``DATUMPARAM`` описанa в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqDatumParam_t (_hmap, _number, _datumparam)

    mapSetMtqDatumParam_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtqDatumParam', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapSetMtqDatumParam(_hmap: maptype.HMAP, _number: int, _datumparam: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        """
        Установить коэффициенты трансформирования геодезических координат матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла матрицы в цепочке
        
        :param _datumparam: адрес структуры, содержащей коэффициенты трансформирования геодезических координат Структурa ``DATUMPARAM`` описанa в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtqDatumParam_t (_hmap, _number, _datumparam)

    mapGetMtqFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqFrame', maptype.HMAP, ctypes.c_long, ctypes.c_char_p, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapGetMtqFrame(_hmap: maptype.HMAP, _number: int, _bits: ctypes.c_char_p, _left: int, _top: int, _width: int, _height: int, _widthinbyte: int) -> int:
        """
        Прочитать прямоугольного участка матрицы качеств в заданную область памяти
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _bits: указатель на начало области памяти
        
        :param _left: смещение участка матрицы слева (в элементах)
        
        :param _top: смещение участка матрицы сверху (в элементах)
        
        :param _width: ширина участка матрицы (в элементах)
        
        :param _height: высота участка матрицы (в элементах)
        
        :param _widthinbyte: ширинa участка матрицы в байтах Размер участка, заданного адресом bits, должен быть не менее (width ``*`` height ``*`` размер элемента матрицы в байтах), в противном случае возможны ошибки работы с памятью Запрос размера элемента матрицы качеств в байтах - функция mapGetMtqElementSize. Значения элементов участка матрицы записываются в область bits в единицах измерения значений данной матрицы качеств Запрос единицы измерения значений матрицы качеств - функция mapGetMtqMeasure.
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqFrame_t (_hmap, _number, _bits, _left, _top, _width, _height, _widthinbyte)

    mapGetMtqMeasure_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqMeasure', maptype.HMAP, ctypes.c_long)
    def mapGetMtqMeasure(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить единицу измерения значений матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке Значение элемента в файле матрицы равно значению качества, умноженному на ``10`` в степени n, где n - единица измерения
        
        :returns: Функция возвращает значение поля Unit структуры параметров создания матрицы BUILDMTW Возвращаемые значения: ``0`` - метры, ``1`` - дециметры, ``2`` - сантиметры, ``3`` - миллиметры При ошибке возвращает -1
        :rtype: int
        """
        return mapGetMtqMeasure_t (_hmap, _number)

    mapBuildFloodZoneUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBuildFloodZoneUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.XYHDOUBLE), ctypes.c_long, ctypes.c_double, ctypes.c_double, maptype.HWND)
    def mapBuildFloodZoneUn(_hmap: maptype.HMAP, _mtqname: mapsyst.WTEXT, _pointarray: ctypes.POINTER(maptype.XYHDOUBLE), _pointcount: int, _areaextension: float, _mindepth: float, _handle: maptype.HWND) -> int:
        """
        Построить зону затопления по набору отметок уровня воды
        
        :param _hmap: исходная карта с матрицей высот для построения зоны затопления
        
        :param _mtqname: полное имя создаваемой матрицы качеств
        
        :param _pointarray: адрес массива точек с отметками уровня воды координаты точек (pointarray->X,pointarray->Y) и значения уровня (pointarray->H) задаются в метрах в системе координат документа уровень воды (pointarray->H) задаётся величиной относительно поверхности рельефа
        
        :param _pointcount: число точек в массиве pointarray
        
        :param _areaextension: положительное число, задающее величину расширения габаритов области в метрах
        
        :param _mindepth: положительное число, задающее минимальную глубину зоны затопления в метрах (глубины, меньшие mindepth в матрицу качеств не заносятся)
        
        :param _handle: идентификатор окна диалога, которому посылаются сообщения о ходе процесса : ``0x0581`` - сообщение о проценте выполненных работ (в ``WPARAM``), если процесс должен быть принудительно завершен, в ответ должно вернуться значение ``0x0581`` ``0`` - сообщения не посылаются Размер в байтах массива, заданного адресом pointarray, должен быть не менее pointCount ``*`` sizeof(``XYHDOUBLE``), в противном случае возможны ошибки работы с памятью В результате построения формируется матрица качеств, элементы которой содержат глубины в зоне затопления
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Габариты матрицы качеств определяются координатами точек с отметками уровня воды (массив pointarray)
           и величиной расширения габаритов области (areaextension)
        """
        return mapBuildFloodZoneUn_t (_hmap, _mtqname.buffer(), _pointarray, _pointcount, _areaextension, _mindepth, _handle)

    mapBuildFloodZoneAbsUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBuildFloodZoneAbsUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.XYHDOUBLE), ctypes.c_long, ctypes.c_double, ctypes.c_double, maptype.HWND)
    def mapBuildFloodZoneAbsUn(_hmap: maptype.HMAP, _mtqname: mapsyst.WTEXT, _pointarray: ctypes.POINTER(maptype.XYHDOUBLE), _pointcount: int, _areaextension: float, _mindepth: float, _handle: maptype.HWND) -> int:
        """
        Построить зону затопления по набору отметок уровня воды
        
        :param _hmap: исходная карта с матрицей высот для построения зоны затопления
        
        :param _mtqname: полное имя создаваемой матрицы качеств
        
        :param _pointarray: адрес массива точек с отметками уровня воды координаты точек (pointarray->X,pointarray->Y) и значения уровня (pointarray->H) задаются в метрах в системе координат документа уровень воды (pointarray->H) задаётся абсолютным значением высоты
        
        :param _pointcount: число точек в массиве pointarray
        
        :param _areaextension: положительное число, задающее величину расширения габаритов области в метрах
        
        :param _mindepth: положительное число, задающее минимальную глубину зоны затопления в метрах (глубины, меньшие mindepth в матрицу качеств не заносятся)
        
        :param _handle: идентификатор окна диалога, которому посылаются сообщения о ходе процесса: ``0x0581`` - сообщение о проценте выполненных работ (в ``WPARAM``), если процесс должен быть принудительно завершен, в ответ должно вернуться значение ``0x0581`` ``0`` - сообщения не посылаются Размер в байтах массива, заданного адресом pointarray, должен быть не менее pointCount ``*`` sizeof(``XYHDOUBLE``), в противном случае возможны ошибки работы с памятью Уровень воды (pointarray->H) задаётся величиной относительно поверхности рельефа В результате построения формируется матрица качеств, элементы которой содержат глубины в зоне затопления
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Габариты матрицы качеств определяются координатами точек с отметками уровня воды (массив pointarray)
           и величиной расширения габаритов области (areaextension)
        """
        return mapBuildFloodZoneAbsUn_t (_hmap, _mtqname.buffer(), _pointarray, _pointcount, _areaextension, _mindepth, _handle)

    mapBuildMtqUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBuildMtqUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.COLORREF), ctypes.c_long, ctypes.POINTER(maptype.XYHDOUBLE), ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_double, maptype.HWND)
    def mapBuildMtqUn(_hmap: maptype.HMAP, _mtqname: mapsyst.WTEXT, _palette: ctypes.POINTER(maptype.COLORREF), _countpalette: int, _pointarray: ctypes.POINTER(maptype.XYHDOUBLE), _pointcount: int, _elemsizemeters: float, _minvalue: float, _maxvalue: float, _handle: maptype.HWND) -> int:
        """
        Построить матрицу качеств по массиву значений характеристики качества
        
        :param _hmap: идентификатор открытой исходной карты для построения матрицы качеств
        
        :param _mtqname: полное имя создаваемой матрицы качеств
        
        :param _palette: адрес палитры создаваемой матрицы качеств, если palette равно нулю - используется палитра по умолчанию
        
        :param _countpalette: количество цветов в палитре
        
        :param _pointarray: адрес массива значений характеристики качества Координаты точек (pointarray->X,pointarray->Y) задаются в метрах в системе координат документа
        
        :param _pointcount: число точек в массиве pointarray Размер в байтах массива, заданного адресом pointarray, должен быть не менее pointCount ``*`` sizeof(``XYHDOUBLE``), в противном случае возможны ошибки работы с памятью
        
        :param _elemsizemeters: размер стороны элементарного участка в метрах на местности (дискрет матрицы)
        
        :param _minvalue: минимальное значение характеристики качества создаваемой матрицы качеств
        
        :param _maxvalue: максимальное значение характеристики качества создаваемой матрицы качеств если minValue >= maxValue - в матрицу заносится фактический диапазон значений из массива pointarray
        
        :param _handle: идентификатор окна диалога, которому посылаются сообщения о ходе процесса: ``0x0581`` - сообщение о проценте выполненных работ (в ``WPARAM``) если процесс должен быть принудительно завершен, в ответ должно вернуться значение ``0x0581`` если handle равно нулю - сообщения не посылаются
        
        :returns: При ошибке возвращает ноль.
        :rtype: int
        """
        return mapBuildMtqUn_t (_hmap, _mtqname.buffer(), _palette, _countpalette, _pointarray, _pointcount, _elemsizemeters, _minvalue, _maxvalue, _handle)

    mapMakeMtqPalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapMakeMtqPalette', ctypes.POINTER(maptype.COLORREF), ctypes.POINTER(maptype.COLORREF), ctypes.c_long, ctypes.c_long)
    def mapMakeMtqPalette(_skeletpalette: ctypes.POINTER(maptype.COLORREF), _resultpalette: ctypes.POINTER(maptype.COLORREF), _resultcolorcount: int, _smoothcolormodification: int) -> int:
        """
        Сформировать палитру матрицы качеств
        
        :param _skeletpalette: исходная (скелетная) палитра, массив размером sizeof(``COLORREF``) ``*256`` , содержащий граничные цвета интервалов, разделённые пустыми элементами (значение ``0xFFFFFFFF``)
        
        :param _resultpalette: результирующая палитра, массив размером sizeof(``COLORREF``) ``*256``
        
        :param _resultcolorcount: количество формируемых цветов результирующей палитры (не более ``256``)
        
        :param _smoothcolormodification: флаг плавного изменения цветов результирующей палитры: ``0`` - внутренние цвета интервала повторяют начальный цвет интервала ``1`` - составляющие интенсивности внутренних цветов интервала равномерно изменяются от начального цвета интервала к конечному Для формирования результирующей палитры (resultpalette) используется исходная палитра (skeletpalette), количество цветов результирующей палитры (resultcolorcount) и флаг плавного изменения цветов (smoothcolormodification) Цвета исходной палитры переносятся в соответствующие позиции результирующей палитры, остальные цвета результирующей палитры заполняются поинтервально в зависимости от значения флага smoothColorModification
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapMakeMtqPalette_t (_skeletpalette, _resultpalette, _resultcolorcount, _smoothcolormodification)

    mapBuildMatrixSurfaceUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBuildMatrixSurfaceUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.BUILDSURFACE))
    def mapBuildMatrixSurfaceUn(_hmap: maptype.HMAP, _mtrname: mapsyst.WTEXT, _mtrparm: ctypes.POINTER(maptype.BUILDSURFACE)) -> int:
        """
        Построить матрицу поверхности (матрицы качеств или матрицы высот) по данным векторной карты
        
        :param _hmap: идентификатор открытых данных
        
        :param _mtrname: полное имя создаваемой матрицы
        
        :param _mtrparm: параметры создаваемой матрицы (структура ``BUILDSURFACE`` описана в maptype.h)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если mtrparm->FileMtw равно 1, то строится матрица высот (``*.mtw``), иначе строится матрица качеств (``*.mtq``)
        """
        return mapBuildMatrixSurfaceUn_t (_hmap, _mtrname.buffer(), _mtrparm)

    mapDeleteMtq_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteMtq', maptype.HMAP, ctypes.c_long)
    def mapDeleteMtq(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Удалить матрицу качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteMtq_t (_hmap, _number)

    mapGetShowMtqByBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetShowMtqByBorder', maptype.HMAP, ctypes.c_long)
    def mapGetShowMtqByBorder(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Определить способ отображения матрицы (относительно рамки)
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :returns: Возвращает: ``1`` - при отображении матрицы по рамке ``0`` - при отображении матрицы без учета рамки
        :rtype: int
        """
        return mapGetShowMtqByBorder_t (_hmap, _number)

    mapGetExistenceMtqBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetExistenceMtqBorder', maptype.HMAP, ctypes.c_long)
    def mapGetExistenceMtqBorder(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Определить существование рамки матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :returns: Если рамка матрицы существует возвращает 1, иначе возвращает 0
        :rtype: int
        """
        return mapGetExistenceMtqBorder_t (_hmap, _number)

    mapSetShowMtqByBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetShowMtqByBorder', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetShowMtqByBorder(_hmap: maptype.HMAP, _number: int, _value: int) -> int:
        """
        Установить отображение матрицы по рамке
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _value: отображение матрицы по рамке: ``1`` - отобразить матрицу по рамке ``0`` - отобразить матрицу без учета рамки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetShowMtqByBorder_t (_hmap, _number, _value)

    mapGetMtqRangeScaleVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqRangeScaleVisible', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapGetMtqRangeScaleVisible(_hmap: maptype.HMAP, _number: int, _bottomscale: ctypes.POINTER(ctypes.c_long), _topscale: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить значения масштаба нижней и верхней границ видимости матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _bottomscale: адрес для записи знаменателя масштаба нижней границы видимости матрицы
        
        :param _topscale: адрес для записи знаменателя масштаба верхней границы видимости матрицы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqRangeScaleVisible_t (_hmap, _number, _bottomscale, _topscale)

    mapSetMtqRangeScaleVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtqRangeScaleVisible', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSetMtqRangeScaleVisible(_hmap: maptype.HMAP, _number: int, _bottomscale: int, _topscale: int) -> int:
        """
        Установить значения масштаба нижней и верхней границ видимости матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _bottomscale: знаменатель масштаба нижней границы видимости матрицы
        
        :param _topscale: знаменатель масштаба верхней границы видимости матрицы
        
        :returns: bottomscale <= topscale, иначе возвращает 0 При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtqRangeScaleVisible_t (_hmap, _number, _bottomscale, _topscale)

    mapGetImmediatePointOfMtqBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetImmediatePointOfMtqBorder', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetImmediatePointOfMtqBorder(_hMap: maptype.HMAP, _number: int, _pointin: ctypes.POINTER(maptype.DOUBLEPOINT), _pointout: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Определить координаты и порядковый номер точки рамки, которая входит в прямоугольник Габариты растра (матрицы)
        
        :param _hMap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _pointin: координаты точки в метрах в системе документа
        
        :param _pointout: адрес для записи координат найденной точки в метрах в системе документа Определяется точка рамки, которая имеет наименьшее удаление от точки pointin
        
        :returns: При ошибке или отсутствии рамки возвращает 0
        :rtype: int
        """
        return mapGetImmediatePointOfMtqBorder_t (_hMap, _number, _pointin, _pointout)

    mapGetSouthWestMtqPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSouthWestMtqPlane', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGetSouthWestMtqPlane(_hmap: maptype.HMAP, _number: int, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить координаты юго-западного угла матрицы в метрах в системе координат матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке x, y   - адреса для записи координат найденной точки в метрах
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapGetSouthWestMtqPlane_t (_hmap, _number, _x, _y)

    mapGetActiveMtq_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetActiveMtq', maptype.HMAP)
    def mapGetActiveMtq(_hmap: maptype.HMAP) -> int:
        """
        Запросить активную матрицу (устанавливается приложением по своему усмотрению)
        
        :param _hmap: идентификатор открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetActiveMtq_t (_hmap)

    mapSetActiveMtq_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetActiveMtq', maptype.HMAP, ctypes.c_long)
    def mapSetActiveMtq(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Установить активную матрицу (устанавливается приложением по своему усмотрению)
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetActiveMtq_t (_hmap, _number)

    mapIsOpenMtq_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsOpenMtq', maptype.HMAP, ctypes.c_int)
    def mapIsOpenMtq(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить открыта ли матрица с номером "number"
        
        :param _hmap: идентификатор открытых данных
        
        :returns: Функция возвращает признак открытия указанной матрицы в документе - (1 / 0) При ошибке возвращает ноль.
        :rtype: int
        """
        return mapIsOpenMtq_t (_hmap, _number)

    mapGetMtqEdit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqEdit', maptype.HMAP, ctypes.c_long)
    def mapGetMtqEdit(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить флаг редактируемости матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqEdit_t (_hmap, _number)

    mapGetMtqCopyFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqCopyFlag', maptype.HMAP, ctypes.c_long)
    def mapGetMtqCopyFlag(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить - может ли матрица копироваться или экспортироваться
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqCopyFlag_t (_hmap, _number)

    mapGetMtqPrintFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqPrintFlag', maptype.HMAP, ctypes.c_long)
    def mapGetMtqPrintFlag(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить - может ли матрица выводиться на печать
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке Для данных, открытых на ГИС Сервере, может устанавливаться запрет вывода изображения на печать
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqPrintFlag_t (_hmap, _number)

    mapGetMtqFileSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqFileSize', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_int64))
    def mapGetMtqFileSize(_hmap: maptype.HMAP, _number: int, _fileSize: ctypes.POINTER(ctypes.c_int64)) -> int:
        """
        Запросить размер файла
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _fileSize: адрес для записи размера файла
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqFileSize_t (_hmap, _number, _fileSize)

    mapGetMtqWidthInElement_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqWidthInElement', maptype.HMAP, ctypes.c_long)
    def mapGetMtqWidthInElement(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить ширину матрицы (элементы)
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqWidthInElement_t (_hmap, _number)

    mapGetMtqHeightInElement_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqHeightInElement', maptype.HMAP, ctypes.c_long)
    def mapGetMtqHeightInElement(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить высоту матрицы (элементы)
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqHeightInElement_t (_hmap, _number)

    mapGetMtqAccuracy_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetMtqAccuracy', maptype.HMAP, ctypes.c_long)
    def mapGetMtqAccuracy(_hmap: maptype.HMAP, _number: int) -> float:
        """
        Запросить точность (метр/элем) матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapGetMtqAccuracy_t (_hmap, _number)

    mapGetMtqLocation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqLocation', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetMtqLocation(_hmap: maptype.HMAP, _number: int, _location: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Запросить привязку матрицы в метрах в системе координат документа
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _location: координаты юго-западного угла матрицы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqLocation_t (_hmap, _number, _location)

    mapSetMtqLocation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtqLocation', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSetMtqLocation(_hmap: maptype.HMAP, _number: int, _location: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Установить привязку матрицы в метрах в системе координат документа
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в списке открытых матриц
        
        :param _location: координаты юго-западного угла матрицы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtqLocation_t (_hmap, _number, _location)

    mapGetMtqFlagLocationChanged_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqFlagLocationChanged', maptype.HMAP, ctypes.c_long)
    def mapGetMtqFlagLocationChanged(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить флаг изменения привязки (метры) матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqFlagLocationChanged_t (_hmap, _number)

    mapSetMtqUserNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtqUserNameUn', maptype.HMAP, ctypes.c_long, maptype.PWCHAR)
    def mapSetMtqUserNameUn(_hmap: maptype.HMAP, _number: int, _username: mapsyst.WTEXT) -> int:
        """
        Установить условное имя матрицы качеств (имя пользователя)
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _username: имя пользователя
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMtqUserNameUn_t (_hmap, _number, _username.buffer())

    mapGetMtqUserNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqUserNameUn', maptype.HMAP, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetMtqUserNameUn(_hmap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _namesize: int) -> int:
        """
        Запросить условное имя матрицы качеств (имя пользователя)
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы в цепочке
        
        :param _name: имя матрицы качеств
        
        :param _namesize: размер строки в байтах
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapGetMtqUserNameUn_t (_hmap, _number, _name.buffer(), _namesize)

    mapGetMtqBlockRow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqBlockRow', maptype.HMAP, ctypes.c_long)
    def mapGetMtqBlockRow(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить число строк блоков матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqBlockRow_t (_hmap, _number)

    mapGetMtqBlockColumn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqBlockColumn', maptype.HMAP, ctypes.c_long)
    def mapGetMtqBlockColumn(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить число столбцов блоков матрицы
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqBlockColumn_t (_hmap, _number)

    mapGetMtqBlockSide_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqBlockSide', maptype.HMAP, ctypes.c_long)
    def mapGetMtqBlockSide(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить вертикальный размер блока матрицы в элементах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqBlockSide_t (_hmap, _number)

    mapGetMtqBlockWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqBlockWidth', maptype.HMAP, ctypes.c_long)
    def mapGetMtqBlockWidth(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить ширину блока матрицы в элементах
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqBlockWidth_t (_hmap, _number)

    mapCheckMtqBlockVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckMtqBlockVisible', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapCheckMtqBlockVisible(_hmap: maptype.HMAP, _number: int, _index: int) -> int:
        """
        Вернуть флаг отображения блока матрицы (0 - не отображается, 1- отображается, 2 - разделен рамкой)
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _index: порядковый номер (индекс) блока, index = row ``*`` blockColumnCount + col, где: row - индекс строки блоков, blockColumnCount - число столбцов блоков матрицы (функция mapGetMtqBlockColumn) col - индекс столбца блоков
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCheckMtqBlockVisible_t (_hmap, _number, _index)

    mapSetMtqBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtqBorder', maptype.HMAP, ctypes.c_long, maptype.HOBJ)
    def mapSetMtqBorder(_hmap: maptype.HMAP, _number: int, _hobj: maptype.HOBJ) -> int:
        """
        Установить рамку матрицы по метрике замкнутого объекта
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _hobj: замкнутый объект карты Замкнутый объект должен иметь не менее ``4``-х точек
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           После выполнения функции отображение матрицы ограничится заданной областью
        """
        return mapSetMtqBorder_t (_hmap, _number, _hobj)

    mapSetMtqBorderEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtqBorderEx', maptype.HMAP, ctypes.c_long, maptype.HOBJ, ctypes.c_long)
    def mapSetMtqBorderEx(_hmap: maptype.HMAP, _number: int, _hobj: maptype.HOBJ, _flagsubject: int) -> int:
        """
        Установить рамку матрицы по метрике замкнутого объекта
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _hobj: замкнутый объект карты
        
        :param _flagsubject: флаг использования подобъектов объекта при установке рамки растра (``0``/``1``) ``0`` - в качестве рамки устанавливается контур объекта ``1`` - в качестве рамки устанавливается контур объекта с подобъектами Замкнутый объект должен иметь не менее ``4``-х точек
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           После выполнения функции отображение матрицы ограничится заданной областью
        """
        return mapSetMtqBorderEx_t (_hmap, _number, _hobj, _flagsubject)

    mapGetMtqBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqBorder', maptype.HMAP, ctypes.c_long, maptype.HOBJ)
    def mapGetMtqBorder(_hmap: maptype.HMAP, _number: int, _hobj: maptype.HOBJ) -> int:
        """
        Запросить объект рамки матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _hobj: идентификатор объекта рамки матрицы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqBorder_t (_hmap, _number, _hobj)

    mapGetMtqCurrentBlockWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqCurrentBlockWidth', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapGetMtqCurrentBlockWidth(_hmap: maptype.HMAP, _number: int, _column: int) -> int:
        """
        Запросить ширину текущего блока column матрицы в элементах (с учетом усеченных блоков)
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _column: ширина текущего блока
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqCurrentBlockWidth_t (_hmap, _number, _column)

    mapGetMtqCurrentBlockHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqCurrentBlockHeight', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapGetMtqCurrentBlockHeight(_hmap: maptype.HMAP, _number: int, _row: int) -> int:
        """
        Запросить высоту текущего блока row матрицы в элементах (с учетом усеченных блоков)
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _row: высота текущего блока
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqCurrentBlockHeight_t (_hmap, _number, _row)

    mapGetMtqBlockAddress_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetMtqBlockAddress', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapGetMtqBlockAddress(_hmap: maptype.HMAP, _number: int, _row: int, _column: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить блок матрицы по номеру строки и столбца
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _row: строка блока
        
        :param _column: столбец блока Блоки последнего ряда могут иметь усеченный размер
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetMtqBlockAddress_t (_hmap, _number, _row, _column)

    mapSaveMtq_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSaveMtq', maptype.HMAP, ctypes.c_long)
    def mapSaveMtq(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Записать изменения матрицы в файл
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSaveMtq_t (_hmap, _number)

    mapDeleteMtqFileUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteMtqFileUn', maptype.PWCHAR)
    def mapDeleteMtqFileUn(_name: mapsyst.WTEXT) -> int:
        """
        Удалить файл матрицы качеств
        
        :param _name: имя матрицы качеств Функция предназначена для удаления матрицы и еe составных частей Матрица размером более 4Gb состоит из ``2``-х файлов: ``*.mtq`` и ``*.mtq.01`` Аналог функции DeleteTheFile()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteMtqFileUn_t (_name.buffer())

    mapMoveMtqFileUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapMoveMtqFileUn', maptype.PWCHAR, maptype.PWCHAR)
    def mapMoveMtqFileUn(_oldname: mapsyst.WTEXT, _newname: mapsyst.WTEXT) -> int:
        """
        Переименовать имя файла матрицы качеств
        
        :param _oldname: старое имя файла матрицы качеств
        
        :param _newname: новое имя файла матрицы качеств Функция предназначена для переименовывания матрицы и её составных частей Матрица размером более 4Gb состоит из ``2``-х файлов: ``*.mtq`` и ``*.mtq.01`` Аналог функции MoveTheFile()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapMoveMtqFileUn_t (_oldname.buffer(), _newname.buffer())

    mapCopyMtqFileUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCopyMtqFileUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapCopyMtqFileUn(_oldname: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _exist: int) -> int:
        """
        Скопировать файл матрицы качеств
        
        :param _oldname: старое имя файла матрицы качеств
        
        :param _newname: новое имя файла матрицы качеств
        
        :param _exist: флаг наличия файла Функция предназначена для копирования матрицы и её составных частей Матрица размером более 4Gb состоит из ``2``-х файлов: ``*.mtq`` и ``*.mtq.01`` Аналог функции CopyTheFile()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCopyMtqFileUn_t (_oldname.buffer(), _newname.buffer(), _exist)

    mapWriteMtqBlock_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapWriteMtqBlock', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_char_p, ctypes.c_long)
    def mapWriteMtqBlock(_hmap: maptype.HMAP, _number: int, _row: int, _column: int, _bits: ctypes.c_char_p, _sizebits: int) -> int:
        """
        Записать блок (row, column) в файл матрицы из памяти bits
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _row: строка блока
        
        :param _column: столбец блока
        
        :param _bits: указатель на начало изображения битовой области
        
        :param _sizebits: размер области bits в байтах
        
        :returns: Возвращает количество записанных байт При ошибке возвращает ноль
        :rtype: int
        """
        return mapWriteMtqBlock_t (_hmap, _number, _row, _column, _bits, _sizebits)

    mapGetMtqCurrentBlockSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqCurrentBlockSize', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapGetMtqCurrentBlockSize(_hmap: maptype.HMAP, _number: int, _row: int, _column: int) -> int:
        """
        Запросить размер текущего блока (row, column) матрицы в байтах (с учетом усеченных блоков)
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _row: строка блока
        
        :param _column: столбец блока
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMtqCurrentBlockSize_t (_hmap, _number, _row, _column)

    mapCreateMtqLegendToXML_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateMtqLegendToXML', maptype.HMAP, ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def mapCreateMtqLegendToXML(_hmap: maptype.HMAP, _number: int, _xmlname: mapsyst.WTEXT, _imgpath: mapsyst.WTEXT, _imgsize: int) -> int:
        """
        Подготовить легенду матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _xmlname: имя выходного xml-файла
        
        :param _imgpath: путь к изображениям формата png
        
        :param _imgsize: нестандартный размер изображения (сторона квадрата), если равен нулю, то будут созданы только изображения размеров 16x16, 24x24 и 32x32) Максимальный размер изображения 1024x1024 При необходимости создания изображения нестандартного размера (отличного от 16x16, 24x24 и 32x32) указать размер в параметре imgsize
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapCreateMtqLegendToXML_t (_hmap, _number, _xmlname.buffer(), _imgpath.buffer(), _imgsize)

    mapGetMtqValueName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqValueName', maptype.HMAP, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetMtqValueName(_hmap: maptype.HMAP, _number: int, _value: mapsyst.WTEXT, _size: int) -> int:
        """
        Прочитать название характеристики матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _value: адрес для записи названия характеристики
        
        :param _size: размер названия характеристики
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapGetMtqValueName_t (_hmap, _number, _value.buffer(), _size)

    mapSetMtqValueName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtqValueName', maptype.HMAP, ctypes.c_long, maptype.PWCHAR)
    def mapSetMtqValueName(_hmap: maptype.HMAP, _number: int, _value: mapsyst.WTEXT) -> int:
        """
        Записать название характеристики матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _value: название характеристики
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapSetMtqValueName_t (_hmap, _number, _value.buffer())

    mapGetMtqUnitName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtqUnitName', maptype.HMAP, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetMtqUnitName(_hmap: maptype.HMAP, _number: int, _unit: mapsyst.WTEXT, _size: int) -> int:
        """
        Прочитать название единицы измерения матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _unit: адрес для записи названия единицы измерения
        
        :param _size: размер названия характеристики
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapGetMtqUnitName_t (_hmap, _number, _unit.buffer(), _size)

    mapSetMtqUnitName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMtqUnitName', maptype.HMAP, ctypes.c_long, maptype.PWCHAR)
    def mapSetMtqUnitName(_hmap: maptype.HMAP, _number: int, _unit: mapsyst.WTEXT) -> int:
        """
        Записать название единицы измерения матрицы качеств
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер файла в цепочке
        
        :param _unit: название единицы измерения
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapSetMtqUnitName_t (_hmap, _number, _unit.buffer())

    mapUpdateMtqDuplicates_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateMtqDuplicates', maptype.HMAP, ctypes.c_long)
    def mapUpdateMtqDuplicates(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Обновить уменьшенную копию
        
        :param _hmap: идентификатор открытых данных
        
        :param _number: номер матрицы качеств в цепочке
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapUpdateMtqDuplicates_t (_hmap, _number)

    mapConvertMatrix_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapConvertMatrix', maptype.PWCHAR, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.POINTER(maptype.COLORREF), ctypes.POINTER(ctypes.c_double))
    def mapConvertMatrix(_name: mapsyst.WTEXT, _minimum: float, _maximum: float, _colorcount: int, _scaletype: int, _palette: ctypes.POINTER(maptype.COLORREF), _diapason: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразовать матрицу MTW/MTQ (MTW - матрица высот, MTQ - матрица качеств)
        
        :param _name: полное имя исходной матрицы MTW или MTQ если исходная матрица - MTW, то функция создаёт матрицу качеств, имя результирующего файла формируется из исходного имени с заменой расширения на mtq если исходная матрица - MTQ, то функция создаёт матрицу высот (файл с расширением mtw)
        
        :param _minimum: минимальное значение характеристики (высоты), устанавливаемое в заголовок результирующей матрицы
        
        :param _maximum: минимальное значение характеристики (высоты), устанавливаемое в заголовок результирующей матрицы если minimum = maximum ``= 0``, то в заголовок результирующей матрицы устанавливаются minimum, maximum исходной матрицы
        
        :param _colorcount: количество цветов палитры результирующей матрицы качеств
        
        :param _scaletype: тип шкалы палитры результирующей матрицы качеств: ``1`` - шкала с равномерными диапазонами ``2`` - шкала с неравномерными диапазонами (необходимо задать параметр diapason)
        
        :param _palette: адрес массива цветов палитры результирующей матрицы качеств, размер массива должен быть не менее colorcount, иначе возможны ошибки работы с памятью
        
        :param _diapason: адрес массива верхних значений диапазонов неравномерной палитры матрицы качеств, используется при scaletype ``= 2``, размер массива должен быть не менее colorcount, иначе возможны ошибки работы с памятью Параметры colorcount, scaletype, palette, diapason задают описание палитры результирующей матрицы качеств и используются только для преобразования MTW в MTQ (если исходная матрица - MTW). Если данные параметры не заданы (равны нулю),
        
        :returns: При успешном завершении возвращает значение 1 При ошибке возвращает значение, меньшее 1 (код ошибки): ``0`` - ошибка входных параметров -``1`` - ошибка открытия исходной матрицы -``2`` - исходный файл не является матрицей -``3`` - ошибка копирования исходной матрицы с заменой расширения -``4`` - ошибка открытия результирующей матрицы
        :rtype: int
        
        .. note::

           то создаваемый файл MTQ содержит палитру матрицы высот
           Матрица высот, полученная в результате преобразования MTQ в MTW,
           отображается в текущей палитре матриц высот, установленной в документе
           Значения характеристики (высоты) матрицы разделяются на colorcount
           диапазонов значений, каждому из которых соответствует цвет палитры
           Диапазоны значений и цвета палитры располагаются от минимального значения
           характеристики (высоты) к максимальному
        """
        return mapConvertMatrix_t (_name.buffer(), _minimum, _maximum, _colorcount, _scaletype, _palette, _diapason)

    mapOpenEgmPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapOpenEgmPro', maptype.PWCHAR, ctypes.c_long)
    def mapOpenEgmPro(_mtrname: mapsyst.WTEXT, _multithread: int) -> ctypes.c_void_p:
        """
        Открыть матрицу (Egm2008 или другой)
        
        :param _mtrname: путь к открываемой модели геоида/квазигеоида (MTW) или ``0``
        
        :param _multithread: признак применения матрицы в потоке (если не равен ``0``, то открывается отдельно, независимо от наличия уже открытой ранее матрицы, со своим буфером для чтения блоков) Каждый поток должен иметь свой идентификатор открытой матрицы, полученный с параметром multithread равным ``1``
        
        :returns: Возвращает идентификатор открытой матрицы Egm2008 При ошибке возвращает 0
        
        .. note::

           Если имя файла не задано (mtrname равно 0), то проверяется наличие следущих
           матриц в папке приложения:
           egm2008_1min.mtw  (размер элемента 1 минута)
           egm2008_2.5min.mtw (размер элемента ``2.5`` минуты)
           При нахождении матрицы выполняется ее открытие
        """
        return mapOpenEgmPro_t (_mtrname.buffer(), _multithread)

    mapCloseEgm_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseEgm', ctypes.c_void_p)
    def mapCloseEgm(_hmtr: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Закрыть матрицу
        
        :param _hmtr: идентификатор открытой матрицы
        """
        return mapCloseEgm_t (_hmtr)

    mapReadEgm_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapReadEgm', ctypes.c_void_p, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double))
    def mapReadEgm(_hmtr: ctypes.c_void_p, _interptype: int, _b: float, _l: float, _h: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Прочитать высоту геоида над поверхностью эллипсоида WGS84
        
        :param _hmtr: идентификатор открытой матрицы
        
        :param _interptype: тип интерполяции: ``1`` - ближайший сосед ``2`` - интерполяция по ближайшим ``3`` элементам ``3`` - билинейная интерполяция по ``4`` ближайшим элементам ``4`` - бикубическая интерполяция по ``16`` ближайшим элементам
        
        :param _b: широта точки на эллипсоиде ``WGS84`` в радианах
        
        :param _l: долгота точки на эллипсоиде ``WGS84`` в радианах
        
        :param _h: возвращаемая высота геоида над эллипсоидом ``WGS84`` в метрах (поправка) При переходе от геодезической высоты ``WGS84`` к нормальной высоте (``MSL``) необходимо вычесть полученную поправку
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapReadEgm_t (_hmtr, _interptype, _b, _l, _h)

    mapGetEgmName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetEgmName', ctypes.c_void_p, maptype.PWCHAR, ctypes.c_long)
    def mapGetEgmName(_hmtr: ctypes.c_void_p, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить имя открытой матрицы
        
        :param _hmtr: идентификатор открытой матрицы
        
        :param _name: адрес строки для размещения результата
        
        :param _size: размер строки
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapGetEgmName_t (_hmtr, _name.buffer(), _size)



def mtrapi_healthcheck():
    return 1
