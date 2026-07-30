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
    *          Диалоги редактирования свойств объекта карты и          *
    *              графического описания видов объектов                *
    *          Диалог Редактора классификатора                         *
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
    if os.environ['gisrsctoolsdll']:
        gisrsctoolsname = os.environ['gisrsctoolsdll']
except KeyError:
    gisrsctoolsname = 'gis64rsctools.dll'

try:
    rsctoolslib = mapsyst.LoadLibrary(gisrsctoolsname)
except Exception as e:
    print(e)
    rsctoolslib = 0

if rsctoolslib == 0:
    print(gisrsctoolsname)
else:
    rscShowStatisticObjectEx_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_long,'rscShowStatisticObjectEx', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def rscShowStatisticObjectEx(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _hobj: maptype.HOBJ, _mode: int, _activepage: int) -> int:
        """
        Открыть диалог "Выбор объекта"
        
        :param _hmap: идентификатор открытых данных
        
        :param _parm: параметры задачи
        
        :param _hobj: идентификатор объекта карты
        
        :param _mode: режим работы диалога: ``0`` - ввод семантики при создании объекта (включена опция ``"Вся семантика"``, отключены кнопки ``"Выбрать"``, ``"Вперед"`` и ``"Назад"``) ``1`` - просмотр, редактирование и выбор объекта карты заполняется список объектов в данной точке -``1`` - режим поиска и выделения объекта ``2`` - просмотр данных объекта (отключены кнопки ``"Выбрать"``, ``"Вперед"`` и ``"Назад"``)
        
        :param _activepage: флаг установки активной вкладки: ``0`` - семантика, ``1`` - метрика, ``2`` - набор, ``3`` - масштаб, ``4`` - вид, ``5`` - графика, ``6`` - 3D -``1`` - устанавливается из ini-файла приложения
        
        :returns: При ошибке возвращает 0
        :rtype: int
        
        .. note::

           Если mode равно 0 или 2, то устанавливается вкладка ``"Семантика"``,
           при отсутствии точек метрики - вкладка ``"Метрика"``
           Основные вкладки ``"Семантика"``, ``"Метрика"``, ``"Масштаб"``.
           Для объекта вид которого определен в классификаторе, добавляется вкладка ``"Вид"``.
           Для объекта, имеющего 3D-вид, добавляется вкладка ``"3D"``.
           Для объекта, входящего в группу объектов, добавляется вкладка ``"Набор объектов"``.
           Для объекта, имеющего графический вид, добавляется вкладка ``"Графика"``.
           Активность и действия при нажатии кнопки ``"Сохранить"`` на всех вкладках
           диалога синхронизированы. Кнопка ``"Сохранить"`` становится активной
           при изменении любого параметра, либо при создании объекта.
           При закрытии диалога:
           - форма освобождается вне зависимости от возвращаемого значения
           - единицы измерения площади и длины записываются в INI-файл документа
           Возвращаемые значения в выбранном режиме работы диалога:
           1) создание объекта (mode ``= 0``):
           ``1`` - при нажатии кнопки ``"Сохранить"``
           ``0`` - закрытие диалога (отказ от сохранения)
           2) выбор объекта (mode ``= 1``):
           -``1`` - при нажатии кнопки ``"Выбор объекта на карте"``
           ``1`` - при нажатии кнопки ``"Сохранить"``
           ``0`` - закрытие диалога (отказ от сохранения и выбора)
           3) поиск объекта (mode ``= -1``):
           -``1`` - при выборе режима ``"Выбор объекта на карте"``
           ``0`` - закрытие диалога (отказ от выбора)
        """
        return rscShowStatisticObjectEx_t (_hmap, _parm, _hobj, _mode, _activepage)

    rscCreateObjectDialog_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_void_p,'rscCreateObjectDialog', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.POINT))
    def rscCreateObjectDialog(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _hobj: maptype.HOBJ, _planepoint: ctypes.POINTER(maptype.DOUBLEPOINT), _mode: int, _activepage: int, _position: ctypes.POINTER(maptype.POINT)) -> ctypes.c_void_p:
        """
        Создать диалог "Выбор объекта"
        
        :param _hmap: идентификатор открытых данных
        
        :param _parm: параметры задачи
        
        :param _hobj: идентификатор объекта карты
        
        :param _planepoint: точка курсора на карте (в метрах на местности) Используется для размещения изображения выбранного объекта в диалоге (соответствует центру окна с объектом).
        
        :param _mode: режим работы диалога: ``0`` - ввод семантики при создании объекта (включена опция ``"Вся семантика"``, отключены кнопки ``"Выбрать"``, ``"Вперед"`` и ``"Назад"``) ``1`` - просмотр, редактирование и выбор объекта карты заполняется список объектов в данной точке -``1`` - режим поиска и выделения объекта ``2`` - просмотр данных объекта (отключены кнопки ``"Выбрать"``, ``"Вперед"`` и ``"Назад"``)
        
        :param _activepage: флаг установки активной вкладки: ``0`` - семантика, ``1`` - метрика, ``2`` - набор, ``3`` - масштаб, ``4`` - вид, ``5`` - графика, ``6`` - 3D -``1`` - устанавливается из ini-файла приложения.
        
        :param _position: положение диалога при открытии
        
        :returns: Возвращает идентификатор открытого диалога (HSTATISTIC) Для освобождения диалога вызывать rscCloseStatisticObject Для смены объекта (без переоткрытия диалога) вызывать rscChangeStatisticObject При ошибке возвращает 0
        
        .. note::

           Если planepoint ``= 0``, то выбирается первая точка метрики объекта,
           (исключение - для линейного объекта выбирается центральная точка)
           Если mode ``= 0`` или 2, то устанавливается вкладка ``"Семантика"``,
           при отсутствии точек метрики - ``"Метрика"``
        """
        return rscCreateObjectDialog_t (_hmap, _parm, _hobj, _planepoint, _mode, _activepage, _position)

    rscChangeStatisticObject_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_long,'rscChangeStatisticObject', ctypes.c_void_p, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT))
    def rscChangeStatisticObject(_hstat: ctypes.c_void_p, _hobj: maptype.HOBJ, _planepoint: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Изменить выбранный объект в диалоге "Выбор объекта" открытого с помощью функции rscCreateObjectDialog
        
        :param _hstat: идентификатор открытого диалога
        
        :param _hobj: идентификатор объекта карты (если hobj ``= 0``, то установить фокус на окно диалога)
        
        :param _planepoint: точка курсора на карте (в метрах на местности) Используется для размещения изображения выбранного объекта в диалоге (соответствует центру окна с объектом).
        
        :returns: При ошибке возвращает 0
        :rtype: int
        
        .. note::

           Если planepoint ``= 0``, то выбирается первая точка метрики объекта,
           (исключение - для линейного объекта выбирается центральная точка)
        """
        return rscChangeStatisticObject_t (_hstat, _hobj, _planepoint)

    rscCloseStatisticObject_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_long,'rscCloseStatisticObject', ctypes.c_void_p)
    def rscCloseStatisticObject(_hstat: ctypes.c_void_p) -> int:
        """
        Закрыть диалог "Выбор объекта" открытый с помощью функции rscCreateObjectDialog
        
        :param _hstat: идентификатор открытого диалога
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return rscCloseStatisticObject_t (_hstat)

    rscEditTextParameters_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_long,'rscEditTextParameters', maptype.HMAP, maptype.HRSC, ctypes.POINTER(mapgdi.IMGTEXT), ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.TASKPARMEX))
    def rscEditTextParameters(_hmap: maptype.HMAP, _hrsc: maptype.HRSC, _text: ctypes.POINTER(mapgdi.IMGTEXT), _function: int, _textflag: int, _typedia: int, _currentpalette: int, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Редактировать параметры текста
        
        :param _hmap: идентификатор открытых данных
        
        :param _hrsc: идентификатор классификатора открытой карты
        
        :param _text: параметры шрифта
        
        :param _function: номер функции шрифта
        
        :param _textflag: режим диалога: ``0`` - чистый диалог текст ``1`` - вызван из ``TRUETYPE`` ``2`` - вызван из ``TRIETYPE`` в шаблоне ``3`` - вызван из шаблона ``4`` - вызван из векторного объекта
        
        :param _typedia: тип параметров вида объекта (``DI_SCR``, ``DI_PRN``, ``DI_IMG``)
        
        :param _currentpalette: номер текущей палитры
        
        :param _parm: параметры задачи
        
        :returns: При успешном завершении возвращает 1 и новые параметры, иначе возвращает 0
        :rtype: int
        """
        return rscEditTextParameters_t (_hmap, _hrsc, _text, _function, _textflag, _typedia, _currentpalette, _parm)

    rscEditColorByType_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_long,'rscEditColorByType', maptype.HRSC, ctypes.POINTER(maptype.COLORREF), ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.TASKPARMEX))
    def rscEditColorByType(_hrsc: maptype.HRSC, _color: ctypes.POINTER(maptype.COLORREF), _currentpalette: int, _diatype: int, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Редактировать цвет
        
        :param _hrsc: идентификатор классификатора открытой карты
        
        :param _color: цвет из классификатора
        
        :param _currentpalette: номер текущей палитры
        
        :param _diatype: тип параметров вида объекта (``DI_SCR``, ``DI_PRN``, ``DI_IMG``)
        
        :param _parm: параметры задачи
        
        :returns: При успешном завершении возвращает 1 и новый цвет, иначе возвращает 0
        :rtype: int
        """
        return rscEditColorByType_t (_hrsc, _color, _currentpalette, _diatype, _parm)

    rscEditTableParameters_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_long,'rscEditTableParameters', maptype.HMAP, maptype.HRSC, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_long, ctypes.c_long, ctypes.c_char_p, ctypes.c_long)
    def rscEditTableParameters(_hmap: maptype.HMAP, _hrsc: maptype.HRSC, _parm: ctypes.POINTER(maptype.TASKPARMEX), _diatype: int, _currentpalette: int, _buff: ctypes.c_char_p, _buffsize: int) -> int:
        """
        Редактировать параметры объекта типа "Таблица" (IMG_TABLE)
        
        :param _hmap: идентификатор открытых данных
        
        :param _hrsc: идентификатор классификатора открытой карты
        
        :param _parm: параметры задачи
        
        :param _diatype: тип параметров вида объекта (``DI_SCR``, ``DI_PRN``, ``DI_IMG``)
        
        :param _currentpalette: номер текущей палитры
        
        :param _buff: параметры ``IMGTABLE``
        
        :param _buffsize: размер выделенного буфера (``1024``)
        
        :returns: При сохранении редактирования возвращает 1 При ошибке или отказе редактирования возвращает 0
        :rtype: int
        """
        return rscEditTableParameters_t (_hmap, _hrsc, _parm, _diatype, _currentpalette, _buff, _buffsize)

    rscCreateObjectTable_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_long,'rscCreateObjectTable', maptype.HMAP, maptype.HOBJ, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_long, ctypes.c_long, ctypes.c_char_p, ctypes.c_long)
    def rscCreateObjectTable(_hmap: maptype.HMAP, _hobj: maptype.HOBJ, _parm: ctypes.POINTER(maptype.TASKPARMEX), _diatype: int, _currentpalette: int, _buff: ctypes.c_char_p, _buffsize: int) -> int:
        """
        Создать объект типа "Таблица" (IMG_TABLE)
        
        :param _hmap: идентификатор открытых данных
        
        :param _hobj: идентификатор создаваемого объекта
        
        :param _parm: параметры задачи
        
        :param _diatype: тип параметров вида объекта (``DI_SCR``, ``DI_PRN``, ``DI_IMG``)
        
        :param _currentpalette: номер текущей палитры
        
        :param _buff: параметры ``IMGTABLE``
        
        :param _buffsize: размер выделенного буфера
        
        :returns: При сохранении редактирования возвращает 1 При ошибке или отказе редактирования возвращает 0
        :rtype: int
        """
        return rscCreateObjectTable_t (_hmap, _hobj, _parm, _diatype, _currentpalette, _buff, _buffsize)


