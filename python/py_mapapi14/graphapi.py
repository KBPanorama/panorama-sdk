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
    *           Интерфейсные функции доступа к графу сети              *
    *              импортируются из "mapacces"                         *
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
# Коды объектов карты графа

NODECODE       = 5558  # Excode узла
EDGECODE       = 5557  # Excode ребра
ONEWAYEDGECODE = 5562  # Excode ребра одностороннего
PARENTLISTCODE = 5555  # Excode рамки родительского листа

# Коды семантики

SEMNETROADTYPE = 1052  # Тип (класс) дороги

# Тип расчета кратчайшего пути, то есть пути с минимальным суммарным весом ребер

SP_LENGTH = 0  # По расстоянию - стоимость ребра равна длине ребра
SP_TIME   = 1  # По времени - стоимость ребра равна длине ребра, деленной на значение семантики

# Если для ребра семантика не задана, то скорость принимается = 60 км/час

SP_SEMCOST = 2  # По стоимости из семантики ребра "Стоимость ребра" (32819)

# Тип решения задачи коммивояжера

TSP_TOFIRST = 0  # Тур заканчивается в первом пункте (классическая постановка задачи)
TSP_TOLAST  = 1  # Тур заканчивается в последнем пункте


#-----------------------------
class OPENNETPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Wnd",maptype.HMESSAGE),
                ("ParentMap",maptype.HMAP),
                ("Reserve",ctypes.c_char*(128))]
#-----------------------------


#-----------------------------
class PATHPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Point1",maptype.DOUBLEPOINT),
                ("Point2",maptype.DOUBLEPOINT),
                ("Wnd",maptype.HMESSAGE),
                ("NodeKey1",ctypes.c_int),
                ("NodeKey2",ctypes.c_int),
                ("IsWgs",ctypes.c_int),
                ("Type",ctypes.c_int),
                ("IsUturn",ctypes.c_int),
                ("UseRoadCount",ctypes.c_int),
                ("UseRoads",ctypes.POINTER(ctypes.c_int)),
                ("UseSelect",maptype.HSELECT),
                ("BanSelect",maptype.HSELECT),
                ("Reserve",ctypes.c_char*(128))]
#-----------------------------


#-----------------------------
class DISTGRAPHPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Dist",ctypes.c_double),
                ("Wnd",maptype.HMESSAGE),
                ("NodeKey",ctypes.c_int),
                ("Type",ctypes.c_int),
                ("IsUturn",ctypes.c_int),
                ("UseRoadCount",ctypes.c_int),
                ("UseRoads",ctypes.POINTER(ctypes.c_int)),
                ("UseSelect",maptype.HSELECT),
                ("BanSelect",maptype.HSELECT),
                ("Reserve",ctypes.c_char*(128))]
#-----------------------------


