#!/usr/bin/env python3

"""
.. code-block:: none

    **********************************************************************
    *                                                                    *
    *              Copyright (c) PANORAMA Group 1991-2026                *
    *                      All Rights Reserved                           *
    *                                                                    *
    **********************************************************************
    *                                                                    *
    *      Описание интерфейса доступа к векторной карте                 *
    *                                                                    *
    *   Под векторными картами понимаются: локально расположенные файлы  *
    *   форматов SITX, SIT, SITZ, MAP, MAPZ или файлы на ГИС Сервере,    *
    *   таблицы пространственных баз данных, открываемые через файлы     *
    *   параметров доступа DBM, данные с сервисов WFS и WFS-T.           *
    *   Карта обстановки (пользовательская) может состоять из одного     *
    *   листа произвольных размеров или набора листов, имеет свой        *
    *   классификатор и  может открываться поверх другой базовой         *
    *   (фоновой) карты местности любого масштаба. Над одной картой      *
    *   местности может отображаться произвольное число других карт      *
    *                                                                    *
    ***********************************************************************
    
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
    mapOpenSiteForMapPro_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapOpenSiteForMapPro', maptype.HMAP, maptype.PWCHAR, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapOpenSiteForMapPro(_hmap: maptype.HMAP, _sitename: mapsyst.WTEXT, _mode: int, _transform: int, _password: mapsyst.WTEXT, _size: int) -> maptype.HSITE:
        """
        Открыть векторную карту в наборе данных (документе)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _sitename: имя открываемого файла векторной карты
        
        :param _mode: режим чтения/записи (``GENERIC_READ``, ``GENERIC_WRITE`` или ``0``)
        
        :param _transform: признак трансформирования карты к ранее открытым данным: ``0`` - не трансформировать данные (преобразовывать ``"на лету"``), ``1`` - трансформировать данные при открытии и сохранить карту в новой проекции, -``1`` - задать вопрос пользователю В серверной версии -``1`` обрабатывается, как ``0``
        
        :param _password: пароль доступа к данным из которого формируется ``256``-битный код для шифрования данных (при утрате данные не восстанавливаются) или ноль
        
        :param _size: длина пароля в байтах или ноль
        
        :returns: Возвращает идентификатор открытой векторной карты При ошибке возвращает ноль
        :rtype: maptype.HSITE
        
        .. note::

           Передача пароля необходима, если при создании карты он был указан
           Если пароль не передан, а он был указан при создании,
           то автоматически вызывается диалог scnGetMapPassword из mapscena64.dll (gis64dlgs.dll)
           Если выдача сообщений запрещена (mapIsMessageEnable), то диалог
           не вызывается, а при отсутствии пароля происходит отказ открытия данных
        """
        return mapOpenSiteForMapPro_t (_hmap, _sitename.buffer(), _mode, _transform, _password.buffer(), _size)

    mapOpenSiteForMapUn_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapOpenSiteForMapUn', maptype.HMAP, maptype.PWCHAR, ctypes.c_long)
    def mapOpenSiteForMapUn(_hmap: maptype.HMAP, _sitename: mapsyst.WTEXT, _mode: int) -> maptype.HSITE:
        """
        Открыть пользовательскую карту в районе работ (добавить в цепочку пользовательских карт)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _sitename: имя открываемого файла пользовательской карты
        
        :param _mode: режим чтения/записи (``GENERIC_READ``, ``GENERIC_WRITE`` или ``0``)
        
        :returns: Возвращает идентификатор открытой пользовательской карты При ошибке возвращает ноль
        :rtype: maptype.HSITE
        """
        return mapOpenSiteForMapUn_t (_hmap, _sitename.buffer(), _mode)

    mapCloseSiteForMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCloseSiteForMap', maptype.HMAP, maptype.HSITE)
    def mapCloseSiteForMap(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Закрыть по идентификатору векторную карту в наборе данных (документе)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если hsite =``= 0``, закрываются все данные обстановки
        """
        return mapCloseSiteForMap_t (_hmap, _hsite)

    mapCloseSiteForMapByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCloseSiteForMapByNameUn', maptype.HMAP, maptype.PWCHAR)
    def mapCloseSiteForMapByNameUn(_hmap: maptype.HMAP, _sitename: mapsyst.WTEXT) -> int:
        """
        Закрыть по названию векторную карту в наборе данных (документе)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _sitename: полный путь к файлу паспорта карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCloseSiteForMapByNameUn_t (_hmap, _sitename.buffer())

    mapDeleteSite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteSite', maptype.HMAP, ctypes.c_long)
    def mapDeleteSite(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Удалить векторную карту (все файлы данных)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: номер векторную карту по номеру от ``1`` до mapGetSiteCount()
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteSite_t (_hmap, _number)

    mapDeleteSiteByNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteSiteByNameUn', maptype.PWCHAR)
    def mapDeleteSiteByNameUn(_sitename: mapsyst.WTEXT) -> int:
        """
        Удалить векторную карту (все файлы данных)
        
        :param _sitename: полное имя файла паспорта карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteSiteByNameUn_t (_sitename.buffer())

    mapClearSite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapClearSite', maptype.HMAP, maptype.HSITE)
    def mapClearSite(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Удалить все объекты векторной карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapClearSite_t (_hmap, _hsite)

    mapCopySiteUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCopySiteUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR)
    def mapCopySiteUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _newname: mapsyst.WTEXT) -> int:
        """
        Скопировать векторную карту с изменением имен файлов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _newname: полный путь к имени паспорта новой карты Имена файлов данных будут иметь такое же имя, как у карты, но свое расширение
        
        :returns: При ошибке (новое имя не создано) возвращает ноль
        :rtype: int
        
        .. note::

           Если классификатор расположен с картой, он тоже копируется в новую директорию
           Для удаления старой копии необходимо вызвать mapDeleteSite
        """
        return mapCopySiteUn_t (_hmap, _hsite, _newname.buffer())

    mapSaveSite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSaveSite', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSaveSite(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _force: int) -> ctypes.c_void_p:
        """
        Сохранить текущее состояние карты на диск
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _force: сохранять всегда, если не ``0``, или только при редактировании При выполнении редактирования карты с отключенным журналом транзакций состояние карты в памяти и на диске может отличаться, в этом случае можно вызвать mapSaveSite
        """
        return mapSaveSite_t (_hmap, _hsite, _force)

    mapSaveMapFrameAs_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSaveMapFrameAs', maptype.HMAP, maptype.HSITE, maptype.HMESSAGE, ctypes.POINTER(maptype.DFRAME), maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(ctypes.c_long))
    def mapSaveMapFrameAs(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _handle: maptype.HMESSAGE, _frame: ctypes.POINTER(maptype.DFRAME), _newname: mapsyst.WTEXT, _sheetframe: int, _error: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Сохранить фрагмент карты в виде векторной карты SITX в см
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _handle: идентификатор окна (``HWND``/функция обратного вызова в Linux) для получения сообщений ``WM_PROGRESSBARUN`` или ``0``
        
        :param _frame: сохраняемая область в метрах в системе координат документа
        
        :param _newname: полный путь к имени паспорта новой карты
        
        :param _sheetframe: признак формирования новой карты с рамкой
        
        :param _error: результат выполнения: код ошибки или ноль
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSaveMapFrameAs_t (_hmap, _hsite, _handle, _frame, _newname.buffer(), _sheetframe, _error)

    gsMapSorting_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'gsMapSorting', maptype.HMAP, maptype.HSITE, maptype.HMESSAGE, ctypes.c_long)
    def gsMapSorting(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _handle: maptype.HMESSAGE, _flags: int) -> int:
        """
        Сортировка отдельной карты документа
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _handle: идентификатор окна, которому посылаются сообщения ``WM_OBJECT`` и ``WM_ERROR``
        
        :param _flags: флажки обработки карты: ``0`` - сортировать все листы, ``1`` - только несортированные, ``2`` - сохранять файлы отката (устанавливается автоматически), ``4`` - повысить точность хранения, ``16`` - повысить точность хранения, формат - см ``32`` - повысить точность хранения, формат - мм ``64`` - повысить точность хранения, формат - радианы
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return gsMapSorting_t (_hmap, _hsite, _handle, _flags)

    mapGetSiteCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteCount', maptype.HMAP)
    def mapGetSiteCount(_hmap: maptype.HMAP) -> int:
        """
        Запросить количество открытых векторных карт поверх фоновой карты (снимка, геопортала или других данных)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteCount_t (_hmap)

    mapGetSiteNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteNumber', maptype.HMAP, maptype.HSITE)
    def mapGetSiteNumber(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Определить номер векторной карты в цепочке по ее идентификатору
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteNumber_t (_hmap, _hsite)

    mapGetSiteFileNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteFileNameUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_long)
    def mapGetSiteFileNameUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Определить имя файла паспорта векторной карты по ее идентификатору
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _name: адрес буфера для записи имени файла
        
        :param _size: размер строки в байтах
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapGetSiteFileNameUn_t (_hmap, _hsite, _name.buffer(), _size)

    mapIsTempSite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsTempSite', maptype.HMAP, maptype.HSITE)
    def mapIsTempSite(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить является ли карта временной, созданной через mapCreateTempSite или mapCreateAndAppendTempSite
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Для временной карты возвращает ненулевое значение При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsTempSite_t (_hmap, _hsite)

    mapIsSiteLimited_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsSiteLimited', maptype.HMAP, maptype.HSITE)
    def mapIsSiteLimited(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить является ли карта ограниченной по территории (по рамке номенклатурного листа)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Если карта содержит номенклатурный лист, то функция возвращает ненулевое значение Если территория карты не ограничена (меняется при добавлении или удалении объектов) - возвращает ноль При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsSiteLimited_t (_hmap, _hsite)

    mapIsSiteRealGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsSiteRealGeo', maptype.HMAP, maptype.HSITE)
    def mapIsSiteRealGeo(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить содержит ли карта координаты в геодезической системе (радианы)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: функция возвращает ненулевое значение При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если карта хранит координаты в геодезической системе,
        """
        return mapIsSiteRealGeo_t (_hmap, _hsite)

    mapGetSitePrecision_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSitePrecision', maptype.HMAP, maptype.HSITE)
    def mapGetSitePrecision(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить признак повышенной точности хранения координат
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Возвращает значения: ``1`` - максимальная точность хранения (метры или радианы), ``2`` - с точностью 2 знака (сантиметры), ``3`` - с точностью 3 знака (миллиметры) При ошибке или нормальной точности хранения координат возвращает ноль
        :rtype: int
        """
        return mapGetSitePrecision_t (_hmap, _hsite)

    mapIsObjectMapRealGeo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsObjectMapRealGeo', maptype.HOBJ)
    def mapIsObjectMapRealGeo(_hobj: maptype.HOBJ) -> int:
        """
        Запросить содержит ли карта объекта координаты в геодезической системе (радианы)
        
        :param _hobj: идентификатор объекта
        
        :returns: функция возвращает ненулевое значение При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если карта хранит координаты в геодезической системе,
        """
        return mapIsObjectMapRealGeo_t (_hobj)

    mapIsSiteGeoSupported_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsSiteGeoSupported', maptype.HMAP, maptype.HSITE)
    def mapIsSiteGeoSupported(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить поддерживается ли пересчет к геодезическим координатам из плоских прямоугольных и обратно
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Если карта поддерживает пересчет к геодезическим координатам, функция возвращает ненулевое значение При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsSiteGeoSupported_t (_hmap, _hsite)

    mapIsSiteMarine_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsSiteMarine', maptype.HMAP, maptype.HSITE)
    def mapIsSiteMarine(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить является ли карта морской (создана по классификатору s57navy.rsc)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Для морской карты возвращает ненулевое значение При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsSiteMarine_t (_hmap, _hsite)

    mapIsSiteS63_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsSiteS63', maptype.HMAP, maptype.HSITE)
    def mapIsSiteS63(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить является ли карта морской по стандарту S63
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных Карта должна быть создана по классификатору s57navy.rsc в формате SITX и закодирована hw_id6
        
        :returns: Для морской карты по стандарту S63 возвращает ненулевое значение При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsSiteS63_t (_hmap, _hsite)

    mapGetS63LicenseTerm_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetS63LicenseTerm', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapGetS63LicenseTerm(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int) -> int:
        """
        Запросить дату завершения срока действия лицензии на карту S63 (полученную из PERMIT.TXT)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _list: номер листа с ``1`` Карта должна быть создана по классификатору s57navy.rsc в формате SITX и закодирована hw_id6
        
        :returns: Возвращается значение, которое было указано в файле PERMIT.TXT при создании карты При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetS63LicenseTerm_t (_hmap, _hsite, _list)

    mapIsSiteArmy_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsSiteArmy', maptype.HMAP, maptype.HSITE)
    def mapIsSiteArmy(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить является ли карта оперативной обстановкой (создана по классификатору operator.rsc)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Для карты обстановки возвращает ненулевое значение При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsSiteArmy_t (_hmap, _hsite)

    mapIsSiteAero_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsSiteAero', maptype.HMAP, maptype.HSITE)
    def mapIsSiteAero(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить является ли карта аэронавигационной (создана по классификатору dfc.rsc)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных,
        
        :returns: Для аэронавигационной карты возвращает ненулевое значение При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsSiteAero_t (_hmap, _hsite)

    mapIsSiteGraph_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsSiteGraph', maptype.HMAP, maptype.HSITE)
    def mapIsSiteGraph(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить является ли карта графом дорог
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных Карта должна быть создана по классификатору service.rsc или road25.rsc и содержать дуги графа
        
        :returns: Для карты графа возвращает ненулевое значение При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsSiteGraph_t (_hmap, _hsite)

    mapIsSiteFromServer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsSiteFromServer', maptype.HMAP, maptype.HSITE)
    def mapIsSiteFromServer(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить открыта ли карта на сервере или локально
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Если карта открыта на сервере возвращает ненулевое значение
        :rtype: int
        """
        return mapIsSiteFromServer_t (_hmap, _hsite)

    mapGetMapStateFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMapStateFlag', maptype.HMAP, maptype.HSITE)
    def mapGetMapStateFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить состояние данных для карты, открытой на сервере
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Для локального представления карты (dbm) из базы данных возвращает значение режима потоковой загрузки данных (такое же, что и функция mapGetLoadState) При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если представление карты формируется на лету из базы данных,
           то при открытии карты устанавливается признак ``"состояние загрузки"``, равное 1.
           Признак сбрасывается в ноль при вызове функций mapAdjustData или mapAdjustSiteData,
           если загрузка карты завершена
        """
        return mapGetMapStateFlag_t (_hmap, _hsite)

    mapAdjustSiteData_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAdjustSiteData', maptype.HMAP, maptype.HSITE)
    def mapAdjustSiteData(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Выполнить согласование данных карты в памяти и на диске (при многопользовательском доступе к данным)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных,
        
        :returns: возвращает ненулевое значение 1, иначе - 0 Если карта должна быть закрыта - возвращает 2 (доступ на ГИС Сервер прекращен) Если карта, открыта с ГИС Сервера, а связи с ним нет, то возвращает -1 Если состояние изменилось - необходимо перерисовать изображение карты Опрос состояния целесообразно выполнять периодически в процессе работы приложения
        :rtype: int
        
        .. note::

           Если состояние данных в памяти изменилось (по данным с диска)
        """
        return mapAdjustSiteData_t (_hmap, _hsite)

    mapAdjustCommonXml_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAdjustCommonXml')
    def mapAdjustCommonXml() -> int:
        """
        Проверить и при необходимости обновить общие файлы XML
        
        Обновляются файлы XML, размещенные в общей папке
        классификаторов по эталонам, размещенным на ГИС Сервере
        
        :returns: Если хост ГИС Сервера не установлен или не доступен - возвращает ноль При успешном обновлении возвращает число обновленных файлов
        :rtype: int
        """
        return mapAdjustCommonXml_t ()

    mapCheckMapStateFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckMapStateFlag', maptype.HMAP)
    def mapCheckMapStateFlag(_hmap: maptype.HMAP) -> int:
        """
        Запросить, есть ли карты в состоянии загрузки на сервере
        
        :param _hmap: идентификатор открытых данных (документа) Проверка выполняется для всех карт в составе ``"документа"`` (hmap)
        
        :returns: Если есть карты в состоянии загрузки, то возвращает 1 При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если представление карты формируется на лету из базы данных,
           то при открытии карты устанавливается признак ``"состояние загрузки"``, равное 1
           Признак сбрасывается при вызове функции mapAdjustData,
           если загрузка карты завершена
        """
        return mapCheckMapStateFlag_t (_hmap)

    mapIsSiteSitX_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsSiteSitX', maptype.HMAP, maptype.HSITE)
    def mapIsSiteSitX(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить, хранится ли карта в одном файле (формат SITX)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Если карта в одном файле возвращает ненулевое значение При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsSiteSitX_t (_hmap, _hsite)

    mapIsSitePackaged_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsSitePackaged', maptype.HMAP, maptype.HSITE)
    def mapIsSitePackaged(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить, хранится ли карта в одном упакованном файле (формат SITZ/MAPZ)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Если карта в одном упакованном файле возвращает ненулевое значение При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsSitePackaged_t (_hmap, _hsite)

    mapSetAlternativeFontsFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetAlternativeFontsFlag', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetAlternativeFontsFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flag: int) -> int:
        """
        Установить признак применения альтернативных шрифтов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _flag: признак применения альтернативных шрифтов, заданных в файле altfonts.xml
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetAlternativeFontsFlag_t (_hmap, _hsite, _flag)

    mapGetAlternativeFontsFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetAlternativeFontsFlag', maptype.HMAP, maptype.HSITE)
    def mapGetAlternativeFontsFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить признак применения альтернативных шрифтов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Возвращает ранее установленное значение
        :rtype: int
        """
        return mapGetAlternativeFontsFlag_t (_hmap, _hsite)

    mapSetRouteMap4DFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetRouteMap4DFlag', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetRouteMap4DFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flag: int) -> int:
        """
        Установить признак использования координаты M, как линейной координаты маршрута
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _flag: признак использования координаты M, как линейной координаты маршрута Используется при загрузке в карту готовых маршрутов без калибровочных точек
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetRouteMap4DFlag_t (_hmap, _hsite, _flag)

    mapGetRouteMap4DFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetRouteMap4DFlag', maptype.HMAP, maptype.HSITE)
    def mapGetRouteMap4DFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить признак использования координаты M, как линейной координаты маршрута
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных Используется при загрузке в карту готовых маршрутов без калибровочных точек
        
        :returns: Возвращает ранее установленное значение
        :rtype: int
        """
        return mapGetRouteMap4DFlag_t (_hmap, _hsite)

    mapSetObjectTimeFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetObjectTimeFlag', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetObjectTimeFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flag: int) -> int:
        """
        Установить признак ведения даты и времени обновления для каждого объекта
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _flag: признак ведения даты и времени обновления Признак устанавливается после создания карты до записи объектов
        
        :returns: Если открытых данных нет возвращает ноль
        :rtype: int
        """
        return mapSetObjectTimeFlag_t (_hmap, _hsite, _flag)

    mapGetObjectTimeFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetObjectTimeFlag', maptype.HMAP, maptype.HSITE)
    def mapGetObjectTimeFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить признак ведения даты и времени обновления для каждого объекта
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Если открытых данных нет или признак не установлен - возвращает ноль
        :rtype: int
        """
        return mapGetObjectTimeFlag_t (_hmap, _hsite)

    mapSetMatchingFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetMatchingFlag', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long)
    def mapSetMatchingFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _flag: int) -> int:
        """
        Установить флаг сводки объектов по рамке листа карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _list: номер листа карты с ``1`` до числа листов
        
        :param _flag: флаг сводки объектов по рамке листа карты
        
        :returns: Если открытых данных нет возвращает ноль
        :rtype: int
        """
        return mapSetMatchingFlag_t (_hmap, _hsite, _list, _flag)

    mapGetMatchingFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMatchingFlag', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapGetMatchingFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int) -> int:
        """
        Запросить флаг сводки объектов по рамке листа карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _list: номер листа карты с ``1`` до числа листов
        
        :returns: Если открытых данных нет или флаг не установлен - возвращает ноль
        :rtype: int
        """
        return mapGetMatchingFlag_t (_hmap, _hsite, _list)

    mapSetAutoObjectGUID_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetAutoObjectGUID', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetAutoObjectGUID(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flag: int) -> int:
        """
        Установить признак ведения уникального идентификатора GUID для объектов карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных,
        
        :param _flag: признак ведения ``GUID`` для объектов карты Признак устанавливается после создания карты до записи объектов
        
        :returns: Если открытых данных нет возвращает ноль
        :rtype: int
        
        .. note::

           Если признак установлен, то каждому объекту карты при создании автоматически
           присваивается семантика с кодом 32799, содержащая уникальную комбинацию
           из 32 шестнадцатеричных символов от 0 до F (GUID)
        """
        return mapSetAutoObjectGUID_t (_hmap, _hsite, _flag)

    mapGetAutoObjectGUID_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetAutoObjectGUID', maptype.HMAP, maptype.HSITE)
    def mapGetAutoObjectGUID(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить признак ведения уникального идентификатора GUID для объектов карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Если открытых данных нет или признак не установлен возвращает ноль
        :rtype: int
        """
        return mapGetAutoObjectGUID_t (_hmap, _hsite)

    mapGetMapFilesName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMapFilesName', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetMapFilesName(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _type: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить имена файлов данных листа карты для контроля целостности данных
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _list: номер листа карты с ``1`` до числа листов
        
        :param _type: тип листа карты: ``1`` - файл заголовков, ``2`` - файл метрики, ``3`` - файл семантики, ``4`` - файл графики
        
        :param _name: адрес буфера для записи имени файла
        
        :param _size: размер буфера для записи имени файла Кроме указанных файлов карта имеет паспорт карты и цифровой классификатор ``RSC`` Файл SITX содержит все данные (кроме ``RSC``) в одном файле
        
        :returns: отмечено, что такие данные есть в листе), то возвращает 1, если таких данных нет, то возвращает -1 Файлы заголовков и метрики присутствуют всегда При ошибке возвращает 0
        :rtype: int
        
        .. note::

           Если запрошенный тип файла должен входить в состав карты (в паспорте карты
        """
        return mapGetMapFilesName_t (_hmap, _hsite, _list, _type, _name.buffer(), _size)

    mapGetSheetFilesLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSheetFilesLength', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_ulong))
    def mapGetSheetFilesLength(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _head: ctypes.POINTER(ctypes.c_ulong), _data: ctypes.POINTER(ctypes.c_ulong), _semn: ctypes.POINTER(ctypes.c_ulong), _draw: ctypes.POINTER(ctypes.c_ulong)) -> int:
        """
        Запросить длину файлов листа карты в байтах
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _list: номер листа карты с ``1`` до числа листов
        
        :param _head: указатель на поле для записи размера индексного файла (может равняться нулю)
        
        :param _data: указатель на поле для записи размера файла метрики (может равняться нулю)
        
        :param _semn: указатель на поле для записи размера файла семантики (может равняться нулю)
        
        :param _draw: указатель на поле для записи размера файла графических параметров графических объектов (может равняться нулю) При экспорте в ``SXF`` размер файла ``SXF`` примерно будет равен сумме размеров всех файлов листа карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSheetFilesLength_t (_hmap, _hsite, _list, _head, _data, _semn, _draw)

    mapGetSiteTotalDataSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_int64,'mapGetSiteTotalDataSize', maptype.HMAP, maptype.HSITE)
    def mapGetSiteTotalDataSize(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить общую длину данных всех файлов карты в байтах
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteTotalDataSize_t (_hmap, _hsite)

    mapGetSitePathUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSitePathUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_long)
    def mapGetSitePathUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Определить путь к папке векторной карты по ее идентификатору
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _name: адрес буфера для записи пути к папке
        
        :param _size: размер буфера для записи пути
        
        :returns: При ошибке возвращает пустую строку
        :rtype: int
        """
        return mapGetSitePathUn_t (_hmap, _hsite, _name.buffer(), _size)

    mapGetLogPathUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetLogPathUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_long)
    def mapGetLogPathUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _path: mapsyst.WTEXT, _size: int) -> int:
        """
        Определить путь к папке LOG векторной карты по ее идентификатору
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _path: адрес буфера для записи пути к папке
        
        :param _size: размер буфера в байтах
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapGetLogPathUn_t (_hmap, _hsite, _path.buffer(), _size)

    mapGetVclxName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetVclxName', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_long)
    def mapGetVclxName(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _vclname: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить имя файла vclx для карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _vclname: адрес буфера для записи имени файла vclx
        
        :param _size: размер буфера в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetVclxName_t (_hmap, _hsite, _vclname.buffer(), _size)

    mapGetSiteIdent_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapGetSiteIdent', maptype.HMAP, ctypes.c_long)
    def mapGetSiteIdent(_hmap: maptype.HMAP, _number: int) -> maptype.HSITE:
        """
        Определить идентификатор векторной карты в открытых данных по ее номеру в цепочке
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: номер пользовательской карты в цепочке
        
        :returns: Если number =``= 0``, возвращается идентификатор фоновой (базовой) карты, равный hmap (он может применяться вместо HSITE) При ошибке возвращает ноль
        :rtype: maptype.HSITE
        """
        return mapGetSiteIdent_t (_hmap, _number)

    mapGetSiteIdentByNameUn_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapGetSiteIdentByNameUn', maptype.HMAP, maptype.PWCHAR)
    def mapGetSiteIdentByNameUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT) -> maptype.HSITE:
        """
        Определить идентификатор векторной карты в открытых данных по имени файла паспорта
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _name: имя файла паспорта пользовательской карты
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HSITE
        """
        return mapGetSiteIdentByNameUn_t (_hmap, _name.buffer())

    mapGetSiteSheetNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteSheetNameUn', maptype.HMAP, maptype.HSITE, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetSiteSheetNameUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить имя листа по его номеру
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _list: номер листа карты
        
        :param _name: адрес буфера для результата запроса
        
        :param _size: размер буфера в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteSheetNameUn_t (_hmap, _hsite, _list, _name.buffer(), _size)

    mapGetSiteNomenclatureUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteNomenclatureUn', maptype.HMAP, maptype.HSITE, ctypes.c_int, maptype.PWCHAR, ctypes.c_long)
    def mapGetSiteNomenclatureUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить номенклатуру листа по его номеру
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _list: номер листа карты
        
        :param _name: адрес буфера для результата запроса
        
        :param _size: размер буфера в байтах Номенклатура листа применяется для поиска в функции mapSeekObject
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteNomenclatureUn_t (_hmap, _hsite, _list, _name.buffer(), _size)

    mapGetSiteListName_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetSiteListName', maptype.HMAP, maptype.HSITE, ctypes.c_int)
    def mapGetSiteListName(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int) -> ctypes.POINTER(ctypes.c_char):
        """
        Запросить номенклатуру листа по его номеру
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _list: номер листа карты
        
        :returns: При ошибке возвращает пустую строку
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetSiteListName_t (_hmap, _hsite, _list)

    mapGetSiteIdentByNomenclatureUn_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapGetSiteIdentByNomenclatureUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long))
    def mapGetSiteIdentByNomenclatureUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _list: ctypes.POINTER(ctypes.c_long)) -> maptype.HSITE:
        """
        Определить идентификатор открытой карты по номенклатуре листа
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _name: номенклатура листа карты
        
        :param _list: поле для размещения номера листа (если лист найден в многолистовой карте)
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HSITE
        """
        return mapGetSiteIdentByNomenclatureUn_t (_hmap, _name.buffer(), _list)

    mapGetSiteIdentBySheetNameUn_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapGetSiteIdentBySheetNameUn', maptype.HMAP, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long))
    def mapGetSiteIdentBySheetNameUn(_hmap: maptype.HMAP, _name: mapsyst.WTEXT, _list: ctypes.POINTER(ctypes.c_long)) -> maptype.HSITE:
        """
        Определить идентификатор открытой векторной карты по имени листа карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _name: имя листа карты
        
        :param _list: поле для размещения номера листа Имя листа карты запрашивается в функции mapGetSiteSheetNameUn
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HSITE
        """
        return mapGetSiteIdentBySheetNameUn_t (_hmap, _name.buffer(), _list)

    mapGetActiveSite_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapGetActiveSite', maptype.HMAP)
    def mapGetActiveSite(_hmap: maptype.HMAP) -> maptype.HSITE:
        """
        Запросить активную векторной карту (устанавливается приложением по своему усмотрению)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HSITE
        """
        return mapGetActiveSite_t (_hmap)

    mapSetActiveSite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetActiveSite', maptype.HMAP, maptype.HSITE)
    def mapSetActiveSite(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Установить активную пользовательскую карту (устанавливается приложением по своему усмотрению)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetActiveSite_t (_hmap, _hsite)

    mapGetCurrentViewSite_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapGetCurrentViewSite', maptype.HMAP)
    def mapGetCurrentViewSite(_hmap: maptype.HMAP) -> maptype.HSITE:
        """
        Запросить идентификатор текущей отображаемой карты
        
        :param _hmap: идентификатор открытых данных (документа) При запросе в момент отображения из вспомогательной библиотеки считаем, что один ``HMAP`` применяется в одном потоке отображения
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HSITE
        """
        return mapGetCurrentViewSite_t (_hmap)

    mapGetSiteMode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteMode', maptype.HMAP, maptype.HSITE)
    def mapGetSiteMode(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить номер состояния пользовательской карты по ее идентификатору
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных Номер состояния меняется при любой операции редактирования карты (увеличивается на ``1``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteMode_t (_hmap, _hsite)

    mapIsSiteWFS_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsSiteWFS', maptype.HMAP, maptype.HSITE)
    def mapIsSiteWFS(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить является ли открытая карта картой с данными c сервиса WFS
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Если нет - возвращает ноль
        :rtype: int
        """
        return mapIsSiteWFS_t (_hmap, _hsite)

    mapGetHWFS_t = mapsyst.GetProcAddress(acceslib,maptype.HWFS,'mapGetHWFS', maptype.HMAP, maptype.HSITE)
    def mapGetHWFS(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> maptype.HWFS:
        """
        Запросить HWFS
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Если нет - возвращает ноль
        :rtype: maptype.HWFS
        """
        return mapGetHWFS_t (_hmap, _hsite)

    mapGetSiteCodeFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteCodeFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSiteCodeFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить установлено ли шифрование данных
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Если нет - возвращает ноль
        :rtype: int
        """
        return mapGetSiteCodeFlag_t (_hmap, _hsite)

    mapGetSiteCodeFlagByName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteCodeFlagByName', maptype.PWCHAR)
    def mapGetSiteCodeFlagByName(_name: mapsyst.WTEXT) -> int:
        """
        Запросить, зашифрована ли карта (формат SITX)
        
        :param _name: имя карты (путь к файлу)
        
        :returns: Если нет - возвращает ноль
        :rtype: int
        """
        return mapGetSiteCodeFlagByName_t (_name.buffer())

    mapGetSiteCopyFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteCopyFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSiteCopyFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить, могут ли объекты карты копироваться на другие карты или экспортироваться
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Если нет - возвращает ноль
        :rtype: int
        """
        return mapGetSiteCopyFlag_t (_hmap, _hsite)

    mapGetSiteFolderEditFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteFolderEditFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSiteFolderEditFlag(_hMap: maptype.HMAP, _hSite: maptype.HSITE) -> int:
        """
        Запросить, можно ли записывать файлы картинок и документов в папке с картой на ГИС Сервере
        
        :param _hMap: идентификатор открытых данных (документа)
        
        :param _hSite: идентификатор векторной карты в открытых данных
        
        :returns: Если нет - возвращает ноль
        :rtype: int
        
        .. note::

           Если запись разрешена, то можно применить функции mapSaveFileOnServer(), mapReadFileOnServer()
        """
        return mapGetSiteFolderEditFlag_t (_hMap, _hSite)

    mapSetSiteHideCopy_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSiteHideCopy', maptype.HMAP, maptype.HSITE)
    def mapSetSiteHideCopy(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запретить копирование объектов с карты (свойство нельзя отменить)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetSiteHideCopy_t (_hmap, _hsite)

    mapGetSiteHidePassportFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteHidePassportFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSiteHidePassportFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить запрещено ли показывать параметры паспорта
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Если нет - возвращает ноль
        :rtype: int
        """
        return mapGetSiteHidePassportFlag_t (_hmap, _hsite)

    mapGetPrintFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetPrintFlag', maptype.HMAP, maptype.HSITE)
    def mapGetPrintFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить может ли карта выводиться на печать
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных Для карт, открытых на ГИС Сервере, может устанавливаться запрет вывода изображения карты на печать
        
        :returns: Если нет - возвращает ноль
        :rtype: int
        """
        return mapGetPrintFlag_t (_hmap, _hsite)

    mapGetDBMapFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetDBMapFlag', maptype.HMAP, maptype.HSITE)
    def mapGetDBMapFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить отражает ли карта содержимое таблицы базы данных
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных Таблица базы данных открыта на ГИС Сервере или с клиентского компьютера (через файл ``DBM``)
        
        :returns: Если карта не отражает данные из базы данных - возвращает ноль (DBMFLAG_NOTDBM) Для карты, открытой на ГИС Сервере, возвращает DBMFLAG_GISSERVER (1) Для локально открытой карты DBM возвращает DBMFLAG_LOCAL (2)
        :rtype: int
        """
        return mapGetDBMapFlag_t (_hmap, _hsite)

    mapGetDBFileName_t = mapsyst.GetProcAddress(acceslib,maptype.PWCHAR,'mapGetDBFileName', maptype.HMAP, maptype.HSITE)
    def mapGetDBFileName(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> mapsyst.WTEXT:
        """
        Запросить полный путь к локальному DBM-файлу
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: mapsyst.WTEXT
        """
        return mapGetDBFileName_t (_hmap, _hsite)

    mapGetDBMapName_t = mapsyst.GetProcAddress(acceslib,maptype.PWCHAR,'mapGetDBMapName', maptype.HMAP, maptype.HSITE)
    def mapGetDBMapName(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> mapsyst.WTEXT:
        """
        Запросить полный путь к карте (map/sit/sitx) для локального DBM-файла
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: mapsyst.WTEXT
        """
        return mapGetDBMapName_t (_hmap, _hsite)

    mapGetObjectTypeLimitIdent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetObjectTypeLimitIdent', maptype.HMAP, maptype.HSITE)
    def mapGetObjectTypeLimitIdent(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить идентификатор группы карт с ограничением типа записываемых объектов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: создаваемых объектов - возвращает ноль, иначе - идентификатор группы карт с одним классификатором
        :rtype: int
        
        .. note::

           Если карта не входит в группу карт с ограничением типа
        """
        return mapGetObjectTypeLimitIdent_t (_hmap, _hsite)

    mapGetSiteForObjectIdent_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapGetSiteForObjectIdent', maptype.HOBJ)
    def mapGetSiteForObjectIdent(_hobj: maptype.HOBJ) -> maptype.HSITE:
        """
        Подобрать карту для записи объекта в таблицу базы данных (DBM)
        
        :param _hobj: идентификатор объекта в памяти, предварительно созданного функцией mapCreateObject() или mapCreateSiteObject() Отображение базы данных формируется из набора таблиц (представленных в интерфейсе программы пользовательскими картами), каждая таблица может содержать определенные виды объектов Не зависимо от текущей пользовательской карты, на которой создается объект, сохранять его нужно именно в ту таблицу, которой соответствует его тип
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HSITE
        """
        return mapGetSiteForObjectIdent_t (_hobj)

    mapGetSiteForObjectCode_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapGetSiteForObjectCode', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapGetSiteForObjectCode(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _incode: int) -> maptype.HSITE:
        """
        Подобрать карту для записи объекта в таблицу базы данных (DBM)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _incode: внутренний код создаваемого объекта Отображение базы данных формируется из набора таблиц (представленных в интерфейсе программы пользовательскими картами), каждая таблица может содержать определенные виды объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HSITE
        """
        return mapGetSiteForObjectCode_t (_hmap, _hsite, _incode)

    mapGetSiteEditFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteEditFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSiteEditFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить - может ли карта редактироваться (включая метрику)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Если нет - возвращает ноль
        :rtype: int
        """
        return mapGetSiteEditFlag_t (_hmap, _hsite)

    mapSetSiteEditFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSiteEditFlag', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSiteEditFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flag: int) -> int:
        """
        Установить флаг редактирования карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _flag: признак возможности редактирования (``0`` - не редактировать)
        
        :returns: Возвращает новое значение флага (запрет редактирования может сохраниться)
        :rtype: int
        """
        return mapSetSiteEditFlag_t (_hmap, _hsite, _flag)

    mapGetSiteEditFlagWithoutMetric_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteEditFlagWithoutMetric', maptype.HMAP, maptype.HSITE)
    def mapGetSiteEditFlagWithoutMetric(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить может ли карта редактироваться (семантика и графика объекта)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных При общем запрете редактирования векторной карты может быть разрешено редактирование семантики и графики объекта (кроме координат)
        
        :returns: Если нет - возвращает ноль
        :rtype: int
        """
        return mapGetSiteEditFlagWithoutMetric_t (_hmap, _hsite)

    mapGetSiteChangeEditFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteChangeEditFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSiteChangeEditFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить можно ли изменить признак редактирования карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Если нет - возвращает ноль
        :rtype: int
        """
        return mapGetSiteChangeEditFlag_t (_hmap, _hsite)

    mapGetSitePaspEditFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSitePaspEditFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSitePaspEditFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить признак редактируемости паспорта карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных Для карт с ГИС Сервера разрешено редактирование паспорта для администраторов и при отсутствии запрета показывать параметры системы координат
        
        :returns: Если нет - возвращает ноль
        :rtype: int
        """
        return mapGetSitePaspEditFlag_t (_hmap, _hsite)

    mapGetScalingToLevelFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetScalingToLevelFlag', maptype.HMAP, maptype.HSITE)
    def mapGetScalingToLevelFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить флаг масштабируемости объектов карты относительно заданного масштаба
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Если нет - возвращает ноль
        :rtype: int
        
        .. note::

           Если признак не установлен, то масштабирование выполняется относительно
           базового масштаба карты, установленного в паспорте
           Заданный масштаб устанавливается программно (например, в библиотеках IMLAPI)
        """
        return mapGetScalingToLevelFlag_t (_hmap, _hsite)

    mapSetScalingToLevelFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetScalingToLevelFlag', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetScalingToLevelFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flag: int) -> int:
        """
        Установить флаг масштабируемости объектов карты относительно заданного масштаба
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _flag: признак возможности редактирования
        
        :returns: Возвращает новое значение флага
        :rtype: int
        """
        return mapSetScalingToLevelFlag_t (_hmap, _hsite, _flag)

    mapGetSiteTransparent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteTransparent', maptype.HMAP, maptype.HSITE)
    def mapGetSiteTransparent(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить степень прозрачности карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Возвращает значение от 0 (карта не видна) до 100 (карта не прозрачная)
        :rtype: int
        """
        return mapGetSiteTransparent_t (_hmap, _hsite)

    mapSetSiteTransparent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSiteTransparent', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSiteTransparent(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _transparent: int) -> int:
        """
        Установить степень прозрачности карты (от 0 до 100)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _transparent: степень прозрачности карты от ``0`` (карта не видна) до ``100`` (карта не прозрачная)
        
        :returns: Возвращает новое значение флага
        :rtype: int
        """
        return mapSetSiteTransparent_t (_hmap, _hsite, _transparent)

    mapGetSiteBackLightText_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteBackLightText', maptype.HMAP, maptype.HSITE)
    def mapGetSiteBackLightText(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить флаг подсветки подписей
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Возвращает значение флага
        :rtype: int
        """
        return mapGetSiteBackLightText_t (_hmap, _hsite)

    mapSetSiteBackLightText_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSiteBackLightText', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSiteBackLightText(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flag: int) -> int:
        """
        Установить флаг подсветки подписей
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _flag: признак подсветки: ``0`` - подсветка отключена (подписи отображаются в соответствии с параметрами); ``1`` - подсветка включена (все подписи отображаются с белым контуром), использовать при отображении карты поверх растров
        
        :returns: Возвращает новое значение флага
        :rtype: int
        """
        return mapSetSiteBackLightText_t (_hmap, _hsite, _flag)

    mapGetSiteInquiryFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteInquiryFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSiteInquiryFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить могут ли на карте выбираться объекты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Если нет - возвращает ноль
        :rtype: int
        """
        return mapGetSiteInquiryFlag_t (_hmap, _hsite)

    mapSetSiteInquiryFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSiteInquiryFlag', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSiteInquiryFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flag: int) -> int:
        """
        Установить флаг разрешения выбора объектов на карте (0 - не выбирать)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _flag: признак возможности выбора объектов в функциях типа mapWhatObject Влияет на работу функции mapWhatObject
        
        :returns: Возвращает новое значение флага
        :rtype: int
        """
        return mapSetSiteInquiryFlag_t (_hmap, _hsite, _flag)

    mapGetSiteViewFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteViewFlag', maptype.HMAP, maptype.HSITE)
    def mapGetSiteViewFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить отображается ли карта
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Если карта не отображается возвращает ноль
        :rtype: int
        """
        return mapGetSiteViewFlag_t (_hmap, _hsite)

    mapSetSiteViewFlag_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSiteViewFlag', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSiteViewFlag(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flag: int) -> int:
        """
        Установить флаг отображения карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _flag: флаг отображения карты: ``0`` - не отображать, ``1`` - отображать
        
        :returns: Возвращает новое значение флага
        :rtype: int
        """
        return mapSetSiteViewFlag_t (_hmap, _hsite, _flag)

    mapHideSiteObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapHideSiteObject', maptype.HOBJ)
    def mapHideSiteObject(_hobj: maptype.HOBJ) -> int:
        """
        Установить объект, который временно не будет виден на карте
        
        :param _hobj: идентификатор скрываемого объекта Установка сохраняется до переоткрытия карты или до восстановления отображения Функция применяется при редактировании отдельного (единственного) объекта в интерактивном режиме
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapHideSiteObject_t (_hobj)

    mapHideSiteObjectByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapHideSiteObjectByNumber', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long)
    def mapHideSiteObjectByNumber(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _key: int, _list: int) -> int:
        """
        Установить объект, который временно не будет виден на карте
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _key: идентификатор объекта на карте (уникальный номер объекта на листе карты)
        
        :param _list: номер листа карты Установка выполняется до переоткрытия карты или до восстановления отображения Функция применяется при редактировании отдельного (единственного) объекта в интерактивном режиме
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapHideSiteObjectByNumber_t (_hmap, _hsite, _key, _list)

    mapUnhideSiteObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapUnhideSiteObject', maptype.HOBJ)
    def mapUnhideSiteObject(_hobj: maptype.HOBJ) -> ctypes.c_void_p:
        """
        Восстановить отображение объекта (после mapHideSiteObject)
        
        :param _hobj: идентификатор восстанавливаемого объекта Функция обнуляет номер скрываемого объекта и номер листа
        """
        return mapUnhideSiteObject_t (_hobj)

    mapClearHideSiteObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapClearHideSiteObject', maptype.HMAP, maptype.HSITE)
    def mapClearHideSiteObject(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> ctypes.c_void_p:
        """
        Восстановить отображение объекта (после mapHideSiteObject)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных Функция обнуляет номер скрываемого объекта и номер листа
        """
        return mapClearHideSiteObject_t (_hmap, _hsite)

    mapGetHideSiteObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetHideSiteObject', maptype.HMAP, maptype.HSITE, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapGetHideSiteObject(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _number: ctypes.POINTER(ctypes.c_long), _list: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить номер скрываемого объекта и номер листа на карте
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _number: указатель на поле для записи номера объекта
        
        :param _list: указатель на поле для записи номера листа
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapGetHideSiteObject_t (_hmap, _hsite, _number, _list)

    mapSetSiteViewOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSiteViewOrder', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapSetSiteViewOrder(_hmap: maptype.HMAP, _number: int, _order: int) -> int:
        """
        Установить порядок отображения карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: номер пользовательской карты в цепочке
        
        :param _order: флаг: ``0`` - под основной картой, ``1`` - над основной картой
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapSetSiteViewOrder_t (_hmap, _number, _order)

    mapGetSiteViewOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteViewOrder', maptype.HMAP, ctypes.c_long)
    def mapGetSiteViewOrder(_hmap: maptype.HMAP, _number: int) -> int:
        """
        Запросить порядок отображения карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: номер пользовательской карты в цепочке
        
        :returns: Возвращает флаг: ``0`` - под основной картой, ``1`` - над основной картой При ошибке возвращает 0
        :rtype: int
        """
        return mapGetSiteViewOrder_t (_hmap, _number)

    mapChangeOrderSiteShow_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapChangeOrderSiteShow', maptype.HMAP, ctypes.c_long, ctypes.c_long)
    def mapChangeOrderSiteShow(_hmap: maptype.HMAP, _oldnumber: int, _newnumber: int) -> int:
        """
        Поменять очередность отображения карт (sit) в цепочке
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _oldnumber: текущий номер файла в цепочке
        
        :param _newnumber: устанавливаемый номер файла в цепочке
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapChangeOrderSiteShow_t (_hmap, _oldnumber, _newnumber)

    mapClearShowObjectList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapClearShowObjectList', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapClearShowObjectList(_hMmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int) -> ctypes.c_void_p:
        """
        Очистить дерево объектов для отображения при больших изменениях листа карты для последующего перестроения
        
        hmap  - идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _list: номер листа карты
        """
        return mapClearShowObjectList_t (_hMmap, _hsite, _list)

    mapGetSiteRangeScaleVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteRangeScaleVisible', maptype.HMAP, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapGetSiteRangeScaleVisible(_hmap: maptype.HMAP, _number: int, _bottomscale: ctypes.POINTER(ctypes.c_long), _topscale: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить значения масштаба нижней и верхней границ видимости карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: номер пользовательской карты в цепочке (если number =``= 0``, базовая карта)
        
        :param _bottomscale: адрес для записи знаменателя масштаба нижней границы видимости карты
        
        :param _topscale: адрес для записи знаменателя масштаба верхней границы видимости карты
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return mapGetSiteRangeScaleVisible_t (_hmap, _number, _bottomscale, _topscale)

    mapSetSiteRangeScaleVisible_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSiteRangeScaleVisible', maptype.HMAP, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapSetSiteRangeScaleVisible(_hmap: maptype.HMAP, _number: int, _bottomscale: int, _topscale: int) -> int:
        """
        Установить значения масштаба нижней и верхней границ видимости карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _number: номер пользовательской карты в цепочке (если number =``= 0``, базовая карта)
        
        :param _bottomscale: знаменатель масштаба нижней границы видимости карты
        
        :param _topscale: знаменатель масштаба верхней границы видимости карты
        
        :returns: bottomscale <= topscale, иначе возвращает 0 При ошибке возвращает 0
        :rtype: int
        """
        return mapSetSiteRangeScaleVisible_t (_hmap, _number, _bottomscale, _topscale)

    mapGetMapPassportRecordLength_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMapPassportRecordLength', maptype.HMAP, maptype.HSITE)
    def mapGetMapPassportRecordLength(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить длину описания паспорта карты в виде записи
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMapPassportRecordLength_t (_hmap, _hsite)

    mapGetMapPassportRecord_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetMapPassportRecord', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.c_long)
    def mapGetMapPassportRecord(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _buffer: ctypes.c_char_p, _size: int) -> int:
        """
        Запросить описание паспорта карты в виде записи
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _buffer: указатель на запись для описания паспорта карты
        
        :param _size: размер записи Описание используется для передачи в другой процесс,на другой компьютер Передается описание только первого листа карты Размер буфера должен быть не менее, чем указано в mapGetMapPassportRecordLength
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetMapPassportRecord_t (_hmap, _hsite, _buffer, _size)

    mapPutMapPassportRecordUn_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapPutMapPassportRecordUn', maptype.HMAP, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_char_p, ctypes.c_long)
    def mapPutMapPassportRecordUn(_hmap: maptype.HMAP, _mapname: mapsyst.WTEXT, _rscname: mapsyst.WTEXT, _buffer: ctypes.c_char_p, _size: int) -> maptype.HSITE:
        """
        Создать карту по записи паспорта карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _mapname: имя файла паспорта (``*.map`` или ``*.sit``)
        
        :param _rscname: имя файла классификатора (``*.rsc``)
        
        :param _buffer: запись описания паспорта карты
        
        :param _size: размер записи Запись создается при вызове mapGetMapPassportRecord
        
        :returns: Если hmap ``= 0``, возвращает идентификатор открытых данных (документа) HMAP (mapCreateMap в mapapi.h) При ошибке возвращает ноль
        :rtype: maptype.HSITE
        """
        return mapPutMapPassportRecordUn_t (_hmap, _mapname.buffer(), _rscname.buffer(), _buffer, _size)

    mapGetSiteListFrameObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteListFrameObject', maptype.HMAP, maptype.HSITE, ctypes.c_long, maptype.HOBJ)
    def mapGetSiteListFrameObject(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _hobj: maptype.HOBJ) -> int:
        """
        Запросить объект "Рамка листа"
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _list: номер листа c ``1``
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteListFrameObject_t (_hmap, _hsite, _list, _hobj)

    mapGetSiteListFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteListFrame', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.POINTER(maptype.DFRAME))
    def mapGetSiteListFrame(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Запросить габариты объекта "Рамка листа"
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _list: номер листа
        
        :param _frame: указатель на габариты листа в метрах Eсли рамки нет, габариты объекта ``"Рамка листа"`` заполняются по габаритам из паспорта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteListFrame_t (_hmap, _hsite, _list, _frame)

    mapCreateSiteObjectEx_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapCreateSiteObjectEx', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapCreateSiteObjectEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _kind: int, _text: int, _pointcount: int) -> maptype.HOBJ:
        """
        Cоздать пустой объект пользовательской карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных, в которой будет расположен создаваемый объект (для первой карты равен hmap)
        
        :param _kind: формат метрики
        
        :param _text: признак метрики с текстом (для объектов типа ``"подпись"``)
        
        :param _pointcount: зарезервировать память под число точек (ускоряет первичное заполнение метрики из массива)
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HOBJ
        
        .. note::

           После вызова функций типа What... и Seek... все параметры
           полученного объекта могут измениться (text, kind и т.п.)
           Для каждого полученного и больше не используемого идентификатора HOBJ необходим вызов функции mapFreeObject
        """
        return mapCreateSiteObjectEx_t (_hmap, _hsite, _kind, _text, _pointcount)

    mapCreateSiteObject_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapCreateSiteObject', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long)
    def mapCreateSiteObject(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _kind: int, _text: int) -> maptype.HOBJ:
        """
        Cоздать пустой объект пользовательской карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных, в которой будет расположен создаваемый объект (для первой карты равен hmap)
        
        :param _kind: формат метрики
        
        :param _text: признак метрики с текстом (для объектов типа ``"подпись"``)
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HOBJ
        
        .. note::

           После вызова функций типа What... и Seek... все параметры
           полученного объекта могут измениться (text, kind и т.п.)
           Для каждого полученного и больше не используемого
           идентификатора HOBJ необходим вызов функции mapFreeObject
        """
        return mapCreateSiteObject_t (_hmap, _hsite, _kind, _text)

    mapGetObjectDocIdent_t = mapsyst.GetProcAddress(acceslib,maptype.HMAP,'mapGetObjectDocIdent', maptype.HOBJ)
    def mapGetObjectDocIdent(_hobj: maptype.HOBJ) -> maptype.HMAP:
        """
        Определить идентификатор открытого документа для заданного объекта
        
        :param _hobj: идентификатор объекта пользовательской карты
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HMAP
        """
        return mapGetObjectDocIdent_t (_hobj)

    mapGetObjectSiteIdent_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapGetObjectSiteIdent', maptype.HMAP, maptype.HOBJ)
    def mapGetObjectSiteIdent(_hmap: maptype.HMAP, _hobj: maptype.HOBJ) -> maptype.HSITE:
        """
        Определить идентификатор открытой векторной карты для заданного объекта
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hobj: идентификатор объекта пользовательской карты
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HSITE
        """
        return mapGetObjectSiteIdent_t (_hmap, _hobj)

    mapChangeObjectMap_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapChangeObjectMap', maptype.HOBJ, maptype.HMAP, maptype.HSITE)
    def mapChangeObjectMap(_hobj: maptype.HOBJ, _hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Перенести объект на другую карту (пересчитать координаты и заменить ссылку в объекте на карту)
        
        :param _hobj: идентификатор объекта пользовательской карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных При переносе объекта выполняется перекодировка объекта для нового классификатора, если код не найден - он устанавливается в ноль, прежнее значение сохраняется в семантике (код ``32800``) Для замены вызывается mapRegisterObject Метрика преобразуется в соответствии с типом карты Объект на исходной карте при этом не удаляется, для записи объекта в новой карте необходимо вызвать mapCommitObject
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapChangeObjectMap_t (_hobj, _hmap, _hsite)

    mapCompareSiteSystemParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCompareSiteSystemParameters', maptype.HMAP, maptype.HSITE, maptype.HMAP, maptype.HSITE)
    def mapCompareSiteSystemParameters(_hmap1: maptype.HMAP, _hsite1: maptype.HSITE, _hmap2: maptype.HMAP, _hsite2: maptype.HSITE) -> int:
        """
        Сравнить параметры системы координат двух карт
        
        :param _hmap1: идентификатор открытых данных
        
        :param _hsite1: идентификатор векторной карты в открытых данных
        
        :param _hmap2: идентификатор открытых данных
        
        :param _hsite2: идентификатор векторной карты в открытых данных
        
        :returns: При несовпадении каких-либо значений параметров возвращает ненулевое значение Некоторые несовпадающие параметры могут считаться идентичными (например, топографическая карта UTM и обзорно-географическая карта UTM) При ошибке возвращает ноль
        :rtype: int
        """
        return mapCompareSiteSystemParameters_t (_hmap1, _hsite1, _hmap2, _hsite2)

    mapClearSiteObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapClearSiteObject', maptype.HOBJ, maptype.HMAP, maptype.HSITE)
    def mapClearSiteObject(_hobj: maptype.HOBJ, _hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Очистить содержание объекта и разместить его на заданной карте
        
        :param _hobj: идентификатор объекта пользовательской карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapClearSiteObject_t (_hobj, _hmap, _hsite)

    mapGetSiteBorderEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteBorderEx', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.POINTER(maptype.DFRAME), ctypes.c_long)
    def mapGetSiteBorderEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _dframe: ctypes.POINTER(maptype.DFRAME), _place: int) -> int:
        """
        Запросить габариты пользовательской карты в системе координат документа
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _list: номер листа для многолистовой карты или ``0``
        
        :param _dframe: координаты прямоугольной области района
        
        :param _place: система координат (``PP_PLANE``, ``PP_GEO``, ``PP_PICTURE``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteBorderEx_t (_hmap, _hsite, _list, _dframe, _place)

    mapSetSiteBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSiteBorder', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.DFRAME), ctypes.c_long)
    def mapSetSiteBorder(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _dframe: ctypes.POINTER(maptype.DFRAME), _place: int) -> int:
        """
        Обновить размеры пользовательской карты и габариты района
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _dframe: координаты прямоугольной области района
        
        :param _place: система координат (``PP_PLANE``, ``PP_GEO``, ``PP_PICTURE``) Данная функция может применяться при создании карты, когда объектов еще нет и необходимо задать пустую область для окна карты При создании или обновлении объектов габариты пользовательской карты будут автоматически пересчитаны
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           После вызова этой функции необходимо согласовать параметры
           скроллинга подобно масштабированию карты
        """
        return mapSetSiteBorder_t (_hmap, _hsite, _dframe, _place)

    mapGetSiteMapBorder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteMapBorder', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.DFRAME))
    def mapGetSiteMapBorder(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _dframe: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Запросить габариты пользовательской карты в системе координат карты в метрах
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _dframe: координаты прямоугольной области района
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteMapBorder_t (_hmap, _hsite, _dframe)

    mapGetSiteObjectBorderReserve_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteObjectBorderReserve', maptype.HMAP, maptype.HSITE)
    def mapGetSiteObjectBorderReserve(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить приращение в метрах на местности, добавляемое при расчете габаритов объектов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных Пример: ``1`` мм на карте -``> 1``. ``00 *`` BaseScale / ``1000``.
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteObjectBorderReserve_t (_hmap, _hsite)

    mapGetSiteListReliefHeight_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetSiteListReliefHeight', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapGetSiteListReliefHeight(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int) -> float:
        """
        Запросить высоту сечения в метрах для листа из паспорта
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _list: номер листа
        
        :returns: При ошибке возвращает ноль
        :rtype: float
        """
        return mapGetSiteListReliefHeight_t (_hmap, _hsite, _list)

    mapChangeSiteRsc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapChangeSiteRsc', maptype.HMAP, maptype.HSITE, maptype.PWCHAR)
    def mapChangeSiteRsc(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _rscname: mapsyst.WTEXT) -> int:
        """
        Заменить файл классификатора и перекодировать карту
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _rscname: имя нового классификатора Поддерживается только для карт, размещенных локально и доступных на запись
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapChangeSiteRsc_t (_hmap, _hsite, _rscname.buffer())

    mapGetSiteRscName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteRscName', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_long)
    def mapGetSiteRscName(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _rscname: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить имя классификатора из паспорта карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _rscname: строка для записи имени классификатора без пути
        
        :param _size: размер строки для записи имени
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteRscName_t (_hmap, _hsite, _rscname.buffer(), _size)

    mapGetSiteRscStyle_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteRscStyle', maptype.HMAP, maptype.HSITE)
    def mapGetSiteRscStyle(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить состояние (стиль) классификатора из паспорта карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных При смене стиля могут быть изменены внутренние коды объектов Для проверки соответствия открытых данных классификатору можно сравнить этот показатель со значением в самом классификаторе (mapGetRscStyle)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteRscStyle_t (_hmap, _hsite)

    mapSetSiteDirectOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSiteDirectOrder', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSiteDirectOrder(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _flag: int) -> int:
        """
        Установить порядок записи объектов на карту в цепочку отображения в порядке их поступления
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _flag: признак последовательной записи и отображения объектов (``0``/``1``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Например, карта содержит один вид объектов
        """
        return mapSetSiteDirectOrder_t (_hmap, _hsite, _flag)

    mapGetSiteDirectOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteDirectOrder', maptype.HMAP, maptype.HSITE)
    def mapGetSiteDirectOrder(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить флаг записи объектов на карту в цепочку отображения в порядке их поступления
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке и выключенном режиме ``"прямой"`` записи возвращает ноль
        :rtype: int
        
        .. note::

           Например, карта содержит один вид объектов
        """
        return mapGetSiteDirectOrder_t (_hmap, _hsite)

    mapCheckCylindrical_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckCylindrical', maptype.HMAP, maptype.HSITE)
    def mapCheckCylindrical(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Проверить параметры системы координат карты на соответствие цилиндрической проекции
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Если параметры соответствуют цилиндрической проекции (Меркатора, Миллера ...) возвращает ненулевое значение
        :rtype: int
        """
        return mapCheckCylindrical_t (_hmap, _hsite)

    mapGetChangedObjectListAndUpdate_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapGetChangedObjectListAndUpdate', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapGetChangedObjectListAndUpdate(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _maxcount: int, _skipaction: int, _checkaction: int) -> ctypes.c_void_p:
        """
        Запросить список изменившихся на ГИС Сервере объектов и обновить описание объектов в памяти
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _maxcount: максимальное число измененных объектов, которое может быть в списке, если изменилось больше объектов, то список не формируется, а карта обновляется с ГИС Сервера полностью (обычно равен ``1000``)
        
        :param _skipaction: код транзакции, который не должен обрабатываться на ГИС Сервере при заполнении списка изменившихся объектов
        
        :param _checkaction: номер транзакции, с которой должен формироваться список изменившихся объектов. Это может быть значение, которое вернула функция mapGetChangedObjectAction или ``0``. Ноль означает формирование списка для текущего состояния (крайней транзакции, запомненной в предыдущем вызове обновления). Но вызов mapAdjust тоже обновляет состояние карты и номер последней транзакции в памяти карты.
        
        :returns: mapGetChangedObjectCount в этом случае возвращает ``"-1"`` Возвращает идентификатор списка объектов После обработки списка объектов он должен быть удален функцией mapFreeChangedObjectList При ошибке возвращает ноль
        """
        return mapGetChangedObjectListAndUpdate_t (_hmap, _hsite, _maxcount, _skipaction, _checkaction)

    mapGetChangedObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetChangedObjectCount', ctypes.c_void_p)
    def mapGetChangedObjectCount(_hObjlist: ctypes.c_void_p) -> int:
        """
        Запросить число объектов в списке
        
        :param _hObjlist: идентификатор списка объектов Число изменившихся объектов может быть нулевым
        
        :returns: заданого в функции mapGetChangedObjectListAndUpdate, то возвращается значение -1 и карта в памяти обновляется полностью Дополнительную информацию можно получить из журнала транзакций функциями из logapi.h
        :rtype: int
        
        .. note::

           Если число изменившихся объектов больше предельного значения maxcount,
        """
        return mapGetChangedObjectCount_t (_hObjlist)

    mapGetChangedObjectAction_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetChangedObjectAction', ctypes.c_void_p)
    def mapGetChangedObjectAction(_hObjlist: ctypes.c_void_p) -> int:
        """
        Запросить номер последней транзакции, по которой заполнен список объектов
        
        :param _hObjlist: идентификатор списка объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetChangedObjectAction_t (_hObjlist)

    mapGetChangedObjectTotalAction_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetChangedObjectTotalAction', ctypes.c_void_p)
    def mapGetChangedObjectTotalAction(_hObjlist: ctypes.c_void_p) -> int:
        """
        Запросить номер последней транзакции в журнале в момент формирования списка
        
        :param _hObjlist: идентификатор списка объектов Номер последней транзакции может быть больше номера обработанной транзакции, если список слишком большой В этом случае нужно запросить следующую порцию обновлений
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetChangedObjectTotalAction_t (_hObjlist)

    mapGetChangedObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetChangedObject', ctypes.c_void_p, ctypes.c_long, maptype.HMAP, maptype.HSITE, maptype.HOBJ)
    def mapGetChangedObject(_hObjlist: ctypes.c_void_p, _number: int, _hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ) -> int:
        """
        Запросить описание изменившегося объекта
        
        :param _hObjlist: идентификатор списка объектов
        
        :param _number: номер объекта в списке
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hobj: идентификатор объекта карты в памяти
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetChangedObject_t (_hObjlist, _number, _hmap, _hsite, _hobj)

    mapGetChangedObjectState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetChangedObjectState', ctypes.c_void_p, ctypes.c_long)
    def mapGetChangedObjectState(_hObjlist: ctypes.c_void_p, _number: int) -> int:
        """
        Запросить описание изменений объекта
        
        :param _hObjlist: идентификатор списка объектов
        
        :param _number: номер объекта в списке
        
        :returns: Возвращает признак изменений объекта: ``1`` - обновлена семантика, ``2`` - обновлена метрика, ``3`` - обновлена метрика и семантика, ``4`` - объект создан, ``8`` - объект удален, ``16`` - объект восстановлен после удаления Нулевое значение может означать изменение кода объекта, границ видимости, масштабируемости
        :rtype: int
        """
        return mapGetChangedObjectState_t (_hObjlist, _number)

    mapGetChangedObjectNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetChangedObjectNumber', ctypes.c_void_p, ctypes.c_long)
    def mapGetChangedObjectNumber(_hObjlist: ctypes.c_void_p, _number: int) -> int:
        """
        Запросить последовательный номер обновлённого объекта
        
        :param _hObjlist: идентификатор списка объектов
        
        :param _number: номер объекта в списке
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetChangedObjectNumber_t (_hObjlist, _number)

    mapGetChangedObjectCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetChangedObjectCode', ctypes.c_void_p, ctypes.c_long)
    def mapGetChangedObjectCode(_hObjlist: ctypes.c_void_p, _number: int) -> int:
        """
        Запросить код вида объекта, который был до обновления
        
        :param _hObjlist: идентификатор списка объектов
        
        :param _number: номер объекта в списке
        
        :returns: Возвращает внутренний код объекта в классификаторе У графических объектов код равен нулю
        :rtype: int
        """
        return mapGetChangedObjectCode_t (_hObjlist, _number)

    mapGetChangedObjectKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetChangedObjectKey', ctypes.c_void_p, ctypes.c_long)
    def mapGetChangedObjectKey(_hObjlist: ctypes.c_void_p, _number: int) -> int:
        """
        Запросить уникальный номер объекта в листе, который был до обновления
        
        :param _hObjlist: идентификатор списка объектов
        
        :param _number: номер объекта в списке В штатных ситуациях номер объекта не меняется при редактировании карты
        
        :returns: Возвращает идентификационный номер объекта (mapObjectKey)
        :rtype: int
        """
        return mapGetChangedObjectKey_t (_hObjlist, _number)

    mapFreeChangedObjectList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeChangedObjectList', ctypes.c_void_p)
    def mapFreeChangedObjectList(_hObjlist: ctypes.c_void_p) -> ctypes.c_void_p:
        """
        Освободить ресурсы, занятые списком объектов, созданным функцией mapGetChangedObjectListAndUpdate
        
        :param _hObjlist: идентификатор списка объектов
        """
        return mapFreeChangedObjectList_t (_hObjlist)

    mapGetSiteDateAndTime_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteDateAndTime', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapGetSiteDateAndTime(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _date: ctypes.POINTER(ctypes.c_long), _time: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить дату и время по Гринвичу обновления карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _list: номер листа карты
        
        :param _date: поле для записи даты в виде числа формата ``YYYYMMDD`` по Гринвичу
        
        :param _time: поле для записи числа секунд с ``0`` часов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если возвращаются нулевые значения, то карта после создания не редактировалась
        """
        return mapGetSiteDateAndTime_t (_hmap, _hsite, _list, _date, _time)

    mapGetCreateSiteDateAndTime_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetCreateSiteDateAndTime', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapGetCreateSiteDateAndTime(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _date: ctypes.POINTER(ctypes.c_long), _time: ctypes.POINTER(ctypes.c_long)) -> int:
        """
        Запросить дату и время по Гринвичу создания карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _list: номер листа карты
        
        :param _date: поле для записи даты в виде числа формата ``YYYYMMDD`` по Гринвичу
        
        :param _time: поле для записи числа секунд с ``0`` часов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetCreateSiteDateAndTime_t (_hmap, _hsite, _list, _date, _time)

    mapDeleteSiteDocumentUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteSiteDocumentUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR)
    def mapDeleteSiteDocumentUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _alias: mapsyst.WTEXT) -> int:
        """
        Удалить документ (произвольный файл) на сервере
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _alias: алиас документа на сервере (может храниться в семантике объекта карты, начинается со строки ``"HOST#"``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteSiteDocumentUn_t (_hmap, _hsite, _alias.buffer())

    mapReadSiteDocumentUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapReadSiteDocumentUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long)
    def mapReadSiteDocumentUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _alias: mapsyst.WTEXT, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Считать документ на сервере
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _alias: алиас документа на сервере (может храниться в семантике объекта карты, начинается со строки ``"HOST#"``) Например: ``HOST#WorkServer#ALIAS#Моя_Карта#DOC#MyFolder#schema.png``
        
        :param _name: полный путь к считанному документу, строка заполняется автоматически при считывании документа, имя документа и дата редактирования устанавливаются такими, какими они были при записи в mapSaveSiteDocument.
        
        :param _size: размер буфера в байтах для записи пути (не менее ``520`` байт)
        
        :returns: При успешном выполнении возвращает имя считанного файла документа в поле name При ошибке возвращает ноль
        :rtype: int
        """
        return mapReadSiteDocumentUn_t (_hmap, _hsite, _alias.buffer(), _name.buffer(), _size)

    mapReadSiteDocumentUnEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapReadSiteDocumentUnEx', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_long, maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def mapReadSiteDocumentUnEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _alias: mapsyst.WTEXT, _name: mapsyst.WTEXT, _size: int, _callevent: maptype.EVENTSTATE, _callparm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Считать документ на сервере
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _alias: алиас документа на сервере (может храниться в семантике объекта карты, начинается со строки ``"HOST#"``) Например: ``HOST#WorkServer#ALIAS#Моя_Карта#DOC#MyFolder#schema.png``
        
        :param _name: полный путь к считанному документу, строка заполняется автоматически при считывании документа, имя документа и дата редактирования устанавливаются такими, какими они были при записи в mapSaveSiteDocument.
        
        :param _size: размер буфера в байтах для записи пути (не менее ``520`` байт)
        
        :param _callevent: адрес функции обратного вызова для уведомления о проценте обработанных наборов данных (см. maptype.h)
        
        :param _callparm: адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы), вторым параметром в вызываемой функции передается процент от ``0`` до ``100``
        
        :returns: При успешном выполнении возвращает имя считанного файла документа в поле name При ошибке возвращает ноль
        :rtype: int
        """
        return mapReadSiteDocumentUnEx_t (_hmap, _hsite, _alias.buffer(), _name.buffer(), _size, _callevent, _callparm)

    mapReadSiteDocumentInfoUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapReadSiteDocumentInfoUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.POINTER(maptype.SYSTEMTIME), ctypes.POINTER(ctypes.c_int64))
    def mapReadSiteDocumentInfoUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _alias: mapsyst.WTEXT, _time: ctypes.POINTER(maptype.SYSTEMTIME), _size: ctypes.POINTER(ctypes.c_int64)) -> int:
        """
        Считать информацию о документе на сервере
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _alias: алиас документа на сервере
        
        :param _time: время обновления файла в хранилище
        
        :param _size: размер файла документа
        
        :returns: При успешном выполнении возвращает размер исходного файла и время его обновления в хранилище При ошибке возвращает ноль
        :rtype: int
        """
        return mapReadSiteDocumentInfoUn_t (_hmap, _hsite, _alias.buffer(), _time, _size)

    mapSaveSiteDocumentUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSaveSiteDocumentUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapSaveSiteDocumentUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _name: mapsyst.WTEXT, _alias: mapsyst.WTEXT, _size: int) -> int:
        """
        Сохранить документ на сервере
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _name: полный путь к сохраняемому документу (один файл любого размера)
        
        :param _alias: алиас документа на сервере (может храниться в семантике объекта карты, начинается со строки ``"HOST#"``), строка формируется сервером и заполняется при сохранении документа
        
        :param _size: размер буфера для записи алиаса (не менее ``260`` символов)
        
        :returns: При успешном выполнении возвращает алиас документа на сервере При ошибке возвращает ноль
        :rtype: int
        """
        return mapSaveSiteDocumentUn_t (_hmap, _hsite, _name.buffer(), _alias.buffer(), _size)

    mapGetSiteDocumentNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteDocumentNameUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, maptype.PWCHAR, ctypes.c_int)
    def mapGetSiteDocumentNameUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _alias: mapsyst.WTEXT, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить путь к кэшу документа на клиенте
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _alias: алиас документа на сервере (может храниться в семантике объекта карты, начинается со строки ``"HOST#"``)
        
        :param _name: полный путь к документу
        
        :param _size: размер буфера для записи пути (не менее ``260`` символов)
        
        :returns: При успешном выполнении возвращает имя кэша файла документа в поле name Операция чтения не выполняется, файл может отсутствовать При успешном выполнении возвращает ненулевое значение, если файл имеется в кэш - возвращает положительное значение, иначе - отрицательное При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteDocumentNameUn_t (_hmap, _hsite, _alias.buffer(), _name.buffer(), _size)

    mapIsSiteDocumentStorage_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsSiteDocumentStorage', maptype.HMAP, maptype.HSITE)
    def mapIsSiteDocumentStorage(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить - можно ли сохранить документ с картой
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если карта размещена на сервере и может редактироваться,
           то в ней есть хранилище документов
        """
        return mapIsSiteDocumentStorage_t (_hmap, _hsite)

    mapGetDocumentFromSitz_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetDocumentFromSitz', maptype.HMAP, maptype.HSITE, ctypes.c_long, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapGetDocumentFromSitz(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _name: mapsyst.WTEXT, _size: ctypes.POINTER(ctypes.c_long), _error: ctypes.POINTER(ctypes.c_long)) -> ctypes.POINTER(ctypes.c_char):
        """
        Считать документ из SITZ/MAPZ архива в память
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _list: номер листа, в котором записан документ
        
        :param _name: имя документа
        
        :param _size: указатель на размер считанного документа и выделенной памяти
        
        :param _error: код ошибки при неудаче (``IDS_PARM``, ``IDS_MEMORY``, ``IDS_READ``, ``IDS_FILE_NOT_FOUND``)
        
        :returns: Возвращает адрес документа в памяти При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetDocumentFromSitz_t (_hmap, _hsite, _list, _name.buffer(), _size, _error)

    mapGetDocumentFromSitzEx_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(ctypes.c_char),'mapGetDocumentFromSitzEx', maptype.HPAINT, maptype.PWCHAR, ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
    def mapGetDocumentFromSitzEx(_hPaint: maptype.HPAINT, _name: mapsyst.WTEXT, _size: ctypes.POINTER(ctypes.c_long), _error: ctypes.POINTER(ctypes.c_long)) -> ctypes.POINTER(ctypes.c_char):
        """
        Считать документ из SITZ/MAPZ архива в память
        
        hmap   - идентификатор открытых данных (документа)
        
        :param _hPaint: идентификатор контекста отображения для многопоточного вызова
        
        :param _name: имя документа
        
        :param _size: указатель на размер считанного документа и выделенной памяти
        
        :param _error: код ошибки при неудаче (``IDS_PARM``, ``IDS_MEMORY``, ``IDS_READ``, ``IDS_FILE_NOT_FOUND``)
        
        :returns: Возвращает адрес документа в памяти При ошибке возвращает ноль
        :rtype: ctypes.POINTER(ctypes.c_char)
        """
        return mapGetDocumentFromSitzEx_t (_hPaint, _name.buffer(), _size, _error)

    mapFreeDocumentFromSitz_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapFreeDocumentFromSitz', ctypes.c_char_p)
    def mapFreeDocumentFromSitz(_memory: ctypes.c_char_p) -> ctypes.c_void_p:
        """
        Освободить память с прочитанным документом
        
        :param _memory: адрес памяти, полученной при вызове mapGetDocumentFromSitz/mapGetDocumentFromSitzEx
        """
        return mapFreeDocumentFromSitz_t (_memory)

    mapPaintExampleSiteObjectPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPaintExampleSiteObjectPro', maptype.HMAP, maptype.HSITE, maptype.HDC, ctypes.POINTER(maptype.RECT), ctypes.c_long, maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(maptype.SEMANTIC))
    def mapPaintExampleSiteObjectPro(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hdc: maptype.HDC, _rect: ctypes.POINTER(maptype.RECT), _incode: int, _text: mapsyst.WTEXT, _factor: int, _semvalue: ctypes.POINTER(maptype.SEMANTIC)) -> int:
        """
        Отобразить образец вида объекта по номеру записи в классификаторе объектов (incode)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hdc: идентификатор контекста устройства вывода,
        
        :param _rect: координаты фрагмента карты (Draw) в изображении (Picture)
        
        :param _incode: внутренний код объекта
        
        :param _text: текст подписи или ноль
        
        :param _factor: коэффициент масштабируемости изображения ``50``, ``100``, ``200``...
        
        :param _semvalue: запись семантики Используется в диалогах выбора вида объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPaintExampleSiteObjectPro_t (_hmap, _hsite, _hdc, _rect, _incode, _text.buffer(), _factor, _semvalue)

    mapGetSiteViewSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteViewSelect', maptype.HMAP, maptype.HSITE, maptype.HSELECT)
    def mapGetSiteViewSelect(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT) -> int:
        """
        Запросить состав отображаемых объектов пользовательской карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hselect: идентификатор контекста поиска/отображения, в который будут помещены текущие условия отображения, создание в mapCreateMapSelectContext
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteViewSelect_t (_hmap, _hsite, _hselect)

    mapSetSiteViewSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'mapSetSiteViewSelect', maptype.HMAP, maptype.HSITE, maptype.HSELECT)
    def mapSetSiteViewSelect(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT) -> ctypes.c_void_p:
        """
        Установить состав отображаемых объектов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hselect: идентификатор контекста поиска/отображения
        """
        return mapSetSiteViewSelect_t (_hmap, _hsite, _hselect)

    mapGetSiteViewSelectState_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteViewSelectState', maptype.HMAP, maptype.HSITE)
    def mapGetSiteViewSelectState(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить номер состояния условий отображения карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных При обновлении условий номер состояния меняется
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteViewSelectState_t (_hmap, _hsite)

    mapGetSiteBright_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteBright', maptype.HMAP, maptype.HSITE)
    def mapGetSiteBright(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить яркость карты (от -16 до +16)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteBright_t (_hmap, _hsite)

    mapSetSiteBright_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSiteBright', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSiteBright(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _bright: int) -> int:
        """
        Установить яркость карты (от -16 до +16)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _bright: яркость карты
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetSiteBright_t (_hmap, _hsite, _bright)

    mapGetSiteContrast_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteContrast', maptype.HMAP, maptype.HSITE)
    def mapGetSiteContrast(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить контрастность  (от -16 до +16)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteContrast_t (_hmap, _hsite)

    mapSetSiteContrast_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSiteContrast', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSiteContrast(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _contrast: int) -> int:
        """
        Установить контрастность (от -16 до +16)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _contrast: контрастность
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetSiteContrast_t (_hmap, _hsite, _contrast)

    mapGetSiteGamma_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteGamma', maptype.HMAP, maptype.HSITE)
    def mapGetSiteGamma(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить параболическую яркость
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteGamma_t (_hmap, _hsite)

    mapSetSiteGamma_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSiteGamma', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSiteGamma(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _gamma: int) -> int:
        """
        Установить параболическую яркость
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _gamma: параболическая яркость
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetSiteGamma_t (_hmap, _hsite, _gamma)

    mapGetSiteColorsCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteColorsCount', maptype.HMAP, maptype.HSITE)
    def mapGetSiteColorsCount(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить число цветов в текущей палитре карты (обычно 16 или 32)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteColorsCount_t (_hmap, _hsite)

    mapGetSitePalette_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSitePalette', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.COLORREF), ctypes.c_long)
    def mapGetSitePalette(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _colors: ctypes.POINTER(maptype.COLORREF), _count: int) -> int:
        """
        Запросить текущую палитру карты (с учетом яркости/контрастности)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _colors: указатель на структуру ``COLORREF`` первого цвета в палитре
        
        :param _count: количество цветов (не более ``256``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSitePalette_t (_hmap, _hsite, _colors, _count)

    mapGetSiteColors_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteColors', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.COLORREF), ctypes.c_long)
    def mapGetSiteColors(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _colors: ctypes.POINTER(maptype.COLORREF), _count: int) -> int:
        """
        Запросить текущую палитру карты (без учета яркости/контрастности)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _colors: указатель на структуру ``COLORREF`` первого цвета в палитре
        
        :param _count: количество цветов (не более ``256``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteColors_t (_hmap, _hsite, _colors, _count)

    mapSetSiteColorsEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSiteColorsEx', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.COLORREF), ctypes.c_long, ctypes.c_long)
    def mapSetSiteColorsEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _colors: ctypes.POINTER(maptype.COLORREF), _count: int, _number: int) -> int:
        """
        Установить текущую палитру карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _colors: указатель на структуру ``COLORREF`` первого цвета в палитре
        
        :param _count: количество цветов (не более ``256``)
        
        :param _number: номер эталонной палитры в классификаторе
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если colors равно 0, устанавливается палитра из классификатора
           (палитра классификатора не меняется, изменения будут временными)
        """
        return mapSetSiteColorsEx_t (_hmap, _hsite, _colors, _count, _number)

    mapSetSitePaletteByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSitePaletteByNumber', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSitePaletteByNumber(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _number: int) -> int:
        """
        Установить текущую палитру в карте из классификатора
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _number: номер палитры в класификаторе
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetSitePaletteByNumber_t (_hmap, _hsite, _number)

    mapGetSitePaletteByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSitePaletteByNumber', maptype.HMAP, maptype.HSITE, ctypes.POINTER(maptype.COLORREF), ctypes.c_long, ctypes.c_long)
    def mapGetSitePaletteByNumber(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _colors: ctypes.POINTER(maptype.COLORREF), _count: int, _number: int) -> int:
        """
        Запросить палитру из классификатора по номеру
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _colors: указатель на структуру ``COLORREF`` первого цвета в палитре
        
        :param _count: количество цветов (не более ``256``)
        
        :param _number: номер палитры в класификаторе
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSitePaletteByNumber_t (_hmap, _hsite, _colors, _count, _number)

    mapGetSitePaletteNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSitePaletteNumber', maptype.HMAP, maptype.HSITE)
    def mapGetSitePaletteNumber(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить номер текущей палитры в карте
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSitePaletteNumber_t (_hmap, _hsite)

    mapGetSitePaletteCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSitePaletteCount', maptype.HMAP, maptype.HSITE)
    def mapGetSitePaletteCount(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить число палитр в классификаторе карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSitePaletteCount_t (_hmap, _hsite)

    mapGetSitePaletteName_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSitePaletteName', maptype.HMAP, maptype.HSITE, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetSitePaletteName(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _number: int, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить название палитры по номеру
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _name: адрес буфера для записи названия палитры
        
        :param _size: размер буфера для записи названия палитры
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSitePaletteName_t (_hmap, _hsite, _number, _name.buffer(), _size)

    mapGetSiteActiveSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteActiveSelect', maptype.HMAP, maptype.HSITE, maptype.HSELECT)
    def mapGetSiteActiveSelect(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT) -> int:
        """
        Запросить условия поиска активных объектов по карте
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hselect: идентификатор контекста поиска/отображения, в который будут помещены текущие условия поиска, создание в mapCreateMapSelectContext Активные объекты доступны для интерактивного выбора (оператором) Выбор выполняется функцией mapWhatActiveObject
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteActiveSelect_t (_hmap, _hsite, _hselect)

    mapSetSiteActiveSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSiteActiveSelect', maptype.HMAP, maptype.HSITE, maptype.HSELECT)
    def mapSetSiteActiveSelect(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT) -> int:
        """
        Установить условия поиска активных объектов для карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hselect: идентификатор контекста поиска, который содержит устанавливаемые условия поиска Активные объекты - доступны для интерактивного выбора (оператором) Выбор выполняется функцией mapWhatActiveObject
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetSiteActiveSelect_t (_hmap, _hsite, _hselect)

    mapGetSiteSeekSelect_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteSeekSelect', maptype.HMAP, maptype.HSITE, maptype.HSELECT)
    def mapGetSiteSeekSelect(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT) -> int:
        """
        Запросить условия поиска объектов по карте
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hselect: идентификатор контекста поиска/отображения, в который будут помещены текущие условия поиска, создание в mapCreateMapSelectContext
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteSeekSelect_t (_hmap, _hsite, _hselect)

    mapSetSiteSeekSelectEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSiteSeekSelectEx', maptype.HMAP, maptype.HSITE, maptype.HSELECT, ctypes.c_long)
    def mapSetSiteSeekSelectEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT, _keepsample: int) -> int:
        """
        Установить условия поиска объектов для карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hselect: идентификатор контекста поиска, который содержит устанавливаемые условия поиска
        
        :param _keepsample: признак сохранения в условиях поиска списка объектов (Sample)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetSiteSeekSelectEx_t (_hmap, _hsite, _hselect, _keepsample)

    mapSeekSiteObject_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapSeekSiteObject', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_long)
    def mapSeekSiteObject(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _key: int) -> maptype.HOBJ:
        """
        Поиск объекта по уникальному номеру на карте
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hobj: идентификатор существующего объекта, созданного функцией CreateObject или CreateSiteObject, в котором будет размещен результат поиска
        
        :param _key: уникальный номер объекта на карте
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HOBJ
        """
        return mapSeekSiteObject_t (_hmap, _hsite, _hobj, _key)

    mapSeekSiteSelectObjectEx_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapSeekSiteSelectObjectEx', maptype.HMAP, maptype.HSITE, maptype.HOBJ, maptype.HSELECT, ctypes.c_long, ctypes.c_long)
    def mapSeekSiteSelectObjectEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _hselect: maptype.HSELECT, _flag: int, _skip: int) -> maptype.HOBJ:
        """
        Поиск объектов по заданным условиям среди всех объектов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hobj: идентификатор существующего объекта, созданного функцией mapCreateObject или mapCreateSiteObject, в котором будет размещен результат поиска
        
        :param _hselect: условия поиска объекта
        
        :param _flag: порядок поиска объектов (``WO_FIRST``, ``WO_NEXT``...)
        
        :param _skip: число найденных объектов, которые нужно пропустить перед выдачей результата
        
        :returns: Если объект не найден - возвращает ноль
        :rtype: maptype.HOBJ
        """
        return mapSeekSiteSelectObjectEx_t (_hmap, _hsite, _hobj, _hselect, _flag, _skip)

    mapSeekSiteSelectNearestObjectEx_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapSeekSiteSelectNearestObjectEx', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), maptype.HSELECT, ctypes.c_int)
    def mapSeekSiteSelectNearestObjectEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _point: ctypes.POINTER(maptype.DOUBLEPOINT), _target: ctypes.POINTER(maptype.DOUBLEPOINT), _hselect: maptype.HSELECT, _flag: int) -> maptype.HOBJ:
        """
        Поиск ближайшего объекта по заданным условиям среди всех объектов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных в которой ищется объект
        
        :param _hobj: идентификатор существующего объекта созданного функцией mapCreateObject() или mapCreateSiteObject(), в котором будет размещен результат поиска
        
        :param _point: координаты точки в метрах в системе карты, среди всех подходящих объектов ищется ближайший к заданной точке
        
        :param _target: координаты ближайшей виртуальной точки на контуре объекта в метрах документа
        
        :param _hselect: условия поиска объекта
        
        :param _flag: дополнительные условия поиска объектов: ``WO_CANCEL``, ``WO_VISUAL``; флажки типа ``WO_FIRST``, ``WO_NEXT`` не учитываются
        
        :returns: Если объект не найден - возвращает ноль
        :rtype: maptype.HOBJ
        """
        return mapSeekSiteSelectNearestObjectEx_t (_hmap, _hsite, _hobj, _point, _target, _hselect, _flag)

    mapSeekSiteSelectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekSiteSelectCount', maptype.HMAP, maptype.HSITE, maptype.HSELECT)
    def mapSeekSiteSelectCount(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT) -> int:
        """
        Запросить число объектов, удовлетворяющих условиям поиска
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hselect: условия поиска объекта Для функции mapSeekSiteSelectObject (выполняет внутренний перебор объектов)
        
        :returns: При ошибке или отсутствии объектов возвращает ноль
        :rtype: int
        """
        return mapSeekSiteSelectCount_t (_hmap, _hsite, _hselect)

    mapSeekSiteSelectCountForList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekSiteSelectCountForList', maptype.HMAP, maptype.HSITE, maptype.HSELECT, ctypes.c_long)
    def mapSeekSiteSelectCountForList(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT, _list: int) -> int:
        """
        Запросить число объектов, удовлетворяющих условиям поиска в заданном листе
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hselect: условия поиска объекта
        
        :param _list: номер листа для многолистовой карты, с ``1``
        
        :returns: При ошибке или отсутствии объектов возвращает ноль
        :rtype: int
        """
        return mapSeekSiteSelectCountForList_t (_hmap, _hsite, _hselect, _list)

    mapSeekSiteViewObject_t = mapsyst.GetProcAddress(acceslib,maptype.HOBJ,'mapSeekSiteViewObject', maptype.HMAP, maptype.HSITE, maptype.HOBJ, maptype.HSELECT, ctypes.c_long)
    def mapSeekSiteViewObject(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _hselect: maptype.HSELECT, _flag: int) -> maptype.HOBJ:
        """
        Поиск объектов по заданным условиям среди отображаемых объектов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hobj: идентификатор существующего объекта, созданного функцией mapCreateObject или mapCreateSiteObject, в котором будет размещен результат поиска
        
        :param _hselect: условия поиска объекта
        
        :param _flag: порядок поиска объектов (``WO_FIRST``, ``WO_NEXT``...)
        
        :returns: Если объект не найден - возвращает ноль
        :rtype: maptype.HOBJ
        """
        return mapSeekSiteViewObject_t (_hmap, _hsite, _hobj, _hselect, _flag)

    mapSeekSiteViewCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSeekSiteViewCount', maptype.HMAP, maptype.HSITE, maptype.HSELECT)
    def mapSeekSiteViewCount(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT) -> int:
        """
        Запросить число объектов, удовлетворяющих условиям поиска
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hselect: условия поиска объекта Для функции mapSeekSiteSelectObject (выполняет внутренний перебор объектов)
        
        :returns: При ошибке или отсутствии объектов возвращает ноль
        :rtype: int
        """
        return mapSeekSiteViewCount_t (_hmap, _hsite, _hselect)

    mapCheckExistSemanticInSheetByCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCheckExistSemanticInSheetByCode', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long)
    def mapCheckExistSemanticInSheetByCode(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _code: int) -> int:
        """
        Проверить наличие кода семантики на карте
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _list: номер листа карты с ``1``
        
        :param _code: код семантики
        
        :returns: В случае отсутствия возвращает ноль
        :rtype: int
        """
        return mapCheckExistSemanticInSheetByCode_t (_hmap, _hsite, _list, _code)

    mapIsSemanticHashReady_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsSemanticHashReady', maptype.HMAP, maptype.HSITE)
    def mapIsSemanticHashReady(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Проверить что хэш семантик готов
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Если не готов - возвращает ``"-1"`` При ошибке возвращает ноль
        :rtype: int
        """
        return mapIsSemanticHashReady_t (_hmap, _hsite)

    mapGetSiteIdentForSelect_t = mapsyst.GetProcAddress(acceslib,maptype.HSITE,'mapGetSiteIdentForSelect', maptype.HMAP, maptype.HSELECT)
    def mapGetSiteIdentForSelect(_hmap: maptype.HMAP, _hselect: maptype.HSELECT) -> maptype.HSITE:
        """
        Запросить идентификатор карты, для которой созданы/заполнены условия поиска
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hselect: условия поиска объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HSITE
        """
        return mapGetSiteIdentForSelect_t (_hmap, _hselect)

    mapGetViewObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetViewObjectCount', maptype.HMAP, maptype.HSITE)
    def mapGetViewObjectCount(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить число отображаемых объектов на карте
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке или отсутствии объектов возвращает ноль
        :rtype: int
        """
        return mapGetViewObjectCount_t (_hmap, _hsite)

    mapGetTotalViewObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetTotalViewObjectCount', maptype.HMAP)
    def mapGetTotalViewObjectCount(_hmap: maptype.HMAP) -> int:
        """
        Запросить число отображаемых объектов в документе
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :returns: При ошибке или отсутствии объектов возвращает ноль
        :rtype: int
        """
        return mapGetTotalViewObjectCount_t (_hmap)

    mapIsSiteSeekSample_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsSiteSeekSample', maptype.HMAP, maptype.HSITE)
    def mapIsSiteSeekSample(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Опросить наличие списка объектов в контексте условий поиска/отображения карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных Список объектов содержит номер листа и номер объекта в листе
        
        :returns: Если список объектов не установлен,возвращает ноль
        :rtype: int
        """
        return mapIsSiteSeekSample_t (_hmap, _hsite)

    mapGetSiteObjectNumberByKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteObjectNumberByKey', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapGetSiteObjectNumberByKey(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _key: int) -> int:
        """
        Запросить последовательный номер объекта по его уникальному идентификатору
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _key: уникальный идентификатор объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteObjectNumberByKey_t (_hmap, _hsite, _key)

    mapGetSiteObjectKeyByNumberEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteObjectKeyByNumberEx', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def mapGetSiteObjectKeyByNumberEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _number: int, _list: int, _isdelete: int) -> int:
        """
        Запросить уникальный идентификатор объекта по последовательному номеру объекта
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _number: последовательный номер объекта
        
        :param _list: номер листа карты с ``1``
        
        :param _isdelete: признак учета удаленных объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteObjectKeyByNumberEx_t (_hmap, _hsite, _number, _list, _isdelete)

    mapGetSiteScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteScale', maptype.HMAP, maptype.HSITE)
    def mapGetSiteScale(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить базовый масштаб карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteScale_t (_hmap, _hsite)

    mapSetSiteScale_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSiteScale', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSiteScale(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _scale: int) -> int:
        """
        Изменить базовый масштаб пользовательской карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _scale: базовый масштаб При отображении в базовом масштабе пользовательской карты размер условных знаков на карте будет соответствовать их размеру в классификаторе ``RSC``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetSiteScale_t (_hmap, _hsite, _scale)

    mapGetSiteNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteNameUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_long)
    def mapGetSiteNameUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _name: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить главное название карты (листа)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _name: адрес строки для размещения результата
        
        :param _size: размер строки для размещения результата в байтах
        
        :returns: При ошибке возвращает пустую строку
        :rtype: int
        """
        return mapGetSiteNameUn_t (_hmap, _hsite, _name.buffer(), _size)

    mapSetSiteNameEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSiteNameEx', maptype.HMAP, maptype.HSITE, maptype.PWCHAR)
    def mapSetSiteNameEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _name: mapsyst.WTEXT) -> int:
        """
        Установить главное название карты (листа)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _name: главное название карты
        
        :returns: При ошибке возвращает пустую строку
        :rtype: int
        """
        return mapSetSiteNameEx_t (_hmap, _hsite, _name.buffer())

    mapGetSiteType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteType', maptype.HMAP, maptype.HSITE)
    def mapGetSiteType(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить тип карты (описание типов в maptype.h)
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteType_t (_hmap, _hsite)

    mapGetSiteX1_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetSiteX1', maptype.HMAP, maptype.HSITE)
    def mapGetSiteX1(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> float:
        """
        Запросить координату X юго-западного угла габаритов карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Возвращает координату в метрах на север в системе координат документа
        :rtype: float
        """
        return mapGetSiteX1_t (_hmap, _hsite)

    mapGetSiteY1_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetSiteY1', maptype.HMAP, maptype.HSITE)
    def mapGetSiteY1(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> float:
        """
        Запросить координату Y юго-западного угла габаритов карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Возвращает координату в метрах на восток в системе координат документа
        :rtype: float
        """
        return mapGetSiteY1_t (_hmap, _hsite)

    mapGetSiteX2_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetSiteX2', maptype.HMAP, maptype.HSITE)
    def mapGetSiteX2(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> float:
        """
        Запросить координату X северо-восточного угла габаритов карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Возвращает координату в метрах на север в системе координат документа
        :rtype: float
        """
        return mapGetSiteX2_t (_hmap, _hsite)

    mapGetSiteY2_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'mapGetSiteY2', maptype.HMAP, maptype.HSITE)
    def mapGetSiteY2(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> float:
        """
        Запросить координату Y северо-восточного угла габаритов карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Возвращает координату в метрах на восток в системе координат документа
        :rtype: float
        """
        return mapGetSiteY2_t (_hmap, _hsite)

    mapGetSiteObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteObjectCount', maptype.HMAP, maptype.HSITE)
    def mapGetSiteObjectCount(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить количество объектов в пользовательской карте
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteObjectCount_t (_hmap, _hsite)

    mapGetSiteRealObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteRealObjectCount', maptype.HMAP, maptype.HSITE)
    def mapGetSiteRealObjectCount(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить количество объектов в пользовательской карте, исключая удаленные
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteRealObjectCount_t (_hmap, _hsite)

    mapGetSiteDeleteObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteDeleteObjectCount', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapGetSiteDeleteObjectCount(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int) -> int:
        """
        Запросить количество удаленных объектов в листе карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _list: номер листа (для совместимости с многолистовыми картами)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteDeleteObjectCount_t (_hmap, _hsite, _list)

    mapGetSiteNewObjectKey_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteNewObjectKey', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapGetSiteNewObjectKey(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int) -> int:
        """
        Запросить идентификатор нового объекта, который будет создан на карте следующим
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _list: номер листа (для совместимости с многолистовыми картами) Идентификатор созданного объекта может быть запрошен функцией mapObjectKey
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteNewObjectKey_t (_hmap, _hsite, _list)

    mapGetSiteListCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteListCount', maptype.HMAP, maptype.HSITE)
    def mapGetSiteListCount(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить общее число листов на карте
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных (может быть равен hmap для доступа к основной карте)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteListCount_t (_hmap, _hsite)

    mapDeleteSiteList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteSiteList', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapDeleteSiteList(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int) -> int:
        """
        Удалить указанный лист карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _list: номер листа с ``1``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteSiteList_t (_hmap, _hsite, _list)

    mapSetSiteListOrder_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSiteListOrder', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long)
    def mapSetSiteListOrder(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _oldnumber: int, _newnumber: int) -> int:
        """
        Изменить порядковый номер листа карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _oldnumber: номер листа карты
        
        :param _newnumber: новое положение листа карты в паспорте
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetSiteListOrder_t (_hmap, _hsite, _oldnumber, _newnumber)

    mapGetSiteObjectCountInList_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteObjectCountInList', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapGetSiteObjectCountInList(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _number: int) -> int:
        """
        Запросить количество объектов в листе
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных (может быть равен hmap для доступа к основной карте)
        
        :param _number: номер листа карты (для пользовательской карты обычно равен ``1``)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteObjectCountInList_t (_hmap, _hsite, _number)

    mapGetSiteInfoPro_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteInfoPro', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(mapcreat.SHEETNAMES), ctypes.c_long)
    def mapGetSiteInfoPro(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _sheetnames: ctypes.POINTER(mapcreat.SHEETNAMES), _sheetnumber: int) -> int:
        """
        Запросить паспортные данные векторной карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _sheetnumber: номер листа карты c ``1`` Структуры ``MAPREGISTEREX``, ``LISTREGISTER``, ``SHEETNAMES`` описаны в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteInfoPro_t (_hmap, _hsite, _mapreg, _listreg, _sheetnames, _sheetnumber)

    mapUpdateSiteInfo_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapUpdateSiteInfo', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.LISTREGISTER), ctypes.POINTER(mapcreat.SHEETNAMES), maptype.PWCHAR, ctypes.c_long, ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_long, ctypes.POINTER(mapcreat.LOCALTRANSFORM), ctypes.c_long)
    def mapUpdateSiteInfo(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _listreg: ctypes.POINTER(mapcreat.LISTREGISTER), _sheetnames: ctypes.POINTER(mapcreat.SHEETNAMES), _mainname: mapsyst.WTEXT, _sheetnumber: int, _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparm: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _type: int, _parm: ctypes.POINTER(mapcreat.LOCALTRANSFORM), _transform: int) -> int:
        """
        Обновить паспортные данные векторной карты
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _mainname: главное название многолистовой карты (MAP), для пользовательской карты совпадает с названием листа карты
        
        :param _sheetnumber: номер листа карты c ``1``
        
        :param _type: тип локального преобразования координат (описан в ``TRANSFORMTYPE`` в mapcreat.h) или ``0``
        
        :param _parm: параметры локального преобразования координат или ``0``
        
        :param _transform: признак пересчета координат при смене параметров: ``0`` - не пересчитывать; ``1`` - пересчитать координаты объектов Структуры ``MAPREGISTEREX``, ``LISTREGISTER``, ``SHEETNAMES``, ``DATUMPARAM``, ``ELLIPSOIDPARAM``, ``LOCALTRANSFORM`` описаны в mapcreat.h При смене параметров проекции карта будет трансформирована в соответствии с новыми параметрами проекции из ``MAPREGISTEREX``, если параметр transform не равен нулю Для листа карты можно изменить название, номенклатуру и метаданные (``LISTREGISTER``), координаты рамки (если территория карты ограничена рамкой) пересчитываются автоматически Время выполнения функции соответствует времени выполнения трансформировании карты (при смене параметров проекции) При выполнении трансформирования посылается сообщение ``WM_PROGRESSBAR`` (maptype.h) окну (mapSetHandleForMessage)
        
        :returns: трансформирование карты - возвращает отрицательное значение, иначе - положительное При ошибке возвращает ноль
        :rtype: int
        
        .. note::

           Если при обновлении параметров проекции выполнялось
        """
        return mapUpdateSiteInfo_t (_hmap, _hsite, _mapreg, _listreg, _sheetnames, _mainname.buffer(), _sheetnumber, _datum, _ellparm, _type, _parm, _transform)

    mapSetSiteDatum_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSiteDatum', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapSetSiteDatum(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _parm: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        """
        Установить параметры Datum для карты
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных datum - параметры датума Структура ``DATUMPARAM`` описана в mapcreat.h Может выполняться или до записи объектов на карту или в другой момент - для карты хранящей геодезические координаты объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetSiteDatum_t (_hmap, _hsite, _parm)

    mapGetSiteDatum_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteDatum', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.DATUMPARAM))
    def mapGetSiteDatum(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _parm: ctypes.POINTER(mapcreat.DATUMPARAM)) -> int:
        """
        Запросить параметры Datum для карты
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных datum - параметры датума Структура ``DATUMPARAM`` описана в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteDatum_t (_hmap, _hsite, _parm)

    mapSetSiteEllipsoidParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSiteEllipsoidParameters', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapSetSiteEllipsoidParameters(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        """
        Установить параметры эллипсоида для карты
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _ellipsoid: параметры эллипсоида Структура ``ELLIPSOIDPARAM`` описана в mapcreat.h Может выполняться или до записи объектов на карту или в другой момент - для карты хранящей геодезические координаты объектов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetSiteEllipsoidParameters_t (_hmap, _hsite, _ellipsoid)

    mapGetSiteEllipsoidParameters_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteEllipsoidParameters', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.ELLIPSOIDPARAM))
    def mapGetSiteEllipsoidParameters(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _ellipsoid: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM)) -> int:
        """
        Запросить параметры эллипсоида для карты
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _ellipsoid: параметры эллипсоида Структура ``ELLIPSOIDPARAM`` описана в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteEllipsoidParameters_t (_hmap, _hsite, _ellipsoid)

    mapGetSiteLocalTransformationType_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteLocalTransformationType', maptype.HMAP, maptype.HSITE)
    def mapGetSiteLocalTransformationType(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить тип локального преобразования системы координат
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке или отсутствии преобразования возвращает ноль
        :rtype: int
        """
        return mapGetSiteLocalTransformationType_t (_hmap, _hsite)

    mapGetSiteLocalTransformationParm_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteLocalTransformationParm', maptype.HMAP, maptype.HSITE, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapGetSiteLocalTransformationParm(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _parm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        """
        Запросить адрес параметров локального преобразования системы координат
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _parm: параметры локального преобразования координат Структура ``LOCALTRANSFORM`` описана в mapcreat.h
        
        :returns: Возвращает тип локального преобразования системы координат При ошибке или отсутствии преобразования возвращает ноль
        :rtype: int
        """
        return mapGetSiteLocalTransformationParm_t (_hmap, _hsite, _parm)

    mapSetLocalTransformation_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetLocalTransformation', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.POINTER(mapcreat.LOCALTRANSFORM))
    def mapSetLocalTransformation(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _type: int, _parm: ctypes.POINTER(mapcreat.LOCALTRANSFORM)) -> int:
        """
        Установить параметры локального преобразования системы координат
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _type: тип локального преобразования координат (``TRANSFORMTYPE`` в mapcreat.h) или ``0``
        
        :param _parm: параметры локального преобразования координат Структура ``LOCALTRANSFORM`` описана в mapcreat.h
        
        :returns: При ошибке или отсутствии преобразования возвращает ноль
        :rtype: int
        """
        return mapSetLocalTransformation_t (_hmap, _hsite, _type, _parm)

    mapGetEPSGCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetEPSGCode', maptype.HMAP, maptype.HSITE)
    def mapGetEPSGCode(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить код EPSG системы координат
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetEPSGCode_t (_hmap, _hsite)

    mapSetEPSGCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetEPSGCode', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetEPSGCode(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _code: int) -> int:
        """
        Установить код EPSG системы координат
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _code: код ``EPSG``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetEPSGCode_t (_hmap, _hsite, _code)

    mapGetCRSIdentUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetCRSIdentUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.c_long)
    def mapGetCRSIdentUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _ident: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить идентификатор системы координат
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _ident: строка длиной не менее ``64`` символов для размещения идентификатора
        
        :param _size: длина строки
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetCRSIdentUn_t (_hmap, _hsite, _ident.buffer(), _size)

    mapSetCRSIdentUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetCRSIdentUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR)
    def mapSetCRSIdentUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _ident: mapsyst.WTEXT) -> int:
        """
        Установить идентификатор системы координат
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _ident: строка со значением идентификатора не более ``64`` символов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetCRSIdentUn_t (_hmap, _hsite, _ident.buffer())

    mapGetDataIdent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetDataIdent', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_char_p, ctypes.c_long)
    def mapGetDataIdent(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _ident: ctypes.c_char_p, _size: int) -> int:
        """
        Запросить идентификатор набора данных листа карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _list: номер листа карты с ``1`` или ``0`` (запрос или установка идентификатора набора листов) для пользовательской карты list равен ``1``
        
        :param _ident: строка длиной не менее ``33`` символов для размещения идентификатора
        
        :param _size: длина строки Для чтения значения необходимо подать буфер не менее ``33`` символов (``32`` + ``1`` для замыкающего нуля)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetDataIdent_t (_hmap, _hsite, _list, _ident, _size)

    mapSetDataIdent_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetDataIdent', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_char_p)
    def mapSetDataIdent(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _list: int, _ident: ctypes.c_char_p) -> int:
        """
        Установить идентификатор набора данных листа карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _list: номер листа карты с ``1`` или ``0`` (запрос или установка идентификатора набора листов) для пользовательской карты list равен ``1``
        
        :param _ident: строка со значением идентификатора (обычно ``32`` шестнадцатеричных символа ``GUID`` и замыкающий ноль) При записи будут записаны не более ``32`` символов
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetDataIdent_t (_hmap, _hsite, _list, _ident)

    mapGetSiteSecurityCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteSecurityCode', maptype.HMAP, maptype.HSITE)
    def mapGetSiteSecurityCode(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить гриф секретности карты
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных code  - код степени секретности данных: ``1`` - открытая информация (unclassified), ``2`` - информация с ограниченным доступом (restricted), ``3`` - информация для служебного пользования (confidential), ``4`` - секретная информация (secret), ``5`` - совершенно секретная информация (topsecret)
        
        :returns: При ошибке или отсутствии значения возвращает ноль
        :rtype: int
        """
        return mapGetSiteSecurityCode_t (_hmap, _hsite)

    mapSetSiteSecurityCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSiteSecurityCode', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSiteSecurityCode(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _code: int) -> int:
        """
        Установить гриф секретности карты
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _code: код степени секретности данных: ``1`` - открытая информация (unclassified), ``2`` - информация с ограниченным доступом (restricted), ``3`` - информация для служебного пользования (confidential), ``4`` - секретная информация (secret), ``5`` - совершенно секретная информация (topsecret)
        
        :returns: При ошибке или отсутствии значения возвращает ноль
        :rtype: int
        """
        return mapSetSiteSecurityCode_t (_hmap, _hsite, _code)

    mapGetSitePaperSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSitePaperSize', maptype.HMAP, maptype.HSITE)
    def mapGetSitePaperSize(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить формат рамки листа для плана
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: Возвращает: ``0`` -  не установлен, ``1`` - установлен пользователем, ``2`` - A0(841x1189 мм), ``3`` - A1(594x841 мм),           ``4`` - A2(420x594 мм), ``5`` - A3(297x420 мм),           ``6`` - A4(210x297 мм) При ошибке или отсутствии значения возвращает ноль
        :rtype: int
        """
        return mapGetSitePaperSize_t (_hmap, _hsite)

    mapSetSitePaperSize_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSitePaperSize', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSetSitePaperSize(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _size: int) -> int:
        """
        Установить формат рамки листа для плана
        
        :param _hmap: идентификатор открытых данных
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _size: формат рамки листа: ``0`` -  не установлен, ``1`` - установлен пользователем,  ``2`` - ``A0`` (841x1189 мм), ``3`` - ``A1`` (594x841 мм),           ``4`` - ``A2`` (420x594 мм), ``5`` - ``A3`` (297x420 мм),           ``6`` - ``A4`` (210x297 мм)
        
        :returns: При ошибке или отсутствии значения возвращает ноль
        :rtype: int
        """
        return mapSetSitePaperSize_t (_hmap, _hsite, _size)

    mapGetSiteUsedSelectEx_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteUsedSelectEx', maptype.HMAP, maptype.HSITE, maptype.HSELECT, ctypes.c_long)
    def mapGetSiteUsedSelectEx(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hselect: maptype.HSELECT, _force: int) -> int:
        """
        Запросить сведения о реально имеющихся объектах на карте
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hselect: идентификатор контекста поиска, в который будут помещены условия, соответствующие имеющимся объектам (слои, объекты, локализации - доступ в seekapi.h)
        
        :param _force: признак принудительного обновления состава условий поиска по реально имеющимся на карте объектам (для больших карт длительное выполнение)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteUsedSelectEx_t (_hmap, _hsite, _hselect, _force)

    mapIsUsedSelectActive_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapIsUsedSelectActive', maptype.HMAP, maptype.HSITE)
    def mapIsUsedSelectActive(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить установлены ли сведения об имеющихся объектах
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: возвращает ноль, иначе - ненулевое значение
        :rtype: int
        
        .. note::

           Если по условиям поиска все объекты выбираются без исключений -
        """
        return mapIsUsedSelectActive_t (_hmap, _hsite)

    mapTransformationSite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapTransformationSite', maptype.HMAP, maptype.HSITE, maptype.HMESSAGE, maptype.PWCHAR, ctypes.POINTER(mapcreat.MAPREGISTEREX), ctypes.POINTER(mapcreat.DATUMPARAM), ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), ctypes.c_long, ctypes.POINTER(mapcreat.LOCALTRANSFORM), ctypes.c_long, ctypes.POINTER(ctypes.c_long), maptype.EVENTSTATE, ctypes.POINTER(ctypes.c_void_p))
    def mapTransformationSite(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hmessage: maptype.HMESSAGE, _mapname: mapsyst.WTEXT, _mapreg: ctypes.POINTER(mapcreat.MAPREGISTEREX), _datum: ctypes.POINTER(mapcreat.DATUMPARAM), _ellparam: ctypes.POINTER(mapcreat.ELLIPSOIDPARAM), _ttype: int, _tparm: ctypes.POINTER(mapcreat.LOCALTRANSFORM), _issavecopy: int, _error: ctypes.POINTER(ctypes.c_long), _callevent: maptype.EVENTSTATE, _callparm: ctypes.POINTER(ctypes.c_void_p)) -> int:
        """
        Трансформировать векторную карту в заданную систему координат
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hmessage: идентификатор окна (``HWND``/функция обратного вызова в Linux) для получения сообщений ``WM_PROGRESSBARUN`` или ``0``
        
        :param _mapname: имя создаваемой карты в заданной системе координат
        
        :param _mapreg: структура параметров системы координат карты
        
        :param _ellparam: параметры эллипсоида (необязательный параметр)
        
        :param _datum: параметры ``DATUM`` для карты (необязательный параметр)
        
        :param _ttype: тип локального преобразования координат (``TRANSFORMTYPE`` в mapcreat.h) или ``0``
        
        :param _tparm: параметры локального преобразования координат или ``0``
        
        :param _issavecopy: признак создания копии исходной карты в поддиректории ИМЯКАРТЫ.``YYYYMMDD``.``HHMMSS``
        
        :param _error: код ошибки при выполнении трансформирвоания
        
        :param _callevent: адрес функции обратного вызова для уведомления о проценте обработанных наборов данных (maptype.h) parm       - адрес параметров, которые будут переданы при вызове функции (обычно адрес класса управляющей программы), вторым параметром в вызываемой функции передается процент от ``0`` до ``100`` Структуры ``MAPREGISTEREX``, ``DATUMPARAM``, ``ELLIPSOIDPARAM``, ``LOCALTRANSFORM`` описаны в mapcreat.h
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapTransformationSite_t (_hmap, _hsite, _hmessage, _mapname.buffer(), _mapreg, _datum, _ellparam, _ttype, _tparm, _issavecopy, _error, _callevent, _callparm)

    mapChangeXY_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapChangeXY', maptype.HMAP, maptype.HSITE)
    def mapChangeXY(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Сменить координатные оси между собой
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных Не может быть выполнено для карты, ограниченной рамкой
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapChangeXY_t (_hmap, _hsite)

    mapGetSiteLayerCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteLayerCount', maptype.HMAP, maptype.HSITE)
    def mapGetSiteLayerCount(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить число слоев на карте
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteLayerCount_t (_hmap, _hsite)

    mapGetSiteLayerNameUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapGetSiteLayerNameUn', maptype.HMAP, maptype.HSITE, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapGetSiteLayerNameUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _layer: int, _layername: mapsyst.WTEXT, _namesize: int) -> int:
        """
        Запросить название слоя по его номеру
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _layer: номер слоя
        
        :param _layername: адрес буфера для записи названия слоя
        
        :param _namesize: размер буфера для возвращаемой строки в байтах Номер первого слоя ``0``
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapGetSiteLayerNameUn_t (_hmap, _hsite, _layer, _layername.buffer(), _namesize)

    mapSiteRscObjectCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSiteRscObjectCount', maptype.HMAP, maptype.HSITE)
    def mapSiteRscObjectCount(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Запросить число объектов описанных в классификаторе
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSiteRscObjectCount_t (_hmap, _hsite)

    mapSiteRscObjectCountInLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSiteRscObjectCountInLayer', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapSiteRscObjectCountInLayer(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _layer: int) -> int:
        """
        Запросить число объектов описанных в классификаторе в заданном слое
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _layer: номер слоя
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSiteRscObjectCountInLayer_t (_hmap, _hsite, _layer)

    mapSiteRscObjectNameInLayerUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSiteRscObjectNameInLayerUn', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def mapSiteRscObjectNameInLayerUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _layer: int, _number: int, _objectname: mapsyst.WTEXT, _namesize: int) -> int:
        """
        Запросить название объекта по порядковому номеру в заданном слое
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _layer: номер слоя
        
        :param _number: номер объекта в слое
        
        :param _objectname: адрес буфера для записи названия объекта
        
        :param _namesize: размер буфера для возвращаемой строки в байтах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSiteRscObjectNameInLayerUn_t (_hmap, _hsite, _layer, _number, _objectname.buffer(), _namesize)

    mapSiteRscObjectExcodeInLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSiteRscObjectExcodeInLayer', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long)
    def mapSiteRscObjectExcodeInLayer(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _layer: int, _number: int) -> int:
        """
        Запросить классификационный код объекта по порядковому номеру в заданном слое
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _layer: номер слоя
        
        :param _number: номер объекта в слое
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSiteRscObjectExcodeInLayer_t (_hmap, _hsite, _layer, _number)

    mapSiteRscObjectLocalInLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSiteRscObjectLocalInLayer', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long)
    def mapSiteRscObjectLocalInLayer(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _layer: int, _number: int) -> int:
        """
        Запросить код локализации объекта по порядковому номеру в заданном слое
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _layer: номер слоя
        
        :param _number: номер объекта в слое
        
        :returns: При ошибке возвращает ноль (ноль допустим)
        :rtype: int
        """
        return mapSiteRscObjectLocalInLayer_t (_hmap, _hsite, _layer, _number)

    mapSiteRscObjectCodeInLayer_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSiteRscObjectCodeInLayer', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long)
    def mapSiteRscObjectCodeInLayer(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _layer: int, _number: int) -> int:
        """
        Запросить внутренний код (индекс) объекта по порядковому номеру в заданном слое
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _layer: номер слоя
        
        :param _number: номер объекта в слое
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSiteRscObjectCodeInLayer_t (_hmap, _hsite, _layer, _number)

    mapSiteRscObjectCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSiteRscObjectCode', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long)
    def mapSiteRscObjectCode(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _excode: int, _local: int) -> int:
        """
        Запросить внутренний код (индекс) объекта по внешнему коду и локализации
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _excode: внешний код объекта
        
        :param _local: локализация объекта
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSiteRscObjectCode_t (_hmap, _hsite, _excode, _local)

    mapDeleteSiteObjectByNumber_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapDeleteSiteObjectByNumber', maptype.HMAP, maptype.HSITE, ctypes.c_long)
    def mapDeleteSiteObjectByNumber(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _number: int) -> int:
        """
        Удалить объект карты по его последовательному номеру
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _number: последовательный номер объекта Для отмены удаления применяются mapUndeleteObjectByNumber и mapUndeleteObject
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapDeleteSiteObjectByNumber_t (_hmap, _hsite, _number)

    mapRestoreBackObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapRestoreBackObject', maptype.HMAP, maptype.HSITE, maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def mapRestoreBackObject(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _hobj: maptype.HOBJ, _date: int, _time: int) -> int:
        """
        Восстановить копию объекта по дате и времени выполнения транзакции
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hobj: идентификатор существующего объекта, созданного функцией CreateObject или CreateSiteObject и прочитанного функцией mapReadObjectByNumber или mapReadObjectByKey, в котором будет размещен результат восстановления
        
        :param _date: дата в формате ``"YYYYMMDD"``
        
        :param _time: время в формате ``"число секунд от 00:00:00"`` (по Гринвичу - GetSystemTime, in Coordinated Universal Time (``UTC``))
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapRestoreBackObject_t (_hmap, _hsite, _hobj, _date, _time)

    mapCreateSiteSelectContext_t = mapsyst.GetProcAddress(acceslib,maptype.HSELECT,'mapCreateSiteSelectContext', maptype.HMAP, maptype.HSITE)
    def mapCreateSiteSelectContext(_hmap: maptype.HMAP, _hsite: maptype.HSITE) -> maptype.HSELECT:
        """
        Создать контекст (описание условий) поиска или отображения объектов карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных В состав условий отбора объектов входят : слой, локализация, диапазон номеров объектов, характеристики (семантика) объекта, область расположения (метрика) объекта В созданном контексте доступны все объекты карты без исключений Запрашивается минимум ``10`` Кб памяти, если заданы условия поиска по метрике и семантике - до ``300`` Кб Каждый созданный контекст должен быть удален функцией mapDeleteSelectContext, когда он больше не используется
        
        :returns: При ошибке возвращает ноль
        :rtype: maptype.HSELECT
        """
        return mapCreateSiteSelectContext_t (_hmap, _hsite)

    mapSetSelectContextSite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapSetSelectContextSite', maptype.HSELECT, maptype.HMAP, maptype.HSITE)
    def mapSetSelectContextSite(_hselect: maptype.HSELECT, _hmap: maptype.HMAP, _hsite: maptype.HSITE) -> int:
        """
        Связать контекст условий поиска с другой картой
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _hselect: идентификатор контекста поиска/отображения Все условия поиска автоматически сбрасываются
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapSetSelectContextSite_t (_hselect, _hmap, _hsite)

    mapAddMarginalRepresentationSite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAddMarginalRepresentationSite', maptype.HMAP, maptype.HSITE, ctypes.c_char_p, ctypes.POINTER(maptype.DFRAME))
    def mapAddMarginalRepresentationSite(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _frmname: ctypes.c_char_p, _frame: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Добавить зарамочное оформление в пользовательскую карту
        
        :param _hmap: идентификатор основной векторной карты
        
        :param _hsite: идентификатор пользовательской карты
        
        :param _frmname: полное имя файла шаблона зарамочного оформления (``*.frm``)
        
        :param _frame: габариты внутреннего контура зарамочного оформления в метрах
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapAddMarginalRepresentationSite_t (_hmap, _hsite, _frmname, _frame)

    mapAddMarginalRepresentationSiteUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapAddMarginalRepresentationSiteUn', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.POINTER(maptype.DFRAME), ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapAddMarginalRepresentationSiteUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _frmname: mapsyst.WTEXT, _frame: ctypes.POINTER(maptype.DFRAME), _angle: float, _center: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Добавить зарамочное оформление в пользовательскую карту
        
        :param _hmap: идентификатор основной векторной карты
        
        :param _hsite: идентификатор пользовательской карты
        
        :param _frmname: полное имя файла шаблона зарамочного оформления (``*.frm``)
        
        :param _frame: габариты внутреннего контура зарамочного оформления в метрах
        
        :param _angle: угол поворота (если есть)
        
        :param _center: центр поворота (если есть угол)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapAddMarginalRepresentationSiteUn_t (_hmap, _hsite, _frmname.buffer(), _frame, _angle, _center)

    mapCreateLineSite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateLineSite', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapCreateLineSite(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _excode: int, _x1: float, _y1: float, _x2: float, _y2: float, _angle: float, _center: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Нанести линию заданного кода на пользовательскую карту
        
        :param _hmap: идентификатор открытой векторной карты
        
        :param _hsite: идентификатор пользовательской карты
        
        :param _excode: код линии x1,y1,x2,y2 - координаты первой и второй точек в метрах
        
        :param _angle: угол поворота (если есть)
        
        :param _center: центр поворота (если есть угол)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCreateLineSite_t (_hmap, _hsite, _excode, _x1, _y1, _x2, _y2, _angle, _center)

    mapCreateFrameFillSite_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateFrameFillSite', maptype.HMAP, maptype.HSITE, ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.POINTER(maptype.DFRAME), ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapCreateFrameFillSite(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _framecode: int, _fillcode: int, _linecode: int, _delta: float, _frame: ctypes.POINTER(maptype.DFRAME), _angle: float, _center: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Создать рамку для зарамочного оформления на пользовательской карте
        
        :param _hmap: идентификатор открытой векторной карты
        
        :param _hsite: идентификатор пользовательской карты
        
        :param _framecode: код внутренней рамки
        
        :param _fillcode: код заполнения
        
        :param _linecode: код внешней рамки
        
        :param _delta: расстояние от внутренней до внешней рамки в метрах
        
        :param _frame: габариты внутренней рамки в м
        
        :param _angle: угол поворота (если есть)
        
        :param _center: центр поворота (если есть угол)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCreateFrameFillSite_t (_hmap, _hsite, _framecode, _fillcode, _linecode, _delta, _frame, _angle, _center)

    mapCreateTitleSiteUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateTitleSiteUn', maptype.HMAP, maptype.HSITE, ctypes.c_long, maptype.PWCHAR, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long, ctypes.c_double, ctypes.POINTER(maptype.DOUBLEPOINT))
    def mapCreateTitleSiteUn(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _excode: int, _text: mapsyst.WTEXT, _x1: float, _y1: float, _x2: float, _y2: float, _wide: int, _vert: int, _angle: float, _center: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Нанести текст заданного кода на пользовательскую карту
        
        :param _hmap: идентификатор открытой векторной карты
        
        :param _hsite: идентификатор пользовательской карты
        
        :param _excode: код текста подписи
        
        :param _text: текст подписи x1,x2,y1,y2 - координаты первой и второй точек в метрах
        
        :param _wide: выравнивание по горизонтали: ``UNIA_LEFT`` - по левому краю, ``UNIA_CENTER`` - по центру, ``UNIA_RIGHT`` - по правому краю
        
        :param _vert: наличие выравнивания по вертикали (``0`` или ``1``)
        
        :param _angle: угол поворота (если есть)
        
        :param _center: центр поворота (если есть угол)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCreateTitleSiteUn_t (_hmap, _hsite, _excode, _text.buffer(), _x1, _y1, _x2, _y2, _wide, _vert, _angle, _center)

    mapPreSscanfUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPreSscanfUn', maptype.PWCHAR, ctypes.c_int, ctypes.c_char)
    def mapPreSscanfUn(_string: mapsyst.WTEXT, _length: int, _simbol: int) -> int:
        """
        Замена буквы 'я' на спецсимвол перед тем как разобрать строку функцией sscanf
        
        :param _string: строка
        
        :param _length: длина строки
        
        :param _simbol: спецсимвол (если =``= 0`` - то заменяет 'я' на '^')
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPreSscanfUn_t (_string.buffer(), _length, _simbol)

    mapPostSscanfUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapPostSscanfUn', maptype.PWCHAR, ctypes.c_int, ctypes.c_char)
    def mapPostSscanfUn(_string: mapsyst.WTEXT, _length: int, _simbol: int) -> int:
        """
        Замена спецсимвола на 'я' после разбора строки функцией sscanf
        
        :param _string: строка
        
        :param _length: длина строки
        
        :param _simbol: спецсимвол (если =``= 0`` - то заменяет '^' на 'я')
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapPostSscanfUn_t (_string.buffer(), _length, _simbol)

    mapCreateLegend_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'mapCreateLegend', maptype.HMAP, maptype.HSITE, maptype.PWCHAR, ctypes.POINTER(mapgdi.LEGENDESC), maptype.HSELECT, ctypes.POINTER(ctypes.c_int))
    def mapCreateLegend(_hmap: maptype.HMAP, _hsite: maptype.HSITE, _outname: mapsyst.WTEXT, _desc: ctypes.POINTER(mapgdi.LEGENDESC), _hselect: maptype.HSELECT, _error: ctypes.POINTER(ctypes.c_int)) -> int:
        """
        Функция создания легенды карты
        
        :param _hmap: идентификатор открытых данных (документа)
        
        :param _hsite: идентификатор векторной карты в открытых данных
        
        :param _outname: полное имя файла выходной карты-легенды
        
        :param _desc: параметры легенды (фон, подпись, контур; описана в mapgdi.h)
        
        :param _hselect: контекст отбора слоев\\объектов карты для формирования легенды (необязательный параметр, может быть равен нулю)
        
        :param _error: код ошибки при построении легенды (необязательный параметр, может быть равен нулю, коды в maperr.rh)
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return mapCreateLegend_t (_hmap, _hsite, _outname.buffer(), _desc, _hselect, _error)



def sitapi_healthcheck():
    return 1