# Создать диалог "Ввод данных"
# value        - значение для установки в редактируемое поле
# parm         - параметры задачи
# callbackfunc - указатель на функцию обратного вызова
# callparam    - параметр, который будет передан вызываемой функции
# Возвращает идентификатор открытого диалога (HEDITVALUE)
# При ошибке возвращает 0

#   rscCreateEditValueDialog_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_void_p,'rscCreateEditValueDialog', maptype.PWCHAR, ctypes.POINTER(maptype.TASKPARMEX), CallbackEditValue, ctypes.c_void_p)
#   def rscCreateEditValueDialog(_value: mapsyst.WTEXT, _parm: ctypes.POINTER(maptype.TASKPARMEX), _callbackfunc: CallbackEditValue, _callparam: ctypes.c_void_p) -> ctypes.c_void_p:
#       return rscCreateEditValueDialog_t (_value.buffer(), _parm, _callbackfunc, _callparam)

    rscChangeEditValueDialogPos_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_long,'rscChangeEditValueDialogPos', ctypes.c_void_p, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.RECT), ctypes.c_uint)
    def rscChangeEditValueDialogPos(_hdial: ctypes.c_void_p, _value: mapsyst.WTEXT, _left: int, _top: int, _isfocus: int, _clrect: ctypes.POINTER(maptype.RECT), _key: int) -> int:
        """
        Обновить положение и текст диалога "Ввод данных"
        
        :param _hdial: идентификатор открытого диалога
        
        :param _value: значение для установки в редактируемое поле
        
        :param _left: положение диалога относительно курсора (справа)
        
        :param _top: положение диалога относительно курсора
        
        :param _isfocus: установка фокуса в диалог для ввода значения
        
        :param _clrect: габариты окна (клиентская область), в пределах которого отображается диалог в пикселях экрана
        
        :param _key: код клавиши, с помощью которой установился фокус на диалог Обрабатываемые символы: ``","`` (код: ``188``), ``"."`` (код: ``190``) и цифры. Добавляется первым символом в поле ввода, курсор ставится на следующую позицию - ``0`` - не добавляется в поле ввода Положение диалога изменяется в пределах габаритов окна (например, в крайней правой точке диалог будет расположен слева от курсора) ``0`` - положение диалога относительно значений left, top без корректировки положения
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return rscChangeEditValueDialogPos_t (_hdial, _value.buffer(), _left, _top, _isfocus, _clrect, _key)

    rscSetEditValueVisible_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_void_p,'rscSetEditValueVisible', ctypes.c_void_p, ctypes.c_long)
    def rscSetEditValueVisible(_hdial: ctypes.c_void_p, _view: int) -> ctypes.c_void_p:
        """
        Установить видимость диалога "Ввод данных"
        
        :param _hdial: идентификатор открытого диалога
        
        :param _view: видимость диалога: - ``0`` - скрыть диалог - ``1`` - отобразить диалог
        """
        return rscSetEditValueVisible_t (_hdial, _view)

    rscCloseEditValueDialog_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_void_p,'rscCloseEditValueDialog', ctypes.c_void_p)
    def rscCloseEditValueDialog(_hdial: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Закрыть диалог "Ввод данных"
        
        :param _hdial: идентификатор открытого диалога
        """
        return rscCloseEditValueDialog_t (_hdial)

    rscEditGraphicMarkParametersEx_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_long,'rscEditGraphicMarkParametersEx', maptype.HMAP, maptype.HRSC, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.c_char_p, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long), ctypes.c_long)
    def rscEditGraphicMarkParametersEx(_hmap: maptype.HMAP, _hrsc: maptype.HRSC, _parm: ctypes.POINTER(maptype.TASKPARMEX), _diatype: int, _currentpalette: int, _function: ctypes.POINTER(ctypes.c_long), _buff: ctypes.c_char_p, _buffsize: int, _mapnumber: ctypes.POINTER(ctypes.c_long), _layernumber: ctypes.POINTER(ctypes.c_long), _regime: int) -> int:
        """
        Редактировать параметры графического файла
        
        :param _hmap: идентификатор открытых данных
        
        :param _hrsc: идентификатор классификатора открытой карты
        
        :param _parm: параметры задачи
        
        :param _diatype: тип параметров вида объекта (``DI_SCR``, ``DI_PRN``, ``DI_IMG``)
        
        :param _currentpalette: номер текущей палитры
        
        :param _function: номер функции визуализации графических объектов
        
        :param _buff: параметры ``IMGGRAPHICMARKEX``
        
        :param _buffsize: размер выделенного буфера (``1024``)
        
        :param _mapnumber: номер пользовательской карты в цепочке
        
        :param _layernumber: номер слоя
        
        :param _regime: режим вызова диалога: ``1`` - нанесение на карту графического файла, иначе - ``0``
        
        :returns: При сохранении редактирования возвращает 1 При ошибке или отказе редактирования возвращает 0
        :rtype: int
        """
        return rscEditGraphicMarkParametersEx_t (_hmap, _hrsc, _parm, _diatype, _currentpalette, _function, _buff, _buffsize, _mapnumber, _layernumber, _regime)

    rscEditPointImageEx_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_long,'rscEditPointImageEx', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_char_p, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long), ctypes.c_long, ctypes.c_long)
    def rscEditPointImageEx(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _buff: ctypes.c_char_p, _buffsize: int, _mapnumber: ctypes.POINTER(ctypes.c_long), _layernumber: ctypes.POINTER(ctypes.c_long), _type: int, _currentpalette: int) -> int:
        """
        Редактировать графический точечный объект
        
        :param _hmap: идентификатор открытых данных
        
        :param _parm: параметры задачи
        
        :param _buff: адрес области для размещения параметров точечного знака
        
        :param _buffsize: размер области параметров (не менее ``8*`` ``1024``)
        
        :param _mapnumber: номер пользовательской карты в цепочке
        
        :param _layernumber: номер слоя
        
        :param _type: тип диалога редактирования параметров (``DI_SCR``, ``DI_PRN``, ``DI_IMG``)
        
        :param _currentpalette: номер текущей палитры
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return rscEditPointImageEx_t (_hmap, _parm, _buff, _buffsize, _mapnumber, _layernumber, _type, _currentpalette)

    rscEditColorEx_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_long,'rscEditColorEx', maptype.HRSC, ctypes.POINTER(maptype.COLORREF), ctypes.c_int, ctypes.POINTER(maptype.TASKPARMEX))
    def rscEditColorEx(_hrsc: maptype.HRSC, _color: ctypes.POINTER(maptype.COLORREF), _currentpalette: int, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Редактировать цвет
        
        :param _hrsc: идентификатор классификатора открытой карты
        
        :param _color: цвет из классификатора
        
        :param _currentpalette: номер текущей палитры
        
        :param _parm: параметры задачи
        
        :returns: При успешном завершении возвращает 1 и новый цвет , иначе возвращает 0
        :rtype: int
        """
        return rscEditColorEx_t (_hrsc, _color, _currentpalette, _parm)

    rscEditPaletteGroup_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_long,'rscEditPaletteGroup', maptype.HRSC, ctypes.POINTER(maptype.TASKPARMEX))
    def rscEditPaletteGroup(_hrsc: maptype.HRSC, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Редактировать палитру классификатора с именованными цветами
        
        :param _hrsc: идентификатор классификатора открытой карты
        
        :param _parm: параметры задачи
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return rscEditPaletteGroup_t (_hrsc, _parm)

    rscEditRSC_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_long,'rscEditRSC', maptype.HMAP, ctypes.POINTER(maptype.TASKPARMEX), ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def rscEditRSC(_hmap: maptype.HMAP, _parm: ctypes.POINTER(maptype.TASKPARMEX), _sitenumber: int, _layernumber: int, _objectnumber: int, _fontnumber: int) -> int:
        """
        Выбрать символ шрифта
        
        parent   - идентификатор окна родителя
        
        :param _hmap: идентификатор открытых данных fontname - имя шрифта symbol   - номер символа в шрифте (если ``0``, то устанавливается первый заданный в шрифте)
        
        :param _hmap: идентификатор открытых данных
        
        :param _parm: параметры задачи
        
        :param _sitenumber: номер пользовательской карты в цепочке (``0`` - для главной карты)
        
        :param _layernumber: номер выбранного слоя или -``1``
        
        :param _objectnumber: номер выбранного объекта или -``1``
        
        :param _fontnumber: номер выбранного шрифта или -``1``
        
        :returns: Возвращает номер символа в шрифте При ошибке или отказе от выбора возвращает 0 Вызов диалога редактирования классификатора При ошибке возвращает 0
        :rtype: int
        """
        return rscEditRSC_t (_hmap, _parm, _sitenumber, _layernumber, _objectnumber, _fontnumber)

    rscCreateRSC_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_long,'rscCreateRSC', maptype.PWCHAR, ctypes.POINTER(maptype.TASKPARMEX))
    def rscCreateRSC(_name: mapsyst.WTEXT, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Вызов диалога создания и редактирования классификатора
        
        :param _name: имя создаваемого классификатора с путем
        
        :param _parm: параметры задачи
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return rscCreateRSC_t (_name.buffer(), _parm)

    rscOpenRSC_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_long,'rscOpenRSC', maptype.PWCHAR, ctypes.POINTER(maptype.TASKPARMEX))
    def rscOpenRSC(_name: mapsyst.WTEXT, _parm: ctypes.POINTER(maptype.TASKPARMEX)) -> int:
        """
        Открыть классификатор с вызовом диалога Редактора классификатора
        
        :param _name: имя существующего классификатора с путем
        
        :param _parm: параметры задачи
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return rscOpenRSC_t (_name.buffer(), _parm)

    rscRscToXsd_t = mapsyst.GetProcAddress(rsctoolslib,ctypes.c_long,'rscRscToXsd', maptype.HRSC)
    def rscRscToXsd(_hrsc: maptype.HRSC) -> int:
        """
        Сформировать XSD-схему по классификатору
        
        :param _hrsc: идентификатор классификатора открытой карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return rscRscToXsd_t (_hrsc)



def rsctools_healthcheck():
    return 1
