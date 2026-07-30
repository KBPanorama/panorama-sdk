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
    *       Описание класса доступа к объекту "журнал транзакций"      *
    *        Интерфейс для программ на языках c, pascal, basic         *
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
    mapGetLogAccess_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetLogAccess', maptype.HMAP, maptype.HSITE)
    def mapGetLogAccess(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить - ведется ли журнал транзакций
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Возвращает ``0`` - если журнал не ведется
        :rtype: int
        """
        return mapGetLogAccess_t (_hmap, _hsite)

    mapLogAccess_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLogAccess', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapLogAccess(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _mode: int) -> int:
        """
        Запретить или разрешить ведение журнала транзакций
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _mode: режим ведения журнала транзакций: ``0`` - ведение журнала транзакций запретить ``1`` - ведение журнала транзакций разрешить
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           После открытия карты ведение журнала разрешено
           Допускается использовать только при потоковой обработке объектов,
           когда быстродействие важнее возможности сохранить данные при сбое системы
           Перед отключением журнала рекомендуется позаботиться о резервной копии данных
        """
        return mapLogAccess_t (_hmap, _hsite, _mode)

    mapLogCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLogCount', maptype.HMAP, maptype.HSITE)
    def mapLogCount(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить число транзакций в журнале
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapLogCount_t (_hmap, _hsite)

    mapLogDate_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLogDate', maptype.HMAP, maptype.HSITE, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapLogDate(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _date: ctypes.POINTER(ctypes.c_long), _time: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить дату создания журнала
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _date: дата по Гринвичу в формате ``"YYYYMMDD"``
        
        :param _time: время по Гринвичу в формате ``"число секунд от 00:00:00"`` на указанную дату
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapLogDate_t (_hmap, _hsite, _date, _time)

    mapLogCreateAction_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLogCreateAction', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapLogCreateAction(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _type: int) -> int:
        """
        Открыть запись транзакции
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _type: тип транзакции (от ``0x4000`` до ``0х0FFFF`` - за Панорамой)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapLogCreateAction_t (_hmap, _hsite, _type)

    mapLogPutRecord_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLogPutRecord', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.ACTIONRECORD))
    def mapLogPutRecord(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _record: ctypes.POINTER(maptype.ACTIONRECORD)) -> int:
        """
        Внести в описание транзакции сведения об операции
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _record: описание операции (структура ``ACTIONRECORD`` описана в maptype.h)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapLogPutRecord_t (_hmap, _hsite, _record)

    mapLogCommitActionEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLogCommitActionEx', maptype.HMAP, maptype.HSITE, ctypes.POINTER(ctypes.c_long))
    def mapLogCommitActionEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _number: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Закрыть запись транзакции
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _number: поле для записи номера выполненной транзакции в журнале транзакций
        
        :returns: Возвращает число выполненных операций в транзакции для карты Если число транзакций не может быть определено возвращает -1 При ошибке возвращает ноль
        :rtype: int
        """
        return mapLogCommitActionEx_t (_hmap, _hsite, _number)

    mapLogGetActionNumberByTime_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLogGetActionNumberByTime', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long)
    def mapLogGetActionNumberByTime(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _date: int, _time: int) -> int:
        """
        Запросить номер первой транзакции, выполненной после указанных даты и времени
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _date: дата в формате ``"YYYYMMDD"``
        
        :param _time: время в формате ``"число секунд от 00:00:00"`` на указанную дату (по Гринвичу - GetSystemTime, in Coordinated Universal Time (``UTC``))
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapLogGetActionNumberByTime_t (_hmap, _hsite, _date, _time)

    mapReadLastActionEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapReadLastActionEx', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.ACTIONHEAD), ctypes.c_long)
    def mapReadLastActionEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _head: ctypes.POINTER(maptype.ACTIONHEAD), _flag: int) -> int:
        """
        Считать заголовок описания последней не отмененной транзакции задачи из журнала
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _head: заголовок описания транзакции (структура ``ACTIONHEAD`` описана в maptype.h)
        
        :param _flag: условия выбора последней транзакции: ``LOG_ANYACTION``(``0``) - нет условий, ``LOG_MYACTION``(``1``) - считывать последнюю свою транзакцию (пропускать транзакции других пользователей)
        
        :returns: или журнал пуст - возвращает ноль При ошибке возвращает ноль, иначе - номер транзакции
        :rtype: int
        
        .. note::

           Если после транзакции выполнялась сортировка карты с удалением копий отредактированных объектов
        """
        return mapReadLastActionEx_t (_hmap, _hsite, _head, _flag)

    mapReadLastUndoActionEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapReadLastUndoActionEx', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.ACTIONHEAD), ctypes.POINTER(ctypes.c_long), ctypes.c_long)
    def mapReadLastUndoActionEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _head: ctypes.POINTER(maptype.ACTIONHEAD), _actionnumber: ctypes.POINTER(ctypes.c_long), _flag: int) -> int:
        """
        Считать заголовок описания последней транзакции "Шаг назад" и запросить номер отмененной транзакции - подготовка команды "Восстановить"
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _head: адрес поля для записи заголовка транзакции ``"Шаг назад"`` (структура ``ACTIONHEAD`` описана в maptype.h)
        
        :param _actionnumber: адрес поля для записи номера отмененной транзакции
        
        :param _flag: условия выбора последней транзакции ``"Шаг назад"``: ``LOG_ANYACTION``(``0``) - нет условий, ``LOG_MYACTION``(``1``) - считывать последнюю свою транзакцию (пропускать транзакции других пользователей)
        
        :returns: или журнал пуст - возвращает ноль При ошибке возвращает ноль, иначе - номер транзакции
        :rtype: int
        
        .. note::

           Если после транзакции выполнялась сортировка карты с удалением копий отредактированных объектов
        """
        return mapReadLastUndoActionEx_t (_hmap, _hsite, _head, _actionnumber, _flag)

    mapLogReadAction_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLogReadAction', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.POINTER(maptype.ACTIONHEAD))
    def mapLogReadAction(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _number: int, _head: ctypes.POINTER(maptype.ACTIONHEAD)) -> int:
        """
        Считать заголовок описания транзакции из журнала
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _number: последовательный номер транзакции (от ``1`` до Count(...))
        
        :param _head: заголовок описания транзакции (структура ``ACTIONHEAD`` описана в maptype.h)
        
        :returns: При ошибке возвращает ноль, иначе - число операций в транзакции
        :rtype: int
        """
        return mapLogReadAction_t (_hmap, _hsite, _number, _head)

    mapLogGetActionRecordEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLogGetActionRecordEx', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long, ctypes.POINTER(maptype.ACTIONRECORD))
    def mapLogGetActionRecordEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _number: int, _recnumber: int, _record: ctypes.POINTER(maptype.ACTIONRECORD)) -> int:
        """
        Запросить сведения об операции
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _number: последовательный номер транзакции (от ``1``)
        
        :param _recnumber: номер операции (от ``1`` до ReadAction(...))
        
        :param _record: описание операции (структура ``ACTIONRECORD`` описана в maptype.h)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapLogGetActionRecordEx_t (_hmap, _hsite, _number, _recnumber, _record)

    mapLogGetActionRecordCountEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLogGetActionRecordCountEx', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapLogGetActionRecordCountEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _number: int) -> int:
        """
        Запросить количество операций в транзакции
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _number: номер транзакции
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapLogGetActionRecordCountEx_t (_hmap, _hsite, _number)

    mapLogIsWrite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLogIsWrite', maptype.HMAP, maptype.HSITE)
    def mapLogIsWrite(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить доступен ли журнал на запись
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapLogIsWrite_t (_hmap, _hsite)

    mapLogRedoLastAction_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLogRedoLastAction', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapLogRedoLastAction(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flag: int) -> int:
        """
        Восстановить последнюю отмененную транзакцию
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _flag: условия выбора последней транзакции: ``LOG_ANYACTION``(``0``) - нет условий, ``LOG_MYACTION``(``1``) - считывать последнюю свою транзакцию (пропускать транзакции других пользователей)
        
        :returns: карты с удалением копий отредактированных объектов или журнал пуст - возвращает ноль При ошибке возвращает ноль, иначе - количество восстановленных операций
        :rtype: int
        
        .. note::

           Если после отмены транзакции выполнялись другие операции или выполнялась сортировка
        """
        return mapLogRedoLastAction_t (_hmap, _hsite, _flag)

    mapLogAbolitionLastActionEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLogAbolitionLastActionEx', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapLogAbolitionLastActionEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flag: int) -> int:
        """
        Отменить последнюю транзакцию
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _flag: условия выбора последней транзакции: ``LOG_ANYACTION``(``0``) - нет условий, ``LOG_MYACTION``(``1``) - обрабатывать последнюю свою транзакцию (пропускать транзакции других пользователей)
        
        :returns: или журнал пуст - возвращает ноль При ошибке возвращает ноль, иначе - количество восстановленных операций
        :rtype: int
        
        .. note::

           Если после транзакции выполнялась сортировка карты с удалением копий отредактированных объектов
        """
        return mapLogAbolitionLastActionEx_t (_hmap, _hsite, _flag)

    mapLogUndoAction_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLogUndoAction', maptype.HMAP, ctypes.POINTER(maptype.HSITE), ctypes.c_long)
    def mapLogUndoAction(_hmap: maptype.HMAP, _hsite: ctypes.POINTER(maptype.HSITE), _flag: int) -> int:
        """
        Отменить последнюю транзакцию в документе
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _flag: условия выбора последней транзакции: ``LOG_ANYACTION``(``0``) - нет условий, ``LOG_MYACTION``(``1``) - обрабатывать последнюю свою транзакцию (пропускать транзакции других пользователей)
        
        :returns: или журнал пуст - возвращает ноль При ошибке возвращает ноль, иначе - количество восстановленных операций
        :rtype: int
        
        .. note::

           Если после транзакции выполнялась сортировка карты
        """
        return mapLogUndoAction_t (_hmap, _hsite, _flag)

    mapLogReadActionForUndo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLogReadActionForUndo', maptype.HMAP, ctypes.POINTER(maptype.HSITE), ctypes.c_long)
    def mapLogReadActionForUndo(_hmap: maptype.HMAP, _hsite: ctypes.POINTER(maptype.HSITE), _flag: int) -> int:
        """
        Прочитать последнюю транзакцию в документе, которую можно отменить
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _flag: условия выбора последней транзакции: ``LOG_ANYACTION``(``0``) - нет условий, ``LOG_MYACTION``(``1``) - обрабатывать последнюю свою транзакцию (пропускать транзакции других пользователей)
        
        :returns: или журнал пуст - возвращает ноль При ошибке возвращает ноль, иначе - номер транзакции
        :rtype: int
        
        .. note::

           Если после транзакции выполнялась сортировка карты с удалением копий отредактированных объектов
        """
        return mapLogReadActionForUndo_t (_hmap, _hsite, _flag)

    mapLogFlush_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapLogFlush', maptype.HMAP, maptype.HSITE)
    def mapLogFlush(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> ctypes.c_void_p:
        """
        Сохранить журнал транзакций и переоткрыть файл
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        """
        return mapLogFlush_t (_hmap, _hsite)

    mapLogGetMyIdent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapLogGetMyIdent', maptype.HMAP, maptype.HSITE)
    def mapLogGetMyIdent(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить идентификатор текущего компьютера
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных Идентификатор текущего компьютера записывается в поле Task структуры ``ACTIONHEAD``
        
        :returns: Возвращает идентификатор текущего компьютера При ошибке возвращает ноль
        :rtype: int
        """
        return mapLogGetMyIdent_t (_hmap, _hsite)

    mapLogGetMyNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'mapLogGetMyNameUn', maptype.HMAP, maptype.HSITE)
    def mapLogGetMyNameUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> ctypes.POINTER(maptype.WCHAR):
        """
        Запросить имя текущего компьютера и пользователя
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных Имя текущего компьютера и пользователя записывается в структуре ``ACTIONHEAD``
        
        :returns: Возвращает имя текущего компьютера и пользователя При ошибке возвращает ноль
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return mapLogGetMyNameUn_t (_hmap, _hsite)

    mapSetExclusiveAccess_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetExclusiveAccess', ctypes.c_long)
    def mapSetExclusiveAccess(_access: int) -> int:
        """
        Установить монопольный доступ ко всем открываемым векторным картам
        
        :param _access: общий признак монопольного доступа (``0`` / ``1``) Ускоряет все операции редактирования карт за счет буферизации операций записи на диск при значении access не равном ``0`` При монопольном доступе другие приложения не смогут редактировать карту
        
        :returns: Возвращает новое значение признака монопольного доступа
        :rtype: int
        
        .. note::

           Если какая-либо карта не может быть открыта в монопольном доступе, то открывается с разделением доступа на запись
        """
        return mapSetExclusiveAccess_t (_access)


# Запросить значение общего признака монопольного доступа ко всем открываемым векторным картам
# Возвращает значение общего признака монопольного доступа ко всем открываемым векторным картам

#   mapGetExclusiveAccess_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetExclusiveAccess', )
#   def mapGetExclusiveAccess(_void) -> int:
#       return mapGetExclusiveAccess_t (_void)

    mapGetActionListEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapGetActionListEx', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.c_int)
    def mapGetActionListEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _number: int, _limit: int, _error: ctypes.POINTER(ctypes.c_long), _outype: int) -> ctypes.c_void_p:
        """
        Запросить список транзакций для заданной карты, начиная с указанного номера
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _number: номер транзакции, с которой начинается выдача
        
        :param _limit: предельное число выдаваемых записей или ``0`` (не ограничивать)
        
        :param _error: поле для записи кода ошибки, возникшей при запросе списка операций
        
        :param _outype: формат вывода ``OST_GML``/``OST_JSON`` Для чтения списка необходимо вызвать функцию mapGetActionListPoint, после чтения списка необходимо освободить память функцией mapFreeActionList
        
        :returns: Возвращает идентификатор списка записей в памяти в формате XML ``<?xml version=\\"1.0\\" encoding=\\"UTF-8\\" ?>`` ``<actionlist fromnumber="37591" date="27/05/2019" time="12:45:08">`` ``<action number="37591" kind="4009" user="user1">`` ``<item type="edit" object="1234567" data="true" sheet="2"/>`` ``<item type="edit" object="1237890" data="true" semn="true"/>`` ``</action>`` ``<action number="37594" kind="4001" user="user1">`` ``<item type="create" object="2345678" data="true" semn="true"/>`` ``</action>`` ``<action number="37599" kind="4003" user="user2">`` ``<item type="delete" object="2345678"/>`` ``</action>`` ``</actionlist>`` При ошибке возвращает ноль
        """
        return mapGetActionListEx_t (_hmap, _hsite, _number, _limit, _error, _outype)

    mapGetActionListPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_char_p,'mapGetActionListPoint', ctypes.c_void_p, ctypes.POINTER(ctypes.c_long))
    def mapGetActionListPoint(_actionlist: ctypes.c_void_p, _size: ctypes.POINTER(ctypes.c_long)) -> ctypes.c_char_p:
        """
        Запросить адрес сформированного списка транзакций для заданной карты и его размер для чтения
        
        :param _actionlist: адрес сформированного списка транзакций для заданной карты
        
        :param _size: размер сформированного списка
        
        :returns: При ошибке возвращает ноль
        :rtype: ctypes.c_char_p
        """
        return mapGetActionListPoint_t (_actionlist, _size)

    mapFreeActionList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeActionList', ctypes.c_void_p)
    def mapFreeActionList(_actionlist: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Удалить список транзакций в памяти
        """
        return mapFreeActionList_t (_actionlist)

    mapGetActionName_t = mapsyst.GetProcAddress(acceslib,maptype.PWCHAR,'mapGetActionName', ctypes.c_long, ctypes.c_long)
    def mapGetActionName(_type: int, _language: int) -> mapsyst.WTEXT:
        """
        Запросить название транзакции по типу
        
        :param _type: код транзакции (описание в maptype.h и transcod.rh)
        
        :param _language: код языка (описание ``MAPAPILANGUAGE`` в maptype.h) или ``0`` для выбора текущего языка интерфейса
        
        :returns: Если код языка ошибочный возвращает строку на английском языке Если код транзакции не известен возвращает текст ``"Транзакция"`` на запрошенном языке При ошибке возвращает строку ``" ? "``
        :rtype: mapsyst.WTEXT
        """
        return mapGetActionName_t (_type, _language)



