#!/usr/bin/env python3

"""
.. code-block:: none

    ********************************************************************
    *                                                                  *
    *              Copyright (c) PANORAMA Group 1991-2026              *
    *                      All Rights Reserved                         *
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
    mapWhatObjectPro_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapWhatObjectPro', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DFRAME), ctypes.c_long, ctypes.c_long, maptype.HPAINT, ctypes.POINTER(ctypes.c_long))
    def mapWhatObjectPro(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _frame: ctypes.POINTER(maptype.DFRAME), _flag: int, _place: int, _hpaint: maptype.HPAINT, _reason: ctypes.POINTER(ctypes.c_long)) -> maptype.HOBJ:
        """
        Найти видимые объекты в окрестности точки, заданной прямоугольной рамкой
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти, в котором будет размещен результат
        
        :param _frame: прямоугольная область поиска объекта в системе координат, заданной переменной place
        
        :param _flag: порядок поиска объектов (``WO_FIRST``, ``WO_NEXT``...)
        
        :param _place: система координат (``PP_PLANE``, ``PP_GEO``, ...)
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функции отображения, создается функцией mapCreatePaintControl
        
        :param _reason: поле для размещения кода причины неудачи при поиске: ``0`` - объект не обнаружен ``1`` - объект обнаружен, но включен режим пропуска объектов оформления (mapGetSkipDesignObjectFlag) Применяется для перебора видимых объектов при нажатии левой кнопки мыши на карте Координаты области пересчитываются в пикселы в текущем масштабе отображения В список выбранных могут попасть объекты, которые отображаются в текущем масштабе рядом с областью выбора в пределах нескольких пикселов Площадные объекты выбираются в пределах рамки размером ``512``х``512`` пикселов в текущем масштабе изображения Выбор объекта в ``"точке карты"`` рекомендуется начинать с последнего, который нарисован поверх остальных (это чуть медленнее прямого поиска) При поиске с флажками ``WO_NEXT``, ``WO_BACK`` параметр hobj должен содержать результат предыдущего поиска Поиск выполнется среди тех объектов, которые видны на экране, если не установлен флаг ``WO_VISUALIGNORE``
        
        :returns: Если объект найден - возвращает значение hobj Если объект не найден - возвращает 0, в reason записывается код причины неудачи при поиске
        :rtype: maptype.HOBJ
        """
        return mapWhatObjectPro_t (_hmap, _hobj, _frame, _flag, _place, _hpaint, _reason)

    mapWhatObjectBySelectEx_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapWhatObjectBySelectEx', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DFRAME), maptype.HSELECT, ctypes.c_long, ctypes.c_long, maptype.HPAINT)
    def mapWhatObjectBySelectEx(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _frame: ctypes.POINTER(maptype.DFRAME), _hselect: maptype.HSELECT, _flag: int, _place: int, _hpaint: maptype.HPAINT) -> maptype.HOBJ:
        """
        Найти видимые объекты в окрестности точки, заданной прямоугольной рамкой, удовлетворяющие условиям поиска
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти, в котором будет размещен результат
        
        :param _frame: прямоугольная область поиска объекта в системе координат, заданной переменной place
        
        :param _hselect: контекст условий отбора объектов
        
        :param _flag: порядок поиска объектов (``WO_FIRST``, ``WO_NEXT``...)
        
        :param _place: система координат (``PP_PLANE``, ``PP_GEO``, ...)
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функции отображения, создается функцией mapCreatePaintControl Применяется для перебора видимых объектов при нажатии левой кнопки мыши на карте
        
        :returns: Если объект найден - возвращает значение hobj, иначе - 0
        :rtype: maptype.HOBJ
        """
        return mapWhatObjectBySelectEx_t (_hmap, _hobj, _frame, _hselect, _flag, _place, _hpaint)

    mapWhatActiveObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapWhatActiveObject', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DFRAME), ctypes.c_long, ctypes.c_long)
    def mapWhatActiveObject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _frame: ctypes.POINTER(maptype.DFRAME), _flag: int, _place: int) -> int:
        """
        Найти активные видимые объекты в окрестности точки, заданной прямоугольной рамкой
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти, в котором будет размещен результат
        
        :param _frame: прямоугольная область поиска объекта в системе координат, заданной переменной place
        
        :param _flag: порядок поиска объектов (``WO_FIRST``, ``WO_NEXT``...)
        
        :param _place: система координат (``PP_PLANE``, ``PP_GEO``, ...) Применяется для перебора видимых объектов при нажатии левой кнопки мыши на карте Активные объекты - доступные для интерактивного выбора (оператором) Установка условий поиска выполняется функцией mapSetSiteActiveSelect
        
        :returns: Если объект найден - возвращает 1, иначе - 0
        :rtype: int
        """
        return mapWhatActiveObject_t (_hmap, _hobj, _frame, _flag, _place)

    mapSetTextPlace_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetTextPlace', maptype.HMAP, ctypes.c_long)
    def mapSetTextPlace(_hmap: maptype.HMAP, _order: int) -> ctypes.c_void_p:
        """
        Установить порядок обнаружения подписей при поиске объектов в точке карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _order: порядок выбора подписи
        
        .. note::

           Если order равен нулю, то при переборе в обратном порядке (WO_LAST, WO_PREV) сначала будут идти подписи
           Если order не равен нулю, то при переборе в обратном порядке подписи будут последними
        """
        return mapSetTextPlace_t (_hmap, _order)

    mapGetTextPlace_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetTextPlace', maptype.HMAP)
    def mapGetTextPlace(_hmap: maptype.HMAP) -> int:
        """
        Запросить порядок обнаружения подписей при поиске объектов в точке карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: Если при переборе в обратном порядке (WO_LAST, WO_PREV) сначала будут идти подписи - возвращает 0 Если при переборе в обратном порядке подписи будут последними - возвращает 1
        :rtype: int
        """
        return mapGetTextPlace_t (_hmap)

    mapSetSkipDesignObjectFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetSkipDesignObjectFlag', ctypes.c_long)
    def mapSetSkipDesignObjectFlag(_flag: int) -> ctypes.c_void_p:
        """
        Установить флаг пропуска объектов оформления при поиске объектов в точке карты
        
        :param _flag: флаг пропуска объектов оформления: ``1`` - пропускать, ``0`` - не пропускать
        """
        return mapSetSkipDesignObjectFlag_t (_flag)

    mapGetSkipDesignObjectFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSkipDesignObjectFlag')
    def mapGetSkipDesignObjectFlag() -> int:
        """
        Запросить флаг пропуска объектов оформления при поиске объектов в точке карты
        
        :returns: Возвращает флаг пропуска объектов оформления: ``1`` - пропускать, ``0`` - не пропускать
        :rtype: int
        """
        return mapGetSkipDesignObjectFlag_t ()

    mapSeekObjectUn_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapSeekObjectUn', maptype.HMAP, maptype.HOBJ, maptype.PWCHAR, ctypes.c_long)
    def mapSeekObjectUn(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _sheetname: mapsyst.WTEXT, _key: int) -> maptype.HOBJ:
        """
        Найти объект по уникальному номеру объекта в карте с заданным названием листа (номенклатуры)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти, в котором будет размещен результат
        
        :param _sheetname: название листа карты
        
        :param _key: уникальный номер объекта в листе карты
        
        :returns: Если объект найден - возвращает значение hobj, иначе - 0
        :rtype: maptype.HOBJ
        """
        return mapSeekObjectUn_t (_hmap, _hobj, _sheetname.buffer(), _key)

    mapSeekObjectInList_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapSeekObjectInList', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapSeekObjectInList(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _sheetnumber: int, _key: int) -> maptype.HOBJ:
        """
        Найти объект по уникальному номеру объекта в заданном листе карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hobj: идентификатор объекта карты в памяти, в котором будет размещен результат
        
        :param _sheetnumber: номер листа карты (с ``1``)
        
        :param _key: уникальный номер объекта в листе карты
        
        :returns: Если объект найден - возвращает значение hobj, иначе - 0
        :rtype: maptype.HOBJ
        """
        return mapSeekObjectInList_t (_hmap, _hsite, _hobj, _sheetnumber, _key)

    mapSeekObjectNumberUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekObjectNumberUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapSeekObjectNumberUn(_hmap: maptype.HMAP, _sheetname: mapsyst.WTEXT, _key: int) -> int:
        """
        Найти порядковый номер объекта по уникальному номеру объекта в карте с заданным названием листа (номенклатуры)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _sheetname: название листа карты
        
        :param _key: уникальный номер объекта в листе карты
        
        :returns: Возвращает порядковый номер объекта в листе карты (в том числе, для удаленных объектов) (при сортировке карты записи удаленных объектов исключаются, порядковые номера объектов изменяются) При ошибке возвращает ноль
        :rtype: int
        """
        return mapSeekObjectNumberUn_t (_hmap, _sheetname.buffer(), _key)

    mapSeekObjectNumberEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekObjectNumberEx', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long)
    def mapSeekObjectNumberEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _sheetnumber: int, _key: int) -> int:
        """
        Найти порядковый номер объекта по уникальному номеру объекта в заданном листе карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _sheetnumber: номер листа карты (с ``1``)
        
        :param _key: уникальный номер объекта в листе карты
        
        :returns: Возвращает порядковый номер объекта в листе карты (в том числе, для удаленных объектов) (при сортировке карты записи удаленных объектов исключаются, порядковые номера объектов изменяются) При ошибке возвращает ноль
        :rtype: int
        """
        return mapSeekObjectNumberEx_t (_hmap, _hsite, _sheetnumber, _key)

    mapSeekObjectByGUID_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekObjectByGUID', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_long, ctypes.POINTER(maptype.INT64TWO))
    def mapSeekObjectByGUID(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _sheetnumber: int, _guid: ctypes.POINTER(maptype.INT64TWO)) -> int:
        """
        Найти объект по GUID в листе (значение семантики с кодом OBJECTGUID = 32799)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hobj: идентификатор объекта карты в памяти, в котором будет размещен результат
        
        :param _sheetnumber: номер листа карты (с ``1``)
        
        :param _guid: структура, содержащая значение ``GUID`` в двоичной форме
        
        :returns: Возвращает порядковый номер объекта в листе карты (в том числе, для удаленных объектов) При ошибке возвращает ноль
        :rtype: int
        """
        return mapSeekObjectByGUID_t (_hmap, _hsite, _hobj, _sheetnumber, _guid)

    mapSeekObjectByStringGUID_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekObjectByStringGUID', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_long, ctypes.c_char_p)
    def mapSeekObjectByStringGUID(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _sheetnumber: int, _guid: ctypes.c_char_p) -> int:
        """
        Найти объект по GUID в листе (значение семантики OBJECTGUID 32799)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hobj: идентификатор объекта карты в памяти, в котором будет размещен результат
        
        :param _sheetnumber: номер листа карты (с ``1``)
        
        :param _guid: строка, содержащая значение ``GUID`` (``32`` или ``36`` символов, если с тире)
        
        :returns: Возвращает порядковый номер объекта в листе карты (в том числе, для удаленных объектов) При ошибке возвращает ноль
        :rtype: int
        """
        return mapSeekObjectByStringGUID_t (_hmap, _hsite, _hobj, _sheetnumber, _guid)

    mapSeekSelectObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekSelectObject', maptype.HMAP, maptype.HOBJ, maptype.HSELECT, ctypes.c_long)
    def mapSeekSelectObject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _hselect: maptype.HSELECT, _flag: int) -> int:
        """
        Найти объект по заданным условиям отбора среди всех объектов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти, в котором будет размещен результат
        
        :param _hselect: контекст условий отбора объектов
        
        :param _flag: порядок поиска объектов (``WO_FIRST``, ``WO_NEXT``...) При поиске с флажками ``WO_NEXT``, ``WO_BACK`` параметр hobj должен содержать результат предыдущего поиска
        
        :returns: Если объект не найден - возвращает ноль
        :rtype: int
        """
        return mapSeekSelectObject_t (_hmap, _hobj, _hselect, _flag)

    mapSeekSelectObjectCountEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekSelectObjectCountEx', maptype.HMAP, maptype.HSELECT, ctypes.c_long)
    def mapSeekSelectObjectCountEx(_hmap: maptype.HMAP, _hselect: maptype.HSELECT, _flag: int) -> int:
        """
        Запросить число объектов на карте, удовлетворяющих условиям отбора
        
        :param _hselect: контекст условий отбора объектов
        
        :param _flag: флаг условий поиска: ``WO_INMAP`` - подсчет выполняется на той карте, для которой был создан контекст поиска, иначе - поиск по всем картам
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSeekSelectObjectCountEx_t (_hmap, _hselect, _flag)

    mapSeekSelectNearestObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekSelectNearestObject', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), maptype.HSELECT, ctypes.c_long)
    def mapSeekSelectNearestObject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _srcpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _destpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _hselect: maptype.HSELECT, _flag: int) -> int:
        """
        Найти ближайший объект по заданным условиям среди всех объектов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти, в котором будет размещен результат
        
        :param _srcpoint: координаты исходной точки (в метрах), относительно которой выполняется поиск
        
        :param _destpoint: поле для размещения координат ближайшей виртуальной точки на контуре объекта (в метрах документа)
        
        :param _hselect: контекст условий отбора объектов
        
        :param _flag: дополнительные условия поиска объектов: ``WO_CANCEL``, ``WO_INMAP``, ``WO_VISUAL`` (значения ``WO_FIRST``, ``WO_NEXT`` не учитываются)
        
        :returns: Если объект не найден - возвращает ноль
        :rtype: int
        
        .. note::

           Если flag равен 0, выполняется поиск по всем картам среди всех объектов
        """
        return mapSeekSelectNearestObject_t (_hmap, _hobj, _srcpoint, _destpoint, _hselect, _flag)

    mapFindAdjustObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapFindAdjustObject', maptype.HMAP, maptype.HOBJ, ctypes.c_long, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double)
    def mapFindAdjustObject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _side: int, _hdest: maptype.HOBJ, _destpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _radius: float) -> int:
        """
        Найти объект, подходящий условиям поиска соседних объектов в первой и последней точках контура
        
        :param _hobj: идентификатор объекта карты в памяти, для которого ищутся соседи
        
        :param _side: сторона объекта, для которой ищутся соседи (``0`` - первая точка, иначе - последняя)
        
        :param _hdest: идентификатор объекта карты в памяти, в котором будет размещен результат
        
        :param _destpoint: поле для размещения координат ближайшей найденной точки (в метрах)
        
        :param _radius: радиус поиска (максимальный радиус поиска ``= 7`` км) Списки видов объектов для первой и последней точек контура и список семантик, которые должны иметь совпадающие значения с семантиками объекта, должны быть настроены в классификаторе заблаговременно
        
        :returns: Если условия для соседей заданы, но сосед не найден - возвращает -1 Если у объекта отсутствуют семантики, которые должны совпадать с семантиками соседних объектов - возвращает -2 Если условия не заданы - возвращает ноль
        :rtype: int
        
        .. note::

           Если поиск выполняется для второй точки (side !``= 0``), то входное значение (hobj) будет пропущено при поиске
        """
        return mapFindAdjustObject_t (_hmap, _hobj, _side, _hdest, _destpoint, _radius)

    mapSeekViewObject_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapSeekViewObject', maptype.HMAP, maptype.HOBJ, maptype.HSELECT, ctypes.c_long)
    def mapSeekViewObject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _hselect: maptype.HSELECT, _flag: int) -> maptype.HOBJ:
        """
        Найти объект по заданным условиям среди отображаемых объектов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти, в котором будет размещен результат
        
        :param _hselect: контекст условий отбора объектов
        
        :param _flag: порядок поиска объектов (``WO_FIRST``, ``WO_NEXT``...) При поиске с флажками ``WO_NEXT``, ``WO_BACK`` параметр hobj должен содержать результат предыдущего поиска
        
        :returns: Если объект не найден - возвращает ноль
        :rtype: maptype.HOBJ
        """
        return mapSeekViewObject_t (_hmap, _hobj, _hselect, _flag)

    mapSeekAdjacentObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekAdjacentObject', maptype.HMAP, maptype.HOBJ, maptype.HOBJ, ctypes.POINTER(maptype.MAPADJACENTSECTION), maptype.HSELECT, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapSeekAdjacentObject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _hdest: maptype.HOBJ, _section: ctypes.POINTER(maptype.MAPADJACENTSECTION), _hselect: maptype.HSELECT, _maxdistance: float, _flag: int, _mode: int) -> int:
        """
        Найти объект, имеющий примыкающие участки контура с заданным объектом
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор существующего объекта, для которого надо найти примыкающие участки
        
        :param _hdest: идентификатор существующего объекта, в котором будет размещен результат
        
        :param _section: указатель на структуру для записи описания найденного участка
        
        :param _hselect: контекст условий отбора объектов
        
        :param _maxdistance: максимальное расстояние между точками участков в метрах
        
        :param _flag: порядок поиска объектов (``WO_FIRST``, ``WO_NEXT``...)
        
        :param _mode: режим поиска общих участков: ``0`` - искать общие участки только с внешним контуром, ``1`` - с учетом подобъектов (нумерация точек объекта и подобъектов ``MAPADJACENTSECTION``::first и last - сквозная) Поиск выполняется в карте, на которой находится выбранный объект При поиске с флажками ``WO_NEXT``, ``WO_BACK`` параметр hdest должен содержать результат предыдущего поиска
        
        :returns: Если объект не найден - возвращает ноль, иначе - возвращает номер участка
        :rtype: int
        """
        return mapSeekAdjacentObject_t (_hmap, _hobj, _hdest, _section, _hselect, _maxdistance, _flag, _mode)

    mapSeekAdjacentListEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekAdjacentListEx', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.MAPADJACENTLISTEX), ctypes.c_long, maptype.HSELECT, ctypes.c_double, ctypes.c_long, ctypes.c_long)
    def mapSeekAdjacentListEx(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _sectionlist: ctypes.POINTER(maptype.MAPADJACENTLISTEX), _sectioncount: int, _hselect: maptype.HSELECT, _maxdistance: float, _excludereverse: int, _mode: int) -> int:
        """
        Найти объекты, имеющие примыкающие участки контура с заданным объектом
        
        Поиск ведется в карте, где находится выбранный объект
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор существующего объекта карты, для которого надо найти примыкающие участки
        
        :param _sectionlist: память для записи общих участков контуров примыкающих объектов
        
        :param _sectioncount: максимальное количество общих участков контуров
        
        :param _hselect: контекст условий отбора объектов
        
        :param _maxdistance: максимальное расстояние между точками участков в метрах
        
        :param _excludereverse: признак исключения обратных примыкающих участков: ``0`` - записывать прямые и обратные примыкающие участки, ``1`` - обратные примыкающие участки (с одинаковой первой и последней точкой) не записывать
        
        :param _mode: режим поиска общих участков: ``0`` - искать общие участки только с внешним контуром, ``1`` - с учетом подобъектов (нумерация точек объекта и подобъектов ``MAPADJACENTLISTEX``::First и Last - сквозная) Поиск выполняется в карте, на которой находится выбранный объект
        
        :returns: Если соседи не найдены - возвращает ноль, иначе - количество соседей
        :rtype: int
        """
        return mapSeekAdjacentListEx_t (_hmap, _hobj, _sectionlist, _sectioncount, _hselect, _maxdistance, _excludereverse, _mode)

    mapCreateSeekConnectPath_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCreateSeekConnectPath', maptype.HMAP, maptype.HSELECT, maptype.HOBJ, ctypes.c_long, maptype.HOBJ, ctypes.c_double)
    def mapCreateSeekConnectPath(_hmap: maptype.HMAP, _hselect: maptype.HSELECT, _hobj: maptype.HOBJ, _subject: int, _hdest: maptype.HOBJ, _maxdistance: float) -> ctypes.c_void_p:
        """
        Создать процесс поиска примыкающих участков контура для заданного подобъекта
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hselect: контекст условий отбора объектов
        
        :param _hobj: идентификатор существующего объекта, для которого надо найти примыкающие участки
        
        :param _subject: номер подобъекта c ``0``
        
        :param _hdest: идентификатор существующего объекта, в котором будет размещен результат
        
        :param _maxdistance: максимальное расстояние между точками участков в метрах По окончании обработки необходимо вызвать mapFreeSeekConnectPath
        
        :returns: При ошибке возвращает 0
        """
        return mapCreateSeekConnectPath_t (_hmap, _hselect, _hobj, _subject, _hdest, _maxdistance)

    mapFreeSeekConnectPath_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeSeekConnectPath', ctypes.c_void_p)
    def mapFreeSeekConnectPath(_seekconnect: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Освободить ресурсы, выделенные в mapCreateSeekConnectPath
        
        :param _seekconnect: идентификатор процесса поиска
        """
        return mapFreeSeekConnectPath_t (_seekconnect)

    mapSeekConnectPath_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekConnectPath', ctypes.c_void_p, ctypes.POINTER(maptype.CONNECTPATH))
    def mapSeekConnectPath(_seekconnect: ctypes.c_void_p, _section: ctypes.POINTER(maptype.CONNECTPATH)) -> int:
        """
        Запросить следующий примыкающий участок для заданного подобъекта
        
        :param _seekconnect: идентификатор процесса поиска
        
        :param _section: указатель на структуру для записи описания найденного участка Возможен возврат участка из одной точки (касание в одной точке) Для замкнутых объектов участок может проходить через первую (последнюю) точку Направление участка на соседнем объекте всегда совпадает с направлением цифрования Направление на главном объекте устанавливается в ``CONNECTPATH``::IsForward
        
        :returns: При ошибке или если смежный участок не найден возвращает ноль
        :rtype: int
        """
        return mapSeekConnectPath_t (_seekconnect, _section)

    mapTestObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapTestObject', maptype.HOBJ, maptype.HSELECT)
    def mapTestObject(_hobj: maptype.HOBJ, _hselect: maptype.HSELECT) -> int:
        """
        Проверить соответствие объекта условиям отбора объектов
        
        :param _hobj: идентификатор существующего объекта карты
        
        :param _hselect: контекст условий отбора объектов
        
        :returns: Если условия поиска не заданы (hselect ``= 0``), возвращает 1 Если соответствует - возвращает ненулевое значение, иначе - 0
        :rtype: int
        """
        return mapTestObject_t (_hobj, _hselect)

    mapTotalTestObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapTotalTestObject', maptype.HMAP, maptype.HOBJ)
    def mapTotalTestObject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ) -> int:
        """
        Проверить соответствие объекта условиям обобщенного поиска объектов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор существующего объекта карты Для установки условий обобщенного поиска объектов используются функции: mapSetTotalSeekMapRule, mapSetTotalSeekViewRule, mapTotalSeekSampleAppendObject, mapSetTotalSeekSampleUn, mapSetTotalSeekAccess
        
        :returns: Если соответствует - возвращает ненулевое значение, иначе - 0
        :rtype: int
        """
        return mapTotalTestObject_t (_hmap, _hobj)

    mapReadObjectByNumberEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapReadObjectByNumberEx', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapReadObjectByNumberEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _sheetnumber: int, _objectnumber: int) -> int:
        """
        Найти объект по номеру листа и порядковому номеру объекта (прямой доступ к объекту без перебора)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hobj: идентификатор объекта карты в памяти, в котором будет размещен результат
        
        :param _sheetnumber: номер листа карты, от ``1`` до mapGetSiteListCount(...)
        
        :param _objectnumber: порядковый номер объекта в листе, от ``1`` до mapGetSiteObjectCount(...)
        
        :returns: Если объект имеет признак ``"удален"``, то функция возвращает 1 (READOBJECT_DELETED) При успешном выполнении возвращает значение 2 (READOBJECT_OK) При ошибке возвращает ноль (READOBJECT_ERROR)
        :rtype: int
        """
        return mapReadObjectByNumberEx_t (_hmap, _hsite, _hobj, _sheetnumber, _objectnumber)

    mapReadObjectByKeyEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapReadObjectByKeyEx', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapReadObjectByKeyEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _sheetnumber: int, _key: int) -> int:
        """
        Выбор объекта по номеру листа и уникальному номеру объекта
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hobj: идентификатор объекта карты в памяти, в котором будет размещен результат
        
        :param _sheetnumber: номер листа карты, от ``1`` до mapGetSiteListCount(...)
        
        :param _key: уникальный номер объекта в листе карты
        
        :returns: Если объект имеет признак ``"удален"``, то функция возвращает 1 При успешном выполнении возвращает значение 2 При ошибке возвращает ноль
        :rtype: int
        """
        return mapReadObjectByKeyEx_t (_hmap, _hsite, _hobj, _sheetnumber, _key)

    mapGetTotalSeekMapRule_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetTotalSeekMapRule', maptype.HMAP)
    def mapGetTotalSeekMapRule(_hmap: maptype.HMAP) -> int:
        """
        Запросить правило обобщенного поиска объектов по картам
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: Возвращает: от 0 до mapGetSiteCount(...) - номер карты, по которой будет выполняться поиск (-1) - поиск будет выполняться по всем картам При ошибке возвращает число (-2)
        :rtype: int
        """
        return mapGetTotalSeekMapRule_t (_hmap)

    mapIsTotalSeekMapRule_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsTotalSeekMapRule', maptype.HMAP, ctypes.c_long)
    def mapIsTotalSeekMapRule(_hmap: maptype.HMAP, _mapnumber: int) -> int:
        """
        Проверить наличие объектов карты, соответствующих условиям обобщенного поиска объектов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _mapnumber: номер карты в открытых данных, от ``0`` до mapGetSiteCount(...)
        
        :returns: Если на карте есть объекты, соответствующие условиям - возвращает ненулевое значение
        :rtype: int
        """
        return mapIsTotalSeekMapRule_t (_hmap, _mapnumber)

    mapSetTotalSeekMapRule_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetTotalSeekMapRule', maptype.HMAP, ctypes.c_long)
    def mapSetTotalSeekMapRule(_hmap: maptype.HMAP, _mapnumber: int) -> ctypes.c_void_p:
        """
        Установить правило обобщенного поиска объектов по картам
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _mapnumber: номер карты, по которой выполняется поиск
        
        .. note::

           Если number ``= -1``, то поиск будет выполняться по всем картам
        """
        return mapSetTotalSeekMapRule_t (_hmap, _mapnumber)

    mapSetTotalSeekViewRule_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetTotalSeekViewRule', maptype.HMAP, ctypes.c_long)
    def mapSetTotalSeekViewRule(_hmap: maptype.HMAP, _view: int) -> ctypes.c_void_p:
        """
        Установить правило обобщенного поиска объектов для отображаемых объектов карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _view: признак поиска среди отображаемых объектов (``1``), использовать mapSeekViewObject
        
        .. note::

           Если view ``= 0``, то поиск будет выполняться среди всех объектов, использовать mapSeekSelectObject
        """
        return mapSetTotalSeekViewRule_t (_hmap, _view)

    mapGetTotalSeekViewRule_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetTotalSeekViewRule', maptype.HMAP)
    def mapGetTotalSeekViewRule(_hmap: maptype.HMAP) -> int:
        """
        Запросить правило обобщенного поиска для отображаемых объектов карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: Возвращает: ``1`` - поиск среди отображаемых объектов ``0`` - поиск среди всех объектов
        :rtype: int
        """
        return mapGetTotalSeekViewRule_t (_hmap)

    mapSetTotalSeekSampleUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetTotalSeekSampleUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapSetTotalSeekSampleUn(_hmap: maptype.HMAP, _sheetname: mapsyst.WTEXT, _key: int) -> int:
        """
        Добавить объект в список условий обобщенного поиска по уникальному номеру объекта и названию листа
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _sheetname: название листа карты
        
        :param _key: уникальный номер объекта в листе карты
        
        :returns: Если карта не найдена - возвращает ноль
        :rtype: int
        
        .. note::

           Если для карты установлены условия поиска по номерам объектов, то остальные условия (слой, локализация...) игнорируются
        """
        return mapSetTotalSeekSampleUn_t (_hmap, _sheetname.buffer(), _key)

    mapTotalSeekSampleAppendObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapTotalSeekSampleAppendObject', maptype.HOBJ)
    def mapTotalSeekSampleAppendObject(_hobj: maptype.HOBJ) -> int:
        """
        Добавить объект в список условий обобщенного поиска
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapTotalSeekSampleAppendObject_t (_hobj)

    mapSetTotalSeekAccess_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetTotalSeekAccess', maptype.HMAP, ctypes.c_long)
    def mapSetTotalSeekAccess(_hmap: maptype.HMAP, _access: int) -> int:
        """
        Установить условия обобщенного поиска объектов по всем картам
        
        :param _hmap: идентификатор открытых данных (документа) acceess - признак отбора объектов: ``0`` - отключить отбор всех объектов всех карт (отключает все локализации и чистит списки) ``1`` - все объекты доступны при поиске с помощью mapTotalSeekObject Альтернатива перебору условий поиска для всех карт (перед применением mapSetTotalSeekSample доступ может быть отключен)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetTotalSeekAccess_t (_hmap, _access)

    mapTotalPaintSelectEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapTotalPaintSelectEx', maptype.HMAP, maptype.HDC, ctypes.POINTER(maptype.RECT), maptype.COLORREF, maptype.HPAINT)
    def mapTotalPaintSelectEx(_hmap: maptype.HMAP, _hdc: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT), _color: maptype.COLORREF, _hpaint: maptype.HPAINT) -> int:
        """
        Выделить на карте объекты, соответствующие условиям обобщенного поиска объектов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hdc: идентификатор контекста устройства отображения
        
        :param _rect: координаты прямоугольной области отображения (в пикселах)
        
        :param _color: цвет, которым будут выделяться объекты на карте
        
        :param _hpaint: идентификатор контекста отображения для многопоточного вызова функции отображения
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapTotalPaintSelectEx_t (_hmap, _hdc, _rect, _color, _hpaint)

    mapTotalViewSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapTotalViewSelect', maptype.HMAP, maptype.HWND, ctypes.POINTER(maptype.DOUBLEPOINT), maptype.COLORREF, ctypes.c_long)
    def mapTotalViewSelect(_hmap: maptype.HMAP, _hwnd: maptype.HWND, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _color: maptype.COLORREF, _place: int) -> int:
        """
        Выделить на карте объекты, соответствующие условиям обобщенного поиска объектов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hwnd: идентификатор окна вывода
        
        :param _color: цвет, которым будут выделяться объекты на карте,
        
        :param _point: координаты верхнего левого угла окна на карте в системе координат, заданной переменной place
        
        :param _place: система координат (``PP_PLANE``, ``PP_GEO``, ...)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapTotalViewSelect_t (_hmap, _hwnd, _point, _color, _place)

    mapIsTotalSeekSiteObjectNotEmpty_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsTotalSeekSiteObjectNotEmpty', maptype.HMAP, maptype.HSITE)
    def mapIsTotalSeekSiteObjectNotEmpty(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Проверить наличие объектов карты, соответствующих условиям обобщенного поиска объектов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Если на карте есть объекты, соответствующие условиям - возвращает ненулевое значение
        :rtype: int
        """
        return mapIsTotalSeekSiteObjectNotEmpty_t (_hmap, _hsite)

    mapIsTotalSeekObjectNotEmpty_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsTotalSeekObjectNotEmpty', maptype.HMAP)
    def mapIsTotalSeekObjectNotEmpty(_hmap: maptype.HMAP) -> int:
        """
        Проверить наличие объектов карты, соответствующих условиям обобщенного поиска объектов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsTotalSeekObjectNotEmpty_t (_hmap)

    mapTotalSeekObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapTotalSeekObjectCount', maptype.HMAP)
    def mapTotalSeekObjectCount(_hmap: maptype.HMAP) -> int:
        """
        Запросить количество объектов, соответствующих условиям обобщенного поиска
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapTotalSeekObjectCount_t (_hmap)

    mapTotalSeekObjectCountEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapTotalSeekObjectCountEx', maptype.HMAP, ctypes.c_long)
    def mapTotalSeekObjectCountEx(_hmap: maptype.HMAP, _flag: int) -> int:
        """
        Запросить количество объектов, соответствующих условиям обобщенного поиска
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _flag: дополнительные условия поиска (например, ``WO_VISUALIGNORE`` - поиск без учета заданных условий отображения)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapTotalSeekObjectCountEx_t (_hmap, _flag)

    mapTotalSeekObject_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapTotalSeekObject', maptype.HMAP, maptype.HOBJ, ctypes.c_long)
    def mapTotalSeekObject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _flag: int) -> maptype.HOBJ:
        """
        Обобщенный поиск объектов по заданным условиям
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти, в котором будет размещен результат
        
        :param _flag: порядок поиска объектов (``WO_FIRST``, ``WO_NEXT``...) При поиске с флажками ``WO_NEXT``, ``WO_BACK`` параметр hobj должен указывать на результат предыдущего поиска Условия обобщенного поиска вводятся предварительно (используются функции mapGetSiteViewSelect, mapGetSiteSeekSelect()...)
        
        :returns: Если объект не найден - возвращает ноль
        :rtype: maptype.HOBJ
        """
        return mapTotalSeekObject_t (_hmap, _hobj, _flag)

    mapTotalSeekObjectEx_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapTotalSeekObjectEx', maptype.HMAP, maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapTotalSeekObjectEx(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _flag: int, _mapnumber: int, _sheetnumber: int, _objectnumber: int) -> maptype.HOBJ:
        """
        Обобщенный поиск объектов по заданным условиям
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти, в котором будет размещен результат
        
        :param _flag: порядок поиска объектов (``WO_FIRST``, ``WO_NEXT``, ``WO_BACK``, ...)
        
        :param _mapnumber: номер карты в открытых данных, от ``0`` до mapGetSiteCount(...)
        
        :param _sheetnumber: номер листа карты (с ``1``)
        
        :param _objectnumber: номер объекта (с ``1``), с которого будет продолжен поиск
        
        :returns: Если объект не найден - возвращает ноль
        :rtype: maptype.HOBJ
        
        .. note::

           Если flag = WO_NEXT, то поиск следующего продолжается с objectnumber + 1
           Если flag = WO_BACK, то поиск следующего продолжается с objectnumber - 1
           При поиске с флажками WO_NEXT, WO_BACK параметры mapnumber, sheetnumber, objectnumber должны быть заданы
        """
        return mapTotalSeekObjectEx_t (_hmap, _hobj, _flag, _mapnumber, _sheetnumber, _objectnumber)

    mapGetTotalSeekState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetTotalSeekState', maptype.HMAP)
    def mapGetTotalSeekState(_hmap: maptype.HMAP) -> int:
        """
        Запросить состояние условий поиска
        
        :param _hmap: идентификатор открытых данных (документа) При любом изменении условий поиска значение состояния увеличивается
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetTotalSeekState_t (_hmap)

    mapSetTotalSelectFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetTotalSelectFlag', maptype.HMAP, ctypes.c_long)
    def mapSetTotalSelectFlag(_hmap: maptype.HMAP, _flag: int) -> ctypes.c_void_p:
        """
        Установить признак отбора объектов карты по обобщенным условиям поиска
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _flag: признак выделения объектов по обобщенным условиям поиска: ``1`` - включить, ``0`` - отключить Перед вызовом функций mapTotalPaintSelectEx или mapTotalSeekObjectEx рекомендуется установить flag ``= 1`` Никакого действия, кроме установки значения, не производит Применяется для связи между различными модулями
        """
        return mapSetTotalSelectFlag_t (_hmap, _flag)

    mapGetTotalSelectFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetTotalSelectFlag', maptype.HMAP)
    def mapGetTotalSelectFlag(_hmap: maptype.HMAP) -> int:
        """
        Запросить признак отбора объектов карты по обобщенным условиям поиска
        
        :param _hmap: идентификатор открытых данных (документа)
        
        .. note::

           Если результат равен нулю, отбор объектов карты по обобщенным условиям поиска не выполняется
        """
        return mapGetTotalSelectFlag_t (_hmap)

    mapGetTotalSeekBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetTotalSeekBorder', maptype.HMAP, ctypes.POINTER(maptype.DFRAME))
    def mapGetTotalSeekBorder(_hmap: maptype.HMAP, _border: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Определить общие габариты объектов, соответствующих обобщенным условиям поиска
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _border: указатель на структуру для размещения координат общих габаритов объектов в метрах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetTotalSeekBorder_t (_hmap, _border)

    mapIsTotalSeekSample_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsTotalSeekSample', maptype.HMAP)
    def mapIsTotalSeekSample(_hmap: maptype.HMAP) -> int:
        """
        Проверить наличие списка объектов в контекстах обобщенных условий поиска хотя бы для одной карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: Если в контекстах условий есть объекты, соответствующие условиям - возвращает ненулевое значение
        :rtype: int
        """
        return mapIsTotalSeekSample_t (_hmap)

    mapInversionTotalSeek_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapInversionTotalSeek', maptype.HMAP)
    def mapInversionTotalSeek(_hmap: maptype.HMAP) -> int:
        """
        Инвертировать выделение объектов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapInversionTotalSeek_t (_hmap)

    mapGetSiteSeekBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteSeekBorder', maptype.HMAP, maptype.HSITE, ctypes.c_long, maptype.HSELECT, ctypes.POINTER(maptype.DFRAME), ctypes.c_long)
    def mapGetSiteSeekBorder(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _sheetnumber: int, _hselect: maptype.HSELECT, _border: ctypes.POINTER(maptype.DFRAME), _place: int) -> int:
        """
        Определить общие габариты объектов, соответствующие заданным условиям на карте
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _sheetnumber: номер листа карты (с ``1``)
        
        :param _hselect: контекст условий отбора объектов
        
        :param _border: указатель на структуру для размещения координат общих габаритов объектов в системе координат, заданной переменной place
        
        :param _place: система координат (``PP_PLANE``, ``PP_GEO``, ...)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteSeekBorder_t (_hmap, _hsite, _sheetnumber, _hselect, _border, _place)

    mapSetTotalSelectRecordName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetTotalSelectRecordName', maptype.HMAP, maptype.PWCHAR)
    def mapSetTotalSelectRecordName(_hmap: maptype.HMAP, _name: mapsyst.WTEXT) -> ctypes.c_void_p:
        """
        Установить имя текущей записи списка объектов условий отбора
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _name: условное имя текущих условий отбора, задаваемых прикладной задачей, или по имени записи списка объектов
        
        :returns: При ошибке возвращает ноль
        """
        return mapSetTotalSelectRecordName_t (_hmap, _name.buffer())

    mapGetTotalSelectRecordName_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapGetTotalSelectRecordName', maptype.HMAP)
    def mapGetTotalSelectRecordName(_hmap: maptype.HMAP) -> ctypes.POINTER(maptype.WCHAR):
        """
        Запросить имя текущей записи списка объектов условий отбора
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapGetTotalSelectRecordName_t (_hmap)

    mapCreateSelectContext_t = mapsyst.GetProcAddress(acceslib,maptype.HSELECT,'mapCreateSelectContext', maptype.HMAP)
    def mapCreateSelectContext(_hmap: maptype.HMAP) -> maptype.HSELECT:
        """
        Создать контекст условий отбора объектов карты для поиска/отображения
        
        :param _hmap: идентификатор открытых данных (документа) В состав условий отбора объектов входят : лист, слой, локализация, диапазон номеров объектов, характеристики (семантика) объекта, область расположения (метрика) объекта и другие свойства В созданном контексте доступны все объекты карты без исключений Каждый созданный контекст должен быть удален вызовом mapDeleteSelectContext, когда он больше не используется
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HSELECT
        
        .. note::

           Рекомендуется удалять контекст условий отбора объектов до закрытия карты (классификатора), с которыми он был создан
        """
        return mapCreateSelectContext_t (_hmap)

    mapCreateCopySelectContext_t = mapsyst.GetProcAddress(acceslib,maptype.HSELECT,'mapCreateCopySelectContext', maptype.HSELECT)
    def mapCreateCopySelectContext(_hselect: maptype.HSELECT) -> maptype.HSELECT:
        """
        Создать копию контекста условий отбора объектов
        
        :param _hselect: контекст условий отбора объектов Каждый созданный контекст должен быть удален, когда он больше не используется
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HSELECT
        """
        return mapCreateCopySelectContext_t (_hselect)

    mapCopySelectContext_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCopySelectContext', maptype.HSELECT, maptype.HSELECT)
    def mapCopySelectContext(_target: maptype.HSELECT, _source: maptype.HSELECT) -> int:
        """
        Копировать контекст условий отбора объектов в существующий контекст условий
        
        :param _target: контекст условий отбора, куда выполняется копирование
        
        :param _source: копируемый контекст условий отбора (источник) При копировании контекста выполняется также смена карты (классификатора) из контекста источника
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCopySelectContext_t (_target, _source)

    mapCopySelectContextEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCopySelectContextEx', maptype.HSELECT, maptype.HSELECT)
    def mapCopySelectContextEx(_target: maptype.HSELECT, _source: maptype.HSELECT) -> int:
        """
        Копировать контекст условий отбора объектов в существующий контекст условий с сохранением связи с картой исходного контекста
        
        :param _target: контекст условий отбора, куда выполняется копирование
        
        :param _source: копируемый контекст условий отбора (источник) При копировании контекста сохраняется связь с картой (с классификатором) исходного контекста
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCopySelectContextEx_t (_target, _source)

    mapGetSelectContextRscIdent_t = mapsyst.GetProcAddress(acceslib,maptype.HRSC,'mapGetSelectContextRscIdent', maptype.HSELECT)
    def mapGetSelectContextRscIdent(_hselect: maptype.HSELECT) -> maptype.HRSC:
        """
        Запросить идентификатор классификатора для условий отбора объектов
        
        :param _hselect: контекст условий отбора объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HRSC
        """
        return mapGetSelectContextRscIdent_t (_hselect)

    mapClearSelectContext_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapClearSelectContext', maptype.HSELECT)
    def mapClearSelectContext(_hselect: maptype.HSELECT) -> int:
        """
        Установить доступ ко всем видам данных контекста условий отбора объектов
        
        :param _hselect: контекст условий отбора объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapClearSelectContext_t (_hselect)

    mapClearSelectContextEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapClearSelectContextEx', maptype.HSELECT, maptype.HMAP, maptype.HSITE)
    def mapClearSelectContextEx(_hselect: maptype.HSELECT, _hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Установить доступ ко всем видам данных контекста условий отбора объектов для заданной карты
        
        :param _hselect: контекст условий отбора объектов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapClearSelectContextEx_t (_hselect, _hmap, _hsite)

    mapDeleteSelectContext_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapDeleteSelectContext', maptype.HSELECT)
    def mapDeleteSelectContext(_hselect: maptype.HSELECT) -> ctypes.c_void_p:
        """
        Удалить контекст условий отбора объектов
        
        :param _hselect: контекст условий отбора объектов
        """
        return mapDeleteSelectContext_t (_hselect)

    mapSetInversionSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetInversionSelect', maptype.HSELECT, ctypes.c_long)
    def mapSetInversionSelect(_hselect: maptype.HSELECT, _flag: int) -> int:
        """
        Установить признак инвертирования условий отбора объектов
        
        :param _hselect: контекст условий отбора объектов
        
        :param _flag: признак инвертирования: ``1`` - включен, ``0`` - отключен
        
        :returns: Возвращает установленное значение
        :rtype: int
        """
        return mapSetInversionSelect_t (_hselect, _flag)

    mapGetInversionSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetInversionSelect', maptype.HSELECT)
    def mapGetInversionSelect(_hselect: maptype.HSELECT) -> int:
        """
        Запросить признак инвертирования условий отбора объектов
        
        :param _hselect: контекст условий отбора объектов
        
        :returns: Возвращает признак инвертирования: ``1`` - включен, ``0`` - отключен
        :rtype: int
        """
        return mapGetInversionSelect_t (_hselect)

    mapSelectAndSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectAndSelect', maptype.HSELECT, maptype.HSELECT)
    def mapSelectAndSelect(_target: maptype.HSELECT, _source: maptype.HSELECT) -> int:
        """
        Установить пересечение условий отбора объектов (target = target & source)
        
        :param _target: контекст условий отбора, в который помещается результат
        
        :param _source: контекст поиска с дополнительными условиями При выполнении операции учитываются только коды объектов, локализация, номера слоев, листов и списки объектов. Семантика и измерения не обрабатываются
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectAndSelect_t (_target, _source)

    mapSelectAndSelectAppendSemantics_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectAndSelectAppendSemantics', maptype.HSELECT, maptype.HSELECT)
    def mapSelectAndSelectAppendSemantics(_target: maptype.HSELECT, _source: maptype.HSELECT) -> int:
        """
        Установить пересечение условий отбора объектов (target = target & source), с добавлением семантики
        
        :param _target: контекст условий отбора объектов, в который помещается результат
        
        :param _source: контекст условий отбора объектов с дополнительными условиями При выполнении операции учитываются только коды объектов, локализация и номер слоя Семантика из source добавляется в target
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectAndSelectAppendSemantics_t (_target, _source)

    mapSelectAndUsedSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectAndUsedSelect', maptype.HSELECT, maptype.HMAP, maptype.HSITE)
    def mapSelectAndUsedSelect(_hselect: maptype.HSELECT, _hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Установить пересечение условий отбора объектов (target = target & used) c составом объектов карты
        
        :param _hselect: контекст условий отбора объектов, в который помещается результат
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных Результат аналогичен вызову функций mapGetSiteUsedSelect и mapSelectAndUsedSelect В исходном контексте условий отбора объектов будут отключены коды объектов, локализация, номера слоев и листов, которых нет на заданной карте Семантика и измерения не обрабатываются
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectAndUsedSelect_t (_hselect, _hmap, _hsite)

    mapSelectOrSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectOrSelect', maptype.HSELECT, maptype.HSELECT)
    def mapSelectOrSelect(_target: maptype.HSELECT, _source: maptype.HSELECT) -> int:
        """
        Объединить условия отбора объектов (target = target OR source)
        
        :param _target: контекст условий отбора объектов, в который помещается результат
        
        :param _source: контекст условий отбора объектов с дополнительными условиями При выполнении операции учитываются только коды объектов, локализация, номер слоя и списки объектов Семантика и измерения не обрабатываются
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectOrSelect_t (_target, _source)

    mapIsSelectActive_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsSelectActive', maptype.HSELECT)
    def mapIsSelectActive(_hselect: maptype.HSELECT) -> int:
        """
        Проверить наличие активных условий отбора объектов
        
        :param _hselect: контекст условий отбора объектов
        
        :returns: Если по условиям поиска все объекты выбираются без исключений - возвращает ноль, иначе - ненулевое значение
        :rtype: int
        """
        return mapIsSelectActive_t (_hselect)

    mapSelectLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectLayer', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSelectLayer(_hselect: maptype.HSELECT, _layer: int, _check: int) -> ctypes.c_void_p:
        """
        Установить признак доступности объектов слоя
        
        :param _hselect: контекст условий отбора объектов
        
        :param _layer: номер слоя, начинается с ``0``
        
        :param _check: признак доступности слоя: ``1`` - включен, ``0`` - отключен
        
        .. note::

           Если layer ``= -1``, то устанавливается доступ ко всем слоям
        """
        return mapSelectLayer_t (_hselect, _layer, _check)

    mapCheckLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckLayer', maptype.HSELECT, ctypes.c_long)
    def mapCheckLayer(_hselect: maptype.HSELECT, _layer: int) -> int:
        """
        Запросить признак доступности объектов слоя
        
        :param _hselect: контекст условий отбора объектов
        
        :param _layer: номер слоя, начинается с ``0``. Если layer ``= -1``, то проверяется доступ ко всем слоям
        
        :returns: Если при layer ``= -1`` возвращает ``0`` - один или более слоев недоступны, иначе - доступны все слои Возвращает признак доступности слоя: ``1`` - включен, ``0`` - отключен
        :rtype: int
        """
        return mapCheckLayer_t (_hselect, _layer)

    mapSelectClass_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectClass', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSelectClass(_hselect: maptype.HSELECT, _layer: int, _check: int) -> ctypes.c_void_p:
        """
        Установить признак доступности объектов расширенного слоя (класса) из дерева слоев
        
        :param _hselect: контекст условий отбора объектов
        
        :param _layer: номер расширенного слоя (класса) из дерева слоев, начинается с ``256``
        
        :param _check: признак доступности слоя: ``1`` - включен, ``0`` - отключен
        
        .. note::

           Если layer ``= -1``, то устанавливается доступ ко всем слоям
        """
        return mapSelectClass_t (_hselect, _layer, _check)

    mapCheckClass_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckClass', maptype.HSELECT, ctypes.c_long)
    def mapCheckClass(_hselect: maptype.HSELECT, _layer: int) -> int:
        """
        Запросить признак доступности объектов расширенного слоя (класса) из дерева слоев
        
        :param _hselect: контекст условий отбора объектов
        
        :param _layer: номер расширенного слоя (класса) из дерева слоев, начинается с ``256``
        
        :returns: Если при layer ``= -1`` возвращает ``0`` - один или более слоев недоступны, иначе - доступны все слои Возвращает признак доступности слоя: ``1`` - включен, ``0`` - отключен
        :rtype: int
        """
        return mapCheckClass_t (_hselect, _layer)

    mapSelectList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectList', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSelectList(_hselect: maptype.HSELECT, _sheetnumber: int, _check: int) -> ctypes.c_void_p:
        """
        Установить признак доступности объектов листа карты
        
        :param _hselect: контекст условий отбора объектов
        
        :param _sheetnumber: номер листа карты (с ``1``). Если равен -``1``, то устанавливается доступ ко всем листам
        
        :param _check: признак доступности листа: ``1`` - включен, ``0`` - отключен
        """
        return mapSelectList_t (_hselect, _sheetnumber, _check)

    mapCheckList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckList', maptype.HSELECT, ctypes.c_long)
    def mapCheckList(_hselect: maptype.HSELECT, _sheetnumber: int) -> int:
        """
        Запросить признак доступности объектов листа карты
        
        :param _hselect: контекст условий отбора объектов
        
        :param _sheetnumber: номер листа карты (с ``1``). Если равен -``1``, то проверяется доступ ко всем листам
        
        :returns: Если при sheetnumber ``= -1`` возвращает ``0`` - один или более листов недоступны, иначе - доступны все листы Возвращает признак доступности листа: ``1`` - включен, ``0`` - отключен
        :rtype: int
        """
        return mapCheckList_t (_hselect, _sheetnumber)

    mapSelectMapObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectMapObject', maptype.HSELECT, maptype.HOBJ)
    def mapSelectMapObject(_hselect: maptype.HSELECT, _hobj: maptype.HOBJ) -> ctypes.c_void_p:
        """
        Включить доступ к объектам c листом, слоем, локализацией и кодом, как у переданного объекта
        
        :param _hselect: контекст условий отбора объектов
        
        :param _hobj: идентификатор существующего объекта карты
        """
        return mapSelectMapObject_t (_hselect, _hobj)

    mapSelectObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectObject', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSelectObject(_hselect: maptype.HSELECT, _code: int, _check: int) -> ctypes.c_void_p:
        """
        Установить признак доступности объектов c заданным внутренним кодом в классификаторе
        
        :param _hselect: контекст условий отбора объектов
        
        :param _code: внутренний код (порядковый номер объекта в классификаторе), от ``1`` до mapGetRscObjectCount(...)
        
        :param _check: признак доступности объекта: ``1`` - включен, ``0`` - отключен
        
        .. note::

           Если code ``= -1``, то устанавливается доступ ко всем объектам
        """
        return mapSelectObject_t (_hselect, _code, _check)

    mapSelectObjectExcode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectObjectExcode', maptype.HSELECT, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSelectObjectExcode(_hselect: maptype.HSELECT, _excode: int, _local: int, _check: int) -> ctypes.c_void_p:
        """
        Установить признак доступности объектов c заданным внешним кодом и локализацией в классификаторе
        
        :param _hselect: контекст условий отбора объектов
        
        :param _excode: внешний код объекта (объекты серии имеют общий внешний код)
        
        :param _local: код локализации объекта (``LOCAL_LINE``, ``LOCAL_SQUARE`` ...)
        
        :param _check: признак доступности объекта: ``1`` - включен, ``0`` - отключен
        
        .. note::

           Если check !``= 0``, то устанавливается доступ ко всем объектам серии (или одному коду объекта),
           путем включения внутренних кодов и локализации
           Если check =``= 0``, то отключаются только внутренние коды объектов (состояние локализации не меняется)
        """
        return mapSelectObjectExcode_t (_hselect, _excode, _local, _check)

    mapCheckObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckObject', maptype.HSELECT, ctypes.c_long)
    def mapCheckObject(_hselect: maptype.HSELECT, _code: int) -> int:
        """
        Запросить признак доступности объектов c заданным внутренним кодом в классификаторе
        
        :param _hselect: контекст условий отбора объектов
        
        :param _code: внутренний код (порядковый номер объекта в классификаторе), от ``1`` до mapGetRscObjectCount(...)
        
        :returns: Если при code ``= -1`` возвращает ``0`` - один или более объектов недоступны, иначе - доступны все объекты Возвращает признак доступности объекта: ``1`` - включен, ``0`` - отключен
        :rtype: int
        
        .. note::

           Если code ``= -1``, то проверяется доступ ко всем объектам
        """
        return mapCheckObject_t (_hselect, _code)

    mapCheckObjectEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckObjectEx', maptype.HSELECT, ctypes.c_long)
    def mapCheckObjectEx(_hselect: maptype.HSELECT, _code: int) -> int:
        """
        Запросить признак доступности объектов c заданным внутренним кодом в классификаторе с учетом локализации и слоя
        
        :param _hselect: контекст условий отбора объектов
        
        :param _code: внутренний код (порядковый номер объекта в классификаторе), от ``1`` до mapGetRscObjectCount(...)
        
        :returns: Если при code ``= -1`` возвращает ``0`` - один или более объектов недоступны, иначе - доступны все объекты Возвращает признак доступности объекта: ``1`` - включен, ``0`` - отключен
        :rtype: int
        
        .. note::

           Если code ``= -1``, то проверяется доступ ко всем объектам
        """
        return mapCheckObjectEx_t (_hselect, _code)

    mapSelectLocal_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectLocal', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSelectLocal(_hselect: maptype.HSELECT, _local: int, _check: int) -> ctypes.c_void_p:
        """
        Установить признак доступности объектов c заданной локализацией
        
        :param _hselect: контекст условий отбора объектов
        
        :param _local: код локализации объекта (``LOCAL_LINE``, ``LOCAL_SQUARE`` ...)
        
        :param _check: признак доступности локализации: ``1`` - включен, ``0`` - отключен
        
        .. note::

           Если local ``= -1``, то устанавливается доступ ко всем локализациям
        """
        return mapSelectLocal_t (_hselect, _local, _check)

    mapCheckLocal_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckLocal', maptype.HSELECT, ctypes.c_long)
    def mapCheckLocal(_hselect: maptype.HSELECT, _local: int) -> int:
        """
        Запросить признак доступности объектов с заданной локализацией
        
        :param _hselect: контекст условий отбора объектов
        
        :param _local: код локализации объекта (``LOCAL_LINE``, ``LOCAL_SQUARE`` ...)
        
        :returns: Если при local ``= -1`` возвращает ``0`` - одна или более локализаций недоступны, иначе - доступны все локализации Возвращает признак доступности локализации: ``1`` - включен, ``0`` - отключен
        :rtype: int
        
        .. note::

           Если local ``= -1``, то проверяется доступ ко всем локализациям
        """
        return mapCheckLocal_t (_hselect, _local)

    mapSelectKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectKey', maptype.HSELECT, ctypes.c_ulong, ctypes.c_ulong)
    def mapSelectKey(_hselect: maptype.HSELECT, _minkey: int, _maxkey: int) -> ctypes.c_void_p:
        """
        Включить доступ к объектам заданного диапазона уникальных номеров
        
        :param _hselect: контекст условий отбора объектов
        
        :param _minkey: минимальное значение диапазона номеров, начинается с ``0``
        
        :param _maxkey: максимальное значение диапазона номеров, начинается с minkey
        
        .. note::

           Если minkey и maxkey ``= -1``, то устанавливается доступ ко всем объектам по номерам
           Применяется для отбора объектов конкретного листа карты
        """
        return mapSelectKey_t (_hselect, _minkey, _maxkey)

    mapCheckKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckKey', maptype.HSELECT, ctypes.c_ulong)
    def mapCheckKey(_hselect: maptype.HSELECT, _key: int) -> int:
        """
        Запросить доступность объекта карты с заданным уникальным номером
        
        :param _hselect: контекст условий отбора объектов
        
        :param _key: уникальный номер объекта в листе карты
        
        :returns: Если при key ``= -1`` возвращает ``0`` - один или более объектов недоступны, иначе - доступны все объекты Возвращает признак доступности объектов по номерам: ``1`` - включен, ``0`` - отключен
        :rtype: int
        
        .. note::

           Если key ``= -1``, то проверяется доступ ко всем объектам по номерам
        """
        return mapCheckKey_t (_hselect, _key)

    mapGetMinKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_ulong,'mapGetMinKey', maptype.HSELECT)
    def mapGetMinKey(_hselect: maptype.HSELECT) -> int:
        """
        Запросить минимальный уникальный номер диапазона доступных объектов
        
        :param _hselect: контекст условий отбора объектов Может равняться ``0``, когда доступны все номера объектов
        """
        return mapGetMinKey_t (_hselect)

    mapGetMaxKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_ulong,'mapGetMaxKey', maptype.HSELECT)
    def mapGetMaxKey(_hselect: maptype.HSELECT) -> int:
        """
        Запросить максимальный уникальный номер диапазона доступных объектов
        
        :param _hselect: контекст условий отбора объектов
        """
        return mapGetMaxKey_t (_hselect)

    mapSelectGuid_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectGuid', maptype.HSELECT, ctypes.c_char_p)
    def mapSelectGuid(_hselect: maptype.HSELECT, _guid: ctypes.c_char_p) -> ctypes.c_void_p:
        """
        Установить доступ к объектам с заданным GUID
        
        :param _hselect: контекст условий отбора объектов
        
        :param _guid: строка, содержащая ``GUID`` в виде строки шестнадцатеричных цифр длиной ``36`` символов (с черточками) или ``32`` символа (без черточек)
        """
        return mapSelectGuid_t (_hselect, _guid)

    mapGetSelectGuid_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSelectGuid', maptype.HSELECT, ctypes.c_char_p, ctypes.c_int)
    def mapGetSelectGuid(_hselect: maptype.HSELECT, _guid: ctypes.c_char_p, _size: int) -> int:
        """
        Запросить условие доступа к объектам с заданным GUID
        
        :param _hselect: контекст условий отбора объектов
        
        :param _guid: адрес строки длиной не менее ``37`` байт, в которую запишется guid (с черточками)
        
        :returns: Если условие поиска не установлено, возвращает ноль и в поле guid записывается ноль
        :rtype: int
        """
        return mapGetSelectGuid_t (_hselect, _guid, _size)

    mapSelectTitlePro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectTitlePro', maptype.HSELECT, maptype.PWCHAR, ctypes.c_long)
    def mapSelectTitlePro(_hselect: maptype.HSELECT, _value: mapsyst.WTEXT, _isspecial: int) -> int:
        """
        Установить/Отменить условие отбора объектов по тексту подписи
        
        :param _hselect: контекст условий отбора объектов
        
        :param _value: значение строки для поиска (может включать служебные символы ``'*'`` и ``'?'``)
        
        :param _isspecial: признак обработки специальных символов при поиске (``'*'`` и ``'?'``): ``1`` - включен, ``0`` - отключен Символ ``%`` или ``*`` в начале строки означает поиск подстроки, которая следует за управляющим символом Символ ``%`` означает поиск подстроки строго в конце или в начале строки (если в конце стоит два символа ``%````%``) Символ ``*`` означает поиск подстроки в любом месте строки Символ ``?`` означает возможность подстановки любого символа, может применяться вместе с символом ``*`` Например: шаблон поиска ``"*ушк*"`` или ``"*ушк"`` или ``"%ушк%%"`` найдет значение ``"Пушкино"``, шаблон ``"%ушк"`` будет искать строки строго оканчивающиеся заданным шаблоном (``"ушк"``); шаблон ``"*39%"`` или ``"%39%"`` найдет строку ``"139%"``; шаблон ``"се??й"`` найдет строки - ``"серый"``, ``"седой"``
        
        :returns: При ошибке возвращает ноль, иначе - номер условия
        :rtype: int
        
        .. note::

           Если value равно нулю, то условие отбора по тексту подписи отменяется
        """
        return mapSelectTitlePro_t (_hselect, _value.buffer(), _isspecial)

    mapSelectSemanticGroupAppendUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectSemanticGroupAppendUn', maptype.HSELECT, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapSelectSemanticGroupAppendUn(_hselect: maptype.HSELECT, _condition: int, _semcode: int, _value: mapsyst.WTEXT, _node: int, _groupsemantic: int) -> int:
        """
        Добавить условие отбора объектов по семантике в список (узла)
        
        :param _hselect: контекст условий отбора объектов
        
        :param _condition: код условия для проверки значения семантики (``CMLESS``, ``CMEQUAL``, ``CMMORE`` ...)
        
        :param _semcode: код семантики, от ``1`` до mapGetRscSemanticCount(...)
        
        :param _value: значение для условия (если code = ``CMANY``, value игнорируется)
        
        :param _node: номер списка условий узла (c ``1``) в дереве условий отбора по семантике
        
        :param _groupsemantic: код групповой семантики, в которую входит семантика с кодом semcode, или ``0``
        
        :returns: При ошибке возвращает ноль, иначе - номер условия
        :rtype: int
        """
        return mapSelectSemanticGroupAppendUn_t (_hselect, _condition, _semcode, _value.buffer(), _node, _groupsemantic)

    mapSelectSemanticAppendExUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectSemanticAppendExUn', maptype.HSELECT, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapSelectSemanticAppendExUn(_hselect: maptype.HSELECT, _condition: int, _semcode: int, _value: mapsyst.WTEXT, _node: int) -> int:
        """
        Добавить условие отбора объектов по семантике в список (узла)
        
        :param _hselect: контекст условий отбора объектов
        
        :param _condition: код условия для проверки значения семантики (``CMLESS``, ``CMEQUAL``, ``CMMORE`` ...)
        
        :param _semcode: код семантики, от ``1`` до mapGetRscSemanticCount(...)
        
        :param _value: значение для условия (если code = ``CMANY``, value игнорируется)
        
        :param _node: номер списка условий узла (c ``1``) в дереве условий отбора по семантике
        
        :returns: При ошибке возвращает ноль, иначе - номер условия
        :rtype: int
        """
        return mapSelectSemanticAppendExUn_t (_hselect, _condition, _semcode, _value.buffer(), _node)

    mapSelectAppendStringArrayUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectAppendStringArrayUn', maptype.HSELECT, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSelectAppendStringArrayUn(_hselect: maptype.HSELECT, _condition: int, _semcode: int, _buffer: mapsyst.WTEXT, _size: int, _istitle: int, _node: int) -> int:
        """
        Добавить список строк из текстового файла в условия отбора объектов по семантике
        
        :param _hselect: контекст условий отбора объектов
        
        :param _condition: код условия для проверки значения семантики (``CMLESS``, ``CMEQUAL``, ``CMMORE`` ...)
        
        :param _semcode: код семантики, от ``1`` до mapGetRscSemanticCount(...)
        
        :param _buffer: буфер для размещения списка строк, разделенных символом '\\n' (при обработке строк символ '\\n' будет заменен на ноль)
        
        :param _size: размер буфера в байтах
        
        :param _istitle: признак отбора подписей по тексту: ``1`` - включен, ``0`` - отключен
        
        :param _node: номер списка условий узла (c ``1``) в дереве условий отбора по семантике
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectAppendStringArrayUn_t (_hselect, _condition, _semcode, _buffer.buffer(), _size, _istitle, _node)

    mapGetSelectStringArrayHandle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapGetSelectStringArrayHandle', maptype.HSELECT, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long), ctypes.c_long)
    def mapGetSelectStringArrayHandle(_hselect: maptype.HSELECT, _condition: ctypes.POINTER(ctypes.c_long), _semcode: ctypes.POINTER(ctypes.c_long), _istitle: ctypes.POINTER(ctypes.c_long), _node: int) -> ctypes.c_void_p:
        """
        Заполнить буфер списка строк в кодировке UTF8, установленных в контекст условий отбора объектов по семантике
        
        :param _hselect: контекст условий отбора объектов
        
        :param _condition: поле для записи кода условия для проверки значения семантики (``CMLESS``, ``CMEQUAL``, ``CMMORE`` ...)
        
        :param _semcode: поле для записи кода семантики
        
        :param _istitle: поле для записи признака отбора подписей по тексту
        
        :param _node: номер списка условий узла (c ``1``) в дереве условий отбора по семантике
        
        :returns: При ошибке возвращает ноль
        """
        return mapGetSelectStringArrayHandle_t (_hselect, _condition, _semcode, _istitle, _node)

    mapGetSelectStringArrayPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetSelectStringArrayPoint', ctypes.c_void_p, ctypes.POINTER(ctypes.c_long))
    def mapGetSelectStringArrayPoint(_record: ctypes.c_void_p, _size: ctypes.POINTER(ctypes.c_long)) -> ctypes.POINTER(ctypes.c_char):
        """
        Получить указатель на список строк в кодировке UTF8 по идентификатору буфера
        
        :param _record: идентификатор буфера списка строк
        
        :param _size: поле для записи длины записи в байтах
        
        :returns: Возвращает указатель на список строк в кодировке UTF8, разделенных символом '\\n' При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetSelectStringArrayPoint_t (_record, _size)

    mapFreeSelectStringArrayHandle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeSelectStringArrayHandle', ctypes.c_void_p)
    def mapFreeSelectStringArrayHandle(_record: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Освободить ресурсы, выделенные в mapGetSelectStringArrayHandle
        
        :param _record: идентификатор записи в памяти
        """
        return mapFreeSelectStringArrayHandle_t (_record)

    mapSelectSemanticClear_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectSemanticClear', maptype.HSELECT)
    def mapSelectSemanticClear(_hselect: maptype.HSELECT) -> ctypes.c_void_p:
        """
        Удалить все условия отбора объектов по семантике
        
        :param _hselect: контекст условий отбора объектов
        """
        return mapSelectSemanticClear_t (_hselect)

    mapSelectSemanticNodeCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectSemanticNodeCount', maptype.HSELECT)
    def mapSelectSemanticNodeCount(_hselect: maptype.HSELECT) -> int:
        """
        Запросить количество узлов в дереве с условиями отбора объектов по семантике
        
        :param _hselect: контекст условий отбора объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectSemanticNodeCount_t (_hselect)

    mapSelectSemanticCountEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectSemanticCountEx', maptype.HSELECT, ctypes.c_long)
    def mapSelectSemanticCountEx(_hselect: maptype.HSELECT, _node: int) -> int:
        """
        Запросить количество установленных условий отбора объектов по семантике в списке (узла)
        
        :param _hselect: контекст условий отбора объектов
        
        :param _node: номер списка условий узла (c ``1``) в дереве условий отбора по семантике
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectSemanticCountEx_t (_hselect, _node)

    mapSelectSemanticConditionEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectSemanticConditionEx', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSelectSemanticConditionEx(_hselect: maptype.HSELECT, _number: int, _node: int) -> int:
        """
        Запросить код условия отбора объектов для семантики по порядковому номеру в списке (узла)
        
        :param _hselect: контекст условий отбора объектов
        
        :param _number: порядковый номер семантики
        
        :param _node: номер списка условий узла (c ``1``) в дереве условий отбора по семантике
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectSemanticConditionEx_t (_hselect, _number, _node)

    mapSelectSemanticCodeEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectSemanticCodeEx', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSelectSemanticCodeEx(_hselect: maptype.HSELECT, _number: int, _node: int) -> int:
        """
        Запросить код семантики по порядковому номеру в списке (узла) условий отбора объектов
        
        :param _hselect: контекст условий отбора объектов
        
        :param _number: порядковый номер семантики
        
        :param _node: номер списка условий узла (c ``1``) в дереве условий отбора по семантике Примеры кодов семантики: ``4`` - абсолютная высота, ``9`` - название, ...
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectSemanticCodeEx_t (_hselect, _number, _node)

    mapSelectSemanticDeleteNode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectSemanticDeleteNode', maptype.HSELECT, ctypes.c_long)
    def mapSelectSemanticDeleteNode(_hselect: maptype.HSELECT, _node: int) -> int:
        """
        Удалить список условий отбора объектов по семантике (узла)
        
        :param _hselect: контекст условий отбора объектов
        
        :param _node: номер списка условий узла (c ``1``) в дереве условий отбора по семантике
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectSemanticDeleteNode_t (_hselect, _node)

    mapSelectSemanticDeleteEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectSemanticDeleteEx', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSelectSemanticDeleteEx(_hselect: maptype.HSELECT, _number: int, _node: int) -> int:
        """
        Удалить условие отбора объектов из списка (узла)
        
        :param _hselect: контекст условий отбора объектов
        
        :param _number: номер условия в списке, от ``1`` до mapSelectSemanticCountEx(...)
        
        :param _node: номер списка условий узла (c ``1``) в дереве условий отбора по семантике
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectSemanticDeleteEx_t (_hselect, _number, _node)

    mapSelectSemanticLinkEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectSemanticLinkEx', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSelectSemanticLinkEx(_hselect: maptype.HSELECT, _condition: int, _node: int) -> ctypes.c_void_p:
        """
        Установить обобщающее условие отбора объектов для списка семантик (узла)
        
        :param _hselect: контекст условий отбора объектов
        
        :param _condition: код условия: ``16`` - ``CMOR`` (выполняется хотя бы одно), ``32`` - ``CMAND`` (выполняются все)
        
        :param _node: номер списка условий узла (c ``1``) в дереве условий отбора по семантике
        """
        return mapSelectSemanticLinkEx_t (_hselect, _condition, _node)

    mapGetSelectSemanticLinkEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSelectSemanticLinkEx', maptype.HSELECT, ctypes.c_long)
    def mapGetSelectSemanticLinkEx(_hselect: maptype.HSELECT, _node: int) -> int:
        """
        Запросить обобщающее условие отбора объектов для списка семантик (узла)
        
        :param _hselect: контекст условий отбора объектов
        
        :param _node: номер списка условий узла (c ``1``) в дереве условий отбора по семантике
        
        :returns: Возвращает код условия: ``16`` - CMOR (выполняется хотя бы одно), ``32`` - CMAND (выполняются все) При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSelectSemanticLinkEx_t (_hselect, _node)

    mapSelectSemanticListLink_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectSemanticListLink', maptype.HSELECT, ctypes.c_long)
    def mapSelectSemanticListLink(_hselect: maptype.HSELECT, _condition: int) -> ctypes.c_void_p:
        """
        Установить обобщающее условие отбора объектов для списка узлов
        
        :param _hselect: контекст условий отбора объектов
        
        :param _condition: код условия: ``16`` - ``CMOR`` (выполняется хотя бы одно), ``32`` - ``CMAND`` (выполняются все)
        """
        return mapSelectSemanticListLink_t (_hselect, _condition)

    mapGetSelectSemanticListLink_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSelectSemanticListLink', maptype.HSELECT)
    def mapGetSelectSemanticListLink(_hselect: maptype.HSELECT) -> int:
        """
        Запросить обобщающее условие отбора объектов для списка узлов
        
        :param _hselect: контекст условий отбора объектов
        
        :returns: Возвращает код условия: ``16`` - CMOR (выполняется хотя бы одно), ``32`` - CMAND (выполняются все) При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSelectSemanticListLink_t (_hselect)

    mapSelectSemanticValueExUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectSemanticValueExUn', maptype.HSELECT, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long)
    def mapSelectSemanticValueExUn(_hselect: maptype.HSELECT, _number: int, _place: mapsyst.WTEXT, _size: int, _node: int) -> int:
        """
        Запросить значение семантики по порядковому номеру в списке (узла) условий отбора объектов
        
        :param _hselect: контекст условий отбора объектов
        
        :param _number: порядковый номер семантики
        
        :param _place: адрес строки для размещения результата
        
        :param _size: размер строки для размещения результата в байтах
        
        :param _node: номер списка условий узла (c ``1``) в дереве условий отбора по семантике
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectSemanticValueExUn_t (_hselect, _number, _place.buffer(), _size, _node)

    mapSelectSemanticGroupCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectSemanticGroupCount', maptype.HSELECT, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapSelectSemanticGroupCount(_hselect: maptype.HSELECT, _number: int, _node: int, _group: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить число условий по семантике в узле и код групповой семантики
        
        :param _hselect: контекст условий отбора объектов
        
        :param _number: порядковый номер семантики
        
        :param _node: номер списка условий узла (c ``1``) в дереве условий отбора по семантике grroup - поле для записи кода групповой семантики
        
        :returns: Если условия заданы по семантике, не входящей в групповую семантику, то обычно возвращается значение 1 и код групповой семантики устанавливается в ноль При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectSemanticGroupCount_t (_hselect, _number, _node, _group)

    mapSelectSemanticGroupItem_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectSemanticGroupItem', maptype.HSELECT, ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSelectSemanticGroupItem(_hselect: maptype.HSELECT, _number: int, _place: mapsyst.WTEXT, _size: int, _node: int, _item: int) -> int:
        """
        Запросить значение семантики по порядковому номеру в списке условий отбора объектов
        
        :param _hselect: контекст условий отбора объектов
        
        :param _number: порядковый номер семантики
        
        :param _place: адрес строки для размещения результата
        
        :param _size: размер строки для размещения результата в байтах
        
        :param _node: номер списка условий узла (c ``1``) в дереве условий отбора по семантике
        
        :param _item: номер семантики в узле для группы семантик или ``1``
        
        :returns: Возвращает код семантики в заданном узле с заданным последовательным номером При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectSemanticGroupItem_t (_hselect, _number, _place.buffer(), _size, _node, _item)

    mapSelectMeasureCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectMeasureCount', maptype.HSELECT)
    def mapSelectMeasureCount(_hselect: maptype.HSELECT) -> int:
        """
        Запросить количество установленных условий отбора объектов по измерениям
        
        :param _hselect: контекст условий отбора объектов Для установки условий по измерениям используются: длина, периметр, площадь, высота
        """
        return mapSelectMeasureCount_t (_hselect)

    mapSelectMeasureClear_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectMeasureClear', maptype.HSELECT)
    def mapSelectMeasureClear(_hselect: maptype.HSELECT) -> ctypes.c_void_p:
        """
        Удалить все условия отбора объектов по измерениям объектов
        
        :param _hselect: контекст условий отбора объектов
        """
        return mapSelectMeasureClear_t (_hselect)

    mapSelectMeasureAppend_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectMeasureAppend', maptype.HSELECT, ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.c_long, ctypes.c_double)
    def mapSelectMeasureAppend(_hselect: maptype.HSELECT, _measurecode: int, _condition1: int, _value1: float, _condition2: int, _value2: float) -> int:
        """
        Добавить условия отбора объектов по измерениям в список
        
        :param _hselect: контекст условий отбора объектов
        
        :param _measurecode: код измерения объекта: ``MEASURE_LENGTH``, ``MEASURE_PERIMETER``, ``MEASURE_SQUARE``, ``MEASURE_HEIGHT``
        
        :param _condition1: код первого условия для проверки значения (``CMLESS``, ``CMEQUAL``, ``CMMORE`` ...)
        
        :param _value1: значение измерения в метрах, для площади - в кв.метрах (для проверки первого условия)
        
        :param _condition2: код второго условия для проверки значения (``CMLESS``, ``CMEQUAL``, ``CMMORE`` ...)
        
        :param _value2: значение измерения в метрах, для площади - в кв.метрах (для проверки второго условия) Для задания диапазона значений condition1 должно равняться ``CMMOREEQ`` (>=) или ``CMMORE`` (>), condition2 должно равняться ``CMLESSEQ`` (<=) или ``CMLESS`` (<)
        
        :returns: При ошибке возвращает ноль, иначе - номер условия в списке
        :rtype: int
        
        .. note::

           Если condition2 ``= 0``, то значение value2 игнорируется
        """
        return mapSelectMeasureAppend_t (_hselect, _measurecode, _condition1, _value1, _condition2, _value2)

    mapIsSelectMeasureRange_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsSelectMeasureRange', maptype.HSELECT, ctypes.c_long)
    def mapIsSelectMeasureRange(_hselect: maptype.HSELECT, _number: int) -> int:
        """
        Запросить количество условий проверки значения измерения по порядковому номеру в списке
        
        :param _hselect: контекст условий отбора объектов
        
        :param _number: номер измерения
        
        :returns: Возвращает: 1 или 2 условия (для диапазона), ``0`` - при ошибке
        :rtype: int
        """
        return mapIsSelectMeasureRange_t (_hselect, _number)

    mapSelectMeasureLink_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectMeasureLink', maptype.HSELECT, ctypes.c_long)
    def mapSelectMeasureLink(_hselect: maptype.HSELECT, _condition: int) -> ctypes.c_void_p:
        """
        Установить обобщающее условие для списка условий отбора объектов по измерениям
        
        :param _hselect: контекст условий отбора объектов
        
        :param _condition: код условия: ``16`` - ``CMOR`` (выполняется хотя бы одно), ``32`` - ``CMAND`` (выполняются все)
        """
        return mapSelectMeasureLink_t (_hselect, _condition)

    mapGetSelectMeasureLink_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSelectMeasureLink', maptype.HSELECT)
    def mapGetSelectMeasureLink(_hselect: maptype.HSELECT) -> int:
        """
        Запросить обобщающее условие для списка условий отбора объектов по измерениям
        
        :param _hselect: контекст условий отбора объектов
        
        :returns: Возвращает код условия: ``16`` - CMOR (выполняется хотя бы одно), ``32`` - CMAND (выполняются все) При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSelectMeasureLink_t (_hselect)

    mapSelectMeasureCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectMeasureCode', maptype.HSELECT, ctypes.c_long)
    def mapSelectMeasureCode(_hselect: maptype.HSELECT, _number: int) -> int:
        """
        Запросить код измерения по порядковому номеру в списке условий отбора объектов
        
        :param _hselect: контекст условий отбора объектов
        
        :param _number: номер измерения
        
        :returns: Возвращает код измерения объекта: MEASURE_LENGTH, MEASURE_PERIMETER, MEASURE_SQUARE, MEASURE_HEIGHT При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectMeasureCode_t (_hselect, _number)

    mapSelectMeasureValue_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectMeasureValue', maptype.HSELECT, ctypes.c_long, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    def mapSelectMeasureValue(_hselect: maptype.HSELECT, _number: int, _value1: ctypes.POINTER(ctypes.c_double), _value2: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить значение измерения по порядковому номеру в списке условий отбора объектов
        
        :param _hselect: контекст условий отбора объектов
        
        :param _number: номер измерения
        
        :param _value1: поле для размещения значения измерения ``1``
        
        :param _value2: поле для размещения значения измерения ``2``
        
        :returns: Возвращает: 1 или 2 условия (для диапазона), ``0`` - при ошибке
        :rtype: int
        """
        return mapSelectMeasureValue_t (_hselect, _number, _value1, _value2)

    mapSelectMeasureCondition_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectMeasureCondition', maptype.HSELECT, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapSelectMeasureCondition(_hselect: maptype.HSELECT, _number: int, _condition1: ctypes.POINTER(ctypes.c_long), _condition2: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить код условия проверки измерения по порядковому номеру в списке условий отбора объектов
        
        :param _hselect: контекст условий отбора объектов
        
        :param _number: номер измерения
        
        :param _condition1: поле для размещения кода условия ``1``
        
        :param _condition2: поле для размещения кода условия ``2``
        
        :returns: Возвращает: 1 или 2 условия (для диапазона), ``0`` - при ошибке
        :rtype: int
        """
        return mapSelectMeasureCondition_t (_hselect, _number, _condition1, _condition2)

    mapSelectFormulaClear_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSelectFormulaClear', maptype.HSELECT)
    def mapSelectFormulaClear(_hselect: maptype.HSELECT) -> ctypes.c_void_p:
        """
        Удалить все условия отбора объектов по формулам
        
        :param _hselect: контекст условий отбора объектов
        """
        return mapSelectFormulaClear_t (_hselect)

    mapGetSelectGroupFormulaCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSelectGroupFormulaCount', maptype.HSELECT)
    def mapGetSelectGroupFormulaCount(_hselect: maptype.HSELECT) -> int:
        """
        Запросить количество групп формул условий отбора объектов
        
        :param _hselect: контекст условий отбора объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSelectGroupFormulaCount_t (_hselect)

    mapGetSelectFormulaCountEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSelectFormulaCountEx', maptype.HSELECT, ctypes.c_long)
    def mapGetSelectFormulaCountEx(_hselect: maptype.HSELECT, _group: int) -> int:
        """
        Запросить количество формул в списке группы условий отбора объектов
        
        :param _hselect: контекст условий отбора объектов
        
        :param _group: номер группы формул
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSelectFormulaCountEx_t (_hselect, _group)

    mapGetSelectFormulaEx_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetSelectFormulaEx', maptype.HSELECT, ctypes.c_long, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_long)
    def mapGetSelectFormulaEx(_hselect: maptype.HSELECT, _number: int, _minvalue: ctypes.POINTER(ctypes.c_double), _maxvalue: ctypes.POINTER(ctypes.c_double), _group: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить описание формулы по номеру в списке группы условий отбора объектов
        
        :param _hselect: контекст условий отбора объектов
        
        :param _number: номер формулы в списке с ``1``
        
        :param _minvalue: поле для записи нижней границы допустимого диапазона для значения формулы
        
        :param _maxvalue: поле для записи верхней границы допустимого диапазона для значения формулы
        
        :param _group: номер группы формул
        
        :returns: Возвращает адрес строки с математическим выражением над семантиками и свойствами объекта При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetSelectFormulaEx_t (_hselect, _number, _minvalue, _maxvalue, _group)

    mapAppendSelectFormulaEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAppendSelectFormulaEx', maptype.HSELECT, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_long)
    def mapAppendSelectFormulaEx(_hselect: maptype.HSELECT, _formula: ctypes.c_char_p, _minvalue: float, _maxvalue: float, _group: int) -> int:
        """
        Добавить описание формулы в список группы условий отбора объектов
        
        :param _hselect: контекст условий отбора объектов
        
        :param _formula: строка с математическим выражением над семантиками и свойствами объекта
        
        :param _minvalue: нижняя граница допустимого диапазона для значения формулы
        
        :param _maxvalue: верхняя граница допустимого диапазона для значения формулы
        
        :param _group: номер группы формул
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapAppendSelectFormulaEx_t (_hselect, _formula, _minvalue, _maxvalue, _group)

    mapDeleteSelectFormulaEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapDeleteSelectFormulaEx', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapDeleteSelectFormulaEx(_hselect: maptype.HSELECT, _number: int, _group: int) -> ctypes.c_void_p:
        """
        Удалить формулу из списка формул группы условий отбора объектов
        
        :param _hselect: контекст условий отбора объектов
        
        :param _number: номер формулы в списке с ``1``
        
        :param _group: номер группы формул
        """
        return mapDeleteSelectFormulaEx_t (_hselect, _number, _group)

    mapSetSelectFormulaLinkEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSelectFormulaLinkEx', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSetSelectFormulaLinkEx(_hselect: maptype.HSELECT, _condition: int, _group: int) -> int:
        """
        Установить обобщающее условие для списка группы условий отбора объектов по формулам
        
        :param _hselect: контекст условий отбора объектов
        
        :param _condition: код условия: ``16`` - ``CMOR`` (выполняется хотя бы одно), ``32`` - ``CMAND`` (выполняются все)
        
        :param _group: номер группы формул
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetSelectFormulaLinkEx_t (_hselect, _condition, _group)

    mapGetSelectFormulaLinkEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSelectFormulaLinkEx', maptype.HSELECT, ctypes.c_long)
    def mapGetSelectFormulaLinkEx(_hselect: maptype.HSELECT, _group: int) -> int:
        """
        Запросить обобщающее условие для списка группы условий отбора объектов по формулам
        
        :param _hselect: контекст условий отбора объектов
        
        :param _group: номер группы формул
        
        :returns: Возвращает код условия: ``16`` - CMOR (выполняется хотя бы одно), ``32`` - CMAND (выполняются все) При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSelectFormulaLinkEx_t (_hselect, _group)

    mapSetSelectFormulaGroupLink_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSelectFormulaGroupLink', maptype.HSELECT, ctypes.c_long)
    def mapSetSelectFormulaGroupLink(_hselect: maptype.HSELECT, _condition: int) -> int:
        """
        Установить обобщающее условие для групп условий отбора объектов по формулам
        
        :param _hselect: контекст условий отбора объектов
        
        :param _condition: код условия: ``16`` - ``CMOR`` (выполняется хотя бы одно), ``32`` - ``CMAND`` (выполняются все)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetSelectFormulaGroupLink_t (_hselect, _condition)

    mapGetSelectFormulaGroupLink_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSelectFormulaGroupLink', maptype.HSELECT)
    def mapGetSelectFormulaGroupLink(_hselect: maptype.HSELECT) -> int:
        """
        Запросить обобщающее условие для групп условий отбора объектов по формулам
        
        :param _hselect: контекст условий отбора объектов
        
        :returns: Возвращает код условия: ``16`` - CMOR (выполняется хотя бы одно), ``32`` - CMAND (выполняются все) При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSelectFormulaGroupLink_t (_hselect)

    mapSetSelectShowScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSelectShowScale', maptype.HSELECT, ctypes.c_long)
    def mapSetSelectShowScale(_hselect: maptype.HSELECT, _scale: int) -> int:
        """
        Установить значение знаменателя условного масштаба отображения для которого проверяются границы видимости объектов
        
        :param _hselect: контекст условий отбора объектов
        
        :param _scale: знаменатель масштаба отображения для проверки видимости объекта при поиске с флажком ``WO_VISUALSCALE``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если значение масштаба отображения не установлено, то при данном поиске проверяется текущий масштаб отображения документа
        """
        return mapSetSelectShowScale_t (_hselect, _scale)

    mapGetSelectRecordSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSelectRecordSize', maptype.HSELECT)
    def mapGetSelectRecordSize(_hselect: maptype.HSELECT) -> int:
        """
        Запросить размер записи, необходимый для сохранения условий поиска
        
        :param _hselect: контекст условий отбора объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSelectRecordSize_t (_hselect)

    mapGetSelectRecord_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSelectRecord', maptype.HSELECT, ctypes.c_char_p, ctypes.c_long)
    def mapGetSelectRecord(_hselect: maptype.HSELECT, _buffer: ctypes.c_char_p, _size: int) -> int:
        """
        Сформировать запись для сохранения условий поиска
        
        :param _hselect: контекст условий отбора объектов
        
        :param _buffer: буфер для размещения условий поиска
        
        :param _size: размер буфера в байтах
        
        :returns: При ошибке возвращает ноль, иначе - длину выходной строки в байтах
        :rtype: int
        """
        return mapGetSelectRecord_t (_hselect, _buffer, _size)

    mapGetSelectRecordHandle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapGetSelectRecordHandle', maptype.HSELECT, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapGetSelectRecordHandle(_hselect: maptype.HSELECT, _name: mapsyst.WTEXT, _realset: int, _isexcode: int, _issample: int) -> ctypes.c_void_p:
        """
        Сформировать запись для сохранения условий поиска в формате XML
        
        :param _hselect: контекст условий отбора объектов
        
        :param _name: имя модели условий поиска или ноль
        
        :param _realset: признак записи реально выбранных объектов и слоев (``1``); eсли realset ``= 0``, то формируется минимальная по размеру запись, которая содержит списки выбранных или отключенных объектов, слоев, локализаций с указанием признаков отбора (выбраны или отключены)
        
        :param _isexcode: признак записи внешних кодов объектов (``1``); если isexcode ``= 0``, то записываются ключи объектов
        
        :param _issample: признак записи списка уникальных номеров объектов в листе карты (``1``) если issample ``= 0``, записываются списки видов объектов (ключи или коды), слоев, локализаций
        
        :returns: Возвращает идентификатор записи формата XML в памяти Для получения указателя на запись применяется функция mapGetSelectRecordXMLPoint Для удаления записи в памяти применяется функция mapFreeSelectRecordXML При ошибке возвращает ноль
        """
        return mapGetSelectRecordHandle_t (_hselect, _name.buffer(), _realset, _isexcode, _issample)

    mapGetSelectRecordXMLPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetSelectRecordXMLPoint', maptype.HSELECT, ctypes.c_void_p, ctypes.POINTER(ctypes.c_long))
    def mapGetSelectRecordXMLPoint(_hselect: maptype.HSELECT, _record: ctypes.c_void_p, _size: ctypes.POINTER(ctypes.c_long)) -> ctypes.POINTER(ctypes.c_char):
        """
        Получить указатель на запись XML для сохранения условий поиска в формате XML
        
        :param _hselect: контекст условий отбора объектов
        
        :param _record: идентификатор записи формата ``XML`` в памяти
        
        :param _size: поле для получения длины записи в байтах name - имя модели (условий поиска) или ноль
        
        :returns: Возвращает указатель на запись XML в кодировке UTF8 Для удаления записи в памяти применяются функция mapFreeSelectRecordXML При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetSelectRecordXMLPoint_t (_hselect, _record, _size)

    mapFreeSelectRecordXML_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeSelectRecordXML', maptype.HSELECT, ctypes.c_void_p)
    def mapFreeSelectRecordXML(_hselect: maptype.HSELECT, _record: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Освободить ресурсы, выделенные в mapGetSelectRecordXML или mapGetSelectRecordHandle
        
        :param _hselect: контекст условий отбора объектов
        
        :param _record: идентификатор записи формата ``XML`` в памяти
        """
        return mapFreeSelectRecordXML_t (_hselect, _record)

    mapPutSelectRecordXML_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPutSelectRecordXML', maptype.HSELECT, ctypes.c_char_p, ctypes.c_long)
    def mapPutSelectRecordXML(_hselect: maptype.HSELECT, _buffer: ctypes.c_char_p, _size: int) -> int:
        """
        Заполнить условия поиска из записи XML
        
        :param _hselect: контекст условий отбора объектов
        
        :param _buffer: адрес записи
        
        :param _size: размер записи в памяти, содержащего запись (не меньше записи)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPutSelectRecordXML_t (_hselect, _buffer, _size)

    mapIsSample_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsSample', maptype.HSELECT)
    def mapIsSample(_hselect: maptype.HSELECT) -> int:
        """
        Проверить наличие списка объектов в контексте условий отбора объектов
        
        :param _hselect: контекст условий отбора объектов Список объектов содержит номер листа и номер объекта в листе
        
        :returns: Если в контексте условий есть объекты, соответствующие условиям - возвращает ненулевое значение
        :rtype: int
        """
        return mapIsSample_t (_hselect)

    mapGetSampleCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSampleCount', maptype.HSELECT, ctypes.c_long)
    def mapGetSampleCount(_hselect: maptype.HSELECT, _sheetnumber: int) -> int:
        """
        Запросить число объектов в списке для указанного листа карты
        
        :param _hselect: контекст условий отбора объектов
        
        :param _sheetnumber: номер листа карты (с ``1``)
        
        :returns: Если список объектов не установлен - возвращает ноль
        :rtype: int
        """
        return mapGetSampleCount_t (_hselect, _sheetnumber)

    mapGetSampleByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSampleByNumber', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapGetSampleByNumber(_hselect: maptype.HSELECT, _sheetnumber: int, _number: int) -> int:
        """
        Запросить уникальный номер объекта из списка для указанного листа по номеру в списке
        
        :param _hselect: контекст условий отбора объектов
        
        :param _sheetnumber: номер листа карты (с ``1``)
        
        :param _number: порядковый номер объекта в списке выбранных объектов листа
        
        :returns: Если список объектов не установлен, то возвращает ноль
        :rtype: int
        """
        return mapGetSampleByNumber_t (_hselect, _sheetnumber, _number)

    mapClearSample_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapClearSample', maptype.HSELECT)
    def mapClearSample(_hselect: maptype.HSELECT) -> ctypes.c_void_p:
        """
        Очистить список объектов в контексте условий отбора объектов
        
        :param _hselect: контекст условий отбора объектов Применяется для отбора объектов, атрибуты которых расположены во внешних базах данных
        """
        return mapClearSample_t (_hselect)

    mapSetSampleComplex_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSampleComplex', maptype.HSELECT, ctypes.c_long)
    def mapSetSampleComplex(_hselect: maptype.HSELECT, _complex: int) -> int:
        """
        Установить признак совместной обработки номеров объектов с условиями по локализации, слоям, семантике и измерениям
        
        :param _hselect: контекст условий отбора объектов
        
        :param _complex: признак совместной обработки:  ``1`` - включен, ``0`` - отключен
        
        :returns: Возвращает предыдущее значение
        :rtype: int
        """
        return mapSetSampleComplex_t (_hselect, _complex)

    mapInvertSample_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapInvertSample', maptype.HSELECT)
    def mapInvertSample(_hselect: maptype.HSELECT) -> int:
        """
        Инвертировать список отобранных объектов в контексте условий отбора объектов
        
        :param _hselect: контекст условий отбора объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapInvertSample_t (_hselect)

    mapSetSampleAllObjects_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSampleAllObjects', maptype.HSELECT, ctypes.c_long)
    def mapSetSampleAllObjects(_hselect: maptype.HSELECT, _sheetnumber: int) -> int:
        """
        Заполнить список объектов всеми номерами объектов, которые есть на листе
        
        :param _hselect: контекст условий отбора объектов
        
        :param _sheetnumber: номер листа карты (с ``1``) Связь контекста условий с картой устанавливается при создании контекста (mapCreateSiteSelectContext) или при чтении контекста с карты (mapGetSiteViewSelect, mapGetSiteSeekSelect)
        
        :returns: Возвращает число объектов, занесенных в список для листа При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetSampleAllObjects_t (_hselect, _sheetnumber)

    mapSelectSampleByObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectSampleByObject', maptype.HSELECT, ctypes.c_long)
    def mapSelectSampleByObject(_hselect: maptype.HSELECT, _code: int) -> int:
        """
        Заполнить список объектов всеми номерами объектов, которые имеют заданный внутренний код
        
        :param _hselect: контекст условий отбора объектов
        
        :param _code: внутренний код объекта (mapObjectCode) Связь контекста условий с картой устанавливается при создании контекста (mapCreateSiteSelectContext) или при чтении контекста с карты (mapGetSiteViewSelect, mapGetSiteSeekSelect)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectSampleByObject_t (_hselect, _code)

    mapUnselectSampleByObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUnselectSampleByObject', maptype.HSELECT, ctypes.c_long)
    def mapUnselectSampleByObject(_hselect: maptype.HSELECT, _code: int) -> int:
        """
        Удалить из списка объектов все номера объектов, которые имеют заданный внутренний код
        
        :param _hselect: контекст условий отбора объектов
        
        :param _code: внутренний код объекта (mapObjectCode) Связь контекста условий с картой устанавливается при создании контекста (mapCreateSiteSelectContext) или при чтении контекста с карты (mapGetSiteViewSelect, mapGetSiteSeekSelect)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUnselectSampleByObject_t (_hselect, _code)

    mapSelectSampleBySelectObjects_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectSampleBySelectObjects', maptype.HSELECT)
    def mapSelectSampleBySelectObjects(_hselect: maptype.HSELECT) -> int:
        """
        Заполнить список отобранных объектов по объектам, отобранным по локализации, слоям, семантике и измерениям
        
        :param _hselect: контекст условий отбора объектов В контексте условий отбора объектов должна быть установлена карта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectSampleBySelectObjects_t (_hselect)

    mapSelectViewSampleUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectViewSampleUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapSelectViewSampleUn(_hmap: maptype.HMAP, _sheetname: mapsyst.WTEXT, _key: int) -> int:
        """
        Установить условия отображения объекта по названию листа карты и уникальному номеру объекта
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _sheetname: название листа карты
        
        :param _key: уникальный номер объекта в листе карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectViewSampleUn_t (_hmap, _sheetname.buffer(), _key)

    mapCheckViewSample_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckViewSample', maptype.HMAP, maptype.HSITE)
    def mapCheckViewSample(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Проверить наличие списка объектов в контексте условий отображения для карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Если в контексте условий есть объекты, соответствующие условиям - возвращает ненулевое значение
        :rtype: int
        """
        return mapCheckViewSample_t (_hmap, _hsite)

    mapCheckSeekSample_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckSeekSample', maptype.HMAP, maptype.HSITE)
    def mapCheckSeekSample(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Проверить наличие списка объектов в контексте условий поиска для карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Если в контексте условий есть объекты, соответствующие условиям - возвращает ненулевое значение
        :rtype: int
        """
        return mapCheckSeekSample_t (_hmap, _hsite)

    mapSelectSeekSampleUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectSeekSampleUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapSelectSeekSampleUn(_hmap: maptype.HMAP, _sheetname: mapsyst.WTEXT, _key: int) -> int:
        """
        Установить условия поиска объекта по названию листа карты и уникальному номеру объекта
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _sheetname: название листа карты
        
        :param _key: уникальный номер объекта в листе карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectSeekSampleUn_t (_hmap, _sheetname.buffer(), _key)

    mapSelectSampleUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectSampleUn', maptype.HSELECT, maptype.PWCHAR, ctypes.c_long)
    def mapSelectSampleUn(_hselect: maptype.HSELECT, _sheetname: mapsyst.WTEXT, _key: int) -> int:
        """
        Установить доступ к объекту по названию листа карты и уникальному номеру объекта
        
        :param _hselect: контекст условий отбора объектов
        
        :param _sheetname: название листа карты
        
        :param _key: уникальный номер объекта в листе карты В контексте условий отбора объектов должна быть установлена карта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectSampleUn_t (_hselect, _sheetname.buffer(), _key)

    mapFastSelectSampleUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapFastSelectSampleUn', maptype.HSELECT, maptype.PWCHAR, ctypes.c_long)
    def mapFastSelectSampleUn(_hselect: maptype.HSELECT, _sheetname: mapsyst.WTEXT, _key: int) -> int:
        """
        Установить доступ к объекту по названию листа карты и уникальному номеру объекта
        
        :param _hselect: контекст условий отбора объектов
        
        :param _sheetname: название листа карты
        
        :param _key: уникальный номер объекта в листе карты Выполняется без проверки повторных значений номеров объектов для ускорения формирования списков В контексте условий отбора объектов должна быть установлена карта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapFastSelectSampleUn_t (_hselect, _sheetname.buffer(), _key)

    mapSelectSampleByKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectSampleByKey', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSelectSampleByKey(_hselect: maptype.HSELECT, _sheetnumber: int, _key: int) -> int:
        """
        Установить доступ к объекту по номеру листа карты и уникальному номеру объекта
        
        :param _hselect: контекст условий отбора объектов
        
        :param _sheetnumber: номер листа карты (с ``1``)
        
        :param _key: уникальный номер объекта в листе карты В контексте условий отбора объектов должна быть установлена карта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectSampleByKey_t (_hselect, _sheetnumber, _key)

    mapSelectSampleByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectSampleByNumber', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSelectSampleByNumber(_hselect: maptype.HSELECT, _sheetnumber: int, _objectnumber: int) -> int:
        """
        Установить доступ к объекту по номеру листа карты и порядковому номеру объекта
        
        :param _hselect: контекст условий отбора объектов
        
        :param _sheetnumber: номер листа карты (с ``1``)
        
        :param _objectnumber: номер объекта в листе В контексте условий отбора объектов должна быть установлена карта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectSampleByNumber_t (_hselect, _sheetnumber, _objectnumber)

    mapUnselectSampleUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUnselectSampleUn', maptype.HSELECT, maptype.PWCHAR, ctypes.c_long)
    def mapUnselectSampleUn(_hselect: maptype.HSELECT, _sheetname: mapsyst.WTEXT, _key: int) -> int:
        """
        Исключить из списка объект по названию листа карты и уникальному номеру объекта
        
        :param _hselect: контекст условий отбора объектов
        
        :param _sheetname: название листа карты
        
        :param _key: уникальный номер объекта в листе карты В контексте условий отбора объектов должна быть установлена карта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUnselectSampleUn_t (_hselect, _sheetname.buffer(), _key)

    mapUnselectSampleByKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUnselectSampleByKey', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapUnselectSampleByKey(_select: maptype.HSELECT, _sheetnumber: int, _key: int) -> int:
        """
        Исключить из списка объект по номеру листа карты и уникальному номеру объекта
        
        hselect - контекст условий отбора объектов
        
        :param _sheetnumber: номер листа карты (с ``1``)
        
        :param _key: уникальный номер объекта в листе карты В контексте условий отбора объектов должна быть установлена карта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUnselectSampleByKey_t (_select, _sheetnumber, _key)

    mapUnselectSampleByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUnselectSampleByNumber', maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapUnselectSampleByNumber(_hselect: maptype.HSELECT, _sheetnumber: int, _objectnumber: int) -> int:
        """
        Исключить из списка объект по номеру листа карты и порядковому номеру объекта
        
        :param _hselect: контекст условий отбора объектов
        
        :param _sheetnumber: номер листа карты (с ``1``)
        
        :param _objectnumber: номер объекта в листе В контексте условий отбора объектов должна быть установлена карта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUnselectSampleByNumber_t (_hselect, _sheetnumber, _objectnumber)

    mapSelectDocArea_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectDocArea', maptype.HMAP, maptype.HOBJ, ctypes.c_double, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSelectDocArea(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _distance: float, _filter: int, _inside: int, _visible: int, _fastlist: int, _mapnumber: int, _subjectflag: int, _samplelistflag: int) -> int:
        """
        Установить параметры поиска объектов по области для карты с заданным номером
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти, содержащий область поиска
        
        :param _distance: расстояние поиска в метрах
        
        :param _filter: признак учета фильтра объектов (условий отбора): ``1`` - включен, ``0`` - отключен
        
        :param _inside: условия поиска объектов по области: ``0`` - по расстоянию, ``1`` - внутри области, ``2`` - целиком внутри области, ``4`` - целиком снаружи области
        
        :param _visible: признак учета видимости объектов на карте: ``1`` - включен, ``0`` - отключен
        
        :param _fastlist: признак создания быстрого списка отобранных объектов: ``1`` - включен, ``0`` - отключен
        
        :param _mapnumber: номер карты поиска. Если mapnumber ``= -1``, поиск по всем картам
        
        :param _subjectflag: признак учета подобъектов области поиска: ``1`` - включен, ``0`` - отключен
        
        :param _samplelistflag: при наличии списка объектов в контексте условий отбора выполнить операцию над объектами из этого списка (``SLF_AND``, ``SLF_OR``, ...) Создание быстрого списка ускоряет многократный запрос отобранных объектов (главному окну приложения посылается ``WM_PROGRESSBAR``) Параметры фильтра объектов для карты должны быть установлены заранее (в контексте условий отбора)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectDocArea_t (_hmap, _hobj, _distance, _filter, _inside, _visible, _fastlist, _mapnumber, _subjectflag, _samplelistflag)

    mapSelectAreaUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectAreaUn', maptype.HMAP, maptype.HOBJ, ctypes.c_double, ctypes.c_long, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapSelectAreaUn(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _distance: float, _filter: int, _inside: int, _visible: int, _sheetname: mapsyst.WTEXT, _fastlist: int) -> int:
        """
        Установить параметры поиска объектов по области для карты с заданным именем
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти, содержащий область поиска
        
        :param _distance: расстояние поиска в метрах
        
        :param _filter: признак учета фильтра объектов (условий отбора): ``1`` - включен, ``0`` - отключен
        
        :param _inside: условия поиска объектов по области: ``0`` - по расстоянию, ``1`` - внутри области, ``2`` - целиком внутри области, ``4`` - целиком снаружи области
        
        :param _visible: признак учета видимости объектов на карте: ``1`` - включен, ``0`` - отключен
        
        :param _sheetname: название листа карты
        
        :param _fastlist: признак создания быстрого списка отобранных объектов: ``1`` - включен, ``0`` - отключен Создание быстрого списка ускоряет многократный запрос отобранных объектов (главному окну приложения посылается ``WM_PROGRESSBAR``) Параметры фильтра объектов для карты должны быть установлены заранее (в контексте условий отбора)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectAreaUn_t (_hmap, _hobj, _distance, _filter, _inside, _visible, _sheetname.buffer(), _fastlist)

    mapUnselectArea_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapUnselectArea', maptype.HMAP)
    def mapUnselectArea(_hmap: maptype.HMAP) -> ctypes.c_void_p:
        """
        Сбросить параметры поиска объектов по области
        
        :param _hmap: идентификатор открытых данных (документа)
        """
        return mapUnselectArea_t (_hmap)

    mapSelectSeekAreaEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectSeekAreaEx', maptype.HSELECT, maptype.HOBJ, ctypes.c_double, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSelectSeekAreaEx(_hselect: maptype.HSELECT, _hobj: maptype.HOBJ, _distance: float, _filter: int, _inside: int, _visible: int, _fastlist: int, _subjectflag: int, _samplelistflag: int) -> int:
        """
        Установить в контексте условий отбора параметры поиска объектов по области
        
        :param _hselect: контекст условий отбора объектов
        
        :param _hobj: идентификатор объекта карты в памяти, содержащий область поиска
        
        :param _distance: расстояние поиска в метрах
        
        :param _filter: признак учета фильтра объектов (условий отбора): ``1`` - включен, ``0`` - отключен
        
        :param _inside: условия поиска объектов по области: ``0`` - по расстоянию, ``1`` - внутри области, ``2`` - целиком внутри области, ``4`` - целиком снаружи области
        
        :param _visible: признак учета видимости объектов на карте: ``1`` - включен, ``0`` - отключен
        
        :param _fastlist: признак создания быстрого списка отобранных объектов: ``1`` - включен, ``0`` - отключен
        
        :param _subjectflag: признак учета подобъектов области поиска: ``1`` - включен, ``0`` - отключен
        
        :param _samplelistflag: при наличии списка объектов в контексте условий отбора выполнить операцию над объектами из этого списка (``SLF_AND``, ``SLF_OR``, ...) Создание быстрого списка ускоряет многократный запрос отобранных объектов (главному окну приложения посылается ``WM_PROGRESSBAR``) Параметры фильтра объектов для карты должны быть установлены заранее (в контексте условий отбора)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectSeekAreaEx_t (_hselect, _hobj, _distance, _filter, _inside, _visible, _fastlist, _subjectflag, _samplelistflag)

    mapSelectSeekAreaFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSelectSeekAreaFrame', maptype.HSELECT, ctypes.POINTER(maptype.DFRAME), ctypes.c_double, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSelectSeekAreaFrame(_hselect: maptype.HSELECT, _dframe: ctypes.POINTER(maptype.DFRAME), _distance: float, _filter: int, _inside: int, _visible: int, _fastlist: int) -> int:
        """
        Установить в контексте условий отбора параметры поиска объектов по прямоугольной области
        
        :param _hselect: контекст условий отбора объектов
        
        :param _dframe: габариты области поиска в метрах
        
        :param _distance: расстояние поиска в метрах (симметрично расширяет область dframe)
        
        :param _filter: признак учета фильтра объектов (условий отбора): ``1`` - включен, ``0`` - отключен
        
        :param _inside: условия поиска объектов по области: ``0`` - по расстоянию, ``1`` - внутри области, ``2`` - целиком внутри области
        
        :param _visible: признак учета видимости объектов на карте: ``1`` - включен, ``0`` - отключен
        
        :param _fastlist: признак создания быстрого списка отобранных объектов: ``1`` - включен, ``0`` - отключен Создание быстрого списка ускоряет многократный запрос отобранных объектов (главному окну приложения посылается ``WM_PROGRESSBAR``) Параметры фильтра объектов для карты должны быть установлены заранее (в контексте условий отбора)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSelectSeekAreaFrame_t (_hselect, _dframe, _distance, _filter, _inside, _visible, _fastlist)

    mapUnselectSeekArea_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapUnselectSeekArea', maptype.HSELECT)
    def mapUnselectSeekArea(_hselect: maptype.HSELECT) -> ctypes.c_void_p:
        """
        Сбросить в контексте условий отбора параметры поиска объектов по области
        
        :param _hselect: контекст условий отбора объектов
        """
        return mapUnselectSeekArea_t (_hselect)

    mapGetAreaSelectFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetAreaSelectFlag', maptype.HSELECT)
    def mapGetAreaSelectFlag(_hselect: maptype.HSELECT) -> int:
        """
        Проверить в контексте условий отбора наличие установленных параметров поиска по области
        
        :param _hselect: контекст условий отбора объектов
        
        :returns: Если в контексте условий установлены параметры поиска по области - возвращает ненулевое значение
        :rtype: int
        """
        return mapGetAreaSelectFlag_t (_hselect)

    mapGetDrawObjectsFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetDrawObjectsFlag', maptype.HSELECT)
    def mapGetDrawObjectsFlag(_hselect: maptype.HSELECT) -> int:
        """
        Запросить в контексте условий отбора признак отбора графических объектов
        
        :param _hselect: контекст условий отбора объектов
        
        :returns: Возвращает: MSL_DRAW_ON (0)   - отбор по ``"общему"`` фильтру, MSL_DRAW_ONLY (1) - отобрать только графические объекты, MSL_DRAW_OFF (2)  - не отбирать графические объекты
        :rtype: int
        """
        return mapGetDrawObjectsFlag_t (_hselect)

    mapSetDrawObjectsFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetDrawObjectsFlag', maptype.HSELECT, ctypes.c_long)
    def mapSetDrawObjectsFlag(_hselect: maptype.HSELECT, _flag: int) -> ctypes.c_void_p:
        """
        Установить в контексте условий отбора признак отбора графических объектов
        
        :param _hselect: контекст условий отбора объектов
        
        :param _flag: условия отбора графических объектов: ``MSL_DRAW_ON`` (``0``)   - отбор по ``"общему"`` фильтру, ``MSL_DRAW_ONLY`` (``1``) - отобрать только графические объекты, ``MSL_DRAW_OFF`` (``2``)  - не отбирать графические объекты
        """
        return mapSetDrawObjectsFlag_t (_hselect, _flag)

    mapGetMetaObjectsFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMetaObjectsFlag', maptype.HSELECT)
    def mapGetMetaObjectsFlag(_hselect: maptype.HSELECT) -> int:
        """
        Запросить в контексте условий отбора признак отбора метаобъектов
        
        :param _hselect: контекст условий отбора объектов
        
        :returns: Возвращает: MSL_META_OFF (0)  - исключить отбор метаобъектов MSL_META_ON (1)   - отбирать метаобъекты наряду с другими MSL_META_ONLY (2) - отбирать только метаобъекты
        :rtype: int
        """
        return mapGetMetaObjectsFlag_t (_hselect)

    mapSetMetaObjectsFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetMetaObjectsFlag', maptype.HSELECT, ctypes.c_long)
    def mapSetMetaObjectsFlag(_hselect: maptype.HSELECT, _flag: int) -> ctypes.c_void_p:
        """
        Установить в контексте условий отбора признак отбора метаобъектов
        
        :param _hselect: контекст условий отбора объектов
        
        :param _flag: условия отбора метаобъектов: ``MSL_META_OFF`` (``0``)  - исключить отбор метаобъектов ``MSL_META_ON`` (``1``)   - отбирать метаобъекты наряду с другими ``MSL_META_ONLY`` (``2``) - отбирать только метаобъекты
        """
        return mapSetMetaObjectsFlag_t (_hselect, _flag)

    mapSetLevelObjectsFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetLevelObjectsFlag', maptype.HSELECT, ctypes.c_long)
    def mapSetLevelObjectsFlag(_hselect: maptype.HSELECT, _flag: int) -> ctypes.c_void_p:
        """
        Установить в контексте условий отбора уровень доступа к объектам по значимости
        
        :param _hselect: контекст условий отбора объектов
        
        :param _flag: уровень значимости: ``0`` - все объекты, ``1`` - отобрать только основные объекты (которые отображаются в базовом масштабе карты), ``2`` - отобрать только дополнительные объекты (которые не отображаются в базовом масштабе карты)
        """
        return mapSetLevelObjectsFlag_t (_hselect, _flag)

    mapGetLevelObjectsFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetLevelObjectsFlag', maptype.HSELECT)
    def mapGetLevelObjectsFlag(_hselect: maptype.HSELECT) -> int:
        """
        Запросить в контексте условий отбора уровень доступа к объектам по значимости
        
        :param _hselect: контекст условий отбора объектов
        
        :returns: Возвращает: ``0`` - все объекты, ``1`` - отобрать только основные объекты (которые отображаются в базовом масштабе карты), ``2`` - отобрать только дополнительные объекты (которые не отображаются в базовом масштабе карты)
        :rtype: int
        """
        return mapGetLevelObjectsFlag_t (_hselect)

    mapSetSelectGroupFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetSelectGroupFlag', maptype.HSELECT, ctypes.c_long)
    def mapSetSelectGroupFlag(_hselect: maptype.HSELECT, _flag: int) -> ctypes.c_void_p:
        """
        Установить в контексте условий отбора признак отбора групп объектов при поиске по области
        
        :param _hselect: контекст условий отбора объектов
        
        :param _flag: признак отбора групп объектов при поиске по области: ``1`` - включен, ``0`` - отключен В этом случае при отборе любого объекта группы включается вся группа (аналогично мультиполигону)
        """
        return mapSetSelectGroupFlag_t (_hselect, _flag)

    mapGetSelectGroupFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSelectGroupFlag', maptype.HSELECT)
    def mapGetSelectGroupFlag(_hselect: maptype.HSELECT) -> int:
        """
        Запросить в контексте условий отбора признак отбора групп объектов при поиске по области
        
        :param _hselect: контекст условий отбора объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSelectGroupFlag_t (_hselect)

    mapGetShowClusterFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetShowClusterFlag', maptype.HSELECT)
    def mapGetShowClusterFlag(_hselect: maptype.HSELECT) -> int:
        """
        Запросить в контексте условий отбора флаг отображения кластеров
        
        :param _hselect: контекст условий отбора объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetShowClusterFlag_t (_hselect)

    mapSetShowClusterFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetShowClusterFlag', maptype.HSELECT, ctypes.c_long)
    def mapSetShowClusterFlag(_hselect: maptype.HSELECT, _flag: int) -> int:
        """
        Установить в контексте условий отбора флаг отображения кластеров
        
        :param _hselect: контекст условий отбора объектов
        
        :param _flag: признак отображения кластеров точечных объектов: ``1`` - включен, ``0`` - отключен
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetShowClusterFlag_t (_hselect, _flag)

    mapFreezeMapContents_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapFreezeMapContents', maptype.HMAP)
    def mapFreezeMapContents(_hmap: maptype.HMAP) -> int:
        """
        Зафиксировать в контексте поиска количественный состав карты
        
        :param _hmap: идентификатор открытых данных (документа) Используется при редактировании карты для исключения из поиска вновь созданных объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapFreezeMapContents_t (_hmap)

    mapDefreezeMapContents_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDefreezeMapContents', maptype.HMAP)
    def mapDefreezeMapContents(_hmap: maptype.HMAP) -> int:
        """
        Сбросить в контексте поиска данные о количественном составе карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDefreezeMapContents_t (_hmap)

    mapSeekNearPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekNearPoint', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long)
    def mapSeekNearPoint(_hobj: maptype.HOBJ, _srcpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _subject: int) -> int:
        """
        Найти номер точки на контурах объекта и подобъектов, ближайшей к заданной
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _srcpoint: координаты исходной точки (в метрах), относительно которой выполняется поиск
        
        :param _subject: номер подобъекта c ``0`` (если равен -``1`` - поиск по всей метрике)
        
        :returns: Возвращает номер точки (номер первой точки равен 1) Для определения номера найденного подобъекта при поиске по всей метрике применяется mapGetCurrentSubject() При ошибке возвращает ноль
        :rtype: int
        """
        return mapSeekNearPoint_t (_hobj, _srcpoint, _subject)

    mapSeekNearVirtualPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekNearVirtualPoint', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSeekNearVirtualPoint(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _srcpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _destpoint: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Найти координаты точки на контурах объекта и подобъектов, ближайшей к заданной
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _srcpoint: координаты исходной точки (в метрах), относительно которой выполняется поиск
        
        :param _destpoint: поле для размещения координат точки (в метрах), ближайшей к заданной
        
        :returns: Возвращает номер точки, после которой находится или c которой совпадает найденная точка Для определения номера найденного подобъекта при поиске по всей метрике применяется mapGetCurrentSubject() При ошибке возвращает ноль
        :rtype: int
        """
        return mapSeekNearVirtualPoint_t (_hmap, _hobj, _srcpoint, _destpoint)

    mapGetCurrentSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetCurrentSubject', maptype.HOBJ)
    def mapGetCurrentSubject(_hobj: maptype.HOBJ) -> int:
        """
        Запросить у объекта номер текущего подобъекта
        
        :param _hobj: идентификатор объекта в памяти Вызывать сразу после поиска точки с помощью функций mapSeekNearPoint, mapSeekNearVirtualPoint
        
        :returns: Возвращает номер подобъекта (начиная с 1) или ноль, если текущим контуром является главный контур объекта
        :rtype: int
        """
        return mapGetCurrentSubject_t (_hobj)

    mapSeekNearVirtualPointSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekNearVirtualPointSubject', maptype.HMAP, maptype.HOBJ, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSeekNearVirtualPointSubject(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _subject: int, _srcpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _destpoint: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Найти координаты точки на контуре подобъекта, ближайшей к заданной
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _subject: номер подобъекта с ``0``
        
        :param _srcpoint: координаты исходной точки (в метрах), относительно которой выполняется поиск
        
        :param _destpoint: поле для размещения координат точки (в метрах), ближайшей к заданной
        
        :returns: Возвращает номер точки, после которой находится или c которой совпадает найденная точка При ошибке возвращает ноль
        :rtype: int
        """
        return mapSeekNearVirtualPointSubject_t (_hmap, _hobj, _subject, _srcpoint, _destpoint)

    mapSeekVirtualPointByDistanceEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekVirtualPointByDistanceEx', maptype.HOBJ, ctypes.c_long, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def mapSeekVirtualPointByDistanceEx(_hobj: maptype.HOBJ, _number: int, _distance: float, _destpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _subject: int, _tail: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Найти координаты точки, лежащей на заданном расстоянии вдоль контура от заданной точки на контуре
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: номер начальной точки
        
        :param _distance: расстояние в метрах (если distance ``> 0`` - поиск по направлению цифрования, иначе - в обратном направлении)
        
        :param _destpoint: поле для размещения координат точки (в метрах), лежащей на заданном расстоянии
        
        :param _subject: номер подобъекта c ``0``
        
        :param _tail: поле для записи длины остатка (в метрах), для которого не нашлось места на контуре объекта Пример: если длина контура ``= 150``, distance ``= 100``, то tail ``= 50``
        
        :returns: Возвращает номер точки, после которой находится или c которой совпадает найденная точка Если найденная точка в точности совпадает с точкой метрики, то возвращается отрицательный номер точки Если запрошенное расстояние превышает длину объекта - возвращает ноль При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если поле tail не задано, то функция вернет ноль при превышении длины объекта
        """
        return mapSeekVirtualPointByDistanceEx_t (_hobj, _number, _distance, _destpoint, _subject, _tail)

    mapSeekVirtualPointByDistanceInMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekVirtualPointByDistanceInMap', maptype.HOBJ, ctypes.c_long, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long)
    def mapSeekVirtualPointByDistanceInMap(_hobj: maptype.HOBJ, _number: int, _distance: float, _destpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _subject: int) -> int:
        """
        Найти координаты точки, лежащей на заданном расстоянии (без учета проекции) вдоль контура от заданной точки на контуре
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _number: номер начальной точки
        
        :param _distance: расстояние в метрах (если distance ``> 0`` - поиск по направлению цифрования, иначе - в обратном направлении)
        
        :param _destpoint: поле для размещения координат точки (в метрах), лежащей на заданном расстоянии
        
        :param _subject: номер подобъекта c ``0`` Расчеты выполняются в системе координат карты без учета проекции
        
        :returns: Возвращает номер точки, после которой находится или c которой совпадает найденная точка Если найденная точка в точности совпадает с точкой метрики, то возвращается отрицательный номер точки Если запрошенное расстояние превышает длину объекта - возвращает ноль При ошибке возвращает ноль
        :rtype: int
        """
        return mapSeekVirtualPointByDistanceInMap_t (_hobj, _number, _distance, _destpoint, _subject)

    mapSeekVirtualPointByDistanceWithHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekVirtualPointByDistanceWithHeight', maptype.HMAP, maptype.HOBJ, ctypes.c_long, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long)
    def mapSeekVirtualPointByDistanceWithHeight(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _number: int, _distance: float, _destpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _subject: int) -> int:
        """
        Найти координаты точки, лежащей на заданном расстоянии (с учетом рельефа) вдоль контура от заданной точки на контуре
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: номер начальной точки
        
        :param _distance: расстояние в метрах (если distance ``> 0`` - поиск по направлению цифрования, иначе - в обратном направлении)
        
        :param _destpoint: поле для размещения координат точки (в метрах), лежащей на заданном расстоянии
        
        :param _subject: номер подобъекта c ``0``
        
        :returns: Возвращает номер точки, после которой находится или c которой совпадает найденная точка Если найденная точка в точности совпадает с точкой метрики, то возвращается отрицательный номер точки При отсутствии рельефа (матрицы высот, слоев, модели рельефа) определяет точку без учета рельефа (mapSeekVirtualPointByDistance) При ошибке возвращает ноль
        :rtype: int
        """
        return mapSeekVirtualPointByDistanceWithHeight_t (_hmap, _hobj, _number, _distance, _destpoint, _subject)

    mapSeekPointObjectByDistance_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekPointObjectByDistance', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double, ctypes.c_long)
    def mapSeekPointObjectByDistance(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _srcpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _radius: float, _visible: int) -> int:
        """
        Найти точечный объект на заданной карте вблизи заданной точки
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hobj: идентификатор объекта карты в памяти, в котором будет размещен результат
        
        :param _srcpoint: координаты исходной точки (в метрах), относительно которой выполняется поиск
        
        :param _radius: радиус области поиска в метрах (от ``1`` мкм до метров)
        
        :param _visible: признак учета видимости объектов на карте: ``1`` - включен, ``0`` - отключен
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSeekPointObjectByDistance_t (_hmap, _hsite, _hobj, _srcpoint, _radius, _visible)

    mapSeekPointObjectByDistanceAndName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekPointObjectByDistanceAndName', maptype.HMAP, maptype.HSITE, maptype.HOBJ, maptype.HOBJ, ctypes.c_double, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapSeekPointObjectByDistanceAndName(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hsrcobj: maptype.HOBJ, _hobj: maptype.HOBJ, _radius: float, _semcode: int, _value: mapsyst.WTEXT, _visible: int) -> int:
        """
        Найти точечный объект на заданной карте вблизи заданного объекта при наличии у объекта семантики с заданным кодом
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hsrcobj: идентификатор объекта, вокруг точек которого выполняется поиск
        
        :param _hobj: идентификатор объекта карты в памяти, в котором будет размещен результат
        
        :param _radius: радиус области поиска в метрах (от ``1`` мкм до метров)
        
        :param _semcode: код семантики, который должен быть у найденного объекта (если semcode ``= 0`` - семантика не учитывается)
        
        :param _value: значение семантики, которое должно быть у найденного объекта (если value ``= 0`` - значение может быть любое)
        
        :param _visible: признак учета видимости объектов на карте: ``1`` - включен, ``0`` - отключен
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSeekPointObjectByDistanceAndName_t (_hmap, _hsite, _hsrcobj, _hobj, _radius, _semcode, _value.buffer(), _visible)

    mapGetObjectsUnion_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapGetObjectsUnion', maptype.HOBJ, maptype.HOBJ, maptype.HOBJ, ctypes.c_long, ctypes.c_double)
    def mapGetObjectsUnion(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ, _hobj: maptype.HOBJ, _method: int, _delta: float) -> maptype.HOBJ:
        """
        Объединение (сшивка) двух объектов
        
        :param _hobj1: идентификатор первого объекта
        
        :param _hobj2: идентификатор второго объекта hdest - идентификатор объекта карты в памяти, в котором будет размещен результат
        
        :param _method: метод сшивки (тип результирующего объекта): ``LOCAL_SQUARE`` - площадной (на входе только два площадных или линейных замкнутых объекта), ``LOCAL_LINE`` - линейный (на входе два линейных незамкнутых объекта)
        
        :param _delta: допуск при дотягивании (в метрах) или ``0``. Если delta ``= 0``,
        
        :returns: При успешном выполнении возвращает значение hobj, иначе - 0
        :rtype: maptype.HOBJ
        
        .. note::

           то для карт масштаба <``= 500000`` устанавливается значение ``0.001``, иначе - ``0.01``
           Только для ПЛОЩАДНЫХ или ЛИНЕЙНЫХ объектов
           Не допускается сшивать замкнутый и незамкнутый объекты
        """
        return mapGetObjectsUnion_t (_hobj1, _hobj2, _hobj, _method, _delta)

    mapSquareObjectsUnion_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapSquareObjectsUnion', maptype.HOBJ, maptype.HOBJ, maptype.HOBJ, ctypes.c_double, ctypes.c_long)
    def mapSquareObjectsUnion(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ, _hdest: maptype.HOBJ, _delta: float, _flag: int) -> maptype.HOBJ:
        """
        Объединение (сшивка) двух площадных объектов
        
        :param _hobj1: идентификатор первого объекта
        
        :param _hobj2: идентификатор второго объекта
        
        :param _hdest: идентификатор объекта карты в памяти, в котором будет размещен результат
        
        :param _delta: допуск при дотягивании (в метрах)
        
        :param _flag: флаг обработки: ``0`` - сшить с предварительной проверкой на пересечение; ``1`` - добавить точки пересечения (требуется дополниетльное время на проверку) и сшить; ``2`` - сшить непересекающиеся объекты, расположенные на расстоянии до delta (без предварительной проверки) При превышении допуска между объектами сшивка выполняется через три ближайших точки (точка одного объекта, отрезок - другого)
        
        :returns: При успешном выполнении возвращает значение hobj, иначе - 0
        :rtype: maptype.HOBJ
        
        .. note::

           Если вторая пара ближайших точек ближе delta, то сшивка выполняется по всем точкам, попавшим в допуск delta
        """
        return mapSquareObjectsUnion_t (_hobj1, _hobj2, _hdest, _delta, _flag)

    mapCreateObjectsConsent_t = mapsyst.GetProcAddress(acceslib,maptype.HCROSSCONS,'mapCreateObjectsConsent', maptype.HOBJ, maptype.HOBJ, ctypes.c_long, ctypes.c_double)
    def mapCreateObjectsConsent(_htemp: maptype.HOBJ, _hobj: maptype.HOBJ, _method: int, _delta: float) -> maptype.HCROSSCONS:
        """
        Создать процесс согласования двух объектов
        
        :param _htemp: идентификатор существующего объекта-шаблона (замкнутый контур без подобъектов), по которому согласовывают внешний контур второго объекта
        
        :param _hobj: идентификатор объекта карты (линейный или площадной объект с подобъектами), у которого нужно найти внешнюю часть, примыкающую к контуру шаблона
        
        :param _method: тип результирующих объектов: ``LOCAL_SQUARE`` - площадной, ``LOCAL_LINE`` - линейный
        
        :param _delta: допуск при дотягивании (в метрах) или ``0``. Если delta ``= 0``,
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HCROSSCONS
        
        .. note::

           то для карт масштаба <``= 500000`` устанавливается значение ``0.001``, иначе - ``0.01``
           Тип результирующих объектов зависит от типа второго объекта:
           - если второй объект незамкнутый, то тип только LOCAL_LINE;
           - если второй объект замкнутый, то тип может быть LOCAL_LINE или LOCAL_SQUARE
           Только для ПЛОЩАДНЫХ или ЛИНЕЙНЫХ объектов
           По окончании обработки необходимо вызвать mapFreeObjectsConsent
        """
        return mapCreateObjectsConsent_t (_htemp, _hobj, _method, _delta)

    mapFreeObjectsConsent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeObjectsConsent', maptype.HCROSSCONS)
    def mapFreeObjectsConsent(_hcross: maptype.HCROSSCONS) -> ctypes.c_void_p:
        """
        Освободить ресурсы, выделенные в mapCreateObjectsConsent
        
        :param _hcross: идентификатор процесса согласования
        """
        return mapFreeObjectsConsent_t (_hcross)

    mapGetNextConsent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetNextConsent', maptype.HCROSSCONS, maptype.HOBJ)
    def mapGetNextConsent(_hcross: maptype.HCROSSCONS, _hobj: maptype.HOBJ) -> int:
        """
        Запросить общую часть контура
        
        :param _hcross: идентификатор процесса согласования
        
        :param _hobj: идентификатор объекта карты в памяти, в котором будет размещен результат
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetNextConsent_t (_hcross, _hobj)

    mapAdjustObjects_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAdjustObjects', maptype.HOBJ, maptype.HOBJ, ctypes.c_double, ctypes.POINTER(ctypes.c_long))
    def mapAdjustObjects(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ, _precision: float, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Согласовать метрику объектов, имеющих одну систему координат
        
        :param _hobj1: идентификатор первого объекта
        
        :param _hobj2: идентификатор второго объекта
        
        :param _precision: точность согласования (в метрах)
        
        :param _error: поле для размещения кода ошибки: ``OVL_ERR_NONE``, ... ``OVL_ERR_END`` (crossapi.h)
        
        :returns: Возвращает: ``0`` - объекты не могут быть согласованы ``1`` - изменена метрика объекта 1 ``2`` - изменена метрика объекта 2 ``3`` - изменена метрика объектов 1 и 2
        :rtype: int
        """
        return mapAdjustObjects_t (_hobj1, _hobj2, _precision, _error)

    mapCompareMetrics_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCompareMetrics', maptype.HOBJ, ctypes.c_long, maptype.HOBJ, ctypes.c_long, ctypes.c_double, ctypes.c_long)
    def mapCompareMetrics(_hobj1: maptype.HOBJ, _subject1: int, _hobj2: maptype.HOBJ, _subject2: int, _delta: float, _mode: int) -> int:
        """
        Проверить совпадение контуров по отрезкам
        
        :param _hobj1: идентификатор первого объекта
        
        :param _hobj2: идентификатор второго объекта
        
        :param _subject1: подобъект объекта hobj1. Если subject1 ``= -1``, то проверяются все подобъекты
        
        :param _subject2: подобъект объекта hobj2. Если subject2 ``= -1``, то проверяются все подобъекты
        
        :param _delta: допуск для сравнения координат точек на совпадение (в метрах)
        
        :param _mode: режим обработки двух площадных объектов: ``1`` - определение числа пар совпадающих внешних контуров, ``2`` - определение числа пар совпадающих внутренних контуров, ``3`` - определение числа пар совпадающих внешних и внутренних контуров, ``0`` - определение наличия хотя бы одной пары совпадающих любых контуров, -``1`` - определение наличия хотя бы одной пары совпадающих внешних контуров, -``2`` - определение наличия хотя бы одной пары совпадающих внутренних контуров, -``3`` - определение наличия хотя бы одной пары совпадающих внешних и внутренних контуров Анализ контуров площадных объектов может выполняться с учетом признаков внешних и внутренних контуров Каждая пара контуров, все отрезки которых совпадают, считаются совпадающими (независимо от направления цифрования, положения начальных точек и последовательности контуров)
        
        :returns: Возвращает число пар совпадающих контуров При ошибке возвращает ноль
        :rtype: int
        """
        return mapCompareMetrics_t (_hobj1, _subject1, _hobj2, _subject2, _delta, _mode)

    mapCompareObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCompareObject', maptype.HOBJ, maptype.HOBJ, ctypes.c_double)
    def mapCompareObject(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ, _delta: float) -> int:
        """
        Проверить точки объектов на совпадение в заданном допуске
        
        :param _hobj1: идентификатор первого объекта
        
        :param _hobj2: идентификатор второго объекта
        
        :param _delta: допуск для сравнения координат точек на совпадение (в метрах)
        
        :returns: Если число точек объектов совпадает и координаты отличаются в пределах заданного допуска, то возвращается ненулевое значения При ошибке возвращает ноль
        :rtype: int
        """
        return mapCompareObject_t (_hobj1, _hobj2, _delta)

    mapCreateObjectCrossPointsEx_t = mapsyst.GetProcAddress(acceslib,maptype.HCROSSPOINTS,'mapCreateObjectCrossPointsEx', maptype.HOBJ, maptype.HOBJ, ctypes.c_double)
    def mapCreateObjectCrossPointsEx(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ, _delta: float) -> maptype.HCROSSPOINTS:
        """
        Создать процесс поиска точек пересечения двух объектов
        
        :param _hobj1: идентификатор первого объекта (линейный или площадной с подобъектами)
        
        :param _hobj2: идентификатор второго объекта (линейный или площадной с подобъектами)
        
        :param _delta: допуск при дотягивании (в метрах) или ``0``. Если delta ``= 0``,
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HCROSSPOINTS
        
        .. note::

           то для карт масштаба <``= 500000`` устанавливается значение ``0.001``, иначе - ``0.01``
           По окончании обработки необходимо вызвать mapFreeCrossPoints
        """
        return mapCreateObjectCrossPointsEx_t (_hobj1, _hobj2, _delta)

    mapCreateSubjectCrossPointsEx_t = mapsyst.GetProcAddress(acceslib,maptype.HCROSSPOINTS,'mapCreateSubjectCrossPointsEx', maptype.HOBJ, maptype.HOBJ, ctypes.c_long, ctypes.c_long, ctypes.c_double)
    def mapCreateSubjectCrossPointsEx(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ, _subject1: int, _subject2: int, _delta: float) -> maptype.HCROSSPOINTS:
        """
        Создать процесс поиска точек пересечения двух объектов или подобъектов
        
        :param _hobj1: идентификатор первого объекта
        
        :param _hobj2: идентификатор второго объекта
        
        :param _subject1: номер подобъекта hobj1
        
        :param _subject2: номер подобъекта hobj2
        
        :param _delta: допуск при дотягивании (в метрах) или ``0``. Если delta ``= 0``,
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HCROSSPOINTS
        
        .. note::

           то для карт масштаба <``= 500000`` устанавливается значение ``0.001``, иначе - ``0.01``
           По окончании обработки необходимо вызвать mapFreeCrossPoints
        """
        return mapCreateSubjectCrossPointsEx_t (_hobj1, _hobj2, _subject1, _subject2, _delta)

    mapGetCrossCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetCrossCount', maptype.HCROSSPOINTS)
    def mapGetCrossCount(_hcross: maptype.HCROSSPOINTS) -> int:
        """
        Запросить количество точек пересечения
        
        :param _hcross: идентификатор процесса поиска точек пересечения
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetCrossCount_t (_hcross)

    mapGetCrossPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetCrossPoint', maptype.HCROSSPOINTS, ctypes.c_long, ctypes.POINTER(maptype.CROSSPOINT))
    def mapGetCrossPoint(_hcross: maptype.HCROSSPOINTS, _number: int, _point: ctypes.POINTER(maptype.CROSSPOINT)) -> int:
        """
        Запросить описание точки пересечения
        
        :param _hcross: идентификатор процесса поиска точек пересечения
        
        :param _number: номер точки (с ``1``)
        
        :param _point: указатель на структуру для размещения результата запроса
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetCrossPoint_t (_hcross, _number, _point)

    mapFreeCrossPoints_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeCrossPoints', maptype.HCROSSPOINTS)
    def mapFreeCrossPoints(_hcross: maptype.HCROSSPOINTS) -> ctypes.c_void_p:
        """
        Освободить ресурсы, выделенные в mapCreateObjectCrossPointsEx
        
        :param _hcross: идентификатор процесса поиска точек пересечения
        """
        return mapFreeCrossPoints_t (_hcross)

    mapInsertPointCross_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapInsertPointCross', maptype.HOBJ, maptype.HOBJ)
    def mapInsertPointCross(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ) -> int:
        """
        Добавить точки пересечения объектов в метрику
        
        :param _hobj1: идентификатор первого объекта
        
        :param _hobj2: идентификатор второго объекта
        
        :returns: При вставке точек пересечения возвращает ненулевое значение При ошибке возвращает ноль
        :rtype: int
        """
        return mapInsertPointCross_t (_hobj1, _hobj2)

    mapCreateIntersectionPointsEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateIntersectionPointsEx', maptype.HMAP, ctypes.c_double, ctypes.c_long)
    def mapCreateIntersectionPointsEx(_hmap: maptype.HMAP, _precision: float, _actioncode: int) -> int:
        """
        Создать точки пересечений выделенных объектов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _precision: точность анализа близости точек (в метрах) или ``0``
        
        :param _actioncode: код транзакции для формирования записи в журнале транзакций (``MED_SEEKCROSS`` или ``0``) Обрабатываются попарно площадные и линейные объекты внутри своих карт с помощью функции mapTotalSeekObject
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCreateIntersectionPointsEx_t (_hmap, _precision, _actioncode)

    mapOpenCheckInsideBaseObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapOpenCheckInsideBaseObject', maptype.HOBJ)
    def mapOpenCheckInsideBaseObject(_hbase: maptype.HOBJ) -> ctypes.c_void_p:
        """
        Создать процесс анализа пересечений базового объекта с остальными
        
        :param _hbase: идентификатор базового объекта По окончании обработки необходимо вызвать mapCloseCheckInsideBaseObject
        
        :returns: При ошибке возвращает 0
        """
        return mapOpenCheckInsideBaseObject_t (_hbase)

    mapCheckInsideBaseObjectEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckInsideBaseObjectEx', ctypes.c_void_p, maptype.HOBJ, ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), ctypes.POINTER(ctypes.c_int))
    def mapCheckInsideBaseObjectEx(_hcheck: ctypes.c_void_p, _htest: maptype.HOBJ, _list: ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), _count: ctypes.POINTER(ctypes.c_int)) -> int:
        """
        Определить взаиморасположение двух объектов с учетом подобъектов
        
        :param _hcheck: идентификатор просесса анализа пересечений, содержащего объект hbase hobj - идентификатор проверяемого объекта на пересечение
        
        :param _list: поле для размещения указателя на отсортированный список номеров подобъектов, с которыми пересекаются габариты шаблона
        
        :param _count: поле для размещения количества номеров в списке list
        
        :returns: Возвращает: ``1`` - объект hbase внутри hobj всеми внешними контурами ``2`` - объект hobj внутри hbase всеми внешними контурами ``3`` - объекты пересекаются, ``4`` - объекты не пересекаются ``5`` - внешние контуры объекта hbase внутри и снаружи второго hobj ``6`` - внешние контуры объекта hobj внутри и снаружи hbase ``7`` - внешние контуры объекта hobj совпадают с подобъектами hbase ``8`` - касание, объект hobj внутри hbase ``9`` - касание, объект hobj снаружи hbase ``10`` - касание, объект hbase внутри hobj При ошибке возвращает ноль
        :rtype: int
        """
        return mapCheckInsideBaseObjectEx_t (_hcheck, _htest, _list, _count)

    mapUpdateInsideBaseObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapUpdateInsideBaseObject', ctypes.c_void_p)
    def mapUpdateInsideBaseObject(_hcheck: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Обновить описание первого объекта после редактирования
        
        :param _hcheck: идентификатор процесса анализа пересечений
        """
        return mapUpdateInsideBaseObject_t (_hcheck)

    mapCloseCheckInsideBaseObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseCheckInsideBaseObject', ctypes.c_void_p)
    def mapCloseCheckInsideBaseObject(_hcheck: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Освободить ресурсы, выделенные в mapOpenCheckInsideBaseObject
        
        :param _hcheck: идентификатор процесса анализа пересечений
        """
        return mapCloseCheckInsideBaseObject_t (_hcheck)

    mapCheckOverlap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckOverlap', maptype.HOBJ, maptype.HOBJ, ctypes.c_double)
    def mapCheckOverlap(_hbase: maptype.HOBJ, _hobj: maptype.HOBJ, _precision: float) -> int:
        """
        Определить взаиморасположение области и объекта
        
        :param _hbase: идентификатор базового объекта (обязательно замкнута)
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _precision: точность анализа близости точек (в метрах)
        
        :returns: Возвращает: ``1`` - область внутри замкнутого объекта ``2`` - объект внутри области ``3`` - область и объект пересекаются, ``4`` - область и объект не пересекаются ``5`` - объект касается области и лежит внутри нее ``6`` - объект касается области и лежит снаружи При ошибке возвращает ноль
        :rtype: int
        """
        return mapCheckOverlap_t (_hbase, _hobj, _precision)

    mapGetObjectsCross_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetObjectsCross', maptype.HOBJ, maptype.HOBJ)
    def mapGetObjectsCross(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ) -> int:
        """
        Проверить наличие пересечения двух объектов
        
        :param _hobj1: идентификатор первого объекта
        
        :param _hobj2: идентификатор второго объекта Только для ПЛОЩАДНЫХ или ЛИНЕЙНЫХ объектов
        
        :returns: Если объекты пересекаются - возвращает ненулевое значение При ошибке или неверном типе объектов возвращает ноль
        :rtype: int
        """
        return mapGetObjectsCross_t (_hobj1, _hobj2)

    mapCheckCrossObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckCrossObject', maptype.HOBJ, maptype.HOBJ)
    def mapCheckCrossObject(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ) -> int:
        """
        Определить пересечение контуров (точек метрики) двух объектов с учетом подобъектов
        
        :param _hobj1: идентификатор первого объекта
        
        :param _hobj2: идентификатор второго объекта
        
        :returns: При наличии пересечений контуров возвращает ненулевое значение При ошибке возвращает 0
        :rtype: int
        """
        return mapCheckCrossObject_t (_hobj1, _hobj2)

    mapCheckCrossSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckCrossSubject', maptype.HOBJ, ctypes.c_long, maptype.HOBJ, ctypes.c_long, ctypes.c_double)
    def mapCheckCrossSubject(_hobj1: maptype.HOBJ, _subject1: int, _hobj2: maptype.HOBJ, _subject2: int, _precision: float) -> int:
        """
        Определить пересечение контуров (подобъектов) двух объектов
        
        :param _hobj1: идентификатор первого объекта
        
        :param _hobj2: идентификатор второго объекта (может быть равен hobj1)
        
        :param _subject1: номер подобъекта hobj1
        
        :param _subject2: номер подобъекта hobj2
        
        :param _precision: точность анализа близости точек и контуров (в метрах)
        
        :returns: При наличии пересечений контуров возвращает ненулевое значение Если hobj1 = hobj2 и subject1 = subject2, то возвращает 1 При ошибке возвращает 0
        :rtype: int
        """
        return mapCheckCrossSubject_t (_hobj1, _subject1, _hobj2, _subject2, _precision)

    mapCheckCrossExclusiveObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckCrossExclusiveObject', maptype.HOBJ, maptype.HOBJ, ctypes.c_double)
    def mapCheckCrossExclusiveObject(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ, _precision: float) -> int:
        """
        Определить пересечение замкнутого контура объектом
        
        :param _hobj1: идентификатор первого объекта (замкнутый контур)
        
        :param _hobj2: идентификатор второго объекта (произвольный объект с подобъектами)
        
        :param _precision: точность анализа близости точек и контуров (в метрах)
        
        :returns: Возвращает ненулевое значение, если в результате пересечения объект hobj2 разбивается на части При ошибке возвращает 0
        :rtype: int
        """
        return mapCheckCrossExclusiveObject_t (_hobj1, _hobj2, _precision)

    mapCheckInsideObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckInsideObject', maptype.HOBJ, maptype.HOBJ)
    def mapCheckInsideObject(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ) -> int:
        """
        Определить взаиморасположение двух объектов без учета подобъектов
        
        :param _hobj1: идентификатор первого объекта
        
        :param _hobj2: идентификатор второго объекта
        
        :returns: Возвращает: ``1`` - первый объект внутри второго, ``2`` - второй объект внутри первого, ``3`` - объекты пересекаются, ``4`` - объекты не пересекаются Значение 3 возвращается всегда при наличии пересечения главных контуров (0) Значения 1 и ``2`` - только для замкнутых объектов При ошибке возвращает ноль
        :rtype: int
        """
        return mapCheckInsideObject_t (_hobj1, _hobj2)

    mapCheckInsideSubjectEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckInsideSubjectEx', maptype.HOBJ, ctypes.c_long, maptype.HOBJ, ctypes.c_long)
    def mapCheckInsideSubjectEx(_hobj1: maptype.HOBJ, _subject1: int, _hobj2: maptype.HOBJ, _subject2: int) -> int:
        """
        Определить взаиморасположение двух контуров
        
        :param _hobj1: идентификатор первого объекта
        
        :param _hobj2: идентификатор второго объекта
        
        :param _subject1: номер подобъекта hobj1
        
        :param _subject2: номер подобъекта hobj2
        
        :returns: Возвращает: ``1`` - первый контур внутри второго, ``2`` - второй контур внутри первого, ``3`` - контуры пересекаются, ``4`` - контуры не пересекаются Значение 3 возвращается всегда при наличии пересечения контуров Значения 1 и ``2`` - только для замкнутых контуров При ошибке возвращает ноль
        :rtype: int
        """
        return mapCheckInsideSubjectEx_t (_hobj1, _subject1, _hobj2, _subject2)

    mapCheckInsideFirstObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckInsideFirstObject', maptype.HOBJ, maptype.HOBJ)
    def mapCheckInsideFirstObject(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ) -> int:
        """
        Определить вхождение первого объекта во второй (включая подобъекты)
        
        :param _hobj1: идентификатор первого объекта
        
        :param _hobj2: идентификатор второго объекта
        
        :returns: Возвращает: ``1`` - первый объект внутри второго (второй объект должен быть замкнутым), ``3`` - объекты пересекаются, ``4`` - первый объект не внутри второго (возможно пересечение объектов) При ошибке возвращает ноль
        :rtype: int
        """
        return mapCheckInsideFirstObject_t (_hobj1, _hobj2)

    mapCheckInsideObjectAndSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckInsideObjectAndSubject', maptype.HOBJ, maptype.HOBJ)
    def mapCheckInsideObjectAndSubject(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ) -> int:
        """
        Определить взаиморасположение двух объектов с учетом подобъектов
        
        :param _hobj1: идентификатор первого объекта
        
        :param _hobj2: идентификатор второго объекта
        
        :returns: Возвращает: ``1`` - первый объект внутри внешнего контура второго, ``2`` - второй объект внутри внешнего контура первого, ``3`` - объекты пересекаются, ``4`` - объекты не пересекаются Значение 3 возвращается всегда при наличии пересечения любых контуров Значения 1 и ``2`` - только для замкнутых объектов Для мультиполигонов значения 1 и 2 возвращаются при выполнении условия для любой пары внешних контуров Попадание контура в подобъект внешнего контура считается внешним расположением При ошибке возвращает 0
        :rtype: int
        """
        return mapCheckInsideObjectAndSubject_t (_hobj1, _hobj2)

    mapCheckInsideObjectTotal_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckInsideObjectTotal', maptype.HOBJ, maptype.HOBJ)
    def mapCheckInsideObjectTotal(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ) -> int:
        """
        Определить взаиморасположение двух объектов с учетом подобъектов
        
        :param _hobj1: идентификатор первого объекта
        
        :param _hobj2: идентификатор второго объекта
        
        :returns: Возвращает: ``1`` - первый объект внутри второго всеми внешними контурами ``2`` - второй объект внутри первого всеми внешними контурами ``3`` - объекты пересекаются, ``4`` - объекты не пересекаются ``5`` - внешние контура первого объекта внутри и снаружи второго ``6`` - внешние контура второго объекта внутри и снаружи первого При ошибке возвращает 0
        :rtype: int
        """
        return mapCheckInsideObjectTotal_t (_hobj1, _hobj2)

    mapCheckInsideObjectPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckInsideObjectPro', maptype.HOBJ, maptype.HOBJ, ctypes.POINTER(ctypes.c_long))
    def mapCheckInsideObjectPro(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ, _subject: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Определить взаиморасположение двух объектов с учетом подобъектов
        
        :param _hobj1: идентификатор первого объекта
        
        :param _hobj2: идентификатор второго объекта
        
        :param _subject: поле для размещения номера подобъекта внешнего контура мультиполигона (код ``1`` или ``2``)
        
        :returns: Возвращает: ``1`` - первый объект внутри второго (второй объект должен быть замкнутым), ``2`` - второй объект внутри первого (первый объект должен быть замкнутым), ``3`` - объекты пересекаются, ``4`` - объекты не пересекаются, -``1`` - первый объект внутри подобъекта второго объекта (второй объект должен быть замкнутым), -``2`` - второй объект внутри подобъекта первого объекта (первый объект должен быть замкнутым) При ошибке возвращает ноль
        :rtype: int
        """
        return mapCheckInsideObjectPro_t (_hobj1, _hobj2, _subject)

    mapCheckInsideObjectPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckInsideObjectPoint', maptype.HOBJ, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapCheckInsideObjectPoint(_hobj1: maptype.HOBJ, _hobj2: maptype.HOBJ, _destpoint: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Определить взаиморасположение двух объектов (включая подобъекты)
        
        :param _hobj1: идентификатор первого объекта
        
        :param _hobj2: идентификатор второго объекта
        
        :param _destpoint: поле для размещения координат первой точки пересечения (в метрах)
        
        :returns: Возвращает: ``1`` - первый объект внутри второго (второй объект должен быть замкнутым), ``2`` - второй объект внутри первого (первый объект должен быть замкнутым), ``3`` - объекты пересекаются, ``4`` - объекты не пересекаются, ``5`` - объекты (подобъекты) имеют общие отрезки или общую точку, - ``1`` - первый объект внутри подобъекта второго объекта (второй объект должен быть замкнутым), - ``2`` - второй объект внутри подобъекта первого объекта (первый объект должен быть замкнутым) При ошибке возвращает ноль
        :rtype: int
        """
        return mapCheckInsideObjectPoint_t (_hobj1, _hobj2, _destpoint)

    mapCheckInsideSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckInsideSubject', maptype.HOBJ, ctypes.c_long, maptype.HOBJ, ctypes.c_long)
    def mapCheckInsideSubject(_hobj1: maptype.HOBJ, _subject1: int, _hobj2: maptype.HOBJ, _subject2: int) -> int:
        """
        Определить вхождение всех точек контура подобъекта в другой контур подобъекта
        
        :param _hobj1: идентификатор первого объекта
        
        :param _hobj2: идентификатор второго объекта
        
        :param _subject1: номер подобъекта объекта hobj1
        
        :param _subject2: номер подобъекта объекта hobj2
        
        :returns: Возвращает: ``1`` - все точки внутри объекта/подобъекта и на контуре, ``2`` - есть внешние точки (хотя бы одна, а может и все), ``3`` - все точки контуров совпадают, ``4`` - все точки лежат на отрезке метрики или совпадают При ошибке возвращает ноль
        :rtype: int
        """
        return mapCheckInsideSubject_t (_hobj1, _subject1, _hobj2, _subject2)

    mapCheckInsidePointEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckInsidePointEx', maptype.HOBJ, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(ctypes.c_long))
    def mapCheckInsidePointEx(_hobj: maptype.HOBJ, _subject: int, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _subjectnumber: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Определить положение точки относительно замкнутого объекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _subject: номер подобъекта с ``0``. Если равно -``1``, то проверяются все контура, учитывая
        
        :param _point: координаты точки в прямоугольной системе координат (в метрах на местности)
        
        :param _subjectnumber: поле для записи номера подобъекта, в который попадает точка (при возврате ``2``, ``3``, ``4``) или ``0``
        
        :returns: мультиполигоны. При попадании в подобъект возвращает 2 и заполняет номер Возвращает: ``1`` - точка внутри объекта (подобъекта), ``2`` - точка за пределами объекта (подобъекта), ``3`` - точка совпадает с точкой метрики, ``4`` - точка лежит на отрезке При ошибке возвращает ноль
        :rtype: int
        """
        return mapCheckInsidePointEx_t (_hobj, _subject, _point, _subjectnumber)

    mapCrossCutData_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCrossCutData', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double)
    def mapCrossCutData(_pounta1: ctypes.POINTER(maptype.DOUBLEPOINT), _pounta2: ctypes.POINTER(maptype.DOUBLEPOINT), _pountb1: ctypes.POINTER(maptype.DOUBLEPOINT), _pountb2: ctypes.POINTER(maptype.DOUBLEPOINT), _crosspoint1: ctypes.POINTER(maptype.DOUBLEPOINT), _crosspoint2: ctypes.POINTER(maptype.DOUBLEPOINT), _precision: float) -> int:
        """
        Найти пересечение двух отрезков
        
        :param _pounta1: координаты точки ``1`` отрезка A
        
        :param _pounta2: координаты точки ``2`` отрезка A
        
        :param _pountb1: координаты точки ``1`` отрезка B
        
        :param _pountb2: координаты точки ``2`` отрезка B
        
        :param _crosspoint1: поле для размещения первой точки пересечения
        
        :param _crosspoint2: поле для размещения второй точки пересечения
        
        :param _precision: точность анализа близости точек (в метрах)
        
        :returns: Возвращает: ``1`` - одна точка пересечения, ``2`` - отрезки A и B имеют общую часть или совпадают При отсутствии точки пересечения или ошибке возвращает ноль
        :rtype: int
        """
        return mapCrossCutData_t (_pounta1, _pounta2, _pountb1, _pountb2, _crosspoint1, _crosspoint2, _precision)

    mapCrossCutAndSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCrossCutAndSubject', maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.NUMBERPOINT), ctypes.POINTER(maptype.NUMBERPOINT), ctypes.c_long, ctypes.c_double)
    def mapCrossCutAndSubject(_hobj: maptype.HOBJ, _pount1: ctypes.POINTER(maptype.DOUBLEPOINT), _pount2: ctypes.POINTER(maptype.DOUBLEPOINT), _first: int, _last: int, _dest1: ctypes.POINTER(maptype.NUMBERPOINT), _dest2: ctypes.POINTER(maptype.NUMBERPOINT), _subject: int, _precision: float) -> int:
        """
        Найти пересечение отрезка и участка контура подобъекта
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _pount1: координаты первой точки отрезка
        
        :param _pount2: координаты второй точки отрезка
        
        :param _first: номер первой точки анализируемого участка
        
        :param _last: номер последней точки анализируемого участка
        
        :param _dest1: указатель на структуру для размещения описания первой точки пересечения
        
        :param _dest2: указатель на структуру для размещения описания второй точки пересечения
        
        :param _subject: номер анализируемого подобъекта
        
        :param _precision: точность анализа близости точек (в метрах)
        
        :returns: При отсутствии точек пересечения или ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если отрезок и участок контура имеют общую часть, то заполняются dest1 и dest2
        """
        return mapCrossCutAndSubject_t (_hobj, _pount1, _pount2, _first, _last, _dest1, _dest2, _subject, _precision)

    mapGetPointPosition_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetPointPosition', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double)
    def mapGetPointPosition(_point: ctypes.POINTER(maptype.DOUBLEPOINT), _pount1: ctypes.POINTER(maptype.DOUBLEPOINT), _pount2: ctypes.POINTER(maptype.DOUBLEPOINT), _precision: float) -> int:
        """
        Запросить признак положения точки относительно отрезка
        
        :param _point: координаты анализируемой точки
        
        :param _pount1: координаты первой точки отрезка
        
        :param _pount2: координаты второй точки отрезка
        
        :param _precision: точность анализа близости точек и отрезка (в метрах)
        
        :returns: Возвращает признак положения точки: PS_FIRST, PS_LEFT, ... (maptype.h) При ошибке возвращает 0
        :rtype: int
        """
        return mapGetPointPosition_t (_point, _pount1, _pount2, _precision)

    mapSeekPointNormalLine_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekPointNormalLine', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapSeekPointNormalLine(_point1: ctypes.POINTER(maptype.DOUBLEPOINT), _point2: ctypes.POINTER(maptype.DOUBLEPOINT), _dest1: ctypes.POINTER(maptype.DOUBLEPOINT), _dest2: ctypes.POINTER(maptype.DOUBLEPOINT), _distance: float, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Найти две точки перпендикуляра от отрезка на заданном расстоянии от произвольной точки
        
        pount1 - координаты первой точки отрезка
        pount2 - координаты второй точки отрезка
        
        :param _dest1: поле для размещения первой точки перпендикуляра
        
        :param _dest2: поле для размещения второй точки перпендикуляра
        
        :param _point: координаты точки, от которой производится расчет (если point ``= 0``, то point = pount1)
        
        :param _distance: растояние от точки point
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSeekPointNormalLine_t (_point1, _point2, _dest1, _dest2, _distance, _point)

    mapCutObjectListFromList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCutObjectListFromList', maptype.HMESSAGE, maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapCutObjectListFromList(_hmessage: maptype.HMESSAGE, _hmap: maptype.HMAP, _editset: int, _tempset: int, _adjust: int, _multi: int) -> int:
        """
        Выполнить вырезание контуров одного набора площадных объектов из другого набора площадных объектов
        
        :param _hmessage: идентификатор окна (для Windows - ``HWND``), которое будет извещаться (для отмены сообщений установить идентификатор в ноль)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _editset: номер набора редактируемых объектов в файле ``OBX`` карты в папке \\LOG
        
        :param _tempset: номер набора вырезаемых объектов в файле ``OBX`` карты в папке \\LOG
        
        :param _adjust: признак согласования: ``1`` - согласовать контуры вырезаемых объектов с редактируемыми объектами ``2`` - заменить внутренние контуры соответствующими контурами эталонных объектов Допустимо совместное использование признаков (``1`` | ``2``)
        
        :param _multi: признак формирования мультиполигона при делении контура редактируемого объекта на части: ``1`` - включен, ``0`` - отключен Процесс посылает сообщение ``WM_PROGRESSBARUN`` (wparm: процент обработки) Для прерывания процесса из обработчика сообщения нужно вернуть ``WM_PROGRESSBARUN``
        
        :returns: Возвращает число обработанных контуров, если ни в одном контуре не было вырезания - возвращает (-1) При ошибке возвращает ноль
        :rtype: int
        """
        return mapCutObjectListFromList_t (_hmessage, _hmap, _editset, _tempset, _adjust, _multi)

    mapSplitObjectListByList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSplitObjectListByList', maptype.HMESSAGE, maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSplitObjectListByList(_hmessage: maptype.HMESSAGE, _hmap: maptype.HMAP, _editset: int, _tempset: int, _adjust: int) -> int:
        """
        Выполнить разрезание контуров одного набора площадных объектов по контурам другого набора объектов
        
        :param _hmessage: идентификатор окна (для Windows - ``HWND``), которое будет извещаться (для отмены сообщений установить идентификатор в ноль)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _editset: номер набора редактируемых объектов в файле ``OBX`` карты в папке \\LOG
        
        :param _tempset: номер набора объектов линий разрезания в файле ``OBX`` карты в папке \\LOG
        
        :param _adjust: признак согласования контуров набора tempset с редактируемыми объектами: ``1`` - включен, ``0`` - отключен Процесс посылает сообщение ``WM_PROGRESSBARUN`` (wparm: процент обработки) Для прерывания процесса из обработчика сообщения нужно вернуть ``WM_PROGRESSBARUN``
        
        :returns: Возвращает число обработанных контуров При ошибке возвращает ноль
        :rtype: int
        """
        return mapSplitObjectListByList_t (_hmessage, _hmap, _editset, _tempset, _adjust)

    mapCutObjectPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCutObjectPro', maptype.HOBJ, maptype.HOBJ, ctypes.c_long, ctypes.c_long, maptype.HOBJSET, ctypes.c_double)
    def mapCutObjectPro(_hobj: maptype.HOBJ, _htemp: maptype.HOBJ, _inside: int, _adjust: int, _hobjset: maptype.HOBJSET, _precision: float) -> int:
        """
        Вырезать площадной или линейный объект по площадному объекту
        
        :param _hobj: редактирумый объект (полигон, мультиполигон или мультилиния)
        
        :param _htemp: идентификатор существующего объекта-шаблона для вырезания (полигон или мультиполигон)
        
        :param _inside: признак сохраняемых частей объекта: ``1`` - сохранить внутренние части, ``0`` - внешние части
        
        :param _adjust: признак согласования вырезающего объекта с редактируемым: ``1`` - включен, ``0`` - отключен
        
        :param _hobjset: список объектов, дополнительно созданных при сохранении внешних частей внутри подобъектов разрезаемого полигона (mapCreateObjectSet)
        
        :param _precision: точность согласования вырезаемых контуров (в метрах)
        
        :returns: Возвращает число внешних частей, если объект удален - возвращает (-1) При ошибке или при отсутствии обработки возвращает ноль
        :rtype: int
        """
        return mapCutObjectPro_t (_hobj, _htemp, _inside, _adjust, _hobjset, _precision)

    mapCutObjectByTemplate_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCutObjectByTemplate', maptype.HOBJ, maptype.HOBJ, ctypes.c_long, ctypes.c_long, maptype.HOVL, maptype.HOBJSET, ctypes.c_double)
    def mapCutObjectByTemplate(_editinfo: maptype.HOBJ, _tempinfo: maptype.HOBJ, _inside: int, _adjust: int, _hovl: maptype.HOVL, _hobjset: maptype.HOBJSET, _precision: float) -> int:
        """
        Вырезать площадной или линейный объект по площадному объекту
        
        :param _editinfo: редактирумый объект (полигон, мультиполигон или мультилиния)
        
        :param _tempinfo: идентификатор существующего объекта-шаблона для вырезания (полигон или мультиполигон)
        
        :param _inside: признак сохраняемых частей объекта: ``1`` - сохранить внутренние части, ``0`` - внешние части
        
        :param _adjust: признак согласования вырезающего объекта с редактируемым: ``1`` - включен, ``0`` - отключен
        
        :param _hovl: идентификатор класса оверлейных операций
        
        :param _hobjset: список объектов, дополнительно созданных при сохранении внешних частей внутри подобъектов разрезаемого полигона (mapCreateObjectSet)
        
        :param _precision: точность согласования вырезаемых контуров (в метрах)
        
        :returns: Возвращает число внешних частей, если объект удален - возвращает (-1) При ошибке или при отсутствии обработки возвращает ноль
        :rtype: int
        """
        return mapCutObjectByTemplate_t (_editinfo, _tempinfo, _inside, _adjust, _hovl, _hobjset, _precision)

    mapCutMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCutMap', maptype.HMESSAGE, maptype.HMAP, maptype.HSELECT, maptype.HOBJ, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapCutMap(_hmessage: maptype.HMESSAGE, _hmap: maptype.HMAP, _hselect: maptype.HSELECT, _templet: maptype.HOBJ, _name: mapsyst.WTEXT, _namesize: int, _inside: int, _adjust: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Вырезать карту по площадному объекту (вырезает объекты всех карт документа)
        
        :param _hmessage: идентификатор окна (для Windows - ``HWND``), которое будет извещаться или ноль Процесс посылает сообщение ``WM_PROGRESSBARUN`` (wparam - процент обработки) Для прерывания процесса из обработчика сообщения нужно вернуть ``WM_PROGRESSBARUN``
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hselect: контекст условий отбора объектов (если hselect ``= 0`` - обработать все объекты) htemp - идентификатор существующего объекта-шаблона для вырезания (полигон или мультиполигон)
        
        :param _name: адрес строки для размещения имени файла карты (sitx/sit/mpt) для записи результата,
        
        :param _namesize: размер буфера с именем проекта (в байтах)
        
        :param _inside: признак сохраняемых частей объектов: ``1`` - сохранить внутренние части, ``0`` - внешние части
        
        :param _adjust: признак согласования вырезающего объекта с редактируемыми: ``1`` - включен, ``0`` - отключен
        
        :param _error: поле для размещения кода ошибки: ``OVL_ERR_NONE``, ... ``OVL_ERR_END`` (crossapi.h)
        
        :returns: При ошибке или при отсутствии обработки возвращает ноль
        :rtype: int
        
        .. note::

           Если если name и namesize !``= 0``, то после вызова функции name содержит уточнённое имя файла проекта
           Если выходная карта содержит несколько карт, то результат сохраняется в виде проекта (mpt)
        """
        return mapCutMap_t (_hmessage, _hmap, _hselect, _templet, _name.buffer(), _namesize, _inside, _adjust, _error)

    mapOpenCrossMultiPolygon_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapOpenCrossMultiPolygon', maptype.HOBJ)
    def mapOpenCrossMultiPolygon(_hobj: maptype.HOBJ) -> ctypes.c_void_p:
        """
        Создать процесс для построения пересечения мультиполигонов или простых полигонов
        
        :param _hobj: идентификатор объекта карты в памяти, с которым будет строится пересечение другим объектом При построении пересечения данный объект не меняется По окончании обработки необходимо вызвать mapCloseCrossMultiPolygon
        
        :returns: При ошибке возвращает ноль
        """
        return mapOpenCrossMultiPolygon_t (_hobj)

    mapCloseCrossMultiPolygon_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapCloseCrossMultiPolygon', ctypes.c_void_p)
    def mapCloseCrossMultiPolygon(_hcrossmultipolygon: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Закрыть процесс построения пересечения мультиполигонов
        
        :param _hcrossmultipolygon: идентификатор процесса, полученный при вызове mapOpenCrossMultiPolygon
        """
        return mapCloseCrossMultiPolygon_t (_hcrossmultipolygon)

    mapChangeCrossMultiPolygon_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapChangeCrossMultiPolygon', ctypes.c_void_p, maptype.HOBJ)
    def mapChangeCrossMultiPolygon(_hcrossmultipolygon: ctypes.c_void_p, _hobj: maptype.HOBJ) -> int:
        """
        Заменить первый объект для построения пересечения мультиполигонов (или простых полигонов)
        
        :param _hobj: идентификатор объекта карты в памяти, с которым будет строится пересечение другим объектом
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapChangeCrossMultiPolygon_t (_hcrossmultipolygon, _hobj)

    mapBuildCrossMultiPolygonEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBuildCrossMultiPolygonEx', ctypes.c_void_p, maptype.HOBJ, ctypes.POINTER(ctypes.c_long))
    def mapBuildCrossMultiPolygonEx(_hcrossmultipolygon: ctypes.c_void_p, _hdest: maptype.HOBJ, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Построить пересечение мультиполигонов в виде мультиполигона
        
        :param _hcrossmultipolygon: идентификатор процесса, полученный при вызове mapOpenCrossMultiPolygon
        
        :param _hdest: идентификатор объекта карты в памяти, с которым будет строится пересечение
        
        :param _error: поле для размещения кода ошибки: ``OVL_ERR_NONE``, ... ``OVL_ERR_END`` (crossapi.h) Результат построения при успешном выполнении записывается в этот же объект
        
        :returns: При успешном выполнении возвращает ненулевое значение При ошибке возвращает ноль
        :rtype: int
        """
        return mapBuildCrossMultiPolygonEx_t (_hcrossmultipolygon, _hdest, _error)

    mapSetPrecision_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapSetPrecision', maptype.HOBJ, ctypes.c_double)
    def mapSetPrecision(_hobj: maptype.HOBJ, _precision: float) -> float:
        """
        Определить допуск для удаления одинаковых точек
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _precision: предлагаемый допуск для удаления одинаковых точек (в метрах) или ``0``
        
        :returns: Возвращает реальный допуск (с учетом параметров карты объекта)
        :rtype: float
        """
        return mapSetPrecision_t (_hobj, _precision)

    mapCreateObjectSet_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJSET,'mapCreateObjectSet')
    def mapCreateObjectSet() -> maptype.HOBJSET:
        """
        Создать контекст набора объектов, объединенных по групповой семантической характеристике
        
        Для связи объектов набора используется семантика GROUPLEADER, GROUPSLAVE, GROUPPARTNER
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HOBJSET
        """
        return mapCreateObjectSet_t ()

    mapFreeObjectSet_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeObjectSet', maptype.HOBJSET)
    def mapFreeObjectSet(_hobjset: maptype.HOBJSET) -> ctypes.c_void_p:
        """
        Освободить ресурсы, выделенные в mapCreateObjectSet
        
        :param _hobjset: идентификатор контекста набора объектов
        """
        return mapFreeObjectSet_t (_hobjset)

    mapBuildObjectSet_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBuildObjectSet', maptype.HOBJSET, maptype.HOBJ)
    def mapBuildObjectSet(_hobjset: maptype.HOBJSET, _hobj: maptype.HOBJ) -> int:
        """
        Создать набор объектов из объектов карты по существующей в объекте групповой семантике
        
        :param _hobjset: идентификатор контекста набора объектов
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapBuildObjectSet_t (_hobjset, _hobj)

    mapBuildObjectSetByType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBuildObjectSetByType', maptype.HOBJSET, maptype.HOBJ, ctypes.c_int)
    def mapBuildObjectSetByType(_hobjset: maptype.HOBJSET, _hobj: maptype.HOBJ, _type: int) -> int:
        """
        Создать набор объектов из объектов карты по заданному типу существующей в объекте групповой семантике
        
        :param _hobjset: идентификатор контекста набора объектов
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _type: тип семантической характеристики (``GROUPLEADER``, ``GROUPSLAVE``, ``GROUPPARTNER``) для поиска в hobj
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если type ``= 0`` - ищет первую попавшуюся групповую семантику
        """
        return mapBuildObjectSetByType_t (_hobjset, _hobj, _type)

    mapBuildObjectSetByTypeGroup_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBuildObjectSetByTypeGroup', maptype.HOBJSET, maptype.HOBJ, ctypes.c_int, ctypes.c_int)
    def mapBuildObjectSetByTypeGroup(_hobjset: maptype.HOBJSET, _hobj: maptype.HOBJ, _type: int, _group: int) -> int:
        """
        Создать набор объектов из объектов карты по заданному типу существующей в объекте групповой семантике и номеру группы
        
        :param _hobjset: идентификатор контекста набора объектов
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _type: тип семантической характеристики для поиска в hobj (``GROUPLEADER``, ``GROUPSLAVE``, ``GROUPPARTNER``)
        
        :param _group: номер группы (объект может принадлежать нескольким группам)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если type ``= 0`` - ищет первую попавшуюся групповую семантику
        """
        return mapBuildObjectSetByTypeGroup_t (_hobjset, _hobj, _type, _group)

    mapBuildSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapBuildSelect', maptype.HOBJSET, maptype.HSELECT)
    def mapBuildSelect(_hobjset: maptype.HOBJSET, _hselect: maptype.HSELECT) -> int:
        """
        Заполнить контекст поиска из объектов набора
        
        :param _hobjset: идентификатор контекста набора объектов
        
        :param _hselect: контекст условий отбора объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapBuildSelect_t (_hobjset, _hselect)

    mapObjectSetCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectSetCount', maptype.HOBJSET)
    def mapObjectSetCount(_hobjset: maptype.HOBJSET) -> int:
        """
        Запросить количество объектов в наборе
        
        :param _hobjset: идентификатор контекста набора объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapObjectSetCount_t (_hobjset)

    mapReadObjectSetObject_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapReadObjectSetObject', maptype.HOBJSET, ctypes.c_long, maptype.HOBJ)
    def mapReadObjectSetObject(_hobjset: maptype.HOBJSET, _number: int, _hobj: maptype.HOBJ) -> maptype.HOBJ:
        """
        Запросить объект из набора по номеру в наборе
        
        :param _hobjset: идентификатор контекста набора объектов
        
        :param _number: порядковый номер объекта в наборе с ``1``
        
        :param _hobj: идентификатор объекта карты в памяти, в котором будет размещен результат
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HOBJ
        """
        return mapReadObjectSetObject_t (_hobjset, _number, _hobj)

    mapObjectSetObject_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapObjectSetObject', maptype.HOBJSET, ctypes.c_long)
    def mapObjectSetObject(_hobjset: maptype.HOBJSET, _number: int) -> maptype.HOBJ:
        """
        Запросить объект из набора по номеру в наборе
        
        :param _hobjset: идентификатор контекста набора объектов
        
        :param _number: порядковый номер объекта в наборе с ``1``
        
        :returns: Возвращает идентификатор объекта карты из набора При ошибке возвращает ноль
        :rtype: maptype.HOBJ
        """
        return mapObjectSetObject_t (_hobjset, _number)

    mapObjectSetFramePlane_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectSetFramePlane', maptype.HOBJSET, ctypes.POINTER(maptype.DFRAME))
    def mapObjectSetFramePlane(_hobjset: maptype.HOBJSET, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Запросить габариты объектов набора
        
        :param _hobjset: идентификатор контекста набора объектов
        
        :param _frame: указатель на структуру для размещения прямоугольной области габаритов набора (в метрах)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapObjectSetFramePlane_t (_hobjset, _frame)

    mapObjectSetNominateLeader_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectSetNominateLeader', maptype.HOBJSET, ctypes.c_long)
    def mapObjectSetNominateLeader(_hobjset: maptype.HOBJSET, _number: int) -> int:
        """
        Назначить главный объект в наборе (добавить признак в семантику GROUPLEADER)
        
        :param _hobjset: идентификатор контекста набора объектов
        
        :param _number: порядковый номер объекта в листе (из числа объектов в наборе)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если number ``= 0``, назначается первый попавшийся объект в наборе
           В семантику объекта GROUPLEADER записывает ключ самого объекта (mapObjectKey)
        """
        return mapObjectSetNominateLeader_t (_hobjset, _number)

    mapObjectSetClearObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectSetClearObject', maptype.HOBJSET, ctypes.c_long, ctypes.c_long)
    def mapObjectSetClearObject(_hobjset: maptype.HOBJSET, _number: int, _save: int) -> int:
        """
        Удалить объект из набора по номеру в наборе
        
        :param _hobjset: идентификатор контекста набора объектов
        
        :param _number: порядковый номер объекта в наборе с ``1``
        
        :param _save: признак сохранения изменений в файл ``OBX``: ``1`` - включен, ``0`` - отключен Удаленный объект заменяется на последний из списка
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если объект главный в группе (GROUPLEADER) - удаляется вся группа
        """
        return mapObjectSetClearObject_t (_hobjset, _number, _save)

    mapObjectSetClear_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapObjectSetClear', maptype.HOBJSET, ctypes.c_long)
    def mapObjectSetClear(_hobjset: maptype.HOBJSET, _save: int) -> ctypes.c_void_p:
        """
        Удалить все объекты из набора
        
        :param _hobjset: идентификатор контекста набора объектов
        
        :param _save: признак сохранения изменений в файл ``OBX``: ``1`` - включен, ``0`` - отключен
        """
        return mapObjectSetClear_t (_hobjset, _save)

    mapObjectSetIsGroup_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectSetIsGroup', maptype.HOBJSET, maptype.HOBJ, ctypes.POINTER(ctypes.c_long))
    def mapObjectSetIsGroup(_hobjset: maptype.HOBJSET, _hobj: maptype.HOBJ, _group: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить признак группового объекта (по семантике)
        
        :param _hobjset: идентификатор контекста набора объектов
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _group: поле для размещения номера группы объекта (если он нужен) или ``0``
        
        :returns: Возвращает код групповой семантики (GROUPLEADER, GROUPSLAVE, GROUPPARTNER) или ноль
        :rtype: int
        """
        return mapObjectSetIsGroup_t (_hobjset, _hobj, _group)

    mapObjectSetGetTypeSemn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectSetGetTypeSemn', maptype.HOBJSET, maptype.HOBJ, ctypes.c_long)
    def mapObjectSetGetTypeSemn(_hobjset: maptype.HOBJSET, _hobj: maptype.HOBJ, _type: int) -> int:
        """
        Проверить наличие групповой семантики у объекта
        
        :param _hobjset: идентификатор контекста набора объектов
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _type: тип групповой семантики ``GROUPLEADER``, ``GROUPSLAVE``, ``GROUPPARTNER``
        
        :returns: Возвращает номер группы или ноль при отсутствии
        :rtype: int
        """
        return mapObjectSetGetTypeSemn_t (_hobjset, _hobj, _type)

    mapObjectSetDelete_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectSetDelete', maptype.HOBJSET)
    def mapObjectSetDelete(_hobjset: maptype.HOBJSET) -> int:
        """
        Удалить все объекты набора с карты
        
        :param _hobjset: идентификатор контекста набора объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapObjectSetDelete_t (_hobjset)

    mapObjectSetDeleteSemantic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectSetDeleteSemantic', maptype.HOBJSET, maptype.HOBJ, ctypes.c_long)
    def mapObjectSetDeleteSemantic(_hobjset: maptype.HOBJSET, _hobj: maptype.HOBJ, _group: int) -> int:
        """
        Удалить групповую семантику из объекта
        
        :param _hobjset: идентификатор контекста набора объектов
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _group: номер группы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если group ``= 0``, то используется текущий номер группы контекста набора объектов hobjset
        """
        return mapObjectSetDeleteSemantic_t (_hobjset, _hobj, _group)

    mapPaintObjectSet_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPaintObjectSet', maptype.HOBJSET, maptype.HMAP, maptype.HDC, ctypes.POINTER(maptype.RECT))
    def mapPaintObjectSet(_hobjset: maptype.HOBJSET, _hmap: maptype.HMAP, _hdc: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT)) -> int:
        """
        Отобразить набор
        
        :param _hobjset: идентификатор контекста набора объектов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hdc: идентификатор контекста устройства отображения
        
        :param _rect: координаты прямоугольной области отображения (в пикселах)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPaintObjectSet_t (_hobjset, _hmap, _hdc, _rect)

    mapObjectSetSave_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectSetSave', maptype.HOBJSET, ctypes.c_long)
    def mapObjectSetSave(_hobjset: maptype.HOBJSET, _always: int) -> int:
        """
        Сохранить набор
        
        :param _hobjset: идентификатор контекста набора объектов
        
        :param _always: признак сохранения: ``1`` - сохранять всегда, ``0`` - сохранять только, если были изменения
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapObjectSetSave_t (_hobjset, _always)

    mapObjectSetRevert_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectSetRevert', maptype.HOBJSET)
    def mapObjectSetRevert(_hobjset: maptype.HOBJSET) -> int:
        """
        Восстановить объекты группы на карте после операций удаления или перемещения
        
        :param _hobjset: идентификатор контекста набора объектов Использовать, если не вызывали mapObjectSetSave
        
        :returns: Возвращает число обработанных объектов При ошибке возвращает ноль
        :rtype: int
        """
        return mapObjectSetRevert_t (_hobjset)

    mapObjectSetRemoveNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectSetRemoveNumber', maptype.HOBJSET, ctypes.c_long, ctypes.c_long)
    def mapObjectSetRemoveNumber(_hobjset: maptype.HOBJSET, _number: int, _save: int) -> int:
        """
        Удалить объект из группы по его номеру в листе
        
        :param _hobjset: идентификатор контекста набора объектов
        
        :param _number: порядковый номер объекта в листе с ``1``
        
        :param _save: признак сохранения изменений в файл ``OBX``: ``1`` - включен, ``0`` - отключен
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapObjectSetRemoveNumber_t (_hobjset, _number, _save)

    mapObjectSetAppendGeneral_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectSetAppendGeneral', maptype.HOBJSET, maptype.HOBJ, ctypes.c_long)
    def mapObjectSetAppendGeneral(_hobjset: maptype.HOBJSET, _hobj: maptype.HOBJ, _save: int) -> int:
        """
        Добавить главный объект группу (добавить признак в семантику GROUPLEADER)
        
        :param _hobjset: идентификатор контекста набора объектов
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _save: признак сохранения изменений в файл ``OBX``: ``1`` - включен, ``0`` - отключен
        
        :returns: Возвращает порядковый номер объекта или ноль
        :rtype: int
        
        .. note::

           Если объект hobj не записан в карту (Key ``= 0``) и (save ``= 1``), то сначала объект будет сохранен, а потом добавлен в группу
           Если объект hobj содержит семантику GROUPLEADER, то объект добавляется в набор, не изменяя групповую семантику
           Если объект hobj содержит семантику GROUPSLAVE или GROUPPARTNER, то в объект добавляется семантика GROUPLEADER:
           создается новая группа, без удаления старой группы (объект может принадлежать нескольким группам)
        """
        return mapObjectSetAppendGeneral_t (_hobjset, _hobj, _save)

    mapObjectSetAppendSubordinate_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectSetAppendSubordinate', maptype.HOBJSET, maptype.HOBJ, ctypes.c_long)
    def mapObjectSetAppendSubordinate(_hobjset: maptype.HOBJSET, _hobj: maptype.HOBJ, _save: int) -> int:
        """
        Добавить подчиненный объект в группу (добавить признак в семантику GROUPSLAVE)
        
        :param _hobjset: идентификатор контекста набора объектов
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :param _save: признак сохранения изменений в файл ``OBX``: ``1`` - включен, ``0`` - отключен
        
        :returns: Возвращает порядковый номер объекта или ноль
        :rtype: int
        
        .. note::

           Если объект hobj не записан в карту (Key ``= 0``) и (save ``= 1``), то сначала объект будет сохранен, а потом добавлен в группу
           Если объект hobj содержит семантику GROUPLEADER, то в объект добавляется семантика GROUPSLAVE:
           создается новая группа, без удаления старой группы (объект может принадлежать нескольким группам)
           Если объект hobj содержит семантику GROUPSLAVE или GROUPPARTNER, то объект добавляется в набор,
           с добавлением семантики GROUPSLAVE
        """
        return mapObjectSetAppendSubordinate_t (_hobjset, _hobj, _save)

    mapObjectSetFindGeneral_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapObjectSetFindGeneral', maptype.HOBJSET, ctypes.c_long)
    def mapObjectSetFindGeneral(_hobjset: maptype.HOBJSET, _group: int) -> maptype.HOBJ:
        """
        Найти главный объект в группе
        
        :param _hobjset: идентификатор контекста набора объектов
        
        :param _group: номер группы (если group ``= 0`` - номер группы устанавливается из набора hobjset)
        
        :returns: Возвращает идентификатор объекта карты из набора При ошибке возвращает ноль
        :rtype: maptype.HOBJ
        """
        return mapObjectSetFindGeneral_t (_hobjset, _group)

    mapObjectSetUnion_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapObjectSetUnion', maptype.HOBJSET, maptype.HOBJSET, ctypes.c_long, maptype.HOBJ, ctypes.c_long)
    def mapObjectSetUnion(_hdestset: maptype.HOBJSET, _hobjset: maptype.HOBJSET, _mode: int, _hobj: maptype.HOBJ, _save: int) -> int:
        """
        Объединить два набора объектов
        
        :param _hdestset: идентификатор контекста набора объектов, в который добавляется набор hobjset
        
        :param _hobjset: идентификатор добавляемого контекста набора объектов
        
        :param _mode: режим добавления: ``1`` - добавить отдельный объект (если объект главный - создать иерархию, включив только его в набор hdestset, если объект подчиненный или равноправный - включить его в текущий набор, удалив из hobjset), ``2`` - набор hobjset и все объекты включаются в набор hdestset, набор hobjset удаляется, ``3`` - найти главный объект набора hobjset и включить его как подчиненный в набор hdestset, создав иерархию
        
        :param _hobj: идентификатор объекта карты в памяти, которой определяет способ обработки Результат помещается в набор hdestset
        
        :param _save: признак сохранения изменений в файл ``OBX``: ``1`` - включен, ``0`` - отключен
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapObjectSetUnion_t (_hdestset, _hobjset, _mode, _hobj, _save)

    mapCalcCharacteristic_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCalcCharacteristic', maptype.HMAP, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def mapCalcCharacteristic(_hmap: maptype.HMAP, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _semcode: int, _value: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Вычисление значения характеристики в заданной точке по данным векторной карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _point: координаты точки (в метрах)
        
        :param _semcode: код семантической характеристики
        
        :param _value: поле для размещения результата запроса Поиск характеристики выполняется по всем объектам векторной карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCalcCharacteristic_t (_hmap, _point, _semcode, _value)

    mapOpenModelFileUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapOpenModelFileUn', maptype.PWCHAR, ctypes.c_long)
    def mapOpenModelFileUn(_name: mapsyst.WTEXT, _mode: int) -> ctypes.c_void_p:
        """
        Открыть процесс чтения/записи макетов условий отбора
        
        :param _name: имя открываемого файла макетов (``VCL``)
        
        :param _mode: режим чтения/записи: ``GENERIC_READ``, ``GENERIC_WRITE`` или ``0`` ``GENERIC_READ`` - все данные только на чтение По окончании обработки необходимо вызвать mapModelFree
        
        :returns: При ошибке возвращает ноль
        """
        return mapOpenModelFileUn_t (_name.buffer(), _mode)

    mapModelCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapModelCount', ctypes.c_void_p)
    def mapModelCount(_hvcl: ctypes.c_void_p) -> int:
        """
        Запросить количество моделей в файле макетов условий отбора
        
        :param _hvcl: идентификатор процесса чтения/записи макетов условий отбора
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapModelCount_t (_hvcl)

    mapAddModelUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAddModelUn', ctypes.c_void_p, maptype.HSELECT, maptype.PWCHAR)
    def mapAddModelUn(_hvcl: ctypes.c_void_p, _hselect: maptype.HSELECT, _name: mapsyst.WTEXT) -> int:
        """
        Добавить модель в конец файла макетов условий отбора
        
        :param _hvcl: идентификатор процесса чтения/записи макетов условий отбора
        
        :param _hselect: контекст условий отбора объектов, который сохраняется в файл моделей
        
        :param _name: имя модели
        
        :returns: Возвращает номер записи в файле или 0 при ошибке
        :rtype: int
        """
        return mapAddModelUn_t (_hvcl, _hselect, _name.buffer())

    mapDeleteModelByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteModelByNumber', ctypes.c_void_p, ctypes.c_long)
    def mapDeleteModelByNumber(_hvcl: ctypes.c_void_p, _number: int) -> int:
        """
        Удалить модель c заданным номером
        
        :param _hvcl: идентификатор процесса чтения/записи макетов условий отбора
        
        :param _number: номер модели в файле макетов условий отбора
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteModelByNumber_t (_hvcl, _number)

    mapDeleteModelByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteModelByNameUn', ctypes.c_void_p, maptype.PWCHAR)
    def mapDeleteModelByNameUn(_hvcl: ctypes.c_void_p, _name: mapsyst.WTEXT) -> int:
        """
        Удалить модель c заданным именем
        
        :param _name: имя модели
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteModelByNameUn_t (_hvcl, _name.buffer())

    mapModelNumberUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapModelNumberUn', ctypes.c_void_p, maptype.PWCHAR)
    def mapModelNumberUn(_hvcl: ctypes.c_void_p, _name: mapsyst.WTEXT) -> int:
        """
        Запросить номер модели по имени модели
        
        :param _hvcl: идентификатор процесса чтения/записи макетов условий отбора
        
        :param _name: имя модели
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapModelNumberUn_t (_hvcl, _name.buffer())

    mapGetModelByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetModelByNumber', ctypes.c_void_p, ctypes.c_long, maptype.HSELECT)
    def mapGetModelByNumber(_hvcl: ctypes.c_void_p, _number: int, _hselect: maptype.HSELECT) -> int:
        """
        Запросить модель по номеру модели
        
        :param _hvcl: идентификатор процесса чтения/записи макетов условий отбора
        
        :param _number: номер модели в файле макетов условий отбора
        
        :param _hselect: контекст условий отбора объектов, в который считывается модель из файла
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetModelByNumber_t (_hvcl, _number, _hselect)

    mapGetModelByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetModelByNameUn', ctypes.c_void_p, maptype.PWCHAR, maptype.HSELECT)
    def mapGetModelByNameUn(_hvcl: ctypes.c_void_p, _name: mapsyst.WTEXT, _hselect: maptype.HSELECT) -> int:
        """
        Запросить модель по имени модели
        
        :param _hvcl: идентификатор процесса чтения/записи макетов условий отбора
        
        :param _name: имя модели
        
        :param _hselect: контекст условий отбора объектов, в который считывается модель из файла
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetModelByNameUn_t (_hvcl, _name.buffer(), _hselect)

    mapModelNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapModelNameUn', ctypes.c_void_p, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapModelNameUn(_hvcl: ctypes.c_void_p, _number: int, _name: mapsyst.WTEXT, _namesize: int) -> int:
        """
        Запросить имя модели по номеру
        
        :param _hvcl: идентификатор процесса чтения/записи макетов условий отбора
        
        :param _number: номер модели в файле макетов условий отбора
        
        :param _name: адрес строки для размещения имени модели
        
        :param _namesize: размер буфера для записи имени модели
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapModelNameUn_t (_hvcl, _number, _name.buffer(), _namesize)

    mapUpdateModelByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateModelByNameUn', ctypes.c_void_p, maptype.PWCHAR, maptype.HSELECT)
    def mapUpdateModelByNameUn(_hvcl: ctypes.c_void_p, _name: mapsyst.WTEXT, _hselect: maptype.HSELECT) -> int:
        """
        Обновить модель с заданным именем
        
        :param _hvcl: идентификатор процесса чтения/записи макетов условий отбора
        
        :param _name: имя модели
        
        :param _hselect: контекст условий отбора объектов, который записывается в файл моделей
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapUpdateModelByNameUn_t (_hvcl, _name.buffer(), _hselect)

    mapModelFree_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapModelFree', ctypes.c_void_p)
    def mapModelFree(_hvcl: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Закрыть файл макетов условий отбора
        
        :param _hvcl: идентификатор процесса чтения/записи макетов условий отбора
        """
        return mapModelFree_t (_hvcl)

    mapRestoreTotalSeekSelectModelEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRestoreTotalSeekSelectModelEx', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapRestoreTotalSeekSelectModelEx(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _mode: int) -> int:
        """
        Восстановить параметры поиска и выделения объектов по области
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _name: имя восстанавливаемой модели условий поиска для всех карт
        
        :param _mode: режим сохранения состояния отбора объектов: ``1`` - записывать в модель список уникальных номеров объектов, ``0`` - записывать в модель списки видов объектов (ключи или коды), слоев, локализаций Зарезервированные имена моделей условий: ``"MarkParameters"`` - имя модели параметров поиска по рамке ``"AreaParameters"`` - имя модели параметров поиска по области ``"PySeekParameters"`` - имя модели сохраненных параметров поиска при запуске отладчика В результате устанавливаются и включаются условия поиска и выделения объектов в документе - mapSetTotalSelectFlag(hmap, ``1``);
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapRestoreTotalSeekSelectModelEx_t (_hmap, _name.buffer(), _mode)

    mapSaveTotalSeekSelectModel_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSaveTotalSeekSelectModel', maptype.HMAP, maptype.PWCHAR)
    def mapSaveTotalSeekSelectModel(_hmap: maptype.HMAP, _name: mapsyst.WTEXT) -> int:
        """
        Сохранить параметры поиска и выделения объектов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _name: имя восстанавливаемой модели условий поиска для всех карт Зарезервированные имена моделей условий: ``"MarkParameters"`` - имя модели параметров поиска по рамке ``"AreaParameters"`` - имя модели параметров поиска по области ``"PySeekParameters"`` - имя модели сохраненных параметров поиска при запуске отладчика
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSaveTotalSeekSelectModel_t (_hmap, _name.buffer())

    olsCreate_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJLISTSEEK,'olsCreate', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR)
    def olsCreate(_hmap: maptype.HMAP, _setname1: mapsyst.WTEXT, _setname2: mapsyst.WTEXT) -> maptype.HOBJLISTSEEK:
        """
        Создать контекст поиска пересечений объектов по спискам объектов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _setname1: имя списка объектов ``1`` в файле ``OBX`` (для карт открытого документа)
        
        :param _setname2: имя списка объектов ``2`` в файле ``OBX`` (для карт открытого документа)
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HOBJLISTSEEK
        
        .. note::

           Если setname1 ``= 0`` или setname2 ``= 0``, то списки объектов устанавливаются
           с помощью функций olsAppendSelectToList1 и olsAppendSelectToList2 (для каждой карты)
           По окончании обработки необходимо вызвать olsFree
        """
        return olsCreate_t (_hmap, _setname1.buffer(), _setname2.buffer())

    olsFree_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'olsFree', maptype.HOBJLISTSEEK)
    def olsFree(_hols: maptype.HOBJLISTSEEK) -> int:
        """
        Освободить ресурсы, выделенные в olsCreate
        
        :param _hols: идентификатор контекста поиска пересечений
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return olsFree_t (_hols)

    olsAppendSelectToList1_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'olsAppendSelectToList1', maptype.HOBJLISTSEEK, ctypes.c_int, maptype.HSELECT)
    def olsAppendSelectToList1(_hols: maptype.HOBJLISTSEEK, _mapnumber: int, _hselect: maptype.HSELECT) -> int:
        """
        Добавить условия отбора объектов карты в список 1
        
        :param _hols: идентификатор контекста поиска пересечений
        
        :param _mapnumber: номер карты в открытых данных, от ``0`` до mapGetSiteCount(...)
        
        :param _hselect: контекст условий отбора объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return olsAppendSelectToList1_t (_hols, _mapnumber, _hselect)

    olsAppendSelectToList2_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'olsAppendSelectToList2', maptype.HOBJLISTSEEK, ctypes.c_int, maptype.HSELECT)
    def olsAppendSelectToList2(_hols: maptype.HOBJLISTSEEK, _mapnumber: int, _hselect: maptype.HSELECT) -> int:
        """
        Добавить условия отбора объектов карты в список 2
        
        :param _hols: идентификатор контекста поиска пересечений
        
        :param _mapnumber: номер карты в открытых данных, от ``0`` до mapGetSiteCount(...)
        
        :param _hselect: контекст условий отбора объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return olsAppendSelectToList2_t (_hols, _mapnumber, _hselect)

    olsRunSeekEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'olsRunSeekEx', maptype.HOBJLISTSEEK, ctypes.POINTER(maptype.SEEKDIALOGPARM), maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def olsRunSeekEx(_hols: maptype.HOBJLISTSEEK, _parm: ctypes.POINTER(maptype.SEEKDIALOGPARM), _callevent: maptype.EVENTSTATE, _callparm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Выполнить поиск по спискам объектов карты
        
        :param _hols: идентификатор контекста поиска пересечений
        
        :param _parm: параметры поиска
        
        :param _callevent: адрес функции оборатного вызова для уведомления о проценте обработанных наборов данных
        
        :param _callparm: адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы, вторым параметром в вызываемой функции передается процент от ``0`` до ``100``)
        
        :returns: Возвращает количество найденных объектов При ошибке возвращает ноль
        :rtype: int
        """
        return olsRunSeekEx_t (_hols, _parm, _callevent, _callparm)

    olsGetResultSelect_t = mapsyst.GetProcAddress(acceslib,maptype.HSELECT,'olsGetResultSelect', maptype.HOBJLISTSEEK, ctypes.c_int)
    def olsGetResultSelect(_hols: maptype.HOBJLISTSEEK, _mapnumber: int) -> maptype.HSELECT:
        """
        Запросить контекст условий отобранных объектов по номеру карты
        
        :param _hols: идентификатор контекста поиска пересечений
        
        :param _mapnumber: номер карты в открытых данных, от ``0`` до mapGetSiteCount(...)
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HSELECT
        """
        return olsGetResultSelect_t (_hols, _mapnumber)



def seekapi_healthcheck():
    return 1
