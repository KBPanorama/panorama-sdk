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
    *     ОПИСАНИЕ ИНТЕРФЕЙСА ДОСТУПА К ОБЪЕКТУ "ЭЛЕКТРОННАЯ КАРТА"    *
    *                                                                  *
    ********************************************************************
    *  long int error = 0;                                             *
    *  HMAP hmap = mapOpenAnyDataPro(WTEXT("c:/data/noginsk.mpt"), 0,  *
    *                                &error, 0, 0);                    *
    *    ...                                                           *
    *  mapCloseData(hmap);                                             *
    *                                                                  *
    *  // Освободить ресурсы ядра перед завершением приложения         *
    *  mapCloseMapAccess();                                            *
    *                                                                  *
    ********************************************************************
    
"""

"""
  Программное обеспечение, применяющее интерфейс "MAPAPI",
  может выполняться в различных операционных системах
  (Windows, Linux, QNX, Android и других)
  Все строковые параметры API - функций имеют кодировку
  ANSI для Windows и KOI-8 для Linux-подобных систем
  Параметры типа HWND и HDC в Windows являются идентификаторами
  окна и графического контекста соответственно.
  В Linux параметр HDC содержит указатель на структуру DEVICECONTEXT
  Версия интерфейса MAPAPI
  #define MAPAPIVERSION ... см. maptype.h
  enum PPLACE             // ПРИМЕНЯЕМАЯ СИСТЕМА КООРДИНАТ
  {
  PP_MAP     = 1,    // КООРДИНАТЫ ТОЧЕК В СИСТЕМЕ КАРТЫ В ДИСКРЕТАХ
  PP_PICTURE = 2,    // КООРДИНАТЫ ТОЧЕК В СИСТЕМЕ ИЗОБРАЖЕНИЯ В ПИКСЕЛАХ
  PP_PLANE   = 3,    // КООРДИНАТЫ ТОЧЕК В ПЛОСКОЙ ПРЯМОУГОЛЬНОЙ СИСТЕМЕ
  // НА МЕСТНОСТИ В МЕТРАХ
  PP_GEO     = 4,    // КООРДИНАТЫ ТОЧЕК В ГЕОДЕЗИЧЕСКИХ КООРДИНАТАХ В РАДИАНАХ
  };
  enum VTYPE              // ТИП ОТОБРАЖЕНИЯ КАРТЫ
  {
  VT_SCREEN        = 1, // ЭКРАННЫЙ (ЧЕРЕЗ DIB)
  VT_SCREENCONTOUR = 2, // ЭКРАННЫЙ КОНТУРНЫЙ
  VT_PRINT         = 3, // ПРИНТЕРНЫЙ (ЧЕРЕЗ WIN API)
  VT_PRINTGLASS    = 4, // ПРИНТЕРНЫЙ БЕЗ ЗАЛИВКИ ПОЛИГОНОВ
  VT_PRINTCONTOUR  = 5, // ПРИНТЕРНЫЙ КОНТУРНЫЙ, БЕЗ УСЛОВНЫХ ЗНАКОВ
  VT_PRINTRST      = 6, // ПРИНТЕРНЫЙ РАСТРИЗОВАННЫЙ (ЧЕРЕЗ WIN API)
  };
"""

import os
import ctypes
import mapsyst
import maptype
import mapcreat
import mapgdi

PACK_WIDTH = 1

class TEMPHMAP(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("hMap",maptype.HMAP)]
    def __init__(self, value: maptype.HMAP = 0):
        super().__init__()
        self.hMap = value
    def __del__(self):
        self.Close()
    def Close(self):
        if self.hMap != 0:
            mapCloseData(self.hMap)
        self.hMap = 0
    def HMAP(self):
        return self.hMap
    def __eq__(self, other):
        return self.hMap == other.hMap
    def __ne__(self, other):
        return self.hMap != other.hMap

class TEMPHOBJ(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("hInfo",maptype.HOBJ)]
    def __init__(self, value: maptype.HOBJ = 0):
        super().__init__()
        self.hInfo = value
    def __del__(self):
        self.Close()
    def Close(self):
        if self.hInfo != 0:
            mapFreeObject(self.hInfo)
        self.hInfo = 0
    def HOBJ(self):
        return self.hInfo
    def __eq__(self, other):
        return self.hInfo == other.hInfo
    def __ne__(self, other):
        return self.hInfo != other.hInfo

class TEMPHUSER(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("hUser",ctypes.c_void_p)]
    def __init__(self, value: ctypes.c_void_p = 0):
        super().__init__()
        self.hUser = value
    def __del__(self):
        self.Close()
    def Close(self):
        if self.hUser != 0:
            mapDeleteUserSystemParameters(self.hUser)
        self.hUser = 0
    def HUSER(self):
        return self.hUser
    def __eq__(self, other):
        return self.hUser == other.hUser
    def __ne__(self, other):
        return self.hUser != other.hUser

class TEMPCONNECT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Connect",ctypes.c_long)]
    def __init__(self, value: ctypes.c_long = 0):
        super().__init__()
        self.Connect = value
    def __del__(self):
        self.Close()
    def Close(self):
        if self.Connect != 0:
            mapCloseConnect(self.Connect)
        self.Connect = 0
    def CONNECT(self):
        return self.Connect
    def __eq__(self, other):
        return self.Connect == other.Connect
    def __ne__(self, other):
        return self.Connect != other.Connect

class TEMPHOBJSET(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("hObjSet",maptype.HOBJSET)]
    def __init__(self, value: maptype.HOBJSET = 0):
        super().__init__()
        self.hObjSet = value
    def __del__(self):
        self.Close()
    def Close(self):
        if self.hObjSet != 0:
            mapFreeObjectSet(self.hObjSet)
        self.hObjSet = 0
    def HOBJSET(self):
        return self.hObjSet
    def __eq__(self, other):
        return self.hObjSet == other.hObjSet
    def __ne__(self, other):
        return self.hObjSet != other.hObjSet



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
    mapOpenAnyDataPro_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapOpenAnyDataPro', maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long), maptype.PWCHAR, ctypes.c_long)
    def mapOpenAnyDataPro(_name: mapsyst.WTEXT, _mode: int, _error: ctypes.POINTER(ctypes.c_long), _password: mapsyst.WTEXT, _size: int) -> maptype.HMAP:
        """
        Открыть данные с автоматическим определением их типа: векторные, растровые, матричные, проект, ...
        
        :param _name: полный путь к открываемому файлу (MAP, SITX, MTW, RSW, MPT и так далее) в кодировке UNICODE
        
        :param _mode: режим чтения/записи: ``GENERIC_READ``, ``GENERIC_WRITE`` или ``0`` ``GENERIC_READ`` - все данные только на чтение, при этом не открываются файлы \\Log\\name.log и \\Log\\name.tac - протокол работы и журнал транзакций
        
        :param _error: после выполнения функции переменная содержит код ошибки, когда ``HMAP`` равен ``0``, или ``0``; коды ошибок приведены в maperr.rh
        
        :param _password: пароль доступа к данным из которого формируется ``256``-битный код для шифрования данных (при утрате пароля данные не восстанавливаются) или ноль
        
        :param _size: длина пароля в байтах или ноль
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HMAP
        
        .. note::

           Передача пароля необходима, если при создании карты он был указан
           Если пароль не передан, а он был указан при создании,
           то автоматически вызывается диалог scnGetMapPassword из mapscena64.dll (gis64dlgs.dll)
           Если выдача сообщений запрещена (mapIsMessageEnable()), то диалог
           не вызывается, а при отсутствии пароля происходит отказ открытия данных
           После завершения использования карты необходимо освободить ресурсы функцией mapCloseData
        """
        if _error == 0:
            etemp = ctypes.c_int(0)
            return mapOpenAnyDataPro_t (_name.buffer(), _mode, ctypes.byref(etemp), _password.buffer(), _size)
        return mapOpenAnyDataPro_t (_name.buffer(), _mode, _error, _password.buffer(), _size)

    mapIsMapHandleCorrect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsMapHandleCorrect', maptype.HMAP)
    def mapIsMapHandleCorrect(_hmap: maptype.HMAP) -> int:
        """
        Проверить идентификатор данных на корректность
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsMapHandleCorrect_t (_hmap)

    mapSetStructureControlFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetStructureControlFlag', ctypes.c_long)
    def mapSetStructureControlFlag(_flag: int) -> int:
        """
        Установить разрешение выполнять структурный контроль карты после сбоев программы
        
        :param _flag: нулевое значение запрещает выполнение контроля структуры при открытии карты, ненулевое значение - разрешает
        
        :returns: Возвращает старое значение флага
        :rtype: int
        """
        return mapSetStructureControlFlag_t (_flag)

    mapUseInsideThread_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUseInsideThread', ctypes.c_long)
    def mapUseInsideThread(_state: int) -> int:
        """
        Установить ограничение на число разрешенных к использованию ядер (процессоров) в системе
        
        :param _state: флаг ограничения числа ядер (процессоров) в системе: ``= 0`` - не использовать многопоточность ``> 1`` - максимальное число потоков в выполняемых задачах ``< -1`` - доля ядер (процессоров) разрешенных для выполнения потоков
        
        :returns: Возвращает старое значение состояния разрешения внутренних потоков
        :rtype: int
        
        .. note::

           Например, -``2`` - использовать не более 1/2 ядер (процессоров) в системе
           Изначально потоки разрешены, но для серверного применения библиотеки,
           работающей в многопоточных приложениях, внутренние потоки понижают
           общую производительность. Например, внутренняя реализация функции
           отображения растра запускает до 8 потоков. Если функция отображения
           вызвана параллельно 10 потоками, одномоментно будет работать 90 потоков.
           Внутреннее число потоков не превышает число ядер процессора, включая виртуальные ядра
        """
        return mapUseInsideThread_t (_state)

    mapGetProcessorNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetProcessorNumber')
    def mapGetProcessorNumber() -> int:
        """
        Запросить число ядер (процессоров) в системе, доступных для приложения с учетом установленных ограничений
        
        Минимальное возвращаемое значение равно 1 (не использовать многопоточность)
        """
        return mapGetProcessorNumber_t ()

    mapSetAppendDataMode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetAppendDataMode', maptype.HMAP, ctypes.c_long)
    def mapSetAppendDataMode(_hmap: maptype.HMAP, _mode: int) -> int:
        """
        Установить режим добавления данных к карте
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _mode: режим добавления данных: ``1`` - ускоренный, ``0`` - стандартный При ускоренном режиме не пересчитываются габариты документа по всем открытым данным и не обновляется палитра, что существенно ускоряет процесс добавления данных потоком
        
        :returns: Возвращает текущее значение режима
        :rtype: int
        
        .. note::

           По окончанию добавления данных рекомендуется вернуть режим добавления
           к стандартному для обновления габаритов и палитры
           Габариты обновляются автоматически и при масштабировании документа,
           а палитра нужна при формировании изображений с ограниченным диапазоном цветов
           После вызова mapOpenProject или mapAppendProject автоматически устанавливает
           стандартный режим обновления данных
        """
        return mapSetAppendDataMode_t (_hmap, _mode)

    mapSetLoadState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetLoadState', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetLoadState(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _state: int) -> int:
        """
        Установить для карты режим потоковой загрузки данных
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в документе, для фоновой карты равен hmap
        
        :param _state: режим потоковой загрузки данных: ``1`` - включен, ``0`` - выключен Применяется для ускорения загрузки данных из обменных форматов при создании карты В процессе загрузки данных другие потоки или процессы не должны выполнять редактирование карты В режиме потоковой загрузки данных отключается журналирование операций
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetLoadState_t (_hmap, _hsite, _state)

    mapGetLoadState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetLoadState', maptype.HMAP, maptype.HSITE)
    def mapGetLoadState(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить для карты режим потоковой загрузки данных
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в документе, для фоновой карты равен hmap Применяется для ускорения загрузки данных из обменных форматов при создании карты В процессе загрузки данных другие потоки или процессы не должны выполнять редактирование карты В режиме потоковой загрузки данных отключается журналирование операций
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetLoadState_t (_hmap, _hsite)

    mapCheckLoadState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckLoadState', maptype.HMAP)
    def mapCheckLoadState(_hmap: maptype.HMAP) -> int:
        """
        Запросить наличие в составе открытых данных карт в состоянии потоковой загрузки данных
        
        :param _hmap: идентификатор открытых данных (документа) В процессе загрузки данных другие потоки или процессы не должны выполнять редактирование карты
        
        :returns: Возвращает ненулевое значение, если хотя бы одна из карт находится в режиме потоковой загрузки При ошибке возвращает ноль
        :rtype: int
        """
        return mapCheckLoadState_t (_hmap)

    mapGetSitePercentLoad_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSitePercentLoad', maptype.HMAP, maptype.HSITE)
    def mapGetSitePercentLoad(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить процент загрузки данных
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в документе, для фоновой карты равен hmap Для локальных данных показывает процесс загрузки в оперативную память, для данных с ГИС Сервера - процесс загрузки в кэш, для баз данных - процесс формирования кэша
        
        :returns: Возвращает процент загрузки данных
        :rtype: int
        """
        return mapGetSitePercentLoad_t (_hmap, _hsite)

    mapGetSitePercentAndSizeLoad_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSitePercentAndSizeLoad', maptype.HMAP, maptype.HSITE, ctypes.POINTER(ctypes.c_long))
    def mapGetSitePercentAndSizeLoad(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _loadsize: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить процент загрузки и объём загруженных данных в Мб
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в документе, для фоновой карты равен hmap
        
        :param _loadsize: поле для записи размера загруженных данных в Мб Для локальных данных показывает процесс загрузки в оперативную память, для данных с ГИС Сервера - процесс загрузки в кэш, для баз данных - процесс формирования кэша
        
        :returns: Возвращает процент загрузки данных
        :rtype: int
        """
        return mapGetSitePercentAndSizeLoad_t (_hmap, _hsite, _loadsize)

    mapAppendAnyDataPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendAnyDataPro', maptype.HMAP, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapAppendAnyDataPro(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _mode: int, _transform: int, _password: mapsyst.WTEXT, _size: int) -> int:
        """
        Добавить данные (карту, растр, матрицу) к открытой карте и выполнить трансформирование при необходимости
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _name: полный путь к открываемому файлу (MAP, SITX, SIT, MTW, MTQ, RSW, MPT) в кодировке UNICODE
        
        :param _mode: режим чтения/записи (``GENERIC_READ``, ``GENERIC_WRITE`` или ``0``)
        
        :param _transform: признак трансформирования векторной карты к ранее открытым данным: ``0`` - не трансформировать данные (преобразовывать ``"на лету"``), ``1`` - трансформировать данные при открытии и сохранить карту в новой проекции, -``1`` - задать вопрос пользователю. В серверной версии -``1`` обрабатывается, как ``0``
        
        :param _password: пароль доступа к данным из которого формируется ``256``-битный код для шифрования данных (при утрате данные не восстанавливаются) или ноль
        
        :param _size: длина пароля в байтах или ноль
        
        :returns: Возвращает идентификатор типа данных (``FILE_MAP`` - для векторной карты, ``FILE_RSW`` - для растра, ``FILE_MTW`` - для матрицы, ``FILE_MTL`` - для матрицы слоев, ``FILE_MTQ`` - для матрицы качеств), данные добавляются в список последними, если данные уже были открыты, число открытых данных (карт, растров, матриц) не меняется При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Передача пароля необходима, если при создании карты он был указан
           Если пароль не передан, а он был указан при создании,
           то автоматически вызывается диалог scnGetMapPassword из mapscena64.dll (gis64dlgs.dll)
           Если выдача сообщений запрещена (mapIsMessageEnable()), то диалог
           не вызывается, а при отсутствии пароля происходит отказ открытия данных
        """
        return mapAppendAnyDataPro_t (_hmap, _name.buffer(), _mode, _transform, _password.buffer(), _size)

    mapAppendAnyDataEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendAnyDataEx', maptype.HMAP, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapAppendAnyDataEx(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _mode: int, _transform: int, _password: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        return mapAppendAnyDataEx_t (_hmap, _name.buffer(), _mode, _transform, _password.buffer(), _size, _error)

    mapSetRegion_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRegion', maptype.HMAP)
    def mapSetRegion(_hmap: maptype.HMAP) -> int:
        """
        Обновить в документе общие габариты района работ
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           После смены ограничения на область отображения или создания объекта на векторной карте
           за пределами текущих габаритов документа необходимо обновить габариты района и затем обновить
           позицию изображения карты в окне
        """
        return mapSetRegion_t (_hmap)

    mapCheckDocIncludeDoc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckDocIncludeDoc', maptype.HMAP, maptype.HMAP)
    def mapCheckDocIncludeDoc(_hmap: maptype.HMAP, _hcheckhmap: maptype.HMAP) -> int:
        """
        Проверить, что карты, растры и матрицы из одного документа, входят в состав открытых данных другого документа
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hcheckhmap: идентификатор открытых данных (документа), в котором ищутся карты из hmap
        
        :returns: Если все данные входят, то возвращает положительное значение При ошибке возвращает ноль
        :rtype: int
        """
        return mapCheckDocIncludeDoc_t (_hmap, _hcheckhmap)

    mapIsNeedTranslate_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsNeedTranslate', maptype.HMAP, maptype.PWCHAR)
    def mapIsNeedTranslate(_hmap: maptype.HMAP, _fileName: mapsyst.WTEXT) -> int:
        """
        Запросить соответствие систем координат добавляемой в документ карты и документа
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _fileName: имя файла добавляемых данных (карты, растра, матрицы)
        
        :returns: Если система координат карты не соответствует открытому району, функция возвращает 1 При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsNeedTranslate_t (_hmap, _fileName.buffer())

    mapGetDataSizeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetDataSizeUn', maptype.PWCHAR)
    def mapGetDataSizeUn(_name: mapsyst.WTEXT) -> float:
        """
        Запросить размер данных по имени файла
        
        :param _name: полный путь к файлу
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapGetDataSizeUn_t (_name.buffer())

    mapGetMainNameEx_t = mapsyst.GetProcAddress(acceslib,maptype.PWCHAR,'mapGetMainNameEx', maptype.HMAP)
    def mapGetMainNameEx(_hmap: maptype.HMAP) -> mapsyst.WTEXT:
        """
        Запросить имя главной карты в документе или имя проекта (mpt, mptz), если открыт проект
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает пустую строку
        :rtype: mapsyst.WTEXT
        """
        return mapGetMainNameEx_t (_hmap)

    mapGetMainNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMainNameUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapGetMainNameUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить в кодировке UNICODE имя главной карты в документе или имя проекта (mpt, mptz), если открыт проект
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _name: адрес буфера для записи полного пути к файлу
        
        :param _size: размер буфера в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMainNameUn_t (_hmap, _name.buffer(), _size)

    mapGetMainMapNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMainMapNameUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_int)
    def mapGetMainMapNameUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _namesize: int) -> int:
        """
        Запросить имя (полный путь к файлу) главной карты в документе или в проекте (MPT)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _name: буфер для возвращаемой строки
        
        :param _namesize: размер буфера в байтах
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapGetMainMapNameUn_t (_hmap, _name.buffer(), _namesize)

    mapRegisterFromMapType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRegisterFromMapType', ctypes.c_int, ctypes.POINTER(mapcreat.MAPREGISTEREX))
    def mapRegisterFromMapType(_maptype: int, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX)) -> int:
        """
        Заполнение справочных данных в зависимости от типа карты
        
        :param _maptype: тип карты, описание в ``MAPTYPE`` в файле mapcreat.h
        
        :param _mapreg: заполняемая структура параметров системы координат карты Структуры ``MAPREGISTEREX``, ``LISTREGISTER`` описаны в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapRegisterFromMapType_t (_maptype, _mapreg)

    mapGetProjectionParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetProjectionParameters', ctypes.c_long)
    def mapGetProjectionParameters(_code: int) -> int:
        """
        Запросить допустимые параметры для проекции
        
        :param _code: номер проекции из ``MAPPROJECTION`` в файле mapcreat.h
        
        :returns: Возвращает комбинацию флагов PROJECTIONPARAMETERS в файле mapcreat.h Например: значение 49 = EPP_AXISMERIDIAN|EPP_FALSEEASTING|EPP_FALSENORTHING При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetProjectionParameters_t (_code)

    mapCreateMapExp_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateMapExp', maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(mapcreat.SHEETNAMES), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long), maptype.HMAP, maptype.HSITE)
    def mapCreateMapExp(_mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _sheetnames: ctypes.POINTER(mapcreat.SHEETNAMES), _mainname: mapsyst.WTEXT, _password: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_long), _hmap: maptype.HMAP, _hsite: maptype.HSITE) -> maptype.HMAP:
        """
        Создать новую векторную карту
        
        :param _mapname: полное имя файла карты (MAP, SIT, SITX)
        
        :param _rscname: полное имя файла ресурсов (``RSC``)
        
        :param _mapreg: структура параметров системы координат карты
        
        :param _listreg: параметры листа многолистовой карты или ``0``
        
        :param _sheetnames: название (UTF-16) листа карты, номенклатуры и файлов даных (для многолистовой карты), для векторной карты не ограниченной рамкой название листа и номенклатуры совпадает, а название файлов данных совпадает с названием паспорта карты
        
        :param _mainname: главное название (UTF-16) многолистовой карты (MAP), для пользовательской карты совпадает с названием листа карты Запросить главное название карты можно функцией mapGetSiteNameUn
        
        :param _password: пароль доступа к данным из которого формируется ``256``-битный код для шифрования данных или ``0``. При утрате пароля данные не восстанавливаются. Поддерживается для карт с расширением SITX - хранилище в одном файле
        
        :param _size: длина пароля в байтах или ``0``
        
        :param _hmap: идентификатор документа с открытыми картами
        
        :param _hsite: идентификатор карты в документе, из которой будет скопирован пароль доступа к данным
        
        :param _error: поле для получения кода ошибки или ``0``; коды ошибок приведены в maperr.rh
        
        :returns: Возвращает идентификатор открытой векторной карты Структуры MAPREGISTEREX, LISTREGISTER и SHEETNAMES описаны в mapcreat.h После завершения использования карты необходимо освободить ресурсы функцией mapCloseData При ошибке возвращает ноль
        :rtype: maptype.HMAP
        """
        return mapCreateMapExp_t (_mapname.buffer(), _rscname.buffer(), _mapreg, _listreg, _sheetnames, _mainname.buffer(), _password.buffer(), _size, _error, _hmap, _hsite)

    mapCreateSiteForMapEx_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateSiteForMapEx', maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, maptype.HMAP, maptype.HSITE, ctypes.POINTER(ctypes.c_long))
    def mapCreateSiteForMapEx(_mapname: mapsyst.WTEXT, _mainname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _saveborder: int, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _error: ctypes.POINTER(ctypes.c_long)) -> maptype.HMAP:
        """
        Создать новую векторную карту по образцу
        
        :param _mapname: полный путь к файлу новой карты (расширение MAP, SIT, SITX): MAP - может быть задано только, если исходная карта имеет тип MAP
        
        :param _mainname: название карты или ``0``; eсли mainname ``= 0``, то используется имя файла (без расширения)
        
        :param _rscname: имя файла классификатора; eсли rscname ``= 0``, используется классификатор исходной карты
        
        :param _saveborder: сохранить объект-рамку (учитывается только при наличии у исходной карты объекта-рамки): ``1`` - сохранить рамку, название листа и номенклатуру; ``0`` - не сохранять рамку; в название листа и номенклатуру записывается название карты
        
        :param _hmap: идентификатор документа с открытыми картами
        
        :param _hsite: идентификатор карты в документе, из которой будут скопированы параметры системы координат
        
        :param _error: поле для получения кода ошибки или ``0``; коды ошибок приведены в maperr.rh
        
        :returns: Возвращает идентификатор новой векторной карты При ошибке возвращает ноль
        :rtype: maptype.HMAP
        """
        return mapCreateSiteForMapEx_t (_mapname.buffer(), _mainname.buffer(), _rscname.buffer(), _saveborder, _hmap, _hsite, _error)

    mapCreateSiteForMap_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateSiteForMap', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, maptype.HMAP, maptype.HSITE, ctypes.POINTER(ctypes.c_long))
    def mapCreateSiteForMap(_mapname: mapsyst.WTEXT, _mainname: mapsyst.WTEXT, _saveborder: int, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _error: ctypes.POINTER(ctypes.c_long)) -> maptype.HMAP:
        return mapCreateSiteForMap_t (_mapname.buffer(), _mainname.buffer(), _saveborder, _hmap, _hsite, _error)

    mapCreateTempSitePro_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateTempSitePro', maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_long)
    def mapCreateTempSitePro(_rscname: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _inmemory: int) -> maptype.HMAP:
        """
        Создать временную пользовательскую карту
        
        :param _rscname: полный путь к файлу ресурсов (``RSC``)
        
        :param _mapreg: параметры проекции создаваемой временной карты или ``0``
        
        :param _datum: параметры датума или ``0``
        
        :param _ellipsoid: параметры эллипсоида или ``0``
        
        :param _inmemory: признак создания карты в оперативной памяти или ``0``
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HMAP
        
        .. note::

           Если mapreg не задан, то создается Цилиндрическая прямая равноугольная Меркатора на шаре EPSG:3857
           Если параметр inmemory не равен 0, то все данные хранятся только в оперативной памяти
           и освобождаются при закрытии карты
           Файлы карты размещаются в рабочей директории системы и имеют уникальные имена, генерируемые автоматически
           При закрытии карты все файлы данных удаляются
           После завершения использования карты необходимо освободить ресурсы функцией mapCloseData
        """
        return mapCreateTempSitePro_t (_rscname.buffer(), _mapreg, _datum, _ellipsoid, _inmemory)

    mapCreateTempSiteForMap_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapCreateTempSiteForMap', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapCreateTempSiteForMap(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _inmemory: int) -> maptype.HMAP:
        """
        Создать временную пользовательскую карту с системой координат и классификатором, как у эталонной карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в документе, для фоновой карты равен hmap
        
        :param _inmemory: признак создания карты в оперативной памяти или ``0``
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HMAP
        """
        return mapCreateTempSiteForMap_t (_hmap, _hsite, _inmemory)

    mapCreateAndAppendTempSitePro_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapCreateAndAppendTempSitePro', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapCreateAndAppendTempSitePro(_hmap: maptype.HMAP, _rscname: mapsyst.WTEXT, _inmemory: int) -> maptype.HSITE:
        """
        Создать временную пользовательскую карту с текущими параметрами документа и добавить ее в документ
        
        :param _hmap: идентификатор открытого документа
        
        :param _rscname: полное имя файла ресурсов, если равно ``0`` - выбирается из открытой карты
        
        :param _inmemory: признак создания карты в оперативной памяти или ``0`` Файлы карты размещаются в рабочей директории системы и имеют уникальные имена, генерируемые автоматически При закрытии векторной карты все файлы данных автоматически удаляются
        
        :returns: Возвращает идентификатор открытой векторной карты При ошибке возвращает ноль
        :rtype: maptype.HSITE
        
        .. note::

           Если параметр inmemory не равен 0, то все данные хранятся только в оперативной памяти
           и освобождаются при закрытии карты
        """
        return mapCreateAndAppendTempSitePro_t (_hmap, _rscname.buffer(), _inmemory)

    mapCloseData_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseData', maptype.HMAP)
    def mapCloseData(_hmap: maptype.HMAP) -> ctypes.c_void_p:
        """
        Закрыть все данные электронной карты
        
        :param _hmap: идентификатор открытых данных (документа) Идентификатор ``HMAP`` становится недействительным
        """
        return mapCloseData_t (_hmap)

    mapCopyMapEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCopyMapEx', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.c_long)
    def mapCopyMapEx(_sourcename: mapsyst.WTEXT, _newname: mapsyst.WTEXT, _ismove: int, _error: ctypes.POINTER(ctypes.c_long), _total: int) -> int:
        """
        Копирование или перемещение векторной карты
        
        :param _sourcename: полный путь к файлу к файлу существующей карты
        
        :param _newname: полный путь к новому файлу карты
        
        :param _ismove: признак необходимости удаления старой копии карты (перемещения)
        
        :param _error: поле для получения кода ошибки при выполнении команды (описаны в maperr.rh)
        
        :param _total: копировать (перемещать) вместе со служебными файлами в папке \\LOG (например, для резервного копирования)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCopyMapEx_t (_sourcename.buffer(), _newname.buffer(), _ismove, _error, _total)

    mapDeleteMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteMap', maptype.HMAP)
    def mapDeleteMap(_hmap: maptype.HMAP) -> int:
        """
        Закрыть и удалить векторную карту (все файлы данных)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           После удаления идентификатор hmap не должен использоваться, как после mapCloseData()
        """
        return mapDeleteMap_t (_hmap)

    mapDeleteMapByNameEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteMapByNameEx', maptype.PWCHAR, ctypes.c_long)
    def mapDeleteMapByNameEx(_name: mapsyst.WTEXT, _rscdelete: int) -> int:
        """
        Удаление района работ
        
        :param _name: полный путь к файлу удаляемой карты
        
        :param _rscdelete: признак удаления файла классификатора вместе с картой
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteMapByNameEx_t (_name.buffer(), _rscdelete)

    mapOpenProjectUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapOpenProjectUn', maptype.PWCHAR)
    def mapOpenProjectUn(_name: mapsyst.WTEXT) -> maptype.HMAP:
        """
        Открыть проект данных (может содержать карты, растры, матрицы, геопорталы ...)
        
        :param _name: полный путь к файлу проекта MPT
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HMAP
        """
        return mapOpenProjectUn_t (_name.buffer())

    mapAppendProjectUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapAppendProjectUn', maptype.HMAP, maptype.PWCHAR)
    def mapAppendProjectUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT) -> int:
        """
        Добавить проект данных
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _name: полный путь к файлу проекта MPT
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendProjectUn_t (_hmap, _name.buffer())

    mapOpenZipProjectUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapOpenZipProjectUn', maptype.PWCHAR)
    def mapOpenZipProjectUn(_name: mapsyst.WTEXT) -> maptype.HMAP:
        """
        Открыть упакованный проект данных
        
        :param _name: полный путь к файлу проекта MPTZ со сжатыми данными
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HMAP
        """
        return mapOpenZipProjectUn_t (_name.buffer())

    mapGetProjectNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetProjectNameUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapGetProjectNameUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _namesize: int) -> int:
        """
        Запросить имя открытого проекта
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _name: буфер для размещения возвращаемой строки
        
        :param _namesize: размер буфера в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetProjectNameUn_t (_hmap, _name.buffer(), _namesize)

    mapSaveProjectUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSaveProjectUn', maptype.HMAP, maptype.PWCHAR)
    def mapSaveProjectUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT) -> int:
        """
        Сохранить список открытых наборов данных и их свойства в проекте данных MPT
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _name: полный путь к файлу проекта MPT
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSaveProjectUn_t (_hmap, _name.buffer())

    mapSaveZipProjectUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSaveZipProjectUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapSaveZipProjectUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _savefromserver: int) -> int:
        """
        Сохранить список открытых наборов данных, их свойства и упакованные наборы данных в проекте данных MPTZ
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _name: полный путь к файлу проекта MPTZ
        
        :param _savefromserver: признак копирования в MPTZ наборов данных с ГИС Сервера, если есть права на их копирование В проект сохраняются упакованные векторные карты (SITZ\\MAPZ), сжатые растры RSW и сжатые матрицы MTW, MTQ
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSaveZipProjectUn_t (_hmap, _name.buffer(), _savefromserver)

    mapIsDocProject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsDocProject', maptype.HMAP)
    def mapIsDocProject(_hmap: maptype.HMAP) -> int:
        """
        Запросить, является ли документ проектом MPT или MPTZ
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: Если это проект, то возвращает ненулевое значение, если это упакованный проект ``MPTZ`` - возвращает значение FILE_MPTZ
        :rtype: int
        """
        return mapIsDocProject_t (_hmap)

    mapCheckProjectState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckProjectState', maptype.HMAP)
    def mapCheckProjectState(_hmap: maptype.HMAP) -> int:
        """
        Проверить изменение состояния файла проекта на ГИС Сервере
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: Если состояние проекта изменилось - возвращает ненулевое значение
        :rtype: int
        """
        return mapCheckProjectState_t (_hmap)

    mapSaveMapState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSaveMapState', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSaveMapState(_hmap: maptype.HMAP, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Сохранить текущие параметры открытого документа в INI-файл карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _point: координаты центра окна в метрах или ``0`` Вызывается перед закрытием окна карты Сохраняет описание открытых данных, масштаб, палитру, признаки видимости, редактируемости, состав отображаемых объектов...
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSaveMapState_t (_hmap, _point)

    mapRestoreMapState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRestoreMapState', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapRestoreMapState(_hmap: maptype.HMAP, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Восстановить параметры окна карты из INI-файла карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _point: поле для записи сохраненных координат центра окна в метрах или ``0`` Имя ``INI``-файла можно запросить через mapGetMapIniName() Вызывается после открытия карты Восстанавливает описание списка данных, масштаб, палитру, признаки видимости, редактируемости, состав отображаемых объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapRestoreMapState_t (_hmap, _point)

    mapIsActive_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsActive', maptype.HMAP)
    def mapIsActive(_hmap: maptype.HMAP) -> int:
        """
        Запросить, есть ли какие-либо открытые карты, растры, матрицы, геопорталы или другие данные
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: Если открытых данных нет, то возвращает ноль
        :rtype: int
        """
        return mapIsActive_t (_hmap)

    mapIsVectorMapActive_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsVectorMapActive', maptype.HMAP)
    def mapIsVectorMapActive(_hmap: maptype.HMAP) -> int:
        """
        Запросить, есть ли какие-либо открытые векторные карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: Если открытых векторных карт нет, то возвращает ноль
        :rtype: int
        """
        return mapIsVectorMapActive_t (_hmap)

    mapIsVectorMapEdit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsVectorMapEdit', maptype.HMAP)
    def mapIsVectorMapEdit(_hmap: maptype.HMAP) -> int:
        """
        Запросить, есть ли какие-либо открытые векторные карты, доступные для редактирования
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: Если доступных для редактирования векторных карт нет, то возвращает ноль
        :rtype: int
        """
        return mapIsVectorMapEdit_t (_hmap)

    mapIsVectorMapEditWithoutMetric_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsVectorMapEditWithoutMetric', maptype.HMAP)
    def mapIsVectorMapEditWithoutMetric(_hmap: maptype.HMAP) -> int:
        """
        Запросить, есть ли какие-либо открытые векторные карты c доступом на редактирование семантики или графики
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: Если доступных для редактирования векторных карт нет, то возвращает ноль
        :rtype: int
        """
        return mapIsVectorMapEditWithoutMetric_t (_hmap)

    mapGetActiveDataCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetActiveDataCount', maptype.HMAP, ctypes.c_long)
    def mapGetActiveDataCount(_hmap: maptype.HMAP, _dataType: int) -> int:
        """
        Запросить, есть ли в документе какие-либо открытые данные помимо указанного типа
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _dataType: идентификатор типа данныхб который не нужно учитывать при подсчете Примеры типов данных: ``FILE_MAP`` - для векторной карты, ``FILE_SITE`` - для пользовательских карт, ``FILE_RSW`` - для растров, ``FILE_MTW`` - для матриц, ``FILE_MTL`` - для матриц слоев, ``FILE_MTQ`` - для матрицы качеств, ``FILE_MTD`` - для модели ``"Облако точек"``, ``FILE_TIN`` - для ``TIN``-модели ", ``FILE_WMS`` - для геопортала).
        
        :returns: Возвращает количество открытых данных в документе помимо указанного типа
        :rtype: int
        
        .. note::

           Если dataType равно 0, то выполняется подсчет всех видов данных документа
        """
        return mapGetActiveDataCount_t (_hmap, _dataType)

    mapAdjustData_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAdjustData', maptype.HMAP)
    def mapAdjustData(_hmap: maptype.HMAP) -> int:
        """
        Выполнить согласование данных электронной карты в памяти и на диске
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: Если состояние данных в памяти изменилось (по данным с диска) - возвращает ненулевое значение (1), иначе - 0 Если карта должна быть закрыта - возвращает 2 (доступ на ГИС Сервер прекращен) Если состояние изменилось - необходимо перерисовать изображение карты Опрос состояния целесообразно выполнять периодически в процессе работы приложения
        :rtype: int
        """
        return mapAdjustData_t (_hmap)

    mapSetAdjustMode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetAdjustMode', maptype.HMAP, ctypes.c_long)
    def mapSetAdjustMode(_hmap: maptype.HMAP, _mode: int) -> int:
        """
        Установить доступность для выполнения команды Adjust
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _mode: признак доступности обработки команды Adjust, если равен ``0``, то команда не обрабатывается При выполнении длительных процедур (отмена длинных транзакций, трансформирование данных и других) целесообразно отключать команду Adjust, если она может быть вызвана из других потоков приложения Команда Adjust может вызывать переоткрытие карт и перераспределение памяти
        
        :returns: Возвращает прежнее значение
        :rtype: int
        """
        return mapSetAdjustMode_t (_hmap, _mode)

    mapCreateListPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateListPro', maptype.HMAP, ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(mapcreat.SHEETNAMES))
    def mapCreateListPro(_hmap: maptype.HMAP, _sheet: ctypes.POINTER(mapcreat.LISTREGISTER), _sheetnames: ctypes.POINTER(mapcreat.SHEETNAMES)) -> int:
        """
        Создать (добавить) новый лист в многолистовой карте типа MAP
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _sheet: описание создаваемого листа в многолистововй карте
        
        :param _sheetnames: имена файлов листа в многолистовой карте Структуры ``LISTREGISTER`` и ``SHEETNAMES`` описаны в mapcreat.h
        
        :returns: При ошибке возвращает ноль, иначе - номер созданного листа c 1
        :rtype: int
        """
        return mapCreateListPro_t (_hmap, _sheet, _sheetnames)

    mapDeleteList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteList', maptype.HMAP, ctypes.c_long)
    def mapDeleteList(_hmap: maptype.HMAP, _list: int) -> int:
        """
        Удалить указанный лист карты в многолистовой карте типа MAP
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _list: номер листа с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteList_t (_hmap, _list)

    mapAppendMapToMapUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendMapToMapUn', maptype.HMAP, maptype.PWCHAR, maptype.HWND)
    def mapAppendMapToMapUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _handle: maptype.HWND) -> int:
        """
        Добавить листы из одной многолистовой карт в другую
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _name: полный путь к файлу добавляемой карты
        
        :param _handle: идентификатор окна, которое будет извещаться о ходе процесса (``0x585`` - ``0x588``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendMapToMapUn_t (_hmap, _name.buffer(), _handle)

    MapSortingSitePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'MapSortingSitePro', maptype.HMAP, maptype.HSITE, ctypes.c_long, maptype.HMESSAGE, ctypes.c_long, ctypes.c_long, maptype.PWCHAR)
    def MapSortingSitePro(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flags: int, _handle: maptype.HMESSAGE, _format: int, _code: int, _password: mapsyst.WTEXT) -> int:
        """
        Сортировка отдельной карты документа
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор сортируемой векторной карты
        
        :param _flags: флажки обработки карты: ``0`` - сортировать все листы, ``1`` - только несортированные, ``2`` - сохранять файлы отката, ``4`` - повысить точность хранения, формат - мкм ``16`` - повысить точность хранения, формат - см ``32`` - повысить точность хранения, формат - мм ``64`` - повысить точность хранения, формат - радианы ``128`` - формировать мультиконтура для объектов с флагом мультиконтурный ``256`` - упаковать карту вместе с локальными документами, на которые есть ссылка из семантики ``512`` - не упаковывать ``RSC`` ``1024`` - перекодировать семантику в кодировку ``ANSI`` (возможна потеря некоторых символов из кодировки ``UTF16``)
        
        :param _handle: идентификатор окна, которому посылаются сообщения ``WM_OBJECT`` и ``WM_ERROR``, если не задан параметр hEvent. Может быть равен ``0``
        
        :param _format: управление форматом карты: ``0`` - не менять, ``1`` - установить формат SITX (на входе может быть SIT или MAP с одним листом), ``2`` - упаковать карту в формат SITZ\\MAPZ, точность - см, -``1`` - установить формат SIT (на входе может быть SITX или MAP с одним листом),
        
        :param _code: управление шифрованием карты: ``0`` - не менять, ``1`` - шифровать данные с помощью пароля из параметра password (формат SITX), -``1`` - снять шифрование данных
        
        :param _password: пароль для шифрования данных, когда code ``= 1``, или ``0``
        
        :returns: Если карта отсортирована успешно, то возвращает 1 Если карта уже отсортирована - возвращает 2 Если оператор прервал операцию - возвращает -1 Если карта не доступна на редактирование - возвращает -2 При ошибке возвращает ноль
        :rtype: int
        """
        return MapSortingSitePro_t (_hmap, _hsite, _flags, _handle, _format, _code, _password.buffer())

    mapCreateObject_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapCreateObject', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapCreateObject(_hmap: maptype.HMAP, _sheetnumber: int, _kind: int, _text: int) -> maptype.HOBJ:
        """
        Cоздать пустой объект векторной карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _sheetnumber: номер листа в котором будет расположен объект
        
        :param _kind: тип создаваемой метрики, описан в maptype.h
        
        :param _text: признак метрики с текстом для создания объектов типа ``"подпись"``
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HOBJ
        
        .. note::

           После вызова функций поиска и чтения объектов все параметры
           полученного объекта могут быть другими
           Для каждого полученного и больше не используемого
           идентификатора HOBJ необходим вызов функции mapFreeObject()
        """
        return mapCreateObject_t (_hmap, _sheetnumber, _kind, _text)

    mapClearObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapClearObject', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapClearObject(_hobj: maptype.HOBJ, _sheetnumber: int, _kind: int) -> int:
        """
        Очистить содержимое объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _sheetnumber: номер листа в котором будет расположен
        
        :param _kind: тип создаваемой метрики, описан в maptype.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapClearObject_t (_hobj, _sheetnumber, _kind)

    mapIsObjectCorrect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsObjectCorrect', maptype.HOBJ)
    def mapIsObjectCorrect(_hobj: maptype.HOBJ) -> int:
        """
        Запросить корректность содержания объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsObjectCorrect_t (_hobj)

    mapIsObjectDeleted_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsObjectDeleted', maptype.HOBJ)
    def mapIsObjectDeleted(_hobj: maptype.HOBJ) -> int:
        """
        Запросить признак удаленного объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsObjectDeleted_t (_hobj)

    mapCreateCopyObject_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapCreateCopyObject', maptype.HMAP, maptype.HOBJ)
    def mapCreateCopyObject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ) -> maptype.HOBJ:
        """
        Cоздать копию объекта векторной карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти Для каждого полученного и больше не используемого идентификатора ``HOBJ`` необходим вызов функции mapFreeObject()
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HOBJ
        """
        return mapCreateCopyObject_t (_hmap, _hobj)

    mapReadCopyObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapReadCopyObject', maptype.HOBJ, maptype.HOBJ)
    def mapReadCopyObject(_hdest: maptype.HOBJ, _hsrc: maptype.HOBJ) -> int:
        """
        Считать полную копию объекта векторной карты в другой объект
        
        :param _hdest: идентификатор заполняемого объекта карты в памяти
        
        :param _hsrc: идентификатор считываемого объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapReadCopyObject_t (_hdest, _hsrc)

    mapReadCopySubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapReadCopySubject', maptype.HOBJ, maptype.HOBJ, ctypes.c_long)
    def mapReadCopySubject(_hdest: maptype.HOBJ, _hsrc: maptype.HOBJ, _subject: int) -> int:
        """
        Считать копию подобъекта векторной карты в другой объект
        
        :param _hdest: идентификатор заполняемого объекта карты в памяти
        
        :param _hsrc: идентификатор считываемого объекта карты в памяти
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Копирует все данные объекта с сохранением в качестве одного главного контура указанный подобъект
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapReadCopySubject_t (_hdest, _hsrc, _subject)

    mapReadCopyMultiSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapReadCopyMultiSubject', maptype.HOBJ, maptype.HOBJ, ctypes.c_long)
    def mapReadCopyMultiSubject(_hdest: maptype.HOBJ, _hsrc: maptype.HOBJ, _number: int) -> int:
        """
        Считать копию внешнего контура мультиполигона вместе с его подобъектами в другой объект
        
        :param _hdest: идентификатор заполняемого объекта карты в памяти
        
        :param _hsrc: идентификатор считываемого объекта карты в памяти
        
        :param _number: порядковый номер внешнего контура, начиная с ``1`` Копирует все данные объекта с сохранением одного внешнего контура и его подобъектов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapReadCopyMultiSubject_t (_hdest, _hsrc, _number)

    mapReadCopyObjectData_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapReadCopyObjectData', maptype.HOBJ, maptype.HOBJ)
    def mapReadCopyObjectData(_hdest: maptype.HOBJ, _hsrc: maptype.HOBJ) -> int:
        """
        Считать копию метрики объекта векторной карты в другой объект
        
        :param _hdest: идентификатор заполняемого объекта карты в памяти
        
        :param _hsrc: идентификатор считываемого объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapReadCopyObjectData_t (_hdest, _hsrc)

    mapCopySubjectOneMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCopySubjectOneMap', maptype.HOBJ, ctypes.c_long, maptype.HOBJ, ctypes.c_long)
    def mapCopySubjectOneMap(_hdest: maptype.HOBJ, _destsub: int, _hsource: maptype.HOBJ, _sourcesub: int) -> int:
        """
        Копировать метрику подобъекта одного объекта в подобъект другого объекта
        
        :param _hdest: объект-приемник, в который добавляется подобъект
        
        :param _destsub: номер подобъекта приемника с ``0``. Если указать -``1`` или несуществующий номер подобъекта,
        
        :param _hsource: объект-источник (source и dest должны принадлежать одной карте)
        
        :param _sourcesub: номер подобъекта источника с ``0``, если указать -``1``, то копируются все подобъекты, а destSub игнорируется Функция выполняет: - добавление подобъекта; - замену подобъекта; - замену всех подобъектов. Пример (назначение последнего подобъекта главным): int sub = mapPolyCount(obj)-``1``;           // Номер последнего контура mapCopySubjectOneMap(obj, -``1``, obj, ``0``);   // Копировать главный контур в дополнительный mapCopySubjectOneMap(obj, ``0``, obj, sub);  // Копировать контур в главный mapDeleteSubject(obj, subject);          // Удалить старую копию контура
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           то добавляется новый подобъект
        """
        return mapCopySubjectOneMap_t (_hdest, _destsub, _hsource, _sourcesub)

    mapCreateCopyObjectAsNew_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapCreateCopyObjectAsNew', maptype.HMAP, maptype.HOBJ)
    def mapCreateCopyObjectAsNew(_hmap: maptype.HMAP, _hobj: maptype.HOBJ) -> maptype.HOBJ:
        """
        Cоздать копию объекта векторной карты, как нового объекта
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти В созданной копии объекта обнуляются порядковый номер и уникальный идентификатор на карте Для каждого полученного и больше не используемого идентификатора ``HOBJ`` необходим вызов функции mapFreeObject()
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HOBJ
        """
        return mapCreateCopyObjectAsNew_t (_hmap, _hobj)

    mapCopyObjectAsNew_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCopyObjectAsNew', maptype.HOBJ, maptype.HOBJ)
    def mapCopyObjectAsNew(_hdest: maptype.HOBJ, _hsrc: maptype.HOBJ) -> int:
        """
        Считать копию объекта векторной карты, как нового объекта
        
        :param _hsrc: исходный объект
        
        :param _hdest: копия объекта В прочитанной копии объекта обнуляются порядковый номер и уникальный идентификатор на карте Для сохранения объекта на карте необходимо выполнить функцию mapCommitObject()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCopyObjectAsNew_t (_hdest, _hsrc)

    mapFreeObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeObject', maptype.HOBJ)
    def mapFreeObject(_hobj: maptype.HOBJ) -> ctypes.c_void_p:
        """
        Удалить описание объекта векторной карты из памяти
        
        :param _hobj: идентификатор объекта карты в памяти Для сохранения объекта на карте необходимо до вызова mapFreeObject(...) выполнить функцию mapCommitObject(...)
        
        :returns: При ошибке возвращает ноль
        """
        return mapFreeObject_t (_hobj)

    mapIsObjectMapActive_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsObjectMapActive', maptype.HMAP, maptype.HOBJ)
    def mapIsObjectMapActive(_hmap: maptype.HMAP, _hobj: maptype.HOBJ) -> int:
        """
        Проверить, что карта объекта еще открыта
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: Если карта уже закрыта, то возвращает ноль При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsObjectMapActive_t (_hmap, _hobj)

    mapReadLastViewObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapReadLastViewObject', maptype.HMAP, maptype.HOBJ)
    def mapReadLastViewObject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ) -> int:
        """
        Считать объект, который отображался последним перед возникновением сбоя отображения карт
        
        Применяется при аварийном завершении функций отображения векторных карт для вывода диагностической информации
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти, в котором будет размещен результат поиска
        
        :returns: Если такой объект не установлен - возвращает ноль
        :rtype: int
        """
        return mapReadLastViewObject_t (_hmap, _hobj)

    mapIsObjectStretch_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsObjectStretch', maptype.HOBJ)
    def mapIsObjectStretch(_hobj: maptype.HOBJ) -> int:
        """
        Запросить признак растягивания объекта по метрике
        
        Данный признак может быть установлен у подписей и векторных объектов
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsObjectStretch_t (_hobj)

    mapSetDocProjectionPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetDocProjectionPro', maptype.HMAP, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_long, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapSetDocProjectionPro(_hmap: maptype.HMAP, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        """
        Установить общие параметры системы координат документа для отображения, печати и расчета координат
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _mapreg: параметры проекции или ``0``
        
        :param _datum: параметры датума или ``0``
        
        :param _ellipsoid: параметры эллипсоида или ``0`` type - тип локального преобразования координат (описан в ``TRANSFORMTYPE`` в mapcreat.h) или ``0``
        
        :param _tparm: параметры локального преобразования координат Структуры ``MAPREGISTER``, ``DATUMPARAM`` и ``ELLIPSOIDPARAM`` описаны в mapcreat.h Устанавливать общие параметры проекции можно для документа поддерживающего пересчет геодезических координат (mapIsGeoSupported() !``= 0``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           После установки общих параметров проекции изображение карты формируется
           в заданной проекции. Векторные карты, матрицы и растры, имеющие другие параметры
           трансформируются в процессе отображения без изменения исходных данных
           Все операции с координатами (mapPlaneToGeo, mapGeoToPlane,
           mapPlaneToGeoWGS84, mapAppendPointPlane, mapInsertPointPlane,
           mapUpdatePointPlane, mapAppendPointGeo и другие) выполняются
           в системе координат документа, определяемой общими параметрами проекции
           При чтении\\записи координат в конкретной карте выполняется пересчет из системы координат документа
           Например, при записи координат из WGS84 на карту в СК-42 можно
           установить общие параметры документа, как ``"Широта/Долгота на WGS84"``
           и выполнить запись координат функцией mapAppendPointGeo, не заботясь
           о дополнительном пересчете координат, или считать координаты функцией
           mapGetGeoPoint (или функцией mapGetGeoPointWGS84, игнорирующей параметры
           документа)
           Чтобы установить текущие параметры проекции и системы координат, как у первой
           карты в документе, можно передать в качестве параметров нули (кроме hmap),
           или вызвать mapClearDocProjection
        """
        return mapSetDocProjectionPro_t (_hmap, _mapreg, _datum, _ellipsoid, _ttype, _tparm)

    mapSetDocProjectionFromUserSystem_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetDocProjectionFromUserSystem', maptype.HMAP, ctypes.c_void_p)
    def mapSetDocProjectionFromUserSystem(_hmap: maptype.HMAP, _huser: ctypes.c_void_p) -> int:
        """
        Установить общие параметры системы координат открытых данных
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _huser: идентификатор пользовательской системы координат, создается в mapCreateUserSystemParametersPro() Общие параметры системы координат открытых данных применяются для отображения, печати и расчета координат из пользовательской системы координат
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetDocProjectionFromUserSystem_t (_hmap, _huser)

    mapClearDocProjection_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapClearDocProjection', maptype.HMAP)
    def mapClearDocProjection(_hmap: maptype.HMAP) -> int:
        return mapClearDocProjection_t (_hmap)

    mapGetDocProjectionPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetDocProjectionPro', maptype.HMAP, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapGetDocProjectionPro(_hmap: maptype.HMAP, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: ctypes.POINTER(ctypes.c_long), _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        """
        Запросить общие параметры системы координат открытых данных
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _mapreg: параметры проекции или ``0``
        
        :param _datum: параметры датума или ``0``
        
        :param _ellipsoid: параметры эллипсоида или ``0``
        
        :param _ttype: тип локального преобразования координат (описан в ``TRANSFORMTYPE`` в mapcreat.h) или ``0``
        
        :param _tparm: параметры локального преобразования координат Структуры ``MAPREGISTER``, ``DATUMPARAM`` и ``ELLIPSOIDPARAM`` описаны в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если параметры не устанавливались функцией mapSetMapInfoEx,
           то они соответсвуют параметрам карты, открытой в документе первой
        """
        return mapGetDocProjectionPro_t (_hmap, _mapreg, _datum, _ellipsoid, _ttype, _tparm)

    mapIsDocProjection_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsDocProjection', maptype.HMAP)
    def mapIsDocProjection(_hmap: maptype.HMAP) -> int:
        """
        Запросить, устанавливались ли общие параметры системы координат открытых данных
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: Если параметры системы координат открытых данных были изменены, то возвращает ненулевое значение При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsDocProjection_t (_hmap)

    mapSetDocShowLimit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetDocShowLimit', maptype.HMAP, ctypes.POINTER(maptype.DFRAME))
    def mapSetDocShowLimit(_hmap: maptype.HMAP, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Установить ограничения области отображения для документа
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _frame: указатель на габариты области ограничения или ноль (отменить ограничение)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           После смены ограничения на область отображения необходимо вызвать функцию mapSetRegion
           для обновления габаритов района и обновить позицию изображения карты в окне
        """
        return mapSetDocShowLimit_t (_hmap, _frame)

    mapGetDocShowLimit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetDocShowLimit', maptype.HMAP, ctypes.POINTER(maptype.DFRAME))
    def mapGetDocShowLimit(_hmap: maptype.HMAP, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Запросить ограничения области отображения для документа
        
        :param _hmap: идентификатор открытой основной карты
        
        :param _frame: указатель на запись для получения габаритов области ограничения
        
        :returns: Если ограничение области отображения не установлено, то возвращает -1 и заполняет габариты документа При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetDocShowLimit_t (_hmap, _frame)

    mapGetPictureHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetPictureHeight', maptype.HMAP)
    def mapGetPictureHeight(_hmap: maptype.HMAP) -> int:
        """
        Запросить высоту общего изображения карты в пикселах для текущего масштаба
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetPictureHeight_t (_hmap)

    mapGetPictureWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetPictureWidth', maptype.HMAP)
    def mapGetPictureWidth(_hmap: maptype.HMAP) -> int:
        """
        Запросить ширину общего изображения карты в пикселах для текущего масштаба
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetPictureWidth_t (_hmap)

    mapGetPictureSizeEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapGetPictureSizeEx', ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long), maptype.HPAINT)
    def mapGetPictureSizeEx(_width: ctypes.POINTER(ctypes.c_long), _height: ctypes.POINTER(ctypes.c_long), _hpaint: maptype.HPAINT) -> ctypes.c_void_p:
        """
        Запросить размеры общего изображения карты в пикселах для текущего масштаба
        
        :param _width: поле для записи ширины изображения в пикселах
        
        :param _height: поле для записи высоты изображения в пикселах
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова, создается функцией mapCreatePaintControl()
        """
        return mapGetPictureSizeEx_t (_width, _height, _hpaint)

    mapGetPixelWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetPixelWidth', maptype.HMAP)
    def mapGetPixelWidth(_hmap: maptype.HMAP) -> float:
        """
        Запросить ширину пиксела изображения карты в метрах на местности для текущего масштаба изображения
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapGetPixelWidth_t (_hmap)

    mapGetPixelHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetPixelHeight', maptype.HMAP)
    def mapGetPixelHeight(_hmap: maptype.HMAP) -> float:
        """
        Запросить высоту пиксела изображения карты в метрах на местности для текущего масштаба изображения
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapGetPixelHeight_t (_hmap)

    mapGetVerticalPixel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetVerticalPixel', maptype.HMAP)
    def mapGetVerticalPixel(_hmap: maptype.HMAP) -> float:
        """
        Запросить текущее число пикселов на метр изображения - разрешение по вертикали
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapGetVerticalPixel_t (_hmap)

    mapGetHorizontalPixel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetHorizontalPixel', maptype.HMAP)
    def mapGetHorizontalPixel(_hmap: maptype.HMAP) -> float:
        """
        Запросить текущее число пикселов на метр изображения - разрешение по горизонтали
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapGetHorizontalPixel_t (_hmap)

    mapGetVerticalPixelEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetVerticalPixelEx', maptype.HPAINT)
    def mapGetVerticalPixelEx(_hpaint: maptype.HPAINT) -> float:
        """
        Запросить текущее число пикселов на метр изображения - разрешение по вертикали
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapGetVerticalPixelEx_t (_hpaint)

    mapGetHorizontalPixelEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetHorizontalPixelEx', maptype.HPAINT)
    def mapGetHorizontalPixelEx(_hpaint: maptype.HPAINT) -> float:
        """
        Запросить текущее число пикселов на метр изображения - разрешение по горизонтали
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapGetHorizontalPixelEx_t (_hpaint)

    mapSetFrameTree_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetFrameTree', ctypes.c_long)
    def mapSetFrameTree(_flag: int) -> int:
        """
        Запретить или разрешить построение дерева объектов для отображения всех карт
        
        :param _flag: признак применения дерева объектов: ``0`` или ``1`` Построение дерева замедляет (от долей секунды до нескольких секунд) открытие неотсортированных карт с большим числом объектов (от нескольких сот тысяч и более), но ускоряет (в ``1``,``5`` - ``3`` раза) отображение больших карт в крупных масштабах
        
        :returns: Возвращает ранее установленное значение
        :rtype: int
        """
        return mapSetFrameTree_t (_flag)

    mapCreatePaintControl_t = mapsyst.GetProcAddress(acceslib,maptype.HPAINT,'mapCreatePaintControl', maptype.HMAP)
    def mapCreatePaintControl(_hmap: maptype.HMAP) -> maptype.HPAINT:
        """
        Создать контекст потока отображения для многопоточного вызова
        
        :param _hmap: идентификатор открытых данных Для каждого потока приложения создается свой контекст и передается в качестве параметров функций отображения или поиска Например: mapPaintByFramePro или mapPaintByFrameToXImagePro В каждом контексте создается свой буфер отображения и выделяется память под служебные области Размер резервируемой памяти помимо буфера отображения может занимать ``1````-2`` Мбайта, внутренний буфер отображения для размера 1920x1080 занимает ``8`` Мбайт Размер может ограничиваться программно в функции mapSetMaxScreenImageSize
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HPAINT
        
        .. note::

           После завершения использования контекст потока отображения его необходимо освободить функцией mapFreePaintControl
        """
        return mapCreatePaintControl_t (_hmap)

    mapCreatePaintControlEx_t = mapsyst.GetProcAddress(acceslib,maptype.HPAINT,'mapCreatePaintControlEx', maptype.HMAP, maptype.HPAINT)
    def mapCreatePaintControlEx(_hmap: maptype.HMAP, _hpaint: maptype.HPAINT) -> maptype.HPAINT:
        """
        Создать контекст потока отображения для многопоточного вызова
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hpaint: контекст потока отображения для копирования параметров отображения и поиска или ``0`` Для каждого потока приложения создается свой контекст и передается в качестве параметров функций отображения или поиска
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HPAINT
        
        .. note::

           После завершения использования контекст потока отображения его необходимо освободить функцией mapFreePaintControl
        """
        return mapCreatePaintControlEx_t (_hmap, _hpaint)

    mapFreePaintControl_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreePaintControl', maptype.HPAINT)
    def mapFreePaintControl(_hpaint: maptype.HPAINT) -> ctypes.c_void_p:
        """
        Удалить контекст потока отображения
        
        :param _hpaint: контекст потока отображения, созданный функциями mapCreatePaintControl или mapCreatePaintControlEx
        """
        return mapFreePaintControl_t (_hpaint)

    mapSetPaintControlMapHandle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetPaintControlMapHandle', maptype.HPAINT, maptype.HMAP)
    def mapSetPaintControlMapHandle(_hpaint: maptype.HPAINT, _hmap: maptype.HMAP) -> int:
        """
        Сменить идентификатор открытых данных в контексте отображения
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
        
        :param _hmap: идентификатор открытых данных (документа) Применяется для последовательной отрисовки в многопоточном варианте в буфер изображения одного контекста из нескольких ``HMAP`` для наложения слоев
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetPaintControlMapHandle_t (_hpaint, _hmap)

    mapSetPaintControlProjection_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetPaintControlProjection', maptype.HPAINT, ctypes.c_long)
    def mapSetPaintControlProjection(_hpaint: maptype.HPAINT, _epsgcode: int) -> int:
        """
        Установить параметры системы координат документа в контексте отображения
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
        
        :param _epsgcode: код ``EPSG`` для требуемой системы координат (например, ``3395``, ``3857``, ``4326``) Применяется для установки системы координат формируемого изображения по коду ``EPSG``
        
        :returns: Для геодезических систем координат возвращает 2, для плоских прямоугольных возвращает 1 При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetPaintControlProjection_t (_hpaint, _epsgcode)

    mapSetPaintControlProjectionEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetPaintControlProjectionEx', maptype.HPAINT, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapSetPaintControlProjectionEx(_hpaint: maptype.HPAINT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        """
        Установить параметры системы координат документа в контексте отображения
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения или поиска
        
        :param _mapreg: параметры проекции или ``0``
        
        :param _datum: параметры датума или ``0``
        
        :param _ellipsoid: параметры эллипсоида или ``0`` Применяется для установки системы координат формируемого изображения
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetPaintControlProjectionEx_t (_hpaint, _mapreg, _datum, _ellipsoid)

    mapSetPaintControlDrawList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetPaintControlDrawList', maptype.HPAINT, ctypes.c_void_p)
    def mapSetPaintControlDrawList(_hpaint: maptype.HPAINT, _drawList: ctypes.c_void_p) -> int:
        """
        Установить параметры рисования объектов новыми примитивами
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
        
        :param _drawList: список примитивов (``DRAWOBJECT``) и условий их отбора для рисования объектов на карте Создать drawList можно с помощью функции mapCreatePaintDrawList (maprscex.h). Объекты, не вошедшие в список, рисуются согласно условным знакам классификатора Добавить объекты в список можно с помощью функции mapAppendDrawToDrawList или в автоматическом режиме функцией gmlCreatePaintDrawListByOgcSld (gmlapi.h) Параметры устанавливаются для текущего контекста рисования Для отключения рисования объектов новыми примитивами необходим вызов mapSetPaintControlDrawList(hPaint, ``0``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetPaintControlDrawList_t (_hpaint, _drawList)

    mapGetPaintControlMapHandle_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapGetPaintControlMapHandle', maptype.HPAINT)
    def mapGetPaintControlMapHandle(_hpaint: maptype.HPAINT) -> maptype.HMAP:
        """
        Запросить идентификатор открытых данных, для которых создан контекст отображения
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HMAP
        """
        return mapGetPaintControlMapHandle_t (_hpaint)

    mapCopyPaintControlToXImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCopyPaintControlToXImage', maptype.HPAINT, ctypes.POINTER(maptype.XIMAGEDESC))
    def mapCopyPaintControlToXImage(_hpaint: maptype.HPAINT, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC)) -> int:
        """
        Скопировать содержимое внутреннего буфера в заданную область
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
        
        :param _imagedesc: описание выходного буфера изображения
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCopyPaintControlToXImage_t (_hpaint, _imagedesc)

    mapGetXImageDescForMapDibPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetXImageDescForMapDibPro', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), maptype.HPAINT)
    def mapGetXImageDescForMapDibPro(_hmap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _hpaint: maptype.HPAINT) -> int:
        """
        Получить описание внутреннего буфера в виде структуры XIMAGEDESC
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _imagedesc: поле для записи описания внутреннего буфера изображения
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска или ``0`` Формат хранения изображения остается: для Linux нисходящий ``DIB``, для Windows - восходящий Описание буфера может измениться (увеличение размера) в процессе выполнения функций отрисовки В буфер будет выполнено отображение документа при вызове функций отрисовки с идентификатором контекста устройства (``HDC``) равным ``0``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetXImageDescForMapDibPro_t (_hmap, _imagedesc, _hpaint)

    mapGetPaintErrorCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetPaintErrorCode', maptype.HPAINT)
    def mapGetPaintErrorCode(_hpaint: maptype.HPAINT) -> int:
        """
        Запросить код ошибки, возникшей при рисовании
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
        
        :returns: В случае успеха возвращает ноль, иначе код ошибки
        :rtype: int
        """
        return mapGetPaintErrorCode_t (_hpaint)

    mapPaintByFrameToFilePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPaintByFrameToFilePro', maptype.HMAP, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.DFRAME), ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.HSELECT, maptype.HPAINT)
    def mapPaintByFrameToFilePro(_hmap: maptype.HMAP, _filename: mapsyst.WTEXT, _erase: int, _frame: ctypes.POINTER(maptype.DFRAME), _width: int, _height: int, _alpha: int, _viewselect: maptype.HSELECT, _hpaint: maptype.HPAINT) -> int:
        """
        Отобразить фрагмент карты и сохранить в файл png
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _filename: полное имя создаваемого файла формата png или ``0``
        
        :param _erase: признак стирания фона перед выводом: ``0`` - фон не стирать, !``= 0`` - очистить фрагмент цветом фона, для экранного способа вывода (``VT_SCREEN``) всегда стирает цветом фона, кроме значения -``2``
        
        :param _frame: координаты фрагмента карты в системе координат документа в метрах, изменяется в mapSetDocProjection()
        
        :param _width: ширина изображения в пикселах
        
        :param _height: высота изображения в пикселах
        
        :param _alpha: флаг использования альфа канала: ``0`` - не использовать ``1`` - использовать
        
        :param _viewselect: условия отбора отображаемых объектов, если равно ``0``, то применяются условия обобщенного поиска\\выделения (внутренние)
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска Данная функция может изменять текущий масштаб отображения документа (если hPaint равен ``0``), для сохранения текущего масштаба можно применить функции mapGetRealShowScale/mapSetRealShowScale
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPaintByFrameToFilePro_t (_hmap, _filename.buffer(), _erase, _frame, _width, _height, _alpha, _viewselect, _hpaint)

    mapPaintDocToXImageEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPaintDocToXImageEx', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.LRECT), ctypes.c_long)
    def mapPaintDocToXImageEx(_hmap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _erase: int, _w: int, _h: int, _rect: ctypes.POINTER(maptype.LRECT), _alpha: int) -> int:
        """
        Отобразить фрагмент карты и врезки (Inset)в буфер изображения в области памяти
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _imagedesc: описание выходного буфера изображения
        
        :param _erase: признак стирания фона перед выводом: ``0`` - фон не стирать, !``= 0`` - очистить фрагмент цветом фона, для экранного способа вывода (``VT_SCREEN``) всегда стирает цветом фона, кроме значения -``2`` (минус ``2``)
        
        :param _w: положение левой верхней точки заполняемой области в буфере по ширине или ``0``
        
        :param _h: положение левой верхней точки заполняемой области в буфере по высоте или ``0``
        
        :param _rect: координаты фрагмента карты в изображении в пикселах
        
        :param _alpha: флаг использования альфа канала: ``0`` - не использовать ``1`` - использовать (фон прозрачный согласно значению альфа в BackColor/BackPrintColor)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPaintDocToXImageEx_t (_hmap, _imagedesc, _erase, _w, _h, _rect, _alpha)

    mapPaintMapObjectToXImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPaintMapObjectToXImage', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.LRECT), ctypes.POINTER(mapgdi.PAINTPARM), maptype.HOBJ)
    def mapPaintMapObjectToXImage(_hmap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _erase: int, _w: int, _h: int, _rect: ctypes.POINTER(maptype.LRECT), _image: ctypes.POINTER(mapgdi.PAINTPARM), _hobj: maptype.HOBJ) -> int:
        """
        Отобразить объект в буфер изображения в области памяти
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _imagedesc: описание выходного буфера изображения
        
        :param _erase: признак предварительной очистки фона изображения: ``0`` - фон не стирать, ``1`` - очистить фрагмент цветом фона, -``2`` - выполнить отображение поверх существующего изображения
        
        :param _w: положение левой верхней точки заполняемой области в буфере по ширине или ``0``
        
        :param _h: положение левой верхней точки заполняемой области в буфере по высоте или ``0``
        
        :param _rect: координаты фрагмента карты в изображении в пикселах
        
        :param _image: описание вида объекта (см. ``MAPGDI``.H), если объект должен рисоваться своим условным знаком,
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке в параметрах возвращает ноль
        :rtype: int
        
        .. note::

           то значение параметра можно установить в ноль
        """
        return mapPaintMapObjectToXImage_t (_hmap, _imagedesc, _erase, _w, _h, _rect, _image, _hobj)

    mapPaintByFrameToXImagePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPaintByFrameToXImagePro', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_long, ctypes.POINTER(maptype.DFRAME), ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.HSELECT, maptype.HPAINT)
    def mapPaintByFrameToXImagePro(_hmap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _erase: int, _frame: ctypes.POINTER(maptype.DFRAME), _width: int, _height: int, _alpha: int, _viewselect: maptype.HSELECT, _hpaint: maptype.HPAINT) -> int:
        """
        Отобразить фрагмент карты в буфер изображения, смасштабировав до заданной ширины и высоты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _imagedesc: описание выходного буфера изображения
        
        :param _erase: признак стирания фона перед выводом: ``0`` - фон не стирать, !``= 0`` - очистить фрагмент цветом фона, для экранного способа вывода (``VT_SCREEN``) всегда стирает цветом фона, кроме значения -``2`` (минус ``2``))
        
        :param _frame: координаты фрагмента карты в системе координат документа в метрах
        
        :param _width: ширина изображения в пикселах
        
        :param _height: высота изображения в пикселах
        
        :param _alpha: флаг использования альфа канала: ``0`` - не использовать ``1`` - использовать
        
        :param _viewselect: условия отбора объектов, если равны ``0``, то применяются условия обобщенного поиска\\выделения
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
        
        :returns: При ошибке в параметрах возвращает ноль
        :rtype: int
        """
        return mapPaintByFrameToXImagePro_t (_hmap, _imagedesc, _erase, _frame, _width, _height, _alpha, _viewselect, _hpaint)

    mapPaintLabelsByFrameToXImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPaintLabelsByFrameToXImage', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_long, ctypes.POINTER(maptype.DFRAME), ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.HPAINT)
    def mapPaintLabelsByFrameToXImage(_hmap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _erase: int, _frame: ctypes.POINTER(maptype.DFRAME), _width: int, _height: int, _alpha: int, _hpaint: maptype.HPAINT) -> int:
        """
        Отобразить динамические подписи карты в буфер изображения, смасштабировав до заданной ширины и высоты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _imagedesc: описание выходного буфера изображения
        
        :param _erase: признак стирания фона перед выводом: ``0`` - фон не стирать, !=``0`` - очистить фрагмент цветом фона, всегда стирает цветом фона, кроме значения -``2`` (минус ``2``)
        
        :param _frame: координаты фрагмента карты в системе координат документа в метрах
        
        :param _width: ширина изображения в пикселах
        
        :param _height: высота изображения в пикселах
        
        :param _alpha: флаг использования альфа канала: ``0`` - не использовать (для WinGDI), ``1`` - использовать
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
        
        :returns: При ошибке в параметрах возвращает ноль
        :rtype: int
        """
        return mapPaintLabelsByFrameToXImage_t (_hmap, _imagedesc, _erase, _frame, _width, _height, _alpha, _hpaint)

    mapPaintToXImageProL_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPaintToXImageProL', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.LRECT), maptype.HPAINT)
    def mapPaintToXImageProL(_hmap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _erase: int, _w: int, _h: int, _rect: ctypes.POINTER(maptype.LRECT), _hpaint: maptype.HPAINT) -> int:
        """
        Отобразить фрагмент карты в буфер изображения в области памяти
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _imagedesc: описание выходного буфера изображения
        
        :param _erase: признак стирания фона перед выводом: ``0`` - фон не стирать, !``= 0`` - очистить фрагмент цветом фона, для экранного способа вывода (``VT_SCREEN``) всегда стирает цветом фона, кроме значения -``2`` (минус ``2``)
        
        :param _w: положение левой верхней точки заполняемой области в буфере по ширине или ``0``
        
        :param _h: положение левой верхней точки заполняемой области в буфере по высоте или ``0``
        
        :param _rect: координаты фрагмента карты в изображении в пикселах
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
        
        :returns: При ошибке в параметрах возвращает ноль
        :rtype: int
        """
        return mapPaintToXImageProL_t (_hmap, _imagedesc, _erase, _w, _h, _rect, _hpaint)

    mapPaintUserObjectToXImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPaintUserObjectToXImage', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.RECT), ctypes.POINTER(mapgdi.PAINTPARM), ctypes.POINTER(mapgdi.PLACEDATA), ctypes.c_long)
    def mapPaintUserObjectToXImage(_hmap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _w: int, _h: int, _rect: ctypes.POINTER(maptype.RECT), _image: ctypes.POINTER(mapgdi.PAINTPARM), _data: ctypes.POINTER(mapgdi.PLACEDATA), _place: int) -> int:
        """
        Отобразить объект заданным видом в буфер изображения в области памяти
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _imagedesc: описание выходного буфера изображения
        
        :param _w: положение левой верхней точки заполняемой области в буфере по ширине или ``0``
        
        :param _h: положение левой верхней точки заполняемой области в буфере по высоте или ``0``
        
        :param _rect: координаты фрагмента карты в изображении в пикселах
        
        :param _image: описание вида объекта (структуры описаны в mapgdi.h),
        
        :param _data: координаты объекта,
        
        :param _place: вид системы координат: ``PP_PICTURE`` - в точках экрана, ``PP_PLANE`` - в метрах в системе координат документа, ``PP_GEO`` - в радианах на эллипсоиде документа
        
        :returns: При ошибке в параметрах возвращает ноль
        :rtype: int
        """
        return mapPaintUserObjectToXImage_t (_hmap, _imagedesc, _w, _h, _rect, _image, _data, _place)

    mapPaintSelectToXImageEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPaintSelectToXImageEx', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.RECT), maptype.HSELECT, maptype.COLORREF, ctypes.c_long, maptype.HPAINT, ctypes.c_long)
    def mapPaintSelectToXImageEx(_hmap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _w: int, _h: int, _rect: ctypes.POINTER(maptype.RECT), _hselect: maptype.HSELECT, _color: maptype.COLORREF, _alpha: int, _hpaint: maptype.HPAINT, _erase: int) -> int:
        """
        Отобразить выделенные объекты в буфер изображения в области памяти
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _imagedesc: описание выходного буфера изображения
        
        :param _w: положение левой верхней точки заполняемой области в буфере по ширине или ``0``
        
        :param _h: положение левой верхней точки заполняемой области в буфере по высоте или ``0``
        
        :param _rect: координаты фрагмента карты в изображении в пикселах
        
        :param _hselect: условие отбора выделенных объектов
        
        :param _color: цвет выделения объектов
        
        :param _alpha: флаг использования альфа канала: ``0`` - не использовать (для WinGDI), ``1`` - использовать
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
        
        :param _erase: признак стирания фона перед выводом: ``0`` - фон не стирать, !``= 0`` - очистить фрагмент цветом фона, для экранного способа вывода (``VT_SCREEN``) всегда стирает цветом фона, кроме значения -``2`` (минус ``2``)
        
        :returns: При ошибке в параметрах возвращает ноль
        :rtype: int
        """
        return mapPaintSelectToXImageEx_t (_hmap, _imagedesc, _w, _h, _rect, _hselect, _color, _alpha, _hpaint, _erase)

    mapPaintSelectByFrameToXImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPaintSelectByFrameToXImage', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_long, ctypes.POINTER(maptype.DFRAME), ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.HSELECT, maptype.HPAINT, maptype.COLORREF)
    def mapPaintSelectByFrameToXImage(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _erase: int, _frame: ctypes.POINTER(maptype.DFRAME), _width: int, _height: int, _alpha: int, _hselect: maptype.HSELECT, _hpaint: maptype.HPAINT, _color: maptype.COLORREF) -> int:
        """
        Отобразить карту и выделенные объекты в буфер изображения, смасштабировав до заданной ширины и высоты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в документе, для фоновой карты равен hmap
        
        :param _imagedesc: описание выходного буфера изображения
        
        :param _erase: признак стирания фона перед выводом: ``0`` - фон не стирать, !``= 0`` - очистить фрагмент цветом фона, для экранного способа вывода (``VT_SCREEN``) всегда стирает цветом фона, кроме значения -``2`` (минус ``2``)
        
        :param _frame: координаты фрагмента карты в системе координат документа в метрах
        
        :param _width: ширина изображения в пикселах
        
        :param _height: высота изображения в пикселах
        
        :param _alpha: флаг использования альфа канала: ``0`` - не использовать (для WinGDI), ``1`` - использовать
        
        :param _hselect: условие отбора для выделенных объектов
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
        
        :param _color: цвет выделения объектов
        
        :returns: При ошибке в параметрах возвращает ноль
        :rtype: int
        """
        return mapPaintSelectByFrameToXImage_t (_hmap, _hsite, _imagedesc, _erase, _frame, _width, _height, _alpha, _hselect, _hpaint, _color)

    mapPaintAndSelectToXImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPaintAndSelectToXImage', maptype.HMAP, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.RECT), maptype.HSELECT, maptype.COLORREF)
    def mapPaintAndSelectToXImage(_hmap: maptype.HMAP, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _w: int, _h: int, _rect: ctypes.POINTER(maptype.RECT), _hselect: maptype.HSELECT, _color: maptype.COLORREF) -> int:
        """
        Отобразить фрагмент карты и выделенные объекты в буфер изображения в области памяти
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _imagedesc: описание выходного буфера изображения
        
        :param _w: положение левой верхней точки заполняемой области в буфере по ширине или ``0``
        
        :param _h: положение левой верхней точки заполняемой области в буфере по высоте или ``0``
        
        :param _rect: координаты фрагмента карты в изображении в пикселах
        
        :param _hselect: условие отбора выделенных объектов, если равно нулю и установлено mapSetTotalSelectFlag(),
        
        :param _color: цвет, которым будут выделяться объекты на карте
        
        :returns: При ошибке в параметрах возвращает ноль
        :rtype: int
        
        .. note::

           то применяются условия обобщенного поиска\\выделения
        """
        return mapPaintAndSelectToXImage_t (_hmap, _imagedesc, _w, _h, _rect, _hselect, _color)

    mapPaintDrawObjectToFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPaintDrawObjectToFile', maptype.HOBJ, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapPaintDrawObjectToFile(_hobj: maptype.HOBJ, _width: int, _height: int, _filename: mapsyst.WTEXT, _transparentColor: int) -> int:
        """
        Вывести изображение графического объекта в файл
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _width: ширина изображения в пикселах кратная ``16``
        
        :param _height: высота изображения в пикселах
        
        :param _filename: имя файла для сохранения
        
        :param _transparentColor: цвет прозрачного фона
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPaintDrawObjectToFile_t (_hobj, _width, _height, _filename.buffer(), _transparentColor)

    mapSetTextQuality_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetTextQuality', ctypes.c_long)
    def mapSetTextQuality(_mode: int) -> int:
        """
        Установить уровень качественного отображения подписей при печати
        
        :param _mode: уровень рисования подписей: ``0`` - рисование подписи без уточнения длины (быстрое рисование) ``1`` - рисование подписи с уточнением длины (пропорционально масштабу) ``2`` - рисование подписи с уточнением длины и короткими пробелами после знаков препинания и цифровых символов При старте программы установлен режим ``1``
        
        :returns: Возвращает предыдущее значение
        :rtype: int
        """
        return mapSetTextQuality_t (_mode)

    mapGetTextQuality_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetTextQuality')
    def mapGetTextQuality() -> int:
        """
        Запросить значение уровня качественного отображения подписей
        """
        return mapGetTextQuality_t ()

    mapGetViewListCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetViewListCount', maptype.HMAP)
    def mapGetViewListCount(_hmap: maptype.HMAP) -> int:
        """
        Запросить число элементов в списке наборов данных
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: Если возвращается нулевое значение, то список отображения не активен При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetViewListCount_t (_hmap)

    mapGetViewListItemName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetViewListItemName', maptype.HMAP, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetViewListItemName(_hmap: maptype.HMAP, _index: int, _itemname: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить название элемента (путь к набору данных) и тип в списке наборов данных
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _index: номер элемента с ``1`` до mapGetViewListCount()
        
        :param _itemname: указатель на буфер для записи пути к набору данных или алиаса данных
        
        :param _size: размер буфера в байтах
        
        :returns: Возвращает один из следующих типов данных: FILE_MAP, FILE_RSW, FILE_MTW, FILE_MTQ, FILE_MTL, FILE_MTD, FILE_TIN, FILE_WMS При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetViewListItemName_t (_hmap, _index, _itemname.buffer(), _size)

    mapGetViewListItemNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetViewListItemNumber', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapGetViewListItemNumber(_hmap: maptype.HMAP, _index: int, _number: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить тип набора данных и его порядковый номер с 1 в списке данных этого типа
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _index: номер элемента с ``1`` до mapGetViewListCount()
        
        :param _number: поле для записи порядкового номера с ``1``
        
        :returns: Возвращает один из следующих типов данных: FILE_MAP, FILE_RSW, FILE_MTW, FILE_MTQ, FILE_MTL, FILE_MTD, FILE_TIN, FILE_WMS При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetViewListItemNumber_t (_hmap, _index, _number)

    mapSetViewListItemPosition_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetViewListItemPosition', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetViewListItemPosition(_hmap: maptype.HMAP, _index: int, _position: int) -> int:
        """
        Переместить элемент в списке наборов данных в позицию перед элементом с заданным номером
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _index: номер перемещаемого элемента с ``1`` до mapGetViewListCount()
        
        :param _position: номер опорного элемента в списке с ``1`` до mapGetViewListCount() + ``1``, перед которым будет размещен перемещаемый элемент
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если position равен mapGetViewListCount() + 1, то элемент переместится в конец списка
           Если элемент перемещается к началу списка (position < index), то его новый номер
           будет равен указанному (position)
           Если элемент перемещается к концу списка (position > index + 1), то его новый номер
           будет на 1 меньше указанного, чтобы элемент встал перед опорным элементом
           Если номер опорного элемента на 1 больше номера перемещаемого элемента (position = index + 1),
           то перемещаемый элемент будет размещен за опорным элементом
        """
        return mapSetViewListItemPosition_t (_hmap, _index, _position)

    mapGetViewListItemIdent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetViewListItemIdent', maptype.HMAP, ctypes.c_long)
    def mapGetViewListItemIdent(_hmap: maptype.HMAP, _index: int) -> int:
        """
        Запросить идентификатор элемента в списке наборов данных
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _index: номер элемента с ``1`` до mapGetViewListCount()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetViewListItemIdent_t (_hmap, _index)

    mapGetViewListItemIndex_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetViewListItemIndex', maptype.HMAP, ctypes.c_long)
    def mapGetViewListItemIndex(_hmap: maptype.HMAP, _ident: int) -> int:
        """
        Запросить номер элемента в списке наборов данных
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _ident: идентификатор элемента
        
        :returns: Возвращает значение от 1 до mapGetViewListCount() При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetViewListItemIndex_t (_hmap, _ident)

    mapGetViewListItemGuid_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.INTQUAD),'mapGetViewListItemGuid', maptype.HMAP, ctypes.c_long)
    def mapGetViewListItemGuid(_hmap: maptype.HMAP, _ident: int) -> ctypes.POINTER(maptype.INTQUAD):
        """
        Запросить GUID элемента в списке наборов данных
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _ident: идентификатор элемента
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(maptype.INTQUAD)
        """
        return mapGetViewListItemGuid_t (_hmap, _ident)

    mapGetViewListItemViewFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetViewListItemViewFlag', maptype.HMAP, ctypes.c_long)
    def mapGetViewListItemViewFlag(_hmap: maptype.HMAP, _index: int) -> int:
        """
        Запросить флаг отображения для элемента списка отображения
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _index: номер элемента с ``1`` до mapGetViewListCount()
        
        :returns: Если элемент не отображается возвращает ноль
        :rtype: int
        """
        return mapGetViewListItemViewFlag_t (_hmap, _index)

    mapSetViewListItemViewFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetViewListItemViewFlag', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetViewListItemViewFlag(_hmap: maptype.HMAP, _index: int, _view: int) -> int:
        """
        Установить флаг отображения для элемента списка отображения
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _index: номер элемента с ``1`` до mapGetViewListCount()
        
        :param _view: флаг отображения элемента: ``0`` или ``1``
        """
        return mapSetViewListItemViewFlag_t (_hmap, _index, _view)

    mapGetViewListItemRangeScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetViewListItemRangeScale', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapGetViewListItemRangeScale(_hmap: maptype.HMAP, _index: int, _bottom: ctypes.POINTER(ctypes.c_long), _top: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить границы видимости отображения для элемента списка отображения
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _index: номер элемента с ``1`` до mapGetViewListCount()
        
        :param _bottom: поле для записи масштаба нижней границы отображения (от ``1:1``)
        
        :param _top: поле для записи масштаба верхней границы отображения (до ``1: 250 000 000``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetViewListItemRangeScale_t (_hmap, _index, _bottom, _top)

    mapSetViewListItemRangeScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetViewListItemRangeScale', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSetViewListItemRangeScale(_hmap: maptype.HMAP, _index: int, _bottom: int, _top: int) -> int:
        """
        Установить границы видимости отображения для элемента списка отображения
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _index: номер элемента с ``1`` до mapGetViewListCount()
        
        :param _bottom: масштаб нижней границы отображения (от ``1:1``)
        
        :param _top: масштаб верхней границы отображения (до ``1: 250 000 000``)
        """
        return mapSetViewListItemRangeScale_t (_hmap, _index, _bottom, _top)

    mapGetViewListState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetViewListState', maptype.HMAP)
    def mapGetViewListState(_hmap: maptype.HMAP) -> int:
        """
        Запросить номер состояния списка наборов данных
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           После изменения состава данных или порядка отображения номер состояния данных увеличивается
        """
        return mapGetViewListState_t (_hmap)

    mapResetViewList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapResetViewList', maptype.HMAP)
    def mapResetViewList(_hmap: maptype.HMAP) -> int:
        """
        Перезаполнить список по стандартному расположению по типам наборов данных (матрицы, снимки, векторные карты)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapResetViewList_t (_hmap)

    mapSetViewListAccess_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetViewListAccess', maptype.HMAP, ctypes.c_long)
    def mapSetViewListAccess(_hmap: maptype.HMAP, _viewlistaccess: int) -> ctypes.c_void_p:
        """
        Включить или отключить отображение документа по общему списку данных
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _viewlistaccess: признак отображения документа по общему списку данных: ``0`` или ``1``
        """
        return mapSetViewListAccess_t (_hmap, _viewlistaccess)

    mapSetupTurn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSetupTurn', maptype.HMAP, ctypes.c_double, ctypes.c_double)
    def mapSetupTurn(_hmap: maptype.HMAP, _angle: float, _fixation: float) -> float:
        """
        Функция настройки отображения карты с поворотом
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _angle: угол поворота карты в плане с вершиной в юго-западном углу карты (от -Pi до Pi)
        
        :param _fixation: угол сектора фиксации поворота отображения карты относительно предыдущего положения (от ``0`` до Pi/``6``) Угол fixation используется для минимизации дрожания изображения при движении по повернутой карте по прямой (или почти по прямой), когда при последовательном вызове функции подаются близкие значения угла поворота (angle). В случае, если разность между текущим углом поворота и требуемым будет меньше fixation,
        
        :returns: Возвращает значение установленного угла поворота При ошибке возвращает 0
        :rtype: float
        
        .. note::

           то новый угол поворота не устанавливается
           hpaint - идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
           Автоматически вызывает функцию mapSetRegion для обновления габаритов документа
        """
        return mapSetupTurn_t (_hmap, _angle, _fixation)

    mapSetupTurnEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSetupTurnEx', maptype.HMAP, ctypes.c_double, ctypes.c_double, maptype.HPAINT)
    def mapSetupTurnEx(_hmap: maptype.HMAP, _angle: float, _fixation: float, _hPaint: maptype.HPAINT) -> float:
        return mapSetupTurnEx_t (_hmap, _angle, _fixation, _hPaint)

    mapTurnIsActive_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapTurnIsActive', maptype.HMAP)
    def mapTurnIsActive(_hmap: maptype.HMAP) -> int:
        """
        Запросить, установлен ли поворот
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: Возвращает: ``1`` - активен, ``0`` - нет
        :rtype: int
        """
        return mapTurnIsActive_t (_hmap)

    mapGetTurnAngle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetTurnAngle', maptype.HMAP)
    def mapGetTurnAngle(_hmap: maptype.HMAP) -> float:
        """
        Запросить угол поворота
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: Возвращает значение от -Pi до Pi
        :rtype: float
        """
        return mapGetTurnAngle_t (_hmap)

    mapSetRealScalePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRealScalePro', maptype.HMAP, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long), ctypes.c_double, maptype.HPAINT)
    def mapSetRealScalePro(_hmap: maptype.HMAP, _wx: ctypes.POINTER(ctypes.c_long), _hy: ctypes.POINTER(ctypes.c_long), _scale: float, _hpaint: maptype.HPAINT) -> int:
        """
        Установить масштаб отображения
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _wx: координата x в пикселах по горизонтали любой точки привязки в текущем масштабе или ``0``
        
        :param _hy: координата y в пикселах по вертикали любой точки привязки в текущем масштабе или ``0``
        
        :param _scale: реальный масштаб отображения, который желают получить
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
        
        :returns: Возвращает: ``0`` - масштаб не изменился, ``1`` - масштаб изменился Координаты в пикселах обновляются с учетом изменения маштаба При изменении масштаба отображения меняются общие габариты изображения в пикселах При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRealScalePro_t (_hmap, _wx, _hy, _scale, _hpaint)

    mapGetRealScalePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetRealScalePro', maptype.HPAINT)
    def mapGetRealScalePro(_hpaint: maptype.HPAINT) -> float:
        """
        Запросить масштаб отображения контекста отображения
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
        
        :returns: Возвращает значение знаменателя масштаба При ошибке возвращает 1
        :rtype: float
        """
        return mapGetRealScalePro_t (_hpaint)

    mapSetRealScalePrint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRealScalePrint', maptype.HMAP, ctypes.c_double, maptype.HPAINT, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_long)
    def mapSetRealScalePrint(_hmap: maptype.HMAP, _scale: float, _hpaint: maptype.HPAINT, _horpix: ctypes.POINTER(ctypes.c_double), _verpix: ctypes.POINTER(ctypes.c_double), _wmsscaleflag: int) -> int:
        """
        Установить масштаб отображения (знаменатель масштаба)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _scale: реальный масштаб отображения, который желают получить
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
        
        :param _horpix: число пикселов в метре по горизонтали или ``0``
        
        :param _verpix: число пикселов в метре по вертикали или ``0``
        
        :param _wmsscaleflag: признак выполнения согласования масштаба с масштабом геопортала (уровнями отображения)
        
        :returns: Возвращает: ``0`` - масштаб не изменился, ``1`` - масштаб изменился
        :rtype: int
        """
        return mapSetRealScalePrint_t (_hmap, _scale, _hpaint, _horpix, _verpix, _wmsscaleflag)

    mapGetRealShowScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetRealShowScale', maptype.HMAP)
    def mapGetRealShowScale(_hmap: maptype.HMAP) -> float:
        """
        Запросить масштаб отображения карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: Возвращает значение знаменателя масштаба
        :rtype: float
        """
        return mapGetRealShowScale_t (_hmap)

    mapSetRealShowScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSetRealShowScale', maptype.HMAP, ctypes.c_double)
    def mapSetRealShowScale(_hmap: maptype.HMAP, _scale: float) -> float:
        """
        Установить масштаб отображения карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _scale: реальный масштаб отображения, который желают получить
        
        :returns: Возвращает значение знаменателя масштаба
        :rtype: float
        """
        return mapSetRealShowScale_t (_hmap, _scale)

    mapGetDrawScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetDrawScale', maptype.HMAP)
    def mapGetDrawScale(_hmap: maptype.HMAP) -> float:
        """
        Запросить текущий коэффициент масштабирования карты
        
        :param _hmap: идентификатор открытых данных (документа) Например: ``5`` - растянута в ``5`` раз относительно базового масштаба, ``0.1`` - сжата в ``10`` раз.
        """
        return mapGetDrawScale_t (_hmap)

    mapScaleToRoundScaleReal_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapScaleToRoundScaleReal', maptype.HMAP, ctypes.c_double)
    def mapScaleToRoundScaleReal(_hmap: maptype.HMAP, _scale: float) -> float:
        """
        Подобрать "стандартный" реальный масштаб, ближайший к заданному (scale)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _scale: масштаб отображения, который желают получить Масштаб подбираетсмя с учетом состава открытых данных, например ``WMTS`` могут быть другие стандартные масштабы
        
        :returns: Возвращает новое реальное (неокругленное) значение знаменателя масштаба
        :rtype: float
        """
        return mapScaleToRoundScaleReal_t (_hmap, _scale)

    mapSetScaleMethod_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetScaleMethod', ctypes.c_long)
    def mapSetScaleMethod(_method: int) -> int:
        """
        Установить способ масштабирования объектов карты при отображении
        
        :param _method: способ масштабирования: ``0`` - картографический ``"с запаздыванием увеличения"``, ``1`` - чертежный
        
        :returns: Возвращает ранее установленное значение
        :rtype: int
        """
        return mapSetScaleMethod_t (_method)

    mapGetScaleMethod_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetScaleMethod')
    def mapGetScaleMethod() -> int:
        """
        Запросить способ масштабирования объектов карты при отображении
        
        :returns: Возвращает ранее установленное значение
        :rtype: int
        """
        return mapGetScaleMethod_t ()

    mapShowAllObjects_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapShowAllObjects', ctypes.c_long)
    def mapShowAllObjects(_flag: int) -> int:
        """
        Установить отображение объектов карт без учета границ видимости и состава
        
        :param _flag: признак установки флага: ``1`` - установить, ``0`` - сбросить Доступно только в составе ГИС
        
        :returns: Возвращает ранее установленное значение
        :rtype: int
        """
        return mapShowAllObjects_t (_flag)

    mapIsShowAllObjects_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsShowAllObjects')
    def mapIsShowAllObjects() -> int:
        """
        Запросить флаг отображение объектов карт без учета границ видимости и состава
        
        Доступно только в составе ГИС
        
        :returns: Возвращает ранее установленное значение в mapShowAllObjects()
        :rtype: int
        """
        return mapIsShowAllObjects_t ()

    mapCreateImageEx_t = mapsyst.GetProcAddress(acceslib,maptype.HIMAGE,'mapCreateImageEx', ctypes.c_long, ctypes.c_long)
    def mapCreateImageEx(_width: int, _height: int) -> maptype.HIMAGE:
        """
        Создать буфер образа окна карты в памяти для исключения мигания перемещаемых по карте объектов
        
        :param _width: ширина клиентской части окна карты в точках
        
        :param _height: высота клиентской части окна карты в точках Создается первый буфер экрана, второй создается при первом вызове функции отображения объекта в буфер (Draw) -  для оптимального применения функций при отображении карты и без перемещаемых объектов Размер одного буфера в байтах - width ``*`` height ``* 4`` ( ``1920*1080*`` ``4`` = ``8 294 400``, для ``3`` - ``24 883 200``) Всего может быть параллельно открыто до ``1024`` образов экранов одновременно Может применяться в паре с функцией mapChangeImageSizeEx
        
        :returns: При успешном выполнении возвращает идентификатор образа экрана При ошибке возвращает ноль
        :rtype: maptype.HIMAGE
        """
        return mapCreateImageEx_t (_width, _height)

    mapCloseImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseImage', maptype.HIMAGE)
    def mapCloseImage(_himage: maptype.HIMAGE) -> ctypes.c_void_p:
        """
        Удалить буфер образа окна карты
        
        :param _himage: идентификатор буфера окна
        """
        return mapCloseImage_t (_himage)

    mapCloseTotalSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseTotalSelect', maptype.HIMAGE)
    def mapCloseTotalSelect(_himage: maptype.HIMAGE) -> ctypes.c_void_p:
        """
        Удалить буфер выделенных объектов в буфере образа окна карты
        
        :param _himage: идентификатор буфера образа окна карты
        
        .. note::

           После удаления буфера выделенных объектов необходимо перерисовать буфер
           объектов, если он был открыт
        """
        return mapCloseTotalSelect_t (_himage)

    mapCloseObjectsImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseObjectsImage', maptype.HIMAGE)
    def mapCloseObjectsImage(_himage: maptype.HIMAGE) -> ctypes.c_void_p:
        """
        Удалить буфер объектов в буфере образа окна карты для ускорения отображения
        
        :param _himage: идентификатор буфера образа окна карты
        """
        return mapCloseObjectsImage_t (_himage)

    mapIsObjectsImageActive_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsObjectsImageActive', maptype.HIMAGE)
    def mapIsObjectsImageActive(_himage: maptype.HIMAGE) -> int:
        """
        Запросить - открыт ли буфер объектов
        
        :param _himage: идентификатор буфера образа окна карты
        """
        return mapIsObjectsImageActive_t (_himage)

    mapChangeImageSizeEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapChangeImageSizeEx', maptype.HIMAGE, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapChangeImageSizeEx(_himage: maptype.HIMAGE, _erase: int, _width: int, _height: int) -> int:
        """
        Обновить размеры буфера образа окна карты
        
        :param _himage: идентификатор буфера образа окна карты
        
        :param _erase: признак очистки окна, если равен ``0`` - содержимое сохраняется
        
        :param _width: новая ширина буфера
        
        :param _height: новая высота буфера
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapChangeImageSizeEx_t (_himage, _erase, _width, _height)

    mapClearMapImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapClearMapImage', maptype.HIMAGE)
    def mapClearMapImage(_himage: maptype.HIMAGE) -> int:
        """
        Очистить буфер образа окна карты
        
        :param _himage: идентификатор буфера образа окна карты
        
        :returns: При ошибке во входных параметрах возвращает ноль
        :rtype: int
        """
        return mapClearMapImage_t (_himage)

    mapClearObjectsImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapClearObjectsImage', maptype.HIMAGE, ctypes.POINTER(maptype.RECT))
    def mapClearObjectsImage(_himage: maptype.HIMAGE, _rect: ctypes.POINTER(maptype.RECT)) -> ctypes.c_void_p:
        """
        Очистить буфер объектов в буфере образа окна карты
        
        :param _himage: идентификатор буфера образа окна карты
        
        :param _rect: область очистки или ноль (очистить весь буфер)
        """
        return mapClearObjectsImage_t (_himage, _rect)

    mapGetImageWidth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetImageWidth', maptype.HIMAGE)
    def mapGetImageWidth(_himage: maptype.HIMAGE) -> int:
        """
        Запросить ширину буфера образа окна карты
        
        :param _himage: идентификатор буфера образа окна карты
        
        :returns: При ошибке во входные параметрах возвращает ноль
        :rtype: int
        """
        return mapGetImageWidth_t (_himage)

    mapGetImageHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetImageHeight', maptype.HIMAGE)
    def mapGetImageHeight(_himage: maptype.HIMAGE) -> int:
        """
        Запросить высоту буфера образа окна карты
        
        :param _himage: идентификатор буфера образа окна карты
        
        :returns: При ошибке во входные параметрах возвращает ноль
        :rtype: int
        """
        return mapGetImageHeight_t (_himage)

    mapViewImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapViewImage', maptype.HIMAGE, maptype.HDC, ctypes.POINTER(maptype.RECT))
    def mapViewImage(_himage: maptype.HIMAGE, _hdc: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT)) -> int:
        """
        Отобразить содержимое буфера образа окна карты в заданный контекст
        
        :param _himage: идентификатор буфера образа окна карты
        
        :param _hdc: контекст области отображения (окна),
        
        :param _rect: координаты область отображения в буфере и контексте
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapViewImage_t (_himage, _hdc, _rect)

    mapViewImageToXImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapViewImageToXImage', maptype.HIMAGE, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.POINTER(maptype.RECT), ctypes.POINTER(maptype.POINT))
    def mapViewImageToXImage(_himage: maptype.HIMAGE, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _rect: ctypes.POINTER(maptype.RECT), _offset: ctypes.POINTER(maptype.POINT)) -> int:
        """
        Отобразить содержимое буфера в заданный внешний XImage
        
        :param _himage: идентификатор буфера образа окна карты
        
        :param _imagedesc: описание выходного буфера изображения
        
        :param _rect: прямоугольник исходного изображения для копирования, если ``= 0`` - используется размер всего буфера
        
        :param _offset: верхняя левая точка области отображения в буфере, если ``= 0`` - копируется с координатами ``0``, ``0``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapViewImageToXImage_t (_himage, _imagedesc, _rect, _offset)

    mapCopyXImageToImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCopyXImageToImage', maptype.HIMAGE, ctypes.POINTER(maptype.XIMAGEDESC), ctypes.POINTER(maptype.RECT), ctypes.POINTER(maptype.POINT))
    def mapCopyXImageToImage(_himage: maptype.HIMAGE, _imagedesc: ctypes.POINTER(maptype.XIMAGEDESC), _rect: ctypes.POINTER(maptype.RECT), _offset: ctypes.POINTER(maptype.POINT)) -> int:
        """
        Отобразить в буфер объектов содержимое внешнего XImage
        
        :param _himage: идентификатор буфера образа окна карты
        
        :param _imagedesc: описание входного буфера изображения
        
        :param _rect: прямоугольник исходного изображения для копирования, если ``= 0`` - используется размер всего буфера
        
        :param _offset: точка для размещения прямоугольника в буфере объектов, если ``= 0`` - копируется с координатами {``0``, ``0``}
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCopyXImageToImage_t (_himage, _imagedesc, _rect, _offset)

    mapScrollImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapScrollImage', maptype.HIMAGE, ctypes.c_long, ctypes.c_long)
    def mapScrollImage(_himage: maptype.HIMAGE, _dx: int, _dy: int) -> int:
        """
        Скроллинг буфера образа окна карты
        
        :param _himage: идентификатор буфера образа окна карты
        
        :param _dx: величина смещения окна по горизонтали (``> 0`` - слева направо, ``< 0`` - справа налево)
        
        :param _dy: величина смещения окна по вертикали   (``> 0`` - сверху вниз, ``< 0`` - снизу вверх)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapScrollImage_t (_himage, _dx, _dy)

    mapClearScreenRect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapClearScreenRect', maptype.HIMAGE, ctypes.POINTER(maptype.RECT), maptype.COLORREF)
    def mapClearScreenRect(_himage: maptype.HIMAGE, _rect: ctypes.POINTER(maptype.RECT), _color: maptype.COLORREF) -> int:
        """
        Очистка буфера образа окна карты заданным цветом
        
        :param _himage: идентификатор буфера образа окна карты
        
        :param _rect: прямоугольник изображения для очистки
        
        :param _color: цвет, которым будет выполнена очистка
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapClearScreenRect_t (_himage, _rect, _color)

    mapDrawImageMapPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDrawImageMapPro', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(maptype.LRECT), ctypes.POINTER(maptype.POINT), maptype.HPAINT)
    def mapDrawImageMapPro(_himage: maptype.HIMAGE, _hmap: maptype.HMAP, _rect: ctypes.POINTER(maptype.LRECT), _position: ctypes.POINTER(maptype.POINT), _hpaint: maptype.HPAINT) -> int:
        """
        Обновить изображение заданного фрагмента карты в буфере образа окна карты
        
        :param _himage: идентификатор буфера образа окна карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _rect: обновляемый фрагмент карты, задается в пикселах в системе координат полного изображения карты (``PICTURE``)
        
        :param _position: положение верхнего левого угла фрагмента в клиентской области окна карты (и образа экрана) или ``0``
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           После обновления карты изображение перемещаемых объектов стирается
           в пределах заданного фрагмента (для стирания объектов текущим видом карты достаточно вызвать mapClearObjectsImage)
        """
        return mapDrawImageMapPro_t (_himage, _hmap, _rect, _position, _hpaint)

    mapDrawImageMapObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDrawImageMapObject', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(mapgdi.PAINTPARM), maptype.HOBJ)
    def mapDrawImageMapObject(_himage: maptype.HIMAGE, _hmap: maptype.HMAP, _parm: ctypes.POINTER(mapgdi.PAINTPARM), _hobj: maptype.HOBJ) -> int:
        """
        Отобразить объект поверх карты местности в буфере объектов образа окна карты
        
        :param _himage: идентификатор буфера образа окна карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _parm: параметры отображения объекта карты в буфере экрана (второй буфер)
        
        :param _hobj: идентификатор описания объекта в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDrawImageMapObject_t (_himage, _hmap, _parm, _hobj)

    mapDrawImageOffsetMapObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDrawImageOffsetMapObject', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(mapgdi.PAINTPARM), maptype.HOBJ)
    def mapDrawImageOffsetMapObject(_himage: maptype.HIMAGE, _hmap: maptype.HMAP, _offset: ctypes.POINTER(maptype.DOUBLEPOINT), _parm: ctypes.POINTER(mapgdi.PAINTPARM), _hobj: maptype.HOBJ) -> int:
        """
        Отобразить объект поверх карты местности в буфере объектов образа окна карты c учетом сдвига
        
        :param _himage: идентификатор буфера образа окна карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _offset: величина смещения изображения объекта в буфере от его реальных координат в метрах в текущей системе координат документа
        
        :param _parm: параметры отображения объекта карты в буфере экрана (второй буфер)
        
        :param _hobj: идентификатор описания объекта в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDrawImageOffsetMapObject_t (_himage, _hmap, _offset, _parm, _hobj)

    mapDrawImageUserObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDrawImageUserObject', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(mapgdi.PAINTPARM), ctypes.POINTER(mapgdi.PLACEDATA), ctypes.c_long)
    def mapDrawImageUserObject(_himage: maptype.HIMAGE, _hmap: maptype.HMAP, _parm: ctypes.POINTER(mapgdi.PAINTPARM), _data: ctypes.POINTER(mapgdi.PLACEDATA), _place: int) -> int:
        """
        Отобразить объект поверх карты местности в буфере образа окна карты
        
        :param _himage: идентификатор буфера образа окна карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _parm: параметры отображения объекта карты в буфере экрана (второй буфер)
        
        :param _data: список координат объекта в системе координат, заданной параметром place
        
        :param _place: вид системы координат: ``PP_PICTURE`` - в точках экрана, ``PP_PLANE`` - в метрах в системе координат документа, ``PP_GEO`` - в радианах на эллипсоиде документа
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDrawImageUserObject_t (_himage, _hmap, _parm, _data, _place)

    mapDrawImageOffsetUserObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDrawImageOffsetUserObject', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(mapgdi.PAINTPARM), ctypes.POINTER(mapgdi.PLACEDATA), ctypes.c_long)
    def mapDrawImageOffsetUserObject(_himage: maptype.HIMAGE, _hmap: maptype.HMAP, _offset: ctypes.POINTER(maptype.DOUBLEPOINT), _parm: ctypes.POINTER(mapgdi.PAINTPARM), _data: ctypes.POINTER(mapgdi.PLACEDATA), _place: int) -> int:
        """
        Отобразить объект поверх карты местности в буфере образа окна карты c учетом сдвига
        
        :param _himage: идентификатор буфера образа окна карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _offset: величина смещения изображения объекта в буфере от его реальных координат в системе координат, заданной параметром place
        
        :param _parm: параметры отображения объекта карты в буфере экрана (второй буфер)
        
        :param _data: список координат объекта в системе координат, заданной параметром place
        
        :param _place: вид системы координат (в точках экрана - ``PP_PICTURE``, в метрах в системе координат документа - ``PP_PLANE``, в радианах на эллипсоиде документа - ``PP_GEO``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDrawImageOffsetUserObject_t (_himage, _hmap, _offset, _parm, _data, _place)

    mapDrawImageGraphics_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDrawImageGraphics', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(maptype.DRAWPOINT), ctypes.c_long, ctypes.c_long, ctypes.c_char_p)
    def mapDrawImageGraphics(_himage: maptype.HIMAGE, _hmap: maptype.HMAP, _points: ctypes.POINTER(maptype.DRAWPOINT), _count: int, _type: int, _parm: ctypes.c_char_p) -> int:
        """
        Отобразить графические данные в буфере образа окна карты
        
        :param _himage: идентификатор буфера образа окна карты hScreen - идентификатор образа экрана
        
        :param _points: координаты в пикселах
        
        :param _count: число координат
        
        :param _type: тип графического примитива (см. mapgdi.h)
        
        :param _parm: параметры графического примитива
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDrawImageGraphics_t (_himage, _hmap, _points, _count, _type, _parm)

    mapDrawImageTextUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDrawImageTextUn', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(maptype.DRAWPOINT), ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapDrawImageTextUn(_himage: maptype.HIMAGE, _hmap: maptype.HMAP, _points: ctypes.POINTER(maptype.DRAWPOINT), _count: int, _text: mapsyst.WTEXT, _height: int, _color: int, _align: int) -> int:
        """
        Отобразить текстовую строку
        
        :param _himage: идентификатор буфера образа окна карты
        
        :param _points: координаты в пикселах
        
        :param _count: число координат
        
        :param _text: текст подписи
        
        :param _height: высота подписи в мкм
        
        :param _color: цвет подписи ``RGB``
        
        :param _align: флажки выравнивания текста (для -``1`` - ``FA_BASELINE``|``FA_LEFT``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDrawImageTextUn_t (_himage, _hmap, _points, _count, _text.buffer(), _height, _color, _align)

    mapDrawImageBitMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDrawImageBitMap', maptype.HIMAGE, maptype.HMAP, ctypes.POINTER(maptype.DRAWPOINT), ctypes.c_char_p, ctypes.c_long)
    def mapDrawImageBitMap(_himage: maptype.HIMAGE, _hmap: maptype.HMAP, _point: ctypes.POINTER(maptype.DRAWPOINT), _bmpmemory: ctypes.c_char_p, _transparent: int) -> int:
        """
        Отобразить BMP в образ экрана
        
        :param _himage: идентификатор буфера образа окна карты
        
        :param _point: координаты в пикселах
        
        :param _bmpmemory: адрес массива байт, содержащего образ ``BMP``-файла
        
        :param _transparent: цвет ``RGB``, который не должен отображаться
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDrawImageBitMap_t (_himage, _hmap, _point, _bmpmemory, _transparent)

    mapDrawTotalSelectEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDrawTotalSelectEx', maptype.HIMAGE, maptype.HMAP, ctypes.c_long, maptype.HPAINT)
    def mapDrawTotalSelectEx(_himage: maptype.HIMAGE, _hmap: maptype.HMAP, _selectcolor: int, _hpaint: maptype.HPAINT) -> int:
        """
        Включить отображение выделенных объектов и обновить буфер выделенных объектов
        
        :param _himage: идентификатор буфера образа окна карты image     - идентификатор образа экрана
        
        :param _selectcolor: цвет выделения объектов на фоне карты (``RGB``)
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска или ``0`` При дальнешем обновлении буфера карты (Map) буфер выделенных объектов будет тоже обновляться
        
        :returns: Если выделение объектов не установлено (mapGetTotalSelectFlag() возвращает ноль) - буфер выделенных объектов автоматически закроется, а функия отображения вернет ноль При ошибке возвращает ноль
        :rtype: int
        """
        return mapDrawTotalSelectEx_t (_himage, _hmap, _selectcolor, _hpaint)

    mapDrawLabels_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDrawLabels', maptype.HIMAGE, maptype.HMAP, maptype.HPAINT)
    def mapDrawLabels(_himage: maptype.HIMAGE, _hmap: maptype.HMAP, _hpaint: maptype.HPAINT) -> int:
        """
        Включить отображение динамических подписей и обновить буфер выделенных объектов
        
        :param _himage: идентификатор буфера образа окна карты image - идентификатор образа экрана
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска или ``0`` При дальнешем обновлении буфера карты (Map) буфер выделенных объектов будет тоже обновляться
        
        :returns: Если отображение подписей не установлено (mapGetLabelingState) возвращает ноль) - буфер выделенных объектов автоматически закроется, а функия отображения вернет ноль При ошибке возвращает ноль
        :rtype: int
        """
        return mapDrawLabels_t (_himage, _hmap, _hpaint)

    mapGetMapScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMapScale', maptype.HMAP)
    def mapGetMapScale(_hmap: maptype.HMAP) -> int:
        """
        Запросить базовый масштаб документа
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMapScale_t (_hmap)

    mapGetMapNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMapNameUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapGetMapNameUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить название карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _name: указатель на буфер для записи названия
        
        :param _size: размер буфера в байтах
        
        :returns: При ошибке возвращает пустую строку
        :rtype: int
        """
        return mapGetMapNameUn_t (_hmap, _name.buffer(), _size)

    mapGetMapPathUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMapPathUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapGetMapPathUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить полный путь к паспорту главной карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _name: указатель на буфер для записи пути
        
        :param _size: размер буфера в байтах
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapGetMapPathUn_t (_hmap, _name.buffer(), _size)

    mapGetMapInfoPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMapInfoPro', maptype.HMAP, ctypes.c_long, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(mapcreat.SHEETNAMES))
    def mapGetMapInfoPro(_hmap: maptype.HMAP, _sheetnumber: int, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _sheetnames: ctypes.POINTER(mapcreat.SHEETNAMES)) -> int:
        """
        Запросить паспортные данные векторной карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _sheetnumber: номер листа карты, для которого запрашиваются паспортные данные
        
        :param _mapreg: заполняемая структура параметров системы координат карты
        
        :param _listreg: параметры листа многолистовой карты или ``0``
        
        :param _sheetnames: название листа карты, номенклатуры и файлов даных (для многолистовой карты) или ``0`` Структуры ``MAPREGISTER``, ``LISTREGISTER`` и ``SHEETNAMES`` описаны в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMapInfoPro_t (_hmap, _sheetnumber, _mapreg, _listreg, _sheetnames)

    mapGetMapInfoByNameMeta_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMapInfoByNameMeta', maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(mapcreat.METAINFO))
    def mapGetMapInfoByNameMeta(_name: mapsyst.WTEXT, _sheetnumber: int, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _metainfo: ctypes.POINTER(mapcreat.METAINFO)) -> int:
        """
        Запросить паспортные данные векторной карты по имени файла - паспорта карты
        
        :param _name: имя файла паспорта карты (MAP,SIT,SITX)
        
        :param _sheetnumber: номер листа карты, для которого запрашиваются паспортные данные
        
        :param _mapreg: заполняемая структура параметров системы координат карты
        
        :param _listreg: параметры листа многолистовой карты или ``0``
        
        :param _metainfo: указатель на структуру для записи метаданных листа карты Структуры ``MAPREGISTER`` и ``LISTREGISTER`` описаны в mapcreat.h
        
        :returns: При ошибке возвращает ноль, иначе - число объектов на листе карты (если нет объектов, то возвращает -1)
        :rtype: int
        """
        return mapGetMapInfoByNameMeta_t (_name.buffer(), _sheetnumber, _mapreg, _listreg, _metainfo)

    mapCheckNomenclatureUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckNomenclatureUn', maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapCheckNomenclatureUn(_nomenclature: mapsyst.WTEXT, _type: int, _scale: int) -> int:
        """
        Контроль номенклатуры карты
        
        :param _nomenclature: строка с номенклатурой length - длина строки
        
        :param _type: тип карты (из ``MAPTYPE``)
        
        :param _scale: знаменатель масштаба, соответствующий типу карты
        
        :returns: Возвращает масштаб карты При ошибке возвращает ноль
        :rtype: int
        """
        return mapCheckNomenclatureUn_t (_nomenclature.buffer(), _type, _scale)

    mapSetFileNameFromNomenclatureUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetFileNameFromNomenclatureUn', maptype.PWCHAR, ctypes.c_int, maptype.PWCHAR)
    def mapSetFileNameFromNomenclatureUn(_filename: mapsyst.WTEXT, _namesize: int, _nomenclature: mapsyst.WTEXT) -> int:
        """
        Формирование имени файла по номенклатуре (удаляет точки, пробелы, -)
        
        :param _filename: буфер для имени файла
        
        :param _namesize: размер буфера в байтах
        
        :param _nomenclature: номенклатура листа Формирование имени удаляет точки, пробелы, тире
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetFileNameFromNomenclatureUn_t (_filename.buffer(), _namesize, _nomenclature.buffer())

    mapCalcTopographicSheetEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCalcTopographicSheetEx', maptype.HMAP, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER))
    def mapCalcTopographicSheetEx(_hmap: maptype.HMAP, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _listreg: ctypes.POINTER(mapcreat.LISTREGISTER)) -> int:
        """
        Расчет данных на лист топографической карты
        
        :param _hmap: идентификатор открытых данных (документа) или ноль
        
        :param _mapreg: заполняемая структура параметров системы координат карты
        
        :param _listreg: параметры листа многолистовой карты или ``0`` Структуры ``MAPREGISTER`` и ``LISTREGISTER`` описаны в mapcreat.h Входные данные заполняются в mapreg: тип карты, масштаб, в listreg - номенклатура Выходные данные заполняются в mapreg: осевой меридиан, в listreg: геодезические координаты, прямоугольные координаты, сближение меридианов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если mapreg и listreg заполняются для создания карты (самый первый лист), то hmap равно 0
           Если mapreg заполняется для добавления листа в карту, то hmap не равно 0
        """
        return mapCalcTopographicSheetEx_t (_hmap, _mapreg, _listreg)

    mapGetAxisMeridianFromNomenclatureEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetAxisMeridianFromNomenclatureEx', ctypes.c_long, ctypes.c_char_p)
    def mapGetAxisMeridianFromNomenclatureEx(_type: int, _nomenclature: ctypes.c_char_p) -> float:
        """
        Рассчитать осевой меридиан (от 0 до 360) по номенклатуре топокарты
        
        :param _type: тип карты: ``CK_42``, ``CK_95``, ``GCK_2011``, Pulkovo2017 ...
        
        :param _nomenclature: номенклатура листа
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapGetAxisMeridianFromNomenclatureEx_t (_type, _nomenclature)

    mapGetTopoScaleByNomenclature_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetTopoScaleByNomenclature', ctypes.c_long, ctypes.c_char_p)
    def mapGetTopoScaleByNomenclature(_type: int, _nomenclature: ctypes.c_char_p) -> float:
        """
        Рассчитать масштаб топокарты по номенклатуре (от 1 : 10 000 до 1 : 1 000 000)
        
        :param _type: тип карты: ``CK_42``, ``CK_95``, ``GCK_2011``, Pulkovo2017 или ``0``
        
        :param _nomenclature: номенклатура листа
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapGetTopoScaleByNomenclature_t (_type, _nomenclature)

    mapGetAxisMeridian_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetAxisMeridian', ctypes.c_double)
    def mapGetAxisMeridian(_longitude: float) -> float:
        """
        Рассчитать осевой меридиан топокарты по долготе
        """
        return mapGetAxisMeridian_t (_longitude)

    mapGetMapPrecision_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMapPrecision', maptype.HMAP)
    def mapGetMapPrecision(_hmap: maptype.HMAP) -> int:
        """
        Запросить признак повышенной точности хранения координат
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: Возвращает значения: ``1`` - максимальная точность хранения (метры или радианы), ``2`` - с точностью 2 знака (сантиметры), ``3`` - с точностью 3 знака (миллиметры) При ошибке или нормальной точности хранения координат возвращает ноль
        :rtype: int
        """
        return mapGetMapPrecision_t (_hmap)

    mapGetEllipsoidCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetEllipsoidCount')
    def mapGetEllipsoidCount() -> int:
        """
        Запросить количество эллипсоидов в списке
        """
        return mapGetEllipsoidCount_t ()

    mapGetEllipsoidNameByCodeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetEllipsoidNameByCodeUn', ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetEllipsoidNameByCodeUn(_code: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить название эллипсоида по коду
        
        :param _code: код эллипсоида
        
        :param _name: адрес строки для размещения названия эллипсоида
        
        :param _size: длина выделенной области под строку в БАЙТАХ
        
        :returns: При ошибке возвращает ноль, name содержит значение ``"Не установлено"``
        :rtype: int
        """
        return mapGetEllipsoidNameByCodeUn_t (_code, _name.buffer(), _size)

    mapGetEllipsoidByNumberUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetEllipsoidByNumberUn', ctypes.c_long, ctypes.POINTER(ctypes.c_long), maptype.PWCHAR, ctypes.c_long)
    def mapGetEllipsoidByNumberUn(_number: int, _code: ctypes.POINTER(ctypes.c_long), _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запрос кода и названия эллипсоида по номеру в таблице
        
        :param _number: номер строки таблицы эллипсоидов с ``1``
        
        :param _code: код эллипсоида
        
        :param _name: адрес строки для размещения названия эллипсоида
        
        :param _size: длина выделенной области под строку в БАЙТАХ
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetEllipsoidByNumberUn_t (_number, _code, _name.buffer(), _size)

    mapGetEllipsoidByEPSGCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetEllipsoidByEPSGCode', ctypes.c_long)
    def mapGetEllipsoidByEPSGCode(_code: int) -> int:
        """
        Запросить по коду EPSG номер эллипсоида
        
        :param _code: код ``EPSG``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetEllipsoidByEPSGCode_t (_code)

    mapGetEllipsoidEPSGCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetEllipsoidEPSGCode', ctypes.c_long)
    def mapGetEllipsoidEPSGCode(_code: int) -> int:
        """
        Запросить код EPSG эллипсоида по его коду
        
        ellipsoid - номер эллипсоида с 1 (ELLIPSOIDKIND)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetEllipsoidEPSGCode_t (_code)

    mapGetMapTypeCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMapTypeCount')
    def mapGetMapTypeCount() -> int:
        """
        Запрос количества типов карт в списке
        """
        return mapGetMapTypeCount_t ()

    mapGetMapTypeByCodeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMapTypeByCodeUn', ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetMapTypeByCodeUn(_code: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запрос названия типа карты по коду
        
        :param _code: код типа карты
        
        :param _name: адрес строки для размещения названия типа карты
        
        :param _size: длина выделенной области под строку в БАЙТАХ
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMapTypeByCodeUn_t (_code, _name.buffer(), _size)

    mapGetMapTypeByNumberUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMapTypeByNumberUn', ctypes.c_long, ctypes.POINTER(ctypes.c_long), maptype.PWCHAR, ctypes.c_long)
    def mapGetMapTypeByNumberUn(_number: int, _code: ctypes.POINTER(ctypes.c_long), _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запрос кода и названия типа карты по номеру в таблице
        
        :param _number: номер строки таблицы типа карты с ``1``
        
        :param _code: код типа карты
        
        :param _name: адрес строки для размещения названия типа карты
        
        :param _size: длина выделенной области под строку в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMapTypeByNumberUn_t (_number, _code, _name.buffer(), _size)

    mapGetProjectionCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetProjectionCount')
    def mapGetProjectionCount() -> int:
        """
        Запрос количества проекций в списке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetProjectionCount_t ()

    mapGetProjectionNameByCodeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetProjectionNameByCodeUn', ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetProjectionNameByCodeUn(_code: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запрос названия проекции по коду
        
        :param _code: код проекции
        
        :param _name: адрес строки для размещения названия проекции
        
        :param _size: длина выделенной области под строку в байтах
        
        :returns: При ошибке возвращает ноль, name содержит значение ``"Не установлено"``
        :rtype: int
        """
        return mapGetProjectionNameByCodeUn_t (_code, _name.buffer(), _size)

    mapGetProjectionByNumberUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetProjectionByNumberUn', ctypes.c_long, ctypes.POINTER(ctypes.c_long), maptype.PWCHAR, ctypes.c_long)
    def mapGetProjectionByNumberUn(_number: int, _code: ctypes.POINTER(ctypes.c_long), _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запрос кода и названия проекции по номеру в таблице
        
        :param _number: номер строки таблицы проекций с ``1``
        
        :param _code: код проекции
        
        :param _name: адрес строки для размещения названия проекции
        
        :param _size: длина выделенной области под строку в БАЙТАХ
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetProjectionByNumberUn_t (_number, _code, _name.buffer(), _size)

    mapGetHeightSystemCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetHeightSystemCount')
    def mapGetHeightSystemCount() -> int:
        """
        Запрос количества систем высот в списке
        """
        return mapGetHeightSystemCount_t ()

    mapGetHeightSystemNameByCodeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetHeightSystemNameByCodeUn', ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetHeightSystemNameByCodeUn(_code: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запрос названия системы высот по коду
        
        :param _code: код системы высот
        
        :param _name: адрес строки для размещения названия системы высот
        
        :param _size: длина выделенной области под строку в байтах
        
        :returns: При ошибке возвращает ноль, name содержит значение ``"Не установлено"``
        :rtype: int
        """
        return mapGetHeightSystemNameByCodeUn_t (_code, _name.buffer(), _size)

    mapGetHeightSystemByNumberUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetHeightSystemByNumberUn', ctypes.c_long, ctypes.POINTER(ctypes.c_long), maptype.PWCHAR, ctypes.c_long)
    def mapGetHeightSystemByNumberUn(_number: int, _code: ctypes.POINTER(ctypes.c_long), _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запрос кода и названия системы высот по номеру в таблице
        
        :param _number: номер строки таблицы систем высот с ``1``
        
        :param _code: код системы высот
        
        :param _name: адрес строки для размещения названия проекции
        
        :param _size: длина выделенной области под строку в БАЙТАХ
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetHeightSystemByNumberUn_t (_number, _code, _name.buffer(), _size)

    mapGetLayerCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetLayerCount', maptype.HMAP)
    def mapGetLayerCount(_hmap: maptype.HMAP) -> int:
        """
        Запросить число слоев на карте
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetLayerCount_t (_hmap)

    mapGetLayerNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetLayerNameUn', maptype.HMAP, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetLayerNameUn(_hmap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить название слоя по его номеру
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: номер слоя с ``0``
        
        :param _name: адрес буфера для результата запроса
        
        :param _size: размер буфера в байтах Номер первого слоя равен ``0``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetLayerNameUn_t (_hmap, _number, _name.buffer(), _size)

    mapWhatListNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapWhatListNumber', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapWhatListNumber(_hmap: maptype.HMAP, _x: float, _y: float, _number: int, _place: int) -> int:
        """
        Определить номер листа в точке по координатам
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: порядковый номер листа в перекрытии (начина с ``1``).
        
        :param _place: вид системы координат: ``PP_PICTURE`` - в точках экрана, ``PP_PLANE`` - в метрах в системе координат документа, ``PP_GEO`` - в радианах на эллипсоиде документа
        
        :returns: Если лист не найден - возвращает ноль При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если в одной точке несколько листов, то для их перебора значение параметра number увеличивается на 1
           Поиск всегда дает одинаковый порядок листов
        """
        return mapWhatListNumber_t (_hmap, _x, _y, _number, _place)

    mapWhatListNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapWhatListNameUn', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapWhatListNameUn(_hmap: maptype.HMAP, _x: float, _y: float, _number: int, _place: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить номенклатуру листа по заданным координатам
        
        :param _hmap: идентификатор открытых данных (документа) x, y - координаты точки в метрах в системе документа
        
        :param _number: номер листа в списке найденных, который нужно вернуть (если точка в габаритах нескольких листов)
        
        :param _place: cистема координат (пикселы, метры, радианы)
        
        :param _name: адрес буфера для результата запроса
        
        :param _size: размер буфера в байтах
        
        :returns: Если лист не найден - возвращает ноль
        :rtype: int
        """
        return mapWhatListNameUn_t (_hmap, _x, _y, _number, _place, _name.buffer(), _size)

    mapGetSheetNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSheetNameUn', maptype.HMAP, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetSheetNameUn(_hmap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _namesize: int) -> int:
        """
        Запросить имя листа по его номеру (number)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _name: адрес буфера для результата запроса size - размер буфера в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSheetNameUn_t (_hmap, _number, _name.buffer(), _namesize)

    mapGetNomenclatureUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetNomenclatureUn', maptype.HMAP, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetNomenclatureUn(_hmap: maptype.HMAP, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить номенклатуру листа по его номеру (number)
        
        Для топокарт номенклатура листа не совпадает с названием листа
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _name: адрес буфера для результата запроса
        
        :param _size: размер буфера
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetNomenclatureUn_t (_hmap, _number, _name.buffer(), _size)

    mapGetListCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetListCount', maptype.HMAP)
    def mapGetListCount(_hmap: maptype.HMAP) -> int:
        """
        Запросить общее число листов в районе
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetListCount_t (_hmap)

    mapGetObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetObjectCount', maptype.HMAP, ctypes.c_long)
    def mapGetObjectCount(_hmap: maptype.HMAP, _list: int) -> int:
        """
        Запросить общее число объектов в листе
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _list: номер листа
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetObjectCount_t (_hmap, _list)

    mapGetRealObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRealObjectCount', maptype.HMAP, ctypes.c_long)
    def mapGetRealObjectCount(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить общее число объектов в листе, исключая удаленные
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: номер листа
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRealObjectCount_t (_hmap, _number)

    mapGetListNumberByNomenclatureUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetListNumberByNomenclatureUn', maptype.HMAP, maptype.PWCHAR)
    def mapGetListNumberByNomenclatureUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT) -> int:
        """
        Запросить номер листа по его номенклатуре
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _name: номенклатура листа
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetListNumberByNomenclatureUn_t (_hmap, _name.buffer())

    mapWhatListLayoutIsUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapWhatListLayoutIsUn', maptype.HMAP, maptype.PWCHAR)
    def mapWhatListLayoutIsUn(_hmap: maptype.HMAP, _listname: mapsyst.WTEXT) -> int:
        """
        Определить по номенклатуре листа его принадлежность карте
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _listname: имя листа (номенклатура)
        
        :returns: Возвращает номер карты в цепочке карт, которой принадлежит лист по имени listname: ``0`` - фоновая карта, ``1`` - первая пользовательская карта и так далее При ошибке возвращает ``"-1"``
        :rtype: int
        """
        return mapWhatListLayoutIsUn_t (_hmap, _listname.buffer())

    mapGetListFrameObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetListFrameObject', maptype.HMAP, ctypes.c_long, maptype.HOBJ)
    def mapGetListFrameObject(_hmap: maptype.HMAP, _list: int, _hobj: maptype.HOBJ) -> int:
        """
        Запросить объект "Рамка листа"
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _list: номер листа c ``1``
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetListFrameObject_t (_hmap, _list, _hobj)

    mapGetListFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetListFrame', maptype.HMAP, ctypes.c_long, ctypes.POINTER(maptype.DFRAME))
    def mapGetListFrame(_hmap: maptype.HMAP, _list: int, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Запросить габариты объекта "Рамка листа"
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _list: номер листа с ``1``
        
        :param _frame: указатель на габариты листа в метрах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если рамки нет габариты заполняются по метаданным из паспорта
        """
        return mapGetListFrame_t (_hmap, _list, _frame)

    mapCreateListFrameObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateListFrameObject', maptype.HMAP, ctypes.c_long, maptype.HOBJ)
    def mapCreateListFrameObject(_hmap: maptype.HMAP, _list: int, _hobj: maptype.HOBJ) -> int:
        """
        Создать объект "Рамка листа"
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _list: последовательный номер листа карты c ``1``
        
        :param _hobj: идентификатор объекта карты в памяти ``HOBJ`` должен быть создан вызовом mapCreateObject При успешном выполнении ``HOBJ`` будет содержать созданную или существующую рамку листа Для пользовательской карты (SIT, SITX) рамка создается, но не записывается Для многолистовой карты (MAP) созданная рамка сохраняется на карте
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCreateListFrameObject_t (_hmap, _list, _hobj)

    mapSetActiveListCountLimit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetActiveListCountLimit', maptype.HMAP, ctypes.c_long)
    def mapSetActiveListCountLimit(_hmap: maptype.HMAP, _islimited: int) -> int:
        """
        Установить ограничение на число листов, открытых одновременно
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _islimited: признак установки ограничения числа открытых листов, обычно от ``8`` до ``32``, но не менее числа потоков, обрабатывающих листы параллельно Применяется при работе с многолистовыми картами местности в ограниченной области памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetActiveListCountLimit_t (_hmap, _islimited)

    mapSetMemoryLimit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_ulong,'mapSetMemoryLimit', maptype.HMAP, ctypes.c_ulong)
    def mapSetMemoryLimit(_hmap: maptype.HMAP, _limit: int) -> int:
        """
        Установить ограничение на размер используемой памяти
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _limit: размер разрешенной к использованию памяти Применяется при работе с большими многолистовыми картами
        
        :returns: При ошибке возвращает 0
        :rtype: int
        
        .. note::

           Если лимит больше доступной приложению памяти, устанавливается доступный объем физической памяти
           Если лимит меньше 32 Мб, то устанавливается 32 Мб
        """
        return mapSetMemoryLimit_t (_hmap, _limit)

    mapGetTotalBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetTotalBorder', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.c_long)
    def mapGetTotalBorder(_hmap: maptype.HMAP, _dframe: ctypes.POINTER(maptype.DFRAME), _place: int) -> int:
        """
        Запросить габариты открытых данных
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _dframe: указатель на заполняемую структуру
        
        :param _place: вид системы координат: ``PP_PICTURE`` - в точках экрана, ``PP_PLANE`` - в метрах в системе координат документа, ``PP_GEO`` - в радианах на эллипсоиде документа Запрашиваются координаты углов района в метрах или радианах на местности в картографической системе или в пикселах относительно верхнего левого угла района
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetTotalBorder_t (_hmap, _dframe, _place)

    mapGetTotalBorderByEPSG_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetTotalBorderByEPSG', maptype.HMAP, ctypes.POINTER(maptype.DFRAME), ctypes.POINTER(maptype.DFRAME), ctypes.c_long)
    def mapGetTotalBorderByEPSG(_hmap: maptype.HMAP, _dframeplane: ctypes.POINTER(maptype.DFRAME), _dframegeo: ctypes.POINTER(maptype.DFRAME), _epsgcode: int) -> int:
        """
        Запросить габариты открытых данных в системе координат, заданной кодом EPSG
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _dframeplane: указатель на заполняемую структуру в метрах
        
        :param _dframegeo: указатель на заполняемую структуру в радианах
        
        :param _epsgcode: код системы координат (``3395``, ``3857``, ``4326`` и другие) Порядок осей - всегда широта\\долгота, север\\восток
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetTotalBorderByEPSG_t (_hmap, _dframeplane, _dframegeo, _epsgcode)

    mapSetLeftIndent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetLeftIndent', maptype.HMAP, ctypes.c_long)
    def mapSetLeftIndent(_hmap: maptype.HMAP, _leftmm: int) -> ctypes.c_void_p:
        """
        Установить левый отступ изображения карты от начала буфера изображения
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _leftmm: примерная величина отступа левой границы изображения от края окна в мм Ширина полосы в метрах, на которую расширяются габариты изображения в текущем масштабе, вычисляется так: double delta = mapGetRealShowScale(hmap) ``*`` mapGetLeftIndent(hmap) / ``1000.0``;
        """
        return mapSetLeftIndent_t (_hmap, _leftmm)

    mapGetLeftIndent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetLeftIndent', maptype.HMAP)
    def mapGetLeftIndent(_hmap: maptype.HMAP) -> int:
        """
        Запросить левый отступ изображения карты от начала буфера изображения
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: Возвращает сдвиг в окне (буфере) левой границы изображения в мм от края окна (буфера)
        :rtype: int
        """
        return mapGetLeftIndent_t (_hmap)

    mapPictureToPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapPictureToPlane', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapPictureToPlane(_hmap: maptype.HMAP, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double)) -> ctypes.c_void_p:
        """
        Преобразование из пикселов в изображении в координаты на местности в метрах
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _x: координата в пикселах по горизонтали
        
        :param _y: координата в пикселах по вертикали Полученные координаты будут в метрах: x - на сервер, y - на восток
        """
        return mapPictureToPlane_t (_hmap, _x, _y)

    mapPictureToPlanePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapPictureToPlanePro', ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), maptype.HPAINT)
    def mapPictureToPlanePro(_x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _hpaint: maptype.HPAINT) -> ctypes.c_void_p:
        """
        Преобразование из пикселов в изображении в координаты на местности в метрах
        
        :param _x: координата в пикселах по горизонтали
        
        :param _y: координата в пикселах по вертикали
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска Полученные координаты будут в метрах: x - на сервер, y - на восток
        """
        return mapPictureToPlanePro_t (_x, _y, _hpaint)

    mapPlaneToPicture_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapPlaneToPicture', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapPlaneToPicture(_hmap: maptype.HMAP, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double)) -> ctypes.c_void_p:
        """
        Преобразование из метров на местности в пикселы на изображении
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _x: координата в метрах на север в системе координат документа
        
        :param _y: координата в метрах на восток в системе координат документа Полученные координаты будут в пикселах: x - по горизонтали, y - по вертикали
        """
        return mapPlaneToPicture_t (_hmap, _x, _y)

    mapPlaneToPicturePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapPlaneToPicturePro', ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), maptype.HPAINT)
    def mapPlaneToPicturePro(_x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _hpaint: maptype.HPAINT) -> ctypes.c_void_p:
        """
        Преобразование из метров на местности в пикселы на изображении
        
        hmap - идентификатор открытых данных (документа)
        
        :param _x: координата в метрах на север в системе координат документа
        
        :param _y: координата в метрах на восток в системе координат документа
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска Полученные координаты будут в пикселах: x - по горизонтали, y - по вертикали
        """
        return mapPlaneToPicturePro_t (_x, _y, _hpaint)

    mapPlaneToGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPlaneToGeo', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapPlaneToGeo(_hmap: maptype.HMAP, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование из метров на местности в геодезические координаты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _bx: координата в метрах на север в системе координат документа
        
        :param _ly: координата в метрах на восток в системе координат документа Полученные координаты будут в радианах: bx - широта, ly - долгота Пересчет выполняется в соответствии с проекцией карты и поддерживается не для всех карт (mapIsGeoSupported() !``= 0``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPlaneToGeo_t (_hmap, _bx, _ly)

    mapGeoToPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGeoToPlane', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoToPlane(_hmap: maptype.HMAP, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование из геодезических координат открытых данных в плоские прямоугольные координаты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _bx: широта в радианах
        
        :param _ly: долгота в радианах Полученные координаты будут в метрах: bx - на сервер, ly - на восток Пересчет выполняется в соответствии с проекцией карты и поддерживается не для всех карт (mapIsGeoSupported() !``= 0``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGeoToPlane_t (_hmap, _bx, _ly)

    mapIsGeoSupported_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsGeoSupported', maptype.HMAP)
    def mapIsGeoSupported(_hmap: maptype.HMAP) -> int:
        """
        Запрос, поддерживается ли пересчет для геодезических координат
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: Если нет - возвращает ноль
        :rtype: int
        """
        return mapIsGeoSupported_t (_hmap)

    mapPlaneToGeoWGS84_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPlaneToGeoWGS84', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapPlaneToGeoWGS84(_hmap: maptype.HMAP, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование из метров на местности в геодезические координаты WGS84
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _bx: координата в метрах на север в системе координат документа
        
        :param _ly: координата в метрах на восток в системе координат документа Полученные координаты будут в радианах: bx - широта в системе ``WGS84``, ly - долгота в системе ``WGS84``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPlaneToGeoWGS84_t (_hmap, _bx, _ly)

    mapNormalHeightToGeoHeightWGS84_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapNormalHeightToGeoHeightWGS84', ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
    def mapNormalHeightToGeoHeightWGS84(_bx: float, _ly: float, _h: ctypes.POINTER(ctypes.c_double), _hegm: ctypes.c_void_p) -> int:
        """
        Преобразование ортометрической высоты (MSL) к геодезической (WGS84)
        
        :param _bx: широта в радианах ``WGS84``
        
        :param _ly: долгота в радианах ``WGS84``
        
        :param _h: ортометрическая высота в метрах
        
        :param _hegm: идентификатор модели геоида, открытой mapOpenEgmPro()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapNormalHeightToGeoHeightWGS84_t (_bx, _ly, _h, _hegm)

    mapGeoHeightToNormalHeightWGS84_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGeoHeightToNormalHeightWGS84', ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
    def mapGeoHeightToNormalHeightWGS84(_bx: float, _ly: float, _h: ctypes.POINTER(ctypes.c_double), _hegm: ctypes.c_void_p) -> int:
        """
        Преобразование геодезической (WGS84) высоты к ортометрической (MSL)
        
        :param _bx: широта в радианах ``WGS84``
        
        :param _ly: долгота в радианах ``WGS84``
        
        :param _h: геодезическая высота на эллипсоиде ``WGS84`` в метрах
        
        :param _hegm: идентификатор модели геоида, открытой mapOpenEgmPro
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGeoHeightToNormalHeightWGS84_t (_bx, _ly, _h, _hegm)

    mapGeoToXYZWGS84_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGeoToXYZWGS84', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoToXYZWGS84(_hmap: maptype.HMAP, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование геодезических координат документа к геоцентрическим для эллипсоида WGS84
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _bx: широта в радианах в системе открытых данных (документа)
        
        :param _ly: долгота в радианах в системе открытых данных (документа)
        
        :param _h: геодезическая высота на эллипсоиде карты в метрах Преобразование ортометрической высоты к геодезической выполняет mapNormalHeightToGeoHeightWGS84 или mapUserPlaneToGeoWGS84Pro Полученные координаты будут в геоцентрической системе ``WGS84`` в метрах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGeoToXYZWGS84_t (_hmap, _bx, _ly, _h)

    mapGeoToXYZ_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGeoToXYZ', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoToXYZ(_hmap: maptype.HMAP, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование геодезических координат к геоцентрическим в системе открытых данных (документа)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _bx: широта в радианах в системе открытых данных (документа)
        
        :param _ly: долгота в радианах в системе открытых данных (документа)
        
        :param _h: геодезическая высота в метрах в системе открытых данных (документа) Полученные координаты будут в геоцентрической системе в метрах на эллипсоиде документа
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGeoToXYZ_t (_hmap, _bx, _ly, _h)

    mapXYZWGS84ToGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapXYZWGS84ToGeo', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapXYZWGS84ToGeo(_hmap: maptype.HMAP, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование геоцентрических координат WGS84 к геодезическим координатам карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _bx: геоцентрическая координата ``WGS84`` в метрах
        
        :param _ly: геоцентрическая координата ``WGS84`` в метрах
        
        :param _h: геоцентрическая координата ``WGS84`` в метрах Полученные координаты будут в радианах: bx - широта в системе карты, ly - долгота в системе карты,
        
        :param _h: геодезическая высота на эллипсоиде карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapXYZWGS84ToGeo_t (_hmap, _bx, _ly, _h)

    mapXYZToGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapXYZToGeo', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapXYZToGeo(_hmap: maptype.HMAP, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование геоцентрических координат на эллипсоиде карты к геодезическим
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _bx: геоцентрическая координата в метрах на эллипсоиде карты
        
        :param _ly: геоцентрическая координата в метрах на эллипсоиде карты
        
        :param _h: геоцентрическая координата в метрах на эллипсоиде карты Полученные координаты будут в радианах: bx - широта в системе карты, ly - долгота в системе карты,
        
        :param _h: геодезическая высота на эллипсоиде карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapXYZToGeo_t (_hmap, _bx, _ly, _h)

    mapTransformXYZ_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapTransformXYZ', ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(mapcreat.LOCALDATUMPARAM))
    def mapTransformXYZ(_X: ctypes.POINTER(ctypes.c_double), _Y: ctypes.POINTER(ctypes.c_double), _Z: ctypes.POINTER(ctypes.c_double), _datum: ctypes.POINTER(mapcreat.LOCALDATUMPARAM)) -> int:
        """
        Пересчет геоцентрических координат по заданным параметрам преобразования
        
        :param _X: геоцентрическая координата в метрах
        
        :param _Y: геоцентрическая координата в метрах
        
        :param _Z: геоцентрическая координата в метрах
        
        :param _datum: параметры преобразования геоцентрических координат Пересчет выполняется по формуле Обратное преобразование Гельмерта, или Coordinate Frame Rotation, ``EPSG``:``1032`` Знаки числовых значений должны быть заданы с учетом направления преобразования
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapTransformXYZ_t (_X, _Y, _Z, _datum)

    mapGeoToGeoWGS843D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGeoToGeoWGS843D', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoToGeoWGS843D(_hmap: maptype.HMAP, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование геодезических координат карты в геодезические координаты WGS84
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _bx: широта в радианах в системе карты
        
        :param _ly: долгота в радианах в системе карты
        
        :param _h: геодезическая высота на эллипсоиде карты в метрах Полученные координаты будут в радианах: bx - широта ``WGS84``, ly - долгота ``WGS84``,
        
        :param _h: геодезическая высота на эллипсоиде ``WGS84``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGeoToGeoWGS843D_t (_hmap, _bx, _ly, _h)

    mapGeoWGS84ToGeo3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGeoWGS84ToGeo3D', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoWGS84ToGeo3D(_hmap: maptype.HMAP, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование геодезических координат WGS84 в геодезические координаты карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _bx: широта в радианах ``WGS84``
        
        :param _ly: долгота в радианах ``WGS84``
        
        :param _h: геодезическая высота на эллипсоиде ``WGS84`` в метрах Полученные координаты будут в радианах: bx - широта в системе карты, ly - долгота в системе карты,
        
        :param _h: геодезическая высота на эллипсоиде карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGeoWGS84ToGeo3D_t (_hmap, _bx, _ly, _h)

    mapGeoWGS84ToPlane3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGeoWGS84ToPlane3D', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoWGS84ToPlane3D(_hmap: maptype.HMAP, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование геодезических координат WGS84 в метры в системе карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _bx: широта в радианах ``WGS84``
        
        :param _ly: долгота в радианах ``WGS84``
        
        :param _h: высота в метрах или ``0`` (не пересчитывается) Полученные координаты будут в метрах: bx - на сервер, ly - на восток, h - высота в метрах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGeoWGS84ToPlane3D_t (_hmap, _bx, _ly, _h)

    mapTransformPoints_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapTransformPoints', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.c_long)
    def mapTransformPoints(_hmap: maptype.HMAP, _srcpoints: ctypes.POINTER(maptype.DOUBLEPOINT), _srctype: int, _tagpoints: ctypes.POINTER(maptype.DOUBLEPOINT), _targettype: int, _count: int) -> ctypes.c_void_p:
        """
        Преобразование набора точек из одной системы координат в другую
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _srcpoints: указатель на список исходных точек
        
        :param _tagpoints: указательн на список пересчитанных точек (может быть равен srcpoints)
        
        :param _srctype: тип входной системы координат: ``PP_PLANE``, ``PP_GEO``, ``PP_GEOWGS84``, ``PP_PICTURE``
        
        :param _targettype: тип выходной системы координат: ``PP_PLANE``, ``PP_GEO``, ``PP_GEOWGS84``, ``PP_PICTURE``
        
        :param _count: число преобразуемых точек в списках
        
        :returns: При ошибке возвращает ноль
        """
        return mapTransformPoints_t (_hmap, _srcpoints, _srctype, _tagpoints, _targettype, _count)

    mapSignDegreeToRadian_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSignDegreeToRadian', ctypes.POINTER(maptype.SIGNDEGREE), ctypes.POINTER(ctypes.c_double))
    def mapSignDegreeToRadian(_degree: ctypes.POINTER(maptype.SIGNDEGREE), _radian: ctypes.POINTER(ctypes.c_double)) -> ctypes.c_void_p:
        """
        Преобразование координат из градусов в радианы с учетом знака
        
        :param _degree: структура, содержащая координаты в градусах, минутах, секундах. Описана в maptype.h
        
        :param _radian: значение в радианах
        """
        return mapSignDegreeToRadian_t (_degree, _radian)

    mapRadianToSignDegree_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapRadianToSignDegree', ctypes.POINTER(ctypes.c_double), ctypes.POINTER(maptype.SIGNDEGREE))
    def mapRadianToSignDegree(_radian: ctypes.POINTER(ctypes.c_double), _degree: ctypes.POINTER(maptype.SIGNDEGREE)) -> ctypes.c_void_p:
        """
        Преобразование координат из радиан в градусы со знаком
        
        :param _radian: значение в радианах
        
        :param _degree: структура, содержащая координаты в градусах, минутах, секундах. Описана в maptype.h
        """
        return mapRadianToSignDegree_t (_radian, _degree)

    mapGetAxisMeridianByZone_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetAxisMeridianByZone', ctypes.c_long)
    def mapGetAxisMeridianByZone(_zone: int) -> float:
        """
        Вычисление осевого маридиана по номеру зоны для топокарт СК-42, 95, ГСК-2011
        
        :param _zone: номер зоны
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapGetAxisMeridianByZone_t (_zone)

    mapGetAxisMeridianByUTMZone_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetAxisMeridianByUTMZone', ctypes.c_long)
    def mapGetAxisMeridianByUTMZone(_zone: int) -> float:
        """
        Вычисление осевого маридиана по номеру зоны для топокарт UTM
        
        :param _zone: номер зоны ``UTM``
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapGetAxisMeridianByUTMZone_t (_zone)

    mapGetAxisMeridianByZoneAndType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetAxisMeridianByZoneAndType', ctypes.c_long, ctypes.c_long)
    def mapGetAxisMeridianByZoneAndType(_zone: int, _maptype: int) -> float:
        """
        Вычисление осевого маридиана топокарты по номеру зоны с учетом типа карты
        
        :param _zone: номер зоны от ``1`` до ``60`` с учетом типа карты type - тип топокарты (``CK_42``, ``CK_95``, ``GCK_2011``, ``UTMWGS84``, ``UTMTYPE``) Для ``UTM`` зоны идут от -``180`` до +``180``, для СК-``42``, ``95``, ГСК-``2011`` - от ``0`` до ``360``
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapGetAxisMeridianByZoneAndType_t (_zone, _maptype)

    mapGetZoneByMeridian_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetZoneByMeridian', ctypes.c_double)
    def mapGetZoneByMeridian(_meridian: float) -> int:
        """
        Вычисление номера зоны по геодезической долготе в радианах (меридиану) для топокарт СК-42, 95, ГСК-2011
        
        :param _meridian: значение меридиана в радианах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetZoneByMeridian_t (_meridian)

    mapGetUTMZoneByMeridian_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetUTMZoneByMeridian', ctypes.c_double)
    def mapGetUTMZoneByMeridian(_meridian: float) -> int:
        """
        Вычисление номера зоны UTM по геодезической долготе в радианах
        
        :param _meridian: значение меридиана в радианах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetUTMZoneByMeridian_t (_meridian)

    mapSetAxisMeridianByMeridian_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetAxisMeridianByMeridian', maptype.HMAP, ctypes.c_double)
    def mapSetAxisMeridianByMeridian(_hmap: maptype.HMAP, _meridian: float) -> int:
        """
        Заполнение осевого меридиана по геодезической долготе в радианах для топографических карт СК-42, 95, ГСК-2011, UTM
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _meridian: значение меридиана в радианах Не рекомендуется применять для карт уже содержащих объекты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetAxisMeridianByMeridian_t (_hmap, _meridian)

    mapSetAxisMeridianByPlaneY_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetAxisMeridianByPlaneY', maptype.HMAP, ctypes.c_double)
    def mapSetAxisMeridianByPlaneY(_hmap: maptype.HMAP, _y: float) -> int:
        """
        Заполнение осевого меридиана по старшей цифре координаты Y для топографических карт СК-42, 95, ГСК-2011
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _y: координата по горизонтали в метрах произвольной точки, попадающей на заданный лист Не рекомендуется применять для карт уже содержащих объекты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetAxisMeridianByPlaneY_t (_hmap, _y)

    mapGetEllipsoidParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetEllipsoidParameters', ctypes.c_long, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapGetEllipsoidParameters(_ellipsoid: int, _parm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        """
        Запросить параметры эллипсоида по его номеру
        
        :param _ellipsoid: номер эллипсоида, описан в ``ELLIPSOIDKIND``
        
        :param _parm: параметры заданного эллипсоида
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetEllipsoidParameters_t (_ellipsoid, _parm)

    mapCreateUserSystemParametersPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCreateUserSystemParametersPro', ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_long, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapCreateUserSystemParametersPro(_mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> ctypes.c_void_p:
        """
        Установить текущие параметры пользовательской системы координат
        
        :param _mapreg: структура параметров системы координат карты
        
        :param _datum: параметры пересчета с эллипсоида рабочей системы координат к ``WGS84`` или ``0``
        
        :param _ellipsoid: параметры пользовательского эллипсоида, когда поле EllipsoidKind в ``MAPREGISTEREX`` равно ``USERELLIPSOID`` или ``0``
        
        :param _ttype: тип локального преобразования координат (``TRANSFORMTYPE`` в mapcreat.h) или ``0``
        
        :param _tparm: параметры локального преобразования координат
        
        :returns: Возвращает идентификатор пользовательской системы координат По завершении использования необходимо вызвать mapDeleteUserSystemParameters Для Широта\\Долгота на WGS84 код равен 4326, для СК-42 зоны 1-``60: 28401``-28460, для СК-95 зоны 1-``60: 20001``-20060 для UTM на WGS84 зоны 1-``60: 32601``-32660 При ошибке возвращает ноль
        """
        return mapCreateUserSystemParametersPro_t (_mapreg, _datum, _ellipsoid, _ttype, _tparm)

    mapCreateUserSystemParametersByEpsg_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCreateUserSystemParametersByEpsg', ctypes.c_long)
    def mapCreateUserSystemParametersByEpsg(_epsgcode: int) -> ctypes.c_void_p:
        """
        Установить текущие параметры пользовательской системы координат по коду EPSG
        
        :param _epsgcode: код ``EPSG``
        
        :returns: Возвращает идентификатор пользовательской системы координат По завершении использования необходимо вызвать mapDeleteUserSystemParameters При ошибке возвращает ноль
        """
        return mapCreateUserSystemParametersByEpsg_t (_epsgcode)

    mapCreateUserSystemParametersByDoc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCreateUserSystemParametersByDoc', maptype.HMAP)
    def mapCreateUserSystemParametersByDoc(_hmap: maptype.HMAP) -> ctypes.c_void_p:
        """
        Установить текущие параметры пользовательской системы координат из открытых данных
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: Возвращает идентификатор пользовательской системы координат По завершении использования необходимо вызвать mapDeleteUserSystemParameters При ошибке возвращает ноль
        """
        return mapCreateUserSystemParametersByDoc_t (_hmap)

    mapCreateUserSystemParametersByXmlNode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCreateUserSystemParametersByXmlNode', ctypes.c_char_p)
    def mapCreateUserSystemParametersByXmlNode(_point: ctypes.c_char_p) -> ctypes.c_void_p:
        """
        Установить текущие параметры пользовательской системы координат из записи XML
        
        :param _point: указатель на строку, завершающуся нулем и содержащую запись параметров системы координат из ``XML`` Запись параметров из ``XML`` можно запросить через mapGetUserSystemXmlNode()
        
        :returns: Возвращает идентификатор пользовательской системы координат По завершении использования необходимо вызвать mapDeleteUserSystemParameters При ошибке возвращает ноль
        """
        return mapCreateUserSystemParametersByXmlNode_t (_point)

    mapDeleteUserSystemParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapDeleteUserSystemParameters', ctypes.c_void_p)
    def mapDeleteUserSystemParameters(_huser: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Освободить ресурсы пользовательской системы координат
        
        :param _huser: идентификатор пользовательской системы координат
        """
        return mapDeleteUserSystemParameters_t (_huser)

    mapGetUserSystemParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetUserSystemParameters', ctypes.c_void_p, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapGetUserSystemParameters(_huser: ctypes.c_void_p, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: ctypes.POINTER(ctypes.c_long), _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        """
        Запросить текущие параметры пользовательской системы координат
        
        :param _huser: идентификатор пользовательской системы координат
        
        :param _mapreg: структура параметров системы координат карты
        
        :param _datum: параметры пересчета с эллипсоида рабочей системы координат к ``WGS84`` или ``0``
        
        :param _ellipsoid: параметры пользовательского эллипсоида, когда поле EllipsoidKind в ``MAPREGISTEREX`` равно ``USERELLIPSOID`` или ``0``
        
        :param _ttype: тип локального преобразования координат (``TRANSFORMTYPE`` в mapcreat.h) или ``0``
        
        :param _tparm: параметры локального преобразования координат
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetUserSystemParameters_t (_huser, _mapreg, _datum, _ellipsoid, _ttype, _tparm)

    mapChangeUserSystemParametersByEpsg_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapChangeUserSystemParametersByEpsg', ctypes.c_void_p, ctypes.c_long)
    def mapChangeUserSystemParametersByEpsg(_huser: ctypes.c_void_p, _epsgcode: int) -> int:
        """
        Изменить текущие параметры пользовательской системы координат по коду EPSG
        
        :param _huser: идентификатор пользовательской системы координат
        
        :param _epsgcode: код ``EPSG``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapChangeUserSystemParametersByEpsg_t (_huser, _epsgcode)

    mapSetUserSystemType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetUserSystemType', ctypes.c_void_p, ctypes.c_long)
    def mapSetUserSystemType(_huser: ctypes.c_void_p, _type: int) -> int:
        """
        Установить тип пользовательской системы координат
        
        :param _huser: идентификатор пользовательской системы координат
        
        :param _type: тип пользовательской системы координат: ``1`` - плоская прямоугольная, ``2`` - геодезическая
        
        :returns: При отсутствии данных возвращает ноль
        :rtype: int
        """
        return mapSetUserSystemType_t (_huser, _type)

    mapGetUserSystemType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetUserSystemType', ctypes.c_void_p)
    def mapGetUserSystemType(_huser: ctypes.c_void_p) -> int:
        """
        Запросить тип пользовательской системы координат
        
        :param _huser: идентификатор пользовательской системы координат
        
        :returns: Возвращает тип пользовательской системы координат: ``1`` - плоская прямоугольная, ``2`` - геодезическая При отсутствии данных возвращает ноль
        :rtype: int
        """
        return mapGetUserSystemType_t (_huser)

    mapGetUserSystemAxisMeridian_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetUserSystemAxisMeridian', ctypes.c_void_p)
    def mapGetUserSystemAxisMeridian(_huser: ctypes.c_void_p) -> float:
        """
        Запросить значение осевого меридиана для пользовательской системы координат
        
        :param _huser: идентификатор пользовательской системы координат
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapGetUserSystemAxisMeridian_t (_huser)

    mapSetUserSystemZone_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetUserSystemZone', ctypes.c_void_p, ctypes.c_long, ctypes.c_long)
    def mapSetUserSystemZone(_huser: ctypes.c_void_p, _zone: int, _isupdateaxis: int) -> int:
        """
        Установить номер зоны для пользовательской системы координат и обновить осевой меридиан
        
        :param _huser: идентификатор пользовательской системы координат
        
        :param _zone: номер зоны от ``1`` до ``60``
        
        :param _isupdateaxis: признак необходимости пересчета осевого меридиана для заданного номера зоны
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetUserSystemZone_t (_huser, _zone, _isupdateaxis)

    mapGetUserSystemZone_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetUserSystemZone', ctypes.c_void_p)
    def mapGetUserSystemZone(_huser: ctypes.c_void_p) -> int:
        """
        Запросить номер зоны для пользовательской системы координат
        
        :param _huser: идентификатор пользовательской системы координат
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetUserSystemZone_t (_huser)

    mapUserGeoToGeoWGS843D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUserGeoToGeoWGS843D', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserGeoToGeoWGS843D(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование пользовательских геодезических координат в геодезические координаты WGS84
        
        :param _huser: идентификатор пользовательской системы координат
        
        :param _bx: широта в радианах в пользовательской системе
        
        :param _ly: долгота в радианах в пользовательской системе
        
        :param _h: геодезическая высота на эллипсоиде пользовательской системы в метрах или ``0`` Полученные координаты будут в радианах: bx - широта ``WGS84``, ly - долгота ``WGS84``,
        
        :param _h: геодезическая высота на эллипсоиде ``WGS84``
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapUserGeoToGeoWGS843D_t (_huser, _bx, _ly, _h)

    mapUserGeoToLocalGeo3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUserGeoToLocalGeo3D', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(mapcreat.LOCALDATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapUserGeoToLocalGeo3D(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _ldatum: ctypes.POINTER(mapcreat.LOCALDATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        """
        Преобразование пользовательских геодезических координат в геодезические координаты на заданном эллипсоиде
        
        :param _huser: идентификатор пользовательской системы координат
        
        :param _bx: широта в радианах в пользовательской системе
        
        :param _ly: долгота в радианах в пользовательской системе
        
        :param _h: геодезическая высота на эллипсоиде пользовательской системы в метрах или ``0``
        
        :param _ldatum: параметры перехода от пользовательской системы координат к геодезической системе на заданном эллипсоиде (обратное преобразование Гельмерта, или Coordinate Frame Rotation; ``EPSG`` dataset coordinate operation method code ``1032``)
        
        :param _ellipsoid: параметры эллипсоида, на котором определяют геодезические координаты Полученные координаты будут в радианах: bx - широта на заданном эллипсоиде, ly - долгота ``WGS84`` на заданном эллипсоиде,
        
        :param _h: геодезическая высота на заданном эллипсоиде
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapUserGeoToLocalGeo3D_t (_huser, _bx, _ly, _h, _ldatum, _ellipsoid)

    mapUserGeoToXYZWGS84_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUserGeoToXYZWGS84', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserGeoToXYZWGS84(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование пользовательских геодезических координат в геоцентрические координаты WGS84
        
        :param _huser: идентификатор пользовательской системы координат
        
        :param _bx: широта в радианах в пользовательской системе
        
        :param _ly: долгота в радианах в пользовательской системе
        
        :param _h: геодезическая высота на эллипсоиде пользовательской системы в метрах Полученные координаты будут в геоцентрической системе ``WGS84`` в метрах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUserGeoToXYZWGS84_t (_huser, _bx, _ly, _h)

    mapXYZWGS84ToUserGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapXYZWGS84ToUserGeo', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapXYZWGS84ToUserGeo(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование геоцентрических координат WGS84 в пользовательские геодезические координаты
        
        :param _huser: идентификатор пользовательской системы координат
        
        :param _bx: геоцентрическая координата ``WGS84`` в метрах
        
        :param _ly: геоцентрическая координата ``WGS84`` в метрах
        
        :param _h: геоцентрическая координата ``WGS84`` в метрах Полученные координаты будут в радианах: bx - широта в пользовательской системе, ly - долгота в пользовательской системе,
        
        :param _h: геодезическая высота на пользовательском эллипсоиде
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapXYZWGS84ToUserGeo_t (_huser, _bx, _ly, _h)

    mapUserGeoToUserXYZ_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUserGeoToUserXYZ', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserGeoToUserXYZ(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование геодезических координат к геоцентрическим для пользовательской системы
        
        :param _bx: широта в радианах в пользовательской системе
        
        :param _ly: долгота в радианах в пользовательской системе
        
        :param _h: геодезическая высота на эллипсоиде пользовательской системы в метрах Полученные координаты будут в геоцентрической системе в метрах на пользователськом эллипсоиде
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUserGeoToUserXYZ_t (_huser, _bx, _ly, _h)

    mapUserXYZToUserGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUserXYZToUserGeo', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserXYZToUserGeo(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование геоцентрических координат в геодезические координаты для пользовательской системы
        
        :param _bx: геоцентрическая координата в метрах на пользовательском эллипсоиде
        
        :param _ly: геоцентрическая координата в метрах  на пользовательском эллипсоиде
        
        :param _h: геоцентрическая координата в метрах на пользовательском эллипсоиде Полученные координаты будут в радианах: bx - широта в пользовательской системе, ly - долгота в пользовательской системе,
        
        :param _h: геодезическая высота на пользовательском эллипсоиде
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUserXYZToUserGeo_t (_huser, _bx, _ly, _h)

    mapUserGeoToUserPlanePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUserGeoToUserPlanePro', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
    def mapUserGeoToUserPlanePro(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _hegm: ctypes.c_void_p) -> int:
        """
        Преобразование геодезических координат в плоские прямоугольные в пользовательской системе
        
        :param _huser: идентификатор пользовательской системы координат
        
        :param _bx: широта в радианах в пользовательской системе
        
        :param _ly: долгота в радианах в пользовательской системе
        
        :param _h: геодезическая высота на эллипсоиде пользовательской системы в метрах или ``0``
        
        :param _hegm: идентификатор модели геоида для пересчета геодезической высоты в ортометрическую (геоид ``MSL``) или ``0`` Для получения hegm применяется функция mapOpenEgmPro Высота пересчитывается сначала из геодезической в геодезическую ``WGS84``, затем в ортометрическую
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если параметр hegm равен нулю, то пересчет высоты не выполняется
           Балтийская система высот (относительно квазигеоида, нормальная) отличается от ортометрической в среднем
           в пределах 1-2 метров
           Полученные координаты будут в метрах: bx - на сервер, ly - на восток, h - ортометрическая высота в метрах (MSL),
           если был задан hegm, или без изменений
        """
        return mapUserGeoToUserPlanePro_t (_huser, _bx, _ly, _h, _hegm)

    mapUserGeoToUserPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUserGeoToUserPlane', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserGeoToUserPlane(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование геодезических координат в плоские прямоугольные в пользовательской системе
        
        :param _huser: идентификатор пользовательской системы координат
        
        :param _bx: широта в радианах в пользовательской системе
        
        :param _ly: долгота в радианах в пользовательской системе Полученные координаты будут в метрах: bx - на сервер, ly - на восток
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUserGeoToUserPlane_t (_huser, _bx, _ly)

    mapUserPlaneToGeoWGS84Pro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUserPlaneToGeoWGS84Pro', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
    def mapUserPlaneToGeoWGS84Pro(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _hegm: ctypes.c_void_p) -> int:
        """
        Преобразование из метров на местности в пользовательской системе в геодезические координаты WGS84
        
        :param _huser: идентификатор пользовательской системы координат
        
        :param _bx: координата в метрах на север
        
        :param _ly: координата в метрах на восток
        
        :param _h: ортометрическая высота в точке (метры) или ``0``
        
        :param _hegm: идентификатор модели геоида для пересчета ортометрической высоты в геодезическую или ``0`` Для получения hegm применяется функция mapOpenEgmPro Полученные координаты будут в радианах: bx - широта ``WGS84``, ly - долгота ``WGS84``,
        
        :param _h: геодезическая высота на эллипсоиде ``WGS84``, если задан параметр hegm, или не изменится
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUserPlaneToGeoWGS84Pro_t (_huser, _bx, _ly, _h, _hegm)

    mapUserPlaneToGeoWGS84_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUserPlaneToGeoWGS84', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserPlaneToGeoWGS84(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование из метров на местности в пользовательской проекции в геодезические координаты WGS84
        
        :param _huser: идентификатор пользовательской системы координат
        
        :param _bx: координата в метрах на север
        
        :param _ly: координата в метрах на восток Полученные координаты будут в радианах: bx - широта ``WGS84``, ly - долгота ``WGS84``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUserPlaneToGeoWGS84_t (_huser, _bx, _ly)

    mapUserPlaneToUserGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUserPlaneToUserGeo', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserPlaneToUserGeo(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование из метров на местности в геодезические координаты в пользовательской системе
        
        :param _huser: идентификатор пользовательской системы координат
        
        :param _bx: координата в метрах на север
        
        :param _ly: координата в метрах на восток Полученные координаты будут в радианах: bx - широта в пользовательской системе, ly - долгота в пользовательской системе
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUserPlaneToUserGeo_t (_huser, _bx, _ly)

    mapUserPlaneToUserGeoPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUserPlaneToUserGeoPro', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
    def mapUserPlaneToUserGeoPro(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _hegm: ctypes.c_void_p) -> int:
        """
        Преобразование из метров на местности в геодезические координаты в пользовательской системе
        
        :param _huser: идентификатор пользовательской системы координат
        
        :param _bx: координата в метрах на север
        
        :param _ly: координата в метрах на восток
        
        :param _h: ортометрическая высота в метрах или ``0``
        
        :param _hegm: идентификатор модели геоида для пересчета ортометрической высоты в геодезическую или ``0`` Полученные координаты будут в радианах: bx - широта в пользовательской системе, ly - долгота в пользовательской системе
        
        :param _h: геодезическая высота на пользовательском эллипсоиде, если задан параметр hegm, или не изменится
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUserPlaneToUserGeoPro_t (_huser, _bx, _ly, _h, _hegm)

    mapGeoWGS84ToUserGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGeoWGS84ToUserGeo', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoWGS84ToUserGeo(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование геодезических координат WGS84 в геодезические в пользовательской системе
        
        :param _huser: идентификатор пользовательской системы координат
        
        :param _bx: широта в радианах ``WGS84``
        
        :param _ly: долгота в радианах ``WGS84`` Полученные координаты будут в радианах: bx - широта в пользовательской системе, ly - долгота в пользовательской системе
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGeoWGS84ToUserGeo_t (_huser, _bx, _ly)

    mapGeoWGS84ToUserGeo3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGeoWGS84ToUserGeo3D', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoWGS84ToUserGeo3D(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование геодезических координат WGS84 в геодезические в пользовательской системе
        
        :param _huser: идентификатор пользовательской системы координат
        
        :param _bx: широта в радианах ``WGS84``
        
        :param _ly: долгота в радианах ``WGS84``
        
        :param _h: геодезическая высота на эллипсоиде ``WGS84`` в метрах или ``0`` Полученные координаты будут в радианах: bx - широта в пользовательской системе, ly - долгота в пользовательской системе
        
        :param _h: геодезическая высота на пользовательском эллипсоиде
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGeoWGS84ToUserGeo3D_t (_huser, _bx, _ly, _h)

    mapGeoWGS84ToUserPlanePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGeoWGS84ToUserPlanePro', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
    def mapGeoWGS84ToUserPlanePro(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _hegm: ctypes.c_void_p) -> int:
        """
        Преобразование геодезических координат WGS84 в плоские прямоугольные в пользовательской системе
        
        :param _huser: идентификатор пользовательской системы координат
        
        :param _bx: широта в радианах ``WGS84``
        
        :param _ly: долгота в радианах ``WGS84``
        
        :param _h: геодезическая высота на эллипсоиде ``WGS84`` в метрах или ``0``
        
        :param _hegm: идентификатор модели геоида для пересчета ортометрической высоты в геодезическую или ``0`` Для получения hegm применяется функция mapOpenEgmPro Полученные координаты будут в метрах: bx - на сервер, ly - на восток, h - ортометрическая высота в метрах (``MSL``), если был задан hegm, или без изменений
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGeoWGS84ToUserPlanePro_t (_huser, _bx, _ly, _h, _hegm)

    mapGeoWGS84ToUserPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGeoWGS84ToUserPlane', ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoWGS84ToUserPlane(_huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование геодезических координат WGS84 в плоские прямоугольные в пользовательской системе
        
        :param _huser: идентификатор пользовательской системы координат
        
        :param _bx: широта в радианах ``WGS84``
        
        :param _ly: долгота в радианах ``WGS84`` Полученные координаты будут в метрах: bx - на сервер, ly - на восток
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGeoWGS84ToUserPlane_t (_huser, _bx, _ly)

    mapGeoToUserGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGeoToUserGeo', maptype.HMAP, ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoToUserGeo(_hmap: maptype.HMAP, _huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование геодезических координат документа в геодезические пользовательские координаты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _huser: идентификатор пользовательской системы координат
        
        :param _bx: широта в радианах в системе открытых данных (документа)
        
        :param _ly: долгота в радианах в системе открытых данных (документа) Полученные координаты будут в радианах: bx - широта в пользовательской системе, ly - долгота в пользовательской системе
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGeoToUserGeo_t (_hmap, _huser, _bx, _ly)

    mapGeoToUserGeo3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGeoToUserGeo3D', maptype.HMAP, ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapGeoToUserGeo3D(_hmap: maptype.HMAP, _huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование геодезических координат документа в геодезические пользовательские координаты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _huser: идентификатор пользовательской системы координат
        
        :param _bx: широта в радианах в системе открытых данных (документа)
        
        :param _ly: долгота в радианах в системе открытых данных (документа)
        
        :param _h: геодезическая высота в метрах на эллипсоиде открытых данных (документа) Полученные координаты будут в радианах: bx - широта в пользовательской системе, ly - долгота в пользовательской системе
        
        :param _h: геодезическая высота на пользовательском эллипсоиде
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGeoToUserGeo3D_t (_hmap, _huser, _bx, _ly, _h)

    mapUserGeoToGeo3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUserGeoToGeo3D', maptype.HMAP, ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserGeoToGeo3D(_hmap: maptype.HMAP, _huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование геодезических пользовательских координат в геодезические координаты документа
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _huser: идентификатор пользовательской системы координат
        
        :param _bx: широта в радианах в пользовательской системе
        
        :param _ly: долгота в радианах в пользовательской системе
        
        :param _h: геодезическая высота на эллипсоиде пользовательской системы в метрах или ``0`` Полученные координаты будут в радианах: bx - широта в системе документа, ly - долгота в системе документа
        
        :param _h: геодезическая высота на эллипсоиде документа
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUserGeoToGeo3D_t (_hmap, _huser, _bx, _ly, _h)

    mapUserGeoToGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUserGeoToGeo', maptype.HMAP, ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapUserGeoToGeo(_hmap: maptype.HMAP, _huser: ctypes.c_void_p, _bx: ctypes.POINTER(ctypes.c_double), _ly: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Преобразование геодезических пользовательских координат в геодезические координаты документа
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _huser: идентификатор пользовательской системы координат
        
        :param _bx: широта в радианах в пользовательской системе
        
        :param _ly: долгота в радианах в пользовательской системе Полученные координаты будут в радианах: bx - широта в системе документа, ly - долгота в системе документа
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUserGeoToGeo_t (_hmap, _huser, _bx, _ly)

    mapCompareSystemParametersPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCompareSystemParametersPro', ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_long, ctypes.POINTER(mapcreat.LOCALTRANSFORM), ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_long, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapCompareSystemParametersPro(_mapreg1: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum1: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid1: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype1: int, _tparm1: ctypes.POINTER(mapcreat.LOCALTRANSFORM), _mapreg2: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum2: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid2: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype2: int, _tparm2: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        """
        Сравнить параметры двух систем координат
        
        :param _mapreg1: параметры первой системы координат
        
        :param _datum1: параметры пересчета с эллипсоида первой системы координат к ``WGS84``, или ``0``
        
        :param _ellipsoid1: параметры пользовательского эллипсоида для первой системы координат, только когда поле EllipsoidKind в ``MAPREGISTEREX`` равно ``USERELLIPSOID``, или ``0`` type1 - тип локального преобразования первой системы координат, описан в ``TRANSFORMTYPE`` в mapcreat.h, или ``0``
        
        :param _tparm1: параметры локального преобразования координат для первой системы координат, или ``0``
        
        :param _mapreg2: параметры второй системы координат
        
        :param _datum2: параметры пересчета с эллипсоида второй системы координат к ``WGS84``, или ``0``
        
        :param _ellipsoid2: параметры пользовательского эллипсоида для второй системы координат, или ``0`` type2 - тип локального преобразования второй системы координат, описан в ``TRANSFORMTYPE`` в mapcreat.h, или ``0``
        
        :param _tparm2: параметры локального преобразования координат второй системы координат, или ``0``
        
        :returns: При несовпадении каких-либо значений параметров возвращает ненулевое значение Некоторые несовпадающие параметры могут считаться идентичными Например, топографическая карта UTM и обзорно-географическая карта ``UTM`` - обозначают одно и тоже
        :rtype: int
        """
        return mapCompareSystemParametersPro_t (_mapreg1, _datum1, _ellipsoid1, _ttype1, _tparm1, _mapreg2, _datum2, _ellipsoid2, _ttype2, _tparm2)

    mapCompareSystemParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCompareSystemParameters', ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapCompareSystemParameters(_mapreg1: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum1: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid1: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _mapreg2: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum2: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid2: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        """
        Сравнить параметры двух систем координат
        
        :param _mapreg1: параметры первой системы координат
        
        :param _datum1: параметры пересчета с эллипсоида первой системы координат к ``WGS84``, или ``0``
        
        :param _ellipsoid1: параметры пользовательского эллипсоида для первой системы координат, только когда поле EllipsoidKind в ``MAPREGISTEREX`` равно ``USERELLIPSOID``, или ``0``
        
        :param _mapreg2: параметры второй системы координат
        
        :param _datum2: параметры пересчета с эллипсоида второй системы координат к ``WGS84``, или ``0``
        
        :param _ellipsoid2: параметры пользовательского эллипсоида для второй системы координат, или ``0``
        
        :returns: При несовпадении каких-либо значений параметров возвращает ненулевое значение
        :rtype: int
        """
        return mapCompareSystemParameters_t (_mapreg1, _datum1, _ellipsoid1, _mapreg2, _datum2, _ellipsoid2)

    mapCompareUserSystemParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCompareUserSystemParameters', ctypes.c_void_p, ctypes.c_void_p)
    def mapCompareUserSystemParameters(_huser1: ctypes.c_void_p, _huser2: ctypes.c_void_p) -> int:
        """
        Сравнить параметры двух пользовательских систем координат
        
        :param _huser1: идентификатор первой пользовательской системы координат
        
        :param _huser2: идентификатор второй пользовательской системы координат
        
        :returns: При несовпадении каких-либо значений параметров возвращает ненулевое значение
        :rtype: int
        """
        return mapCompareUserSystemParameters_t (_huser1, _huser2)

    mapGetUserSystemXmlNode_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetUserSystemXmlNode', ctypes.c_void_p, maptype.PWCHAR)
    def mapGetUserSystemXmlNode(_huser: ctypes.c_void_p, _name: mapsyst.WTEXT) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить описание пользовательской системы координат в виде XML-строки, заканчивающейся нулем
        
        :param _huser: идентификатор пользовательской системы координат
        
        :param _name: условное имя системы координат (атрибут Name), указывается обязательно Строка содержит узел с названием Project (смотри mapOpenMapRegisterListUn())

        Пример XML::

            <Project Name="Nicaragua NAD-27"><Projection Type="Transverse Mercator" CentralMeridian="-87.0" ...
            ScaleFactor="0.9996" Angle="0.0"/><Spheroid Type="Clarke 1866" Parm="6378206.400, 294.97869821"/>
            <Datum DX="2.478" ... M="0.000000685000"/></Project>
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        
        .. note::

           После чтения строки необходимо освободить память через mapFreeUserSystemXmlNode
        """
        return mapGetUserSystemXmlNode_t (_huser, _name.buffer())

    mapFreeUserSystemXmlNode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeUserSystemXmlNode', ctypes.c_char_p)
    def mapFreeUserSystemXmlNode(_point: ctypes.c_char_p) -> ctypes.c_void_p:
        """
        Освободить память строки с описанием параметров системы координат
        
        :param _point: адрес строки, полученной из mapGetUserSystemXmlNode
        """
        return mapFreeUserSystemXmlNode_t (_point)

    mapSetCurrentPointFormat_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetCurrentPointFormat', maptype.HMAP, ctypes.c_long)
    def mapSetCurrentPointFormat(_hmap: maptype.HMAP, _format: int) -> int:
        """
        Установить формат отображения текущих координат курсора
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _format: номер формата отображения координат (``CURRENTPOINTFORMAT``, например: ``PLANEPOINT``, ``PLANE42POINT``, ``GEORADWGS84``)
        
        :returns: При ошибке возвращает ноль, иначе - установленное значение
        :rtype: int
        """
        return mapSetCurrentPointFormat_t (_hmap, _format)

    mapGetCurrentPointFormat_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetCurrentPointFormat', maptype.HMAP)
    def mapGetCurrentPointFormat(_hmap: maptype.HMAP) -> int:
        """
        Запросить формат отображения текущих координат курсора
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: Возвращает номер формата отображения координат (CURRENTPOINTFORMAT) При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetCurrentPointFormat_t (_hmap)

    mapSetCurrentPointPlaneDecimal_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetCurrentPointPlaneDecimal', maptype.HMAP, ctypes.c_long)
    def mapSetCurrentPointPlaneDecimal(_hmap: maptype.HMAP, _decimal: int) -> int:
        """
        Установить число цифр после точки (запятой) в формате отображения координат на плоскости
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _decimal: число цифр после точки в формате отображения текущих координат курсора на плоскости
        
        :returns: При ошибке возвращает ноль, иначе - установленное значение
        :rtype: int
        """
        return mapSetCurrentPointPlaneDecimal_t (_hmap, _decimal)

    mapGetCurrentPointPlaneDecimal_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetCurrentPointPlaneDecimal', maptype.HMAP)
    def mapGetCurrentPointPlaneDecimal(_hmap: maptype.HMAP) -> int:
        """
        Запросить число цифр после точки (запятой) в формате отображения координат на плоскости
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает ноль, иначе - установленное значение
        :rtype: int
        """
        return mapGetCurrentPointPlaneDecimal_t (_hmap)

    mapPlaneToPointFormat_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPlaneToPointFormat', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapPlaneToPointFormat(_hmap: maptype.HMAP, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Пересчитать плоские прямоугольные координаты документа в заданный формат отображения
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _x: координата в метрах на север в системе открытых данных (документа)
        
        :param _y: координата в метрах на восток в системе открытых данных (документа)
        
        :param _h: высота в метрах в системе открытых данных (документа) или ``0`` Формат отображения устанавливается вызовом mapSetCurrentPointFormat
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPlaneToPointFormat_t (_hmap, _x, _y, _h)

    mapPlaneToPointFormatStringPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPlaneToPointFormatStringPro', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_void_p, maptype.PWCHAR, ctypes.c_long)
    def mapPlaneToPointFormatStringPro(_hmap: maptype.HMAP, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _hegm: ctypes.c_void_p, _place: mapsyst.WTEXT, _size: int) -> int:
        """
        Пересчитать плоские прямоугольные координаты документа в заданный формат в виде комментария
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _x: координата в метрах на север в системе открытых данных (документа)
        
        :param _y: координата в метрах на восток в системе открытых данных (документа)
        
        :param _h: высота в метрах в системе открытых данных (документа) или ``0``
        
        :param _hegm: идентификатор модели геоида для пересчета ортометрической высоты в геодезическую или ``0`` Для получения hegm применяется функция mapOpenEgmPro
        
        :param _place: адрес строки для записи результата
        
        :param _size: размер выделеной строки (не менее ``256`` байт) Пример строки: B= -``73`` ° ``27``' ``04.53````"  L= 175° 51' 21.07"``  H= ``109.51`` m (``WGS84``) X= ``6 309 212``.``12`` м   Y= ``7 412 249``.``25`` м (СК``42``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPlaneToPointFormatStringPro_t (_hmap, _x, _y, _h, _hegm, _place.buffer(), _size)

    mapPlaneToPointFormatStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPlaneToPointFormatStringUn', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), maptype.PWCHAR, ctypes.c_long)
    def mapPlaneToPointFormatStringUn(_hmap: maptype.HMAP, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _place: mapsyst.WTEXT, _size: int) -> int:
        """
        Пересчитать плоские прямоугольные координаты документа в заданный формат в виде комментария
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _x: координата в метрах на север в системе открытых данных (документа)
        
        :param _y: координата в метрах на восток в системе открытых данных (документа)
        
        :param _h: высота в метрах в системе открытых данных (документа) или ``0``
        
        :param _place: адрес строки для записи результата
        
        :param _size: размер выделеной строки (не менее ``256`` байт) Пример строки: B= -``73`` ° ``27``' ``04.53````"  L= 175° 51' 21.07"``  H= ``109.51`` m (``WGS84``) X= ``6 309 212``.``12`` м   Y= ``7 412 249``.``25`` м (СК``42``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPlaneToPointFormatStringUn_t (_hmap, _x, _y, _h, _place.buffer(), _size)

    mapPlaneToPointFormatText_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPlaneToPointFormatText', maptype.HMAP, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_void_p, ctypes.c_char_p, ctypes.c_long)
    def mapPlaneToPointFormatText(_hmap: maptype.HMAP, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _hegm: ctypes.c_void_p, _place: ctypes.c_char_p, _size: int) -> int:
        """
        Пересчитать плоские прямоугольные координаты документа в заданный формат в виде строки
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _x: координата в метрах на север в системе открытых данных (документа)
        
        :param _y: координата в метрах на восток в системе открытых данных (документа)
        
        :param _h: высота в метрах в системе открытых данных (документа) или ``0``
        
        :param _hegm: идентификатор модели геоида для пересчета ортометрической высоты в геодезическую или ``0`` Для получения hegm применяется функция mapOpenEgmPro
        
        :param _place: адрес строки для записи результата
        
        :param _size: размер выделеной строки (не менее ``256`` байт) Пример строки: ``-73.45093678`` ``175.83160324`` ``109.51`` ``6309212.123`` ``7412249.257``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPlaneToPointFormatText_t (_hmap, _x, _y, _h, _hegm, _place, _size)

    mapPlaneToStringUnEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapPlaneToStringUnEx', ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapPlaneToStringUnEx(_x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _h: ctypes.POINTER(ctypes.c_double), _place: mapsyst.WTEXT, _size: int, _maptype: int, _decimal: int) -> ctypes.c_void_p:
        """
        Вывод плоских прямоугольных координат точки в строку
        
        :param _x: координата в метрах на север в системе открытых данных (документа)
        
        :param _y: координата в метрах на восток в системе открытых данных (документа)
        
        :param _h: высота в метрах в системе открытых данных (документа) или ``0``
        
        :param _place: адрес строки для размещения результата
        
        :param _size: размер строки в байтах (не менее ``80`` байт)
        
        :param _maptype: тип карты (``MAPTYPE``), если не равен нулю, то добавляется строка с обозначением системы координат: ``"   (СК42)"``, ``"   (CК95)"``,...
        
        :param _decimal: число знаков после запятой (точки) Пример результата: ``"X=  438 145.27 m  Y= 6 230 513.03 m  H=  54.12 m"``
        """
        return mapPlaneToStringUnEx_t (_x, _y, _h, _place.buffer(), _size, _maptype, _decimal)

    mapXYZToString_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapXYZToString', ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_char_p, ctypes.c_long, ctypes.c_long)
    def mapXYZToString(_x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _z: ctypes.POINTER(ctypes.c_double), _place: ctypes.c_char_p, _size: int, _maptype: int) -> ctypes.c_void_p:
        """
        Вывод геоцентрических координат точки в строку
        
        :param _x: геоцентрическая координата в метрах
        
        :param _y: геоцентрическая координата в метрах h - геоцентрическая координата в метрах
        
        :param _place: адрес строки для размещения результата
        
        :param _size: размер строки в байтах (не менее ``80`` байт) Пример результата: ``"X= -4 438 145.271 Y= 3 230 513.034 H= 6 632 054.125 m"``
        """
        return mapXYZToString_t (_x, _y, _z, _place, _size, _maptype)

    mapDoubleFormatPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDoubleFormatPro', ctypes.c_double, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapDoubleFormatPro(_value: float, _string: mapsyst.WTEXT, _size: int, _precision: int, _separator: int) -> int:
        """
        Запись вещественного числа в символьном виде с фиксированной точкой
        
        :param _value: значение числа, записываемого в строку
        
        :param _string: адрес строки для размещения результата
        
        :param _size: длина строки в байтах (не менее ``32``)
        
        :param _precision: число знаков после точки (запятой), если равно ``0``, то округление до целого числа, если меньше ``0``, то округление в большую сторону
        
        :param _separator: разделитель целой и дробной части: ``0`` - десятичную точку не изменять ``1`` - заменить десятичную точку на символ, установленный в системе '.' или ',' - заменить десятичную точку на separator: '.' или ','
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDoubleFormatPro_t (_value, _string.buffer(), _size, _precision, _separator)

    mapDoubleFormat_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDoubleFormat', ctypes.c_double, ctypes.c_char_p, ctypes.c_long, ctypes.c_long)
    def mapDoubleFormat(_value: float, _string: ctypes.c_char_p, _size: int, _precision: int) -> int:
        """
        Запись вещественного числа в символьном виде с фиксированной точкой
        
        :param _value: значение числа, записываемого в строку
        
        :param _string: адрес строки для размещения результата
        
        :param _size: длина строки в байтах (не менее ``16``)
        
        :param _precision: число знаков после точки (запятой)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDoubleFormat_t (_value, _string, _size, _precision)

    mapDoubleToStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDoubleToStringUn', ctypes.c_double, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapDoubleToStringUn(_value: float, _string: mapsyst.WTEXT, _size: int, _precision: int) -> int:
        """
        Запись вещественного числа в символьном виде с фиксированной точкой со вставкой разделяющих пробелов
        
        :param _value: значение числа, записываемого в строку
        
        :param _string: адрес строки для размещения результата
        
        :param _size: длина строки в байтах (не менее ``16``)
        
        :param _precision: число знаков после точки (запятой) При записи числа в строку выполняется разделение на тройки символов от конца строки к началу Например: ``7 390 621``.``458``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDoubleToStringUn_t (_value, _string.buffer(), _size, _precision)

    mapLongToStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLongToStringUn', ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapLongToStringUn(_value: int, _string: mapsyst.WTEXT, _size: int) -> int:
        """
        Запись целого числа в символьном виде со вставкой разделяющих пробелов
        
        :param _value: значение числа, записываемого в строку
        
        :param _string: адрес строки для размещения результата
        
        :param _size: длина строки в байтах (не менее ``16``) При записи числа в строку выполняется разделение на тройки символов от конца строки к началу Например: ``7 390 621``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapLongToStringUn_t (_value, _string.buffer(), _size)

    mapInt64ToStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapInt64ToStringUn', ctypes.c_int64, maptype.PWCHAR, ctypes.c_long)
    def mapInt64ToStringUn(_value: int, _string: mapsyst.WTEXT, _size: int) -> int:
        """
        Запись целого числа типа __int64 в символьном виде со вставкой разделяющих пробелов
        
        :param _value: значение числа, записываемого в строку
        
        :param _string: адрес строки для размещения результата
        
        :param _size: длина строки в байтах (не менее ``32``) При записи числа в строку выполняется разделение на тройки символов от конца строки к началу
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapInt64ToStringUn_t (_value, _string.buffer(), _size)

    mapRoundDouble_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapRoundDouble', ctypes.c_double, ctypes.c_int)
    def mapRoundDouble(_value: float, _count: int) -> float:
        """
        Округлить дробную часть числа до заданного числа знаков
        
        :param _value: исходное значение числа, которое нужно округлить
        
        :param _count: число знаков после запятой (от ``0`` до ``9``) Целая часть числа остается без изменения
        """
        return mapRoundDouble_t (_value, _count)

    mapScaleToStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapScaleToStringUn', ctypes.c_double, maptype.PWCHAR, ctypes.c_long)
    def mapScaleToStringUn(_scale: float, _string: mapsyst.WTEXT, _size: int) -> int:
        """
        Запись масштаба в символьном виде со вставкой разделяющих пробелов
        
        :param _scale: значение знаменателя масштаба, записываемого в строку
        
        :param _string: адрес строки для размещения результата
        
        :param _size: длина строки в байтах (не менее ``20``) При записи числа в строку выполняется разделение на тройки символов от конца строки к началу Например: ``"1 : 50 000"``, ``"2 : 1"`` - если scale ``< 1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapScaleToStringUn_t (_scale, _string.buffer(), _size)

    mapGetParametersForEPSG_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetParametersForEPSG', ctypes.c_long, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapGetParametersForEPSG(_epsgcode: int, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        """
        Запросить параметры проекции и системы координат по коду EPSG
        
        :param _epsgcode: код ``EPSG``, для СК-``42`` зоны ``2``-``32 : 28402``-``28432``, для СК-``95`` зоны ``4``-``32: 20004``-``20032``
        
        :param _mapreg: параметры системы координат и проекции
        
        :param _datum: параметры пересчета с эллипсоида рабочей системы координат к ``WGS84``
        
        :param _ellipsoid: параметры пользовательского эллипсоида для рабочей системы координат
        
        :returns: Для геодезических систем координат возвращает 2, для геоцентрических - 3, для плоских прямоугольных - 1 При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если код EPSG задает геодезическую или геоцентрическую систему координат,
           то устанавливается проекция Широта\\Долгота и соответствующие
           параметры эллипсоида и датум
           Если код EPSG задает плоскую прямоугольную систему координат,
           то все параметры устанавливаются из базы EPSG
        """
        return mapGetParametersForEPSG_t (_epsgcode, _mapreg, _datum, _ellipsoid)

    mapRegisterUserEpsgParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRegisterUserEpsgParameters', ctypes.c_long, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapRegisterUserEpsgParameters(_epsg: int, _mapregister: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellips: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        """
        Зарегистрировать пользовательский код параметров Epsg
        
        :param _epsg: регистрируемый код системы координат mapreg - параметры системы координат и проекции
        
        :param _datum: параметры пересчета от заданного эллипсоида к эллипсоиду ``WGS84`` ellipsoid - параметры эллипсоида Заданный код и его параметры запоминаются на сеанс работы приложения и будут выдаваться по запросу из mapGetParametersForEPSG()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapRegisterUserEpsgParameters_t (_epsg, _mapregister, _datum, _ellips)

    mapOpenEPSGDatabase_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapOpenEPSGDatabase')
    def mapOpenEPSGDatabase() -> ctypes.c_void_p:
        """
        Открыть базу данных EPSG
        
        :returns: При успешном выполнении возвращает идентификатор открытой базы данных EPSG При ошибке возвращает ноль
        """
        return mapOpenEPSGDatabase_t ()

    mapCloseEPSGDatabase_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseEPSGDatabase', ctypes.c_void_p)
    def mapCloseEPSGDatabase(_epsgdata: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Закрыть базу данных EPSG
        
        :param _epsgdata: идентификатор открытой базы данных ``EPSG``
        """
        return mapCloseEPSGDatabase_t (_epsgdata)

    mapGetEPSGProjectedSystemCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetEPSGProjectedSystemCount', ctypes.c_void_p)
    def mapGetEPSGProjectedSystemCount(_epsgdata: ctypes.c_void_p) -> int:
        """
        Запросить количество прямоугольных систем координат в базе данных EPSG
        
        :param _epsgdata: идентификатор открытой базы данных ``EPSG``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetEPSGProjectedSystemCount_t (_epsgdata)

    mapGetEPSGGeodeticSystemCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetEPSGGeodeticSystemCount', ctypes.c_void_p)
    def mapGetEPSGGeodeticSystemCount(_epsgdata: ctypes.c_void_p) -> int:
        """
        Запросить количество геодезических систем координат в базе данных EPSG
        
        :param _epsgdata: идентификатор открытой базы данных ``EPSG``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetEPSGGeodeticSystemCount_t (_epsgdata)

    mapReadEPSGProjectedSystemByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapReadEPSGProjectedSystemByNumber', ctypes.c_void_p, ctypes.c_long, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.EPSGRECTSYS), ctypes.POINTER(mapcreat.EPSGGEODSYS), ctypes.POINTER(mapcreat.EPSGMEASUNIT))
    def mapReadEPSGProjectedSystemByNumber(_epsgdata: ctypes.c_void_p, _number: int, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _rectsys: ctypes.POINTER(mapcreat.EPSGRECTSYS), _geodsys: ctypes.POINTER(mapcreat.EPSGGEODSYS), _unit: ctypes.POINTER(mapcreat.EPSGMEASUNIT)) -> int:
        """
        Считать данные на прямоугольную систему координат по номеру записи в базе данных EPSG
        
        :param _epsgdata: идентификатор открытой базы данных ``EPSG``
        
        :param _number: номер записи в списке прямоугольных систем координат c ``1``
        
        :param _mapreg: параметры системы координат и проекции
        
        :param _ellipsoid: параметры эллипсоида
        
        :param _datum: параметры пересчета от заданного эллипсоида к эллипсоиду ``WGS84``
        
        :param _rectsys: параметры прямоугольной системы координат
        
        :param _geodsys: параметры базовой геодезической системы координат
        
        :param _unit: единицы измерения
        
        :returns: При ошибке или при выходе за границы набора данных возвращает ноль
        :rtype: int
        """
        return mapReadEPSGProjectedSystemByNumber_t (_epsgdata, _number, _mapreg, _ellipsoid, _datum, _rectsys, _geodsys, _unit)

    mapReadEPSGGeodeticSystemByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapReadEPSGGeodeticSystemByNumber', ctypes.c_void_p, ctypes.c_long, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.EPSGGEODSYS))
    def mapReadEPSGGeodeticSystemByNumber(_epsgdata: ctypes.c_void_p, _number: int, _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _geodsys: ctypes.POINTER(mapcreat.EPSGGEODSYS)) -> int:
        """
        Считать параметры геодезической системы координат по порядковому номеру в базе данных EPSG
        
        :param _epsgdata: идентификатор открытой базы данных ``EPSG``
        
        :param _number: порядковый номер геодезической системы координат в базе данных ``EPSG`` c ``1``
        
        :param _ellipsoid: параметры эллипсоида или ``0``
        
        :param _datum: параметры пересчета от заданного эллипсоида к эллипсоиду ``WGS84``
        
        :param _geodsys: параметры геодезической системы координат или ``0``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapReadEPSGGeodeticSystemByNumber_t (_epsgdata, _number, _ellipsoid, _datum, _geodsys)

    mapGetEPSGGeodeticSystem_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetEPSGGeodeticSystem', ctypes.c_long, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.EPSGGEODSYS))
    def mapGetEPSGGeodeticSystem(_epsgcode: int, _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _geodsys: ctypes.POINTER(mapcreat.EPSGGEODSYS)) -> int:
        """
        Запросить параметры геодезической системы координат по коду
        
        :param _epsgcode: код геодезической системы координат в базе данных ``EPSG``
        
        :param _ellipsoid: параметры эллипсоида
        
        :param _datum: параметры пересчета от заданного эллипсоида к эллипсоиду ``WGS84``
        
        :param _geodsys: параметры геодезической системы координат
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetEPSGGeodeticSystem_t (_epsgcode, _ellipsoid, _datum, _geodsys)

    mapGetEPSGGeodeticSystemByName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetEPSGGeodeticSystemByName', ctypes.c_char_p, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.EPSGGEODSYS))
    def mapGetEPSGGeodeticSystemByName(_name: ctypes.c_char_p, _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _geodsys: ctypes.POINTER(mapcreat.EPSGGEODSYS)) -> int:
        """
        Запросить параметры геодезической системы координат по имени в базе данных EPSG
        
        :param _name: имя геодезической системы координат
        
        :param _ellipsoid: параметры эллипсоида
        
        :param _datum: параметры пересчета от заданного эллипсоида к эллипсоиду ``WGS84``
        
        :param _geodsys: параметры геодезической системы координат
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetEPSGGeodeticSystemByName_t (_name, _ellipsoid, _datum, _geodsys)

    mapGetEPSGProjectedSystem_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetEPSGProjectedSystem', ctypes.c_long, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.EPSGRECTSYS))
    def mapGetEPSGProjectedSystem(_epsgcode: int, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _rectsys: ctypes.POINTER(mapcreat.EPSGRECTSYS)) -> int:
        """
        Запросить параметры прямоугольной системы координат по коду в базе данных EPSG
        
        :param _epsgcode: код прямоугольной системы координат в базе данных ``EPSG``
        
        :param _mapreg: параметры системы координат и проекции
        
        :param _rectsys: параметры прямоугольной системы координат
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetEPSGProjectedSystem_t (_epsgcode, _mapreg, _rectsys)

    mapGetEPSGUnit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetEPSGUnit', ctypes.c_long, ctypes.POINTER(mapcreat.EPSGMEASUNIT))
    def mapGetEPSGUnit(_epsgcode: int, _unit: ctypes.POINTER(mapcreat.EPSGMEASUNIT)) -> int:
        """
        Запросить параметры единицы измерения по коду в базе данных EPSG
        
        :param _epsgcode: код единицы измерения в базе данных ``EPSG``
        
        :param _unit: параметры единицы измерения
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetEPSGUnit_t (_epsgcode, _unit)

    mapSetProj4String_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetProj4String', ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.c_char_p, ctypes.c_long, ctypes.c_int)
    def mapSetProj4String(_mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _proj4str: ctypes.c_char_p, _proj4strsize: int, _flag3D: int) -> int:
        """
        Заполнить параметры системы координат в виде строки Proj4
        
        на основе MAPREGISTEREX, ELLIPSOIDPARAM, DATUMPARAM
        Параметры:
        - mapreg       - паспортные данные электронной карты
        - ellipsoid    - параметры эллипсоида
        - datum        - параметры датума
        - proj4str     - буфер для выходной строки с описанием системы координат
        - proj4strsize - размер буфера в байтах
        - flag3D       - признак необходимости добавить информацию о системе высот
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetProj4String_t (_mapreg, _ellipsoid, _datum, _proj4str, _proj4strsize, _flag3D)

    mapSetWKTStringEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetWKTStringEx', ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.c_char_p, ctypes.c_long, ctypes.c_int)
    def mapSetWKTStringEx(_mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _wktstr: ctypes.c_char_p, _wktstrsize: int, _flag3D: int) -> int:
        """
        Заполнить WKT строку из MAPREGISTEREX, ELLIPSOIDPARAM, DATUMPARAM
        
        :param _mapreg: параметры системы координат и проекции
        
        :param _ellipsoid: параметры эллипсоида
        
        :param _datum: параметры пересчета от заданного эллипсоида к эллипсоиду ``WGS84``
        
        :param _wktstr: заполняемая строка с описанием системы координат
        
        :param _wktstrsize: зарезервированный размер строки (``4`` Кбайта достаточно)
        
        :param _flag3D: флаг добавления вертикальной системы координат, соответствующей значению поля ``MAPREGISTEREX``::HeightSystem
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetWKTStringEx_t (_mapreg, _ellipsoid, _datum, _wktstr, _wktstrsize, _flag3D)

    mapReadWKTString_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapReadWKTString', ctypes.c_char_p, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapReadWKTString(_wktstr: ctypes.c_char_p, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        """
        Заполнить MAPREGISTEREX, ELLIPSOIDPARAM, DATUMPARAM из WKT строки
        
        :param _wktstr: строка с описанием системы координат
        
        :param _mapreg: параметры системы координат и проекции
        
        :param _ellipsoid: заполняемые параметры эллипсоида
        
        :param _datum: параметры пересчета от заданного эллипсоида к эллипсоиду ``WGS84``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapReadWKTString_t (_wktstr, _mapreg, _ellipsoid, _datum)

    mapReadWKTStringEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapReadWKTStringEx', ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.EPSGRECTSYS), ctypes.POINTER(mapcreat.EPSGGEODSYS), ctypes.POINTER(mapcreat.EPSGMEASUNIT))
    def mapReadWKTStringEx(_wktstr: ctypes.c_char_p, _isprojection: ctypes.POINTER(ctypes.c_int), _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _sysrect: ctypes.POINTER(mapcreat.EPSGRECTSYS), _sysgeo: ctypes.POINTER(mapcreat.EPSGGEODSYS), _unit: ctypes.POINTER(mapcreat.EPSGMEASUNIT)) -> int:
        """
        Прочитать описание системы координат из строки WKT (стандарт OGC 12-063r5)
        
        :param _wktstr: ``WKT``-строка с описанием системы координат
        
        :param _mapreg: параметры системы координат и проекции или ``0``
        
        :param _ellipsoid: параметры эллипсоида или ``0``
        
        :param _datum: параметры пересчета от заданного эллипсоида к эллипсоиду ``WGS84`` или ``0``
        
        :param _sysrect: параметры прямоугольной системы координат (при isprojection ``= 1``) или ``0``
        
        :param _sysgeo: параметры геодзической системы координат (при isprojection ``= 0``) или ``0``
        
        :param _unit: заполняемые параметры единицы измерения или ``0``
        
        :returns: isprojection - возвращает признак прямоугольной системы координат (1) При ошибке возвращает ноль
        :rtype: int
        """
        return mapReadWKTStringEx_t (_wktstr, _isprojection, _mapreg, _ellipsoid, _datum, _sysrect, _sysgeo, _unit)

    mapFindEPSGCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapFindEPSGCode', ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapFindEPSGCode(_mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _datum: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        """
        Определить EPSG код для известных систем координат
        
        :param _mapreg: параметры системы координат и проекции или ``0``
        
        :param _ellipsoid: параметры эллипсоида или ``0``
        
        :param _datum: параметры пересчета от заданного эллипсоида к эллипсоиду ``WGS84`` или ``0``
        
        :returns: Возвращает код EPSG или ноль
        :rtype: int
        """
        return mapFindEPSGCode_t (_mapreg, _ellipsoid, _datum)

    mapOpenMapRegisterListUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAPREG,'mapOpenMapRegisterListUn', maptype.PWCHAR)
    def mapOpenMapRegisterListUn(_name: mapsyst.WTEXT) -> maptype.HMAPREG:
        """
        Открыть список параметров систем координат
        
        :param _name: имя файла списка параметров
        
        :returns: При успешном выполнении возвращает идентификатор списка в памяти При ошибке возвращает ноль
        :rtype: maptype.HMAPREG
        """
        return mapOpenMapRegisterListUn_t (_name.buffer())

    mapCreateMapRegisterListUn_t = mapsyst.GetProcAddress(acceslib,maptype.HMAPREG,'mapCreateMapRegisterListUn', maptype.PWCHAR)
    def mapCreateMapRegisterListUn(_name: mapsyst.WTEXT) -> maptype.HMAPREG:
        """
        Создать список параметров систем координат
        
        :param _name: имя файла списка параметров
        
        :returns: При успешном выполнении возвращает идентификатор списка в памяти При ошибке возвращает ноль
        :rtype: maptype.HMAPREG
        """
        return mapCreateMapRegisterListUn_t (_name.buffer())

    mapCloseMapRegisterList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseMapRegisterList', maptype.HMAPREG)
    def mapCloseMapRegisterList(_hmapreg: maptype.HMAPREG) -> ctypes.c_void_p:
        """
        Закрыть список параметров систем координат
        
        :param _hmapreg: идентификатор списка параметров систем координат
        """
        return mapCloseMapRegisterList_t (_hmapreg)

    mapMapRegisterListCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapMapRegisterListCount', maptype.HMAPREG)
    def mapMapRegisterListCount(_hmapreg: maptype.HMAPREG) -> int:
        """
        Запросить число систем координат в списке
        
        :param _hmapreg: идентификатор списка параметров систем координат
        
        :returns: При успешном выполнении возвращает число записей параметров Одной системе соответствует один узел ``"Project"`` в списке ``<ProjectList Version="1.0">`` При ошибке возвращает ноль
        :rtype: int
        """
        return mapMapRegisterListCount_t (_hmapreg)

    mapMapRegisterListNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapMapRegisterListNameUn', maptype.HMAPREG, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapMapRegisterListNameUn(_hmapreg: maptype.HMAPREG, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить название системы координат по заданному порядковому номеру в списке
        
        :param _hmapreg: идентификатор списка параметров систем координат
        
        :param _number: порядковый номер записи параметров с ``1``
        
        :param _name: адрес строки для размещения результата
        
        :param _size: размер выделенной строки в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapMapRegisterListNameUn_t (_hmapreg, _number, _name.buffer(), _size)

    mapMapRegisterListCommentUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapMapRegisterListCommentUn', maptype.HMAPREG, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapMapRegisterListCommentUn(_hmapreg: maptype.HMAPREG, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить комментарий для системы координат по порядковому номеру
        
        :param _hmapreg: идентификатор списка параметров систем координат
        
        :param _number: порядковый номер записи параметров с ``1``
        
        :param _name: адрес строки для размещения результата
        
        :param _size: длина выделенной строки для размещения результата
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapMapRegisterListCommentUn_t (_hmapreg, _number, _name.buffer(), _size)

    mapSeekMapRegisterListByEPSG_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekMapRegisterListByEPSG', maptype.HMAPREG, ctypes.c_long)
    def mapSeekMapRegisterListByEPSG(_hmapreg: maptype.HMAPREG, _epsg: int) -> int:
        """
        Запросить порядковый номер записи в списке по коду EPSG
        
        :param _hmapreg: идентификатор списка параметров систем координат
        
        :param _epsg: код ``EPSG`` для системы координат
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSeekMapRegisterListByEPSG_t (_hmapreg, _epsg)

    mapMapRegisterListEPSG_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapMapRegisterListEPSG', maptype.HMAPREG, ctypes.c_long)
    def mapMapRegisterListEPSG(_hmapreg: maptype.HMAPREG, _number: int) -> int:
        """
        Запросить код EPSG для системы координат по порядковому номеру
        
        :param _hmapreg: идентификатор списка параметров систем координат
        
        :param _number: порядковый номер записи параметров с ``1``
        
        :returns: Если код не задан - возвращает ``"-1"`` При ошибке возвращает ноль
        :rtype: int
        """
        return mapMapRegisterListEPSG_t (_hmapreg, _number)

    mapMapRegisterListCrsIdentUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapMapRegisterListCrsIdentUn', maptype.HMAPREG, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapMapRegisterListCrsIdentUn(_hmapreg: maptype.HMAPREG, _number: int, _ident: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить идентификатор для системы координат по порядковому номеру
        
        :param _hmapreg: идентификатор списка параметров систем координат
        
        :param _number: порядковый номер записи параметров с ``1``
        
        :param _ident: адрес строки для размещения идентификатора
        
        :param _size: длина выделенной строки для размещения идентификатора
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapMapRegisterListCrsIdentUn_t (_hmapreg, _number, _ident.buffer(), _size)

    mapMapRegisterListParametersPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapMapRegisterListParametersPro', maptype.HMAPREG, ctypes.c_long, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapMapRegisterListParametersPro(_hmapreg: maptype.HMAPREG, _number: int, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: ctypes.POINTER(ctypes.c_long), _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        """
        Запросить параметры системы координат по заданному порядковому номеру
        
        :param _hmapreg: идентификатор списка параметров систем координат
        
        :param _number: порядковый номер записи параметров с ``1``
        
        :param _mapreg: параметры проекции ``<Projection ...>``
        
        :param _datum: параметры датума ``<Datum ...>``
        
        :param _ellparm: параметры эллипсоида ``<Spheroid ...>``
        
        :param _ttype: адрес поля для записи типа локального преобразования координат (``TRANSFORMTYPE`` в mapcreat.h) или ``0``
        
        :param _tparm: параметры локального преобразования координат
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapMapRegisterListParametersPro_t (_hmapreg, _number, _mapreg, _datum, _ellparm, _ttype, _tparm)

    mapAppendMapRegisterListParametersPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendMapRegisterListParametersPro', maptype.HMAPREG, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_long, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapAppendMapRegisterListParametersPro(_hmapreg: maptype.HMAPREG, _name: mapsyst.WTEXT, _comment: mapsyst.WTEXT, _epsgcode: int, _ident: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        """
        Добавить запись параметров системы координат
        
        :param _hmapreg: идентификатор списка параметров систем координат
        
        :param _name: уникальное название системы отсчета
        
        :param _comment: комментарий для системы отсчета или ноль
        
        :param _epsgcode: код ``EPSG`` или ноль
        
        :param _ident: идентификатор системы отсчета или ноль
        
        :param _mapreg: описание параметров системы отсчета
        
        :param _datum: описание параметров датума или ноль ellparam - описание параметров эллипсоида или ноль
        
        :param _ttype: тип локального преобразования координат (``TRANSFORMTYPE`` в mapcreat.h) или ``0``
        
        :param _tparm: параметры локального преобразования координат
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendMapRegisterListParametersPro_t (_hmapreg, _name.buffer(), _comment.buffer(), _epsgcode, _ident.buffer(), _mapreg, _datum, _ellparm, _ttype, _tparm)

    mapDeleteMapRegisterListParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteMapRegisterListParameters', maptype.HMAPREG, ctypes.c_long)
    def mapDeleteMapRegisterListParameters(_hmapreg: maptype.HMAPREG, _number: int) -> int:
        """
        Удалить запись параметров систем отсчета по порядковому номеру в списке
        
        :param _hmapreg: идентификатор списка параметров систем координат
        
        :param _number: порядковый номер записи параметров c ``1`` Для немедленного изменения данных в файле нужно вызвать функцию mapCommitMapRegisterList
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteMapRegisterListParameters_t (_hmapreg, _number)

    mapUpdateMapRegisterListNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateMapRegisterListNameUn', maptype.HMAPREG, ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, maptype.PWCHAR)
    def mapUpdateMapRegisterListNameUn(_hmapreg: maptype.HMAPREG, _number: int, _name: mapsyst.WTEXT, _comment: mapsyst.WTEXT, _code: int, _ident: mapsyst.WTEXT) -> int:
        """
        Обновить название, комментарий и код системы отсчета по заданному порядковому номеру
        
        :param _hmapreg: идентификатор списка параметров систем координат
        
        :param _number: порядковый номер записи параметров c ``1``
        
        :param _name: название системы отсчета или ``0`` (не менять)
        
        :param _comment: комментарий к системе отсчета или ``0`` (не менять)
        
        :param _code: код ``EPSG`` или ``0`` (не менять)
        
        :param _ident: идентификатор системы отсчета или ``0`` (не менять)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdateMapRegisterListNameUn_t (_hmapreg, _number, _name.buffer(), _comment.buffer(), _code, _ident.buffer())

    mapCommitMapRegisterList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCommitMapRegisterList', maptype.HMAPREG)
    def mapCommitMapRegisterList(_hmapreg: maptype.HMAPREG) -> int:
        """
        Сохранить изменения списка параметров систем отсчета в файле
        
        :param _hmapreg: идентификатор списка параметров систем координат
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCommitMapRegisterList_t (_hmapreg)

    mapUndoMapRegisterList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUndoMapRegisterList', maptype.HMAPREG)
    def mapUndoMapRegisterList(_hmapreg: maptype.HMAPREG) -> int:
        """
        Отменить изменения списка параметров систем отсчета в памяти
        
        :param _hmapreg: идентификатор списка параметров систем координат Отмена изменений может быть выполнена до вызова mapCommitMapRegisterList
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUndoMapRegisterList_t (_hmapreg)

    mapListNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapListNameUn', maptype.HOBJ, maptype.PWCHAR, ctypes.c_long)
    def mapListNameUn(_hobj: maptype.HOBJ, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить название листа на котором расположен объект
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _name: адрес буфера для результата запроса
        
        :param _size: размер буфера в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapListNameUn_t (_hobj, _name.buffer(), _size)

    mapNomenclatureUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapNomenclatureUn', maptype.HOBJ, maptype.PWCHAR, ctypes.c_long)
    def mapNomenclatureUn(_hobj: maptype.HOBJ, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить номенклатуру листа на котором расположен объект
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _name: адрес буфера для результата запроса
        
        :param _size: размер буфера в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapNomenclatureUn_t (_hobj, _name.buffer(), _size)

    mapObjectMapScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectMapScale', maptype.HOBJ)
    def mapObjectMapScale(_hobj: maptype.HOBJ) -> int:
        """
        Запросить базовый масштаб карты
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapObjectMapScale_t (_hobj)

    mapGetRscIdentByObject_t = mapsyst.GetProcAddress(acceslib,maptype.HRSC,'mapGetRscIdentByObject', maptype.HOBJ)
    def mapGetRscIdentByObject(_hobj: maptype.HOBJ) -> maptype.HRSC:
        """
        Запросить идентификатор классификатора карты, содержащей объект
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HRSC
        """
        return mapGetRscIdentByObject_t (_hobj)

    mapObjectKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectKey', maptype.HOBJ)
    def mapObjectKey(_hobj: maptype.HOBJ) -> int:
        """
        Запросить уникальный номер объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapObjectKey_t (_hobj)

    mapSetObjectKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetObjectKey', maptype.HOBJ, ctypes.c_long)
    def mapSetObjectKey(_hobj: maptype.HOBJ, _number: int) -> int:
        """
        Установить уникальный номер объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: уникальный номер объекта в листе Программа, вызывающая данную функцию, должна обеспечить уникальность номеров в листе Для резервирования уникального номера объекта в листе до вызова mapCommitObject можно вызвать функцию mapGetSiteNewObjectKey()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetObjectKey_t (_hobj, _number)

    mapObjectExcode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectExcode', maptype.HOBJ)
    def mapObjectExcode(_hobj: maptype.HOBJ) -> int:
        """
        Запросить классификационный код объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль, ноль допустим для нового объекта до вызова mapCommitObject()
        :rtype: int
        """
        return mapObjectExcode_t (_hobj)

    mapObjectLocal_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectLocal', maptype.HOBJ)
    def mapObjectLocal(_hobj: maptype.HOBJ) -> int:
        """
        Запросить характер локализации объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        """
        return mapObjectLocal_t (_hobj)

    mapObjectNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectNameUn', maptype.HOBJ, maptype.PWCHAR, ctypes.c_long)
    def mapObjectNameUn(_hobj: maptype.HOBJ, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить условное название объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _name: адрес буфера для результата запроса
        
        :param _size: размер буфера в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapObjectNameUn_t (_hobj, _name.buffer(), _size)

    mapObjectComment_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectComment', maptype.HOBJ, maptype.PWCHAR, ctypes.c_long)
    def mapObjectComment(_hobj: maptype.HOBJ, _comment: mapsyst.WTEXT, _size: int) -> int:
        """
        Сформировать строку с описанием объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _comment: адрес буфера для результата запроса
        
        :param _size: размер буфера в байтах Cтрока с описанием объекта имеет вид: ``"номер_объекта - имя_объекта - имя_слоя - имя_листа_карты"``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapObjectComment_t (_hobj, _comment.buffer(), _size)

    mapObjectDirect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectDirect', maptype.HOBJ)
    def mapObjectDirect(_hobj: maptype.HOBJ) -> int:
        """
        Запросить текущее направление цифрования контура объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: Возвращает: OD_UNDEFINED (1) - не определено (незамкнутый контур или контур, вырожденный в точку или контур, имеющий ``"петли"``) 0D_RIGHT     (2) - объект справа (основной контур замкнутого объекта по часовой стрелке) 0D_LEFT      (4) - объект слева (основной контур замкнутого объекта против часовой стрелки) При ошибке возвращает ноль
        :rtype: int
        """
        return mapObjectDirect_t (_hobj)

    mapSubjectDirect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSubjectDirect', maptype.HOBJ, ctypes.c_long)
    def mapSubjectDirect(_hobj: maptype.HOBJ, _subject: int) -> int:
        """
        Запросить текущее направление цифрования контура подобъекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _subject: номер подобъекта (для объекта - равен нулю)
        
        :returns: Возвращает: OD_UNDEFINED (1) - не определено (незамкнутый контур или контур, вырожденный в точку или контур, имеющий ``"петли"``) 0D_RIGHT     (2) - объект справа (замкнутый контур объекта по часовой стрелке) 0D_LEFT      (4) - объект слева (замкнутый контур объекта против часовой стрелки) При ошибке возвращает ноль
        :rtype: int
        """
        return mapSubjectDirect_t (_hobj, _subject)

    mapSegmentNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSegmentNumber', maptype.HOBJ)
    def mapSegmentNumber(_hobj: maptype.HOBJ) -> int:
        """
        Запросить номер слоя объекта
        
        :param _hobj: идентификатор объекта карты в памяти Номера слоев начинаются с ноля
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSegmentNumber_t (_hobj)

    mapSegmentNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSegmentNameUn', maptype.HOBJ, maptype.PWCHAR, ctypes.c_long)
    def mapSegmentNameUn(_hobj: maptype.HOBJ, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить название слоя объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _name: адрес буфера для результата запроса
        
        :param _size: размер буфера в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSegmentNameUn_t (_hobj, _name.buffer(), _size)

    mapObjectClassNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectClassNumber', maptype.HOBJ)
    def mapObjectClassNumber(_hobj: maptype.HOBJ) -> int:
        """
        Запросить класс объекта в дереве слоев и классов
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: Если объект не включен в дерево слоев - возвращает ноль При ошибке возвращает ноль
        :rtype: int
        """
        return mapObjectClassNumber_t (_hobj)

    mapObjectClassName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectClassName', maptype.HOBJ, maptype.PWCHAR, ctypes.c_int)
    def mapObjectClassName(_hobj: maptype.HOBJ, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить название класса объекта (название подслоя в дереве слоев)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _name: адрес буфера для результата запроса
        
        :param _size: размер буфера в байтах
        
        :returns: Если объект не включен в дерево слоев - возвращает ноль При ошибке возвращает ноль
        :rtype: int
        """
        return mapObjectClassName_t (_hobj, _name.buffer(), _size)

    mapObjectCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectCode', maptype.HOBJ)
    def mapObjectCode(_hobj: maptype.HOBJ) -> int:
        """
        Запросить внутренний код объекта в классификаторе
        
        :param _hobj: идентификатор объекта карты в памяти При удалении объектов классификатора внутренние коды объектов могут изменяться. Внутренний код может использоваться для идентификации объекта классификатора только в течение одного сеанса работы с картой при неизменном классификаторе
        
        :returns: При ошибке возвращает ноль, ноль допустим для нового объекта и для графического объекта
        :rtype: int
        """
        return mapObjectCode_t (_hobj)

    mapObjectGUID_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectGUID', maptype.HOBJ, ctypes.c_char_p, ctypes.c_long)
    def mapObjectGUID(_hobj: maptype.HOBJ, _ident: ctypes.c_char_p, _size: int) -> int:
        """
        Запросить уникальный идентификатор объекта GUID
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _ident: поле для записи идентификатора (``32`` шестнадцатеричных символов от ``0`` до F)
        
        :param _size: размер поля в байтах Идентификатор ``GUID`` может автоматически присваиваться объектам карты, если установлен признак ведения ``GUID`` (например, mapSetAutoObjectGUID()) Идентификатор хранится в семантике объекта с кодом ``32799``
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapObjectGUID_t (_hobj, _ident, _size)

    mapCheckObjectGUID_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckObjectGUID', maptype.HOBJ, ctypes.c_long)
    def mapCheckObjectGUID(_hobj: maptype.HOBJ, _force: int) -> int:
        """
        Проверить наличие GUID и создать при необходимости
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _force: признак принудительного заполнения или замены ``GUID`` в семантике ``32799``
        
        :returns: Если изменений семантики нет - возвращает ноль
        :rtype: int
        
        .. note::

           Если значение семантики не соответствует формату ``GUID`` - выполняется принудительное обновление семантики
        """
        return mapCheckObjectGUID_t (_hobj, _force)

    mapClearBotTop_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapClearBotTop', maptype.HOBJ)
    def mapClearBotTop(_hobj: maptype.HOBJ) -> ctypes.c_void_p:
        """
        Установить значение границ видимости по классификатору объектов
        
        :param _hobj: идентификатор объекта карты в памяти
        """
        return mapClearBotTop_t (_hobj)

    mapSetObjectBotScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetObjectBotScale', maptype.HOBJ, ctypes.c_long)
    def mapSetObjectBotScale(_hobj: maptype.HOBJ, _scale: int) -> int:
        """
        Установить масштаб нижней границы видимости на карте
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _scale: знаменатель масштаба отображения от ``1:1`` до ``1:40 000 000``
        """
        return mapSetObjectBotScale_t (_hobj, _scale)

    mapObjectTopScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectTopScale', maptype.HOBJ)
    def mapObjectTopScale(_hobj: maptype.HOBJ) -> int:
        """
        Запросить масштаб нижней границы видимости на карте
        
        :param _hobj: идентификатор объекта карты в памяти
        """
        return mapObjectTopScale_t (_hobj)

    mapSetObjectTopScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetObjectTopScale', maptype.HOBJ, ctypes.c_long)
    def mapSetObjectTopScale(_hobj: maptype.HOBJ, _scale: int) -> int:
        """
        Установить масштаб верхней границы видимости на карте
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _scale: знаменатель масштаба отображения от ``1:1`` до ``1:40 000 000``
        """
        return mapSetObjectTopScale_t (_hobj, _scale)

    mapObjectBotScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectBotScale', maptype.HOBJ)
    def mapObjectBotScale(_hobj: maptype.HOBJ) -> int:
        """
        Запросить масштаб верхней границы видимости на карте
        
        :param _hobj: идентификатор объекта карты в памяти
        """
        return mapObjectBotScale_t (_hobj)

    mapObjectBotTopUniqueness_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectBotTopUniqueness', maptype.HOBJ)
    def mapObjectBotTopUniqueness(_hobj: maptype.HOBJ) -> int:
        """
        Запросить, являются ли границы видимости объекта уникальными
        
        :param _hobj: идентификатор объекта карты в памяти Уникальные границы устанавливаются при вызове mapSetObjectTopScale() и mapSetObjectBotScale()
        
        :returns: Если границы видимости беруться из классификатора - возвращает ноль
        :rtype: int
        """
        return mapObjectBotTopUniqueness_t (_hobj)

    mapRegisterObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRegisterObject', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapRegisterObject(_hobj: maptype.HOBJ, _excode: int, _local: int) -> int:
        """
        Зарегистрировать объекта в классификаторе по внешнему коду и локализации
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _excode: внешний код объекта,
        
        :param _local: локализация метрики объекта: ``LOCAL_LINE`` (линейны), ``LOCAL_SQUARE`` (площадной, или полигон), ``LOCAL_POINT`` (точечный) ... Обычно вызывается после mapCreateObject(...)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapRegisterObject_t (_hobj, _excode, _local)

    mapRegisterObjectByKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRegisterObjectByKey', maptype.HOBJ, ctypes.c_char_p)
    def mapRegisterObjectByKey(_hobj: maptype.HOBJ, _name: ctypes.c_char_p) -> int:
        """
        Сформировать описание нового объекта по короткому имени объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _name: символьный код объекта в классификаторе (до ``31`` символа) Обычно вызывается после mapCreateObject(...)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapRegisterObjectByKey_t (_hobj, _name)

    mapDescribeObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDescribeObject', maptype.HOBJ, ctypes.c_long)
    def mapDescribeObject(_hobj: maptype.HOBJ, _code: int) -> int:
        """
        Сформировать описание нового объекта по внутреннему коду объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _code: внутренний код объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDescribeObject_t (_hobj, _code)

    mapRegisterDrawObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRegisterDrawObject', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapRegisterDrawObject(_hobj: maptype.HOBJ, _layer: int, _local: int) -> int:
        """
        Сформировать описание нового графического объекта по номеру слоя и локализации
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _layer: порядковый номер слоя в классификаторе с ``0``
        
        :param _local: локализация метрики объекта: ``LOCAL_LINE``, ``LOCAL_SQUARE``, ``LOCAL_POINT``... Вызывается после mapCreateObject(...) Для формирования условного знака необходимо использовать функцию mapAppendDraw(...)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapRegisterDrawObject_t (_hobj, _layer, _local)

    mapSetObjectListNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetObjectListNumber', maptype.HOBJ, ctypes.c_long)
    def mapSetObjectListNumber(_hobj: maptype.HOBJ, _list: int) -> int:
        """
        Установить номер листа для нового объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _list: последовательный номер листа с ``1`` Обнуляет последовательный и уникальный номера объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetObjectListNumber_t (_hobj, _list)

    mapGetListNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetListNumber', maptype.HOBJ)
    def mapGetListNumber(_hobj: maptype.HOBJ) -> int:
        """
        Запросить номер листа для объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetListNumber_t (_hobj)

    mapGetObjectKind_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetObjectKind', maptype.HOBJ)
    def mapGetObjectKind(_hobj: maptype.HOBJ) -> int:
        """
        Запросить формат хранения метрики
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль, иначе - тип формата хранения метрики (IDLONG2, IDLONG3, IDDOUBLE2, IDDOUBLE3 ...)
        :rtype: int
        """
        return mapGetObjectKind_t (_hobj)

    mapSetObjectKind_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetObjectKind', maptype.HOBJ, ctypes.c_long)
    def mapSetObjectKind(_hobj: maptype.HOBJ, _kind: int) -> int:
        """
        Установить тип и размерность метрики объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _kind: тип метрики: ``IDLONG2``, ``IDLONG3``, ``IDDOUBLE2``, ``IDDOUBLE3``, ``IDDOUBLE4``, ``IDDOUBLE4F`` Преобразование метрики из типа ``IDDOUBLE4`` и ``IDDOUBLE4F`` не выполняется, если число точек больше нуля Для удаления ``4``-го измерения применяется функция mapDeletePointMeasurement4D Пересчет выполняется с сохранением существующих координат
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetObjectKind_t (_hobj, _kind)

    mapDeletePointMeasurement4D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeletePointMeasurement4D', maptype.HOBJ)
    def mapDeletePointMeasurement4D(_hobj: maptype.HOBJ) -> int:
        """
        Удалить из метрики измерение 4D
        
        Метрика приводится к типу IDDOUBLE3
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeletePointMeasurement4D_t (_hobj)

    mapGetObjectRecord_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetObjectRecord', maptype.HOBJ, ctypes.c_char_p, ctypes.c_long)
    def mapGetObjectRecord(_hobj: maptype.HOBJ, _buffer: ctypes.c_char_p, _size: int) -> int:
        """
        Запросить описание объекта в виде двоичной записи для передачи по сети
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _buffer: адрес памяти для размещения результата
        
        :param _size: размер выделенной памяти для контроля Может применяться для переноса объекта на другую карту той же проекции (ограничение данной версии)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Передача объекта может выполняться между различными потоками, процессами, компьютерами
           по соответствующим протоколам
        """
        return mapGetObjectRecord_t (_hobj, _buffer, _size)

    mapGetObjectRecordLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetObjectRecordLength', maptype.HOBJ)
    def mapGetObjectRecordLength(_hobj: maptype.HOBJ) -> int:
        """
        Запросить длину описания объекта в виде записи
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetObjectRecordLength_t (_hobj)

    mapPutObjectRecord_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapPutObjectRecord', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.c_long, ctypes.c_long)
    def mapPutObjectRecord(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _buffer: ctypes.c_char_p, _size: int, _mode: int) -> maptype.HOBJ:
        """
        Создать объект на указанной карте из записи объекта
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в документе, для фоновой карты равен hmap
        
        :param _buffer: адрес области памяти с записью объекта, созданной в mapGetObjectRecord
        
        :param _mode: режим создания: ``0`` - записать,как новый; ``1`` - заменить объект при совпадении Key(); ``4`` - создать в памяти,как новый, ``5`` - заменить объект при совпадении Key() в памяти; Для режимов ``4`` и ``5`` требуется последующий вызов mapCommitObject()
        
        :returns: При ошибке возвращает ноль, иначе - идентификатор созданного объекта
        :rtype: maptype.HOBJ
        
        .. note::

           После завершения использования объекта необходимо освободить ресурсы функцией mapFreeObject()
        """
        return mapPutObjectRecord_t (_hmap, _hsite, _buffer, _size, _mode)

    mapSaveObjectDump_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSaveObjectDump', maptype.HOBJ, maptype.PWCHAR)
    def mapSaveObjectDump(_hobj: maptype.HOBJ, _filename: mapsyst.WTEXT) -> int:
        """
        Сформировать дамп объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _filename: имя файла дампа или ноль (в этом случае имя будет - \\LOG\\имя_карты.номер_объекта.dump)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если имя не задано, то дамп обновляется не чаще 1 раз в 5 минут
        """
        return mapSaveObjectDump_t (_hobj, _filename.buffer())

    mapGetObjectNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetObjectNumber', maptype.HOBJ)
    def mapGetObjectNumber(_hobj: maptype.HOBJ) -> int:
        """
        Запросить порядковый номер объекта в карте
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: Если объект только создан и метод mapCommitObject() не вызывался - возвращает ноль При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetObjectNumber_t (_hobj)

    mapClearObjectNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapClearObjectNumber', maptype.HOBJ)
    def mapClearObjectNumber(_hobj: maptype.HOBJ) -> int:
        """
        Очистить порядковый номер объекта в карте
        
        :param _hobj: идентификатор объекта карты в памяти Очистка номера приводит к тому, что в mapCommitObject объект записывается как новый, но без изменения уникального номера объекта, который в этом случае должен устанавливаться через mapSetObjectKey При вызове mapCopyObjectAsNew уникальный номер объекта устанавливается автоматически как автоинкрементное поле от предыдущего максимального значения
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapClearObjectNumber_t (_hobj)

    mapSetObjectViewSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetObjectViewSemantic', maptype.HOBJ, ctypes.c_long)
    def mapSetObjectViewSemantic(_hobj: maptype.HOBJ, _isview: int) -> int:
        """
        Установить признак использования семантики при отображении графического объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _isview: признак использования семантики при отображении объекта При отображении объектов классификатора и присвоении служебных семантик, влияющих на вид объекта, использование семантики происходит автоматически
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetObjectViewSemantic_t (_hobj, _isview)

    mapObjectDescribe_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectDescribe', maptype.HOBJ, ctypes.POINTER(maptype.MAPOBJDESCEX))
    def mapObjectDescribe(_hobj: maptype.HOBJ, _desc: ctypes.POINTER(maptype.MAPOBJDESCEX)) -> int:
        """
        Запросить положение объекта в документе
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _desc: положение объекта в документе (номер листа, номер объекта, идентификатор карты)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapObjectDescribe_t (_hobj, _desc)

    mapReadObjectByDescribe_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapReadObjectByDescribe', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.MAPOBJDESCEX))
    def mapReadObjectByDescribe(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _desc: ctypes.POINTER(maptype.MAPOBJDESCEX)) -> int:
        """
        Прочитать объект по заданному положению в документе
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _desc: положение объекта в документе
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapReadObjectByDescribe_t (_hmap, _hobj, _desc)

    mapObjectRscKeyUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectRscKeyUn', maptype.HOBJ, maptype.PWCHAR, ctypes.c_long)
    def mapObjectRscKeyUn(_hobj: maptype.HOBJ, _key: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить уникальный идентификатор вида объекта в классификаторе
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _key: адрес буфера для записи результата
        
        :param _size: длина строки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapObjectRscKeyUn_t (_hobj, _key.buffer(), _size)

    mapSetObjectMetricDuplicationForObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetObjectMetricDuplicationForObject', maptype.HOBJ, maptype.HOBJ)
    def mapSetObjectMetricDuplicationForObject(_hobj: maptype.HOBJ, _hsource: maptype.HOBJ) -> int:
        """
        Установить признак общей метрики объекта из объекта источника
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _hsource: идентификатор объекта c исходной эталонной метрикой или ``0``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если после установки общей метрики будет отредактирована метрика
           клона, то изменится и метрика эталонного объекта
           При удалении эталонного объекта будет удаляться и клон
           При переносе объектов на другой лист (другую карту) признак клонирования сбрасывается
           и должен отслеживаться и устанавливаться программой, выполняющей перенос - mapSetObjectMetricDuplication()
           После установки общей метрики нужно сохранить (в mapCommitObject()) оба объекта - hobj и hsource
        """
        return mapSetObjectMetricDuplicationForObject_t (_hobj, _hsource)

    mapClearMetricDuplicationForClone_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapClearMetricDuplicationForClone', maptype.HOBJ)
    def mapClearMetricDuplicationForClone(_hobj: maptype.HOBJ) -> int:
        """
        Cбросить признак общей метрики в объекте - эталоне и перевести клон на свою метрику
        
        :param _hobj: идентификатор объекта карты в памяти - эталон метрики
        
        :returns: Если объект не ссылаются на общую метрику - возвращает -2 Если объект был клоном - возвращает -1 Если объект был эталоном для клонов - возвращает 1, клон пересохраняется со своей метрикой Если функция вернула ненулевое значение, то после завершения других операций редактирования нужно вызвать mapCommitObject При ошибке возвращает ноль
        :rtype: int
        """
        return mapClearMetricDuplicationForClone_t (_hobj)

    mapGetObjectMetricDuplication_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetObjectMetricDuplication', maptype.HOBJ, ctypes.POINTER(ctypes.c_long))
    def mapGetObjectMetricDuplication(_hobj: maptype.HOBJ, _ismainclone: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить идентификатор дубликата метрики, если метрика объекта дублируется в другом объекте
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _ismainclone: признак объекта - эталона метрики Применяется при восстановлении признака клонирования метрики в различных процедурах обработки объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetObjectMetricDuplication_t (_hobj, _ismainclone)

    mapGetObjectBigMetric_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetObjectBigMetric', maptype.HOBJ)
    def mapGetObjectBigMetric(_hobj: maptype.HOBJ) -> int:
        """
        Запросить признак размещения записи метрики по смещению более 4 Гб от начала файла
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetObjectBigMetric_t (_hobj)

    mapSetObjectScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetObjectScale', maptype.HOBJ, ctypes.c_long)
    def mapSetObjectScale(_hobj: maptype.HOBJ, _scale: int) -> int:
        """
        Установить признак увеличения графического объекта при приближении карты на экране
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _scale: признак увеличения объекта на масштабах, крупнее базового масштаба карты: ``0`` или ``1`` Применяется только для графических объектов, имеющих внутренний код равный нулю Для объектов из классификатора значение игнорируется
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetObjectScale_t (_hobj, _scale)

    mapGetObjectScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetObjectScale', maptype.HOBJ)
    def mapGetObjectScale(_hobj: maptype.HOBJ) -> int:
        """
        Запросить признак увеличения графического объекта при приближении карты на экране
        
        :param _hobj: идентификатор объекта карты в памяти
        """
        return mapGetObjectScale_t (_hobj)

    mapSetObjectPress_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetObjectPress', maptype.HOBJ, ctypes.c_long)
    def mapSetObjectPress(_hobj: maptype.HOBJ, _dontpress: int) -> int:
        """
        Установить графическому объекту признак "Не сжимать"
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _dontpress: значение признака: ``1`` - для установки признака ``"Не сжимать"``, ``0`` - для сброса признака Применяется только для графических объектов, имеющих внутренний код равный нулю Разрешает уменьшение объекта при сжатии карты мельче базового масштаба Для объектов из классификатора значение игнорируется
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetObjectPress_t (_hobj, _dontpress)

    mapGetObjectPress_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetObjectPress', maptype.HOBJ)
    def mapGetObjectPress(_hobj: maptype.HOBJ) -> int:
        """
        Запросить признак "Не сжимать"
        
        :param _hobj: идентификатор объекта карты в памяти Применяется только для графических объектов, имеющих внутренний код равный нулю Разрешает уменьшение объекта при сжатии карты мельче базового масштаба
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetObjectPress_t (_hobj)

    mapSetObjectSpline_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetObjectSpline', maptype.HOBJ, ctypes.c_long)
    def mapSetObjectSpline(_hobj: maptype.HOBJ, _type: int) -> int:
        """
        Установить способ отображения метрики объекта в виде динамического сплайна
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _type: тип сплайна: ``SPLINETYPE_SMOOTH`` - сглаживает углы, ``SPLINETYPE_POINTS`` - дуги по точкам
        
        :returns: При ошибке или отмене рисования сплайна возвращает ноль
        :rtype: int
        """
        return mapSetObjectSpline_t (_hobj, _type)

    mapGetObjectSpline_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetObjectSpline', maptype.HOBJ)
    def mapGetObjectSpline(_hobj: maptype.HOBJ) -> int:
        """
        Запросить способ отображения метрики объекта в виде динамического сплайна
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке или отмене рисования сплайна возвращает ноль
        :rtype: int
        """
        return mapGetObjectSpline_t (_hobj)

    mapSetObjectVerticalAlignment_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetObjectVerticalAlignment', maptype.HOBJ, ctypes.c_long)
    def mapSetObjectVerticalAlignment(_hobj: maptype.HOBJ, _flag: int) -> int:
        """
        Установить признак выравнивания подобъекта векторного знака или подписи по вертикали
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _flag: выравнивания первой точки подобъекта по первой точке объекта по вертикали: ``0`` или ``1`` При отображении первая точка метрики подобъекта выравнивается по вертикали по первой точке метрики объекта для векторных знаков и подписей
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetObjectVerticalAlignment_t (_hobj, _flag)

    mapGetObjectVerticalAlignment_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetObjectVerticalAlignment', maptype.HOBJ)
    def mapGetObjectVerticalAlignment(_hobj: maptype.HOBJ) -> int:
        """
        Запросить признак выравнивания подобъекта векторного знака или подписи по вертикали
        
        :param _hobj: идентификатор объекта карты в памяти При отображении первая точка метрики подобъекта выравнивается по вертикали по первой точке метрики объекта для векторных знаков и подписей
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetObjectVerticalAlignment_t (_hobj)

    mapGetObjectShowUp_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetObjectShowUp', maptype.HOBJ)
    def mapGetObjectShowUp(_hobj: maptype.HOBJ) -> int:
        """
        Запросить признак отображать объект Выше всех
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetObjectShowUp_t (_hobj)

    mapSetObjectShowUp_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetObjectShowUp', maptype.HOBJ, ctypes.c_long)
    def mapSetObjectShowUp(_hobj: maptype.HOBJ, _flag: int) -> int:
        """
        Установить новому объекту признак отображать объект Выше всех
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _flag: признак Выше всех: ``0`` или ``1`` Объекты любой локализации с признаком Выше всех всегда отображаются после всех других объектов одной с ними карты Для установки свойства существующему объекту необходимо вызвать функцию mapUpdateObjectUp()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetObjectShowUp_t (_hobj, _flag)

    mapGetObjectShowDown_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetObjectShowDown', maptype.HOBJ)
    def mapGetObjectShowDown(_hobj: maptype.HOBJ) -> int:
        """
        Запросить признак отображать объект Ниже всех
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetObjectShowDown_t (_hobj)

    mapSetObjectShowDown_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetObjectShowDown', maptype.HOBJ, ctypes.c_long)
    def mapSetObjectShowDown(_hobj: maptype.HOBJ, _flag: int) -> int:
        """
        Установить новому объекту признак отображать объект Ниже всех
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _flag: признак Ниже всех: ``0`` или ``1`` Объекты любой локализации с признаком Ниже всех всегда отображаются до всех других объектов одной с ними карты Для установки свойства существующему объекту необходимо вызвать функцию mapUpdateObjectDown()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetObjectShowDown_t (_hobj, _flag)

    mapSemanticAmount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticAmount', maptype.HOBJ)
    def mapSemanticAmount(_hobj: maptype.HOBJ) -> int:
        """
        Запросить число семантических характеристик (семантик) у объекта
        
        :param _hobj: идентификатор объекта карты в памяти Одна семантическая характеристика записывается в виде последовательности: числовой код семантики и значение семантики Разные экземпляры объектов одного вида могут иметь разное число семантик и любой порядок их записи По числовому коду из классификатора ``RSC`` можно запросить описание семантики, аналогичное описанию поля в таблице базы данных: ключ (имя поля), название, формат, точность, описание справочника и другие свойства
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSemanticAmount_t (_hobj)

    mapSemanticFullName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticFullName', maptype.HOBJ, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapSemanticFullName(_hobj: maptype.HOBJ, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить по номеру название семантической характеристики объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: последовательный номер семантики c ``1``
        
        :param _name: адрес буфера для записи названия семантики
        
        :param _size: размер буфера в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSemanticFullName_t (_hobj, _number, _name.buffer(), _size)

    mapSemanticNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticNumber', maptype.HOBJ, ctypes.c_long)
    def mapSemanticNumber(_hobj: maptype.HOBJ, _code: int) -> int:
        """
        Найти номер семантики для экземпляра объекта по ее коду
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _code: код семантики Разные экземпляры объектов одного вида могут иметь разное число семантик и любой порядок их записи
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSemanticNumber_t (_hobj, _code)

    mapSemanticCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticCode', maptype.HOBJ, ctypes.c_long)
    def mapSemanticCode(_hobj: maptype.HOBJ, _number: int) -> int:
        """
        Запросить код семантики по ее номеру для экземпляра объекта с проверкой сервисных семантик
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: последовательный номер семантики c ``1`` Разные экземпляры объектов одного вида могут иметь разное число семантик и любой порядок их записи Для сервисной семантики (код от ``TEMPSEMANTICFIRST`` до ``TEMPSEMANTICFIRST``), выполняется подбор кода по ключу из классификатора (классификатор могли дополнить после формирования карты) Сервисные семантики могут формироваться, например, при импорте данных из обменных форматов, когда по имени поля не найден подходящий код семантики в классификаторе ``RSC`` Сервисная семантика хранится в формате ``"имя_поля:значение"``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSemanticCode_t (_hobj, _number)

    mapRealSemanticCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRealSemanticCode', maptype.HOBJ, ctypes.c_long)
    def mapRealSemanticCode(_hobj: maptype.HOBJ, _number: int) -> int:
        """
        Запросить код семантики по ее номеру для экземпляра объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: последовательный номер семантики c ``1`` Разные экземпляры объектов одного вида могут иметь разное число семантик и любой порядок их записи
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapRealSemanticCode_t (_hobj, _number)

    mapIsSemanticUnicode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsSemanticUnicode', maptype.HOBJ, ctypes.c_long)
    def mapIsSemanticUnicode(_hobj: maptype.HOBJ, _number: int) -> int:
        """
        Запросить, является ли семантика строкой UTF16
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: последовательный номер характеристики c ``1``
        
        :returns: Если семантика в кодировке ``UTF16`` - возвращает ненулевое значение
        :rtype: int
        """
        return mapIsSemanticUnicode_t (_hobj, _number)

    mapSemanticValuePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticValuePro', maptype.HOBJ, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapSemanticValuePro(_hobj: maptype.HOBJ, _number: int, _place: mapsyst.WTEXT, _size: int, _separator: int) -> int:
        """
        Запросить по номеру значение семантики в виде строки
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: последовательный номер характеристики c ``1``
        
        :param _place: адрес буфера для записи семантики
        
        :param _size: длина буфера в байтах
        
        :param _separator: разделитель целой и дробной части для числового значения: ``0`` - десятичную точку не изменять ``1`` - заменить десятичную точку на символ, установленный в системе '.' или ',' - заменить десятичную точку на separator: '.' или ',' Значение преобразуется в символьный вид без раскодирования семантик типа справочник Значение семантики типа справочник будет прочитано в виде числового кода справочника
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSemanticValuePro_t (_hobj, _number, _place.buffer(), _size, _separator)

    mapSemanticValueNamePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticValueNamePro', maptype.HOBJ, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapSemanticValueNamePro(_hobj: maptype.HOBJ, _number: int, _place: mapsyst.WTEXT, _size: int, _separator: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить по номеру значение семантики в символьном раскодированном виде
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: последовательный номер характеристики c ``1``
        
        :param _place: адрес буфера для записи семантики
        
        :param _size: длина буфера в байтах
        
        :param _separator: разделитель целой и дробной части ``0`` - десятичную точку не изменять ``1`` - заменить десятичную точку на символ, установленный в системе '.' или ',' - заменить десятичную точку на separator: '.' или ','
        
        :param _error: поле для записи ошибки после анализа значения или ``0`` Коды ошибок: ``IDS_STRUCT`` - значение поля не соответствует формату (нечисловые символы вместо числа и т.п.), ``IDS_VALUEOUTSIDE`` - нарушение ожидаемого диапазона значений Например: для семантики типа справочник ``"СОСТОЯНИЕ"`` значение ``"5"`` заменется на ``"жилой"``
        
        :returns: При ошибке возвращает ноль, иначе - код семантики
        :rtype: int
        """
        return mapSemanticValueNamePro_t (_hobj, _number, _place.buffer(), _size, _separator, _error)

    mapSemanticDoubleValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSemanticDoubleValue', maptype.HOBJ, ctypes.c_long)
    def mapSemanticDoubleValue(_hobj: maptype.HOBJ, _number: int) -> float:
        """
        Запросить по номеру значение семантики в виде числа с плавающей точкой
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: последовательный номер характеристики c ``1``
        
        :returns: или не найдено - возвращает ноль
        :rtype: float
        
        .. note::

           Если значение семантики не может быть преобразовано к числовому виду
        """
        return mapSemanticDoubleValue_t (_hobj, _number)

    mapSemanticLongIntValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticLongIntValue', maptype.HOBJ, ctypes.c_long)
    def mapSemanticLongIntValue(_hobj: maptype.HOBJ, _number: int) -> int:
        """
        Запросить значение семантической характеристики объекта в виде целого числа
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: последовательный номер характеристики
        
        :returns: к числовому виду или - возвращает ноль
        :rtype: int
        
        .. note::

           Если значение семантики не может быть преобразовано
        """
        return mapSemanticLongIntValue_t (_hobj, _number)

    mapSemanticValueNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticValueNameUn', maptype.HOBJ, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapSemanticValueNameUn(_hobj: maptype.HOBJ, _number: int, _place: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить по номеру значение семантики в символьном раскодированном виде
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: последовательный номер характеристики c ``1``
        
        :param _place: адрес буфера для записи значения семантики
        
        :param _size: длина буфера в байтах Например: для семантики типа справочник ``"СОСТОЯНИЕ"`` значение ``"5"`` заменется на ``"жилой"``
        
        :returns: При ошибке возвращает ноль, иначе - код семантики
        :rtype: int
        """
        return mapSemanticValueNameUn_t (_hobj, _number, _place.buffer(), _size)

    mapSemanticValueFullNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticValueFullNameUn', maptype.HOBJ, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapSemanticValueFullNameUn(_hobj: maptype.HOBJ, _number: int, _place: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить по номеру значение семантики в раскодированном виде с единицей измерения
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: последовательный номер характеристики c ``1``
        
        :param _place: адрес буфера для записи значения семантики
        
        :param _size: длина буфера в байтах Например: для семантики типа справочник ``"СОСТОЯНИЕ"`` значение ``"5"`` заменется на ``"жилой"`` Для числовой семантики ``"ВЫСОТА"`` значение ``"205,5"`` заменется на ``"205,5 м"``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSemanticValueFullNameUn_t (_hobj, _number, _place.buffer(), _size)

    mapSemanticCodeValueUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticCodeValueUn', maptype.HOBJ, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapSemanticCodeValueUn(_hobj: maptype.HOBJ, _code: int, _place: mapsyst.WTEXT, _size: int, _number: int) -> int:
        """
        Запросить по коду семантики значение в виде строки
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _code: код семантики, для которой ищется значение
        
        :param _place: адрес буфера для записи значения семантики или ``0``
        
        :param _size: длина буфера в байтах или ``0``
        
        :param _number: последовательный номер с ``1`` запрашиваемого значения среди семантик с тем же кодом, не равен последовательному номеру характеристики Значение семантики преобразуется в символьный вид без раскодирования справочников Например: код ``"code"`` имеют ``3``-я и ``6``-я характеристики, соответственно для number ``= 1`` вернется значение семантики ``3``, для number ``= 2`` - семаники ``6``, для number ``= 3`` вернется ноль Семантика с одним кодом может иметь несколько значений, если в классификаторе ``RSC`` для нее установлено свойство Разрешается повторение Чтобы найти семантику с нужным кодом без запроса значения - необходимо передать параметры place и size равными нулю
        
        :returns: При ошибке возвращает ноль, иначе - последовательный номер найденной характеристики
        :rtype: int
        """
        return mapSemanticCodeValueUn_t (_hobj, _code, _place.buffer(), _size, _number)

    mapSemanticCodeValuePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticCodeValuePro', maptype.HOBJ, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSemanticCodeValuePro(_hobj: maptype.HOBJ, _code: int, _place: mapsyst.WTEXT, _size: int, _number: int, _separator: int) -> int:
        """
        Запросить по коду семантики значение в виде строки с разделителем для числа
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _code: код семантики, для которой ищется значение
        
        :param _place: адрес буфера для записи значения семантики или ``0``
        
        :param _size: длина буфера в байтах или ``0``
        
        :param _number: последовательный номер с ``1`` запрашиваемого значения среди семантик с тем же кодом, не равен последовательному номеру характеристики
        
        :param _separator: разделитель целой и дробной части ``0`` - десятичную точку не изменять ``1`` - заменить десятичную точку на символ, установленный в системе '.' или ',' - заменить десятичную точку на separator: '.' или ',' Например: код ``"code"`` имеют ``3``-я и ``6``-я характеристики, соответственно для number ``= 1`` вернется значение семантики ``3``, для number ``= 2`` - семаники ``6``, для number ``= 3`` вернется ноль Семантика с одним кодом может иметь несколько значений, если в классификаторе ``RSC`` для нее установлено свойство Разрешается повторение Чтобы найти семантику с нужным кодом без запроса значения - необходимо передать параметры place и size равными нулю Разные экземпляры объектов одного вида могут иметь разное число семантик и любой порядок их записи
        
        :returns: При ошибке возвращает ноль, иначе - последовательный номер найденной характеристики
        :rtype: int
        """
        if _place is None:
            return mapSemanticCodeValuePro_t (_hobj, _code, 0, 0, _number, 0) # Поиск номера семантики с заданным кодом
        else:
            return mapSemanticCodeValuePro_t (_hobj, _code, _place.buffer(), _size, _number, _separator)

    mapSemanticCodeValueNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticCodeValueNameUn', maptype.HOBJ, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapSemanticCodeValueNameUn(_hobj: maptype.HOBJ, _code: int, _place: mapsyst.WTEXT, _size: int, _number: int) -> int:
        """
        Запросить по коду значение семантики в символьном раскодированном виде
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _code: код семантики, для которой ищется значение
        
        :param _place: адрес буфера для записи значения семантики
        
        :param _size: длина буфера в байтах
        
        :param _number: последовательный номер с ``1`` запрашиваемого значения среди семантик с тем же кодом, не равен последовательному номеру характеристики Например: для семантики типа справочник ``"СОСТОЯНИЕ"`` значение ``"5"`` заменется на ``"жилой"`` Разные экземпляры объектов одного вида могут иметь разное число семантик и любой порядок их записи
        
        :returns: При ошибке возвращает ноль, иначе - последовательный номер найденной характеристики
        :rtype: int
        """
        return mapSemanticCodeValueNameUn_t (_hobj, _code, _place.buffer(), _size, _number)

    mapSemanticCodeLabel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticCodeLabel', maptype.HOBJ, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSemanticCodeLabel(_hobj: maptype.HOBJ, _code: int, _place: mapsyst.WTEXT, _size: int, _number: int, _issystemdot: int) -> int:
        """
        Сформировать по коду значение семантики для подписывания
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _code: код семантики, для которой ищется значение
        
        :param _place: адрес буфера для записи обработанного значения семантики или ``0``
        
        :param _size: длина буфера в байтах или ``0``
        
        :param _number: последовательный номер с ``1`` запрашиваемого значения среди семантик с тем же кодом, не равен последовательному номеру характеристики separator - разделитель целой и дробной части ``0`` - десятичную точку не изменять ``1`` - заменить десятичную точку на символ, установленный в системе '.' или ',' - заменить десятичную точку на separator: '.' или ',' Заполняет строку для подписи (place) в формате: ``"[префикс] <значение> [постфикс]"``
        
        :returns: При ошибке возвращает ноль, иначе - последовательный номер найденной характеристики
        :rtype: int
        
        .. note::

           Если значение пусто, то префикс и постфикс не добавляются
           Например: - для названия озера может быть задан префикс ``"оз."``:    ``"оз. Южное"``
           - для площади участка может быть задан постфикс ``"(га)"``: "``1.2`` (га)"
           Настройки текста подписи хранятся в классификаторе RSC
        """
        return mapSemanticCodeLabel_t (_hobj, _code, _place.buffer(), _size, _number, _issystemdot)

    mapSemanticCodeDoubleValueEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticCodeDoubleValueEx', maptype.HOBJ, ctypes.c_long, ctypes.POINTER(ctypes.c_double), ctypes.c_long)
    def mapSemanticCodeDoubleValueEx(_hobj: maptype.HOBJ, _code: int, _value: ctypes.POINTER(ctypes.c_double), _number: int) -> int:
        """
        Запросить по коду семантики значение в виде числа с плавающей точкой
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _code: код семантики, для которой ищется значение
        
        :param _value: поле для размещения результата запроса
        
        :param _number: последовательный номер с ``1`` запрашиваемого значения среди семантик с тем же кодом, не равен последовательному номеру характеристики
        
        :returns: или не найдено - возвращает ноль
        :rtype: int
        
        .. note::

           Если значение семантики не может быть преобразовано к числовому виду
        """
        return mapSemanticCodeDoubleValueEx_t (_hobj, _code, _value, _number)

    mapSemanticCodeDoubleValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSemanticCodeDoubleValue', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSemanticCodeDoubleValue(_hobj: maptype.HOBJ, _code: int, _number: int) -> float:
        """
        Запросить по коду семантики значение в виде числа с плавающей точкой
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _code: код семантики, для которой ищется значение
        
        :param _number: последовательный номер с ``1`` запрашиваемого значения среди семантик с тем же кодом, не равен последовательному номеру характеристики
        
        :returns: или не найдено - возвращает ноль
        :rtype: float
        
        .. note::

           Если значение семантики не может быть преобразовано к числовому виду
        """
        return mapSemanticCodeDoubleValue_t (_hobj, _code, _number)

    mapSemanticCodeLongValueEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticCodeLongValueEx', maptype.HOBJ, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.c_long)
    def mapSemanticCodeLongValueEx(_hobj: maptype.HOBJ, _code: int, _value: ctypes.POINTER(ctypes.c_long), _number: int) -> int:
        """
        Запросить по коду семантики значение в виде целого числа
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _code: код семантики, для которой ищется значение
        
        :param _value: поле для размещения результата запроса
        
        :param _number: последовательный номер с ``1`` запрашиваемого значения среди семантик с тем же кодом, не равен последовательному номеру характеристики
        
        :returns: или не найдено - возвращает ноль
        :rtype: int
        
        .. note::

           Если значение семантики не может быть преобразовано к числовому виду
        """
        return mapSemanticCodeLongValueEx_t (_hobj, _code, _value, _number)

    mapSemanticCodeLongValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticCodeLongValue', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSemanticCodeLongValue(_hobj: maptype.HOBJ, _code: int, _number: int) -> int:
        """
        Запросить по коду семантики значение в виде целого числа
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _code: код семантики, для которой ищется значение
        
        :param _number: последовательный номер с ``1`` запрашиваемого значения среди семантик с тем же кодом, не равен последовательному номеру характеристики
        
        :returns: или не найдено - возвращает ноль
        :rtype: int
        
        .. note::

           Если значение семантики не может быть преобразовано к числовому виду
        """
        return mapSemanticCodeLongValue_t (_hobj, _code, _number)

    mapSemanticCodeKeyValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticCodeKeyValue', maptype.HOBJ, ctypes.c_long, ctypes.c_char_p, ctypes.c_long, ctypes.c_long)
    def mapSemanticCodeKeyValue(_hobj: maptype.HOBJ, _code: int, _place: ctypes.c_char_p, _size: int, _number: int) -> int:
        """
        Запросить по коду значение семантики типа справочник в виде ключа значения
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _code: код семантики, для которой ищется значение
        
        :param _place: адрес буфера для записи значения семантики
        
        :param _size: длина буфера в байтах Семантика типа справочник для каждого значения имеет числовой код, ключ, короткое обозначение и название
        
        :param _number: последовательный номер с ``1`` запрашиваемого значения среди семантик с тем же кодом, не равен последовательному номеру характеристики Ключ и короткое обозначение имеют одинаковое назначение и позволяют использовать фактически ``2`` разных ключа
        
        :returns: При ошибке возвращает ноль, иначе - последовательный номер найденной характеристики
        :rtype: int
        """
        return mapSemanticCodeKeyValue_t (_hobj, _code, _place, _size, _number)

    mapSemanticCodeShortName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticCodeShortName', maptype.HOBJ, ctypes.c_long, ctypes.c_char_p, ctypes.c_long, ctypes.c_long)
    def mapSemanticCodeShortName(_hobj: maptype.HOBJ, _code: int, _place: ctypes.c_char_p, _size: int, _number: int) -> int:
        """
        Запросить по коду значение семантики типа справочник в виде короткого обозначения
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _code: код семантики, для которой ищется значение
        
        :param _place: адрес буфера для записи значения семантики
        
        :param _size: длина буфера в байтах (значение может быть до ``64`` символов ``ANSI`` c замыкающим нулем) Семантика типа справочник для каждого значения имеет числовой код, ключ, короткое обозначение и название
        
        :param _number: последовательный номер с ``1`` запрашиваемого значения среди семантик с тем же кодом, не равен последовательному номеру характеристики Ключ и короткое обозначение имеют одинаковое назначение и позволяют использовать фактически ``2`` разных ключа
        
        :returns: При ошибке возвращает ноль, иначе - последовательный номер найденной характеристики
        :rtype: int
        """
        return mapSemanticCodeShortName_t (_hobj, _code, _place, _size, _number)

    mapSemanticClassificatorCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticClassificatorCount', maptype.HOBJ, ctypes.c_long)
    def mapSemanticClassificatorCount(_hobj: maptype.HOBJ, _code: int) -> int:
        """
        Запросить из RSC количество записей в семантике типа справочник по коду семантики
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _code: код семантики типа справочник (``TCODE``) Описание семантики типа справочник запрашивается из классификатора формата ``RSC``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSemanticClassificatorCount_t (_hobj, _code)

    mapSemanticClassificatorNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticClassificatorNameUn', maptype.HOBJ, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapSemanticClassificatorNameUn(_hobj: maptype.HOBJ, _code: int, _number: int, _place: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить название значения семантики типа справочник
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _code: код семантики типа справочник (``TCODE``)
        
        :param _number: последовательный номер в справочнике с ``1``
        
        :param _place: адрес буфера для записи названия
        
        :param _size: длина буфера в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSemanticClassificatorNameUn_t (_hobj, _code, _number, _place.buffer(), _size)

    mapSemanticClassificatorCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticClassificatorCode', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSemanticClassificatorCode(_hobj: maptype.HOBJ, _code: int, _number: int) -> int:
        """
        Запросить код значения семантики типа справочник
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _code: код семантики типа справочник (``TCODE``)
        
        :param _number: последовательный номер значения в справочнике с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSemanticClassificatorCode_t (_hobj, _code, _number)

    mapFindTextGroup_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapFindTextGroup', maptype.HOBJ, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapFindTextGroup(_hobj: maptype.HOBJ, _code: ctypes.POINTER(ctypes.c_long), _number: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Найти номер объекта в семантике для кодов SEMOBJECTTOTEXT, SEMOBJECTFROMTEXT
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _code: поле для записи кода найденной семантики: ``SEMOBJECTTOTEXT`` или ``SEMOBJECTFROMTEXT``
        
        :param _number: поле для записи номера найденной семантики
        
        :returns: Возвращает значение найденной семантики - номер объекта или подписи При создании на карте подписи некоторой характеристики исходный объект и его подписи связываются через служебные семантики SEMOBJECTTOTEXT, SEMOBJECTFROMTEXT Значением этих семантик являютсяуникальные номера подписи и объекта соответственно Служебные семантики позволяют автоматически обновить текст пописи при обновлении семантики объекта При ошибке возвращает ноль
        :rtype: int
        """
        return mapFindTextGroup_t (_hobj, _code, _number)

    mapAvailableSemanticCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAvailableSemanticCount', maptype.HOBJ)
    def mapAvailableSemanticCount(_hobj: maptype.HOBJ) -> int:
        """
        Запросить количество видов семантик, которые еще могут быть добавлены для данного объекта
        
        :param _hobj: идентификатор объекта карты в памяти Объекту могут быть добавлены те семантики, которые ему назначены в классификаторе ``RSC``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если для семантики не установлено свойство Разрешается повторение, то она может быть
           у объекта только в одном экземпляре
           Результат запроса изменяется в процессе добавления семантик объекту
        """
        return mapAvailableSemanticCount_t (_hobj)

    mapAvailableSemanticList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAvailableSemanticList', maptype.HOBJ, ctypes.POINTER(ctypes.c_long), ctypes.c_long)
    def mapAvailableSemanticList(_hobj: maptype.HOBJ, _list: ctypes.POINTER(ctypes.c_long), _count: int) -> int:
        """
        Запросить список кодов семантик, которые могут быть добавлены объекту
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _list: указатель на область памяти для списка кодов семантик или ``0``
        
        :param _count: максимальное число элементов в списке (размер буфера деленный на размер long int)
        
        :returns: Возвращает число кодов доступных семантик на объект, которые могут быть записаны Если параметр list равен нулю, то функция только считает число доступных семантик При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если count меньше требуемого числа семантик, то заполняться первые count семантик
        """
        return mapAvailableSemanticList_t (_hobj, _list, _count)

    mapAvailableMustSemanticList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAvailableMustSemanticList', maptype.HOBJ, ctypes.POINTER(ctypes.c_long), ctypes.c_long)
    def mapAvailableMustSemanticList(_hobj: maptype.HOBJ, _list: ctypes.POINTER(ctypes.c_long), _count: int) -> int:
        """
        Запросить список кодов доступных обязательных семантик на объект
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _list: указатель на область памяти для размещения списка кодов семантик
        
        :param _count: максимальное число элементов в списке (размер буфера деленный на sizeof(long int)) Семантики, которые назначены объекту в классификаторе ``RSC``, могут быть обязательными и дополнительными. Все обязательные семантики необходимо заполнить при создании объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapAvailableMustSemanticList_t (_hobj, _list, _count)

    mapAppendSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendSemantic', maptype.HOBJ, ctypes.c_long, ctypes.c_char_p, ctypes.c_long)
    def mapAppendSemantic(_hobj: maptype.HOBJ, _code: int, _value: ctypes.c_char_p, _size: int) -> int:
        """
        Добавить семантику объекту
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _code: код семантической характеристики
        
        :param _value: адрес строки, содержащей значение семантики в символьном виде
        
        :param _size: длина добавляемой строки в байтах (если необходимо взять часть строки) или ноль Для семантики числового типа значения будут преобразовываться в двоичный вид Для семантики типа справочник, если значение не числовое, выполняется поиск кода по ключу и названию
        
        :returns: При успешном выполнении возвращает последовательный номер созданной характеристики При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если такая семантика была и она не повторяемая - значение заменяется
        """
        return mapAppendSemantic_t (_hobj, _code, _value, _size)

    mapAppendSemanticUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendSemanticUn', maptype.HOBJ, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapAppendSemanticUn(_hobj: maptype.HOBJ, _code: int, _value: mapsyst.WTEXT, _size: int) -> int:
        """
        Добавить семантику объекту в кодировке UTF-16
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _code: код семантической характеристики
        
        :param _value: значение характеристики в кодировке UTF-16
        
        :param _size: длина добавляемой строки в байтах, если нужно добавить подстроку, или ``0`` Для семантики числового типа значения будут преобразовываться в двоичный вид Для семантики типа справочник, если значение не числовое, выполняется поиск кода по ключу и названию
        
        :returns: При успешном выполнении возвращает последовательный номер созданной характеристики При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если такая семантика была и она не повторяемая - значение заменяется
        """
        return mapAppendSemanticUn_t (_hobj, _code, _value.buffer(), _size)

    mapAppendServiceSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendServiceSemantic', maptype.HOBJ, maptype.PWCHAR, maptype.PWCHAR)
    def mapAppendServiceSemantic(_hobj: maptype.HOBJ, _name: mapsyst.WTEXT, _value: mapsyst.WTEXT) -> int:
        """
        Добавить произвольную характеристику в семантику объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _name: условное имя характеристики в кодировке UTF-16
        
        :param _value: значение характеристики в кодировке UTF-16 Применяется для записи произвольного атрибута в формате ``"имя_поля:значение"`` (``"name:value"``) в кодировке UTF-16 с кодом ``32862`` (``SEMSERVICECODE``) или временным сервисным кодом в диапазоне от ``TEMPSEMANTICFIRST`` до ``TEMPSEMANTICFIRST``
        
        :returns: При успешном выполнении возвращает последовательный номер созданной характеристики При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendServiceSemantic_t (_hobj, _name.buffer(), _value.buffer())

    mapAppendSemanticDouble_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendSemanticDouble', maptype.HOBJ, ctypes.c_long, ctypes.c_double)
    def mapAppendSemanticDouble(_hobj: maptype.HOBJ, _code: int, _value: float) -> int:
        """
        Добавить семантику типа число
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _code: код семантической характеристики
        
        :param _value: значение в виде числа двойной точности
        
        :returns: При успешном выполнении возвращает последовательный номер созданной характеристики При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendSemanticDouble_t (_hobj, _code, _value)

    mapAppendSemanticLong_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendSemanticLong', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapAppendSemanticLong(_hobj: maptype.HOBJ, _code: int, _value: int) -> int:
        """
        Добавить семантику типа целое число
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _code: код семантической характеристики
        
        :param _value: значение в виде целого числа
        
        :returns: При успешном выполнении возвращает последовательный номер созданной характеристики При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendSemanticLong_t (_hobj, _code, _value)

    mapDeleteSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteSemantic', maptype.HOBJ, ctypes.c_long)
    def mapDeleteSemantic(_hobj: maptype.HOBJ, _number: int) -> int:
        """
        Удалить по номеру семантику объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: последовательный номер характеристики с ``1``, если номер равен ``"-1"``, удаляются все характеристики
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteSemantic_t (_hobj, _number)

    mapSetSemanticCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSemanticCode', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSetSemanticCode(_hobj: maptype.HOBJ, _number: int, _code: int) -> int:
        """
        Изменить по номеру код семантики объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: последовательный номер характеристики с ``1``
        
        :param _code: новый код семантики
        
        :returns: При ошибке возвращает ноль, иначе - код семантики
        :rtype: int
        """
        return mapSetSemanticCode_t (_hobj, _number, _code)

    mapSetSemanticDoubleValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSemanticDoubleValue', maptype.HOBJ, ctypes.c_long, ctypes.c_double)
    def mapSetSemanticDoubleValue(_hobj: maptype.HOBJ, _number: int, _value: float) -> int:
        """
        Изменить значение семантики типа число
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: последовательный номер характеристики с ``1``
        
        :param _value: новое значение семантики
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetSemanticDoubleValue_t (_hobj, _number, _value)

    mapSetSemanticLongValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSemanticLongValue', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSetSemanticLongValue(_hobj: maptype.HOBJ, _number: int, _value: int) -> int:
        """
        Изменить значение семантики типа целое число
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: последовательный номер характеристики с ``1``
        
        :param _value: новое значение семантики
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetSemanticLongValue_t (_hobj, _number, _value)

    mapSetSemanticValueUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSemanticValueUn', maptype.HOBJ, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapSetSemanticValueUn(_hobj: maptype.HOBJ, _number: int, _place: mapsyst.WTEXT, _maxsize: int) -> int:
        """
        Изменить значение семантики объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: последовательный номер характеристики c ``1``
        
        :param _place: адрес строки, содержащей новое значение в виде строки ``UTF16`` size - длина добавляемой строки в байтах, если нужно добавить подстроку, или ноль - размер будет определен автоматически до замыкающего нуля Семантика числового типа будет автоматически преобразовываться в двоичный вид Для семантики типа справочник, если значение не числовое, выполняется поиск кода по ключу и названию
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetSemanticValueUn_t (_hobj, _number, _place.buffer(), _maxsize)

    mapRedefineObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRedefineObject', maptype.HOBJ)
    def mapRedefineObject(_hobj: maptype.HOBJ) -> int:
        """
        Обновить условный знак объекта при изменении семантических характеристик
        
        :param _hobj: идентификатор объекта карты в памяти Данная функция выполняется автоматически при сохранении объекта функцией mapCommitObject()
        
        :returns: Если вид объекта не изменился возвращает ноль
        :rtype: int
        
        .. note::

           Если для кода объекта назначена серия объектов по семантике, то будет выполнен подбор
           подходящего условного знака
        """
        return mapRedefineObject_t (_hobj)

    mapUpdateSemanticByFormula_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateSemanticByFormula', maptype.HOBJ, ctypes.c_long)
    def mapUpdateSemanticByFormula(_hobj: maptype.HOBJ, _int: int) -> int:
        """
        Обновить значения семантик типа формула при обновлении семантики или метрики объекта
        
        :param _hobj: идентификатор объекта карты в памяти Применяется для обновления значений семантик типа формула, зависящих от других семантик и координат объекта Данная функция автоматически вызывается при сохранении объекта функцией mapCommitObject()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdateSemanticByFormula_t (_hobj, _int)

    mapCreateSemanticRecord_t = mapsyst.GetProcAddress(acceslib,maptype.HSEMRECORD,'mapCreateSemanticRecord', maptype.HOBJ)
    def mapCreateSemanticRecord(_hobj: maptype.HOBJ) -> maptype.HSEMRECORD:
        """
        Создать запись набора семантик объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: Возвращает идентификатор групповой семантики в памяти
        :rtype: maptype.HSEMRECORD
        
        .. note::

           После завершения работы с записью набора семантик необходимо освободить ресурсы функцией mapFreeSemanticRecord
        """
        return mapCreateSemanticRecord_t (_hobj)

    mapFreeSemanticRecord_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeSemanticRecord', maptype.HSEMRECORD)
    def mapFreeSemanticRecord(_hsemrecord: maptype.HSEMRECORD) -> ctypes.c_void_p:
        """
        Освободить ресурсы записи набора семантик объекта
        
        :param _hsemrecord: идентификатор записи набора семантик объекта
        """
        return mapFreeSemanticRecord_t (_hsemrecord)

    mapClearSemanticRecord_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapClearSemanticRecord', maptype.HSEMRECORD)
    def mapClearSemanticRecord(_hsemrecord: maptype.HSEMRECORD) -> ctypes.c_void_p:
        """
        Очистить содержимое записи групповой семантики для записи новых значений
        
        :param _hsemrecord: идентификатор записи набора семантик объекта
        """
        return mapClearSemanticRecord_t (_hsemrecord)

    mapGetSemanticRecordCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSemanticRecordCount', maptype.HSEMRECORD)
    def mapGetSemanticRecordCount(_hsemrecord: maptype.HSEMRECORD) -> int:
        """
        Запросить число семантик в записи групповой семантики
        
        :param _hsemrecord: идентификатор записи набора семантик объекта
        """
        return mapGetSemanticRecordCount_t (_hsemrecord)

    mapAppendSemanticToSemanticRecord_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendSemanticToSemanticRecord', maptype.HSEMRECORD, ctypes.c_long, ctypes.c_char_p, ctypes.c_long)
    def mapAppendSemanticToSemanticRecord(_hsemrecord: maptype.HSEMRECORD, _code: int, _value: ctypes.c_char_p, _size: int) -> int:
        """
        Добавить семантику в запись набора семантик объекта со значением в виде строки ANSI
        
        :param _hsemrecord: идентификатор записи набора семантик объекта
        
        :param _code: код характеристики
        
        :param _value: адрес строки, содержащей значение характеристики в кодировке ``ANSI``
        
        :param _size: длина добавляемого значения (подстроки) в байтах или ``0``
        
        :returns: При успешном выполнении возвращает последовательный номер записанной характеристики Если параметр value указывает на пустую строку и тип семантики не является формулой, то семантика не будет добавлена При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если записывается значение семантиики типа ``"справочник"``, то строка может содержать код,
           ключ или строку со значением из справочника. По ключу и значению будет найден код и записан
           Если код из справочника не будет найден, то запишется строка с переданным значением
        """
        return mapAppendSemanticToSemanticRecord_t (_hsemrecord, _code, _value, _size)

    mapAppendSemanticUnToSemanticRecord_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendSemanticUnToSemanticRecord', maptype.HSEMRECORD, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapAppendSemanticUnToSemanticRecord(_hsemrecord: maptype.HSEMRECORD, _code: int, _value: mapsyst.WTEXT, _size: int) -> int:
        """
        Добавить семантику в запись набора семантик объекта со значением в виде строки UTF16
        
        :param _hsemrecord: идентификатор записи набора семантик объекта
        
        :param _code: код характеристики
        
        :param _value: адрес строки, содержащей значение характеристики в кодировке ``UTF16``
        
        :param _size: длина добавляемого значения (подстроки) в байтах или ``0``
        
        :returns: При успешном выполнении возвращает последовательный номер записанной характеристики При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если записывается значение семантиики типа ``"справочник"``, то строка может содержать код,
           ключ или строку со значением из справочника. По ключу и значению будет найден код и записан.
           Если код из справочника не будет найден, то запишется строка с переданным значением
        """
        return mapAppendSemanticUnToSemanticRecord_t (_hsemrecord, _code, _value.buffer(), _size)

    mapAppendSemanticDoubleToSemanticRecord_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendSemanticDoubleToSemanticRecord', maptype.HSEMRECORD, ctypes.c_long, ctypes.c_double)
    def mapAppendSemanticDoubleToSemanticRecord(_hsemrecord: maptype.HSEMRECORD, _code: int, _value: float) -> int:
        """
        Добавить семантику в запись набора семантик объекта со значением в виде числа двойной точности
        
        :param _hsemrecord: идентификатор записи набора семантик объекта
        
        :param _code: код характеристики
        
        :param _value: значение в виде числа двойной точности
        
        :returns: При успешном выполнении возвращает последовательный номер записанной характеристики При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendSemanticDoubleToSemanticRecord_t (_hsemrecord, _code, _value)

    mapAppendSemanticLongToSemanticRecord_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendSemanticLongToSemanticRecord', maptype.HSEMRECORD, ctypes.c_long, ctypes.c_long)
    def mapAppendSemanticLongToSemanticRecord(_hsemrecord: maptype.HSEMRECORD, _code: int, _value: int) -> int:
        """
        Добавить семантику в запись набора семантик объекта со значением в виде целого числа
        
        :param _hsemrecord: идентификатор записи набора семантик объекта
        
        :param _code: код характеристики
        
        :param _value: значение в виде целого числа
        
        :returns: При успешном выполнении возвращает последовательный номер записанной характеристики При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendSemanticLongToSemanticRecord_t (_hsemrecord, _code, _value)

    mapAppendGroupSemanticToSemanticRecord_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendGroupSemanticToSemanticRecord', maptype.HSEMRECORD, ctypes.c_long, maptype.HSEMRECORD)
    def mapAppendGroupSemanticToSemanticRecord(_hsemrecord: maptype.HSEMRECORD, _code: int, _hsubrecord: maptype.HSEMRECORD) -> int:
        """
        Добавить семантику в запись набора семантик со значением в виде набора семантик
        
        :param _hsemrecord: идентификатор записи набора семантик объекта
        
        :param _code: код характеристики
        
        :param _hsubrecord: идентификатор записи набора семантик объекта, которая (запись) запишется как значение семантики с кодом code
        
        :returns: При успешном выполнении возвращает последовательный номер записанной характеристики В список семантик добавляется семантика содержащая другой список - формируется дерево наборов семантик При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendGroupSemanticToSemanticRecord_t (_hsemrecord, _code, _hsubrecord)

    mapAppendGroupSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendGroupSemantic', maptype.HOBJ, ctypes.c_long, maptype.HSEMRECORD)
    def mapAppendGroupSemantic(_hobj: maptype.HOBJ, _code: int, _hsemrecord: maptype.HSEMRECORD) -> int:
        """
        Добавить семантику объекту со значением в виде набора семантик
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _code: код семантической характеристики hsubrecord - идентификатор записи набора семантик объекта, которая (запись) запишется как значение семантики с кодом code
        
        :returns: При успешном выполнении возвращает последовательный номер созданной характеристики В список семантик объекта добавляется семантика содержащая другой список - формируется ветка верхнего уровня дерева наборов семантик При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если такая семантика была и она не повторяемая - значение заменяется
        """
        return mapAppendGroupSemantic_t (_hobj, _code, _hsemrecord)

    mapGetGroupSemanticValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetGroupSemanticValue', maptype.HOBJ, ctypes.c_long, maptype.HSEMRECORD, maptype.PWCHAR, ctypes.c_int)
    def mapGetGroupSemanticValue(_hobj: maptype.HOBJ, _code: int, _hsemrecord: maptype.HSEMRECORD, _value: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить обобщенное значение групповой семантики
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _code: код семантической характеристики
        
        :param _hsemrecord: идентификатор записи набора семантик объекта
        
        :param _value: адрес области памяти для записи обобщенного значения, сформированного из значений групповых семантик
        
        :param _size: размер области в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetGroupSemanticValue_t (_hobj, _code, _hsemrecord, _value.buffer(), _size)

    mapSemanticCodeGroupValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticCodeGroupValue', maptype.HOBJ, ctypes.c_long, maptype.HSEMRECORD, ctypes.c_long)
    def mapSemanticCodeGroupValue(_hobj: maptype.HOBJ, _code: int, _hsemrecord: maptype.HSEMRECORD, _number: int) -> int:
        """
        Запросить по коду семантики значение семантической характеристики в виде набора семантик
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _code: код семантики, для которой ищется значение
        
        :param _hsemrecord: идентификатор записи набора семантик объекта, которая заполнится набором семантик из семантики с кодом code
        
        :param _number: последовательный номер с ``1`` запрашиваемого значения среди семантик с тем же кодом, не равен последовательному номеру характеристики
        
        :returns: При ошибке возвращает ноль, иначе - последовательный номер найденной характеристики
        :rtype: int
        """
        return mapSemanticCodeGroupValue_t (_hobj, _code, _hsemrecord, _number)

    mapSemanticGroupValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticGroupValue', maptype.HOBJ, ctypes.c_long, maptype.HSEMRECORD)
    def mapSemanticGroupValue(_hobj: maptype.HOBJ, _number: int, _hsemrecord: maptype.HSEMRECORD) -> int:
        """
        Запросить по номеру значение семантики в виде набора семантик
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: последовательный номер характеристики c ``1``
        
        :param _hsemrecord: идентификатор записи набора семантик объекта, которая заполнится набором семантик из семантики с кодом code
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSemanticGroupValue_t (_hobj, _number, _hsemrecord)

    mapSemanticRecordCodeGroupValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticRecordCodeGroupValue', maptype.HSEMRECORD, ctypes.c_long, maptype.HSEMRECORD, ctypes.c_long)
    def mapSemanticRecordCodeGroupValue(_hsemrecord: maptype.HSEMRECORD, _code: int, _hsubrecord: maptype.HSEMRECORD, _number: int) -> int:
        """
        Запросить значение семантической характеристики объекта в виде набора семантик
        
        :param _hsemrecord: идентификатор записи набора семантик объекта
        
        :param _code: код семантики, для которой ищется значение
        
        :param _hsubrecord: идентификатор записи набора семантик объекта, которая (запись) заполнится набором семантик из значения семантики с кодом code
        
        :param _number: последовательный номер с ``1`` запрашиваемого значения среди семантик с тем же кодом, не равен последовательному номеру характеристики Семантика, значением которой является набор семантик, может быть прочитана и как строка с коротким значением через функцию mapSemanticRecordValueNamee(). Содержание короткого значения определяется формулой, заданной в классификаторе
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSemanticRecordCodeGroupValue_t (_hsemrecord, _code, _hsubrecord, _number)

    mapSemanticRecordGroupValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticRecordGroupValue', maptype.HSEMRECORD, ctypes.c_long, maptype.HSEMRECORD)
    def mapSemanticRecordGroupValue(_hsemrecord: maptype.HSEMRECORD, _number: int, _hsubrecord: maptype.HSEMRECORD) -> int:
        """
        Запросить значение семантической характеристики объекта в виде набора семантик по номеру
        
        :param _hsemrecord: идентификатор записи набора семантик объекта
        
        :param _number: последовательный номер характеристики c ``1``
        
        :param _hsubrecord: идентификатор записи набора семантик объекта, которая (запись) заполнится набором семантик из значения семантики с кодом code
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSemanticRecordGroupValue_t (_hsemrecord, _number, _hsubrecord)

    mapSemanticRecordValueNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticRecordValueNameUn', maptype.HSEMRECORD, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapSemanticRecordValueNameUn(_hsemrecord: maptype.HSEMRECORD, _number: int, _value: mapsyst.WTEXT, _size: int, _separator: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить по номеру значение семантики в символьном раскодированном виде
        
        :param _hsemrecord: идентификатор записи набора семантик объекта
        
        :param _number: последовательный номер характеристики c ``1``
        
        :param _value: адрес буфера для записи значения семантики
        
        :param _size: длина буфера в байтах
        
        :param _separator: разделитель целой и дробной части ``0`` - десятичную точку не изменять ``1`` - заменить десятичную точку на символ, установленный в системе '.' или ',' - заменить десятичную точку на separator: '.' или ','
        
        :param _error: поле для записи кода ошибки, если значение семантики не соответствует ее типу Например: для семантики типа справочник ``"СОСТОЯНИЕ"`` значение ``"5"`` заменется на ``"жилой"``
        
        :returns: При ошибке возвращает ноль, иначе - код семантики
        :rtype: int
        """
        return mapSemanticRecordValueNameUn_t (_hsemrecord, _number, _value.buffer(), _size, _separator, _error)

    mapSemanticRecordValueFullNameUnicode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticRecordValueFullNameUnicode', maptype.HSEMRECORD, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapSemanticRecordValueFullNameUnicode(_hsemrecord: maptype.HSEMRECORD, _number: int, _value: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить по номеру значение семантики в раскодированном виде с единицей измерения
        
        :param _hsemrecord: идентификатор записи набора семантик объекта
        
        :param _number: последовательный номер характеристики c ``1``
        
        :param _value: адрес буфера для записи значения семантики
        
        :param _size: длина буфера в байтах Например: для семантики типа справочник ``"СОСТОЯНИЕ"`` значение ``"5"`` заменется на ``"жилой"`` Для числовой семантики ``"ВЫСОТА"`` значение ``"205,5"`` заменется на ``"205,5 м"``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSemanticRecordValueFullNameUnicode_t (_hsemrecord, _number, _value.buffer(), _size)

    mapSemanticRecordCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticRecordCode', maptype.HSEMRECORD, ctypes.c_long)
    def mapSemanticRecordCode(_hsemrecord: maptype.HSEMRECORD, _number: int) -> int:
        """
        Запросить код семантики по номеру семантики в наборе семантик
        
        :param _hsemrecord: идентификатор записи набора семантик объекта
        
        :param _number: последовательный номер характеристики c ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSemanticRecordCode_t (_hsemrecord, _number)

    mapSemanticRecordCodeValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticRecordCodeValue', maptype.HSEMRECORD, ctypes.c_long, ctypes.c_char_p, ctypes.c_long, ctypes.c_long)
    def mapSemanticRecordCodeValue(_hsemrecord: maptype.HSEMRECORD, _code: int, _value: ctypes.c_char_p, _size: int, _number: int) -> int:
        """
        Запросить по коду семантики значение в виде строки с разделителем для числа
        
        :param _hsemrecord: идентификатор записи набора семантик объекта
        
        :param _code: код семантики, для которой ищется значение
        
        :param _value: адрес буфера для записи значения семантики
        
        :param _size: длина буфера в байтах или ``0``
        
        :param _number: последовательный номер с ``1`` запрашиваемого значения среди семантик с тем же кодом, не равен последовательному номеру характеристики
        
        :returns: При ошибке возвращает ноль, иначе - последовательный номер найденной характеристики
        :rtype: int
        """
        return mapSemanticRecordCodeValue_t (_hsemrecord, _code, _value, _size, _number)

    mapSemanticRecordCodeValueUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticRecordCodeValueUn', maptype.HSEMRECORD, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSemanticRecordCodeValueUn(_hsemrecord: maptype.HSEMRECORD, _code: int, _value: mapsyst.WTEXT, _size: int, _number: int, _separator: int) -> int:
        """
        Запросить по коду семантики значение в виде строки с разделителем для числа
        
        :param _hsemrecord: идентификатор записи набора семантик объекта
        
        :param _code: код семантики, для которой ищется значение
        
        :param _value: адрес буфера для записи значения семантики
        
        :param _size: длина буфера в байтах
        
        :param _number: последовательный номер с ``1`` запрашиваемого значения среди семантик с тем же кодом, не равен последовательному номеру характеристики
        
        :param _separator: разделитель целой и дробной части ``0`` - десятичную точку не изменять ``1`` - заменить десятичную точку на символ, установленный в системе '.' или ',' - заменить десятичную точку на separator: '.' или ','
        
        :returns: При ошибке возвращает ноль, иначе - последовательный номер найденной характеристики
        :rtype: int
        """
        return mapSemanticRecordCodeValueUn_t (_hsemrecord, _code, _value.buffer(), _size, _number, _separator)

    mapSemanticRecordCodeKeyValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticRecordCodeKeyValue', maptype.HSEMRECORD, ctypes.c_long, ctypes.c_char_p, ctypes.c_long, ctypes.c_long)
    def mapSemanticRecordCodeKeyValue(_hsemrecord: maptype.HSEMRECORD, _code: int, _key: ctypes.c_char_p, _size: int, _number: int) -> int:
        """
        Запросить по коду семантики значение семантической характеристики типа справочник в виде ключа значения
        
        :param _hsemrecord: идентификатор записи набора семантик объекта
        
        :param _code: код семантики, для которой ищется значение
        
        :param _key: адрес буфера для записи значения ключа семантики (до ``64`` байт)
        
        :param _size: длина буфера в байтах
        
        :param _number: последовательный номер с ``1`` запрашиваемого значения среди семантик с тем же кодом, не равен последовательному номеру характеристики
        
        :returns: При ошибке возвращает ноль, иначе - последовательный номер найденной характеристики
        :rtype: int
        """
        return mapSemanticRecordCodeKeyValue_t (_hsemrecord, _code, _key, _size, _number)

    mapSemanticRecordCodeLongKeyValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticRecordCodeLongKeyValue', maptype.HSEMRECORD, ctypes.c_long, ctypes.c_char_p, ctypes.c_long, ctypes.c_long)
    def mapSemanticRecordCodeLongKeyValue(_hsemrecord: maptype.HSEMRECORD, _code: int, _key: ctypes.c_char_p, _size: int, _number: int) -> int:
        """
        Запросить по коду семантики значение семантической характеристики типа справочник в виде альтернативного ключа значения
        
        :param _hsemrecord: идентификатор записи набора семантик объекта
        
        :param _code: код семантики, для которой ищется значение
        
        :param _key: адрес буфера для записи значения ключа семантики (до ``256`` байт)
        
        :param _size: длина буфера в байтах
        
        :param _number: последовательный номер с ``1`` запрашиваемого значения среди семантик с тем же кодом, не равен последовательному номеру характеристики
        
        :returns: При ошибке возвращает ноль, иначе - последовательный номер найденной характеристики
        :rtype: int
        """
        return mapSemanticRecordCodeLongKeyValue_t (_hsemrecord, _code, _key, _size, _number)

    mapSemanticRecordCodeDoubleValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticRecordCodeDoubleValue', maptype.HSEMRECORD, ctypes.c_long, ctypes.POINTER(ctypes.c_double), ctypes.c_long)
    def mapSemanticRecordCodeDoubleValue(_hsemrecord: maptype.HSEMRECORD, _code: int, _value: ctypes.POINTER(ctypes.c_double), _number: int) -> int:
        """
        Запросить по коду семантики значение семантической характеристики типа справочник в виде числа двойной точности
        
        :param _hsemrecord: идентификатор записи набора семантик объекта
        
        :param _code: код семантики, для которой ищется значение
        
        :param _value: поле для записи значения семантики
        
        :param _number: последовательный номер с ``1`` запрашиваемого значения среди семантик с тем же кодом, не равен последовательному номеру характеристики
        
        :returns: При ошибке возвращает ноль, иначе - последовательный номер найденной характеристики
        :rtype: int
        """
        return mapSemanticRecordCodeDoubleValue_t (_hsemrecord, _code, _value, _number)

    mapSemanticRecordCodeLongValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSemanticRecordCodeLongValue', maptype.HSEMRECORD, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.c_long)
    def mapSemanticRecordCodeLongValue(_hsemrecord: maptype.HSEMRECORD, _code: int, _value: ctypes.POINTER(ctypes.c_long), _number: int) -> int:
        """
        Запросить по коду семантики значение семантической характеристики типа справочник в виде целого числа
        
        :param _hsemrecord: идентификатор записи набора семантик объекта
        
        :param _code: код семантики, для которой ищется значение
        
        :param _value: поле для записи значения семантики
        
        :param _number: последовательный номер с ``1`` запрашиваемого значения среди семантик с тем же кодом, не равен последовательному номеру характеристики
        
        :returns: При ошибке возвращает ноль, иначе - последовательный номер найденной характеристики
        :rtype: int
        """
        return mapSemanticRecordCodeLongValue_t (_hsemrecord, _code, _value, _number)

    mapGetExclusiveSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetExclusiveSubject', maptype.HOBJ, ctypes.c_long)
    def mapGetExclusiveSubject(_hobj: maptype.HOBJ, _number: int) -> int:
        """
        Запросить замкнутость объекта или подобъекта
        
        :param _hobj: идентификатор объекта карты в памяти subject - номер объекта (``0``) или подобъекта (больше ``0``) Внешний контур полигона или первый контур мультилинии - это контур объекта, внутренние контура полигона или второй и последующие контура мультилинии - это подобъекты
        
        :returns: Возвращает:  ``0`` - не замкнут, не ``0`` - замкнут
        :rtype: int
        """
        return mapGetExclusiveSubject_t (_hobj, _number)

    mapObjectFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectFrame', maptype.HOBJ, ctypes.POINTER(maptype.DFRAME))
    def mapObjectFrame(_hobj: maptype.HOBJ, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Запрос габаритов объекта в метрах в системе открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _dframe: поле для записи габаритов метрики объекта в метрах в системе документа
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Габариты перевычисляются по координатам объекта при каждом запросе
           Для полигона учитываются только внешние контура, для остальных локализаций - все контура
        """
        return mapObjectFrame_t (_hobj, _dframe)

    mapObjectFrameGeoWGS84_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectFrameGeoWGS84', maptype.HOBJ, ctypes.POINTER(maptype.DFRAME))
    def mapObjectFrameGeoWGS84(_hobj: maptype.HOBJ, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Запрос габаритов объекта в радианах в системе WGS84
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _dframe: поле для записи габаритов в радианах ``WGS84``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Габариты перевычисляются по координатам объекта при каждом запросе
           Для полигона учитываются только внешние контура, для остальных локализаций - все контура
        """
        return mapObjectFrameGeoWGS84_t (_hobj, _dframe)

    mapSubjectFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSubjectFrame', maptype.HOBJ, ctypes.c_long, ctypes.POINTER(maptype.DFRAME))
    def mapSubjectFrame(_hobj: maptype.HOBJ, _subject: int, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Запросить габариты подобъекта в метрах
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _dframe: поле для записи габаритов подобъекта в метрах в системе документа
        
        :param _subject: номер объекта (``0``) или подобъекта (больше ``0``) Внешний контур полигона или первый контур мультилинии - это контур объекта, внутренние контура полигона или второй и последующие контура мультилинии - это подобъекты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Габариты перевычисляются при каждом запросе
        """
        return mapSubjectFrame_t (_hobj, _subject, _dframe)

    mapObjectViewFrameEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectViewFrameEx', maptype.HOBJ, ctypes.POINTER(maptype.DFRAME), ctypes.c_long)
    def mapObjectViewFrameEx(_hobj: maptype.HOBJ, _dframe: ctypes.POINTER(maptype.DFRAME), _force: int) -> int:
        """
        Запрос габаритов изображения знака объекта в метрах
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _dframe: поле для записи габаритов изображения объекта в метрах
        
        :param _force: признак принудительного пересчета габаритов, необходимо установить, если объект редактировался, но не записан на карту
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Габариты считываются из заголовка объекта или перевычисляются по координатам объекта
           с учетом вида условного знака, если параметр force не равен нулю
        """
        return mapObjectViewFrameEx_t (_hobj, _dframe, _force)

    mapGetObjectContour_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetObjectContour', maptype.HOBJ, maptype.HOBJ, maptype.HPAINT)
    def mapGetObjectContour(_hobj: maptype.HOBJ, _hcontour: maptype.HOBJ, _hpaint: maptype.HPAINT) -> int:
        """
        Определить габаритную рамку изображения объекта в текущих условиях отображения
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _hcontour: идентификатор объекта, в метрику которого заносятся габариты исходного объекта
        
        :param _hpaint: идентификатор контекста отображения или ``0`` Определяет габариты объектов (точечных, векторных и подписей) с учетом текущих условий отображения (масштаб, разрешение устройства вывода) Для каждого подобъекта подписи создается прямоугольный подобъект, ограничивающий текст подписи
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapGetObjectContour_t (_hobj, _hcontour, _hpaint)

    mapPolyCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPolyCount', maptype.HOBJ)
    def mapPolyCount(_hobj: maptype.HOBJ) -> int:
        """
        Запрос числа частей метрики (объект и подобъекты)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: Если подобъектов нет - возвращает 1 (только объект) При ошибке возвращает ноль
        :rtype: int
        """
        return mapPolyCount_t (_hobj)

    mapPointCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPointCount', maptype.HOBJ, ctypes.c_long)
    def mapPointCount(_hobj: maptype.HOBJ, _subject: int) -> int:
        """
        Запрос числа точек метрики объекта или подобъекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Внешний контур полигона или первый контур мультилинии - это контур объекта, внутренние контура полигона или второй и последующие контура мультилинии - это подобъекты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPointCount_t (_hobj, _subject)

    mapGetGeoPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetGeoPoint', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.c_long)
    def mapGetGeoPoint(_hobj: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _number: int, _subject: int) -> int:
        """
        Запросить геодезические координаты точки в радианах в системе документа
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _point: поле для записи координат точки ``DOUBLEPOINT``::X - широта в радианах ``DOUBLEPOINT``::Y - долгота в радианах
        
        :param _number: номер точки с ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetGeoPoint_t (_hobj, _point, _number, _subject)

    mapGetMapGeoPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMapGeoPoint', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.c_long)
    def mapGetMapGeoPoint(_hobj: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _number: int, _subject: int) -> int:
        """
        Запросить геодезические координаты точки в радианах в системе координат карты
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _point: поле для записи координат точки ``DOUBLEPOINT``::X - широта в радианах ``DOUBLEPOINT``::Y - долгота в радианах
        
        :param _number: номер точки с ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMapGeoPoint_t (_hobj, _point, _number, _subject)

    mapGetGeoPointWGS84_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetGeoPointWGS84', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.c_long)
    def mapGetGeoPointWGS84(_hobj: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _number: int, _subject: int) -> int:
        """
        Запросить геодезические координаты 2D точки в радианах на эллипсоиде WGS84
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _point: поле для записи координат точки ``DOUBLEPOINT``::X - широта в радианах ``WGS84`` ``DOUBLEPOINT``::Y - долгота в радианах ``WGS84``
        
        :param _number: номер точки с ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetGeoPointWGS84_t (_hobj, _point, _number, _subject)

    mapGetGeoPointWGS843D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetGeoPointWGS843D', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(ctypes.c_double), ctypes.c_long, ctypes.c_long)
    def mapGetGeoPointWGS843D(_hobj: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _heigth: ctypes.POINTER(ctypes.c_double), _number: int, _subject: int) -> int:
        """
        Запросить геодезические координаты 3D точки в радианах на эллипсоиде WGS84
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _point: поле для записи координат точки ``DOUBLEPOINT``::X - широта в радианах ``WGS84`` ``DOUBLEPOINT``::Y - долгота в радианах ``WGS84``
        
        :param _heigth: поле для записи нормальной или ортометрической высоты (например, ``MSL``) или ``0``
        
        :param _number: номер точки с ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetGeoPointWGS843D_t (_hobj, _point, _heigth, _number, _subject)

    mapGetMapPlanePoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMapPlanePoint', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.c_long)
    def mapGetMapPlanePoint(_hobj: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _number: int, _subject: int) -> int:
        """
        Запрос координат точки в метрах в системе координат карты
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _point: поле для записи координат точки ``DOUBLEPOINT``::X - координата в метрах на север, ``DOUBLEPOINT``::Y - координата в метрах на восток
        
        :param _number: номер точки с ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMapPlanePoint_t (_hobj, _point, _number, _subject)

    mapGetPlanePoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetPlanePoint', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.c_long)
    def mapGetPlanePoint(_hobj: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _number: int, _subject: int) -> int:
        """
        Запросить координаты точки в системе координат документа в метрах
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _point: поле для записи координат точки ``DOUBLEPOINT``::X - координата в метрах на север, ``DOUBLEPOINT``::Y - координата в метрах на восток
        
        :param _number: номер точки (начинается с ``1``)
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetPlanePoint_t (_hobj, _point, _number, _subject)

    mapHPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapHPlane', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapHPlane(_hobj: maptype.HOBJ, _number: int, _subject: int) -> float:
        """
        Запрос высоты точки объекта в метрах на местности
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: номер точки с ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Для получения значения высоты объект должен иметь тип метрики ``IDDOUBLE3``, ``IDDOUBLE4``, ``IDDOUBLE4F`` или ``IDLONG3``
        
        :returns: Возвращает значение координаты высота или ноль
        :rtype: float
        
        .. note::

           Если значение высоты для точки не устанавливалось, то возвращаемое значение может
           быть равно псевдокоду высоты: -111111 (ERRORHEIGHT)
        """
        return mapHPlane_t (_hobj, _number, _subject)

    mapHPlaneEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapHPlaneEx', maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def mapHPlaneEx(_hobj: maptype.HOBJ, _number: int, _subject: int, _h: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запрос высоты точки объекта в метрах на местности с контролем наличия высоты
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: номер точки с ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :param _h: поле для записи значения высоты точки Для получения значения высоты объект должен иметь тип метрики ``IDDOUBLE3``, ``IDDOUBLE4``, ``IDDOUBLE4F`` или ``IDLONG3``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если значение высоты для точки не устанавливалось, то возвращаемое значение может
           быть равно псевдокоду высоты: -111111 (ERRORHEIGHT)
        """
        return mapHPlaneEx_t (_hobj, _number, _subject, _h)

    mapIsObject3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsObject3D', maptype.HOBJ)
    def mapIsObject3D(_hobj: maptype.HOBJ) -> int:
        """
        Запросить, имеет ли объект 3D метрику
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: Если да, возвращает ненулевое значение
        :rtype: int
        """
        return mapIsObject3D_t (_hobj)

    mapGetHeightType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetHeightType', maptype.HOBJ)
    def mapGetHeightType(_hobj: maptype.HOBJ) -> int:
        """
        Запросить тип высоты в третьей координате
        
        :param _hobj: идентификатор объекта карты в памяти Реально высота может быть и не задана
        
        :returns: Возвращает: ``0`` - если в метрике хранитя абсолютная высота, ненулевое значение - относительная высота При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetHeightType_t (_hobj)

    mapSetHeightType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetHeightType', maptype.HOBJ, ctypes.c_long)
    def mapSetHeightType(_hobj: maptype.HOBJ, _type: int) -> int:
        """
        Установить тип высоты в третьей координате
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _type: тип высоты: ``0`` - абсолютная, иначе - относительная Значение высоты может быть установлено позднее Объекты с относительной высотой не влияют на построение матрицы высот
        """
        return mapSetHeightType_t (_hobj, _type)

    mapCheckHeightCorrect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckHeightCorrect', maptype.HOBJ)
    def mapCheckHeightCorrect(_hobj: maptype.HOBJ) -> int:
        """
        Проверить, что третья координата метрики содержит допустимые значения абсолютной высоты
        
        :param _hobj: идентификатор объекта карты в памяти Выполняется проверка, что хотя бы одна точка содержит высоту, не равную псевдокоду: -``111111``
        
        :returns: При отсутствии допустимых значений возвращает ноль
        :rtype: int
        """
        return mapCheckHeightCorrect_t (_hobj)

    mapMValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapMValue', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapMValue(_hobj: maptype.HOBJ, _number: int, _subject: int) -> float:
        """
        Запросить значение 4-го измерения точки метрики
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: номер точки с ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Для получения значения измерения объект должен иметь тип метрики ``IDDOUBLE4``
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapMValue_t (_hobj, _number, _subject)

    mapFValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int64,'mapFValue', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapFValue(_hobj: maptype.HOBJ, _number: int, _subject: int) -> int:
        """
        Запросить значение 4-го измерения точки метрики в виде большого целого числа
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: номер точки с ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Для получения значения измерения объект должен иметь тип метрики ``IDDOUBLE4F``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapFValue_t (_hobj, _number, _subject)

    mapIsMultiPolygon_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsMultiPolygon', maptype.HOBJ)
    def mapIsMultiPolygon(_hobj: maptype.HOBJ) -> int:
        """
        Запросить является ли объект мультиполигоном
        
        :param _hobj: идентификатор объекта карты в памяти Мультиполигон - это площадной объект, у которого некоторые подобъекты могут быть вне границ объекта При подсчете площади мультиполигона площадь внешних подобъектов будет добавляться к площади основного объекта, а площади внутренних подобъектов - вычитаться
        
        :returns: Если объект является мультиполигоном, то возвращается ненулевое значение
        :rtype: int
        """
        return mapIsMultiPolygon_t (_hobj)

    mapSetMultiPolygonAndCheckObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMultiPolygonAndCheckObject', maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSetMultiPolygonAndCheckObject(_hobj: maptype.HOBJ, _multi: int, _isautoset: int, _ischeckobject: int) -> int:
        """
        Установить или сбросить признак мультиполигона
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _multi: признак мультиполигона: ``0`` или ``1``
        
        :param _isautoset: признак необходимости подтверждения наличия внешних контуров: ``0`` или ``1``
        
        :param _ischeckobject: контроль главного контура объекта - проверить, что объект не входит в какой-либо подобъект и перенести этот подобъект перед объектом при необходимости (сделать главным), если в главном (нулевом) контуре меньше ``4`` точек, то он удаляется
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если при подтверждении наличия внешних контуров они не будут найдены, то
           признак мультиполигона не будет установлен. Для большого числа точек и подобъектов
           для подтверждения запускается набор потоков для определения входимости подобъектов
        """
        return mapSetMultiPolygonAndCheckObject_t (_hobj, _multi, _isautoset, _ischeckobject)

    mapGetSubjectMultiFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSubjectMultiFlag', maptype.HOBJ, ctypes.c_long)
    def mapGetSubjectMultiFlag(_hobj: maptype.HOBJ, _subject: int) -> int:
        """
        Запросить флаг размещения подобъекта вне площадного объекта (полигона)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: Для внешних подобъектов возвращает отрицательное значение (-1), для внутренних подобъектов возвращает номер внешнего подобъекта (c 0), в который входит данный подобъект При отсутствии описания возвращает ноль
        :rtype: int
        """
        return mapGetSubjectMultiFlag_t (_hobj, _subject)

    mapSetSubjectMultiFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSubjectMultiFlag', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSetSubjectMultiFlag(_hobj: maptype.HOBJ, _subject: int, _flag: int) -> int:
        """
        Установить флаг размещения подобъекта вне площадного объекта (полигона)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :param _flag: признак размещения (входимости) подобъекта Для внешних подобъектов устанавливается отрицательное значение (-``1``), для внутренних подобъектов устанавливается номер внешнего подобъекта (c ``0``), в который входит данный подобъект
        
        :returns: При отсутствии описания возвращает ноль
        :rtype: int
        """
        return mapSetSubjectMultiFlag_t (_hobj, _subject, _flag)

    mapGetMultiSubjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMultiSubjectCount', maptype.HOBJ)
    def mapGetMultiSubjectCount(_hobj: maptype.HOBJ) -> int:
        """
        Запросить число внешних контуров в площадном объекте (полигоне)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMultiSubjectCount_t (_hobj)

    mapGetMultiSubjectNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMultiSubjectNumber', maptype.HOBJ, ctypes.c_long)
    def mapGetMultiSubjectNumber(_hobj: maptype.HOBJ, _number: int) -> int:
        """
        Запросить номер подобъекта внешнего контура в площадном объекте (полигоне)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: порядковый номер внешнего контура от ``1`` до mapGetMultiSubjectCount
        
        :returns: При отсутствии описания возвращает -1
        :rtype: int
        """
        return mapGetMultiSubjectNumber_t (_hobj, _number)

    mapIsMultiContour_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsMultiContour', maptype.HOBJ)
    def mapIsMultiContour(_hobj: maptype.HOBJ) -> int:
        """
        Запросить, является ли объект мультимасштабным
        
        :param _hobj: идентификатор объекта карты в памяти Мультимасштабный объект имеет несколько контуров для разных масштабов Мультимасштабные объекты могут формироваться при сортировке карты, если задана соответствующая опция, и в классификаторе карты объект имеет свойство ``"мультимасштабный"``
        
        :returns: Если объект мультимасштабный, то возвращается ненулевое значение
        :rtype: int
        """
        return mapIsMultiContour_t (_hobj)

    mapClearMultiContour_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapClearMultiContour', maptype.HOBJ)
    def mapClearMultiContour(_hobj: maptype.HOBJ) -> ctypes.c_void_p:
        """
        Удалить признак мультимасштабного объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        """
        return mapClearMultiContour_t (_hobj)

    mapIsPolygonWithPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsPolygonWithPoint', maptype.HOBJ)
    def mapIsPolygonWithPoint(_hobj: maptype.HOBJ) -> int:
        """
        Запросить, является ли объект полигоном с центральной точкой
        
        :param _hobj: идентификатор объекта карты в памяти Центральная точка - это подобъект с одной точкой, которая вычисляется в центре полигона, но может быть смещена оператором В этой точке отображается точечный знак, заданный в классификаторе
        
        :returns: Если да, возвращает ненулевое значение
        :rtype: int
        """
        return mapIsPolygonWithPoint_t (_hobj)

    mapIsDesignObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsDesignObject', maptype.HOBJ)
    def mapIsDesignObject(_hobj: maptype.HOBJ) -> int:
        """
        Запросить, является ли объект объектом оформления
        
        :param _hobj: идентификатор объекта карты в памяти Свойство ``"объект оформления"`` устанавливается в классификаторе ``RSC``
        
        :returns: Если это объект оформления, то возвращается ненулевое значение
        :rtype: int
        """
        return mapIsDesignObject_t (_hobj)

    mapGetObjectCenterEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetObjectCenterEx', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_long)
    def mapGetObjectCenterEx(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _x: ctypes.POINTER(ctypes.c_double), _y: ctypes.POINTER(ctypes.c_double), _type: int) -> int:
        """
        Определить центр объекта
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _x: поле для записи координаты x центра (на север) в метрах в системе документа
        
        :param _y: поле для записи координаты y центра (на восток) в метрах в системе документа
        
        :param _type: тип алгоритма определения центра контура: ``0`` - для полигона строится линия сечения по центру вертикальных габаритов объекта с поиском середины отрезка сечения; для линии ищется примерная середина контура по всей длине ``1`` - для полигона вычисляется геометрическое среднее значение контура объекта, для остальных объектов вычисляется геометрическое среднее значение координат всех точек
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetObjectCenterEx_t (_hmap, _hobj, _x, _y, _type)

    mapGetDrawedObjectFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetDrawedObjectFrame', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DFRAME), ctypes.c_long, ctypes.c_long)
    def mapGetDrawedObjectFrame(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _frame: ctypes.POINTER(maptype.DFRAME), _viewtype: int, _flag: int) -> int:
        """
        Запросить габариты объекта (векторного, точечного, подписи) в текущем масштабе
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта
        
        :param _frame: поле для записи габаритов объекта
        
        :param _viewtype: тип отображения карты: ``VT_SCREEN`` - экранный вид ``VT_PRINT`` - принтерный вид ``0`` - тип отображения карты определяется автоматически (текущий вид карты hmap)
        
        :param _flag: признак системы координат габаритов объекта: ``0`` - в метрах на местности (относительно точки привязки знака) ``1`` - в абсолютных метрах на местности ``2`` - не расширять габариты знака (допустимо совместное использование флагов - ``1``|``2``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetDrawedObjectFrame_t (_hmap, _hobj, _frame, _viewtype, _flag)

    mapIsObjectDataEquivalent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsObjectDataEquivalent', maptype.HOBJ, maptype.HOBJ)
    def mapIsObjectDataEquivalent(_hobj: maptype.HOBJ, _hanother: maptype.HOBJ) -> int:
        """
        Запросить, совпадают ли координаты объектов с точностью DELTANULL
        
        :param _hobj: идентификатор исходного объекта карты в памяти
        
        :param _hanother: идентификатор объекта карты в памяти для сравнения метрики
        
        :returns: При совпадении возвращает ненулевое значение
        :rtype: int
        """
        return mapIsObjectDataEquivalent_t (_hobj, _hanother)

    mapIsObjectDataEquivalentEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsObjectDataEquivalentEx', maptype.HOBJ, maptype.HOBJ, ctypes.c_long, ctypes.c_double, ctypes.POINTER(ctypes.c_double))
    def mapIsObjectDataEquivalentEx(_hobj: maptype.HOBJ, _hanother: maptype.HOBJ, _subject: int, _precision: float, _hprecision: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить, совпадают ли координаты подобъекта с заданной точностью
        
        :param _hobj: идентификатор исходного объекта карты в памяти
        
        :param _hanother: идентификатор объекта карты в памяти для сравнения метрики
        
        :param _subject: номер подобъекта или -``1`` (все подобъекты)
        
        :param _precision: точность сравнения координат на плоскости
        
        :param _hprecision: точность сравнения высот или ноль (не проверять)
        
        :returns: При совпадении возвращает ненулевое значение
        :rtype: int
        """
        return mapIsObjectDataEquivalentEx_t (_hobj, _hanother, _subject, _precision, _hprecision)

    mapHideCommonBuffer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapHideCommonBuffer', ctypes.c_int)
    def mapHideCommonBuffer(_hide: int) -> int:
        """
        Включить или отключить доступ к общему буферу векторных карт для работы с большими объемами данных
        
        :param _hide: признак отключения общего буфера памяти для векторных карт (``1`` или ``0``) Общий буфер не рекомендуется применять для многопоточных приложений
        
        :returns: Возвращает значение флага доступа, который был до вызова функции
        :rtype: int
        
        .. note::

           Если буфер отключен, то при нехватке памяти будет формироватся ошибка при чтении данных карт
        """
        return mapHideCommonBuffer_t (_hide)

    mapIsCommonBufferActive_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsCommonBufferActive')
    def mapIsCommonBufferActive() -> int:
        """
        Запросить, используется ли общий буфер векторных карт
        
        В этом случае многопоточный режим использования MAPAPI-функций не применим
        
        :returns: Если буфер используется, то возвращает ненулевое значение
        :rtype: int
        """
        return mapIsCommonBufferActive_t ()

    mapSetTotalMapMemoryLimitKb_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetTotalMapMemoryLimitKb', ctypes.c_int64)
    def mapSetTotalMapMemoryLimitKb(_maxsize: int) -> ctypes.c_void_p:
        """
        Установить ограничение объема открытых векторных карт в Кб
        
        :param _maxsize: предельное значение объема памяти в Кб для размещения векторных карт При достижении ``75````%`` от заданного объема открытых данных будет включаться механизм прокачки векторных карт через буфер обмена
        """
        return mapSetTotalMapMemoryLimitKb_t (_maxsize)

    mapGetTotalMapMemoryLimitKb_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int64,'mapGetTotalMapMemoryLimitKb')
    def mapGetTotalMapMemoryLimitKb() -> int:
        """
        Запросить ограничение объема открытых векторных карт в Кб
        """
        return mapGetTotalMapMemoryLimitKb_t ()

    mapSetTimeForWaitingDataReady_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetTimeForWaitingDataReady', ctypes.c_int)
    def mapSetTimeForWaitingDataReady(_waitTime: int) -> int:
        """
        Установить максимальное время работы функций в милисекундах
        
        Пример функций на которые влияет установленное время: поиск объектов, рисование области
        и другие функции, обращающиеся к данным
        Функция используется для работы с большими объёмами данных, время первой загрузки
        или обновления которых может занимать минуты
        Если установлено время и данные не готовы для работы за заданный промежуток времени,
        то выполнение функции, обращающейся к данным, завершится с ошибкой
        
        :returns: Возвращает старое значение в милисекундах
        :rtype: int
        """
        return mapSetTimeForWaitingDataReady_t (_waitTime)

    mapGetLinearPointCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetLinearPointCount', maptype.HOBJ)
    def mapGetLinearPointCount(_hobj: maptype.HOBJ) -> int:
        """
        Запросить количество калибровочных точек линейных координат для объекта
        
        :param _hobj: идентификатор объекта карты в памяти Любому линейному объекту могут быть присвоены калибровочные точки для определения линейных координат Например: участок дороги может иметь километровые столбы по которым определяется (интерполируется) линейная координата любой точки дороги
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если калибровочные точки не заданы, то вычисления линейных координат идут
           по длине объекта от его начала
        """
        return mapGetLinearPointCount_t (_hobj)

    mapGetLinearPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetLinearPoint', maptype.HOBJ, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(ctypes.c_double))
    def mapGetLinearPoint(_hobj: maptype.HOBJ, _number: int, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _linear: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить описание калибровочной точки линейных координат по номеру
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: номер калибровочной точки от ``1`` до mapGetLinearPointCount
        
        :param _point: поле для записи координаты калибровочной точки линейных координат в метрах в системе координат документа
        
        :param _linear: поле для записи калибровочного расстояния от первой точки объекта до калибровочной точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetLinearPoint_t (_hobj, _number, _point, _linear)

    mapAppendLinearPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendLinearPoint', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double)
    def mapAppendLinearPoint(_hobj: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _linear: float) -> int:
        """
        Добавить калибровочную точку линейных координат для объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _point: координаты калибровочной точки линейных координат в метрах в системе координат документа
        
        :param _linear: калибровочное расстояние от первой точки объекта до калибровочной точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendLinearPoint_t (_hobj, _point, _linear)

    mapDeleteLinearPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteLinearPoint', maptype.HOBJ, ctypes.c_long)
    def mapDeleteLinearPoint(_hobj: maptype.HOBJ, _number: int) -> int:
        """
        Удалить калибровочную точку линейных координат для объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: номер удалаяемой калибровочной точки от ``1`` до GetLinearPointCount()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если number равен -1, удаляются все калибровочные точки
        """
        return mapDeleteLinearPoint_t (_hobj, _number)

    mapPlanePointToLinearPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPlanePointToLinearPoint', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(ctypes.c_double))
    def mapPlanePointToLinearPoint(_hobj: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _linear: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Рассчитать линейную координату для заданной точки по ее плоским прямоугольным координатам
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _point: координаты точки в системе документа, для которой определяется линейная координата
        
        :param _linear: поле для записи линейной координаты в метрах При наличии калибровочных точек линейных координат выполняется интерполяция положения заданной точки, иначе - поиск положения точки в SeekNearVirtualPoint()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPlanePointToLinearPoint_t (_hobj, _point, _linear)

    mapLinearPointToPlanePointEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLinearPointToPlanePointEx', maptype.HOBJ, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long)
    def mapLinearPointToPlanePointEx(_hobj: maptype.HOBJ, _linear: float, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _intermediate: int) -> int:
        """
        Определить координаты в системе документа для заданной линейной координаты
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _linear: линейные координаты точки на контуре объекта в метрах
        
        :param _point: поле для записи координат точки в системе документа, для которой вычисляется линейная координата
        
        :param _intermediate: флаг определения положения точки между крайними точками подобъектов: ``0`` - выбирать результирующую точку на контуре объекта или подобъектов ``1`` - выбирать точку между последней точкой одного подобъекта и первой точкой другого подобъекта, если в этих точках есть калибровочные точки или ``4``-е измерение с линейной координатой и входное значение линейной координаты попадает между ними
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapLinearPointToPlanePointEx_t (_hobj, _linear, _point, _intermediate)

    mapLinearPointToPlanePointForObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLinearPointToPlanePointForObject', maptype.HOBJ, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapLinearPointToPlanePointForObject(_hobj: maptype.HOBJ, _linear: float, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Определить координаты в системе документа для заданных линейных координат
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _linear: линейные координаты точки на контуре объекта в метрах
        
        :param _point: поле для записи координат точки в системе документа, для которой вычисляется линейная координата Найденная точка притягивается к контуру объекта в системе координат карты (искажается) Не применять для заполнения баз данных - результат зависим от системы координат карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapLinearPointToPlanePointForObject_t (_hobj, _linear, _point)

    mapLoadSelectedLinearPoints_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLoadSelectedLinearPoints', maptype.HMAP, maptype.HSELECT, maptype.HSELECT, ctypes.c_double, ctypes.c_long)
    def mapLoadSelectedLinearPoints(_hmap: maptype.HMAP, _hrouteselect: maptype.HSELECT, _hpointsselect: maptype.HSELECT, _deviation: float, _linearsemanticcode: int) -> int:
        """
        Связать калибровочные точки с маршрутами по двум группам выделенных объектов
        
        :param _hmap: идентификатор открытых данных (документа), в состав которых входит карта маршрутов и карта с калибровочными точками (могут быть на одной карте)
        
        :param _hrouteselect: условия отбора объектов - маршрутов
        
        :param _hpointsselect: условия отбора объектов - калибровочных точек
        
        :param _deviation: значение допустимого отклонения координат калибровочной точки от осевой линии маршрута в метрах
        
        :param _linearsemanticcode: код семантики калибровочной точки, содержащий калибровочное значение линейной координаты Для каждой найденной пары маршрут и калибровочная точка вызывается mapAppendLinearPoint
        
        :returns: Если все найденные точки уже есть в маршруте - возвращает отрицательное число найденных точек При ошибке или отсутствии добавленных и дублирующихся точек возвращает ноль
        :rtype: int
        """
        return mapLoadSelectedLinearPoints_t (_hmap, _hrouteselect, _hpointsselect, _deviation, _linearsemanticcode)

    mapSetMaxLengthDistortionFactor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMaxLengthDistortionFactor', ctypes.c_long)
    def mapSetMaxLengthDistortionFactor(_factor: int) -> int:
        """
        Установить предельное искажение линейных измерений для линейных координат
        
        :param _factor: предельное искажение линейных измерений от ``1`` до ``10``, определяется как предел соотношения разницы линейных координат между смежными калибровочными точками и расчетной длины этих участков на эллипсоиде
        
        :returns: Возвращает установленное значение
        :rtype: int
        """
        return mapSetMaxLengthDistortionFactor_t (_factor)

    mapGetMaxLengthDistortionFactor_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMaxLengthDistortionFactor')
    def mapGetMaxLengthDistortionFactor() -> int:
        """
        Запросить предельное искажение линейных измерений для линейных координат
        """
        return mapGetMaxLengthDistortionFactor_t ()

    mapSetLinearPointAsMValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetLinearPointAsMValue', maptype.HOBJ)
    def mapSetLinearPointAsMValue(_hobj: maptype.HOBJ) -> int:
        """
        Установить в четвертое измерение каждой точки значение линейной координаты в этой точке (калибровка маршрута)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если объект не содержит калибровочных точек, то в четвертое измерение будет записана длина от начала объекта на эллипсоиде WGS84
           Применяется перед записью объекта в таблицу маршрутов базы пространственных данных
        """
        return mapSetLinearPointAsMValue_t (_hobj)

    mapAppendPointPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendPointPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapAppendPointPlane(_hobj: maptype.HOBJ, _x: float, _y: float, _subject: int) -> int:
        """
        Добавить в конец метрики объекта точку
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _x: координата x (на север) точки в метрах в системе координат документа
        
        :param _y: координата y (на восток) точки в метрах в системе координат документа
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Для изменения координаты Н необходимо далее выполнить функцию SetHPlane()
        
        :returns: Возвращает номер добавленной точки в подобъекте (с 1) При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendPointPlane_t (_hobj, _x, _y, _subject)

    mapAppendMapPointPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendMapPointPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapAppendMapPointPlane(_hobj: maptype.HOBJ, _x: float, _y: float, _subject: int) -> int:
        """
        Добавить в конец метрики объекта точку в прямоугольной системе в метрах на местности в проекции карты
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _x: координата x (на север) точки в метрах в системе координат карты
        
        :param _y: координата y (на восток) точки в метрах в системе координат карты
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Для изменения координаты Н необходимо далее выполнить функцию SetHPlane()
        
        :returns: Возвращает номер добавленной точки в подобъекте (с 1) При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendMapPointPlane_t (_hobj, _x, _y, _subject)

    mapAppendPointPlane3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendPointPlane3D', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapAppendPointPlane3D(_hobj: maptype.HOBJ, _x: float, _y: float, _h: float, _subject: int) -> int:
        """
        Добавить в конец метрики объекта точку
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _x: координата x (на север) точки в метрах в системе координат документа
        
        :param _y: координата y (на восток) точки в метрах в системе координат документа
        
        :param _h: высота (абсолютная или относительная) в метрах
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Тип высоты определяется функциями mapGetHeightType и mapSetHeightType
        
        :returns: Возвращает номер добавленной точки в подобъекте (с 1) При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendPointPlane3D_t (_hobj, _x, _y, _h, _subject)

    mapAppendPointPlane4D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendPointPlane4D', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapAppendPointPlane4D(_hobj: maptype.HOBJ, _x: float, _y: float, _h: float, _m: float, _subject: int) -> int:
        """
        Добавить в конец метрики объекта точку и измерение (свойство) в точке
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _x: координата x (на север) точки в метрах в системе координат документа
        
        :param _y: координата y (на восток) точки в метрах в системе координат документа
        
        :param _h: нормальная или ортометрическая высота в точке (записывается без преобразований) или относительная высота Тип высоты определяется функциями mapGetHeightType и mapSetHeightType
        
        :param _m: измерение в формате double (для типа метрики ``IDDOUBLE4``)
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: Возвращает номер добавленной точки в подобъекте (с 1) При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendPointPlane4D_t (_hobj, _x, _y, _h, _m, _subject)

    mapAppendPointPlane4F_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendPointPlane4F', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int64, ctypes.c_long)
    def mapAppendPointPlane4F(_hobj: maptype.HOBJ, _x: float, _y: float, _h: float, _f: int, _subject: int) -> int:
        """
        Добавить в конец метрики объекта точку и целочисленное измерение (свойство) в точке
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _x: координата x (на север) точки в метрах в системе координат документа
        
        :param _y: координата y (на восток) точки в метрах в системе координат документа
        
        :param _h: нормальная или ортометрическая высота в точке (записывается без преобразований) или относительная высота Тип высоты определяется функциями mapGetHeightType и mapSetHeightType
        
        :param _f: измерение в формате __int64 (для типа метрики ``IDDOUBLE4F``)
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: Возвращает номер добавленной точки в подобъекте (с 1) При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendPointPlane4F_t (_hobj, _x, _y, _h, _f, _subject)

    mapDeletePointPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeletePointPlane', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapDeletePointPlane(_hobj: maptype.HOBJ, _number: int, _subject: int) -> int:
        """
        Удалить заданную точку метрики
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: номер точки с ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeletePointPlane_t (_hobj, _number, _subject)

    mapDeleteEqualPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteEqualPoint', maptype.HOBJ, ctypes.c_double, ctypes.c_long)
    def mapDeleteEqualPoint(_hobj: maptype.HOBJ, _precision: float, _height: int) -> int:
        """
        Удаление из метрики одинаковых точек
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _precision: величина расхождения значений координат в метрах на местности
        
        :param _height: признак учета трехмерной метрики (в этом случае две одинаковые точки с разной высотой считаются разными)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteEqualPoint_t (_hobj, _precision, _height)

    mapDeletePartObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeletePartObject', maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapDeletePartObject(_hobj: maptype.HOBJ, _number1: int, _number2: int, _subject: int) -> int:
        """
        Удалить из подобъекта участок по номерам точек
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number1: номер с ``1`` первой удаляемой точки в диапазоне
        
        :param _number2: номер с ``1`` последней удаляемой точки в диапазоне
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки При удалении всех точек подобъекта удаляется только метрика, подобъект не удаляется и будет содержать ``0`` точек
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeletePartObject_t (_hobj, _number1, _number2, _subject)

    mapInsertPointPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapInsertPointPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapInsertPointPlane(_hobj: maptype.HOBJ, _x: float, _y: float, _number: int, _subject: int) -> int:
        """
        Вставить в метрику объекта точку
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _x: координата x (на север) точки в метрах в системе координат документа
        
        :param _y: координата y (на восток) точки в метрах в системе координат документа
        
        :param _number: номер точки с ``0``, за которой будет добавлена новая точка
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Для изменени координаты Н необходимо далее выполнить функцию mapSetHPlane()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapInsertPointPlane_t (_hobj, _x, _y, _number, _subject)

    mapInsertMapPointPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapInsertMapPointPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapInsertMapPointPlane(_hobj: maptype.HOBJ, _x: float, _y: float, _number: int, _subject: int) -> int:
        """
        Вставить в метрику объекта точку
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _x: координата x (на север) точки в метрах в системе координат карты
        
        :param _y: координата y (на восток) точки в метрах в системе координат карты
        
        :param _number: номер точки c ``0``, за которой будет добавлена новая точка
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Для изменени координаты Н необходимо далее выполнить функцию mapSetHPlane()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapInsertMapPointPlane_t (_hobj, _x, _y, _number, _subject)

    mapUpdatePointPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdatePointPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapUpdatePointPlane(_hobj: maptype.HOBJ, _x: float, _y: float, _number: int, _subject: int) -> int:
        """
        Изменить координаты точки метрики
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _x: координата x (на север) точки в метрах в системе координат документа
        
        :param _y: координата y (на восток) точки в метрах в системе координат документа
        
        :param _number: номер точки c ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdatePointPlane_t (_hobj, _x, _y, _number, _subject)

    mapUpdatePointPlane3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdatePointPlane3D', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapUpdatePointPlane3D(_hobj: maptype.HOBJ, _x: float, _y: float, _h: float, _number: int, _subject: int) -> int:
        """
        Изменить координаты точки метрики
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _x: координата x (на север) точки в метрах в системе координат документа
        
        :param _y: координата y (на восток) точки в метрах в системе координат документа
        
        :param _h: нормальная или ортометрическая высота в точке (записывается без преобразований) или относительная высота Тип высоты определяется функциями mapGetHeightType и mapSetHeightType
        
        :param _number: номер точки c ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdatePointPlane3D_t (_hobj, _x, _y, _h, _number, _subject)

    mapUpdateMapPointPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateMapPointPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapUpdateMapPointPlane(_hobj: maptype.HOBJ, _x: float, _y: float, _number: int, _subject: int) -> int:
        """
        Изменить координаты точки метрики
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _x: координата x (на север) точки в метрах в системе координат карты
        
        :param _y: координата y (на восток) точки в метрах в системе координат карты
        
        :param _number: номер точки с ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdateMapPointPlane_t (_hobj, _x, _y, _number, _subject)

    mapAppendPointGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendPointGeo', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapAppendPointGeo(_hobj: maptype.HOBJ, _b: float, _l: float, _subject: int) -> int:
        """
        Добавить в конец метрики объекта точку
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _b: широта точки в радианах в геодезической системе координат документа
        
        :param _l: долгота точки в радианах в геодезической системе координат документа
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: Возвращает номер добавленной точки в подобъекте с 1 При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendPointGeo_t (_hobj, _b, _l, _subject)

    mapAppendMapPointGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendMapPointGeo', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapAppendMapPointGeo(_hobj: maptype.HOBJ, _b: float, _l: float, _subject: int) -> int:
        """
        Добавить в конец метрики объекта точку в геодезической системе карты
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _b: широта точки в радианах в геодезической системе координат карты
        
        :param _l: долгота точки в радианах в геодезической системе координат карты
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Значение координат задано в радианах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendMapPointGeo_t (_hobj, _b, _l, _subject)

    mapAppendPointGeoWGS84_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendPointGeoWGS84', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapAppendPointGeoWGS84(_hobj: maptype.HOBJ, _b: float, _l: float, _subject: int) -> int:
        """
        Добавить в конец метрики объекта точку
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _b: широта точки в радианах в геодезической системе ``WGS84``
        
        :param _l: долгота точки в радианах в геодезической системе ``WGS84``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: Возвращает номер добавленной точки в подобъекте с 1 При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendPointGeoWGS84_t (_hobj, _b, _l, _subject)

    mapAppendPointGeoWGS843D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendPointGeoWGS843D', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapAppendPointGeoWGS843D(_hobj: maptype.HOBJ, _b: float, _l: float, _h: float, _subject: int) -> int:
        """
        Добавить в конец метрики объекта точку
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _b: широта точки в радианах в геодезической системе ``WGS84``
        
        :param _l: долгота точки в радианах в геодезической системе ``WGS84``
        
        :param _h: нормальная или ортометрическая высота в точке (записывается без преобразований) или относительная высота
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Тип высоты определяется функциями mapGetHeightType и mapSetHeightType
        
        :returns: Возвращает номер добавленной точки в подобъекте с 1 При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendPointGeoWGS843D_t (_hobj, _b, _l, _h, _subject)

    mapInsertPointGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapInsertPointGeo', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapInsertPointGeo(_hobj: maptype.HOBJ, _b: float, _l: float, _number: int, _subject: int) -> int:
        """
        Вставить в метрику объекта точку
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _b: широта точки в радианах в геодезической системе координат документа
        
        :param _l: долгота точки в радианах в геодезической системе координат документа
        
        :param _number: номер точки c ``0``, за которой будет добавлена новая точка
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Для изменения координаты Н необходимо далее выполнить функцию HPlane()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapInsertPointGeo_t (_hobj, _b, _l, _number, _subject)

    mapUpdatePointGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdatePointGeo', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapUpdatePointGeo(_hobj: maptype.HOBJ, _b: float, _l: float, _number: int, _subject: int) -> int:
        """
        Изменить координаты точки метрики
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _b: широта точки в радианах в геодезической системе координат документа
        
        :param _l: долгота точки в радианах в геодезической системе координат документа
        
        :param _number: номер обновляемой точки c ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdatePointGeo_t (_hobj, _b, _l, _number, _subject)

    mapUpdatePointGeo3D_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdatePointGeo3D', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapUpdatePointGeo3D(_hobj: maptype.HOBJ, _b: float, _l: float, _h: float, _number: int, _subject: int) -> int:
        """
        Изменить координаты точки метрики
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _b: широта точки в радианах в геодезической системе координат документа
        
        :param _l: долгота точки в радианах в геодезической системе координат документа
        
        :param _h: нормальная или ортометрическая высота в точке (записывается без преобразований) или относительная высота Тип высоты определяется функциями mapGetHeightType и mapSetHeightType
        
        :param _number: номер обновляемой точки c ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdatePointGeo3D_t (_hobj, _b, _l, _h, _number, _subject)

    mapUpdatePointPlaneInMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdatePointPlaneInMap', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapUpdatePointPlaneInMap(_hobj: maptype.HOBJ, _x: float, _y: float, _number: int, _subject: int) -> int:
        """
        Изменить координаты общей точки метрики у объекта и у всех объектов карты, имеющих такую точку
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _x: координата x (на север) точки в метрах в системе координат документа
        
        :param _y: координата y (на восток) точки в метрах в системе координат документа
        
        :param _number: номер точки c ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Изменение выполняется после вызова mapCommitObject() или mapCommitWithPlace()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdatePointPlaneInMap_t (_hobj, _x, _y, _number, _subject)

    mapUpdatePointPlane3DInMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdatePointPlane3DInMap', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapUpdatePointPlane3DInMap(_hobj: maptype.HOBJ, _x: float, _y: float, _h: float, _number: int, _subject: int) -> int:
        """
        Изменить координаты общей точки метрики у объекта и у всех объектов карты, имеющих такую точку
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _x: координата x (на север) точки в метрах в системе координат документа
        
        :param _y: координата y (на восток) точки в метрах в системе координат документа
        
        :param _h: нормальная или ортометрическая высота в точке (записывается без преобразований) или относительная высота Тип высоты определяется функциями mapGetHeightType и mapSetHeightType
        
        :param _number: номер точки c ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Изменение выполняется после вызова mapCommitObject() или mapCommitWithPlace()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdatePointPlane3DInMap_t (_hobj, _x, _y, _h, _number, _subject)

    mapUpdatePointPlaneInLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdatePointPlaneInLayer', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapUpdatePointPlaneInLayer(_hobj: maptype.HOBJ, _x: float, _y: float, _number: int, _subject: int) -> int:
        """
        Изменить координаты общей точки у объекта и у всех объектов общего слоя, имеющих такую точку
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _x: координата x (на север) точки в метрах в системе координат документа
        
        :param _y: координата y (на восток) точки в метрах в системе координат документа
        
        :param _number: номер точки c ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Изменение выполняется после вызова mapCommitObject() или mapCommitWithPlace()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdatePointPlaneInLayer_t (_hobj, _x, _y, _number, _subject)

    mapUpdatePointPlane3DInLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdatePointPlane3DInLayer', maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapUpdatePointPlane3DInLayer(_hobj: maptype.HOBJ, _x: float, _y: float, _h: float, _number: int, _subject: int) -> int:
        """
        Изменить координаты общей точки у объекта и у всех объектов общего слоя, имеющих такую точку
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _x: координата x (на север) точки в метрах в системе координат документа
        
        :param _y: координата y (на восток) точки в метрах в системе координат документа
        
        :param _h: нормальная или ортометрическая высота в точке (записывается без преобразований) или относительная высота Тип высоты определяется функциями mapGetHeightType и mapSetHeightType
        
        :param _number: номер точки c ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Изменение выполняется после вызова mapCommitObject() или mapCommitWithPlace()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdatePointPlane3DInLayer_t (_hobj, _x, _y, _h, _number, _subject)

    mapSetXPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetXPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapSetXPlane(_hobj: maptype.HOBJ, _x: float, _number: int, _subject: int) -> int:
        """
        Редактирование координаты точки объекта/подобъекта в прямоугольной системе в метрах на местности
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _x: координата x (на север) точки в метрах в системе координат документа
        
        :param _number: номер точки c ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetXPlane_t (_hobj, _x, _number, _subject)

    mapSetYPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetYPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapSetYPlane(_hobj: maptype.HOBJ, _y: float, _number: int, _subject: int) -> int:
        """
        Редактирование координаты точки объекта/подобъекта в прямоугольной системе в метрах на местности
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _y: координата y (на восток) точки в метрах в системе координат документа
        
        :param _number: номер точки c ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetYPlane_t (_hobj, _y, _number, _subject)

    mapSetHPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetHPlane', maptype.HOBJ, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapSetHPlane(_hobj: maptype.HOBJ, _h: float, _number: int, _subject: int) -> int:
        """
        Редактирование высоты точки объекта/подобъекта в метрах
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _h: нормальная или ортометрическая высота в точке (записывается без преобразований) или относительная высота Тип высоты определяется функциями mapGetHeightType и mapSetHeightType
        
        :param _number: номер точки c ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Тип высоты может быть запрошен функцией mapGetHeightType Система высот устанавливается в паспорте карты (``HEIGHTSYSTEM``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если объект имел двухмерную метрику (mapIsObject3D() =``= 0``), то будет изменен формат записи с установкой значения высоты ERRORHEIGHT
        """
        return mapSetHPlane_t (_hobj, _h, _number, _subject)

    mapSetMValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMValue', maptype.HOBJ, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapSetMValue(_hobj: maptype.HOBJ, _m: float, _number: int, _subject: int) -> int:
        """
        Изменить измерение (свойство) точки метрики
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _m: измерение в формате double (для типа метрики ``IDDOUBLE4``)
        
        :param _number: номер точки c ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMValue_t (_hobj, _m, _number, _subject)

    mapSetFValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetFValue', maptype.HOBJ, ctypes.c_int64, ctypes.c_long, ctypes.c_long)
    def mapSetFValue(_hobj: maptype.HOBJ, _f: int, _number: int, _subject: int) -> int:
        """
        Изменить измерение (свойство) точки метрики
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _f: измерение в формате __int64 (для типа метрики ``IDDOUBLE4F``)
        
        :param _number: номер точки c ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetFValue_t (_hobj, _f, _number, _subject)

    mapCreateSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateSubject', maptype.HOBJ)
    def mapCreateSubject(_hobj: maptype.HOBJ) -> int:
        """
        Создать пустой подобъект в конце записи метрики
        
        :param _hobj: идентификатор объекта карты в памяти В конец записи добавляется дескриптор подобъекта с нулевым числом точек
        
        :returns: Возвращает номер созданного подобъекта При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если предыдущий подобъект не содержит ни одной точки, то новый подобъект не будет создан
        """
        return mapCreateSubject_t (_hobj)

    mapDeleteSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteSubject', maptype.HOBJ, ctypes.c_long)
    def mapDeleteSubject(_hobj: maptype.HOBJ, _subject: int) -> int:
        """
        Удалить подобъект в записи метрики
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки, если равен (-``1``), то удаляется вся метрика объекта вместе с подобъектами Текущей становится первая точка объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteSubject_t (_hobj, _subject)

    mapDeleteMultiSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteMultiSubject', maptype.HOBJ, ctypes.c_long)
    def mapDeleteMultiSubject(_hobj: maptype.HOBJ, _subject: int) -> int:
        """
        Удалить подобъект - главный контур из указанной записи и его подобъекты
        
        :param _hobj: идентификатор объекта карты в памяти number - номер подобъекта, который является внешним контуром (запросить число внешних конутров - mapGetMultiSubjectNumber())
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteMultiSubject_t (_hobj, _subject)

    mapAppendSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendSubject', maptype.HOBJ, maptype.HOBJ, ctypes.c_long)
    def mapAppendSubject(_hobj: maptype.HOBJ, _hsource: maptype.HOBJ, _subject: int) -> int:
        """
        Добавить подобъект из указанной записи в конец метрики
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _hsource: идентификатор объекта карты в памяти, из которого добавляют подобъет
        
        :param _subject: номер добавляемого подобъекта или -``1`` (добавить все подобъекты)
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapAppendSubject_t (_hobj, _hsource, _subject)

    mapRelocateObjectPlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRelocateObjectPlane', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapRelocateObjectPlane(_hobj: maptype.HOBJ, _delta: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Сместить все координаты метрики объекта на заданную величину
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _delta: смещение в метрах в системе координат карты на север (delta->X) и на восток (delta->Y)
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapRelocateObjectPlane_t (_hobj, _delta)

    mapChangeSubjectDirect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapChangeSubjectDirect', maptype.HOBJ, ctypes.c_long)
    def mapChangeSubjectDirect(_hobj: maptype.HOBJ, _subject: int) -> int:
        """
        Изменить направление цифрования подобъекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Порядок точек заданного контура от первой до последней меняется на обратный Для полигона направление цифрование внутренних контуров обычно противоположно направлению внешнего контура
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapChangeSubjectDirect_t (_hobj, _subject)

    mapChangeObjectDirect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapChangeObjectDirect', maptype.HOBJ)
    def mapChangeObjectDirect(_hobj: maptype.HOBJ) -> int:
        """
        Изменить направление цифрования объекта
        
        :param _hobj: идентификатор объекта карты в памяти Порядок точек всех контуров объекта от первой до последней меняется на обратный в пределах каждого контура Для полигона направление цифрование внутренних контуров обычно противоположно направлению внешнего контура
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapChangeObjectDirect_t (_hobj)

    mapCorrectPolygonDirect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCorrectPolygonDirect', maptype.HOBJ)
    def mapCorrectPolygonDirect(_hobj: maptype.HOBJ) -> int:
        """
        Проверить и исправить направление цифрования контуров площадного объекта (полигона)
        
        :param _hobj: идентификатор объекта карты в памяти Направление цифрования внешних контуров полигона сравнивается со значением, заданным в классификаторе ``RSC``: ``OD_LEFT``, ``OD_RIGHT`` При иных значениях (``OD_NONE``, ...) и для графических объектов устанавливается ``OD_LEFT`` (объект слева - против часовой стрелки)
        
        :returns: Возвращает установленное направление цифрования для внешних контуров При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если выбрано значение OD_LEFT, то направление внешних контуров
           устанавливается равным OD_LEFT, а внутренних - OD_RIGHT
        """
        return mapCorrectPolygonDirect_t (_hobj)

    mapSetFirstPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetFirstPoint', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSetFirstPoint(_hobj: maptype.HOBJ, _number: int, _subject: int) -> int:
        """
        Установить в метрике объекта или подобъекта полигона первой заданную точку
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: номер точки c ``1``, которая будет первой
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Выполняется циклический сдвиг точек, не меняя их последовательности в контуре
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetFirstPoint_t (_hobj, _number, _subject)

    mapLinearFilter_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLinearFilter', maptype.HOBJ, ctypes.c_double)
    def mapLinearFilter(_hobj: maptype.HOBJ, _precision: float) -> int:
        """
        Выполнить линейную фильтрацию точек метрики
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _precision: минимальное расстояние в метрах от точки до прямой, соединяющей предыдущую и следующую точки При линейной фильтрации метрики удаляются: - двойные точки метрики, - незамкнутые подобъекты ``< 2`` точек, - замкнутые подобъекты ``< 4`` точек, - точки метрики, лежащие в середине отрезка прямой на расстоянии precision от прямой. Объект не удаляется никогда
        
        :returns: Возвращает общее число точек метрики При ошибках возвращает: ``0`` - ошибка структуры -``1`` - объект состоит из одной точки -``2`` - объект состоит из двух одинаковых точек -``3`` - число точек замкнутого контура объекта равно 3 -``10`` - число точек метрики превышает длину записи метрики
        :rtype: int
        """
        return mapLinearFilter_t (_hobj, _precision)

    mapGeneralFilter_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGeneralFilter', maptype.HMAP, maptype.HOBJ, ctypes.c_double)
    def mapGeneralFilter(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _precision: float) -> int:
        """
        Выполнить фильтрацию точек объекта с учетом топологических связей с соседними объектами
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _precision: точность в метрах на местности (минимальное расстояние от точки до прямой, соединяющей предыдущую и следующую точки) При фильтрации объекта будут фильтроваться на той же карте и соседние объекты, имеющие общие точки, для сохранения общих точек контуров Концевые общие точки не фильтруются
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGeneralFilter_t (_hmap, _hobj, _precision)

    mapGeneralFilterInMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGeneralFilterInMap', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_double, maptype.HMESSAGE)
    def mapGeneralFilterInMap(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _precision: float, _hwnd: maptype.HMESSAGE) -> int:
        """
        Выполнить фильтрацию точек всех объектов на заданной карте с учетом топологических связей с соседними объектами
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в документе, для фоновой карты равен hmap
        
        :param _list: номер листа для многолистовой карты или ``1``
        
        :param _precision: минимальное расстояние в метрах от точки до прямой, соединяющей предыдущую и следующую точки
        
        :param _hwnd: идентификатор обработчика, которое будут отправляться сообщения, или ``0`` Процесс отправляет сообщение ``WM_PROGRESSBARUN``: wparm - процент обработки, Для прерывания процесса из обработчика сообщения нужно вернуть ``WM_PROGRESSBARUN``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGeneralFilterInMap_t (_hmap, _hsite, _list, _precision, _hwnd)

    mapGeneralDuplicatePointFilter_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGeneralDuplicatePointFilter', maptype.HMAP, maptype.HOBJ, ctypes.c_double)
    def mapGeneralDuplicatePointFilter(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _precision: float) -> int:
        """
        Выполнить фильтрацию двойных точек с учетом топологических связей с соседними объектами
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _precision: минимальное расстояние между точками в метрах для определения двойных точек
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGeneralDuplicatePointFilter_t (_hmap, _hobj, _precision)

    mapObjectGeneralization_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectGeneralization', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapObjectGeneralization(_hobj: maptype.HOBJ, _scale: int, _force: int) -> int:
        """
        Выполнить генерализацию метрики линейного или площадного объекта для выбранного масштаба
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _scale: масштаб генерализации метрики (``1: 100 000`` соответствует сетке с шагом ``100`` м на местности и ``1`` мм на изображении)
        
        :param _force: признак формирования минимальной метрики при вырождении Выполняет фильтрацию метрики объекта с подбором точности для заданного масштаба изображения При сжатии изображения точки на изображении будут совмещаться и выстраиваться на одной линии, что позволяет их исключить без нарушения вида контура на данном масштабе
        
        :returns: Возвращает: ``1`` - метрика генерализирована успешно ``2`` - метрика не изменилась (исходные точки достаточно разряжены для заданного масштаба) -``1`` - метрика не изменилась (объект вырождается или максимальное число точек подобъектов меньше 64) При ошибке возвращает ноль
        :rtype: int
        """
        return mapObjectGeneralization_t (_hobj, _scale, _force)

    mapSetGeneralizationGridStep_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSetGeneralizationGridStep', ctypes.c_double)
    def mapSetGeneralizationGridStep(_step: float) -> float:
        """
        Установить шаг сетки в мм для генерализации контуров объектов в масштабе карты
        
        :param _step: точность генерализации в мм - минимальное расстояние на изображении от точки до прямой, соединяющей предыдущую и следующую точки Применяется для управления степенью генерализации метрики объектов
        
        :returns: Возвращает установленное значение
        :rtype: float
        """
        return mapSetGeneralizationGridStep_t (_step)

    mapGetGeneralizationGridStep_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetGeneralizationGridStep')
    def mapGetGeneralizationGridStep() -> float:
        """
        Запросить шаг сетки в мм для генерализации контуров объектов в масштабе карты
        
        :returns: Возвращает установленное значение
        :rtype: float
        """
        return mapGetGeneralizationGridStep_t ()

    mapCashionSpline_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCashionSpline', maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_double)
    def mapCashionSpline(_hobj: maptype.HOBJ, _cashion: int, _smooth: int, _precision: float) -> int:
        """
        Построить сглаживающий сплайн по координатам объекта и всех его подобъектов
        
        :param _hobj: исходная метрика объекта, по которому строится сплайн
        
        :param _cashion: условный процент спиливания углов ломаной линии объекта (``1``<= cashion <``= 50``) (метрика исходного объекта/подобъекта) Чем больше cashion, тем больше спиливается угол
        
        :param _smooth: плавность кривой сплайна (число точек между узлами объекта smooth >``= 3``) Чем больше smooth, тем более гладкой смотрится линия
        
        :param _precision: порог (точность) при фильтрации точек, для автоматического определения точности установить значение ``"-1"`` Это сплайн, который проходит только через первую и последнюю точки объекта (подобъекта) и как бы сглаживает (спиливает) углы ломаной, соединяющей точки объекта (метрику исходного объекта/подобъекта)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если исходный объект имел 3-ю координату (высоту), то у сплайна также есть высота (интерполяция для новых точек)
        """
        return mapCashionSpline_t (_hobj, _cashion, _smooth, _precision)

    mapCashionSplineSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCashionSplineSubject', maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_double)
    def mapCashionSplineSubject(_hobj: maptype.HOBJ, _subject: int, _cashion: int, _smooth: int, _precision: float) -> int:
        """
        Построить сглаживающий сплайн по координатам заданного подобъекта
        
        :param _hobj: исходная метрика объекта, по подобъекту которого строится сплайн
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :param _cashion: условный процент спиливания углов ломаной линии объекта (``1``<= cashion <``= 50``) Чем больше cashion, тем больше спиливается угол
        
        :param _smooth: плавность кривой сплайна (число точек между узлами подобъекта smooth >``= 3``) Чем больше smooth, тем более гладкой смотрится линия
        
        :param _precision: порог (точность) при фильтрации точек, для автоматического определения точности установить значение ``"-1"`` Это сплайн, который проходит только через первую и последнюю точки подобъекта и как бы сглаживает (спиливает) углы ломаной, соединяющей точки объекта (метрику исходного подобъекта)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если исходный подобъект имел 3-ю координату (высоту), то у сплайна также есть высота
        """
        return mapCashionSplineSubject_t (_hobj, _subject, _cashion, _smooth, _precision)

    mapBendSpline_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBendSpline', maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_double)
    def mapBendSpline(_hobj: maptype.HOBJ, _press: int, _smooth: int, _precision: float) -> int:
        """
        Построить огибающий сплайн для объекта и всех его подобъектов
        
        :param _hobj: исходная метрика объекта, по которому строится сплайн
        
        :param _press: максимальная амплитуда отхода кривой сплайна от отрезка в процентах от длины отрезка ( >``= 5`` ) Чем больше press, тем более сплайн может удаляться от отрезка ломаной (метрики исходного объекта/подобъекта).
        
        :param _smooth: плавность кривой сплайна (число точек между узлами объекта smooth >``= 3``) Чем больше smooth, тем более гладкой смотрится линия
        
        :param _precision: порог (точность) при фильтрации точек, для автоматического определения точности установить значение ``"-1"`` Это сплайн, который проходит через все точки исходного объекта по гладкой кривой заданной амплитуды
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если исходный объект имел 3-ю координату (высоту), то у сплайна также есть высота (интерполяция для новых точек)
        """
        return mapBendSpline_t (_hobj, _press, _smooth, _precision)

    mapBendSplineSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBendSplineSubject', maptype.HOBJ, ctypes.c_int, ctypes.c_long, ctypes.c_long, ctypes.c_double)
    def mapBendSplineSubject(_hobj: maptype.HOBJ, _subject: int, _press: int, _smooth: int, _precision: float) -> int:
        """
        Построить огибающий сплайн для заданного подобъекта
        
        :param _hobj: исходная метрика объекта, по которому строится сплайн
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :param _press: максимальная амплитуда отхода кривой сплайна от отрезка в процентах от длины отрезка ( >``= 5`` ) Чем больше press, тем более сплайн может удаляться от отрезка ломаной (метрики исходного объекта/подобъекта)
        
        :param _smooth: плавность кривой сплайна (число точек между узлами объекта smooth >``= 3``) Чем больше smooth, тем более гладкой смотрится линия
        
        :param _precision: порог (точность) при фильтрации точек Это сплайн, который проходит через все точки исходного объекта по гладкой кривой заданной амплитуды
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если исходный подобъект имел 3-ю координату (высоту), то у сплайна также есть высота
        """
        return mapBendSplineSubject_t (_hobj, _subject, _press, _smooth, _precision)

    mapGeneralBendSpline_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGeneralBendSpline', maptype.HMAP, maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.c_double)
    def mapGeneralBendSpline(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _press: int, _smooth: int, _adjustdist: float, _filterprec: float) -> int:
        """
        Построить огибающий сплайн для объекта и подобъектов с учетом топологических связей с соседними объектами
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: фильтруемый объект
        
        :param _press: максимальная амплитуда отхода кривой сплайна от отрезка в процентах от длины отрезка (>``= 5``), чем больше press, тем больше сплайн может оклоняться от исходного контура
        
        :param _smooth: плавность кривой сплайна (>``= 3``) число точек между узлами объекта, чем больше smooth, тем более гладким будет сплайн
        
        :param _adjustdist: допуск согласования - максимальное расстояние, при котором две соседние точки считаются расположенными на одном месте
        
        :param _filterprec: уровень фильтрации (минимальное расстояние от точки до прямой, соединяющей предыдущую и следующую точки)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGeneralBendSpline_t (_hmap, _hobj, _press, _smooth, _adjustdist, _filterprec)

    mapSmoothingSpline1_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSmoothingSpline1', ctypes.POINTER(ctypes.c_double), ctypes.c_long, ctypes.c_double)
    def mapSmoothingSpline1(_points: ctypes.POINTER(ctypes.c_double), _count: int, _smooth: float) -> int:
        """
        Построить одномерный сглаживающий сплайн
        
        :param _points: массив точек, содержащих одну координату
        
        :param _count: количество точек
        
        :param _smooth: уровень сглаживания от ``0.0`` до ``1.0``, где: ``0`` - прямая линия, ``1`` - кубический сплайн
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSmoothingSpline1_t (_points, _count, _smooth)

    mapSmoothingSpline2_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSmoothingSpline2', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.c_double)
    def mapSmoothingSpline2(_points: ctypes.POINTER(maptype.DOUBLEPOINT), _count: int, _smooth: float) -> int:
        """
        Построить двухмерный сглаживающий сплайн
        
        :param _points: массив точек (x, y)
        
        :param _count: количество точек
        
        :param _smooth: уровень сглаживания от ``0.0`` до ``1.0``, где: ``0`` - прямая линия, ``1`` - кубический сплайн
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSmoothingSpline2_t (_points, _count, _smooth)

    mapSmoothingSpline3_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSmoothingSpline3', ctypes.POINTER(maptype.XYHDOUBLE), ctypes.c_long, ctypes.c_double)
    def mapSmoothingSpline3(_points: ctypes.POINTER(maptype.XYHDOUBLE), _count: int, _smooth: float) -> int:
        """
        Построить трёхмерный сглаживающий сплайн
        
        :param _points: массив точек (x, y, h)
        
        :param _count: количество точек
        
        :param _smooth: уровень сглаживания от ``0.0`` до ``1.0``, где: ``0`` - прямая линия, ``1`` - кубический сплайн
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSmoothingSpline3_t (_points, _count, _smooth)

    mapSmoothingSplineSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSmoothingSplineSubject', maptype.HOBJ, ctypes.c_long, ctypes.c_double)
    def mapSmoothingSplineSubject(_hobj: maptype.HOBJ, _subject: int, _smooth: float) -> int:
        """
        Построить сглаживающий сплайн подобъекта (2-х или 3-х мерный в зависимости от наличия высоты)
        
        :param _hobj: сглаживаемый объект
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :param _smooth: уровень сглаживания от ``0.0`` до ``1.0``, где: ``0`` - прямая линия, ``1`` - кубический сплайн
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSmoothingSplineSubject_t (_hobj, _subject, _smooth)

    mapSmoothingSplineObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSmoothingSplineObject', maptype.HOBJ, ctypes.c_double)
    def mapSmoothingSplineObject(_hobj: maptype.HOBJ, _smooth: float) -> int:
        """
        Построить сглаживающий сплайн всего объекта (2-х или 3-х мерный в зависимости от наличия высоты)
        
        :param _hobj: сглаживаемый объект
        
        :param _smooth: уровень сглаживания от ``0.0`` до ``1.0``, где: ``0`` - прямая линия, ``1`` - кубический сплайн
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSmoothingSplineObject_t (_hobj, _smooth)

    mapCreateArc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateArc', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double)
    def mapCreateArc(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _first: ctypes.POINTER(maptype.DOUBLEPOINT), _center: ctypes.POINTER(maptype.DOUBLEPOINT), _last: ctypes.POINTER(maptype.DOUBLEPOINT), _radius: float) -> int:
        """
        Построить дугу по часовой стрелке заданного радиуса с заданным центром
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти, в который запишется дуга
        
        :param _first: координаты первой точки дуги в метрах
        
        :param _center: координаты центра дуги в метрах
        
        :param _last: координаты последней точки дуги в метрах
        
        :param _radius: радиус дуги в метрах Координаты дуги заполняются в метрах в системе исходного документа Применяется для коротких радиусов в пределах километров
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCreateArc_t (_hmap, _hobj, _first, _center, _last, _radius)

    mapCreateGeoArc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateGeoArc', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double)
    def mapCreateGeoArc(_hobj: maptype.HOBJ, _first: ctypes.POINTER(maptype.DOUBLEPOINT), _center: ctypes.POINTER(maptype.DOUBLEPOINT), _last: ctypes.POINTER(maptype.DOUBLEPOINT), _step: float) -> int:
        """
        Построить геодезическую дугу по часовой стрелке заданного радиуса с заданным центром
        
        :param _hobj: идентификатор объекта карты в памяти, в который запишется дуга
        
        :param _first: координаты первой точки дуги в радианах ``WGS84``
        
        :param _center: координаты центра дуги в радианах ``WGS84``
        
        :param _last: координаты последней точки дуги в радианах ``WGS84``
        
        :param _step: шаг дуги в градусах (угловой интервал между точками) Применяется для больших радиусов порядка десятков километров и более Радиус определяется по расстоянию до первой точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCreateGeoArc_t (_hobj, _first, _center, _last, _step)

    mapCreateGeoArcByAngle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateGeoArcByAngle', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    def mapCreateGeoArcByAngle(_hobj: maptype.HOBJ, _center: ctypes.POINTER(maptype.DOUBLEPOINT), _startangle: float, _endangle: float, _radius: float, _step: float) -> int:
        """
        Построить геодезическую дугу по часовой стрелке заданного радиуса с заданным центром
        
        :param _hobj: идентификатор объекта карты в памяти, в который запишется дуга
        
        :param _center: координаты центра дуги в радианах ``WGS84``
        
        :param _startangle: истинный азимут на первую точку дуги в радианах
        
        :param _endangle: истинный азимут на последнюю точку дуги в радианах
        
        :param _radius: радиус дуги в метрах
        
        :param _step: шаг дуги в градусах (угловой интервал между точками) Применяется для больших радиусов порядка десятков километров и более
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCreateGeoArcByAngle_t (_hobj, _center, _startangle, _endangle, _radius, _step)

    mapCreateArcByPoints_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateArcByPoints', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapCreateArcByPoints(_hobj: maptype.HOBJ, _first: ctypes.POINTER(maptype.DOUBLEPOINT), _middle: ctypes.POINTER(maptype.DOUBLEPOINT), _last: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Построить дугу заданного радиуса по трем точкам дуги в метрах
        
        :param _hobj: идентификатор объекта карты в памяти, в который запишется дуга
        
        :param _first: координаты первой точки дуги в метрах
        
        :param _middle: координаты промежуточной точки дуги в метрах
        
        :param _last: координаты последней точки дуги в метрах Координаты дуги заполняются в метрах в системе исходного документа Применяется для коротких радиусов в пределах километров
        
        :returns: При ошибке возвращает ноль-
        :rtype: int
        """
        return mapCreateArcByPoints_t (_hobj, _first, _middle, _last)

    mapZoneObjectWithFilter_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapZoneObjectWithFilter', ctypes.c_double, maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_double)
    def mapZoneObjectWithFilter(_radius: float, _hobj: maptype.HOBJ, _subject: int, _form: int, _arcdist: float, _cornerfactor: float, _side: int, _filterprec: float) -> int:
        """
        Построить зону вокруг подобъекта с фильтрацией
        
        :param _radius: радиус создаваемой зоны в метрах на местности
        
        :param _hobj: идентификатор копии объекта, по метрике которого строится зона В этот объект будет записана метрика построенной зоны
        
        :param _subject: номер объекта (``0``) или подобъекта (больше ``0``) или -``1`` - построить зону вокруг всех контуров
        
        :param _form: тип угла: ``0`` - прямой, ``1`` - закругленный
        
        :param _arcdist: расстояние между точками по дуге (в метрах на местности), рекомендуется radius / ``15``
        
        :param _cornerfactor: коэффициент для расчета максимальной длины угла, рекомендуется ``3``
        
        :param _side: направление построения зоны: ``1``-справа, ``2``-слева, ``3``-с обеих сторон, ``4``-внешняя для полигонов, ``5``-внутренняя для полигонов
        
        :param _filterprec: уровень фильтрации для построенной зоны: минимальное расстояние в метрах от точки до прямой, соединяющей предыдущую и следующую точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если задан прямой тип угла, то внешний угол обрезается по расстоянию от узла по
           допуску radius * cornerfactor для устранения длинных углов
        """
        return mapZoneObjectWithFilter_t (_radius, _hobj, _subject, _form, _arcdist, _cornerfactor, _side, _filterprec)

    mapZoneObjectEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapZoneObjectEx', ctypes.c_double, maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapZoneObjectEx(_radius: float, _hobj: maptype.HOBJ, _subject: int, _form: int, _arcdist: float, _cornerfactor: float, _side: int) -> int:
        """
        Построить зону вокруг подобъекта
        
        :param _radius: радиус создаваемой зоны в метрах на местности
        
        :param _hobj: идентификатор копии объекта, по метрике которого строится зона В этот объект будет записана метрика построенной зоны
        
        :param _subject: номер объекта (``0``) или подобъекта (больше ``0``) или -``1`` - построить зону вокруг всех контуров
        
        :param _form: тип угла: ``0`` - прямой, ``1`` - закругленный
        
        :param _arcdist: расстояние между точками по дуге (в метрах на местности), рекомендуется radius / ``15``
        
        :param _cornerfactor: коэффициент для расчета максимальной длины угла, рекомендуется ``3``
        
        :param _side: направление построения зоны: ``1``-справа, ``2``-слева, ``3``-с обеих сторон, ``4``-внешняя для полигонов, ``5``-внутренняя для полигонов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если задан прямой тип угла, то внешний угол обрезается по расстоянию от узла по
           допуску radius * cornerfactor для устранения длинных углов
        """
        return mapZoneObjectEx_t (_radius, _hobj, _subject, _form, _arcdist, _cornerfactor, _side)

    mapZoneObjectWithFilterEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapZoneObjectWithFilterEx', ctypes.c_double, maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_double, ctypes.c_long)
    def mapZoneObjectWithFilterEx(_radius: float, _hobj: maptype.HOBJ, _subject: int, _form: int, _arcdist: float, _cornerfactor: float, _side: int, _filterprec: float, _calcinmap: int) -> int:
        """
        Построить зону снаружи подобъекта
        
        :param _radius: радиус создаваемой зоны в метрах на местности
        
        :param _hobj: идентификатор копии объекта, по метрике которого строится зона. В этот объект будет записана метрика построенной зоны.
        
        :param _subject: номер объекта (``0``) или подобъекта (больше ``0``) или -``1`` - построить зону вокруг всех контуров
        
        :param _form: тип угла: ``0`` - прямой, ``1`` - закругленный
        
        :param _arcdist: расстояние между точками по дуге (в метрах на местности), рекомендуется radius / ``15``
        
        :param _cornerfactor: коэффициент для расчета максимальной длины угла, рекомендуется ``3``
        
        :param _side: направление построения зоны: ``1``-справа, ``2``-слева, ``3``-с обеих сторон, ``4``-внешняя для полигонов, ``5``-внутренняя для полигонов
        
        :param _filterprec: уровень фильтрации для построенной зоны: минимальное расстояние в метрах от точки до прямой, соединяющей предыдущую и следующую точки
        
        :param _calcinmap: признак выполнения расчетов в системе карты (``0``/``1``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если тип угла прямой, то внешний угол обрезается по расстоянию от узла по
           допуску radius*cornerfactor для устранения длинных углов
        """
        return mapZoneObjectWithFilterEx_t (_radius, _hobj, _subject, _form, _arcdist, _cornerfactor, _side, _filterprec, _calcinmap)

    mapInsideZoneObjectWithFilterEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapInsideZoneObjectWithFilterEx', ctypes.c_double, maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapInsideZoneObjectWithFilterEx(_radius: float, _hobj: maptype.HOBJ, _subject: int, _form: int, _arcdist: float, _cornerfactor: float, _filterprec: float, _calcinmap: int) -> int:
        """
        Построить зону внутри подобъекта
        
        :param _radius: радиус создаваемой зоны в метрах на местности
        
        :param _hobj: идентификатор копии объекта, по метрике которого строится зона. В этот объект будет записана метрика построенной зоны.
        
        :param _subject: номер объекта (``0``) или подобъекта (больше ``0``) или -``1`` - построить зону вокруг всех контуров
        
        :param _form: тип угла: ``0`` - прямой, ``1`` - закругленный
        
        :param _arcdist: расстояние между точками по дуге (в метрах на местности), рекомендуется radius / ``15``
        
        :param _cornerfactor: коэффициент для расчета максимальной длины угла, рекомендуется ``3`` side    - направление построения зоны: ``1``-справа, ``2``-слева, ``3``-с обеих сторон, ``4``-внешняя для полигонов, ``5``-внутренняя для полигонов
        
        :param _filterprec: уровень фильтрации для построенной зоны: минимальное расстояние в метрах от точки до прямой, соединяющей предыдущую и следующую точки
        
        :param _calcinmap: признак выполнения расчетов в системе карты (``0``/``1``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если тип угла прямой, то внешний угол обрезается по расстоянию от узла по
           допуску radius*cornerfactor для устранения длинных углов
        """
        return mapInsideZoneObjectWithFilterEx_t (_radius, _hobj, _subject, _form, _arcdist, _cornerfactor, _filterprec, _calcinmap)

    mapHalfZoneObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapHalfZoneObject', ctypes.c_double, maptype.HOBJ, ctypes.c_long)
    def mapHalfZoneObject(_radius: float, _hobj: maptype.HOBJ, _subject: int) -> int:
        """
        Построить половину зоны вокруг заданного подобъекта
        
        :param _radius: радиус создаваемой зоны (в метрах на местности)
        
        :param _hobj: метрика объекта, по которому строится зона
        
        :param _subject: номер подобъекта с ``0``, вокруг которого строим зону Зона строится справа от объекта по направлению цифрования
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapHalfZoneObject_t (_radius, _hobj, _subject)

    mapOffsetLineEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapOffsetLineEx', maptype.HOBJ, ctypes.c_long, ctypes.c_double, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapOffsetLineEx(_hobj: maptype.HOBJ, _subject: int, _radius: float, _form: int, _arcdist: float, _cornerfactor: float, _calcinmap: int) -> int:
        """
        Построить линейный объект, смещенный относительно заданного линейного подобъекта
        
        :param _hobj: идентификатор линейного объекта, относительно которого строится смещенная линия В этот же объект будет записана метрика смещенной линии вместо всей исходной метрики
        
        :param _subject: номер подобъекта, относительно которого строится смещенная линия
        
        :param _radius: смещение создаваемой зоны в метрах на местности ``> 0`` - смещение вправо, ``< 0`` - смещение влево
        
        :param _form: тип угла: ``0`` - прямой, ``1`` - закругленный
        
        :param _arcdist: расстояние между точками по дуге для закругленного угла в метрах на местности, рекомендуется radius / ``15``
        
        :param _cornerfactor: коэффициент для расчета максимальной длины угла для прямого угла, рекомендуется ``3``
        
        :param _calcinmap: признак выполнения вычислений в системе карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если тип угла прямой, то внешний угол обрезается по расстоянию от узла
           по допуску radius*cornerfactor для устранения длинных углов
        """
        return mapOffsetLineEx_t (_hobj, _subject, _radius, _form, _arcdist, _cornerfactor, _calcinmap)

    mapBuildAxisLine_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBuildAxisLine', maptype.HMAP, maptype.HOBJ, maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapBuildAxisLine(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _haxis: maptype.HOBJ, _width: float, _length: float, _mode: int) -> int:
        """
        Построить осевую линию по площадному объекту
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: исходный площадной объект (простой или мультиполигон)
        
        :param _haxis: линейный объект для записи результата
        
        :param _width: минимальная ширина исходного объекта в метрах или ``0``
        
        :param _length: минимальная длина осевой линии или ``0``
        
        :param _mode: метод построения: ``1`` - построить по объекту произвольной формы ``2`` - построить по объекту в форме ленты ``0`` - использовать оба метода
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapBuildAxisLine_t (_hmap, _hobj, _haxis, _width, _length, _mode)

    mapWaterwayCreate_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapWaterwayCreate', maptype.HMAP, maptype.HOBJ, maptype.HOBJ, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapWaterwayCreate(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _axis: maptype.HOBJ, _width: float, _length: float, _mode: int) -> int:
        """
        Построить фарватер (средней линии) для полигона
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: исходный площадной объект, например - река, для которой строим фарватер haxis - объект, в метрику которого запишется результат - линейный объект c подобъектами
        
        :param _width: минимальная ширина исходного объекта в метрах или ``0``
        
        :param _length: минимальная длина участка фарватера или ``0``
        
        :param _mode: метод построения, равен ``0`` Для подобъектов hobj средняя линия не строится В объект haxis и его подобъекты записываются отрезки средней линии, построенные для участков реки шире width и длиной более length При width ``= 0`` и length ``= 0`` средняя линия строится по всему исходному объекту
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapWaterwayCreate_t (_hmap, _hobj, _axis, _width, _length, _mode)

    mapGetEndPointSetBeginPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetEndPointSetBeginPoint', maptype.HOBJ)
    def mapGetEndPointSetBeginPoint(_hobj: maptype.HOBJ) -> int:
        """
        Установить первую точку контура по вытянутости площадного объекта (полигона)
        
        :param _hobj: идентификатор объекта карты в памяти Выполняется сдвиг метрики на найденную по вытянутости первую точку полигона
        
        :returns: Возвращает номер ``"последней"`` точки в метрике объекта, выходящей на условную осевую линию При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetEndPointSetBeginPoint_t (_hobj)

    mapAbridge_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAbridge', maptype.HOBJ, ctypes.c_double)
    def mapAbridge(_hobj: maptype.HOBJ, _delta: float) -> int:
        """
        Замкнуть метрику объекта и всех его подобъектов для площадного или линейного объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _delta: порог замыкания в мм на карте в базовом масштабе или ``0``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если расстояние между первой и последней точкой меньше delta, то вместо последней точки пишем первую
           Если расстояние между первой и последней точкой больше delta, то после последней точки добавляем первую
        """
        return mapAbridge_t (_hobj, _delta)

    mapAbridgeSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAbridgeSubject', maptype.HOBJ, ctypes.c_long, ctypes.c_double)
    def mapAbridgeSubject(_hobj: maptype.HOBJ, _subject: int, _delta: float) -> int:
        """
        Замкнуть метрику подобъекта для площадного или линейного объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _delta: порог замыкания в мм на карте в базовом масштабе или ``0``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если расстояние между первой и последней точкой меньше delta, то вместо последней точки пишем первую
           Если расстояние между первой и последней точкой больше delta, то после последней точки добавляем первую
        """
        return mapAbridgeSubject_t (_hobj, _subject, _delta)

    mapRoundObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRoundObject', maptype.HOBJ)
    def mapRoundObject(_hobj: maptype.HOBJ) -> int:
        """
        Округлить метрику объекта по установленной точности карты (мм, см)
        
        :param _hobj: идентификатор объекта карты в памяти Точность карты запрашивается функцией mapGetSitePrecision()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapRoundObject_t (_hobj)

    mapOrthodrome_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapOrthodrome', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long)
    def mapOrthodrome(_first: ctypes.POINTER(maptype.DOUBLEPOINT), _second: ctypes.POINTER(maptype.DOUBLEPOINT), _array: ctypes.POINTER(maptype.DOUBLEPOINT), _count: int) -> int:
        """
        Построить ортодромию в виде массива точек
        
        :param _first: геодезические координаты первой точки в радианах на эллипсоиде документа
        
        :param _second: геодезические координаты второй точки в радианах на эллипсоиде документа
        
        :param _array: адрес массива для записи координат построенной ортодромии, размер массива в параметре count
        
        :param _count: количество точек для построения ортодромии (если точки размещены ближе ``0.000001`` радиан, заполняет только ``2`` точки) Ортодромия - это дуга между двумя точками на поверхности Земли по кратчайшему расстоянию При больших расстояниях точки дуги формируются с шагом не более ``0``,``5`` градуса, при малых растояниях - не чаще ``10`` километров, что обеспечивает определение длин и углов с точностью триангуляции ``1`` класса
        
        :returns: Возвращает заполненное число точек в массиве При ошибке возвращает ноль
        :rtype: int
        """
        return mapOrthodrome_t (_first, _second, _array, _count)

    mapOrthodromeObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapOrthodromeObject', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapOrthodromeObject(_hobj: maptype.HOBJ, _first: ctypes.POINTER(maptype.DOUBLEPOINT), _second: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Построить ортодромию в метрику объекта
        
        :param _hobj: идентификатор объекта карты в памяти, в метрику которого будет записан построенный контур
        
        :param _first: геодезические координаты первой точки в радианах на эллипсоиде документа
        
        :param _second: геодезические координаты второй точки в радианах на эллипсоиде документа Ортодромия - это дуга между двумя точками на поверхности Земли по кратчайшему расстоянию При больших расстояниях точки дуги формируются с шагом не более ``0``,``5`` градуса, при малых растояниях - не чаще ``10`` километров, что обеспечивает определение длин и углов с точностью триангуляции ``1`` класса
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapOrthodromeObject_t (_hobj, _first, _second)

    mapLoxodrome_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLoxodrome', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long)
    def mapLoxodrome(_first: ctypes.POINTER(maptype.DOUBLEPOINT), _second: ctypes.POINTER(maptype.DOUBLEPOINT), _array: ctypes.POINTER(maptype.DOUBLEPOINT), _count: int) -> int:
        """
        Построить локсодромию в виде массива точек
        
        :param _first: геодезические координаты первой точки в радианах на эллипсоиде документа
        
        :param _second: геодезические координаты второй точки в радианах на эллипсоиде документа
        
        :param _array: адрес массива для записи координат построенной локсодромии, размер массива в параметре count
        
        :param _count: количество точек для построения локсодромии Локсодромия - это кривая между двумя точками на поверхности Земли, пересекающая все меридианы под постоянным углом
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapLoxodrome_t (_first, _second, _array, _count)

    mapLoxodromeObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLoxodromeObject', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapLoxodromeObject(_hobj: maptype.HOBJ, _first: ctypes.POINTER(maptype.DOUBLEPOINT), _second: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Построить локсодромию в метрику объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _first: геодезические координаты первой точки в радианах на эллипсоиде документа
        
        :param _second: геодезические координаты второй точки в радианах на эллипсоиде документа Локсодромия - это кривая между двумя точками на поверхности Земли, пересекающая все меридианы под постоянным углом
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapLoxodromeObject_t (_hobj, _first, _second)

    mapBuildGeoPath_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBuildGeoPath', maptype.HOBJ, maptype.HOBJ, ctypes.c_double, ctypes.c_long)
    def mapBuildGeoPath(_sourceInfo: maptype.HOBJ, _destInfo: maptype.HOBJ, _step: float, _method: int) -> int:
        """
        Построить географическую линию (ортодромию или локсодромию)
        
        :param _sourceInfo: объект, содержащий точки исходных контуров
        
        :param _destInfo: объект для записи точех кривых, построенных по каждому отрезку объекта sourceInfo
        
        :param _step: шаг между точками в угловых секундах от ``0.001`` до ``3600`` (``1`` градус)
        
        :param _method: метод построения: ``0`` - ортодромия (дуговые контуры на поверхности Земли, проходящие по кратчайшему расстоянию) ``1`` - локсодромия (дуговые контуры на поверхности Земли, пересекающие меридианы под постоянным углом)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapBuildGeoPath_t (_sourceInfo, _destInfo, _step, _method)

    mapBuildEllipse_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBuildEllipse', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapBuildEllipse(_hobj: maptype.HOBJ, _center: ctypes.POINTER(maptype.DOUBLEPOINT), _bigaxis: float, _littleaxis: float, _angle: float, _count: int) -> int:
        """
        Построить эллипс по двум точкам и параметрам полуосей
        
        :param _hobj: идентификатор объекта карты в памяти centre - координаты центра эллипса в метрах на местности в системе документа
        
        :param _bigaxis: большая полуось в метрах на местности
        
        :param _littleaxis: малая полуось в метрах на местности
        
        :param _angle: угол поворота большой полуоси в радианах против часовой стрелки от направления на восток
        
        :param _count: число точек создаваемой метрики эллипса: от ``16`` до ``256`` Создаваемый объект отображается сплайном, что позволяет минимизировать число точек метрики
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapBuildEllipse_t (_hobj, _center, _bigaxis, _littleaxis, _angle, _count)

    mapVisibilityZonePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapVisibilityZonePro', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(maptype.TBUILDZONEVISIBILITY), maptype.HPAINT, ctypes.c_long)
    def mapVisibilityZonePro(_hmap: maptype.HMAP, _rstname: mapsyst.WTEXT, _zoneparm: ctypes.POINTER(maptype.TBUILDZONEVISIBILITY), _hpaint: maptype.HPAINT, _flags: int) -> int:
        """
        Построить зону видимости по матрице высот в виде растрового изображения
        
        :param _hmap: идентификатор открытой векторной карты
        
        :param _rstname: полное имя растра
        
        :param _zoneparm: параметры построения зоны (maptype.h)
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функций отображения и поиска или ``0``
        
        :param _flags: управляющие флаги: ``1`` - запретить нанесение границы зоны на растр Построение производится при наличии открытой матрицы высот Результат записывается в файл rstname
        
        :returns: Возвращает номер растра в цепочке При ошибке возвращает ноль
        :rtype: int
        """
        return mapVisibilityZonePro_t (_hmap, _rstname.buffer(), _zoneparm, _hpaint, _flags)

    mapVisibilityFromPointEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapVisibilityFromPointEx', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double, ctypes.c_double)
    def mapVisibilityFromPointEx(_hmap: maptype.HMAP, _point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT), _deltaheight1: float, _deltaheight2: float) -> int:
        """
        Определить видимость точки point2 из точки point1 (координаты в метрах на местности)
        
        :param _hmap: идентификатор открытой векторной карты
        
        :param _point1: координаты точки наблюдателя в метрах на местности в системе документа
        
        :param _point2: координаты наблюдаемой точки в метрах на местности в системе документа
        
        :param _deltaheight1: высота наблюдения (в метрах), добавляется к высоте в точке point1
        
        :param _deltaheight2: высота наблюдения (в метрах), добавляется к высоте в точке point2 Вычисление производится при наличии открытой матрицы высот
        
        :returns: Возвращает: ``0`` - point2 не видна из point1 ``1`` - point2 видна из point1 При ошибке в параметрах или отсутствии матрицы возвращает ``"-1"``
        :rtype: int
        """
        return mapVisibilityFromPointEx_t (_hmap, _point1, _point2, _deltaheight1, _deltaheight2)

    mapCreateObjectVoid_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateObjectVoid', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_long)
    def mapCreateObjectVoid(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _incode: int) -> int:
        """
        Создать объекты - пустоты по выделенным объектам
        
        :param _hmap: идентификатор открытой векторной карты с выделенными объектами
        
        :param _hsite: идентификатор векторной карты для записи объектов - пустот
        
        :param _hobj: идентификатор объекта карты в памяти, граница области для создания объектов - пустот
        
        :param _incode: внутренний код объекта для выбора условного знака объектов - пустот
        
        :returns: Возвращает количество созданных объектов - пустот При ошибке возвращает ноль
        :rtype: int
        """
        return mapCreateObjectVoid_t (_hmap, _hsite, _hobj, _incode)

    mapDeleteLoopEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteLoopEx', maptype.HOBJ, ctypes.c_double, ctypes.c_double)
    def mapDeleteLoopEx(_hobj: maptype.HOBJ, _precision: float, _minsquare: float) -> int:
        """
        Удалить петли у объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _precision: точность (величина расхождения координат) при проверке совпадения точек
        
        :param _minsquare: минимальная площадь петли полигона, при которой петля сохраняется как подобъект При сохранении петель в виде подобъектов будет сформирован мультиполигон
        
        :returns: Если петли удалялись - возвращает -1 При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteLoopEx_t (_hobj, _precision, _minsquare)

    mapRotateObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRotateObject', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(ctypes.c_double))
    def mapRotateObject(_hobj: maptype.HOBJ, _center: ctypes.POINTER(maptype.DOUBLEPOINT), _angle: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Повернуть объект вокруг заданной точки на заданный угол
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _center: координаты точки, вокруг которой поворачивается объект, в метрах в системе координат документа
        
        :param _angle: угол поворота против часовой стрелки в радианах от -``PI`` до +``PI``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapRotateObject_t (_hobj, _center, _angle)

    mapContourTotalSeekObjects_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapContourTotalSeekObjects', maptype.HMAP, maptype.HOBJ, ctypes.c_double)
    def mapContourTotalSeekObjects(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _precision: float) -> int:
        """
        Построить внешнюю границу для объектов, выделенных по условиям обобщенного поиска
        
        :param _hmap: идентификатор главной карты
        
        :param _hobj: объект в который записывается определенный контур
        
        :param _precision: допуск согласования объектов (должен быть >= ``DELTANULL``) Объекты могут быть выделены на разных картах Условия поиска задаются функциями mapSetTotalSeekMapRule(), mapSetSiteSeekSelectEx() и другими
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapContourTotalSeekObjects_t (_hmap, _hobj, _precision)

    mapSetFirstPointOfLockedContour_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetFirstPointOfLockedContour', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSetFirstPointOfLockedContour(_hobj: maptype.HOBJ, _number: int, _subject: int) -> int:
        """
        Установить указанную точку замкнутого контура объекта первой
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: номер выбранной точки с ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetFirstPointOfLockedContour_t (_hobj, _number, _subject)

    mapGetTextUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetTextUn', maptype.HOBJ, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapGetTextUn(_hobj: maptype.HOBJ, _text: mapsyst.WTEXT, _size: int, _subject: int) -> int:
        """
        Запросить содержание текста подписи
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _text: адрес для размещения строки
        
        :param _size: длина выделенной области под строку в байтах
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetTextUn_t (_hobj, _text.buffer(), _size, _subject)

    mapGetTextUnSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetTextUnSize', maptype.HOBJ, ctypes.c_long)
    def mapGetTextUnSize(_hobj: maptype.HOBJ, _subject: int) -> int:
        """
        Запросить длину в байтах строки, возвращаемой функцией mapGetTextUn
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetTextUnSize_t (_hobj, _subject)

    mapGetShowText_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetShowText', maptype.HOBJ, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapGetShowText(_hobj: maptype.HOBJ, _text: mapsyst.WTEXT, _size: int, _subject: int) -> int:
        """
        Запросить текст подписи, который будет реально отображаться на карте
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _text: адрес для размещения строки
        
        :param _size: длина выделенной области под строку
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Текст подписи может содержать ссылки на семантики, которые на карте будут отображаться содержимым этих подписей с учетом заданного форматирования - добавления единиц измерения, округления числовых значений и других операций Например: строка ``#27``(``1``)-этажный - заменится на ``"9-этажный"``, ``#46``(``#11``)``#55`` - ``"7,5(9)АСФАЛЬТ"`` и так далее
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetShowText_t (_hobj, _text.buffer(), _size, _subject)

    mapPutTextUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPutTextUn', maptype.HOBJ, maptype.PWCHAR, ctypes.c_long)
    def mapPutTextUn(_hobj: maptype.HOBJ, _text: mapsyst.WTEXT, _subject: int) -> int:
        """
        Установить новое содержание текстовой строки
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _text: новый текст подписи в кодировке UTF-16
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPutTextUn_t (_hobj, _text.buffer(), _subject)

    mapPutMultilineText_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPutMultilineText', maptype.HOBJ, maptype.PWCHAR, ctypes.c_long)
    def mapPutMultilineText(_hobj: maptype.HOBJ, _text: mapsyst.WTEXT, _subject: int) -> int:
        """
        Установить новое содержание текста подобъекта в виде многострочного текста
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _text: адрес новой строки, если text ``= 0``, то обрабатывается ранее записанный текст подобъекта
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если вид подписи не установлен (для графического объекта), у объекта менее двух точек
           либо расстояние между точками слишком мало - разбиение на строки не выполняется
           Разбиение на строки выполняется с учетом параметров вида подписи и расстояния между
           двумя точками подобъекта. В ходе разбиения текста записываются коды переноса строки '\\n'
        """
        return mapPutMultilineText_t (_hobj, _text.buffer(), _subject)

    mapBuildText_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBuildText', maptype.HOBJ, maptype.HOBJ, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR)
    def mapBuildText(_htitle: maptype.HOBJ, _hobj: maptype.HOBJ, _semcode: int, _precision: int, _prefix: mapsyst.WTEXT, _postfix: mapsyst.WTEXT, _text: mapsyst.WTEXT) -> int:
        """
        Сформировать текст подписи и заполнить семантику по семантике подписываемого объекта
        
        :param _hobj: подписываемый объект
        
        :param _semcode: текст семантики для подписывания или ноль
        
        :param _precision: число знаков после запятой для числовой семантики или ``"-1"``
        
        :param _prefix: текст, который вставляется перед выводимым значением семантики или ``0``
        
        :param _postfix: текст, который вставляется после выводимого значения семантики или ``0``
        
        :param _text: текст подписи (может включать номера семантик ``#````XXXX``) для подписывания при отсутствии семантики
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если код семантики не задан, то значения полей precision, prefix и postfix игнорируются
           Добавляет семантики - ссылки на подпись у объекта и на объект у подписи, если у объекту
           уже присвоен уникальный номер
        """
        return mapBuildText_t (_htitle, _hobj, _semcode, _precision, _prefix.buffer(), _postfix.buffer(), _text.buffer())

    mapFitTextForRect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapFitTextForRect', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.FITTEXT))
    def mapFitTextForRect(_source: mapsyst.WTEXT, _text: mapsyst.WTEXT, _textsize: int, _param: ctypes.POINTER(maptype.FITTEXT)) -> int:
        """
        Подогнать текст по размерам прямоугольной области
        
        :param _source: исходный текст
        
        :param _text: буфер для размещения подогнанного текста
        
        :param _textsize: размер буфера text в байтах (рекомендуется в ``2`` раза больше размера исходного текста)
        
        :param _param: параметры обработки
        
        :returns: Возвращает: - в исходном тексте символы переноса строки '\\n' заменяются на пробелы; - многострочный текст в буфере text; - рекомендуемую высоту текста (FITTEXT::TextHeight); - рекомендуемую высоту ячейки (FITTEXT::RectHeight); При ошибке возвращает 0 и код ошибки (FITTEXT::Error)
        :rtype: int
        """
        return mapFitTextForRect_t (_source.buffer(), _text.buffer(), _textsize, _param)

    mapIsTextUnicode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsTextUnicode', maptype.HOBJ)
    def mapIsTextUnicode(_hobj: maptype.HOBJ) -> int:
        """
        Запросить, хранится ли текст подписи в кодировке UTF16
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: Если текст в ``UTF16`` - возвращает ненулевое значение При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsTextUnicode_t (_hobj)

    mapGetTextLengthMkm_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetTextLengthMkm', maptype.HOBJ, ctypes.c_long)
    def mapGetTextLengthMkm(_hobj: maptype.HOBJ, _subject: int) -> int:
        """
        Запросить длину текста в микронах на карте
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: Для подписи, растягиваемой по метрике от точки до точки, возвращает 0 При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetTextLengthMkm_t (_hobj, _subject)

    mapGetTextHeightMkm_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetTextHeightMkm', maptype.HOBJ)
    def mapGetTextHeightMkm(_hobj: maptype.HOBJ) -> int:
        """
        Запросить высоту строки текста для объектов типа подпись в микронах
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: Для подписи, растягиваемой по метрике от точки до точки, возвращает 0 При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetTextHeightMkm_t (_hobj)

    mapGetPaintTextBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetPaintTextBorder', maptype.HMAP, maptype.HDC, ctypes.POINTER(maptype.RECT), maptype.HOBJ, ctypes.POINTER(maptype.DRAWBOX))
    def mapGetPaintTextBorder(_hmap: maptype.HMAP, _hdc: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT), _hobj: maptype.HOBJ, _box: ctypes.POINTER(maptype.DRAWBOX)) -> int:
        """
        Запросить рамку подписи в пикселах для текущих условий отображения
        
        :param _hmap: идентификатор документа
        
        :param _hdc: идентификатор контекста, на котором рассчитывается размер рамки, или ``0``
        
        :param _rect: положение области отображения, относительно которой считается рамка, в пикселах на документе или ``0``
        
        :param _hobj: идентификатор объекта типа подпись, параметры отображения должны быть типа ``IMG_TEXT``
        
        :param _box: поле для записи координат ``4``-ех точек наклонной рамки относительно верхнего левого угла области rect Подобъекты подписи не учитываются при расчете рамки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetPaintTextBorder_t (_hmap, _hdc, _rect, _hobj, _box)

    mapGetTextHorizontalAlign_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetTextHorizontalAlign', maptype.HOBJ, ctypes.c_long)
    def mapGetTextHorizontalAlign(_hobj: maptype.HOBJ, _subject: int) -> int:
        """
        Запросить способ выравнивания текста по горизонтали
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: Возвращает значение: FA_LEFT, FA_RIGHT или FA_CENTER При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetTextHorizontalAlign_t (_hobj, _subject)

    mapGetTextVerticalAlign_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetTextVerticalAlign', maptype.HOBJ, ctypes.c_long)
    def mapGetTextVerticalAlign(_hobj: maptype.HOBJ, _subject: int) -> int:
        """
        Запросить способ выравнивания текста по вертикали
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: Возвращает значение: FA_BOTTOM, FA_TOP, FA_BASELINE, FA_MIDDLE При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetTextVerticalAlign_t (_hobj, _subject)

    mapPutTextHorizontalAlign_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPutTextHorizontalAlign', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapPutTextHorizontalAlign(_hobj: maptype.HOBJ, _align: int, _subject: int) -> int:
        """
        Установить способ выравнивания текста по горизонтали
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _align: код выравнивания по горизонтали: ``FA_LEFT``, ``FA_RIGHT``, ``FA_CENTER``
        
        :param _subject: номер объекта (``0``) или подобъекта (больше ``0``) или -``1`` - установить всем подобъектам По умолчанию выравнивание установлено как ``FA_LEFT`` (текст прижат к первой точке координат)
        
        :returns: При успешном выполнении возвращает установленное значение
        :rtype: int
        """
        return mapPutTextHorizontalAlign_t (_hobj, _align, _subject)

    mapPutTextVerticalAlign_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPutTextVerticalAlign', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapPutTextVerticalAlign(_hobj: maptype.HOBJ, _align: int, _subject: int) -> int:
        """
        Установить способ выравнивания текста по вертикали
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _align: код выравнивания по вертикали: ``FA_BOTTOM``, ``FA_TOP``, ``FA_BASELINE``, ``FA_MIDDLE``
        
        :param _subject: номер объекта (``0``) или подобъекта (больше ``0``) или -``1`` - установить всем подобъектам По умолчанию выравнивание установлено как ``FA_BASELINE``
        
        :returns: При успешном выполнении возвращает установленное значение
        :rtype: int
        """
        return mapPutTextVerticalAlign_t (_hobj, _align, _subject)

    mapPutTextAlign_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPutTextAlign', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapPutTextAlign(_hobj: maptype.HOBJ, _align: int, _subject: int) -> int:
        """
        Установить способ выравнивания текста по горизонтали и вертикали
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _align: код выравнивания содержит сумму кодов по горизонтали и вертикали [``FA_LEFT``,``FA_RIGHT``,``FA_CENTER``] | [``FA_BOTTOM``,``FA_TOP``,``FA_BASELINE``,``FA_MIDDLE``]
        
        :param _subject: номер объекта (``0``) или подобъекта (больше ``0``) или -``1`` - установить всем подобъектам По умолчанию выравнивание установлено как ``FA_LEFT`` | ``FA_BASELINE``
        
        :returns: При успешном выполнении возвращает установленное значение
        :rtype: int
        """
        return mapPutTextAlign_t (_hobj, _align, _subject)

    mapIsDrawObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsDrawObject', maptype.HOBJ)
    def mapIsDrawObject(_hobj: maptype.HOBJ) -> int:
        """
        Запросить, имеет ли объект графическое описание
        
        :param _hobj: идентификатор объекта карты в памяти Графическое описание имеется, как правило, у объектов векторной карты,
        
        :returns: не связанных с классификатором - функция mapObjectCode() возвращает ноль При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsDrawObject_t (_hobj)

    mapDrawCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDrawCount', maptype.HOBJ)
    def mapDrawCount(_hobj: maptype.HOBJ) -> int:
        """
        Запросить количество элементов графического описания
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDrawCount_t (_hobj)

    mapDrawImage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDrawImage', maptype.HOBJ, ctypes.c_long)
    def mapDrawImage(_hobj: maptype.HOBJ, _number: int) -> int:
        """
        Запросить вид элемента графического описания по его номеру
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: порядковый номер элемента от ``1`` до mapDrawCount()
        
        :returns: Возвращает номер функции типа IMG_XXXXXXX (описаны в mapgdi.h) При ошибке возвращает ноль
        :rtype: int
        """
        return mapDrawImage_t (_hobj, _number)

    mapDrawParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_char_p,'mapDrawParameters', maptype.HOBJ, ctypes.c_long)
    def mapDrawParameters(_hobj: maptype.HOBJ, _number: int) -> ctypes.c_char_p:
        """
        Запросить адрес параметров элемента графического описания по его номеру
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: порядковый номер элемента от ``1`` до mapDrawCount() или ``0``
        
        :returns: Возвращает адрес структуры типа IMGXXXXXX, в соответствии с видом элемента (описаны в mapgdi.h) Для запроса с 0 номером возвращает адрес параметров графического описания объекта в виде структуры IMGDRAW При ошибке возвращает ноль
        :rtype: ctypes.c_char_p
        """
        return mapDrawParameters_t (_hobj, _number)

    mapDrawLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDrawLength', maptype.HOBJ, ctypes.c_long)
    def mapDrawLength(_hobj: maptype.HOBJ, _number: int) -> int:
        """
        Запросить длину параметров элемента графического описания по его номеру
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: порядковый номер элемента от ``1`` до mapDrawCount() или ``0``
        
        :returns: Для запроса с 0 номером возвращает длину параметров графического описания всех элементов При ошибке возвращает ноль
        :rtype: int
        """
        return mapDrawLength_t (_hobj, _number)

    mapLoadDrawObjectViewToMemory_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapLoadDrawObjectViewToMemory', maptype.HOBJ, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapLoadDrawObjectViewToMemory(_hobj: maptype.HOBJ, _number: int, _size: ctypes.POINTER(ctypes.c_long)) -> ctypes.POINTER(ctypes.c_char):
        """
        Загрузить внешний вид объекта типа IMGGRAPHICFILE в память RSC (освобождается при закрытии карты)
        
        :param _hobj: идентификатор объекта
        
        :param _number: порядковый номер элемента от ``1`` до mapDrawCount(), тип элемента должен быть ``IMGGRAPHICFILE``
        
        :param _size: поле для записи длины считанного графического файла Выделенная для файла память освобождается при закрытии карты и классификатора
        
        :returns: При ошибке возвращает ноль, иначе - адрес файла в памяти
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapLoadDrawObjectViewToMemory_t (_hobj, _number, _size)

    mapAppendDraw_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendDraw', maptype.HOBJ, ctypes.c_long, ctypes.c_char_p)
    def mapAppendDraw(_hobj: maptype.HOBJ, _image: int, _parm: ctypes.c_char_p) -> int:
        """
        Добавить элемент графического описания объектов
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _image: номер функции типа ``IMG_XXXXXXX`` (описаны в mapgdi.h)
        
        :param _parm: адрес структуры типа ``IMGXXXXXX``
        
        :returns: При ошибке возвращает ноль, иначе - число элементов в записи
        :rtype: int
        """
        return mapAppendDraw_t (_hobj, _image, _parm)

    mapClearDraw_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapClearDraw', maptype.HOBJ)
    def mapClearDraw(_hobj: maptype.HOBJ) -> int:
        """
        Удалить все элементы графического описания объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        """
        return mapClearDraw_t (_hobj)

    mapDeleteDraw_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteDraw', maptype.HOBJ, ctypes.c_int)
    def mapDeleteDraw(_hobj: maptype.HOBJ, _number: int) -> int:
        """
        Удалить элемент графического описания объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: порядковый номер элемента от ``1`` до mapDrawCount()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteDraw_t (_hobj, _number)

    mapReadObjectDraw_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapReadObjectDraw', maptype.HOBJ, maptype.HDRAW)
    def mapReadObjectDraw(_hobj: maptype.HOBJ, _hdrw: maptype.HDRAW) -> int:
        """
        Считать графические параметры объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _hdrw: идентификатор набора примитивов в памяти (создается функцией mapCreateDraw())
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapReadObjectDraw_t (_hobj, _hdrw)

    mapWriteObjectDraw_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapWriteObjectDraw', maptype.HOBJ, maptype.HDRAW)
    def mapWriteObjectDraw(_hobj: maptype.HOBJ, _hdrw: maptype.HDRAW) -> int:
        """
        Записать графические параметры в объект
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _hdrw: идентификатор записываемого набора примитивов в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapWriteObjectDraw_t (_hobj, _hdrw)

    mapGetPolyStyleEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetPolyStyleEx', maptype.HOBJ, ctypes.POINTER(mapgdi.IMGSQUARE), ctypes.POINTER(mapgdi.IMGLINE), ctypes.c_long)
    def mapGetPolyStyleEx(_hobj: maptype.HOBJ, _square: ctypes.POINTER(mapgdi.IMGSQUARE), _line: ctypes.POINTER(mapgdi.IMGLINE), _isalpha: int) -> int:
        """
        Запросить обобщенные графические параметры для полигона или линейного объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _square: цвет полигона (на входе рекомендуется установить цвет в ``IMGC_TRANSPARENT`` для контроля изменения
        
        :param _line: цвет линии и толщина в пикселах
        
        :param _isalpha: признак добавления alpha-канала
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetPolyStyleEx_t (_hobj, _square, _line, _isalpha)

    mapGetPolyStyle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetPolyStyle', maptype.HOBJ, ctypes.POINTER(mapgdi.IMGSQUARE), ctypes.POINTER(mapgdi.IMGLINE))
    def mapGetPolyStyle(_hobj: maptype.HOBJ, _square: ctypes.POINTER(mapgdi.IMGSQUARE), _line: ctypes.POINTER(mapgdi.IMGLINE)) -> int:
        """
        Запросить обобщенные графические параметры для полигона или линейного объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _square: цвет полигона (на входе рекомендуется установить цвет в ``IMGC_TRANSPARENT`` для контроля изменения
        
        :param _line: цвет линии и толщина в пикселах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetPolyStyle_t (_hobj, _square, _line)

    mapIsEdit_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsEdit', maptype.HOBJ)
    def mapIsEdit(_hobj: maptype.HOBJ) -> int:
        """
        Запросить, является ли карта объекта редактируемой (включая редактирование координат)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsEdit_t (_hobj)

    mapIsEditWithoutMetric_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsEditWithoutMetric', maptype.HOBJ)
    def mapIsEditWithoutMetric(_hobj: maptype.HOBJ) -> int:
        """
        Запросить, может ли на карте объекта редактироваться семантика и графика объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsEditWithoutMetric_t (_hobj)

    mapIsDirtyObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsDirtyObject', maptype.HOBJ)
    def mapIsDirtyObject(_hobj: maptype.HOBJ) -> int:
        """
        Запросить, изменились ли какие-либо данные объекта в памяти: метрика, семантика, графика
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: то возвращает ненулевое значение Изменение кода объекта, границ видимости и других свойств эта функция не проверяет При наличии изменений возвращает флаг изменения: ``2`` - метрика, ``4`` - семантика, ``8`` - графика При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если данные были изменены, но еще не были сохранены функцией типа mapCommitObject,
        """
        return mapIsDirtyObject_t (_hobj)

    mapCommitObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCommitObject', maptype.HOBJ)
    def mapCommitObject(_hobj: maptype.HOBJ) -> int:
        """
        Добавить новый объект или обновить существующий объект на карте
        
        :param _hobj: идентификатор объекта карты в памяти Под сохранением объекта на карте понимается запись в файл, в таблицу базы данных, отправка данных по протоколу ``WFS``-T и другие действия, зависящие от источника данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если объект был создан в памяти и отредактирован, то он добавляется на карту
           Если объект был считан с карты и отредактирован, то он обновляется на карте
           Предыдущее состояние объекта сохраняется в резервных файлах и может быть восстановлено
        """
        return mapCommitObject_t (_hobj)

    mapCommitObjectPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCommitObjectPro', maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapCommitObjectPro(_hobj: maptype.HOBJ, _isnewobject: int, _isload: int, _isorder: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Сохранить данные объекта в карту
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _isnewobject: признак записи нового объекта (аналог mapCommitObjectAsNew)
        
        :param _isload: признак записи объекта без пересчета семантики-формула (аналог mapCommitObjectForLoad)
        
        :param _isorder: признак записи объектов в порядке поступления (аналог mapCommitObjectByOrder)
        
        :param _error: поле для записи кода ошибки (описаны в maperr.rh) Под сохранением объекта на карте понимается запись в файл, в таблицу базы данных, отправка данных по протоколу ``WFS``-T и другие действия, зависящие от источника данных Предыдущее состояние объекта сохраняется в резервных файлах и может быть восстановлено
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCommitObjectPro_t (_hobj, _isnewobject, _isload, _isorder, _error)

    mapCommitObjectForLoadEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCommitObjectForLoadEx', maptype.HOBJ, ctypes.POINTER(ctypes.c_long))
    def mapCommitObjectForLoadEx(_hobj: maptype.HOBJ, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Сохранить данные объекта в карту без пересчета семантики типа формула
        
        Это бывает необходимо при чтении данных из базы данных или наборов данных
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _error: поле для записи кода ошибки (описаны в maperr.rh) Номер листа в районе должен быть установлен Предыдущее состояние объекта сохраняется в резервных файлах и может быть восстановлено
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCommitObjectForLoadEx_t (_hobj, _error)

    mapCommitObjectAsNewEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCommitObjectAsNewEx', maptype.HOBJ, ctypes.POINTER(ctypes.c_long))
    def mapCommitObjectAsNewEx(_hobj: maptype.HOBJ, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Добавить новый объект в карту
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _error: поле для записи кода ошибки (описаны в maperr.rh) Объект сохраняется с новым уникальным номером и порядковым номером Может применяться при чтении существующего объекта, как образца, изменении координат и семантики и сохранении как нового объекта Под сохранением объекта на карте понимается запись в файл, в таблицу базы данных, отправка данных по протоколу ``WFS``-T и другие действия, зависящие от источника данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCommitObjectAsNewEx_t (_hobj, _error)

    mapCommitWithPlace_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCommitWithPlace', maptype.HOBJ)
    def mapCommitWithPlace(_hobj: maptype.HOBJ) -> int:
        """
        Сохранить данные об объекте в многолистовой карте MAP с автоматическим делением контура по листам
        
        :param _hobj: идентификатор объекта карты в памяти Предыдущее состояние объекта сохраняется в резервных файлах и может быть восстановлено
        
        :returns: Если объект не попал в габариты какого-либо листа - возвращает -2 Под сохранением объекта на карте понимается запись в файл, в таблицу базы данных, отправка данных по протоколу WFS-T и другие действия, зависящие от источника данных При ошибке возвращает ноль
        :rtype: int
        """
        return mapCommitWithPlace_t (_hobj)

    mapCommitWithPlaceAsNew_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCommitWithPlaceAsNew', maptype.HOBJ)
    def mapCommitWithPlaceAsNew(_hobj: maptype.HOBJ) -> int:
        """
        Добавить объект в многолистовой карте MAP с автоматическим делением контура по листам
        
        Объект будет сохранен, как новый, с присвоением нового уникального номера
        
        :param _hobj: идентификатор объекта карты в памяти Для объектов пользовательских карт (обстановки) достаточно mapCommitObject() - там один лист и нет границ Предыдущее состояние объекта сохраняется в резервных файлах и может быть восстановлено
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCommitWithPlaceAsNew_t (_hobj)

    mapCommitWithPlaceForList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCommitWithPlaceForList', maptype.HOBJ, ctypes.c_long)
    def mapCommitWithPlaceForList(_hobj: maptype.HOBJ, _list: int) -> int:
        """
        Сохранить данные об объекте в многолистовой карте с обрезанием объекта по границам листа
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _list: номер листа с ``1``, по рамке которого будет обрезан контур объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCommitWithPlaceForList_t (_hobj, _list)

    mapGetCommitObjectParm_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetCommitObjectParm', maptype.HMAP, ctypes.POINTER(maptype.COMMITOBJECTPARM))
    def mapGetCommitObjectParm(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.COMMITOBJECTPARM)) -> int:
        """
        Запрость параметры обработки метрики линейных и площадных объектов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _parm: параметры, используемые при разрезания объектов по рамкам листов карты Параметры обработки метрики линейных и площадных объектов используются при сохранении объектов для автоматического удаления малых отрезков, малых линейных и вырожденных площадных объектов, которые получаются при разрезания объектов по рамкам листов карты Параметры применяются в функциях типа: mapCommitWithPlace, mapCommitWithPlaceAsNew, mapCommitWithPlaceForList
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetCommitObjectParm_t (_hmap, _parm)

    mapSetCommitObjectParm_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetCommitObjectParm', maptype.HMAP, ctypes.POINTER(maptype.COMMITOBJECTPARM))
    def mapSetCommitObjectParm(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.COMMITOBJECTPARM)) -> int:
        """
        Установить параметры обработки метрики линейных и площадных объектов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _parm: параметры, используемые при разрезания объектов по рамкам листов карты Параметры обработки метрики линейных и площадных объектов используются при сохранении объектов для автоматического удаления малых отрезков, малых линейных и вырожденных площадных объектов, которые получаются при разрезания объектов по рамкам листов карты Параметры применяются в функциях типа: mapCommitWithPlace, mapCommitWithPlaceAsNew, mapCommitWithPlaceForList
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetCommitObjectParm_t (_hmap, _parm)

    mapCommitObjectAsSimple_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCommitObjectAsSimple', maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapCommitObjectAsSimple(_hobj: maptype.HOBJ, _forload: int, _makeset: int, _asnew: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Сохранить объект в файле с разбиением мультигеометрии на простые объекты
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _forload: флаг режима загрузки: при сохранении объекта не пересчитываются семантики-формулы;
        
        :param _makeset: флаг необходимости объединить полученные объекты в набор
        
        :param _asnew: флаг сохранения объекта как нового, если ноль, то объект в hobj будет заменен, иначе все объекты, включая основной контур, будут сохранены новыми объектами, объект переданный в hobj на карте останется без изменений;
        
        :param _error: буфер для возврата кода ошибки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если объект не содержит мультигеометрии, то он сохраняется одним объектом
           При успешном завершении в hobj останется основной контур объекта, а все его
           внешние подобъекты станут самостоятельными объектами, при необходимости объединенными
           в набор (параметр makeset)
        """
        return mapCommitObjectAsSimple_t (_hobj, _forload, _makeset, _asnew, _error)

    mapIsObjectLoading_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsObjectLoading', maptype.HOBJ)
    def mapIsObjectLoading(_hobj: maptype.HOBJ) -> int:
        """
        Запросить, выполняется ли загрузка объекта из базы данных или набора данных
        
        :param _hobj: идентификатор объекта карты в памяти Применяется в функциях обратного вызова для определения того, что выполняется функция mapCommitObjectForLoad()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsObjectLoading_t (_hobj)

    mapDeleteObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteObject', maptype.HOBJ)
    def mapDeleteObject(_hobj: maptype.HOBJ) -> int:
        """
        Удалить объект карты
        
        :param _hobj: идентификатор объекта карты в памяти Предыдущее состояние объекта сохраняется в резервных файлах и может быть восстановлено Признак удаления сразу записывается в памяти и в карте Под сохранением объекта на карте понимается запись в файл, в таблицу базы данных, отправка данных по протоколу ``WFS``-T и другие действия, зависящие от источника данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteObject_t (_hobj)

    mapDeleteObjectByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteObjectByNumber', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapDeleteObjectByNumber(_hmap: maptype.HMAP, _list: int, _number: int) -> int:
        """
        Удалить объект карты по его номеру
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _list: последовательный номер листа с ``1``
        
        :param _number: последовательный ноиер объекта в листе с ``1`` Предыдущее состояние объекта сохраняется в резервных файлах и может быть восстановлено Признак удаления сразу записывается в карте Под сохранением объекта на карте понимается запись в файл, в таблицу базы данных, отправка данных по протоколу ``WFS``-T и другие действия, зависящие от источника данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteObjectByNumber_t (_hmap, _list, _number)

    mapUndeleteObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUndeleteObject', maptype.HOBJ)
    def mapUndeleteObject(_hobj: maptype.HOBJ) -> int:
        """
        Отменить удаление объекта карты
        
        :param _hobj: идентификатор объекта карты в памяти Признак удаления убирается в памяти и в карте
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUndeleteObject_t (_hobj)

    mapUpdateObjectUp_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateObjectUp', maptype.HOBJ)
    def mapUpdateObjectUp(_hobj: maptype.HOBJ) -> int:
        """
        Переместить объект в цепочке объектов в конец для отображения над всеми
        
        :param _hobj: идентификатор объекта карты в памяти Объекту присваивается признак ``"выше всех"`` и выполняется обновление на карте
        
        :returns: Возвращает новый последовательный номер объекта на карте - mapGetObjectNumber() При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdateObjectUp_t (_hobj)

    mapUpdateObjectDown_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateObjectDown', maptype.HOBJ)
    def mapUpdateObjectDown(_hobj: maptype.HOBJ) -> int:
        """
        Переместить объект в цепочке объектов в начало для отображения под всеми
        
        :param _hobj: идентификатор объекта карты в памяти Объекту присваивается признак ``"ниже всех"`` и выполняется обновление на карте
        
        :returns: Возвращает новый последовательный номер объекта на карте - mapGetObjectNumber() При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdateObjectDown_t (_hobj)

    mapUpdateObjectNormal_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateObjectNormal', maptype.HOBJ)
    def mapUpdateObjectNormal(_hobj: maptype.HOBJ) -> int:
        """
        Сбросить признаки "выше всех" и "ниже всех" в объекте
        
        :param _hobj: идентификатор объекта карты в памяти У объекта сбрасываются признаки ``"выше всех"`` и ``"ниже всех"`` и выполняется обновление на карте Положение объекта в соответствии с его слоем и локализацией восстановится только после сортировки карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdateObjectNormal_t (_hobj)

    mapObjectUpDownState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectUpDownState', maptype.HOBJ)
    def mapObjectUpDownState(_hobj: maptype.HOBJ) -> int:
        """
        Запросить признаки размещения объекта "выше всех" и "ниже всех"
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: Возвращает код размещения объекта: ``2`` - над всеми, ``3`` - под всеми, ``1`` - не задано При ошибке возвращает ноль
        :rtype: int
        """
        return mapObjectUpDownState_t (_hobj)

    mapUndeleteObjectByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUndeleteObjectByNumber', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long)
    def mapUndeleteObjectByNumber(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _number: int) -> int:
        """
        Отменить удаление объекта карты по его номеру
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в документе, для фоновой карты равен hmap
        
        :param _list: последовательный номер листа с ``1``
        
        :param _number: последовательный ноиер объекта в листе c ``1`` Признак удаления объекта убирается в карте
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUndeleteObjectByNumber_t (_hmap, _hsite, _list, _number)

    mapRevertObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRevertObject', maptype.HOBJ)
    def mapRevertObject(_hobj: maptype.HOBJ) -> int:
        """
        Восстановить в памяти данные об объекте из карты
        
        :param _hobj: идентификатор объекта карты в памяти Номер листа в районе и номер объекта должны быть установлены
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapRevertObject_t (_hobj)

    mapRestoreBackObjectByAction_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRestoreBackObjectByAction', maptype.HOBJ, ctypes.c_long)
    def mapRestoreBackObjectByAction(_hobj: maptype.HOBJ, _number: int) -> int:
        """
        Восстановить копию объекта, по состоянию до выполнения заданной транзакции
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: номер транзакции
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapRestoreBackObjectByAction_t (_hobj, _number)

    mapRestoreBackObjectByTime_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRestoreBackObjectByTime', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapRestoreBackObjectByTime(_hobj: maptype.HOBJ, _date: int, _time: int) -> int:
        """
        Восстановить копию объекта, по состоянию до выполнения транзакции, ближайшей к заданному времени
        
        :param _hobj: идентификатор объекта карты в памяти number - номер транзакции
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapRestoreBackObjectByTime_t (_hobj, _date, _time)

    mapLoadMulticontourLevel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLoadMulticontourLevel', maptype.HOBJ, ctypes.c_long)
    def mapLoadMulticontourLevel(_hobj: maptype.HOBJ, _level: int) -> int:
        """
        Считать в объект метрику мультимасштабного объекта заданного уровня
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _level: уровень генерализации контура от ``1`` до ``4``
        
        :returns: Если у объекта нет дополнительных контуров - возвращает ноль Возвращает номер считанного уровня При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если для заданного уровня контура нет, то считывается соседний более сжатый
           контур, если его нет, то менее сжатый
        """
        return mapLoadMulticontourLevel_t (_hobj, _level)

    mapSetObjectEditDateTime_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetObjectEditDateTime', maptype.HOBJ)
    def mapSetObjectEditDateTime(_hobj: maptype.HOBJ) -> int:
        """
        Записать в объект дату, время создания или редактирования объекта и имя оператора
        
        :param _hobj: идентификатор объекта карты в памяти Для вновь создаваемого объекта пишется дата и время создания ``SEMOBJECTDATE`` и ``SEMOBJECTTIME``, имя оператора пишется в семантику ``SEMOBJECTAUTHOR`` Для редактируемого объекта пишется (при отсутствии) или изменяется (при наличии) время последнего редактирования ``SEMOBJECTREDATE`` и ``SEMOBJECTRETIME``, имя оператора пишется в семантику ``SEMOBJECTREAUTHOR`` (``SEMOBJECTREAUTHOR``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetObjectEditDateTime_t (_hobj)

    mapSideLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSideLength', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSideLength(_hobj: maptype.HOBJ, _number: int, _subject: int) -> float:
        """
        Вычисление длины участка объекта на эллипсоиде (местности), начиная с указанной точки
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: номер точки, начиная с ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Для последней точки вычисляет расстояние до первой точки У замкнутых объектов первая и последняя точки совпадают Расчет выполняется на основе геодезических вычислений на эллипсоиде Для точек, удаленных по долготе более чем на ``5`` градусов, расчет выполняется по ортодромии
        
        :returns: При ошибке возвращает ноль (при совпадении точек также вернет ноль)
        :rtype: float
        """
        return mapSideLength_t (_hobj, _number, _subject)

    mapSideLengthEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSideLengthEx', maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def mapSideLengthEx(_hobj: maptype.HOBJ, _number: int, _subject: int, _length: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Вычисление длины участка объекта на эллипсоиде (местности), начиная с указанной точки
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: номер точки, начиная с ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :param _length: поле для записи результата вычисления Для последней точки вычисляет расстояние до первой точки У замкнутых объектов первая и последняя точки совпадают Расчет выполняется на основе геодезических вычислений на эллипсоиде Для точек, удаленных по долготе более чем на ``5`` градусов, расчет выполняется по ортодромии
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSideLengthEx_t (_hobj, _number, _subject, _length)

    mapSideLengthInMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSideLengthInMap', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSideLengthInMap(_hobj: maptype.HOBJ, _number: int, _subject: int) -> float:
        """
        Вычисление длины участка объекта на карте, начиная с указанной точки
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: номер точки, начиная с ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Для последней точки вычисляет расстояние до первой точки Вычисляет корень квадратный из суммы квадратов приращений координат
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapSideLengthInMap_t (_hobj, _number, _subject)

    mapSetCalculationConventional_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetCalculationConventional', maptype.HMAP, ctypes.c_long)
    def mapSetCalculationConventional(_hmap: maptype.HMAP, _flag: int) -> int:
        """
        Установить метод для расчета расстояний и площадей
        
        :param _hmap: идентификатор открытых данных (документа) method - метод выполнения расчетов: ``0`` - выполнять геодезические вычисления на эллипсоиде, ``1`` - выполнять геометрические вычисления в текущей проекции документа
        
        :returns: Возвращает предыдущее значение условия
        :rtype: int
        
        .. note::

           Если текущая проекция документа топографическая (UTM, Гаусса-Крюгера), то результаты
           вычислений двумя методами будут совпадать по мере приближения точек к осевому меридиану
        """
        return mapSetCalculationConventional_t (_hmap, _flag)

    mapGetCalculationConventional_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetCalculationConventional', maptype.HMAP)
    def mapGetCalculationConventional(_hmap: maptype.HMAP) -> int:
        """
        Запросить текущий метод для расчета расстояний и площадей по карте
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: Возвращает метод выполнения расчетов : ``0`` - выполнять геодезические вычисления на эллипсоиде, ``1`` - выполнять геометрические вычисления в текущей проекции документа Если текущая проекция документа топографическая (UTM, Гаусса-Крюгера), то результаты вычислений двумя методами будут совпадать по мере приближения точек к осевому меридиану
        :rtype: int
        """
        return mapGetCalculationConventional_t (_hmap)

    mapConventionalSideLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapConventionalSideLength', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapConventionalSideLength(_hobj: maptype.HOBJ, _number: int, _subject: int) -> float:
        """
        Вычисление длины участка объекта заданным методом
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: номер точки, начиная с ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки Вычисление выполняется на карте или на эллипсоиде, в зависимости от текущего метода вычислений, установленного в mapSetCalculationConventional()
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapConventionalSideLength_t (_hobj, _number, _subject)

    mapSideAzimuth_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSideAzimuth', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSideAzimuth(_hobj: maptype.HOBJ, _number: int, _subject: int) -> float:
        """
        Вычисление азимута участка объекта (стороны)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: номер точки, начиная с ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: Возвращает величину угла в радианах между направлением меридиана, проходящего через первую точку на север, и стороной объекта Если в документе геодезия не поддерживается (крупномасштабный план), то вычисляется дирекционный угол между направлением на север (вертикаль) и стороной объекта Для цилиндрических проекций азимут и дирекционный угол совпадают Для последней точки вычисляет направление на первую точку У замкнутых объектов первая и последняя точки совпадают При ошибке возвращает ноль
        :rtype: float
        """
        return mapSideAzimuth_t (_hobj, _number, _subject)

    mapSideAzimuthEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSideAzimuthEx', maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def mapSideAzimuthEx(_hobj: maptype.HOBJ, _number: int, _subject: int, _azimuth: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Вычисление азимута участка объекта (стороны)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: номер точки, начиная с ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :param _azimuth: поле для записи вычисленного угла
        
        :returns: Возвращает величину угла в радианах между направлением касательной меридиана, проходящего через первую точку на север, и направлениемна вторую точку Для последней точки вычисляет направление на первую точку При ошибке возвращает ноль
        :rtype: int
        """
        return mapSideAzimuthEx_t (_hobj, _number, _subject, _azimuth)

    mapSideDirection_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSideDirection', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSideDirection(_hobj: maptype.HOBJ, _number: int, _subject: int) -> float:
        """
        Вычисление дирекционного угла участка объекта (стороны) в системе координат документа
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: номер точки, начиная с ``1``
        
        :param _subject: номер подобъекта (если ``= 0``, обрабатывается объект)
        
        :returns: Возвращает величину угла в радианах между направлением на север (вертикаль) и стороной объекта Дирекционный угол зависит от текущей системы координат документа Для последней точки вычисляет направление на первую точку У замкнутых объектов первая и последняя точки совпадают При ошибке возвращает ноль
        :rtype: float
        """
        return mapSideDirection_t (_hobj, _number, _subject)

    mapSideDirectionInMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSideDirectionInMap', maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSideDirectionInMap(_hobj: maptype.HOBJ, _number: int, _subject: int) -> float:
        """
        Вычисление дирекционного угла участка объекта (стороны) по координатам в системе карты
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: номер точки, начиная с ``1``
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``), контура содержат не менее ``1`` точки
        
        :returns: Возвращает величину угла в радианах между направлением на север (вертикаль) и стороной объекта При ошибке возвращает ноль
        :rtype: float
        """
        return mapSideDirectionInMap_t (_hobj, _number, _subject)

    mapSquare_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSquare', maptype.HOBJ)
    def mapSquare(_hobj: maptype.HOBJ) -> float:
        """
        Вычисление площади объекта на местности
        
        :param _hobj: идентификатор объекта карты в памяти Для вычисления площади объекта его координаты пересчитываются в проекцию топографической карты ближайшей зоны
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapSquare_t (_hobj)

    mapSquareEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSquareEx', maptype.HOBJ, ctypes.POINTER(ctypes.c_double))
    def mapSquareEx(_hobj: maptype.HOBJ, _square: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Вычисление площади объекта на местности
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _square: поле для записи значения площади Для вычисления площади объекта его координаты пересчитываются в проекцию топографической карты ближайшей зоны
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSquareEx_t (_hobj, _square)

    mapPrecisionSquare_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapPrecisionSquare', maptype.HOBJ)
    def mapPrecisionSquare(_hobj: maptype.HOBJ) -> float:
        """
        Вычисление уточненной площади объекта на местности
        
        :param _hobj: идентификатор объекта карты в памяти Для вычисления площади объекта его контур делится на участки, занимающие по долготе не более ``6`` градусов для повышения точности Координаты участков пересчитываются в проекцию топографической карты ближайшей зоны Для корректных вычислений контура не должны иметь самопересечений
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapPrecisionSquare_t (_hobj)

    mapSquareInMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSquareInMap', maptype.HOBJ)
    def mapSquareInMap(_hobj: maptype.HOBJ) -> float:
        """
        Вычисление площади объекта в системе координат карты
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapSquareInMap_t (_hobj)

    mapConventionalSquare_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapConventionalSquare', maptype.HOBJ)
    def mapConventionalSquare(_hobj: maptype.HOBJ) -> float:
        """
        Вычисление площади объекта заданным методом
        
        :param _hobj: идентификатор объекта карты в памяти Вычисление выполняется на карте или на эллипсоиде (на местности), в зависимости от текущего метода вычислений, установленного в mapSetCalculationConventional()
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapConventionalSquare_t (_hobj)

    mapConventionalSubjectSquare_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapConventionalSubjectSquare', maptype.HOBJ, ctypes.c_long)
    def mapConventionalSubjectSquare(_hobj: maptype.HOBJ, _subject: int) -> float:
        """
        Вычисление площади контура отдельного подобъекта заданным методом
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``) Вычисление выполняется на карте или на эллипсоиде, в зависимости от текущего метода вычислений, установленного в mapSetCalculationConventional()
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapConventionalSubjectSquare_t (_hobj, _subject)

    mapPrecisionSubjectSquare_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapPrecisionSubjectSquare', maptype.HOBJ, ctypes.c_long)
    def mapPrecisionSubjectSquare(_hobj: maptype.HOBJ, _subject: int) -> float:
        """
        Вычисление уточненной площади контура отдельного подобъекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``) Для вычисления площади контур делится на участки, занимающие по долготе не более ``6`` градусов для повышения точности Координаты участков пересчитываются в проекцию топографической карты ближайшей зоны Для корректных вычислений контура не должны иметь самопересечений
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapPrecisionSubjectSquare_t (_hobj, _subject)

    mapSubjectSquareInMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSubjectSquareInMap', maptype.HOBJ, ctypes.c_long)
    def mapSubjectSquareInMap(_hobj: maptype.HOBJ, _subject: int) -> float:
        """
        Вычисление площади подобъекта в системе координат карты
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``)
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapSubjectSquareInMap_t (_hobj, _subject)

    mapSquareWithHeightEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSquareWithHeightEx', maptype.HMAP, maptype.HOBJ, ctypes.c_double)
    def mapSquareWithHeightEx(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _step: float) -> float:
        """
        Вычисление площади объекта c учетом рельефа
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _step: шаг интерполяции в метрах (размер ячейки, на которой высота принимается одинаковой), если ``0`` - то вычисляется автоматически При отсутствии рельефа (матрицы высот, слоев, ``TIN``-модели) вычисляет без учета рельефа Координаты участков пересчитываются в проекцию топографической карты ближайшей зоны
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapSquareWithHeightEx_t (_hmap, _hobj, _step)

    mapLengthEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLengthEx', maptype.HOBJ, ctypes.POINTER(ctypes.c_double))
    def mapLengthEx(_hobj: maptype.HOBJ, _length: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Вычисление длины объекта на местности
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _length: поле для записи вычисленной длины объекта Для подобъектов считается суммарная длина При вычислении длины объекта его координаты пересчитываются в проекцию топографической карты по каждому отрезку отдельно с установкой осевого меридиана в центре отрезка
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapLengthEx_t (_hobj, _length)

    mapLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapLength', maptype.HOBJ)
    def mapLength(_hobj: maptype.HOBJ) -> float:
        """
        Вычисление длины объекта на местности
        
        :param _hobj: идентификатор объекта карты в памяти Для подобъектов считается суммарная длина При вычислении длины объекта его координаты пересчитываются в проекцию топографической карты по каждому отрезку отдельно с установкой осевого меридиана в центре отрезка
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapLength_t (_hobj)

    mapLengthInMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapLengthInMap', maptype.HOBJ)
    def mapLengthInMap(_hobj: maptype.HOBJ) -> float:
        """
        Вычисление длины объекта в системе координат карты
        
        :param _hobj: идентификатор объекта карты в памяти Координаты объекта не пересчитываются к топокарте, длины отрезков вычисляются геометрическим методом Полученная длина для некоторых популярных проекций может в разы отличаться от реальной длины объекта на местности Для подобъектов считается суммарная длина
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapLengthInMap_t (_hobj)

    mapLengthToPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapLengthToPoint', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapLengthToPoint(_hobj: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        """
        Вычисление длины объекта от начала до заданной точки рядом с контуром
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _point: координаты точки, расположенной вблизи объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        
        .. note::

           Если точка не на объекте - ищется ближайшая точка на контуре
           Координаты точки обновляются найденной точкой на контуре
           При вычислении длины объекта его координаты пересчитываются
           в проекцию топографической карты по каждому отрезку отдельно
           с установкой осевого меридиана в центре отрезка
        """
        return mapLengthToPoint_t (_hobj, _point)

    mapSubjectLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSubjectLength', maptype.HOBJ, ctypes.c_long)
    def mapSubjectLength(_hobj: maptype.HOBJ, _subject: int) -> float:
        """
        Вычисление длины подобъекта или всего объекта на местности
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _subject: номер подобъекта: ``0`` или более - вычисляется длина подобъекта -``1`` - вычисляется суммарная длина всех подобъектов -``2`` - вычисляется суммарная длина всех главных (внешних) подобъектов мультиполигона При вычислении длины объекта его координаты пересчитываются в проекцию топографической карты по каждому отрезку отдельно с установкой осевого меридиана в центре отрезка
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapSubjectLength_t (_hobj, _subject)

    mapSubjectLengthInMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSubjectLengthInMap', maptype.HOBJ, ctypes.c_long)
    def mapSubjectLengthInMap(_hobj: maptype.HOBJ, _subject: int) -> float:
        """
        Вычисление длины объекта или подобъекта в проекции карты
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _subject: номер подобъекта: ``0`` или более - вычисляется длина подобъекта -``1`` - вычисляется суммарная длина всех подобъектов; -``2`` - вычисляется суммарная длина всех главных (внешних) подобъектов Координаты объекта не пересчитываются к топокарте, длины отрезков вычисляются геометрическим методом
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapSubjectLengthInMap_t (_hobj, _subject)

    mapConventionalSubjectLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapConventionalSubjectLength', maptype.HOBJ, ctypes.c_long)
    def mapConventionalSubjectLength(_hobj: maptype.HOBJ, _subject: int) -> float:
        """
        Вычисление длины объекта или подобъекта заданным методом
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _subject: номер подобъекта: ``0`` или более - вычисляется длина подобъекта; -``1`` - вычисляется суммарная длина всех подобъектов; -``2`` - вычисляется суммарная длина всех главных (внешних) подобъектов Вычисление выполняется на карте или на эллипсоиде (на местности), в зависимости от текущего метода вычислений, установленного в mapSetCalculationConventional()
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapConventionalSubjectLength_t (_hobj, _subject)

    mapLengthWithHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapLengthWithHeight', maptype.HMAP, maptype.HOBJ)
    def mapLengthWithHeight(_hmap: maptype.HMAP, _hobj: maptype.HOBJ) -> float:
        """
        Вычисление длины объекта c учетом рельефа
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При отсутствии данных о рельефе (матрицы высот, слоев, TIN-модели) возвращает длину объекта При вычислении длины объекта его координаты пересчитываются в проекцию топографической карты по каждому отрезку отдельно с установкой осевого меридиана в центре отрезка При ошибке возвращает ноль
        :rtype: float
        """
        return mapLengthWithHeight_t (_hmap, _hobj)

    mapPerimeter_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapPerimeter', maptype.HOBJ)
    def mapPerimeter(_hobj: maptype.HOBJ) -> float:
        """
        Вычисление периметра объекта
        
        :param _hobj: идентификатор объекта карты в памяти При вычислении координаты объекта пересчитываются в проекцию топографической карты по каждому отрезку отдельно с установкой осевого меридиана в центре отрезка
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapPerimeter_t (_hobj)

    mapCircuitousSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCircuitousSubject', maptype.HOBJ, ctypes.c_long)
    def mapCircuitousSubject(_hobj: maptype.HOBJ, _subject: int) -> int:
        """
        Определение замкнутости контура подобъекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``)
        
        :returns: Возвращает: ``1`` - объект замкнут, иначе - 0
        :rtype: int
        """
        return mapCircuitousSubject_t (_hobj, _subject)

    mapDistancePointSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapDistancePointSubject', maptype.HMAP, maptype.HOBJ, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapDistancePointSubject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _subject: int, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        """
        Определение кратчайшего расстояния от точки до объекта
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _subject: номер контура объекта (``0``) или контура подобъекта (больше ``0``) Координаты точки point заданы в плоской прямоугольной системе координат документа в метрах на местности При вычислении координаты пересчитываются в проекцию топографической карты с установкой осевого меридиана в центре отрезка
        
        :returns: Возвращает вычисленное расстояние в метрах При ошибке возвращает ноль
        :rtype: float
        """
        return mapDistancePointSubject_t (_hmap, _hobj, _subject, _point)

    mapDistancePointObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapDistancePointObject', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapDistancePointObject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        """
        Определение кратчайшего расстояния от точки до объекта, включая подобъекты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _point: координаты точки в системе координат документа При вычислении координаты пересчитываются в проекцию топографической карты с установкой осевого меридиана в центре отрезка
        
        :returns: Возвращает вычисленное расстояние в метрах При ошибке возвращает ноль
        :rtype: float
        """
        return mapDistancePointObject_t (_hmap, _hobj, _point)

    mapDistanceObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapDistanceObject', maptype.HOBJ, maptype.HOBJ)
    def mapDistanceObject(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ) -> float:
        """
        Определение кратчайшего расстояния между объектами
        
        :param _hobj1: идентификатор ``1``-го объекта карты в памяти
        
        :param _hobj2: идентификатор ``2``-го объекта карты в памяти При вычислении координаты найденных ближайших точек пересчитываются в проекцию топографической карты с установкой осевого меридиана в центре отрезка
        
        :returns: Возвращает вычисленное расстояние в метрах При ошибке возвращает ноль
        :rtype: float
        """
        return mapDistanceObject_t (_hobj1, _hobj2)

    mapDistanceObjectEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapDistanceObjectEx', maptype.HOBJ, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapDistanceObjectEx(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ, _point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        """
        Определение кратчайшего расстояния между объектами и координат точек на контурах объектов
        
        :param _hobj1: идентификатор первого объекта карты в памяти
        
        :param _hobj2: идентификатор второго объекта карты в памяти
        
        :param _point1: координаты первой точки линии кратчайшего расстояния между объектами (на объекте hobj1)
        
        :param _point2: координаты второй точки линии кратчайшего расстояния между объектами (на объекте hobj2) При вычислении координаты найденных ближайших точек пересчитываются в проекцию топографической карты с установкой осевого меридиана в центре отрезка
        
        :returns: Возвращает вычисленное расстояние  в метрах или большое значение (100000001) в случае ошибки
        :rtype: float
        """
        return mapDistanceObjectEx_t (_hobj1, _hobj2, _point1, _point2)

    mapDirectPositionComputation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDirectPositionComputation', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapDirectPositionComputation(_hmap: maptype.HMAP, _b1: float, _l1: float, _angle1: float, _distance: float, _b2: ctypes.POINTER(ctypes.c_double), _l2: ctypes.POINTER(ctypes.c_double), _angle2: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Прямая геодезическая задача на эллипсоиде
        
        :param _hmap: идентификатор открытых данных (документа) или ``0`` (координаты на ``WGS84``) b - широта исходной точки в радианах в геодезической системе координат документа или ``WGS84`` l - долгота исходной точки в радианах в геодезической системе координат документа или ``WGS84``
        
        :param _angle1: азимут на вторую точку в радианах
        
        :param _distance: расстояние до второй точки в метрах на местности
        
        :param _b2: широта найденной точки в радианах в геодезической системе координат документа или ``WGS84``
        
        :param _l2: долгота найденной точки в радианах в геодезической системе координат документа или ``WGS84``
        
        :param _angle2: рассчитанный азимут со второй точки на первую в радианах (если angle2 равен ``0``, то обратный азимут не вычисляется) Для расстояния не более ``250`` км координаты определяются с ошибкой до ``0``,``0001````", а обратный азимут - до 0,001"``, что соответствует триангуляции ``1`` класса Способ вспомогательной точки по методу Красовского Метод предназначен для расстояний меньше радиуса Земли Вычисления выполняются на текущем эллипсоиде, установленном в документе - mapSetDocProjection
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если hmap равен 0, то вычисления выполняются на эллипсоиде WGS84
        """
        return mapDirectPositionComputation_t (_hmap, _b1, _l1, _angle1, _distance, _b2, _l2, _angle2)

    mapInversePositionComputation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapInversePositionComputation', maptype.HMAP, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double))
    def mapInversePositionComputation(_hmap: maptype.HMAP, _b1: float, _l1: float, _b2: float, _l2: float, _angle: ctypes.POINTER(ctypes.c_double)) -> float:
        """
        Обратная геодезическая задача на эллипсоиде
        
        :param _hmap: идентификатор открытых данных (документа) или ``0`` (координаты на ``WGS84``) b - широта исходной точки в радианах в геодезической системе координат документа или ``WGS84`` l - долгота исходной точки в радианах в геодезической системе координат документа или ``WGS84``
        
        :param _b2: широта найденной точки в радианах в геодезической системе координат документа или ``WGS84``
        
        :param _l2: долгота найденной точки в радианах в геодезической системе координат документа или ``WGS84``
        
        :param _angle: рассчитанный азимут с первой точки на вторую в радианах Для расстояния не более ``180`` градусов по широте Выполняется построение ортодромии функцией mapOrthodromeObject и запрос длины объекта и азимута первого отрезка Точность порядка точности триангуляции ``1`` класса Вычисления выполняются на текущем эллипсоиде, установленном в документе - mapSetDocProjection
        
        :returns: Возвращает расстояние между заданными точками на текущем эллипсоиде в метрах на местности При ошибке возвращает ноль
        :rtype: float
        
        .. note::

           Если hmap равен 0, то вычисления выполняются на эллипсоиде WGS84
        """
        return mapInversePositionComputation_t (_hmap, _b1, _l1, _b2, _l2, _angle)

    mapGetGeoCircleRadius_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetGeoCircleRadius', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetGeoCircleRadius(_first: ctypes.POINTER(maptype.DOUBLEPOINT), _middle: ctypes.POINTER(maptype.DOUBLEPOINT), _last: ctypes.POINTER(maptype.DOUBLEPOINT), _center: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        """
        Определить центр и радиус окружности, проходящей через три точки
        
        :param _first: координаты первой точки на эллипсоиде ``WGS84`` в радианах
        
        :param _middle: координаты второй точки на эллипсоиде ``WGS84`` в радианах
        
        :param _last: координаты третьей точки в радианах
        
        :param _center: рассчитанные координаты центра окружности в радианах
        
        :returns: Возвращает длину радиуса окружности в метрах на местности При ошибке в параметрах или расположении точек на одной линии возвращает ноль
        :rtype: float
        
        .. note::

           Рекомендуется применять для расчетов окружностей с радиусом в пределах ``500 000`` метров
        """
        return mapGetGeoCircleRadius_t (_first, _middle, _last, _center)

    mapDistance_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapDistance', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapDistance(_point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        """
        Вычисление расстояния между двумя точками на плоскости
        
        :param _point1: координаты первой точки в метрах
        
        :param _point2: координаты второй точки в метрах Расстояние вычисляется геометрическим методом
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapDistance_t (_point1, _point2)

    mapRealDistance_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapRealDistance', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapRealDistance(_hmap: maptype.HMAP, _point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        """
        Вычисление расстояния между двумя точками на местности
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _point1: координаты первой точки в метрах в системе координат документа
        
        :param _point2: координаты второй точки в метрах в системе координат документа Для вычисления расстояния координаты пересчитываются в проекцию топографической карты с установкой осевого меридиана в центре отрезка
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapRealDistance_t (_hmap, _point1, _point2)

    mapConventionalDistance_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapConventionalDistance', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapConventionalDistance(_hmap: maptype.HMAP, _point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        """
        Вычисление расстояния между двумя точками заданным методом
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _point1: координаты первой точки в метрах в системе координат документа
        
        :param _point2: координаты второй точки в метрах в системе координат документа Вычисление выполняется на карте или на эллипсоиде (на местности), в зависимости от текущего метода вычислений, установленного в mapSetCalculationConventional()
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapConventionalDistance_t (_hmap, _point1, _point2)

    mapBisectorAngle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapBisectorAngle', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapBisectorAngle(_p1: ctypes.POINTER(maptype.DOUBLEPOINT), _p2: ctypes.POINTER(maptype.DOUBLEPOINT), _p3: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        """
        Определение направления биссектрисы угла, заданного тремя точками
        
        point1 - координаты первой точки угла в метрах в системе координат документа
        point2 - координаты центра угла в метрах в системе координат документа
        point3 - координаты последней точки угла в метрах в системе координат документа
        Возвращаемый дирекционный угол в радианах задан относительно вертикальной оси X, его положительное
        направление соответствует положительному направлению горизонтальной оси Y
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapBisectorAngle_t (_p1, _p2, _p3)

    mapSeekPointOnVectorGeoWGS84_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekPointOnVectorGeoWGS84', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSeekPointOnVectorGeoWGS84(_base: ctypes.POINTER(maptype.DOUBLEPOINT), _angle: float, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _target: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Определение положения проекции точки на векторе, заданном точкой и азимутом
        
        :param _base: координаты точки основания вектора в радианах в системе ``WGS84`` (широта, долгота)
        
        :param _angle: азимут (угол от касательной к меридиану в базовой точке до направления вектора по часовой стрелке)
        
        :param _point: координаты точки, для которой строится проекция на вектор, в радианах системе ``WGS84``
        
        :param _target: координаты точки проекции на векторе в радианах в системе ``WGS84``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Рекомендуется применять для расстояний менее 3 градусов по долготе
        """
        return mapSeekPointOnVectorGeoWGS84_t (_base, _angle, _point, _target)

    mapGetLineSideForPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetLineSideForPoint', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetLineSideForPoint(_point: ctypes.POINTER(maptype.DOUBLEPOINT), _first: ctypes.POINTER(maptype.DOUBLEPOINT), _last: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Определить положение точки относительно прямой
        
        :param _point: координаты точки в метрах в системе координат документа
        
        :param _first: координаты первой точки отрезка на линии в метрах в системе координат документа
        
        :param _last: координаты второй точки отрезка на линии в метрах в системе координат документа Возвращаемое значение: ``1`` - точка слева, ``0`` - точка справа или на линии
        """
        return mapGetLineSideForPoint_t (_point, _first, _last)

    mapGetDirectionAngle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetDirectionAngle', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapGetDirectionAngle(_point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        """
        Вычисление дирекционного угла по двум точкам
        
        :param _point1: координаты точки ``1`` в метрах в заданной плоской прямоугольной системе координат
        
        :param _point2: координаты точки ``2`` в метрах в заданной плоской прямоугольной системе координат
        
        :returns: Возвращает величину угла в радианах между направлением на север (вертикаль) и направлением от первой точки до второй Дирекционный угол зависит от текущей системы координат документа При ошибке возвращает ноль
        :rtype: float
        """
        return mapGetDirectionAngle_t (_point1, _point2)

    mapSetLineLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetLineLength', ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_double, ctypes.c_long)
    def mapSetLineLength(_x1: ctypes.POINTER(ctypes.c_double), _y1: ctypes.POINTER(ctypes.c_double), _x2: ctypes.POINTER(ctypes.c_double), _y2: ctypes.POINTER(ctypes.c_double), _delta: float, _number: int) -> int:
        """
        Установить заданную длину отрезка между точками с исходными координатами x1,y1 и x2,y2
        
        :param _x1: координата первой точки в метрах на север в системе координат документа
        
        :param _y1: координата первой точки в метрах на восток в системе координат документа
        
        :param _x2: координата второй точки в метрах на север в системе координат документа
        
        :param _y2: координата второй точки в метрах на восток в системе координат документа
        
        :param _delta: новое расстояние в соответствии с котором по вектору сдвигается ``1``-я или ``2``-я точка
        
        :param _number: номер редактируемой точки: ``1`` или ``2`` Для определения координат выполняются геометрические вычисления Для выполнения геодезических вычислений применяется функция mapDirectPositionComputation()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetLineLength_t (_x1, _y1, _x2, _y2, _delta, _number)

    mapSeekNormalInMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekNormalInMap', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double)
    def mapSeekNormalInMap(_p1: ctypes.POINTER(maptype.DOUBLEPOINT), _p2: ctypes.POINTER(maptype.DOUBLEPOINT), _forwleft: ctypes.POINTER(maptype.DOUBLEPOINT), _forwright: ctypes.POINTER(maptype.DOUBLEPOINT), _backleft: ctypes.POINTER(maptype.DOUBLEPOINT), _backright: ctypes.POINTER(maptype.DOUBLEPOINT), _size: float) -> int:
        """
        Построить перпендикуляры к отрезку, заданному двумя точками (p1 и p2)
        
        :param _p1: координаты первой точки отрезка в метрах
        
        :param _p2: координаты второй точки отрезка в метрах
        
        :param _forwleft: поле для записи координат левого перпендикуляра от второй точки или ``0``
        
        :param _forwright: поле для записи координат правого перпендикуляра от второй точки или ``0``
        
        :param _backleft: поле для записи координат левого перпендикуляра от первой точки или ``0``
        
        :param _backright: поле для записи координат правого перпендикуляра от первой точки или ``0``
        
        :param _size: длина перпендикуляров в метрах Построения производятся в координатах карты, без пересчета длины с учетом проекции
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSeekNormalInMap_t (_p1, _p2, _forwleft, _forwright, _backleft, _backright, _size)

    mapCloseMapAccess_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCloseMapAccess')
    def mapCloseMapAccess() -> int:
        """
        Освободить ресурсы ядра перед закрытием приложения и
        
        освобождением библиотеки ``"gis64acces.dll"``
        """
        return mapCloseMapAccess_t ()

    mapGetTheTimeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetTheTimeUn', maptype.PWCHAR, ctypes.c_long)
    def mapGetTheTimeUn(_buffer: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить текущее время в формате "HH:MM:SS" в кодировке UTF16
        
        :param _buffer: адрес памяти для размещения результата запроса
        
        :param _size: размер выделенной памяти в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetTheTimeUn_t (_buffer.buffer(), _size)

    mapGetTheTime_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetTheTime', ctypes.c_char_p, ctypes.c_long)
    def mapGetTheTime(_buffer: ctypes.c_char_p, _size: int) -> int:
        """
        Запросить текущее время в формате "HH:MM:SS"
        
        :param _buffer: адрес памяти для размещения результата запроса
        
        :param _size: размер выделенной памяти в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetTheTime_t (_buffer, _size)

    mapCheckFileExUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckFileExUn', maptype.PWCHAR)
    def mapCheckFileExUn(_name: mapsyst.WTEXT) -> int:
        """
        Определить тип файла по его имени
        
        :param _name: полный путь к файлу Анализируются первые ``4`` байта, содержащие идентификатор данных
        
        :returns: При ошибке возвращает ноль, иначе - идентификатор файла: FILE_SXF, FILE_MAP, FILE_MTW, ... Дополнительно различает MAP (FILE_MAP) и SIT (FILE_MAPSIT) Имя может быть в виде ALIAS#XXXX для карт на ГИС Сервере
        :rtype: int
        """
        return mapCheckFileExUn_t (_name.buffer())

    mapGetFileNameForRefFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetFileNameForRefFile', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapGetFileNameForRefFile(_name: mapsyst.WTEXT, _outname: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить реальный путь к файлу по пути к файлу, который может быть ссылкой
        
        :param _name: полный путь к файлу
        
        :param _outname: буфер для записи пути к реальному файлу (совпадает с исходным или определен из записи ``".ref"``)
        
        :param _size: размер буфера в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если в файле строка ``".ref путь или URL"`` - вернет реальный путь или URL
           Строка .ref в файле должна быть в кодировке UTF-8
        """
        return mapGetFileNameForRefFile_t (_name.buffer(), _outname.buffer(), _size)

    mapCompareFiles_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCompareFiles', maptype.PWCHAR, maptype.PWCHAR)
    def mapCompareFiles(_first: mapsyst.WTEXT, _second: mapsyst.WTEXT) -> int:
        """
        Сравнить содержимое файлов
        
        :param _first: полный путь к первому файлу
        
        :param _second: полный путь ко второму файлу Дата и время обновления файлов игнорируются
        
        :returns: При несовпадении возвращает ноль, иначе - ненулевое значение
        :rtype: int
        """
        return mapCompareFiles_t (_first.buffer(), _second.buffer())

    mapGetFolderFromPath_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetFolderFromPath', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def mapGetFolderFromPath(_path: mapsyst.WTEXT, _folder: mapsyst.WTEXT, _size: int) -> int:
        """
        Выделить имя крайней папки из пути
        
        :param _path: путь к папке, который завершается символом прямой '\\\\' или обратный слэш '/'
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetFolderFromPath_t (_path.buffer(), _folder.buffer(), _size)

    mapSetPathShellUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetPathShellUn', maptype.PWCHAR)
    def mapSetPathShellUn(_path: mapsyst.WTEXT) -> ctypes.c_void_p:
        """
        Установить путь к директории приложения
        
        :param _path: путь к директории (папке) приложения В директории приложения располагаются вспомогательные файлы для функционирования ГИС-ядра: библиотеки ядра, библиотеки отрисовки программируемых знаков ``*.iml``, файлы базы данных epsg.``*`` и другие файлы
        
        .. note::

           Рекомендуется устанавливать путь при запуске приложения
        """
        return mapSetPathShellUn_t (_path.buffer())

    mapGetPathShellUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapGetPathShellUn', maptype.PWCHAR, ctypes.c_long)
    def mapGetPathShellUn(_path: mapsyst.WTEXT, _size: int) -> ctypes.c_void_p:
        """
        Запросить путь к директории приложения
        
        :param _path: буфер для записи пути к директории (папке) приложения
        
        :param _size: длина буфера в байтах
        """
        return mapGetPathShellUn_t (_path.buffer(), _size)

    mapSetIniPathUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetIniPathUn', maptype.PWCHAR)
    def mapSetIniPathUn(_inipath: mapsyst.WTEXT) -> ctypes.c_void_p:
        """
        Установить новое имя INI-файла приложения
        
        :param _inipath: полнй путь к ini-файлу приложения, в котором будут запоминаться параметры сеанса работы
        """
        return mapSetIniPathUn_t (_inipath.buffer())

    mapGetIniPathUn_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapGetIniPathUn')
    def mapGetIniPathUn() -> ctypes.POINTER(maptype.WCHAR):
        """
        Запросить имя INI-файла приложения
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapGetIniPathUn_t ()

    mapGetCommonIniPath_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapGetCommonIniPath')
    def mapGetCommonIniPath() -> ctypes.POINTER(maptype.WCHAR):
        """
        Запросить путь к общей папке файлов параметров задач приложения (INI, XML)
        
        Пример возращаемой строки: ``"c:\\Users\\Public\\Documents\\Panorama\\"``,  ``"/var/Panorama/"``
        
        :returns: При ошибке возвращает "" (пустую строку)
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapGetCommonIniPath_t ()

    mapSetCommonIniPath_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapSetCommonIniPath', maptype.PWCHAR)
    def mapSetCommonIniPath(_path: mapsyst.WTEXT) -> int:
        """
        Установить путь к общей папке файлов параметров задач системы (INI, XML)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetCommonIniPath_t (_path.buffer())

    mapGetApplicationCommonIniPath_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetApplicationCommonIniPath', maptype.PWCHAR, ctypes.c_long)
    def mapGetApplicationCommonIniPath(_path: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить путь к общей папке файлов параметров задач приложения с учетом версии (INI, XML)
        
        :param _path: адрес буфера для записи пути
        
        :param _size: размер буфера в байтах Добавляет к пути mapGetCommonIniPath имя папки приложения mapGetAppFolderName и старшие цифры номера версии Пример возращаемой строки: ``"c:\\Users\\Public\\Documents\\Panorama\\Panorama15\\"``,  ``"/var/Panorama/Panorama15/"``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetApplicationCommonIniPath_t (_path.buffer(), _size)

    mapGetUserIniPath_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetUserIniPath', maptype.PWCHAR, ctypes.c_long)
    def mapGetUserIniPath(_path: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить путь к пользовательской папке файлов параметров задач приложения (INI, XML)
        
        :param _path: адрес буфера для записи пути
        
        :param _size: размер буфера в байтах Пример возращаемой строки: ``"c:\\Users\\<User>\\Application Data\\Roaming\\Panorama15\\"``,  ``"/home/user/.panorama/"`` <User> - имя пользователя в системе
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetUserIniPath_t (_path.buffer(), _size)

    mapGetDBConnectionListFileName_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapGetDBConnectionListFileName')
    def mapGetDBConnectionListFileName() -> ctypes.POINTER(maptype.WCHAR):
        """
        Запросить полный путь к файлу соединений с БД
        
        Пример возращаемой строки: ``"c:\\Users\\Имя_пользователя\\Application Data\\Panorama15\\dbmlist.xml"``
        или ``"/home/имя_пользователя/panorama15/dbmlist.xml"``
        
        :returns: При ошибке возвращает "" (пустую строку)
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapGetDBConnectionListFileName_t ()

    mapSetDBConnectionListFileName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetDBConnectionListFileName', maptype.PWCHAR)
    def mapSetDBConnectionListFileName(_path: mapsyst.WTEXT) -> int:
        """
        Установить полный путь к файлу соединений с БД и проверить его наличие
        
        :param _path: полный путь к файлу
        
        .. note::

           Если путь не задан, то он будет сгенерирован по умолчанию:
           ``"c:\\Users\\Имя_пользователя\\Application Data\\Panorama15\\dbmlist.xml"`` или
           ``"/home/имя_пользователя/panorama15/dbmlist.xml"``
           При отсутствии файла заданный путь будет установлен, но функция вернет ноль
        """
        return mapSetDBConnectionListFileName_t (_path.buffer())

    mapGetMapIniNameEx_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapGetMapIniNameEx', maptype.HMAP)
    def mapGetMapIniNameEx(_hmap: maptype.HMAP) -> ctypes.POINTER(maptype.WCHAR):
        """
        Запросить имя INI-файла документа
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает пустую строку
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapGetMapIniNameEx_t (_hmap)

    mapGetMapIniNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMapIniNameUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapGetMapIniNameUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить имя INI-файла документа
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _name: адрес строки для размещения результата
        
        :param _size: размер строки в байтах
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapGetMapIniNameUn_t (_hmap, _name.buffer(), _size)

    mapSetCommonRscPathUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetCommonRscPathUn', maptype.PWCHAR)
    def mapSetCommonRscPathUn(_rscpath: mapsyst.WTEXT) -> int:
        """
        Установить путь к общим файлам классификаторам (RSC)
        
        :param _rscpath: путь к общим файлам классификаторам (``RSC``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetCommonRscPathUn_t (_rscpath.buffer())

    mapGetCommonRscPathUn_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapGetCommonRscPathUn')
    def mapGetCommonRscPathUn() -> ctypes.POINTER(maptype.WCHAR):
        """
        Запросить путь к общим файлам классификаторам (RSC)
        
        :returns: При ошибке возвращает пустую строку
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapGetCommonRscPathUn_t ()

    mapSetCommonRscHost_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapSetCommonRscHost', ctypes.c_char_p)
    def mapSetCommonRscHost(_rschost: ctypes.c_char_p) -> ctypes.POINTER(ctypes.c_char):
        """
        Установить имя хоста для согласования общей папки классификаторов на ГИС Сервере
        
        :param _rschost: имя хоста или ``IP``-адрес
        """
        return mapSetCommonRscHost_t (_rschost)

    mapGetCommonRscHost_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetCommonRscHost')
    def mapGetCommonRscHost() -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить имя хоста для согласования общей папки классификаторов на ГИС Сервере
        """
        return mapGetCommonRscHost_t ()

    mapIsNormalPathUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsNormalPathUn', maptype.PWCHAR)
    def mapIsNormalPathUn(_name: mapsyst.WTEXT) -> int:
        """
        Проверить, что имя файла не является алиасом сервера или геопортала
        
        :returns: При отсутствии спецсимволов возвращает ненулевое значение
        :rtype: int
        """
        return mapIsNormalPathUn_t (_name.buffer())

    mapAliasToNormalNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAliasToNormalNameUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def mapAliasToNormalNameUn(_alias: mapsyst.WTEXT, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Преобразовать имя алиаса или соединения с сервисом в имя файла (без пути)
        
        :param _alias: имя алиаса или соединения с сервисом (``WMS``, ``WFS``, ``WCS``)
        
        :param _name: адрес строки для размещения результата
        
        :param _size: размер выделенной памяти в строке в байтах Длина имени c расширением усекается до ``204`` символов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapAliasToNormalNameUn_t (_alias.buffer(), _name.buffer(), _size)

    mapBuildShortNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapBuildShortNameUn', maptype.PWCHAR, maptype.PWCHAR)
    def mapBuildShortNameUn(_templ: mapsyst.WTEXT, _name: mapsyst.WTEXT) -> ctypes.POINTER(maptype.WCHAR):
        """
        Построить "короткое" имя файла
        
        :param _templ: эталонный путь, относительно которого строится короткий путь например, путь к библиотекам приложения - mapGetPathShellUn()
        
        :param _name: исходное полное имя файла
        
        :returns: Возвращает указатель на ``"короткое"`` имя файла При ошибке возвращает ноль
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapBuildShortNameUn_t (_templ.buffer(), _name.buffer())

    mapBuildShellShortNameUnicode_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapBuildShellShortNameUnicode', maptype.PWCHAR)
    def mapBuildShellShortNameUnicode(_name: mapsyst.WTEXT) -> ctypes.POINTER(maptype.WCHAR):
        """
        Построить "короткое" имя файла
        
        :param _name: полное имя файла В качестве эталонного пути применяется путь к библиотекам приложения - mapGetPathShellUn()
        
        :returns: Возвращает указатель на ``"короткое"`` имя файла При ошибке возвращает ноль
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapBuildShellShortNameUnicode_t (_name.buffer())

    mapBuildLongNameEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBuildLongNameEx', maptype.PWCHAR, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def mapBuildLongNameEx(_templ: mapsyst.WTEXT, _name: mapsyst.WTEXT, _path: mapsyst.WTEXT, _size: int) -> int:
        """
        Построить "длинное" имя файла (полный путь к файлу)
        
        :param _templ: эталонный путь, относительно которого строится полный путь, например, путь к библиотекам приложения - mapGetPathShellUn()
        
        :param _name: исходный короткий путь к файлу; например, имя_папки/имя_файла или ../имя_папки/имя_файла и тому подобное
        
        :param _path: указатель на буфер для размещения полного пути к файлу
        
        :param _size: размер буфера в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapBuildLongNameEx_t (_templ.buffer(), _name.buffer(), _path.buffer(), _size)

    mapGetFileCrc32_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetFileCrc32', maptype.PWCHAR, ctypes.POINTER(ctypes.c_uint))
    def mapGetFileCrc32(_filename: mapsyst.WTEXT, _value32: ctypes.POINTER(ctypes.c_uint)) -> int:
        """
        Подсчитать контрольную сумму файла по алгоритму CRC32
        
        :param _filename: полный путь к файлу
        
        :param _value32: поле для записи результата подсчета
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetFileCrc32_t (_filename.buffer(), _value32)

    mapGetRecordCrc32_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRecordCrc32', ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_uint))
    def mapGetRecordCrc32(_buffer: ctypes.c_char_p, _size: int, _value32: ctypes.POINTER(ctypes.c_uint)) -> int:
        """
        Подсчитать контрольную сумму записи по алгоритму CRC32
        
        :param _buffer: адрес записи
        
        :param _size: длина записи в байтах
        
        :param _value32: текущее значение контрольной суммы и новый результат с учетом переданного буфера При первом обращении поле value32 нужно обнулить
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetRecordCrc32_t (_buffer, _size, _value32)

    mapSaveFilesToZip_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSaveFilesToZip', maptype.PWCHAR, ctypes.POINTER(ctypes.POINTER(maptype.WCHAR)), ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapSaveFilesToZip(_zipname: mapsyst.WTEXT, _filelist: ctypes.POINTER(ctypes.POINTER(maptype.WCHAR)), _count: int, _flag: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Сохранить в архиве список файлов
        
        :param _zipname: имя zip-архива
        
        :param _filelist: массив указателей на пути к файлам
        
        :param _count: число сохраняемых файлов (элементов массива указателей)
        
        :param _flag: управляющие флажки: ``1`` - записывать относительные пути в архив или ``0``
        
        :param _error: поле для записи ошибки выполнения программы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если файл один или все файлы в одной папке, то они сохраняются без пути
           Если файлы размещены в поддиректориях одной папки, то они сохраняются с относительными путями
           Если файлы не имеют общего пути, то они сохраняются без пути
        """
        return mapSaveFilesToZip_t (_zipname.buffer(), _filelist, _count, _flag, _error)

    mapUnzipFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapUnzipFile', ctypes.c_char_p, ctypes.c_ulong, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapUnzipFile(_source: ctypes.c_char_p, _sourcesize: int, _zipfile: int, _error: ctypes.POINTER(ctypes.c_long)) -> ctypes.c_void_p:
        """
        Распаковать файл из ZIP-архива в памяти
        
        :param _source: адрес упакованного ``ZIP``-архива в памяти
        
        :param _sourcesize: размер упакованного архива в байтах
        
        :param _zipfile: номер распаковываемого файла в Zip-архиве с ``1``
        
        :param _error: поле для записи ошибки распаковки
        
        :returns: Возвращает идентификатор распакованного файла в памяти Для чтения данных необходимо вызвать mapGetUnzipFilePoint и mapFreeUnzipFile При ошибке возвращает ноль
        """
        return mapUnzipFile_t (_source, _sourcesize, _zipfile, _error)

    mapGetUnzipFilePoint_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetUnzipFilePoint', ctypes.c_void_p, ctypes.POINTER(ctypes.c_long))
    def mapGetUnzipFilePoint(_hunzipfile: ctypes.c_void_p, _size: ctypes.POINTER(ctypes.c_long)) -> ctypes.POINTER(ctypes.c_char):
        """
        Чтение распакованного файла из ZIP-архива после распаковки mapUnzipFile
        
        :param _hunzipfile: идентификатор распакованного файла в памяти
        
        :param _size: поле, в которое запишется длина файла в памяти
        
        :returns: Возвращает указатель на начало записи файла в памяти При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetUnzipFilePoint_t (_hunzipfile, _size)

    mapFreeUnzipFile_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeUnzipFile', ctypes.c_void_p)
    def mapFreeUnzipFile(_hunzipfile: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Освободить ресурсы распакованного файла в mapUnzipFile
        
        :param _hunzipfile: идентификатор распакованного файла в памяти
        """
        return mapFreeUnzipFile_t (_hunzipfile)

    mapMessageEnable_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapMessageEnable', ctypes.c_long)
    def mapMessageEnable(_enable: int) -> int:
        """
        Запретить выдачу сообщений на экран (серверный режим работы)
        
        :param _enable: флаг разрешения (``1``) или запрета (``0``) выдачи сообщений При выполнении автоматических процедур без диалогов с оператором выдача сообщений должна быть запрещена
        
        :returns: Возвращает предыдущее значение флага
        :rtype: int
        """
        return mapMessageEnable_t (_enable)

    mapIsMessageEnable_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsMessageEnable')
    def mapIsMessageEnable() -> int:
        """
        Запросить, разрешена ли выдача сообщений
        """
        return mapIsMessageEnable_t ()

    mapMessageEnableForThread_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapMessageEnableForThread', ctypes.c_long)
    def mapMessageEnableForThread(_enable: int) -> ctypes.c_void_p:
        """
        :param _enable: флаг разрешения (``1``) или запрета (``0``) выдачи сообщений При выполнении автоматических процедур без диалогов с оператором выдача сообщений должна быть запрещена
        """
        return mapMessageEnableForThread_t (_enable)

    mapIsMessageEnableForThread_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsMessageEnableForThread')
    def mapIsMessageEnableForThread() -> int:
        """
        Запросить признак разрешения выдачи сообщений на экран для текущего потока
        """
        return mapIsMessageEnableForThread_t ()

    mapErrorMessageLog_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapErrorMessageLog', maptype.HWND, ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapErrorMessageLog(_hwnd: maptype.HWND, _code: int, _filename: mapsyst.WTEXT, _message: mapsyst.WTEXT, _size: int, _isshow: int) -> ctypes.c_void_p:
        """
        Выдать сообщение об ошибке (на экран)
        
        :param _hwnd: идентификатор родительского окна для выдачи сообщения или ``0``
        
        :param _code: код ошибки (maperr.rh)
        
        :param _filename: имя файла (объекта), для которого возникла ошибка
        
        :param _message: адрес буфера для размещения текста сообщения (для записи в протокол и т.п.), область памяти должна быть не менее длины имени файла + ``256`` байт; значение может быть ``0``
        
        :param _size: длина буфера в байтах
        
        :param _isshow: признак вывода сообщения на экран
        """
        return mapErrorMessageLog_t (_hwnd, _code, _filename.buffer(), _message.buffer(), _size, _isshow)

    mapErrorMessageUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapErrorMessageUn', ctypes.c_long, maptype.PWCHAR)
    def mapErrorMessageUn(_code: int, _filename: mapsyst.WTEXT) -> ctypes.c_void_p:
        """
        Выдать сообщение об ошибке (на экран)
        
        :param _code: код ошибки (maperr.rh)
        
        :param _filename: имя файла (объекта), для которого возникла ошибка
        """
        if (isinstance(_filename, str)):
            return mapErrorMessageUn_t (_code, (_filename + '\0').encode('utf-16LE'))
        return mapErrorMessageUn_t (_code, _filename.buffer())

    mapMessageBoxUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapMessageBoxUn', maptype.HWND, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def mapMessageBoxUn(_hwnd: maptype.HWND, _message: mapsyst.WTEXT, _title: mapsyst.WTEXT, _flag: int) -> int:
        """
        Выдать сообщение на экран через системную функцию MessageBox
        
        :param _hwnd: идентификатор родительского окна для выдачи сообщения или ``0``
        
        :param _message: текст сообщения
        
        :param _title: заголовок сообщения
        
        :param _flag: флажки выбора иконок и кнопок в диалоге сообщения: ``MB_OK``, ``MB_YESNO`` и ``MB_ICONINFORMATION``, ``MB_ICONWARNING``, ``MB_ICONSTOP``
        
        :returns: Если mapIsMessageEnable() равно 0,  то сообщение не выдается и функция возвращает ноль Если установлена функция обратного вызова mapSetMessageBoxCall, то выдача сообщения будет через эту функцию
        :rtype: int
        """
        return mapMessageBoxUn_t (_hwnd, _message.buffer(), _title.buffer(), _flag)

    mapSetMapAccessLanguage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetMapAccessLanguage', ctypes.c_int)
    def mapSetMapAccessLanguage(_code: int) -> ctypes.c_void_p:
        """
        Установить язык сообщений
        
        :param _code: код языка сообщений: ``ML_ENGLISH`` (``1``) - английский, ``ML_RUSSIAN`` (``2``) - русский
        """
        return mapSetMapAccessLanguage_t (_code)

    mapGetMapAccessLanguage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapGetMapAccessLanguage')
    def mapGetMapAccessLanguage() -> int:
        """
        Запросить язык сообщений
        """
        return mapGetMapAccessLanguage_t ()

    mapGetHandleForMessage_t = mapsyst.GetProcAddress(acceslib,maptype.HMESSAGE,'mapGetHandleForMessage')
    def mapGetHandleForMessage() -> maptype.HMESSAGE:
        """
        Запросить идентификатор главного окна для приема сообщений
        
        Может применяться в MS Windows при установке поля Handle в структуре TASKPARMEX для вызова стандартных диалогов
        """
        return mapGetHandleForMessage_t ()

    mapSetTimeStringExUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetTimeStringExUn', ctypes.POINTER(maptype.SYSTEMTIME), ctypes.c_double, ctypes.c_double, maptype.PWCHAR, ctypes.c_long)
    def mapSetTimeStringExUn(_begtime: ctypes.POINTER(maptype.SYSTEMTIME), _total: float, _current: float, _message: mapsyst.WTEXT, _size: int) -> int:
        """
        Расчёт времени выполнения процесса в виде строки "HH:MM:SS / HH:MM:SS",
        
        :param _begtime: временя старта программы,
        
        :param _total: общее число обрабатываемых элементов (например, ``100`` - в процентах),
        
        :param _current: число обработанных элементов (например, выполненный процент работы программы)
        
        :param _message: буфер для записи строки
        
        :param _size: размер буфера в байтах (не менее ``64`` байт) В строке указано прошедшее время и оставшееся до завершения процесса обработки
        
        :returns: При ошибке в параметрах возвращает ноль
        :rtype: int
        """
        return mapSetTimeStringExUn_t (_begtime, _total, _current, _message.buffer(), _size)

    mapMessageToLogEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapMessageToLogEx', maptype.HMAP, maptype.HSITE, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapMessageToLogEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _code: int, _message: mapsyst.WTEXT, _type: int) -> ctypes.c_void_p:
        """
        Записать сообщение в протокол карты по коду ошибки
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в документе, для фоновой карты равен hmap
        
        :param _code: код ошибки (из maperr.rh) или ``0``
        
        :param _message: текст сообщения
        
        :param _type: тип сообщения: ``MT_INFO``, ``MT_ERROR``, ``MT_WARNING``
        """
        return mapMessageToLogEx_t (_hmap, _hsite, _code, _message.buffer(), _type)

    mapMessageToLogPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapMessageToLogPro', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def mapMessageToLogPro(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _message: mapsyst.WTEXT, _messageex: mapsyst.WTEXT, _type: int) -> ctypes.c_void_p:
        """
        Записать сообщение в протокол карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в документе, для фоновой карты равен hmap
        
        :param _message: текст сообщения
        
        :param _messageex: продолжение сообщения или ``0``
        
        :param _type: тип сообщения: ``MT_INFO``, ``MT_ERROR``, ``MT_WARNING``
        """
        return mapMessageToLogPro_t (_hmap, _hsite, _message.buffer(), _messageex.buffer(), _type)

    mapOpenProgressBar_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapOpenProgressBar')
    def mapOpenProgressBar() -> ctypes.c_void_p:
        """
        Открыть линейку progressbar в главном окне приложения
        
        Приложение должно заранее установить идентификатор главного окна функцией mapSetHandleForMessage (ГИС Панорама делает автоматически)
        Для создания линейки необходимо вызвать mapOpenProgressBar, для смены процента вызывается mapProgressBar,
        для скрытия линейки - mapCloseProgressBar
        В один момент времени в главной панели может быть только одна линейка
        
        :returns: При ошибке возвращает ноль, при успешном выполнении возвращает идентификатор линейки
        """
        return mapOpenProgressBar_t ()

    mapProgressBar_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapProgressBar', ctypes.c_void_p, ctypes.c_long, maptype.PWCHAR)
    def mapProgressBar(_progressbar: ctypes.c_void_p, _percent: int, _message: mapsyst.WTEXT) -> int:
        """
        Отобразить линейку progressbar в главном окне приложения
        
        :param _progressbar: идентификатор линейки, полученной в mapOpenProgressBar
        
        :param _percent: процент заполнения линейки от ``0`` до ``100``
        
        :param _message: комментарий к выполняемой операции, отображается на линейке после процентов
        
        :returns: При ошибке возвращает ноль, при успешном выполнении возвращает 1
        :rtype: int
        
        .. note::

           Если оператор желает прервать процесс, функция вернет значение -1
        """
        return mapProgressBar_t (_progressbar, _percent, _message.buffer())

    mapCloseProgressBar_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseProgressBar', ctypes.c_void_p)
    def mapCloseProgressBar(_progressbar: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Закрыть линейку progressbar в главном окне приложения
        
        :param _progressbar: идентификатор линейки, полученной в mapOpenProgressBar
        """
        return mapCloseProgressBar_t (_progressbar)

    mapShowMessage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapShowMessage', maptype.PWCHAR, maptype.PWCHAR)
    def mapShowMessage(_text: mapsyst.WTEXT, _caption: mapsyst.WTEXT) -> ctypes.c_void_p:
        """
        Показать всплывающее информационное сообщение
        
        :param _text: текст сообщения
        
        :param _caption: заголовок сообщения Посылает главному окну приложения сообщение ``AW_MESSAGEBOX`` через mapSendMessage Сообщение гаснет через ``3`` секунды или после нажатия клавиатуры\\мышки
        """
        return mapShowMessage_t (_text.buffer(), _caption.buffer())

    mapShowErrorMessage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapShowErrorMessage', maptype.PWCHAR, maptype.PWCHAR)
    def mapShowErrorMessage(_text: mapsyst.WTEXT, _caption: mapsyst.WTEXT) -> ctypes.c_void_p:
        """
        Показать всплывающее сообщение об ошибке
        
        :param _text: текст сообщения
        
        :param _caption: заголовок сообщения Посылает главному окну приложения сообщение ``AW_ERRORBOX`` через mapSendMessage Сообщение гаснет через ``3`` секунды или после нажатия клавиатуры\\мышки
        """
        return mapShowErrorMessage_t (_text.buffer(), _caption.buffer())

    mapSendMessage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int64,'mapSendMessage', ctypes.c_long, ctypes.c_int64, ctypes.c_int64)
    def mapSendMessage(_command: int, _wparam: int, _lparam: int) -> int:
        """
        Отправить команду главному окну (текущему окну карты)
        
        Приложение должно заранее установить идентификатор главного окна функцией mapSetHandleForMessage (ГИС Панорама делает автоматически)
        
        :param _command: идентификатор команды
        
        :param _wparam: первый параметр
        
        :param _lparam: второй параметр Примеры: перерисовать окно карты: mapSendMessage(``MT_MAPWINPORT``, ``MWP_INVALIDATE``, ``0``); выделить объекты на карте по общим условиям: mapSendMessage(``CM_PAN_SEARCH``, ``1``, ``0``);
        """
        return mapSendMessage_t (_command, _wparam, _lparam)

    mapDateToLongUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDateToLongUn', maptype.PWCHAR)
    def mapDateToLongUn(_date: mapsyst.WTEXT) -> int:
        """
        Преобразовать дату из строки в число ГГГГММДД
        
        :param _date: исходная строка с датой Строка может иметь вид ДД/ММ/ГГГГ или ДД.ММ.ГГГГ или ГГГГММДД или ГГГГ/ММ/ДД или ГГГГ-ММ-ДД
        
        :returns: При ошибке возвращает ноль, иначе - значение даты в виде числа
        :rtype: int
        """
        return mapDateToLongUn_t (_date.buffer())

    mapLongToDateUn_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapLongToDateUn', ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapLongToDateUn(_number: int, _date: mapsyst.WTEXT, _size: int) -> ctypes.POINTER(maptype.WCHAR):
        """
        Преобразовать дату из из числа ГГГГММДД в строку ДД/ММ/ГГГГ
        
        :param _number: числовое значение даты
        
        :param _date: адрес буфера для записи строки с датой
        
        :param _size: размер буфера в байтах
        
        :returns: При ошибке возвращает ноль, иначе - адрес входной строки
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapLongToDateUn_t (_number, _date.buffer(), _size)

    mapTimeToLongUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapTimeToLongUn', maptype.PWCHAR)
    def mapTimeToLongUn(_time: mapsyst.WTEXT) -> int:
        """
        Преобразовать время из строки в число ЧЧММСС
        
        :param _time: исходная строка со временем Строка может иметь вид ЧЧ:ММ:СС
        
        :returns: При ошибке возвращает ноль, иначе - значение времени в виде числа
        :rtype: int
        """
        return mapTimeToLongUn_t (_time.buffer())

    mapLongToDoubleTime_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapLongToDoubleTime', ctypes.c_long, ctypes.c_char_p, ctypes.c_long)
    def mapLongToDoubleTime(_number: int, _time: ctypes.c_char_p, _size: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Преобразовать время из числа ЧЧММСС в строку с системным и локальным временем
        
        :param _number: числовое значение времени
        
        :param _time: адрес буфера для записи результата
        
        :param _size: размер буфера в байтах Строка будет иметь вид ЧЧ:ММ:СС (ЧЧ:ММ:СС) - значение в скобках содержит локальное время
        
        :returns: При ошибке возвращает ноль, иначе - адрес входной строки
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapLongToDoubleTime_t (_number, _time, _size)

    mapLongToTimeUn_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapLongToTimeUn', ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapLongToTimeUn(_number: int, _time: mapsyst.WTEXT, _size: int) -> ctypes.POINTER(maptype.WCHAR):
        """
        Преобразовать время из числа ЧЧММСС в строку ЧЧ:ММ:СС
        
        :param _number: числовое значение времени
        
        :param _time: адрес буфера для записи результата
        
        :param _size: размер буфера в байтах
        
        :returns: При ошибке возвращает ноль, иначе - адрес входной строки
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapLongToTimeUn_t (_number, _time.buffer(), _size)

    mapAngleToRadianUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapAngleToRadianUn', maptype.PWCHAR)
    def mapAngleToRadianUn(_angle: mapsyst.WTEXT) -> float:
        """
        Преобразовать угловую величину в градусах из строки в числовое значение в радианах
        
        :param _angle: исходная строка с угловой величиной Строка может иметь вид ГГГ°ММ'``CC``.``CC``" или ГГГ.ГГГГГГГГ° Для Linux вместо символа ° (\\xB0) д.б. ^
        
        :returns: При ошибке возвращает ноль, иначе - значение в радианах
        :rtype: float
        """
        return mapAngleToRadianUn_t (_angle.buffer())

    mapRadianToAngleUn_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapRadianToAngleUn', ctypes.c_double, maptype.PWCHAR, ctypes.c_int)
    def mapRadianToAngleUn(_radian: float, _angle: mapsyst.WTEXT, _size: int) -> ctypes.POINTER(maptype.WCHAR):
        """
        Преобразовать числовое значение из радиан в строку вида ГГГ°ММ'CC.CC"
        
        :param _radian: исходное значение в радианах
        
        :param _angle: адрес буфера для записи результата
        
        :param _size: размер буфера в байтах Для Linux вместо символа ° (\\xB0) д.б. ^
        
        :returns: При ошибке возвращает ноль, иначе - адрес входной строки
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapRadianToAngleUn_t (_radian, _angle.buffer(), _size)

    ConvertStringToXmlStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'ConvertStringToXmlStringUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def ConvertStringToXmlStringUn(_instring: mapsyst.WTEXT, _outval: mapsyst.WTEXT, _outsize: int) -> int:
        """
        Сконвертировать значение строки, убрав спецсимволы XML ('\\"', '?', '>', '<', '&', '\\'' '\\n')
        
        :param _instring: входная строка outstring - выходная строка (&quot; и т.д.)
        
        :param _outsize: размер выходной строки в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return ConvertStringToXmlStringUn_t (_instring.buffer(), _outval.buffer(), _outsize)

    ConvertStringToJsonStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'ConvertStringToJsonStringUn', maptype.PWCHAR)
    def ConvertStringToJsonStringUn(_inval: mapsyst.WTEXT) -> ctypes.c_void_p:
        """
        Сконвертировать значение строки, заменив спецсимволы JSON ('\\"', '\\n', '\\r', '\\v', '\\\\', '\\t')
        
        :param _inval: обрабатываемая строка в кодировке ``UTF16``, заканчивающаяся символом конца строки Заменяет '\\"' на '\\'', а остальные спецсимволы на пробелы
        """
        return ConvertStringToJsonStringUn_t (_inval.buffer())

    ShieldStringToJsonStringUnEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'ShieldStringToJsonStringUnEx', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def ShieldStringToJsonStringUnEx(_instring: mapsyst.WTEXT, _outstring: mapsyst.WTEXT, _outsize: int) -> ctypes.c_void_p:
        """
        Экранировать спецсимволы строки JSON ('\\"', '\\n', '\\r', '\\v', '\\\\', '\\t')
        
        :param _instring: обрабатываемая строка в кодировке ``UTF16``, заканчивающаяся символом конца строки
        
        :param _outstring: выходная строка
        
        :param _outsize: размер выходной строки в байтах
        """
        return ShieldStringToJsonStringUnEx_t (_instring.buffer(), _outstring.buffer(), _outsize)

    ConvertJsonStringToStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'ConvertJsonStringToStringUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def ConvertJsonStringToStringUn(_instring: mapsyst.WTEXT, _outstring: mapsyst.WTEXT, _outsize: int) -> ctypes.c_void_p:
        """
        Убрать экранирующие слеши
        
        :param _instring: обрабатываемая строка
        
        :param _outstring: выходная строка
        
        :param _outsize: размер выходной строки в байтах
        
        :returns: Возвращает количество убранных символов
        """
        return ConvertJsonStringToStringUn_t (_instring.buffer(), _outstring.buffer(), _outsize)

    ConvertFromXmlToStringUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'ConvertFromXmlToStringUn', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def ConvertFromXmlToStringUn(_instring: mapsyst.WTEXT, _outstring: mapsyst.WTEXT, _outsize: int) -> int:
        """
        Сконвертировать значение строки, восстановив спецсимволы XML
        
        :param _instring: входная строка outtext - выходная строка
        
        :param _outsize: размер выходной строки в байтах
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return ConvertFromXmlToStringUn_t (_instring.buffer(), _outstring.buffer(), _outsize)

    mapBase64Encode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBase64Encode', ctypes.POINTER(ctypes.c_void_p), ctypes.c_long, ctypes.c_char_p, ctypes.c_long)
    def mapBase64Encode(_srcdata: ctypes.POINTER(ctypes.c_void_p), _srclength: int, _result: ctypes.c_char_p, _resultlength: int) -> int:
        """
        Закодировать данные в base64
        
        :param _srcdata: указатель на буфер с исходными данными для кодирования
        
        :param _srclength: размер исходных данных в байтах
        
        :param _result: указатель на выходной буфер в кодировке base64
        
        :param _resultlength: размер выделенной памяти в выходном буфере в байтах
        
        :returns: Возвращает длину выходного буфера вместе с замыкающим нулем Если буфер не задан или его длина меньше требуемой, то вернется требуемая длина выходного буфера При ошибке возвращает ноль
        :rtype: int
        """
        return mapBase64Encode_t (_srcdata, _srclength, _result, _resultlength)

    mapBase64Decode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBase64Decode', ctypes.c_char_p, ctypes.c_long, ctypes.POINTER(ctypes.c_byte), ctypes.c_long)
    def mapBase64Decode(_srcdata: ctypes.c_char_p, _srclength: int, _result: ctypes.POINTER(ctypes.c_byte), _resultlength: int) -> int:
        """
        Раскодировать данные из base64
        
        :param _srcdata: указатель на буфер с исходными данными для раскодирования
        
        :param _srclength: размер исходных данных в байтах
        
        :param _result: указатель на выходной буфер в кодировке base64 resultSize - размер выделенной памяти в выходном буфере в байтах
        
        :returns: Возвращает длину выходного буфера вместе с замыкающим нулем Если буфер не задан или его длина меньше требуемой, то вернется требуемая длина выходного буфера При ошибке возвращает ноль
        :rtype: int
        """
        return mapBase64Decode_t (_srcdata, _srclength, _result, _resultlength)

    mapSetPythonLibraryPath_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetPythonLibraryPath', maptype.PWCHAR)
    def mapSetPythonLibraryPath(_pythondirectory: mapsyst.WTEXT) -> int:
        """
        Установить до начала работы с python путь к папке с библиотеками Python
        
        :param _pythondirectory: путь к каталогу, который содержит библиотеку Python и установленные пакеты расширений
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если эта функция не была вызвана, то интерпретатор запускается из директории, заданой в ОС по умолчанию
        """
        return mapSetPythonLibraryPath_t (_pythondirectory.buffer())

    mapSetPythonInterpreter_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetPythonInterpreter', maptype.PWCHAR)
    def mapSetPythonInterpreter(_pythoninterpreter: mapsyst.WTEXT) -> int:
        """
        Установить до начала работы с python путь к исполняемому файлу интерпретатора Python
        
        :param _pythoninterpreter: полный путь к исполняемому файлу интерпретатора Python
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если функции mapSetPythonInterpreter или не были mapSetPythonLibraryPath вызваны,
           то интерпретатор запускается из директории, заданой в ОС по умолчанию
           Для выбора другого интерпретатора Python необходимо завершить приложение
           Функция является альтернативной для функции mapSetPythonLibraryPath
        """
        return mapSetPythonInterpreter_t (_pythoninterpreter.buffer())

    mapRunPythonFromBuf_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRunPythonFromBuf', ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_double))
    def mapRunPythonFromBuf(_buffer: ctypes.c_char_p, _function: ctypes.c_char_p, _args: ctypes.POINTER(ctypes.c_void_p), _error: ctypes.POINTER(ctypes.c_long), _value: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Выполнить на python скрипт из строкового буфера
        
        :param _buffer: адрес строки со скриптом
        
        :param _function: имя выполняемой функции на python вида def Function(args) -> float:
        
        :param _args: идентификатор объекта, передаваемого в функцию в качестве аргумента
        
        :param _error: возвращаемый код ошибки выполнения скрипта
        
        :param _value: адрес переменной для записи результата
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapRunPythonFromBuf_t (_buffer, _function, _args, _error, _value)

    mapCallPython_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCallPython', maptype.HMAP, maptype.HOBJ, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_double))
    def mapCallPython(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _path: mapsyst.WTEXT, _function: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_long), _value: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Выполнить скрипт на python и вернуть результат вычислений
        
        :param _hmap: идентификатор открытого документа
        
        :param _hobj: идентификатор выбранного объекта или ноль
        
        :param _path: полный путь к файлу py, содержащему код скрипта на python
        
        :param _function: имя выполняемой функции на python вида def Function(hmap:``HMAP``, hobj:``HOBJ``) -> float:
        
        :param _error: возвращаемый код ошибки выполнения скрипта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCallPython_t (_hmap, _hobj, _path.buffer(), _function.buffer(), _error, _value)

    mapCallTaskPython_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCallTaskPython', ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_double))
    def mapCallTaskPython(_hident: ctypes.POINTER(ctypes.c_void_p), _parm: ctypes.POINTER(ctypes.c_void_p), _path: mapsyst.WTEXT, _function: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_long), _value: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Выполнить скрипт на python из прикладной задачи и вернуть результат вычислений
        
        :param _hident: идентификатор объекта прикладной задачи или ноль
        
        :param _parm: указатель на параметры скрипта или ноль
        
        :param _path: полный путь к файлу py, содержащему код скрипта на python
        
        :param _function: имя выполняемой функции на python вида def Function(hmap:``HMAP``, hobj:``HOBJ``) -> float:
        
        :param _error: возвращаемый код ошибки выполнения скрипта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCallTaskPython_t (_hident, _parm, _path.buffer(), _function.buffer(), _error, _value)

    mapGetPythonVersion_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetPythonVersion', maptype.PWCHAR, ctypes.c_int)
    def mapGetPythonVersion(_versionString: mapsyst.WTEXT, _size: int) -> int:
        """
        Получить строку версии активного интерпретатора Python
        
        :param _versionString: адрес строки для записи версии
        
        :param _size: размер строки в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetPythonVersion_t (_versionString.buffer(), _size)

    mapClosePython_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapClosePython')
    def mapClosePython() -> ctypes.c_void_p:
        """
        Закрыть текущую сессию интерпретатора Python
        
        Применяется при необходимости отредактировать скрипты, которые запускались в сеансе работы
        """
        return mapClosePython_t ()

    mapDebugPython_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDebugPython', maptype.HMAP, maptype.HOBJ, maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long))
    def mapDebugPython(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _path: mapsyst.WTEXT, _function: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Выполнить скрипт из указанного файла с заданным именем функции и параметром HMAP в режиме отладки
        
        :param _hmap: идентификатор открытого документа
        
        :param _hobj: идентификатор выбранного объекта или ноль
        
        :param _path: полный путь к файлу py, содержащему код скрипта на python
        
        :param _function: имя выполняемой функции на python вида def Function(hmap:``HMAP``, hobj:``HOBJ``) -> float:
        
        :param _error: возвращаемый код ошибки выполнения скрипта Вызывает команду: pythonw.exe idle.pyw debug_имя_скрипта.py
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDebugPython_t (_hmap, _hobj, _path.buffer(), _function.buffer(), _error)

    mapFindPathExePython_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapFindPathExePython', maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapFindPathExePython(_pathexe: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Найти путь к программе запуска скрипта pythonw.exe
        
        :param _pathexe: возвращаемый полный путь к pythonw.exe
        
        :param _size: размер строки pathexe в байтах
        
        :param _error: возвращаемый код ошибки выполнения скрипта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapFindPathExePython_t (_pathexe.buffer(), _size, _error)

    mapActiveServerCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapActiveServerCount')
    def mapActiveServerCount() -> int:
        """
        Запросить число подключений к ГИС Серверам
        
        :returns: При отсутствии подключений возвращает ноль
        :rtype: int
        """
        return mapActiveServerCount_t ()

    mapBuildAliasNameEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBuildAliasNameEx', ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def mapBuildAliasNameEx(_number: int, _alias: mapsyst.WTEXT, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Сформировать алиас данных на Сервере
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _alias: имя ресурса (условное имя карты)
        
        :param _name: имя строки для размещения результата
        
        :param _size: размер строки в байтах Алиас создается в формате ``"HOST#ХОСТ#ПОРТ#ALIAS#условное_имя_карты"``
        
        :returns: При ошибке в параметрах возвращает ноль
        :rtype: int
        """
        return mapBuildAliasNameEx_t (_number, _alias.buffer(), _name.buffer(), _size)

    mapIsAliasNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsAliasNameUn', maptype.PWCHAR)
    def mapIsAliasNameUn(_name: mapsyst.WTEXT) -> int:
        """
        Запросить является ли имя идентификатором данных на Сервере
        
        :param _name: строка с именем файла
        
        :returns: Если да, то возвращает ненулевое значение (``1`` - устаревший формат без имени сервера, ``2`` - содержит имя сервера) Если имя не указывает на данные с сервера, то возвращает ноль
        :rtype: int
        """
        return mapIsAliasNameUn_t (_name.buffer())

    mapGetDataNameFromAliasUn_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapGetDataNameFromAliasUn', maptype.PWCHAR)
    def mapGetDataNameFromAliasUn(_name: mapsyst.WTEXT) -> ctypes.POINTER(maptype.WCHAR):
        """
        Запросить имя алиаса данных из полной строки имени, включающей имя хоста
        
        :param _name: строка с именем файла на ГИС Сервере
        
        :returns: Возвращает указатель на имя алиаса (первый символ после ALIAS#) или 0
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapGetDataNameFromAliasUn_t (_name.buffer())

    mapIsServerActiveEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsServerActiveEx', ctypes.c_long)
    def mapIsServerActiveEx(_number: int) -> int:
        """
        Запросить состояние подключения к серверу
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount() При потоковом открытии\\добавлении данных с ГИС Сервера рекомендуется после первой ошибки открытия данных проверить состояние подключения и при ошибке прервать потоковую обработку
        
        :returns: Если подключение к серверу установлено - возвращает ненулевое значение
        :rtype: int
        
        .. note::

           Если после ошибки открытия данных с именем ``"HOST#..."`` или ``"ALIAS#..."``
           подключение не установлено, то нужно убедится, что Сервер запущен и
           введены правильные параметры соединения
        """
        return mapIsServerActiveEx_t (_number)

    mapIsServerMonitoringEnable_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsServerMonitoringEnable', ctypes.c_long)
    def mapIsServerMonitoringEnable(_number: int) -> int:
        """
        Запросить доступ к средствам мониторинга состояния сервера
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :returns: Если мониторинг запрещен - возвращает нулевое значение
        :rtype: int
        """
        return mapIsServerMonitoringEnable_t (_number)

    mapIsServerAdministrationEnable_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsServerAdministrationEnable', ctypes.c_long)
    def mapIsServerAdministrationEnable(_number: int) -> int:
        """
        Запросить доступ к средствам администрирования состояния сервера
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :returns: Если администрирование запрещено - возвращает нулевое значение
        :rtype: int
        """
        return mapIsServerAdministrationEnable_t (_number)

    mapGetServerVersion_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetServerVersion', ctypes.c_long)
    def mapGetServerVersion(_number: int) -> int:
        """
        Запросить версию ГИС Сервера по номеру подключения
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :returns: Возвращает шестнадцатеричный номер версии ГИС Сервер, например: ``0x00040503`` соответствует версии 4.5.3 При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetServerVersion_t (_number)

    mapGetServerState_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.GSMONITOR),'mapGetServerState', ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapGetServerState(_number: int, _version: mapsyst.WTEXT, _size: int, _state: int) -> ctypes.POINTER(maptype.GSMONITOR):
        """
        Считать информацию о состоянии открытых подключений (мониторинг)
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount() versin - буфер для размещения строки с именем и версией ГИС Сервера
        
        :param _size: размер буфера (не менее ``80`` байт)
        
        :param _state: состояние ГИС Сервера, полученное в предыдущем запросе,
        
        :returns: если состояние не изменилось, то возвращается сокращенный отчет После завершения обработки данных необходимо освободить ресурсы путем вызова mapFreeServerState с указателем, полученным в mapGetServerState При ошибке возвращает ноль
        :rtype: ctypes.POINTER(maptype.GSMONITOR)
        """
        return mapGetServerState_t (_number, _version.buffer(), _size, _state)

    mapFreeServerState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeServerState', ctypes.POINTER(maptype.GSMONITOR))
    def mapFreeServerState(_buffer: ctypes.POINTER(maptype.GSMONITOR)) -> ctypes.c_void_p:
        """
        Освободить ресурсы после обработки данных мониторинга состояния сервера
        
        :param _buffer: информация о состоянии, полученная в функции mapGetServerState
        """
        return mapFreeServerState_t (_buffer)

    mapReadLogOnServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_char_p,'mapReadLogOnServer', ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapReadLogOnServer(_number: int, _size: ctypes.POINTER(ctypes.c_long), _error: ctypes.POINTER(ctypes.c_long)) -> ctypes.c_char_p:
        """
        Прочитать журнал на сервере (если есть права администратора)
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _size: поле для записи размера считанного журнала
        
        :param _error: поле для записи кода ощибки, если функция вернет ноль Содержимое журнала не должно сохраняться на диск в целях безопасности
        
        :returns: Возвращает указатель на буфер с журналом в кодировке UTF-8 Если размер журнала больше 2 Мб, то считывает последние 2 Мб После чтения записи необходимо освободить память функцией mapFreeServerLog При ошибке возвращает ноль
        :rtype: ctypes.c_char_p
        """
        return mapReadLogOnServer_t (_number, _size, _error)

    mapFreeServerLog_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeServerLog', ctypes.c_char_p)
    def mapFreeServerLog(_buffer: ctypes.c_char_p) -> ctypes.c_void_p:
        """
        Освободить ресурсы после обработки данных журнала
        
        :param _buffer: адрес записи журнала в памяти, созданный функцией mapReadLogOnServer
        """
        return mapFreeServerLog_t (_buffer)

    mapCheckConnectForAliasUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckConnectForAliasUn', maptype.PWCHAR)
    def mapCheckConnectForAliasUn(_name: mapsyst.WTEXT) -> int:
        """
        Запросить, выполнено ли подключение и регистрация пользователя для алиаса
        
        :param _name: алиас в формате ``"HOST#ХОСТ:ПОРТ#ALIAS#условное_имя_карты"``, или ``"HOST#ХОСТ"`` или ``"HOST#ХОСТ:ПОРТ"``
        
        :returns: При успешной проверке возвращает номер подключения При ошибке возвращает ноль
        :rtype: int
        """
        return mapCheckConnectForAliasUn_t (_name.buffer())

    mapCheckConnectForAliasEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckConnectForAliasEx', ctypes.c_char_p, ctypes.c_long)
    def mapCheckConnectForAliasEx(_name: ctypes.c_char_p, _port: int) -> int:
        """
        Запросить, выполнено ли подключение и регистрация пользователя для алиаса и порта
        
        :param _name: алиас в формате ``"HOST#ХОСТ:ПОРТ#ALIAS#условное_имя_карты"``, или ``"HOST#ХОСТ"`` или ``"HOST#ХОСТ:ПОРТ"``
        
        :param _port: номер порта для проверки или ``0`` (любой) На одном сервере могут быть несколько экземпляров ГИС Сервера с разными портами
        
        :returns: При успешной проверке возвращает номер подключения При ошибке возвращает ноль
        :rtype: int
        """
        return mapCheckConnectForAliasEx_t (_name, _port)

    mapOpenConnectUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapOpenConnectUn', maptype.PWCHAR, ctypes.c_long)
    def mapOpenConnectUn(_name: mapsyst.WTEXT, _port: int) -> int:
        """
        Открыть новое подключение к ГИС-серверу
        
        :param _name: имя хоста (до ``256`` символов) или адрес ``"XXX.XXX.XXX.XXX"``
        
        :param _port: номер порта от ``1024`` до ``65536``, по умолчанию - ``2047`` (если port ``= 0``)
        
        :returns: В случае удачно выполненного подключения возвращает его порядковый номер При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если параметр равен нулю - сервер ищется на локальном хосте ``"localhost"``
        """
        return mapOpenConnectUn_t (_name.buffer(), _port)

    mapOpenConnectExUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapOpenConnectExUn', maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapOpenConnectExUn(_name: mapsyst.WTEXT, _port: int, _cansleep: int) -> int:
        """
        Открыть новое подключение к ГИС-серверу
        
        :param _name: имя хоста (до ``256`` символов) или адрес ``"XXX.XXX.XXX.XXX"``
        
        :param _port: номер порта от ``1024`` до ``65536``, по умолчанию - ``2047`` (если port ``= 0``)
        
        :param _cansleep: разрешение на открытие виртуального (спящего) соединения, при отсутствии физического доступа к серверу Данные будут открываться из кэш, если он есть При появлении физического соединения оно автоматически (по мере вызова mapAdjustData) будет восстановлено вместо вирутального (кэш обновится по данным с сервера)
        
        :returns: В случае удачно выполненного подключения возвращает его порядковый номер При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если параметр равен нулю - сервер ищется на локальном хосте ``"localhost"``.
        """
        return mapOpenConnectExUn_t (_name.buffer(), _port, _cansleep)

    mapCanCloseConnect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCanCloseConnect', ctypes.c_long)
    def mapCanCloseConnect(_number: int) -> int:
        """
        Запросить, можно ли закрыть подключение
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :returns: При ошибке (подключение не найдено) возвращает ноль При занятости подключения возвращает ``"-1"`` Если соединение может быть закрыто, то возвращает положительное значение
        :rtype: int
        """
        return mapCanCloseConnect_t (_number)

    mapCloseConnect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCloseConnect', ctypes.c_long)
    def mapCloseConnect(_number: int) -> int:
        """
        Закрыть подключение к ГИС-серверу
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :returns: При ошибке (подключение не найдено) возвращает ноль При занятости подключения возвращает ``"-1"`` При успешном выполнении возвращает положительное значение Если счетчик ссылок на соединения равен 0 и все соединения закрыты возвращает 2
        :rtype: int
        """
        return mapCloseConnect_t (_number)

    mapSetConnectParametersExUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetConnectParametersExUn', ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapSetConnectParametersExUn(_number: int, _name: mapsyst.WTEXT, _port: int) -> int:
        """
        Изменить параметры подключения с ГИС-сервером
        
        Вызывается до открытия карт на сервере
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _name: имя хоста (до ``256`` символов) или адрес ``"XXX.XXX.XXX.XXX"``
        
        :param _port: номер порта от ``1024`` до ``65536``, по умолчанию - ``2047`` (если port ``= 0``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если параметр равен нулю - сервер ищется на локальном хосте ``"localhost"``.
        """
        return mapSetConnectParametersExUn_t (_number, _name.buffer(), _port)

    mapGetConnectPortEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetConnectPortEx', ctypes.c_long)
    def mapGetConnectPortEx(_number: int) -> int:
        """
        Запросить номер порта для связи с ГИС-сервером
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount() Номер порта от ``1024`` до ``65536``, по умолчанию - ``2047``
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        """
        return mapGetConnectPortEx_t (_number)

    mapGetConnectHostExUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetConnectHostExUn', ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetConnectHostExUn(_number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить имя или адрес хоста
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _name: адрес строки для размещения результата
        
        :param _size: размер строки (для имени хоста не менее ``256``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если было установлен адрес хоста - возвращаемое значение 1,
           если имя хоста - возвращаемое значение 2
        """
        return mapGetConnectHostExUn_t (_number, _name.buffer(), _size)

    mapRegisterUserUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRegisterUserUn', ctypes.c_long, ctypes.POINTER(maptype.TMCUSERPARMUN))
    def mapRegisterUserUn(_number: int, _parm: ctypes.POINTER(maptype.TMCUSERPARMUN)) -> int:
        """
        Зарегистрировать пользователя
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _parm: логин и пароль для подключения
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если соединение с сервером не было установлено -
           пытается соединиться с установленными ранее параметрами
           Пароль должен передаваться в зашифрованном виде по алгоритму MD5 (в виде хэша)
           Для получения хэша пароля следует использовать функцию mapStringToMd5Hash
           или svStringToHash (описана в gisdlgs.h)
           выделив выходной буфер для размещения не менее 33 символов (32 символа и замыкающий ноль)
        """
        return mapRegisterUserUn_t (_number, _parm)

    mapRegisterSystemUserEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRegisterSystemUserEx', ctypes.c_long)
    def mapRegisterSystemUserEx(_number: int) -> int:
        """
        Зарегистрировать текущего пользователя ОС как пользователя ГИС Сервера в домене
        
        :param _number: номер активного подключения (соединения) к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если соединение с сервером не было установлено -
           пытается соединиться с установленными ранее параметрами
        """
        return mapRegisterSystemUserEx_t (_number)

    mapUnRegisterUserEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapUnRegisterUserEx', ctypes.c_long)
    def mapUnRegisterUserEx(_number: int) -> ctypes.c_void_p:
        """
        Удалить в памяти параметры регистрации пользователя
        
        :param _number: номер активного подключения (соединения) к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        .. note::

           После закрытия последнего документа на Сервере соединение
           разрывается и для последующего открытия карты нужно повторно
           выполнить mapRegisterUser()
        """
        return mapUnRegisterUserEx_t (_number)

    mapGetRegisterUserType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRegisterUserType', ctypes.c_long)
    def mapGetRegisterUserType(_number: int) -> int:
        """
        Запросить тип регистрации пользователя
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :returns: то возвращается положительное значение
        :rtype: int
        
        .. note::

           Если регистрация пользователя выполнялась через функцию mapRegisterSystemUserEx,
        """
        return mapGetRegisterUserType_t (_number)

    mapGetMapListforUserUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMapListforUserUn', ctypes.c_long, ctypes.POINTER(maptype.TMCDATALIST), ctypes.c_int)
    def mapGetMapListforUserUn(_number: int, _buffer: ctypes.POINTER(maptype.TMCDATALIST), _buffersize: int) -> int:
        """
        Запросить список доступных пользователю карт на ГИС-сервере
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _buffer: адрес памяти для размещения списка карт, структура ``TMCMAPLIST`` описана в maptype.h
        
        :param _buffersize: длина выделенной области памяти
        
        :returns: Возвращает общий размер считанной записи (значение поля TMCDATALIST::Length) или 0 Если общий размер считанной записи больше чем значение buffersize, то необходимо увеличить размер буфера и повторить запрос
        :rtype: int
        """
        return mapGetMapListforUserUn_t (_number, _buffer, _buffersize)

    mapGetAlsListforUserUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetAlsListforUserUn', ctypes.c_long, ctypes.POINTER(maptype.TMCDATALIST), ctypes.c_int)
    def mapGetAlsListforUserUn(_number: int, _buffer: ctypes.POINTER(maptype.TMCDATALIST), _buffersize: int) -> int:
        """
        Запросить список доступных пользователю атласов на ГИС-сервере
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _buffer: адрес памяти для размещения списка атласов, структура ``TMCMAPLIST`` описана в maptype.h
        
        :param _buffersize: длина выделенной области памяти
        
        :returns: Возвращает общий размер считанной записи (значение поля TMCDATALIST::Length) или 0 Если общий размер считанной записи больше чем значение buffersize, то необходимо увеличить размер буфера и повторить запрос
        :rtype: int
        """
        return mapGetAlsListforUserUn_t (_number, _buffer, _buffersize)

    mapGetMtwListforUserUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMtwListforUserUn', ctypes.c_long, ctypes.POINTER(maptype.TMCDATALIST), ctypes.c_int)
    def mapGetMtwListforUserUn(_number: int, _buffer: ctypes.POINTER(maptype.TMCDATALIST), _buffersize: int) -> int:
        """
        Запросить список доступных пользователю матриц на ГИС-сервере
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _buffer: адрес памяти для размещения списка матриц, структура ``TMCMAPLIST`` описана в maptype.h
        
        :param _buffersize: длина выделенной области памяти
        
        :returns: Возвращает общий размер считанной записи (значение поля TMCDATALIST::Length) или 0 Если общий размер считанной записи больше чем значение buffersize, то необходимо увеличить размер буфера и повторить запрос
        :rtype: int
        """
        return mapGetMtwListforUserUn_t (_number, _buffer, _buffersize)

    mapGetRswListforUserUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRswListforUserUn', ctypes.c_long, ctypes.POINTER(maptype.TMCDATALIST), ctypes.c_int)
    def mapGetRswListforUserUn(_number: int, _buffer: ctypes.POINTER(maptype.TMCDATALIST), _buffersize: int) -> int:
        """
        Запросить список доступных пользователю растров на ГИС-сервере
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _buffer: адрес памяти для размещения списка растров, структура ``TMCMAPLIST`` описана в maptype.h
        
        :param _buffersize: длина выделенной области памяти
        
        :returns: Возвращает общий размер считанной записи (значение поля TMCDATALIST::Length) или 0 Если общий размер считанной записи больше чем значение buffersize, то необходимо увеличить размер буфера и повторить запрос
        :rtype: int
        """
        return mapGetRswListforUserUn_t (_number, _buffer, _buffersize)

    mapGetCurrentUserNameUn_t = mapsyst.GetProcAddress(acceslib,maptype.PWCHAR,'mapGetCurrentUserNameUn', ctypes.c_long)
    def mapGetCurrentUserNameUn(_number: int) -> mapsyst.WTEXT:
        """
        Запросить имя пользователя, подключившегося к ГИС-серверу
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :returns: При ошибке возвращает пустую строку
        :rtype: mapsyst.WTEXT
        """
        return mapGetCurrentUserNameUn_t (_number)

    mapGetCachePathUn_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapGetCachePathUn')
    def mapGetCachePathUn() -> ctypes.POINTER(maptype.WCHAR):
        """
        Запросить путь к папке для хранения кэшируемых данных с ГИС Сервера
        """
        return mapGetCachePathUn_t ()

    mapSetCachePathUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetCachePathUn', maptype.PWCHAR)
    def mapSetCachePathUn(_path: mapsyst.WTEXT) -> int:
        """
        Установить путь к папке для хранения кэшируемых данных с ГИС Сервера
        
        :param _path: путь к папке для хранения кэшируемых данных с ГИС Сервера
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если приложение не установило путь к папке для кэширования данных,
           то она автоматически будет размещена внутри системной папки Temp
           в папке Panorama.Cache
        """
        return mapSetCachePathUn_t (_path.buffer())

    mapSetMapCacheSubfolder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMapCacheSubfolder', maptype.PWCHAR)
    def mapSetMapCacheSubfolder(_subfolder: mapsyst.WTEXT) -> int:
        """
        Установить имя папки для хранения кэша векторных карт с ГИС Сервера
        
        :param _subfolder: имя папки для хранения кэша векторных карт с ГИС Сервера Необходимо для организации устойчивой параллельной работы нескольких приложений на одном компьюере с картами на ГИС Сервере при редактировании карт Имя папки задается без косых и специальных символов, недопустимых в файловой системе
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetMapCacheSubfolder_t (_subfolder.buffer())

    mapClearDataCache_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapClearDataCache')
    def mapClearDataCache() -> ctypes.c_void_p:
        """
        Очистить папку с кэшем данных, открытых с ГИС Сервера или с геопорталов
        
        Имя папки определяется функцией mapGetCachePathUn
        Данные, открытые в момент вызова функции, могут не удалиться
        """
        return mapClearDataCache_t ()

    mapClearDocCache_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapClearDocCache', maptype.HMAP)
    def mapClearDocCache(_hmap: maptype.HMAP) -> ctypes.c_void_p:
        """
        Очистить кэш данных для всех карт текущего документа, открытых с ГИС Сервера
        
        :param _hmap: идентификатор открытых данных Кэш автоматически очищается при сортировке карты на ГИС Сервере или обнаружении большого числа выполненных транзакций, с момента предыдущего обращения к данным Иначе кэш обновляется (реплицируется) в соответствии с журналом транзакций на ГИС Сервере
        """
        return mapClearDocCache_t (_hmap)

    mapClearSiteCache_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapClearSiteCache', maptype.HMAP, maptype.HSITE)
    def mapClearSiteCache(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> ctypes.c_void_p:
        """
        Очистить кэш данных для векторной карты, открытой с ГИС Сервера
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных Кэш автоматически очищается при сортировке карты на ГИС Сервере или обнаружении большого числа выполненных транзакций, с момента предыдущего обращения к данным Иначе кэш обновляется (реплицируется) в соответствии с журналом транзакций на ГИС Сервере
        """
        return mapClearSiteCache_t (_hmap, _hsite)

    mapClearLocalDbmCache_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapClearLocalDbmCache', maptype.HMAP, maptype.HSITE)
    def mapClearLocalDbmCache(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> ctypes.c_void_p:
        """
        Очистить кэш карты из пространственной базы открытой без ГИС Сервера
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных Запускает процесс полного переформирования картографического представления на основе данных из пространственной базы данных
        """
        return mapClearLocalDbmCache_t (_hmap, _hsite)

    mapClearServerCache_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapClearServerCache', maptype.HMAP)
    def mapClearServerCache(_hmap: maptype.HMAP) -> ctypes.c_void_p:
        """
        Очистить кэш данных для всех карт текущего документа с ГИС Сервера
        
        :param _hmap: идентификатор открытых данных Кэш автоматически очищается при сортировке карты на ГИС Сервере или обнаружении большого числа выполненных транзакций, с момента предыдущего обращения к данным Иначе кэш обновляется (реплицируется) в соответствии с журналом транзакций на ГИС Сервере
        """
        return mapClearServerCache_t (_hmap)

    mapIsMapFromServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsMapFromServer', maptype.HMAP, maptype.HSITE)
    def mapIsMapFromServer(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить открыта ли карта на сервере или локально
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Если карта открыта на сервере возвращает ненулевое значение
        :rtype: int
        """
        return mapIsMapFromServer_t (_hmap, _hsite)

    mapGetFolderList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetFolderList', ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.TMCDATALIST), ctypes.c_long)
    def mapGetFolderList(_number: int, _folder: mapsyst.WTEXT, _allfiles: int, _parm: ctypes.POINTER(maptype.TMCDATALIST), _size: int) -> int:
        """
        Запросить список папок на сервере, доступных для записи файлов
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _folder: путь к виртуальной папке, в которой запрашивается список файлов и папок или ``0``
        
        :param _allfiles: признак запроса всех файлов в папке folder, если не установлен,
        
        :param _parm: адрес буфера для размещения списка запрошенных данных или ``0``
        
        :param _size: размер буфера для размещения списка Список данных заполняется только для файлов и папок, непосредственно расположенных в заданной папке без вложений
        
        :returns: При успешном выполнении возвращает размер сформированного списка Если размер списка превышает размер буфера, то данные считаны не полностью Тогда нужно выделить больший буфер и запросить данные повторно При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Например, ``"Data\\\\Maps"``
           Если folder равно 0, то запрашивается список алиасов всех доступных папок
           то буден выдан список внутренних папок и файлов MAP,SIT,SITX,RSC,MTW,MTQ,RSW
           Если parm равно 0, то запрашивается размер буфера, требуемый для размещения списка
        """
        return mapGetFolderList_t (_number, _folder.buffer(), _allfiles, _parm, _size)

    mapGetMapFolderOnServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMapFolderOnServer', ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def mapGetMapFolderOnServer(_number: int, _alias: mapsyst.WTEXT, _folder: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить виртуальную папку по алиасу карты
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _alias: алиас карты
        
        :param _folder: адрес строки для записи алиаса виртуальной папки
        
        :param _size: длина строки в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMapFolderOnServer_t (_number, _alias.buffer(), _folder.buffer(), _size)

    mapCreateFolderOnServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateFolderOnServer', ctypes.c_long, maptype.PWCHAR)
    def mapCreateFolderOnServer(_number: int, _folder: mapsyst.WTEXT) -> int:
        """
        Создать папку на сервере относительно алиаса доступной папки
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _folder: путь к создаваемой папке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Например, ``"Data\\\\Maps"`` или ``"Data/Maps"``,
           где ``"Data"`` - виртуальная папка в настройках ГИС Сервера, ``"Maps"`` - создаваемая папка
        """
        return mapCreateFolderOnServer_t (_number, _folder.buffer())

    mapDeleteFolderOnServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteFolderOnServer', ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapDeleteFolderOnServer(_number: int, _folder: mapsyst.WTEXT, _deletefiles: int, _deletefolders: int) -> int:
        """
        Удалить папку на сервере относительно алиаса доступной папки
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _folder: путь к удаляемой папке
        
        :param _deletefiles: удалить все файлы в папке (если задано ненулевое значение)
        
        :param _deletefolders: удалить все подпапки с файлами в них (если задано ненулевое значение)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Например, для удаления папки ``"Maps"``: ``"Data\\\\Maps"`` или ``"Data/Maps"``,
           где ``"Data"`` - виртуальная папка в настройках ГИС Сервера, ``"Maps"`` - удаляемая папка
        """
        return mapDeleteFolderOnServer_t (_number, _folder.buffer(), _deletefiles, _deletefolders)

    mapDeleteFileOnServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteFileOnServer', ctypes.c_long, maptype.PWCHAR)
    def mapDeleteFileOnServer(_number: int, _file: mapsyst.WTEXT) -> int:
        """
        Удалить файл на сервере
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _file: путь к удаляемому файлу
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Например, ``"Data\\\\Maps\\\\image.rsw"``,
           где ``"Data"`` - виртуальная папка в настройках ГИС Сервера, ``"image.rsw"`` - удаляемый файл
        """
        return mapDeleteFileOnServer_t (_number, _file.buffer())

    mapCopyFileOnServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCopyFileOnServer', ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR)
    def mapCopyFileOnServer(_number: int, _source: mapsyst.WTEXT, _target: mapsyst.WTEXT) -> int:
        """
        Скопировать файл на сервере
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _source: путь к изменяемому файлу
        
        :param _target: новый путь к файлу
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Например, ``"Data\\\\Maps\\\\image.sitx"``,
           где ``"Data"`` - виртуальная папка на ГИС Сервере, ``"image.sitx"`` - перемещаемый файл
           Например, ``"Storage\\\\Roads\\\\road_M4.sitx"``,
        """
        return mapCopyFileOnServer_t (_number, _source.buffer(), _target.buffer())

    mapRenameFileOnServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRenameFileOnServer', ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR)
    def mapRenameFileOnServer(_number: int, _source: mapsyst.WTEXT, _target: mapsyst.WTEXT) -> int:
        """
        Переименовать (переместить) файл или папку на сервере
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _source: путь к изменяемому файлу или папке
        
        :param _target: новый путь к файлу или папке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Например, ``"Data\\\\Maps\\\\image.sitx"``,
           где ``"Data"`` - виртуальная папка на ГИС Сервере, ``"image.sitx"`` - перемещаемый файл
           Например, ``"Storage\\\\Roads\\\\road_M4.sitx"``,
        """
        return mapRenameFileOnServer_t (_number, _source.buffer(), _target.buffer())

    mapSaveFileOnServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSaveFileOnServer', ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR)
    def mapSaveFileOnServer(_number: int, _folder: mapsyst.WTEXT, _file: mapsyst.WTEXT) -> int:
        """
        Сохранить файл на сервере
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _folder: путь для сохранения файла, путь может начинаться с имени алиаса папки, доступной для записи данных Например: ``"Data\\\\Maps"`` или ``"Data/Maps/Images"``, где ``"Data"`` - виртуальная папка на ГИС Сервере, /Maps/Images - поддиректории или содержать полный алиас виртуальной папки на сервере с поддиректориями Например: ``"HOST#123.345.0.12#ALIAS#Data/Maps/Images"`` или содержать полный алиас карты, записанной в виртуальной папке на сервере, с поддиректориями относительно карты Например: ``"HOST#123.345.0.12#ALIAS#Mymap/Images"``
        
        :param _file: путь к файлу, который будет записан в папку на сервере (файл должен содержать данные, а не выполняемый код). Имя файла, расширение и атрибуты чтения/записи сохраняются Отсутствующие директории создаются автоматически Символ косой может быть любого вида - ``"/"`` или ``"\\\\"`` Для доступа к файлу в дальнейшем нужно объединить путь к папке и имя файла, например: ``"HOST#123.345.0.12#ALIAS#Data/Maps/example.sitx"``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSaveFileOnServer_t (_number, _folder.buffer(), _file.buffer())

    mapSaveMapOnServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSaveMapOnServer', ctypes.c_long, maptype.PWCHAR, maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSaveMapOnServer(_number: int, _folder: mapsyst.WTEXT, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _rscsave: int) -> int:
        """
        Сохранить карту на сервере
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _folder: путь для сохранения файла, путь должен начинаться с алиаса папки, доступной для записи данных
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _rscsave: признак необходимости сохранения файла ``RSC`` на сервер
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Например, ``"Data\\\\Maps"`` или ``"Data/Maps"``,
           где ``"Data"`` - виртуальная папка на ГИС Сервере
        """
        return mapSaveMapOnServer_t (_number, _folder.buffer(), _hmap, _hsite, _rscsave)

    mapReadFileOnServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapReadFileOnServer', ctypes.c_long, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapReadFileOnServer(_number: int, _alias: mapsyst.WTEXT, _path: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Прочитать файл на сервере (если есть доступ к виртуальной папке)
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _alias: алиас файла на сервере, начиная с имени виртуальной папки (кроме выполняемых файлов, файлов карт, матриц и растров)
        
        :param _path: путь, по которому будет сохранен файл (после записи путь дополняется именем файла)
        
        :param _size: размер поля, содержащего путь
        
        :param _error: поле для записи кода ощибки, если функция вернет ноль
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapReadFileOnServer_t (_number, _alias.buffer(), _path.buffer(), _size, _error)

    mapGetServerUsersListInXml_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetServerUsersListInXml', ctypes.c_long, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long))
    def mapGetServerUsersListInXml(_number: int, _xmlname: mapsyst.WTEXT, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить список пользователей, ролей и данных, размещенных на ГИС Сервере в виде xml
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount() path    - путь, по которому будет сохранен файл
        
        :param _error: поле для записи кода ощибки, если функция вернет ноль
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetServerUsersListInXml_t (_number, _xmlname.buffer(), _error)

    mapSaveToGeoDB_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSaveToGeoDB', ctypes.c_long, maptype.HMESSAGE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def mapSaveToGeoDB(_number: int, _handle: maptype.HMESSAGE, _dslist: mapsyst.WTEXT, _logname: mapsyst.WTEXT, _size: int) -> int:
        """
        Сохранить данные в Банк данных ЦК и ДЗЗ
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _handle: иденетификатор окна, которому посылаются сообщения о ходе загрузки данных в Банк данных (``WM_PROGRESSBAR``, ``WPARAM`` ``= -1`` - старт, ``LPARAM`` - текст сообщения в кодировке приложения, ``0````-100`` - ``%`` выполнения, -``2`` - завершение процесса) цикл сообщений посылается при передаче каждого набора данных (файла) на сервер и при загрузке наборов в Банк данных на сервере
        
        :param _dslist: путь к файлу - списку загружаемых наборов данных (``111``, ``222``, ``333`` - имена файлов)

        Пример XML::

            <?xml version="1.0" encoding="UTF-8"?> <dsl> 111, 222, 333 </dsl>
        
        :param _logname: буфер строки для получения имени файла с протоколом загрузки наборов в Банк данных
        
        :param _size: размера буфера для записи имени файла протокола
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSaveToGeoDB_t (_number, _handle, _dslist.buffer(), _logname.buffer(), _size)

    mapCallGeoDBLoaderPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCallGeoDBLoaderPro', ctypes.c_long, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapCallGeoDBLoaderPro(_number: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _dslist: mapsyst.WTEXT, _logname: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Отправить команду на загрузку наборов данных c ГИС Сервера в Банк данных
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount() handle  - идентификатор окна, которому посылаются сообщения о ходе загрузки данных в Банк данных
        
        :param _dslist: имя файла - списка загружаемых наборов данных
        
        :param _callevent: адрес функции оборатного вызова для уведомления о проценте обработанных наборов данных (см. maptype.h)
        
        :param _parm: адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы), вторым параметром в вызываемой функции передается процент от ``0`` до ``100``
        
        :param _logname: буфер строки для получения имени файла с протоколом загрузки наборов в Банк данных
        
        :param _size: размера буфера для записи имени файла протокола
        
        :param _error: код ошибки выполнения запроса Наборы данных могут быть загружены удаленно другим приложением на ГИС Сервер в специальную папку для Банка Данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCallGeoDBLoaderPro_t (_number, _callevent, _parm, _dslist.buffer(), _logname.buffer(), _size, _error)

    mapCallDbCommand_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCallDbCommand', ctypes.c_long, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_long), maptype.PWCHAR)
    def mapCallDbCommand(_number: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _dslist: mapsyst.WTEXT, _logname: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_long), _command: mapsyst.WTEXT) -> int:
        """
        Отправить команду к Банку данных ЦК и ДЗЗ
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _callevent: адрес функции оборатного вызова для уведомления о проценте обработанных наборов данных (см. maptype.h)
        
        :param _parm: адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы), вторым параметром в вызываемой функции передается процент от ``0`` до ``100``
        
        :param _dslist: имя файла xml - списка обрабатываемых наборов данных (пути, идентификаторы записей базы и т.д.)
        
        :param _logname: буфер строки для получения имени файла с протоколом загрузки наборов в Банк данных
        
        :param _size: размера буфера для записи имени файла протокола
        
        :param _error: поле для записи кода ощибки, если функция вернет ноль
        
        :param _command: имя команды: ``"adjust"`` - выполнить сводку наборов данных, ``"control"`` - выполнить контроль качества векторных наборов данных, ``"opencontrol"`` - выполнить контроль отсутствия закрытых сведений на карте, ``"export"`` - выполнить экспорт геопокрытий, ``"expertise"`` - выполнить входной контроль наборов данных по шаблону требований, ``"upscheme"`` - обновить схему наличия наборов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCallDbCommand_t (_number, _callevent, _parm, _dslist.buffer(), _logname.buffer(), _size, _error, _command.buffer())

    mapCallGeoLevelEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCallGeoLevelEx', ctypes.c_long, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapCallGeoLevelEx(_number: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _geolist: mapsyst.WTEXT, _logname: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Отправить команду на формирование геопокрытия из наборов данных Банка данных ЦК и ДЗЗ
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _callevent: адрес функции оборатного вызова для уведомления о проценте обработанных наборов данных (см. maptype.h)
        
        :param _parm: адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы), вторым параметром в вызываемой функции передается процент от ``0`` до ``100``
        
        :param _geolist: имя файла - списка наборов данных для формирования геопокрытий
        
        :param _logname: буфер строки для получения имени файла с протоколом загрузки наборов в Банк данных
        
        :param _size: размера буфера для записи имени файла протокола
        
        :param _error: поле для записи кода ошибки (maperr.rh)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCallGeoLevelEx_t (_number, _callevent, _parm, _geolist.buffer(), _logname.buffer(), _size, _error)

    mapCallExport_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCallExport', ctypes.c_long, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int, ctypes.POINTER(ctypes.c_long))
    def mapCallExport(_number: int, _callevent: maptype.EVENTSTATE, _parm: ctypes.POINTER(ctypes.c_void_p), _exportlist: mapsyst.WTEXT, _logname: mapsyst.WTEXT, _size: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Отправить команду на экспорт геопокрытия в Банке данных ЦК и ДЗЗ
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _exportlist: имя файла - списка экспортируемых геопокрытий (формат для экспорта задается в списке)
        
        :param _callevent: адрес функции оборатного вызова для уведомления о проценте обработанных наборов данных (см. maptype.h)
        
        :param _parm: адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы), вторым параметром в вызываемой функции передается процент от ``0`` до ``100``
        
        :param _logname: буфер строки для получения имени файла с протоколом загрузки наборов в Банк данных
        
        :param _size: размера буфера для записи имени файла протокола
        
        :param _error: поле для записи кода ошибки (maperr.rh)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCallExport_t (_number, _callevent, _parm, _exportlist.buffer(), _logname.buffer(), _size, _error)

    mapIsCopyDataEnabled_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsCopyDataEnabled', ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapIsCopyDataEnabled(_number: int, _alias: mapsyst.WTEXT, _type: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить разрешение на копирование файлов карты на клиент
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _alias: алиас данных на сервере
        
        :param _error: код ошибки доступа (см. maperr.rh)
        
        :returns: При ошибке возвращает ноль, иначе - тип данных (``1`` - карта, ``2`` - растр, ``3`` - матрица)
        :rtype: int
        """
        return mapIsCopyDataEnabled_t (_number, _alias.buffer(), _type, _error)

    mapCopyDataFromServerEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCopyDataFromServerEx', ctypes.c_long, maptype.PWCHAR, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapCopyDataFromServerEx(_number: int, _alias: mapsyst.WTEXT, _type: int, _target: mapsyst.WTEXT, _targetsize: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Скопировать набор данных с ГИС Сервера на клиент
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _alias: алиас данных на сервере
        
        :param _type: тип данных (``1`` - карта, ``2`` - растр, ``3`` - матрица или ``0`` - требуется определить)
        
        :param _target: имя файла выходного набора данных (если задана только папка, то имя формируется с учетом алиаса и типа данных
        
        :param _targetsize: длина буфера target в байтах (для обновления выходного имени)
        
        :param _error: код ошибки доступа (см. maperr.rh)
        
        :returns: При ошибке возвращает ноль, иначе - тип данных (``1`` - карта, ``2`` - растр, ``3`` - матрица)
        :rtype: int
        """
        return mapCopyDataFromServerEx_t (_number, _alias.buffer(), _type, _target.buffer(), _targetsize, _error)

    mapGetRscListOnServer_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetRscListOnServer', ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapGetRscListOnServer(_number: int, _size: ctypes.POINTER(ctypes.c_long)) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить список классификаторов, доступных для операций импорта данных
        
        После завершения обработки ответа необходимо освободить память - mapFreeRscList

        Пример XML::

            <?xml version="1.0" encoding="UTF-8"?>
            <rsclist><rsc name="Топокарты масштаба 1:25 000" alias="25t17g.rsc"/></rsclist>
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetRscListOnServer_t (_number, _size)

    mapFreeRscList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeRscList', ctypes.c_char_p)
    def mapFreeRscList(_buffer: ctypes.c_char_p) -> ctypes.c_void_p:
        """
        Освободить память, выделенную функцией mapGetRscListOnServer
        
        :param _buffer: адрес памяти, выделенной функцией mapGetRscListOnServer
        """
        return mapFreeRscList_t (_buffer)

    mapReadFileStateOnServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapReadFileStateOnServer', ctypes.c_long, maptype.PWCHAR, ctypes.POINTER(ctypes.c_int64), ctypes.POINTER(maptype.SYSTEMTIME), ctypes.POINTER(ctypes.c_long))
    def mapReadFileStateOnServer(_number: int, _alias: mapsyst.WTEXT, _size: ctypes.POINTER(ctypes.c_int64), _time: ctypes.POINTER(maptype.SYSTEMTIME), _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Прочитать состояние файла (дату и время обновления, размер) на сервере (если есть доступ к виртуальной папке)
        
        :param _number: номер активного подключения к ГИС Серверу от ``1`` до mapActiveServerCount()
        
        :param _alias: алиас файла на сервере, начиная с имени виртуальной папки (кроме выполняемых файлов, файлов карт, матриц и растров)
        
        :param _size: поле для записи размера файла
        
        :param _time: поле для записи даты и времени обновления файла
        
        :param _error: поле для записи кода ощибки, если функция вернет ноль
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapReadFileStateOnServer_t (_number, _alias.buffer(), _size, _time, _error)

    mapStringToMd5Hash_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapStringToMd5Hash', ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
    def mapStringToMd5Hash(_instring: ctypes.c_char_p, _outstring: ctypes.c_char_p, _length: int) -> int:
        """
        Преобразовать входную строку (не более 1024 байта), заканчивающуюся 0, в строку в формате md5
        
        :param _instring: входная строка
        
        :param _outstring: выходная строка в формате md5
        
        :param _length: размер выходной строки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapStringToMd5Hash_t (_instring, _outstring, _length)

    mapOpenDiagnosticsEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapOpenDiagnosticsEx', maptype.PWCHAR, ctypes.c_long)
    def mapOpenDiagnosticsEx(_logname: mapsyst.WTEXT, _hideinfo: int) -> int:
        """
        Открыть запись в диагностический протокол
        
        :param _logname: путь к протоколу диагностической печати, если равен нулю,
        
        :param _hideinfo: признак отключения выдачи информационных сообщений (``MT_INFO``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           то запись идет в \\ProgramData\\mapdiagnostics.log или /var/Panorama/
        """
        return mapOpenDiagnosticsEx_t (_logname.buffer(), _hideinfo)

    mapIsDiagnostics_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsDiagnostics')
    def mapIsDiagnostics() -> int:
        """
        Запросить, открыт ли диагностический протокол
        """
        return mapIsDiagnostics_t ()

    mapCloseDiagnostics_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseDiagnostics')
    def mapCloseDiagnostics() -> ctypes.c_void_p:
        """
        Закрыть запись в диагностический протокол
        """
        return mapCloseDiagnostics_t ()

    mapWriteToDiagnosticsLog_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapWriteToDiagnosticsLog', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def mapWriteToDiagnosticsLog(_message: mapsyst.WTEXT, _messageex: mapsyst.WTEXT, _type: int) -> ctypes.c_void_p:
        """
        Записать сообщение в диагностический протокол
        
        :param _message: первая часть сообщения
        
        :param _messageex: вторая часть сообщения
        
        :param _type: тип сообщения (>>> ``MT_ERROR``, --> ``MT_WARNING``, ``MT_INFO``, ``MT_CONTINUE`` - продолжение) error - код ошибки, запрошенный у системы (если равен ``0``, то будет запрошен при выводе сообщения) value - число, которое будет преобразовано в строку и добавлено к сообщению
        """
        return mapWriteToDiagnosticsLog_t (_message.buffer(), _messageex.buffer(), _type)

    mapWriteToLogLastError_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapWriteToLogLastError', maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapWriteToLogLastError(_message: mapsyst.WTEXT, _messageex: mapsyst.WTEXT, _type: int, _error: int) -> ctypes.c_void_p:
        """
        Записать сообщение в диагностический протокол
        
        :param _message: первая часть сообщения
        
        :param _messageex: вторая часть сообщения
        
        :param _type: тип сообщения (>>> ``MT_ERROR``, --> ``MT_WARNING``, ``MT_INFO``, ``MT_CONTINUE`` - продолжение)
        
        :param _error: код ошибки, запрошенный у системы (если равен ``0``, то будет запрошен при выводе сообщения) value - число, которое будет преобразовано в строку и добавлено к сообщению
        """
        return mapWriteToLogLastError_t (_message.buffer(), _messageex.buffer(), _type, _error)

    mapWriteErrorToDiagnosticsLog_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapWriteErrorToDiagnosticsLog', ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapWriteErrorToDiagnosticsLog(_code: int, _message: mapsyst.WTEXT, _type: int) -> ctypes.c_void_p:
        """
        Записать сообщение по коду ошибки в диагностический протокол
        
        :param _code: код ошибки для формирования сообщения (maperr.rh)
        
        :param _message: сообщение, добавляемое к описанию ошибки
        
        :param _type: тип сообщения (>>> ``MT_ERROR``, --> ``MT_WARNING``, ``MT_INFO``, ``MT_CONTINUE`` - продолжение) error - код ошибки, запрошенный у системы (если равен ``0``, то будет запрошен при выводе сообщения)
        """
        return mapWriteErrorToDiagnosticsLog_t (_code, _message.buffer(), _type)

    mapWriteToLogInt_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapWriteToLogInt', maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapWriteToLogInt(_message: mapsyst.WTEXT, _value: int, _type: int) -> ctypes.c_void_p:
        """
        Записать сообщение с числом в диагностический протокол
        
        :param _message: текст сообщения
        
        :param _value: число, которое будет преобразовано в строку и добавлено к сообщению
        
        :param _type: тип сообщения (>>> ``MT_ERROR``, --> ``MT_WARNING``, ``MT_INFO``, ``MT_CONTINUE`` - продолжение)
        """
        return mapWriteToLogInt_t (_message.buffer(), _value, _type)

    SetConsoleOutput_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'SetConsoleOutput', ctypes.c_long)
    def SetConsoleOutput(_flag: int) -> ctypes.c_void_p:
        """
        Включить или отключить вывод диагностического протокола в консоль
        
        :param _flag: флаг включения вывода на консоль: ``1`` или ``0`` std::cout << ``"Diagnostics"`` << ``": "`` << message << std::endl;
        """
        return SetConsoleOutput_t (_flag)

    mapGetDiagnosticFileName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetDiagnosticFileName', maptype.PWCHAR, ctypes.c_long)
    def mapGetDiagnosticFileName(_mapdiagnostic: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить полный путь к диагностическому протоколу
        
        :param _mapdiagnostic: буфер для записи пути к файлу протокола
        
        :param _size: размер буфера в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetDiagnosticFileName_t (_mapdiagnostic.buffer(), _size)

    mapCreateCoder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCreateCoder', ctypes.c_char_p, ctypes.c_int)
    def mapCreateCoder(_key: ctypes.c_char_p, _size: int) -> ctypes.c_void_p:
        """
        Получить идентификатор системы кодирования
        
        :param _key: строка, содержащая двоичный ключ для кодирования данных Ключ должен иметь случайное равномерное заполнение, например, методом преобразования пароля пользователя и текущего времени по алгоритму ``MD5``
        
        :param _size: длина строки (должна быть равна ``32`` байта)
        
        :returns: При ошибке возвращает ноль
        
        .. note::

           После завершения кодирования/раскодирования нужно освободить ресурсы
           функцией mapDeleteCoder
        """
        return mapCreateCoder_t (_key, _size)

    mapCoderOn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCoderOn', ctypes.c_void_p, ctypes.c_char_p, ctypes.c_long)
    def mapCoderOn(_hcoder: ctypes.c_void_p, _memory: ctypes.c_char_p, _size: int) -> int:
        """
        Закодировать область данных заданным ключом (длина области кратна 16)
        
        :param _hcoder: идентификатор системы кодирования
        
        :param _memory: адрес области памяти, которую нужно закодировать
        
        :param _size: размер области памяти для кодирования, кратный ``16`` байтам Для кодирования применяются операции ``XOR`` и циклического сдвига данных Состояние ключа меняется при кодировании под управлением кодируемых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCoderOn_t (_hcoder, _memory, _size)

    mapCoderOff_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCoderOff', ctypes.c_void_p, ctypes.c_char_p, ctypes.c_long)
    def mapCoderOff(_hcoder: ctypes.c_void_p, _memory: ctypes.c_char_p, _size: int) -> int:
        """
        Раскодировать область данных заданным ключом (длина области кратна 16)
        
        :param _hcoder: идентификатор системы кодирования
        
        :param _memory: адрес области памяти, которую нужно декодировать
        
        :param _size: размер области памяти для декодирования, кратный ``16`` байтам Для кодирования применяются операции ``XOR`` и циклического сдвига данных Состояние ключа меняется при кодировании под управлением кодируемых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCoderOff_t (_hcoder, _memory, _size)

    mapDeleteCoder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapDeleteCoder', ctypes.c_void_p)
    def mapDeleteCoder(_hcoder: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Освободить ресурсы после завершения кодирования/раскодирования
        
        :param _hcoder: идентификатор системы кодирования
        """
        return mapDeleteCoder_t (_hcoder)

    mapCommitObjectAsNew_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int,'mapCommitObjectAsNew', maptype.HOBJ)
    def mapCommitObjectAsNew(_info: maptype.HOBJ) -> int:
        """
        Добавить новый объект в карту
        
        :param _info: идентификатор объекта карты в памяти
               
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCommitObjectAsNew_t (_info)

    def mapInvalidate():
        """
        Перерисовать окно карты
        """
        mapSendMessage(maptype.MT_MAPWINPORT, maptype.MWP_INVALIDATE, 0)

    def mapSelectObjects(flag = 1):
        """
        Выделить объекты на карте по общим условиям
        """
        mapSendMessage(maptype.CM_PAN_SEARCH, flag, 0)

    def IntToStr(_number:int):
        """
        Целое число в строку
        """
        text = mapsyst.WTEXT(64)
        mapLongToStringUn(_number, text, text.size())
        return text.string()

    def FloatToStr(_value:float, _precision = 3):
        """
        Десятичная дробь в строку
        """
        text = mapsyst.WTEXT(64)
        mapDoubleToStringUn(_value, text, text.size(), _precision)
        return text.string()



def mapapi_healthcheck():
    return 1
