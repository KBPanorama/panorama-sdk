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
    *          Функции установки контекста поиска и отображения        *
    *                                                                  *
    ********************************************************************
    
"""

import os
import ctypes
import mapsyst
import maptype
import mapcreat
import mapgdi
import mmstruct

PACK_WIDTH = 1



try:
    if os.environ['gisselecdll']:
        gisselecname = os.environ['gisselecdll']
except KeyError:
    gisselecname = 'gis64selec.dll'

try:
    seleclib = mapsyst.LoadLibrary(gisselecname)
except Exception as e:
    print(e)
    seleclib = 0

if seleclib == 0:
    print(gisselecname)
else:
    selSemanticSelectInit_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selSemanticSelectInit', maptype.HRSC, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_long)
    def selSemanticSelectInit(_hrsc: maptype.HRSC, _parm: ctypes.POINTER(maptype.TASKPARMEX), _code: int) -> int:
        """
        Выбор из классификатора семантики c предустановленным кодом
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _code: код предустановленной семантики При открытии формы данный код семантики будет выбран
        
        :returns: При успешном выполнении возвращает код выбранной семантики При ошибке возвращает ноль
        :rtype: int
        """
        return selSemanticSelectInit_t (_hrsc, _parm, _code)

    selSemanticSelectFilterInit_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selSemanticSelectFilterInit', maptype.HRSC, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.c_long)
    def selSemanticSelectFilterInit(_hrsc: maptype.HRSC, _parm: ctypes.POINTER(maptype.TASKPARMEX), _code: int, _filter: ctypes.POINTER(ctypes.c_long), _count: int) -> int:
        """
        Выбор из классификатора семантики по фильтру семантик c предустановленным кодом
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _code: код предустановленной семантики При открытии формы данный код семантики будет выбран
        
        :param _filter: массив кодов семантик для выбора (фильтр)
        
        :param _count: количество элементов в массиве filter
        
        :returns: При успешном выполнении возвращает код выбранной семантики, иначе возвращает ноль
        :rtype: int
        """
        return selSemanticSelectFilterInit_t (_hrsc, _parm, _code, _filter, _count)

    selStringSemanticSelect_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selStringSemanticSelect', maptype.HRSC, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_long)
    def selStringSemanticSelect(_hrsc: maptype.HRSC, _parm: ctypes.POINTER(maptype.TASKPARMEX), _code: int) -> int:
        """
        Выбор из классификатора кода символьной семантики
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _code: код предустановленной семантики При открытии формы данный код семантики будет выбран, при code ``= 0`` первоначально будет выбран первый по порядку код При открытии формы будут доступны для выбора только семантики типа ``TSTRING`` - Символьная строка
        
        :returns: При успешном выполнении возвращает код выбранной семантики, при ошибке возвращает ноль
        :rtype: int
        """
        return selStringSemanticSelect_t (_hrsc, _parm, _code)

    selSetSiteViewStaff_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selSetSiteViewStaff', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(ctypes.c_long))
    def selSetSiteViewStaff(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _parm: ctypes.POINTER(maptype.TASKPARMEX), _activepage: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Установить фильтр отображения объектов карты
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных (``0`` - показать все карты)
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _activepage: номер активной вкладки (допустимо activepage ``= 0``)
        
        :returns: Если фильтр изменился, возвращает ненулевое значение
        :rtype: int
        """
        return selSetSiteViewStaff_t (_hmap, _hsite, _parm, _activepage)

    selRestoreSelect_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selRestoreSelect', maptype.HMAP)
    def selRestoreSelect(_hmap: maptype.HMAP) -> int:
        """
        Восстановить параметры отображения карты
        
        :param _hmap: идентификатор открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return selRestoreSelect_t (_hmap)

    selSaveSelect_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selSaveSelect', maptype.HMAP)
    def selSaveSelect(_hmap: maptype.HMAP) -> int:
        """
        Сохранить параметры отображения объектов
        
        :param _hmap: идентификатор открытых данных Установить доступ ко всем видам данных контекста поиска для всех карт
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return selSaveSelect_t (_hmap)

    selSetSearchFilterUn_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selSetSearchFilterUn', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(ctypes.c_long), maptype.PWCHAR)
    def selSetSearchFilterUn(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _activepage: ctypes.POINTER(ctypes.c_long), _title: mapsyst.WTEXT) -> int:
        """
        Установить фильтр поиска объектов карты
        
        :param _hmap: идентификатор открытых данных
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _activepage: номер активной вкладки (допустимо activepage ``= 0``)
        
        :param _title: заголовок окна фильтра объектов карты Фильтр поиска объектов карты автоматически восстанавливается/запоминается в служебном файле при старте/завершении программы
        
        :returns: Возвращает: ``1`` - выбран режим поиска объектов ``2`` - выделение объектов карты ``0`` - отмена При ошибке возвращает 0
        :rtype: int
        """
        return selSetSearchFilterUn_t (_hmap, _parm, _activepage, _title.buffer())

    selRestoreSeekSelect_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selRestoreSeekSelect', maptype.HMAP)
    def selRestoreSeekSelect(_hmap: maptype.HMAP) -> int:
        """
        Восстановить параметры поиска объектов
        
        :param _hmap: идентификатор открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return selRestoreSeekSelect_t (_hmap)

    selSaveSeekSelect_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selSaveSeekSelect', maptype.HMAP)
    def selSaveSeekSelect(_hmap: maptype.HMAP) -> int:
        """
        Сохранить параметры поиска объектов
        
        :param _hmap: идентификатор открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return selSaveSeekSelect_t (_hmap)

    selSetFilterMode_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selSetFilterMode', maptype.HSELECT, maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR)
    def selSetFilterMode(_hselect: maptype.HSELECT, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _isallobject: int, _parm: ctypes.POINTER(maptype.TASKPARMEX), _title: mapsyst.WTEXT) -> int:
        """
        Установить фильтр объектов карты с полным набором вкладок
        
        :param _hselect: контекст отбора объектов карты в hselect должна быть установлена карта
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _isallobject: режим установки списка слоев, локализаций и объектов в диалоге фильтра ``1`` - устанавливается полный состав слоев, локализаций и объектов в соответствии с составом объектов классификатора ``0`` - состав слоев, локализаций и объектов устанавивается в соответствии с составом объектов карты
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _title: заголовок окна фильтра объектов карты (``0`` - устанавливается стандартный заголовок)
        
        :returns: Если фильтр изменился, возвращает ненулевое значение
        :rtype: int
        """
        return selSetFilterMode_t (_hselect, _hmap, _hsite, _isallobject, _parm, _title.buffer())

    selSetMarkFilter_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selSetMarkFilter', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def selSetMarkFilter(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Установить фильтр объектов карты для выделения по рамке
        
        :param _hmap: идентификатор открытых данных
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return selSetMarkFilter_t (_hmap, _parm)

    selSetFilterByNameUn_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selSetFilterByNameUn', ctypes.POINTER(maptype.TASKPARMEX), maptype.HSELECT, maptype.HRSC, ctypes.POINTER(mmstruct.NAMESARRAY), maptype.PWCHAR)
    def selSetFilterByNameUn(_parm: ctypes.POINTER(maptype.TASKPARMEX), _hselect: maptype.HSELECT, _hrsc: maptype.HRSC, _namesarray: ctypes.POINTER(mmstruct.NAMESARRAY), _title: mapsyst.WTEXT) -> int:
        """
        Установить фильтр объектов классификатора с полным набором вкладок
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _hselect: контекст поиска объектов карты
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _namesarray: установить ``0`` (не используется)
        
        :param _title: заголовок окна фильтра объектов карты (``0`` - устанавливается стандартный заголовок)
        
        :returns: Если фильтр изменился, возвращает ненулевое значение
        :rtype: int
        """
        return selSetFilterByNameUn_t (_parm, _hselect, _hrsc, _namesarray, _title.buffer())

    selSetObjectFilter_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selSetObjectFilter', maptype.HSELECT, maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR)
    def selSetObjectFilter(_hselect: maptype.HSELECT, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _isallobject: int, _parm: ctypes.POINTER(maptype.TASKPARMEX), _title: mapsyst.WTEXT) -> int:
        """
        Установить фильтр объектов классификатора с вкладками слоев и объектов
        
        :param _hselect: контекст отбора объектов карты в hselect должна быть установлена карта (``HSITE``)
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _isallobject: режим установки списка слоев, локализаций и объектов в диалоге фильтра ``1`` - устанавливается полный состав слоев, локализаций и объектов в соответствии с составом объектов классификатора ``0`` - состав слоев, локализаций и объектов устанавивается в соответствии с составом объектов карты
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _title: заголовок окна фильтра объектов карты (``0`` - устанавливается стандартный заголовок)
        
        :returns: Если фильтр изменился, возвращает ненулевое значение
        :rtype: int
        """
        return selSetObjectFilter_t (_hselect, _hmap, _hsite, _isallobject, _parm, _title.buffer())

    selSetSiteModelFilterTitleEx_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selSetSiteModelFilterTitleEx', maptype.HMAP, maptype.HSITE, maptype.HSELECT, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, ctypes.c_long, maptype.PWCHAR)
    def selSetSiteModelFilterTitleEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT, _parm: ctypes.POINTER(maptype.TASKPARMEX), _modelname: mapsyst.WTEXT, _namesize: int, _title: mapsyst.WTEXT) -> int:
        """
        Сформировать модель отбора объектов и записать ее в файл моделей
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных для которой формируется модель
        
        :param _hselect: пользовательский контекст отображения/поиска объектов карты (устанавливается, если не выбрана модель)
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _modelname: имя модели
        
        :param _namesize: длина модели в байтах
        
        :param _title: заголовок окна фильтра объектов карты (``0`` - устанавливается стандартный заголовок)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return selSetSiteModelFilterTitleEx_t (_hmap, _hsite, _hselect, _parm, _modelname.buffer(), _namesize, _title.buffer())

    selSetModelsFilterTitleUn_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selSetModelsFilterTitleUn', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_long), maptype.PWCHAR)
    def selSetModelsFilterTitleUn(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _modelnames: mapsyst.WTEXT, _modelnames3d: mapsyst.WTEXT, _namesize: int, _modelcount: int, _modifyflag: ctypes.POINTER(ctypes.c_long), _title: mapsyst.WTEXT) -> int:
        """
        Сформировать модели отбора объектов для наборов 2D и 3D и записать их в файл моделей
        
        :param _hmap: идентификатор открытых данных
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _modelnames: массив имен моделей
        
        :param _modelnames3d: массив имен 3D-моделей
        
        :param _namesize: размер имен моделей
        
        :param _modelcount: количество моделей
        
        :param _modifyflag: массив флагов изменений моделей
        
        :param _title: заголовок окна фильтра объектов карты (``0`` - устанавливается стандартный заголовок) Размерность массивов modelnames и modifyflag равна (количество сайтов + ``1``) ``* 2`` для наборов 2D и 3D
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return selSetModelsFilterTitleUn_t (_hmap, _parm, _modelnames.buffer(), _modelnames3d.buffer(), _namesize, _modelcount, _modifyflag, _title.buffer())

    selSetLayersFilter_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selSetLayersFilter', maptype.HWND, maptype.HRSC, maptype.HSELECT, ctypes.c_char_p, maptype.HINSTANCE)
    def selSetLayersFilter(_hwnd: maptype.HWND, _hrsc: maptype.HRSC, _hselect: maptype.HSELECT, _title: ctypes.c_char_p, _rc: maptype.HINSTANCE) -> int:
        """
        Установить фильтр слоев карты
        
        :param _hwnd: идентификатор родительского окна
        
        :param _hrsc: идентификатор классификатора карты
        
        :param _hselect: контекст поиска объектов карты
        
        :param _title: заголовок окна фильтра слоев карты
        
        :param _rc: записать ``0`` (архаизм)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return selSetLayersFilter_t (_hwnd, _hrsc, _hselect, _title, _rc)

    selSearchName_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selSearchName', maptype.HMAP, maptype.HSELECT, ctypes.POINTER(mmstruct.ARRAYNAME), ctypes.POINTER(maptype.TASKPARMEX))
    def selSearchName(_hmap: maptype.HMAP, _hselect: maptype.HSELECT, _arrayname: ctypes.POINTER(mmstruct.ARRAYNAME), _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Установить условия поиска объектов карты по названию семантики
        
        :param _hmap: идентификатор открытых данных
        
        :param _hselect: контекст поиска объектов карты
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _arrayname: условия поиска по названию (описание mmstruct.h) Help вызывается по топику ``MARPOISK``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return selSearchName_t (_hmap, _hselect, _arrayname, _parm)

    selSearchObjectByArea_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selSearchObjectByArea', ctypes.POINTER(maptype.TASKPARMEX), maptype.HMAP, maptype.HOBJ, maptype.HWND, ctypes.POINTER(mmstruct.AREASEEKPARM))
    def selSearchObjectByArea(_parm: ctypes.POINTER(maptype.TASKPARMEX), _hmap: maptype.HMAP, _hobj: maptype.HOBJ, _hwnd: maptype.HWND, _seekparm: ctypes.POINTER(mmstruct.AREASEEKPARM)) -> int:
        """
        Установить параметры поиска объектов карты по области
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _hmap: идентификатор открытых данных
        
        :param _hobj: рамка области поиска Метрика рамки области поиска должна быть в метрах
        
        :param _hwnd: идентификатор окна назначения сообщений ``WM_PROGRESSBAR``
        
        :param _seekparm: параметры поиска по области Help вызывается по топику ``POISKOBL``
        
        :returns: Возвращает: ``1`` - выбран режим поиска объектов ``2`` - выбран режим выделения объектов карты ``3`` - выбран режим выбора области ``0`` - ошибка или отказ
        :rtype: int
        """
        return selSearchObjectByArea_t (_parm, _hmap, _hobj, _hwnd, _seekparm)

    selFindStaff_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selFindStaff', maptype.HMAP, maptype.HSELECT, ctypes.POINTER(maptype.TASKPARMEX))
    def selFindStaff(_hmap: maptype.HMAP, _hselect: maptype.HSELECT, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Поиск объектов карты по форме
        
        :param _hmap: идентификатор открытых данных
        
        :param _hselect: контекст поиска объектов карты
        
        :param _parm: параметры задачи (описание в maptype.h) Help вызывается по топику ``FORMPOISK``
        
        :returns: Если фильтр изменился, возвращает ненулевое значение При ошибке возвращает ноль
        :rtype: int
        """
        return selFindStaff_t (_hmap, _hselect, _parm)

    selRestoreParmsUn_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selRestoreParmsUn', maptype.HMAP, maptype.PWCHAR)
    def selRestoreParmsUn(_hmap: maptype.HMAP, _modelname: mapsyst.WTEXT) -> int:
        """
        Boccтановить параметры поиска объектов по имени модели
        
        :param _hmap: идентификатор открытых данных
        
        :param _modelname: имя модели
        
        :returns: При ошибке возвращает 0, иначе 1
        :rtype: int
        """
        return selRestoreParmsUn_t (_hmap, _modelname.buffer())

    selMarkParmsModelName_t = mapsyst.GetProcAddress(seleclib,ctypes.POINTER(ctypes.c_char),'selMarkParmsModelName')
    def selMarkParmsModelName() -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить имя модели параметров выделения объектов по рамке
        
        :returns: Возвращает имя модели
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return selMarkParmsModelName_t ()

    selSetSelectByModel_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selSetSelectByModel', maptype.HSELECT, maptype.HMAP, ctypes.c_int, ctypes.c_int)
    def selSetSelectByModel(_hselect: maptype.HSELECT, _hmap: maptype.HMAP, _nmap: int, _nmodel: int) -> int:
        """
        Установить контекст по модели с номером nmodel
        
        :param _hselect: контекст поиска объектов карты
        
        :param _hmap: идентификатор открытых данных
        
        :param _nmap: номер карты в цепочке
        
        :param _nmodel: номер модели
        
        :returns: При ошибке возвращает 0, иначе 1
        :rtype: int
        """
        return selSetSelectByModel_t (_hselect, _hmap, _nmap, _nmodel)

    selSearchAddress_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selSearchAddress', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX))
    def selSearchAddress(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Установить условия поиска объектов карты по адресу
        
        :param _hmap: идентификатор открытых данных
        
        :param _parm: параметры задачи (описание в maptype.h) Help вызывается по топику ``IDN_SEARCH_ADDR``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return selSearchAddress_t (_hmap, _parm)

    selSetSelectByMap_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selSetSelectByMap', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_long)
    def selSetSelectByMap(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _flag: int) -> int:
        """
        Открыть диалог выбора карт и установить параметры поиска объектов по выбранным картам
        
        :param _hmap: идентификатор открытых данных
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _flag: флаг выделения карт в списке ``0`` - не выделять ``1`` - выделить все ``2`` - выделить карты, доступные для редактирования Для выделения объектов в окне карты после функции selSetSelectByMap вызвать PostTheMessage(parm->DocHandle, ``CM_PAN_SEARCH``, ``1``, ``0``)
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return selSetSelectByMap_t (_hmap, _parm, _flag)

    selSetAreaFilter_t = mapsyst.GetProcAddress(seleclib,ctypes.c_long,'selSetAreaFilter', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.POINTER(ctypes.c_long))
    def selSetAreaFilter(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _activepage: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Установить фильтр поиска объектов карты по модели
        
        :param _hmap: идентификатор открытых данных
        
        :param _parm: параметры задачи (описание в maptype.h)
        
        :param _activepage: номер активной вкладки (допустимо activepage ``= 0``) Фильтр поиска объектов карты автоматически восстанавливается/запоминается в служебном файле при старте/завершении программы
        
        :returns: Возвращает: ``1`` - выбран режим поиска объектов ``2`` - выбран режим выделения объектов карты ``0`` - ошибка или отказ
        :rtype: int
        """
        return selSetAreaFilter_t (_hmap, _parm, _activepage)



def mapselec_healthcheck():
    return 1