TAC_MED_CREATEOBJECT = 4001
"""  Создание объекта"""
TAC_MED_UNDO         = 4002
"""  Отмена"""
TAC_MED_DELETEOBJECT = 4003
"""  Удаление объекта"""
TAC_MED_PASTE        = 4004
"""  Сшивка объектов"""
TAC_MED_MOVEKNOT     = 4005
"""  Перемещение узлов"""
TAC_MED_MOVEPART     = 4006
"""  Перемещение участка объекта"""
TAC_MED_EDITPART     = 4007
"""  Редактирование участка объекта"""
TAC_MED_LINECUT      = 4008
"""  Рассечение линейного объекта"""
TAC_MED_ADJUST       = 4009
"""  Согласование объектов"""
TAC_MED_SPLINE       = 4010
"""  Сглаживание объектов"""
TAC_MED_FILTER       = 4011
"""  Фильтрация объектов"""
TAC_MED_REVERT       = 4012
"""  Изменение направления"""
TAC_MED_CUT          = 4013
"""  Разрезание объекта"""
TAC_MED_POLYTITLE    = 4014
"""  Сборка сложной подписи"""
TAC_MED_SEMAPPEND    = 4015
"""  Добавление семантики"""
TAC_MED_SEMUPDATE    = 4016
"""  Обновление семантики"""
TAC_MED_SEMDELETE    = 4017
"""  Удаление семантики"""
TAC_MED_ROTATE       = 4018
"""  Вращение объекта"""
TAC_MED_MOVE         = 4019
"""  Перемещение объекта"""
TAC_MED_MODIFY       = 4020
"""  Изменение кода объекта"""
TAC_MED_HIGHT        = 4021
"""  Редактирование высоты"""
TAC_MED_TITLE        = 4022
"""  Редактирование текста"""
TAC_MED_BOTTOP       = 4023
"""  Изменение границ видимости"""
TAC_MED_MOVEROTATE   = 4024
"""  Масштабирование и поворот объектов"""
TAC_MED_SCENARIO     = 4025
"""  Создание сценария"""
TAC_MED_SCENEOBJECT  = 4026
"""  Создание/обновление объекта по сценарию"""
TAC_MED_DRAWEDIT     = 4027
"""  Редактирование графики объекта"""
TAC_MED_COPYSEEK     = 4028
"""  Копирование(перемещение) на другую карту"""
TAC_MED_DELONESUB    = 4029
"""  Удаление одного подобъекта"""
TAC_MED_DELALLSUB    = 4030
"""  Удаление всех подобъектов"""
TAC_MED_SEEKDELALSUB = 4031
"""  Удаление всех подобъектов у выделенных объектов"""
TAC_MED_DELSEEK      = 4032
"""  Удаление выделенных объектов"""
TAC_MED_SMOVE        = 4033
"""  Быстрое редактирование и удаление объектов"""
TAC_MED_POINTGROUP   = 4034
"""  Редактирование общих точек смежных объектов"""
TAC_MED_DELETEPOINT  = 4035
"""  Удаление точек"""
TAC_MED_ADDPOINT     = 4036
"""  Добавление точек"""
TAC_MED_LOCKOBJ      = 4037
"""  Замыкание объекта"""
TAC_MED_RECTANGLE    = 4039
"""  Приведение объектов к прямоугольному виду"""
TAC_MED_SETBEGIN     = 4040
"""  Установить первую точку метрики"""
TAC_MED_CHANGESEMCODE = 4041
"""  Изменение кода семантики"""
TAC_MED_LISTSEM      = 4042
"""  Редактирование семантики списком"""
TAC_MED_CALCVALUE    = 4043
"""  Расчёты по семантике"""
TAC_MED_CALCSTRING   = 4044
"""  Сборка символьной семантики"""
TAC_MED_SET_COLOR    = 4045
"""  Изменить цвет"""
TAC_MED_SET_SCALE    = 4046
"""  Масштабирование объекта"""
TAC_MED_COPYHIGHT    = 4047
"""  Копия значения абсолютной высоты"""
TAC_MED_DELETEHIGHT  = 4048
"""  Удаление высоты"""
TAC_MED_COPYPART     = 4049
"""  Копия участка объекта"""
TAC_MED_COPYSUB      = 4050
"""  Создание подобъекта"""
TAC_MED_SEEKSUBJECT  = 4051
"""  Создание подобъектов  по выделенным объектам"""
TAC_MED_CROSSPOINT   = 4052
"""  Создание точек пересечения выбранных объектов"""
TAC_MED_ADJUSPOINT   = 4053
"""  Согласование двух точек двух объектов"""
TAC_MED_ADJUSOBJECT  = 4054
"""  Согласование концов (сводка) линейных объектов """
TAC_MED_ADJLINEFRAME = 4055
"""  Сводка объектов по рамке"""
TAC_MED_KNOT         = 4056
"""  Формирование узла"""
TAC_MED_ADJSHORTPOINT = 4057
"""  Согласование точек"""
TAC_MED_CUTSET       = 4058
"""  Вырезание списков"""
TAC_MED_ADJSET       = 4059
"""  Согласование списков"""
TAC_MED_TOTALFILTR   = 4060
"""  Согласованная фильтрация объекта"""
TAC_MED_LINEPOINTCUT = 4061
"""  Рассечение в точке"""
TAC_MED_SQUARECUT    = 4062
"""  Рассечение площадного объекта объектом"""
TAC_MED_BUILDING     = 4063
"""  Составление кварталов"""
TAC_MED_SEEKLINECUT  = 4064
"""  Рассечение линейных объектов"""
TAC_MED_EXCAVAT      = 4065
"""  Насыпь (пропорционально)"""
TAC_MED_EMBANKMENT   = 4066
"""  Насыпь (перпендикулярно)"""
TAC_MED_PLATFORM     = 4067
"""  Создание объекта типа ЭСТАКАДА"""
TAC_MED_STAIRS       = 4068
"""  Оформление объекта типа ЛЕСТНИЦА"""
TAC_MED_ZIGZAG       = 4069
"""  Создание зигзагообразного объекта"""
TAC_MED_CREATECOPY   = 4070
"""  Создание по типу"""
TAC_MED_CREATESUB    = 4071
"""  Создание подобъекта"""
TAC_MED_COPY         = 4072
"""  Копия объекта"""
TAC_MED_CHOICEMAP    = 4073
"""  Копия на другую карту"""
TAC_MED_SAVEOBJECT   = 4074
"""  Создание по условному"""
TAC_MED_SIT_LINE     = 4075
"""  Нанесение линии"""
TAC_MED_SIT_SQUARE   = 4076
"""  Нанесение полигона"""
TAC_MED_SIT_POINT    = 4077
"""  Нанесение растрового знака"""
TAC_MED_SIT_TEXT     = 4078
"""  Нанесение подписи"""
TAC_MED_CRMODE0      = 4079
"""  Комбинированный метод"""
TAC_MED_LABELLINEFROMSEM = 4080
"""  Подпись линии по семантике"""
TAC_MED_LABELFROMSEM1    = 4081
"""  Подпись объекта по семантике(произвольный контур)"""
TAC_MED_LABELFROMSEM2    = 4082
"""  Подпись объекта по семантике(сглаживающий сплайн)"""
TAC_MED_LINECONTINUE = 4083
"""  Продолжение линии"""
TAC_MED_PARTMOVE     = 4084
"""  Перемещение участка"""
TAC_MED_TITLEMOVE    = 4085
"""  Редактирование составной подписи"""
TAC_MED_RESTORESEEK  = 4086
"""  Восстановление удаленных"""
TAC_MED_SEEKCODE     = 4087
"""  Перекодировка выделенных"""
TAC_MED_SEEKCROSS    = 4088
"""  Пересечение выделенных"""
TAC_MED_SEEKSPLINE   = 4089
"""  Сглаживание выделенных"""
TAC_MED_SEEKFILTER   = 4090
"""  Фильтрация выделенных"""
TAC_MED_SHAB         = 4092
"""  Нанесение из макета"""
TAC_MED_SEEKHIGHTADD = 4093
"""  Обновление высоты объекта из матрицы """
TAC_MED_HIGHTADD     = 4094
"""  Добавление высот"""
TAC_MED_STAFFCREATE  = 4095
"""  Нанесение КП"""
TAC_MED_BERGLINE     = 4096
"""  Бергштрих в точке"""
TAC_MED_DOUBLEBERGLINE = 4097
"""  Парные бергштрихи"""
TAC_MED_ADDOBJECTDRAW  = 4098
"""  Копия графики"""
TAC_MED_POSUPDATE      = 4099
"""  Изменить порядок отображения объекта в цепочке"""
TAC_MED_OUTBORDER      = 4100
"""  Общая граница"""
TAC_MED_EDITLINE       = 4101
"""  Редактирование линии"""
TAC_MED_GENSPLINE      = 4102
"""  Согласованное сглаживание"""
TAC_MED_ROTATESELECTED = 4199
"""  Привязка выделенных объектов"""
TAC_MED_UPDATEOBJECT   = 4200
"""  Обновление объекта"""
TAC_MED_AZIMUTHCIRCLE  = 4201
"""  Азимутальный круг"""
TAC_MED_EXPAND         = 4202
"""  Расширяющаяся зона"""
TAC_MED_COPYMETRIC     = 4203
"""  Копирование метрики"""
TAC_MED_DELETE4D       = 4204
"""  Удаление 4D"""


def logapi_healthcheck():
    return 1