#-----------------------------
class TSPPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Wnd",maptype.HMESSAGE),
                ("PointCount",ctypes.c_int),
                ("Points",ctypes.POINTER(maptype.DOUBLEPOINT)),
                ("CalcType",ctypes.c_int),
                ("IsWgs",ctypes.c_int),
                ("Type",ctypes.c_int),
                ("IsUturn",ctypes.c_int),
                ("UseRoadCount",ctypes.c_int),
                ("UseRoads",ctypes.POINTER(ctypes.c_int)),
                ("UseSelect",maptype.HSELECT),
                ("BanSelect",maptype.HSELECT),
                ("Reserve",ctypes.c_char*(128))]
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
    onOpenNetEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'onOpenNetEx', maptype.HMAP, maptype.HSITE, ctypes.POINTER(OPENNETPARM))
    def onOpenNetEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _parm: ctypes.POINTER(OPENNETPARM)) -> ctypes.c_void_p:
        """
        Открыть граф сети
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _parm: параметры открытия графа
        
        :returns: Возвращает идентификатор открытого графа При ошибке возвращает 0
        """
        return onOpenNetEx_t (_hmap, _hsite, _parm)

    onOpenNet_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'onOpenNet', maptype.PWCHAR, ctypes.POINTER(OPENNETPARM))
    def onOpenNet(_mapname: mapsyst.WTEXT, _parm: ctypes.POINTER(OPENNETPARM)) -> ctypes.c_void_p:
        """
        Открыть граф сети по имени карты графа
        
        :param _mapname: имя карты графа
        
        :param _parm: параметры открытия графа
        
        :returns: Возвращает идентификатор открытого графа При ошибке возвращает 0
        """
        return onOpenNet_t (_mapname.buffer(), _parm)

    onCloseNet_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'onCloseNet', ctypes.c_void_p)
    def onCloseNet(_hnet: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Закрыть граф сети
        
        :param _hnet: идентификатор графа сети, полученный onOpenNet
        """
        return onCloseNet_t (_hnet)

    onCloseNetByName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'onCloseNetByName', maptype.PWCHAR)
    def onCloseNetByName(_mapname: mapsyst.WTEXT) -> ctypes.c_void_p:
        """
        Закрыть граф сети по имени файла карты графа
        
        :param _mapname: имя файла карты графа
        """
        return onCloseNetByName_t (_mapname.buffer())

    onGetHMAP_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'onGetHMAP', ctypes.c_void_p)
    def onGetHMAP(_hnet: ctypes.c_void_p) -> maptype.HMAP:
        """
        Запросить идентификатор открытой карты графа
        
        :param _hnet: идентификатор графа сети, полученный onOpenNet
        
        :returns: Возвращает идентификатор открытой карты графа
        :rtype: maptype.HMAP
        """
        return onGetHMAP_t (_hnet)

    onGetHSITE_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'onGetHSITE', ctypes.c_void_p)
    def onGetHSITE(_hnet: ctypes.c_void_p) -> maptype.HSITE:
        """
        Запросить идентификатор векторной карты в открытых данных
        
        :param _hnet: идентификатор графа сети, полученный onOpenNet
        
        :returns: Возвращает идентификатор векторной карты в открытых данных графа
        :rtype: maptype.HSITE
        """
        return onGetHSITE_t (_hnet)

    onGetParentMap_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'onGetParentMap', ctypes.c_void_p)
    def onGetParentMap(_hnet: ctypes.c_void_p) -> maptype.HMAP:
        """
        Запросить документ, в котором открыты карты, по которым построен граф
        
        :param _hnet: идентификатор графа сети, полученный onOpenNet
        
        :returns: Возвращает поле ParentMap структуры OPENNETPARM, переданной при открытии графа
        :rtype: maptype.HMAP
        """
        return onGetParentMap_t (_hnet)

    onGetParentRoadTypeCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetParentRoadTypeCount', ctypes.c_void_p)
    def onGetParentRoadTypeCount(_hnet: ctypes.c_void_p) -> int:
        """
        Запросить количество типов дорог, участвующих в построении карты графа
        
        :param _hnet: идентификатор графа сети, полученный onOpenNet Тип дороги - значение семантики ``SEMNETROADTYPE`` в ребрах графа
        
        :returns: Возвращает количество типов дорог, участвующих в построении карты графа При ошибке возвращает 0
        :rtype: int
        """
        return onGetParentRoadTypeCount_t (_hnet)

    onGetParentRoadTypeName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetParentRoadTypeName', ctypes.c_void_p, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def onGetParentRoadTypeName(_hnet: ctypes.c_void_p, _number: int, _name: mapsyst.WTEXT, _namesize: int) -> int:
        """
        Запросить имя типа дороги, участвовавшей в построении графа
        
        :param _hnet: идентификатор графа сети, полученный onOpenNet
        
        :param _number: порядковый номер типа дороги (от ``0``)
        
        :param _name: имя типа дороги, участвовавшей в построении графа
        
        :param _namesize: размер name в байтах Тип дороги - значение семантики ``SEMNETROADTYPE`` в ребрах графа
        
        :returns: Возвращает имя типа дороги, участвовавшей в построении графа При ошибке возвращает 0
        :rtype: int
        """
        return onGetParentRoadTypeName_t (_hnet, _number, _name.buffer(), _namesize)

    onFindNearPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onFindNearPoint', ctypes.c_void_p, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    def onFindNearPoint(_hnet: ctypes.c_void_p, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _nearpoint: ctypes.POINTER(maptype.DOUBLEPOINT), _key: ctypes.POINTER(ctypes.c_int), _isnearedge: ctypes.POINTER(ctypes.c_int)) -> int:
        """
        Найти ближайший узел или точку на ребре
        
        :param _hnet: идентификатор графа сети, полученный onOpenNet
        
        :param _point: исходная точка на карте
        
        :param _nearpoint: координаты точки сети, ближайшей к исходной
        
        :returns: key        - возвращает уникальный номер ближайшего элемента (ребра или узла сети) isnearedge - возвращает признак ближайшего элемента (``1`` - ребро, ``0`` - узел) (если указатель isnearedge ``= 0``, то ищет только узлы) Возвращает номер сети, на которой найдена ближайшая точка При ошибке возвращает 0
        :rtype: int
        """
        return onFindNearPoint_t (_hnet, _point, _nearpoint, _key, _isnearedge)

    onCreatePath_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'onCreatePath', ctypes.c_void_p, ctypes.POINTER(PATHPARM))
    def onCreatePath(_hnet: ctypes.c_void_p, _parm: ctypes.POINTER(PATHPARM)) -> ctypes.c_void_p:
        """
        Построить кратчайший маршрут по графу дорог
        
        :param _hnet: идентификатор графа сети, полученный onOpenNet
        
        :param _parm: параметры определения маршрута Чтобы отобрать разрешенные ребра для построения маршрута и/или исключить отдельные ребра из построения маршрута необходимо в структуре ``PATHPARM`` установить условия отбора ``HSELECT`` (UseSelect и/или BanSelect)
        
        :returns: Возвращает идентификатор маршрута При ошибке возвращает 0
        """
        return onCreatePath_t (_hnet, _parm)

    onFreePath_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'onFreePath', ctypes.c_void_p)
    def onFreePath(_hpath: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Удалить маршрут
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        """
        return onFreePath_t (_hpath)

    onGetPathTime_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'onGetPathTime', ctypes.c_void_p)
    def onGetPathTime(_hpath: ctypes.c_void_p) -> float:
        """
        Запросить время проезда по всему маршруту в часах
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :returns: Возвращает время проезда по всему маршруту в часах При ошибке возвращает 0
        :rtype: float
        """
        return onGetPathTime_t (_hpath)

    onGetPathLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'onGetPathLength', ctypes.c_void_p)
    def onGetPathLength(_hpath: ctypes.c_void_p) -> float:
        """
        Вычислить длину всего маршрута в метрах
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :returns: Возвращает длину всего маршрута в метрах При ошибке возвращает 0
        :rtype: float
        """
        return onGetPathLength_t (_hpath)

    onGetPathCost_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'onGetPathCost', ctypes.c_void_p)
    def onGetPathCost(_hpath: ctypes.c_void_p) -> float:
        """
        Запросить стоимость всего маршрута
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :returns: Возвращает стоимость всего маршрута При ошибке возвращает 0
        :rtype: float
        """
        return onGetPathCost_t (_hpath)

    onGetPathEdgeCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetPathEdgeCount', ctypes.c_void_p)
    def onGetPathEdgeCount(_hpath: ctypes.c_void_p) -> int:
        """
        Запросить количество ребер в маршруте
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :returns: Возвращает количество ребер в маршруте При ошибке возвращает 0
        :rtype: int
        """
        return onGetPathEdgeCount_t (_hpath)

    onGetPathEdgeKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetPathEdgeKey', ctypes.c_void_p, ctypes.c_long)
    def onGetPathEdgeKey(_hpath: ctypes.c_void_p, _number: int) -> int:
        """
        Запросить уникальный номер ребра маршрута на карте графа
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :param _number: номер ребра в маршруте (от ``0`` до onGetPathEdgeCount - ``1``)
        
        :returns: Возвращает уникальный номер ребра маршрута на карте графа При ошибке возвращает 0
        :rtype: int
        """
        return onGetPathEdgeKey_t (_hpath, _number)

    onGetPathEdgeNum_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetPathEdgeNum', ctypes.c_void_p, ctypes.c_long)
    def onGetPathEdgeNum(_hpath: ctypes.c_void_p, _number: int) -> int:
        """
        Запросить номер объекта ребра маршрута на карте графа
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :param _number: номер ребра в маршруте (от ``0`` до onGetPathEdgeCount - ``1``)
        
        :returns: Возвращает номер объекта ребра маршрута на карте графа При ошибке возвращает 0
        :rtype: int
        """
        return onGetPathEdgeNum_t (_hpath, _number)

    onGetPathParentEdgeType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetPathParentEdgeType', ctypes.c_void_p, ctypes.c_long)
    def onGetPathParentEdgeType(_hpath: ctypes.c_void_p, _number: int) -> int:
        """
        Запросить номер типа дороги ребра маршрута в списке типов дорог, участвовавших в построении карты графа
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :param _number: номер ребра в маршруте (от ``0`` до onGetPathEdgeCount - ``1``) Для получения имени типа дороги используйте onGetParentRoadTypeName
        
        :returns: Возвращает номер типа дороги ребра маршрута в списке типов дорог, участвовавших в построении карты графа При ошибке возвращает -1
        :rtype: int
        """
        return onGetPathParentEdgeType_t (_hpath, _number)

    onGetPathParentEdgeSite_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'onGetPathParentEdgeSite', ctypes.c_void_p, ctypes.c_long)
    def onGetPathParentEdgeSite(_hpath: ctypes.c_void_p, _number: int) -> maptype.HSITE:
        """
        Запросить идентификатор карты, по объекту которой построено ребро маршрута при создании карты графа
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :param _number: номер ребра в маршруте (от ``0`` до onGetPathEdgeCount - ``1``) Для работы функции необходимо чтобы: - карта графа была построена с флагом ``"Сохранять связь с объектами исходной карты"`` - при открытии графа указан документ ParentMap, в котором открыты карты, по которым построен граф
        
        :returns: Возвращает идентификатор карты, по объекту которой построено ребро маршрута при создании карты графа При ошибке возвращает 0
        :rtype: maptype.HSITE
        """
        return onGetPathParentEdgeSite_t (_hpath, _number)

    onGetPathParentEdgeSheetNum_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetPathParentEdgeSheetNum', ctypes.c_void_p, ctypes.c_long)
    def onGetPathParentEdgeSheetNum(_hpath: ctypes.c_void_p, _number: int) -> int:
        """
        Запросить номер листа карты, по объекту которой построено ребро маршрута при создании карты графа
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :param _number: номер ребра в маршруте (от ``0`` до onGetPathEdgeCount - ``1``) Для работы функции необходимо чтобы: - карта графа была построена с флагом ``"Сохранять связь с объектами исходной карты"`` - при открытии графа указан документ ParentMap, в котором открыты карты, по которым построен граф
        
        :returns: Возвращает номер листа карты, по объекту которой построено ребро маршрута при создании карты графа При ошибке возвращает 0
        :rtype: int
        """
        return onGetPathParentEdgeSheetNum_t (_hpath, _number)

    onGetPathParentEdgeKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetPathParentEdgeKey', ctypes.c_void_p, ctypes.c_long)
    def onGetPathParentEdgeKey(_hpath: ctypes.c_void_p, _number: int) -> int:
        """
        Запросить уникальный номер объекта по которому построено ребро маршрута при создании карты графа
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :param _number: номер ребра в маршруте (от ``0`` до onGetPathEdgeCount - ``1``) Для работы функции необходимо чтобы карта графа была построена с флагом ``"Сохранять связь с объектами исходной карты"``
        
        :returns: Возвращает уникальный номер объекта по которому построено ребро маршрута при создании карты графа При ошибке возвращает 0
        :rtype: int
        """
        return onGetPathParentEdgeKey_t (_hpath, _number)

    onGetPathParentEdgeObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetPathParentEdgeObject', ctypes.c_void_p, ctypes.c_long, maptype.HOBJ)
    def onGetPathParentEdgeObject(_hpath: ctypes.c_void_p, _number: int, _hobj: maptype.HOBJ) -> int:
        """
        Запросить объект из которого нарезано ребро маршрута при создании карты графа
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :param _number: номер ребра в маршруте (от ``0`` до onGetPathEdgeCount - ``1``)
        
        :param _hobj: идентификатор, в который будет считан родительский объект Для работы функции необходимо чтобы: - карта графа была построена с флагом ``"Сохранять связь с объектами исходной карты"`` - при открытии графа указан документ ParentMap, в котором открыты карты, по которым построен граф
        
        :returns: Возвращает объект из которого нарезано ребро маршрута при создании карты графа При ошибке возвращает 0
        :rtype: int
        """
        return onGetPathParentEdgeObject_t (_hpath, _number, _hobj)

    onGetPathEdgeLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'onGetPathEdgeLength', ctypes.c_void_p, ctypes.c_long)
    def onGetPathEdgeLength(_hpath: ctypes.c_void_p, _number: int) -> float:
        """
        Запросить длину ребра маршрута по порядковому номеру ребра в маршруте в метрах
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :param _number: номер ребра в маршруте (от ``0`` до onGetPathEdgeCount - ``1``)
        
        :returns: Возвращает длину ребра маршрута по порядковому номеру ребра в маршруте в метрах При ошибке возвращает 0
        :rtype: float
        """
        return onGetPathEdgeLength_t (_hpath, _number)

    onGetPathEdgeTime_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'onGetPathEdgeTime', ctypes.c_void_p, ctypes.c_long)
    def onGetPathEdgeTime(_hpath: ctypes.c_void_p, _number: int) -> float:
        """
        Запросить время проезда ребра маршрута по порядковому номеру ребра в маршруте в часах
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :param _number: номер ребра в маршруте (от ``0`` до onGetPathEdgeCount - ``1``)
        
        :returns: Возвращает время проезда ребра маршрута по порядковому номеру ребра в маршруте в часах При ошибке возвращает 0
        :rtype: float
        """
        return onGetPathEdgeTime_t (_hpath, _number)

    onGetPathEdgeCost_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'onGetPathEdgeCost', ctypes.c_void_p, ctypes.c_long)
    def onGetPathEdgeCost(_hpath: ctypes.c_void_p, _number: int) -> float:
        """
        Запросить стоимость ребра маршрута по порядковому номеру ребра в маршруте
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :param _number: номер ребра в маршруте (от ``0`` до onGetPathEdgeCount - ``1``)
        
        :returns: Возвращает стоимость ребра маршрута по порядковому номеру ребра в маршруте При ошибке возвращает 0
        :rtype: float
        """
        return onGetPathEdgeCost_t (_hpath, _number)

    onGetPathEdgeFirstPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetPathEdgeFirstPoint', ctypes.c_void_p, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT))
    def onGetPathEdgeFirstPoint(_hpath: ctypes.c_void_p, _number: int, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Запросить координаты первой точки ребра маршрута
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :param _number: номер ребра в маршруте (от ``0`` до onGetPathEdgeCount - ``1``)
        
        :param _point: возвращаемые координаты первой точки ребра маршрута
        
        :returns: Возвращает координаты первой точки ребра маршрута При ошибке возвращает 0
        :rtype: int
        
        .. note::

           Если маршрут создавался onCreatePath, onCreatePathEx, то возвращаемые координаты
           в системе координат карты графа
           Если маршрут создавался onCreatePathWgs, onCreatePathWgsEx, то возвращаемые координаты-
           широта, долгота в радианах на WGS84
        """
        return onGetPathEdgeFirstPoint_t (_hpath, _number, _point)

    onGetPathEdgeLastPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetPathEdgeLastPoint', ctypes.c_void_p, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT))
    def onGetPathEdgeLastPoint(_hpath: ctypes.c_void_p, _number: int, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Запросить координаты последней точки ребра маршрута
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :param _number: номер ребра в маршруте (от ``0`` до onGetPathEdgeCount - ``1``)
        
        :param _point: возвращаемые координаты последней точки ребра маршрута
        
        :returns: Возвращает координаты последней точки ребра маршрута При ошибке возвращает 0
        :rtype: int
        
        .. note::

           Если маршрут создавался onCreatePath, onCreatePathEx, то возвращаемые координаты
           в системе координат карты графа
           Если маршрут создавался onCreatePathWgs, onCreatePathWgsEx, то возвращаемые координаты-
           широта, долгота в радианах на WGS84
        """
        return onGetPathEdgeLastPoint_t (_hpath, _number, _point)

    onGetPathEdgeLastPointAngle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetPathEdgeLastPointAngle', ctypes.c_void_p, ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def onGetPathEdgeLastPointAngle(_hpath: ctypes.c_void_p, _number: int, _angle: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить угол поворота на последней точке ребра маршрута
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :param _number: номер ребра в маршруте (от ``0`` до onGetPathEdgeCount - ``2``, НА ПОСЛЕДНЕМ РЕБРЕ НЕТ ПОВОРОТА)
        
        :param _angle: возвращаемый угол поворота на последней точке ребра маршрута
        
        :returns: Возвращает угол поворота на последней точке ребра маршрута При ошибке возвращает 0
        :rtype: int
        """
        return onGetPathEdgeLastPointAngle_t (_hpath, _number, _angle)

    onGetPathEdgeFirstPointAngle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetPathEdgeFirstPointAngle', ctypes.c_void_p, ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def onGetPathEdgeFirstPointAngle(_hpath: ctypes.c_void_p, _number: int, _angle: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить угол поворота на первой точке ребра маршрута
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :param _number: номер ребра в маршруте (от ``1`` до onGetPathEdgeCount - ``1``, НА ПЕРВОМ РЕБРЕ НЕТ ПОВОРОТА)
        
        :param _angle: возвращаемый угол поворота на первой точке ребра маршрута
        
        :returns: Возвращает угол поворота на первой точке ребра маршрута При ошибке возвращает 0
        :rtype: int
        """
        return onGetPathEdgeFirstPointAngle_t (_hpath, _number, _angle)

    onGetPathEdgeFirstSegmentDir_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetPathEdgeFirstSegmentDir', ctypes.c_void_p, ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def onGetPathEdgeFirstSegmentDir(_hpath: ctypes.c_void_p, _number: int, _dir: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить дирекционный угол первого отрезка ребра маршрута
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :param _number: номер ребра в маршруте (от ``0`` до onGetPathEdgeCount - ``1``)
        
        :param _dir: возвращаемый дирекционный угол (угол на первой точке между направлением на север и на вторую точку против часовой стрелки)
        
        :returns: Возвращает дирекционный угол первого отрезка ребра маршрута При ошибке возвращает 0
        :rtype: int
        """
        return onGetPathEdgeFirstSegmentDir_t (_hpath, _number, _dir)

    onGetPathEdgeLastSegmentDir_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetPathEdgeLastSegmentDir', ctypes.c_void_p, ctypes.c_long, ctypes.POINTER(ctypes.c_double))
    def onGetPathEdgeLastSegmentDir(_hpath: ctypes.c_void_p, _number: int, _dir: ctypes.POINTER(ctypes.c_double)) -> int:
        """
        Запросить дирекционный угол последнего отрезка ребра маршрута
        
        (угол на последней точке между направлением на север и на предпоследнюю точку против часовой стрелки)
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :param _number: номер ребра в маршруте (от ``0`` до onGetPathEdgeCount - ``1``)
        
        :param _dir: возвращаемый дирекционный угол (угол на последней точке между направлением на север и на предпоследнюю точку против часовой стрелки)
        
        :returns: Возвращает дирекционный угол последнего отрезка ребра маршрута При ошибке возвращает 0
        :rtype: int
        """
        return onGetPathEdgeLastSegmentDir_t (_hpath, _number, _dir)

    onGetPathNodeCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetPathNodeCount', ctypes.c_void_p)
    def onGetPathNodeCount(_hpath: ctypes.c_void_p) -> int:
        """
        Запросить количество узлов в маршруте (= количество ПОЛНЫХ ребер + 1)
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :returns: Возвращает количество узлов в маршруте (= количество ПОЛНЫХ ребер + 1) При ошибке возвращает 0
        :rtype: int
        """
        return onGetPathNodeCount_t (_hpath)

    onGetPathNodeKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetPathNodeKey', ctypes.c_void_p, ctypes.c_long)
    def onGetPathNodeKey(_hpath: ctypes.c_void_p, _number: int) -> int:
        """
        Запросить уникальный номер узла маршрута на карте графа
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :param _number: номер ребра в маршруте (от ``0`` до onGetPathNodeCount - ``1``)
        
        :returns: Возвращает уникальный номер узла маршрута на карте графа При ошибке возвращает 0
        :rtype: int
        """
        return onGetPathNodeKey_t (_hpath, _number)

    onGetPathNodeNum_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetPathNodeNum', ctypes.c_void_p, ctypes.c_long)
    def onGetPathNodeNum(_hpath: ctypes.c_void_p, _number: int) -> int:
        """
        Запросить номер объекта узла маршрута на карте графа
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :param _number: номер ребра в маршруте (от ``0`` до onGetPathNodeCount - ``1``)
        
        :returns: Возвращает номер объекта узла маршрута на карте графа При ошибке возвращает 0
        :rtype: int
        """
        return onGetPathNodeNum_t (_hpath, _number)

    onGetPathObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetPathObject', ctypes.c_void_p, maptype.HOBJ)
    def onGetPathObject(_hpath: ctypes.c_void_p, _hobj: maptype.HOBJ) -> int:
        """
        Записать в объект метрику маршрута
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :param _hobj: объект, в который записывается метрика маршрута
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return onGetPathObject_t (_hpath, _hobj)

    onGetPathSubject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetPathSubject', ctypes.c_void_p, maptype.HOBJ, ctypes.c_long)
    def onGetPathSubject(_hpath: ctypes.c_void_p, _hobj: maptype.HOBJ, _subject: int) -> int:
        """
        Записать в объект метрику маршрута
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :param _hobj: объект, в который записывается метрика маршрута
        
        :param _subject: номер подобъекта, в который записывается метрика маршрута
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return onGetPathSubject_t (_hpath, _hobj, _subject)

    onGetPathPointCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetPathPointCount', ctypes.c_void_p)
    def onGetPathPointCount(_hpath: ctypes.c_void_p) -> int:
        """
        Запросить количество точек в маршруте
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :returns: Возвращает количество точек в маршруте При ошибке возвращает 0
        :rtype: int
        """
        return onGetPathPointCount_t (_hpath)

    onGetPathPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetPathPoint', ctypes.c_void_p, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT))
    def onGetPathPoint(_hpath: ctypes.c_void_p, _number: int, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Запросить координаты точки маршрута по порядковому номеру в маршруте
        
        :param _hpath: идентификатор маршрута, полученный onCreatePath
        
        :param _number: номер точки в маршруте (от ``0`` до onGetPathPointCount - ``1``)
        
        :param _point: возвращаемые координтаы точки маршрута
        
        :returns: Возвращает координаты точки маршрута по порядковому номеру в маршруте При ошибке возвращает 0
        :rtype: int
        
        .. note::

           Если маршрут создавался onCreatePath, onCreatePathEx, то возвращаемые координаты
           в системе координат карты графа
           Если маршрут создавался onCreatePathWgs, onCreatePathWgsEx, то возвращаемые координаты-
           широта, долгота в радианах на WGS84
        """
        return onGetPathPoint_t (_hpath, _number, _point)

    onCreateDistGraph_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'onCreateDistGraph', ctypes.c_void_p, ctypes.POINTER(DISTGRAPHPARM))
    def onCreateDistGraph(_hnet: ctypes.c_void_p, _parm: ctypes.POINTER(DISTGRAPHPARM)) -> ctypes.c_void_p:
        """
        Создать граф удаленности
        
        :param _hnet: идентификатор графа сети
        
        :param _parm: параметры построения графа удаленности
        
        :returns: Возвращает идентификатор графа удаленности При ошибке возвращает 0
        """
        return onCreateDistGraph_t (_hnet, _parm)

    onFreeDistGraph_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'onFreeDistGraph', ctypes.c_void_p)
    def onFreeDistGraph(_hdgr: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Удалить граф удаленности
        
        :param _hdgr: идентификатор графа удаленности
        """
        return onFreeDistGraph_t (_hdgr)

    onGetDistGraphEdgeCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetDistGraphEdgeCount', ctypes.c_void_p)
    def onGetDistGraphEdgeCount(_hdgr: ctypes.c_void_p) -> int:
        """
        Запросить количество ребер в графе удаленности
        
        :param _hdgr: идентификатор графа удаленности
        
        :returns: Возвращает количество ребер в графе удаленности При ошибке возвращает 0
        :rtype: int
        """
        return onGetDistGraphEdgeCount_t (_hdgr)

    onGetDistGraphEdgeKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetDistGraphEdgeKey', ctypes.c_void_p, ctypes.c_long)
    def onGetDistGraphEdgeKey(_hdgr: ctypes.c_void_p, _number: int) -> int:
        """
        Запросить уникальный номер ребра графа удаленности на карте графа
        
        :param _hdgr: идентификатор графа удаленности
        
        :param _number: номер ребра в графе удаленности (от ``0`` до onGetDistGraphEdgeCount - ``1``)
        
        :returns: Возвращает уникальный номер ребра графа удаленности на карте графа При ошибке возвращает 0
        :rtype: int
        """
        return onGetDistGraphEdgeKey_t (_hdgr, _number)

    onGetDistGraphEdgeNum_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetDistGraphEdgeNum', ctypes.c_void_p, ctypes.c_long)
    def onGetDistGraphEdgeNum(_hdgr: ctypes.c_void_p, _number: int) -> int:
        """
        Запросить номер объекта ребра графа удаленности на карте графа
        
        :param _hdgr: идентификатор графа удаленности
        
        :param _number: номер ребра в графе удаленности (от ``0`` до onGetDistGraphEdgeCount - ``1``)
        
        :returns: Возвращает номер объекта ребра графа удаленности на карте графа При ошибке возвращает 0
        :rtype: int
        """
        return onGetDistGraphEdgeNum_t (_hdgr, _number)

    onCreateTSP_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'onCreateTSP', ctypes.c_void_p, ctypes.POINTER(TSPPARM))
    def onCreateTSP(_hnet: ctypes.c_void_p, _parm: ctypes.POINTER(TSPPARM)) -> ctypes.c_void_p:
        """
        Создать тур проходящий через несколько точек (задача коммивояжера)
        
        :param _hnet: идентификатор графа сети
        
        :param _parm: параметры построения графа удаленности
        
        :returns: Возвращает идентификатор задачи коммивояжера При ошибке возвращает 0
        """
        return onCreateTSP_t (_hnet, _parm)

    onFreeTSP_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'onFreeTSP', ctypes.c_void_p)
    def onFreeTSP(_htsp: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Удалить задачу коммивояжера
        
        :param _htsp: идентификатор задачи коммивояжера
        """
        return onFreeTSP_t (_htsp)

    onGetTSPPathCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetTSPPathCount', ctypes.c_void_p)
    def onGetTSPPathCount(_htsp: ctypes.c_void_p) -> int:
        """
        Запросить количество маршрутов в туре
        
        :param _htsp: идентификатор задачи коммивояжера
        
        :returns: Возвращает количество маршрутов в туре
        :rtype: int
        """
        return onGetTSPPathCount_t (_htsp)

    onGetTSPPath_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'onGetTSPPath', ctypes.c_void_p, ctypes.c_long)
    def onGetTSPPath(_htsp: ctypes.c_void_p, _pathnum: int) -> ctypes.c_void_p:
        """
        Запросить маршрут между парой пунктов в туре
        
        :param _htsp: идентификатор задачи коммивояжера
        
        :param _pathnum: номер маршрута в туре (от ``0``) Освобождать ``HPATH`` не надо, это делается автоматически в onFreeTSP
        
        :returns: Возвращает маршрут между парой пунктов в туре При ошибке возвращает 0
        """
        return onGetTSPPath_t (_htsp, _pathnum)

    onGetTSPPathFirstPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetTSPPathFirstPoint', ctypes.c_void_p, ctypes.c_long)
    def onGetTSPPathFirstPoint(_htsp: ctypes.c_void_p, _pathnum: int) -> int:
        """
        Запросить номер пункта в начале маршрута (от 0)
        
        :param _htsp: идентификатор задачи коммивояжера
        
        :param _pathnum: номер маршрута в туре (от ``0``)
        
        :returns: Возвращает номер пункта в начале маршрута (от 0) При ошибке возвращает -1
        :rtype: int
        """
        return onGetTSPPathFirstPoint_t (_htsp, _pathnum)

    onGetTSPPathLastPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'onGetTSPPathLastPoint', ctypes.c_void_p, ctypes.c_long)
    def onGetTSPPathLastPoint(_htsp: ctypes.c_void_p, _pathnum: int) -> int:
        """
        Запросить номер пункта в конце маршрута
        
        :param _htsp: идентификатор задачи коммивояжера
        
        :param _pathnum: номер маршрута в туре (от ``0``)
        
        :returns: Возвращает номер пункта в конце маршрута При ошибке возвращает -1
        :rtype: int
        """
        return onGetTSPPathLastPoint_t (_htsp, _pathnum)



def graphapi_healthcheck():
    return 1
