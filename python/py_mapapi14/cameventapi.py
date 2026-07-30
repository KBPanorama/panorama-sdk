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
    *      API-функции для передачи во внешние скрипты информации      *
    *               о событиях, принятых от камеры                     *
    *                                                                  *
    ********************************************************************
    
"""

import os
import ctypes
import mapsyst
import maptype
import mapcreat
import mapgdi
import camtype

PACK_WIDTH = 1



try:
    if os.environ['gisvideodll']:
        gisvideoname = os.environ['gisvideodll']
except KeyError:
    gisvideoname = 'gis64video.dll'

try:
    videolib = mapsyst.LoadLibrary(gisvideoname)
except Exception as e:
    print(e)
    videolib = 0

if videolib == 0:
    print(gisvideoname)
else:
    camCreateEventDescriptor_t = mapsyst.GetProcAddress(videolib,camtype.HCAMEVENT,'camCreateEventDescriptor', camtype.HCAM, maptype.HOBJ, ctypes.POINTER(camtype.CAMERAEVENT))
    def camCreateEventDescriptor(_hcam: camtype.HCAM, _hobj: maptype.HOBJ, _message: ctypes.POINTER(camtype.CAMERAEVENT)) -> camtype.HCAMEVENT:
        """
        Создать объект для передачи информации о возникшем событии во внешний скрипт
        
        :param _hcam: идентификатор объекта для управления ``IP``-камерой
        
        :param _hobj: идентификатор объекта карты, к которому привязана ``IP``-камера
        
        :param _message: адрес структуры с описанием события
        
        :returns: В случае успеха возвращает идентификатор созданного объекта При ошибке возвращает 0
        :rtype: camtype.HCAMEVENT
        """
        return camCreateEventDescriptor_t (_hcam, _hobj, _message)

    camDeleteEventDescriptor_t = mapsyst.GetProcAddress(videolib,ctypes.c_void_p,'camDeleteEventDescriptor', camtype.HCAMEVENT)
    def camDeleteEventDescriptor(_hevent: camtype.HCAMEVENT) -> ctypes.c_void_p:
        """
        Удалить объект для передачи информации о возникшем событии
        
        :param _hevent: идентификатор объекта с описанием события
        """
        return camDeleteEventDescriptor_t (_hevent)

    camGetSnapshotByEvent_t = mapsyst.GetProcAddress(videolib,ctypes.c_long,'camGetSnapshotByEvent', camtype.HCAMEVENT, maptype.PWCHAR, ctypes.c_long)
    def camGetSnapshotByEvent(_hevent: camtype.HCAMEVENT, _path: mapsyst.WTEXT, _pathsize: int) -> int:
        """
        Запросить скриншот с камеры
        
        :param _hevent: идентификатор объекта с описанием события
        
        :param _path: адрес строки для возврата пути к файлу со скриншотом в формате ``JPEG``
        
        :param _pathsize: размер строки для возврата пути к файлу скриншота в байтах При повторном вызове обновляет изображение в файле
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return camGetSnapshotByEvent_t (_hevent, _path.buffer(), _pathsize)

    camGetEventMessageUn_t = mapsyst.GetProcAddress(videolib,ctypes.c_long,'camGetEventMessageUn', camtype.HCAMEVENT, maptype.PWCHAR, ctypes.c_long)
    def camGetEventMessageUn(_hevent: camtype.HCAMEVENT, _message: mapsyst.WTEXT, _messagesize: int) -> int:
        """
        Запросить текстовое описание события
        
        :param _hevent: идентификатор объекта с описанием события
        
        :param _message: адрес строки для возврата описания события
        
        :param _messagesize: размер выделенного буфера в байтах Формат описания события: ``"ГГГГ-ММ-ДД ЧЧ:ММ:СС, Тема уведомления, Данные"``
        
        :returns: В случае успеха возвращает текстовое описание события Время возникновения события указывается во временной зоне камеры При ошибке возвращает 0
        :rtype: int
        """
        return camGetEventMessageUn_t (_hevent, _message.buffer(), _messagesize)

    camGetEventStucture_t = mapsyst.GetProcAddress(videolib,ctypes.c_long,'camGetEventStucture', camtype.HCAMEVENT, ctypes.POINTER(camtype.CAMERAEVENT))
    def camGetEventStucture(_hevent: camtype.HCAMEVENT, _message: ctypes.POINTER(camtype.CAMERAEVENT)) -> int:
        """
        Заполнить структуру с описанием события
        
        :param _hevent: идентификатор объекта с описанием события
        
        :param _message: адрес структуры для записи информации о событии
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return camGetEventStucture_t (_hevent, _message)

    camGetCameraByEvent_t = mapsyst.GetProcAddress(videolib,camtype.HCAM,'camGetCameraByEvent', camtype.HCAMEVENT)
    def camGetCameraByEvent(_hevent: camtype.HCAMEVENT) -> camtype.HCAM:
        """
        Запросить идентификатор камеры, от которой было принято событие
        
        :param _hevent: идентификатор объекта с описанием события
        
        :returns: В случае успеха возвращает идентификатор камеры, от которой было принято уведомление о событии При ошибке возвращает 0
        :rtype: camtype.HCAM
        """
        return camGetCameraByEvent_t (_hevent)

    camGetCameraNameByEvent_t = mapsyst.GetProcAddress(videolib,ctypes.c_long,'camGetCameraNameByEvent', camtype.HCAMEVENT, maptype.PWCHAR, ctypes.c_long)
    def camGetCameraNameByEvent(_hevent: camtype.HCAMEVENT, _name: mapsyst.WTEXT, _namesize: int) -> int:
        """
        Запросить название камеры, от которой было принято событие
        
        :param _hevent: идентификатор объекта с описанием события
        
        :param _name: адрес строки для записи названия камеры
        
        :param _namesize: размер выделенного буфера в байтах
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return camGetCameraNameByEvent_t (_hevent, _name.buffer(), _namesize)

    camGetCameraAddrByEvent_t = mapsyst.GetProcAddress(videolib,ctypes.c_long,'camGetCameraAddrByEvent', camtype.HCAMEVENT, maptype.PWCHAR, ctypes.c_long)
    def camGetCameraAddrByEvent(_hevent: camtype.HCAMEVENT, _addr: mapsyst.WTEXT, _addrsize: int) -> int:
        """
        Запросить сетевой адрес камеры, от которой было принято событие
        
        :param _hevent: идентификатор объекта с описанием события
        
        :param _addr: адрес строки для записи сетевого адреса
        
        :param _addrsize: размер выделенного буфера в байтах
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return camGetCameraAddrByEvent_t (_hevent, _addr.buffer(), _addrsize)

    camGetObjectByEvent_t = mapsyst.GetProcAddress(videolib,maptype.HOBJ,'camGetObjectByEvent', camtype.HCAMEVENT)
    def camGetObjectByEvent(_hevent: camtype.HCAMEVENT) -> maptype.HOBJ:
        """
        Запросить идентификатор объекта-камеры на карте
        
        :param _hevent: идентификатор объекта с описанием события
        
        :returns: В случае успеха возвращает идентификатор объекта-камеры, от которого было принято уведомление о событие При ошибке возвращает 0
        :rtype: maptype.HOBJ
        """
        return camGetObjectByEvent_t (_hevent)

    camGetProfileNumByEvent_t = mapsyst.GetProcAddress(videolib,ctypes.c_long,'camGetProfileNumByEvent', camtype.HCAMEVENT)
    def camGetProfileNumByEvent(_hevent: camtype.HCAMEVENT) -> int:
        """
        Запросить номер активного медиапрофиля камеры
        
        :param _hevent: идентификатор объекта с описанием события
        
        :returns: В случае успеха возвращает номер медиапрофиля (начиная с 0), который был активным во время возникновения события При ошибке возвращает -1
        :rtype: int
        """
        return camGetProfileNumByEvent_t (_hevent)



def cameventapi_healthcheck():
    return 1
