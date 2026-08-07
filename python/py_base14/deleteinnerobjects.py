# -*- coding: utf-8 -*-
"""
Удаление объектов карты, полностью расположенных внутри объектов другой.

Скрипт предназначен для запуска из ГИС «Панорама» с Python 3.5 и
модулями py_mapapi14 из штатной поставки.
"""

import ctypes
import datetime
import os
import webbrowser
import xml.etree.ElementTree as elementTree
import tkinter
import tkinter.ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename

import mapapi
import maperr
import mapsyst
import maptype
import rscapi
import seekapi
import sitapi


TITLE = u'Удаление объектов внутри объектов другой карты'
SECTION = u'DELETEINNEROBJECTS'
BUFFER_SIZE = 4096
HELP_URL = u'https://help.gisserver.ru/v15/russian/mapscena/index.html?idn4.html'
LOG_PREFIX = u'TPythonScript::DeleteInnerObjects(): '


def WriteLog(message, details=u'', messageType=None):
    """Пишет сообщение в диагностический протокол Панорамы."""
    try:
        if messageType is None:
            messageType = maptype.MT_INFO
        mapapi.mapWriteToDiagnosticsLog(
            mapsyst.WTEXT(LOG_PREFIX + message),
            mapsyst.WTEXT(details), messageType)
    except Exception:
        pass


def ShowMessage(text, warning=False, parent=None):
    WriteLog(
        u'Сообщение пользователю: {0}'.format(text), u'',
        maptype.MT_WARNING if warning else maptype.MT_INFO)
    style = maptype.MB_WARNING if warning else maptype.MB_OK
    window = 0
    try:
        if parent is not None and parent.winfo_exists():
            # Главное окно больше не перекрывает модальное сообщение.
            parent.wm_attributes('-topmost', 0)
            window = parent.winfo_id()
        mapapi.mapMessageBoxUn(
            window, mapsyst.WTEXT(text), mapsyst.WTEXT(TITLE), style)
    finally:
        try:
            if parent is not None and parent.winfo_exists():
                parent.wm_attributes('-topmost', 1)
                parent.lift()
                parent.focus_force()
        except Exception:
            pass


def GetIniFileName(hmap):
    iniName = mapsyst.WTEXT(BUFFER_SIZE)
    if mapapi.mapGetMapIniNameUn(hmap, iniName, iniName.size()) == 0:
        return u''
    return iniName.string()


def ReadIniValue(iniName, section, key, defaultValue=u''):
    if not iniName:
        return defaultValue
    try:
        value = ctypes.create_unicode_buffer(BUFFER_SIZE)
        length = ctypes.windll.kernel32.GetPrivateProfileStringW(
            section, key, defaultValue, value, BUFFER_SIZE, iniName)
        if length == 0:
            return defaultValue
        return value.value
    except Exception:
        return defaultValue


def ReadSetting(iniName, key, defaultValue=u''):
    return ReadIniValue(iniName, SECTION, key, defaultValue)


def WriteSettings(iniName, settings):
    if not iniName:
        return
    try:
        for key, value in settings.items():
            ctypes.windll.kernel32.WritePrivateProfileStringW(
                SECTION, key, value, iniName)
    except Exception:
        pass


def GetOpenMaps(hmap):
    mapItems = []
    siteCount = sitapi.mapGetSiteCount(hmap)
    WriteLog(u'Получение списка карт',
                    u'hmap={0}; mapGetSiteCount={1}'.format(hmap, siteCount))
    # В документе базовая векторная карта имеет номер 0, а добавленные
    # пользовательские карты имеют номера от 1 до siteCount включительно.
    # Поэтому для двух карт в одном документе при siteCount == 1 нужны
    # оба индекса: 0 и 1.
    for siteNumber in range(0, siteCount + 1):
        hsite = sitapi.mapGetSiteIdent(hmap, siteNumber)
        WriteLog(u'Карта по номеру {0}'.format(siteNumber),
                        u'hsite={0}'.format(hsite))
        if not hsite:
            continue
        name = mapsyst.WTEXT(BUFFER_SIZE)
        sheetResult = sitapi.mapGetSiteSheetNameUn(
            hmap, hsite, 1, name, name.size())
        mapName = name.string()
        if not mapName:
            siteResult = sitapi.mapGetSiteNameUn(
                hmap, hsite, name, name.size())
            mapName = name.string()
            WriteLog(u'Запрошено основное имя карты {0}'.format(siteNumber),
                            u'result={0}; name={1}'.format(siteResult, mapName))
        if not mapName:
            mapName = u'Карта {0}'.format(siteNumber)
        WriteLog(u'Добавлена карта {0}'.format(siteNumber),
                        u'sheetResult={0}; name={1}'.format(sheetResult, mapName))
        mapItems.append((mapName, hsite))
    WriteLog(u'Список карт сформирован',
                    u'Количество карт: {0}'.format(len(mapItems)))
    return mapItems


def GetSiteByName(mapItems, name):
    for mapItem in mapItems:
        if mapItem[0] == name:
            return mapItem[1]
    return 0


def GetClassifierFileName(hmap, hsite):
    """Возвращает полный путь к фактически открытому классификатору карты."""
    hrsc = rscapi.mapGetRscIdent(hmap, hsite)
    if not hrsc:
        return u''
    rscFileName = mapsyst.WTEXT(BUFFER_SIZE)
    if rscapi.mapGetRscFileNameUn(
            hrsc, rscFileName, rscFileName.size()) == 0:
        return u''
    return rscFileName.string()


def GetDefaultModelFile(hmap, hsite):
    rscFileName = GetClassifierFileName(hmap, hsite)
    if not rscFileName:
        return u''
    # Формат VCLX именуется по полному имени классификатора, включая
    # расширение: map5000m.rscz.vclx, 100otkr.rsc.vclx.
    modelFileName = rscFileName + u'.vclx'
    WriteLog(u'Классификатор: {0}; файл моделей по умолчанию: {1}'.format(
        rscFileName, modelFileName))
    return modelFileName


def ShortenPath(fileName, maximumLength=60):
    """Сокращает путь только для отображения, полный путь хранится отдельно."""
    if len(fileName) <= maximumLength:
        return fileName
    drive, tail = os.path.splitdrive(fileName)
    return drive + u'\\...\\' + os.path.basename(tail)


def GetModelName(element, number):
    for attributeName in (u'name', u'Name', u'title', u'Title'):
        value = element.attrib.get(attributeName)
        if value:
            return value
    for child in list(element):
        tag = child.tag.split(u'}')[-1].lower()
        if tag in (u'name', u'title') and child.text:
            return child.text.strip()
    return u'Модель {0}'.format(number)


def LoadXmlModels(fileName):
    """Возвращает пары (имя модели, XML-запись для mapPutSelectRecordXML)."""
    if not fileName or not os.path.isfile(fileName):
        return []
    try:
        root = elementTree.parse(fileName).getroot()
    except Exception:
        return []

    elements = []
    rootTag = root.tag.split(u'}')[-1].lower()
    if rootTag in (u'model',) or u'select' in rootTag:
        elements.append((root, root))
    for element in root.iter():
        if element is root:
            continue
        tag = element.tag.split(u'}')[-1].lower()
        if tag == u'model' or u'select' in tag:
            elements.append((element, element))
        elif u'model' in tag:
            for child in element.iter():
                childTag = child.tag.split(u'}')[-1].lower()
                if child is not element and u'select' in childTag:
                    # В VCLX имя модели может храниться в контейнере Model,
                    # а XML-запись для HSELECT — во вложенном Select.
                    elements.append((element, child))
                    break

    models = []
    names = set()
    xmlRecords = set()
    for number, pair in enumerate(elements, 1):
        nameElement, xmlElement = pair
        xmlRecord = elementTree.tostring(xmlElement, encoding='utf-8')
        if xmlRecord in xmlRecords:
            continue
        xmlRecords.add(xmlRecord)
        name = GetModelName(nameElement, number)
        if name in names:
            name = u'{0} ({1})'.format(name, number)
        names.add(name)
        models.append((name, xmlRecord))
    return models


def GetSelectXml(hselect):
    record = 0
    try:
        record = seekapi.mapGetSelectRecordHandle(
            hselect, mapsyst.WTEXT(u''), 0, 0, 0)
        if not record:
            return None
        size = ctypes.c_long(0)
        buffer = seekapi.mapGetSelectRecordXMLPoint(
            hselect, record, ctypes.byref(size))
        if not buffer or size.value <= 0:
            return None
        return ctypes.string_at(buffer, size.value)
    finally:
        if record:
            seekapi.mapFreeSelectRecordXML(hselect, record)


def LoadModels(hmap, hsite, fileName):
    """Читает имена и XML моделей штатным API Panorama."""
    if not hsite or not fileName or not os.path.isfile(fileName):
        WriteLog(u'Файл моделей не найден: {0}'.format(fileName))
        return []
    if fileName.lower().endswith(u'.vclx'):
        models = LoadXmlModels(fileName)
        WriteLog(u'Загружено моделей VCLX: {0}; файл: {1}'.format(
            len(models), fileName))
        return models
    modelFile = seekapi.mapOpenModelFileUn(
        mapsyst.WTEXT(fileName), maptype.GENERIC_READ)
    if not modelFile:
        return LoadXmlModels(fileName)
    models = []
    try:
        modelCount = seekapi.mapModelCount(modelFile)
        for number in range(1, modelCount + 1):
            name = mapsyst.WTEXT(BUFFER_SIZE)
            if seekapi.mapModelNameUn(
                    modelFile, number, name, name.size()) == 0:
                continue
            hselect = sitapi.mapCreateSiteSelectContext(hmap, hsite)
            if not hselect:
                continue
            try:
                if seekapi.mapGetModelByNumber(modelFile, number, hselect) == 0:
                    continue
                xmlRecord = GetSelectXml(hselect)
                if xmlRecord:
                    models.append((name.string(), xmlRecord))
            finally:
                seekapi.mapDeleteSelectContext(hselect)
        if not models:
            models = LoadXmlModels(fileName)
        WriteLog(u'Загружено моделей: {0}; файл: {1}'.format(
            len(models), fileName))
        return models
    finally:
        seekapi.mapModelFree(modelFile)


def GetModelXml(models, modelName):
    for model in models:
        if model[0] == modelName:
            return model[1]
    return None


def CreateSelectContext(hmap, hsite, modelXml):
    hselect = sitapi.mapCreateSiteSelectContext(hmap, hsite)
    if not hselect:
        raise RuntimeError(u'Не удалось создать контекст условий поиска.')
    try:
        xmlBuffer = ctypes.create_string_buffer(modelXml, len(modelXml))
        if seekapi.mapPutSelectRecordXML(hselect, xmlBuffer, len(modelXml)) == 0:
            raise RuntimeError(u'Не удалось загрузить модель условий поиска.')
        return hselect
    except Exception:
        seekapi.mapDeleteSelectContext(hselect)
        raise


def CollectObjectKeys(hmap, hsite, hselect):
    keys = []
    hobj = sitapi.mapCreateSiteObject(hmap, hsite, maptype.IDDOUBLE2, 0)
    if not hobj:
        raise RuntimeError(u'Не удалось создать объект для поиска.')
    try:
        hfound = sitapi.mapSeekSiteSelectObjectEx(
            hmap, hsite, hobj, hselect, maptype.WO_FIRST, 0)
        while hfound:
            keys.append(mapapi.mapObjectKey(hobj))
            hfound = sitapi.mapSeekSiteSelectObjectEx(
                hmap, hsite, hobj, hselect, maptype.WO_NEXT, 0)
    finally:
        mapapi.mapFreeObject(hobj)
    return keys


def IsDegenerateSubject(hobj):
    """Проверяет, что объект имеет метрику, пригодную для анализа вхождения."""
    return mapapi.mapPolyCount(hobj) <= 0


def IsObjectInsideAnyContainer(hmap, hsite, objectKey, containerSite,
                               containerKeys):
    hobject = sitapi.mapCreateSiteObject(hmap, hsite, maptype.IDDOUBLE2, 0)
    hcontainer = sitapi.mapCreateSiteObject(
        hmap, containerSite, maptype.IDDOUBLE2, 0)
    if not hobject or not hcontainer:
        if hobject:
            mapapi.mapFreeObject(hobject)
        if hcontainer:
            mapapi.mapFreeObject(hcontainer)
        return False
    try:
        if not sitapi.mapSeekSiteObject(hmap, hsite, hobject, objectKey):
            return False
        if IsDegenerateSubject(hobject):
            return False
        for containerKey in containerKeys:
            if not sitapi.mapSeekSiteObject(
                    hmap, containerSite, hcontainer, containerKey):
                continue
            if IsDegenerateSubject(hcontainer):
                continue
            # mapCheckInsideObjectAndSubject возвращает 1, если проверяемый
            # объект полностью находится внутри хотя бы одного внешнего
            # контура мультиполигона-контейнера. Пересечения исключаются.
            if seekapi.mapCheckInsideObjectAndSubject(hobject, hcontainer) == 1:
                return True
        return False
    finally:
        mapapi.mapFreeObject(hobject)
        mapapi.mapFreeObject(hcontainer)


def CopyAndDeleteObject(hmap, sourceSite, archiveMap, archiveSite, objectKey):
    sourceObject = sitapi.mapCreateSiteObject(
        hmap, sourceSite, maptype.IDDOUBLE2, 0)
    archiveObject = 0
    if not sourceObject:
        if sourceObject:
            mapapi.mapFreeObject(sourceObject)
        return False
    try:
        if not sitapi.mapSeekSiteObject(hmap, sourceSite, sourceObject, objectKey):
            return False
        archiveObject = mapapi.mapCreateCopyObjectAsNew(archiveMap, sourceObject)
        if not archiveObject:
            WriteLog(u'Не удалось создать копию объекта {0}.'.format(objectKey))
            return False
        if sitapi.mapChangeObjectMap(archiveObject, archiveMap, archiveSite) == 0:
            WriteLog(u'Не удалось назначить карту-приемник объекту {0}.'.format(objectKey))
            return False
        if mapapi.mapCommitObject(archiveObject) == 0:
            WriteLog(u'Не удалось записать копию объекта {0}.'.format(objectKey))
            return False
        if mapapi.mapDeleteObject(sourceObject) == 0:
            WriteLog(u'Не удалось удалить исходный объект {0}.'.format(objectKey))
            return False
        WriteLog(u'Перенесен и удален объект {0}.'.format(objectKey))
        return True
    finally:
        mapapi.mapFreeObject(sourceObject)
        if archiveObject:
            mapapi.mapFreeObject(archiveObject)


def GetArchiveFileName(hmap, sourceSite, sourceName):
    siteName = mapsyst.WTEXT(BUFFER_SIZE)
    if sitapi.mapGetSiteFileNameUn(
            hmap, sourceSite, siteName, siteName.size()) == 0:
        return u''
    directory = os.path.dirname(siteName.string())
    invalidChars = u'<>:"/\\|?*'
    safeName = u''.join(
        u'_' if character in invalidChars else character for character in sourceName)
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    return os.path.join(
        directory, u'{0}_deleted_{1}.sitx'.format(safeName, timestamp))


def CreateArchiveMap(hmap, sourceSite, sourceName, archiveFileName):
    rscFileName = GetClassifierFileName(hmap, sourceSite)
    if not rscFileName:
        return 0, 0, u''
    if not archiveFileName:
        archiveFileName = GetArchiveFileName(hmap, sourceSite, sourceName)
    if not archiveFileName:
        return 0, 0, u''
    error = ctypes.c_long(0)
    archiveMap = mapapi.mapCreateSiteForMapEx(
        mapsyst.WTEXT(archiveFileName),
        mapsyst.WTEXT(os.path.splitext(os.path.basename(archiveFileName))[0]),
        mapsyst.WTEXT(rscFileName), 0, hmap, sourceSite, ctypes.byref(error))
    if not archiveMap:
        WriteLog(u'Не создана карта архива {0}; error={1}'.format(
            archiveFileName, error.value))
        return 0, 0, archiveFileName
    archiveSite = sitapi.mapGetSiteIdent(archiveMap, 0)
    WriteLog(u'Создана карта удаленных объектов: {0}; hmap={1}; hsite={2}'.format(
        archiveFileName, archiveMap, archiveSite))
    return archiveMap, archiveSite, archiveFileName


def ProcessDeleteInnerObjects(hmap, hobj, settings):
    containerSelect = 0
    objectSelect = 0
    progress = 0
    try:
        containerSelect = CreateSelectContext(
            hmap, settings['containerSite'], settings['containerXml'])
        objectSelect = CreateSelectContext(
            hmap, settings['objectSite'], settings['objectXml'])

        containerKeys = CollectObjectKeys(
            hmap, settings['containerSite'], containerSelect)
        objectKeys = CollectObjectKeys(hmap, settings['objectSite'], objectSelect)
        if not containerKeys or not objectKeys:
            return 0, False

        progress = mapapi.mapOpenProgressBar()
        archiveMap = 0
        archiveSite = 0
        movedCount = 0
        cancelled = False
        totalCount = len(objectKeys)
        for index, objectKey in enumerate(objectKeys, 1):
            percent = int(index * 100 / totalCount)
            if mapapi.mapProgressBar(
                    progress, percent, mapsyst.WTEXT(u'Поиск объектов внутри контуров')) == -1:
                cancelled = True
                break
            if not IsObjectInsideAnyContainer(
                    hmap, settings['objectSite'], objectKey,
                    settings['containerSite'], containerKeys):
                continue
            if not archiveMap:
                archiveMap, archiveSite, archiveFileName = CreateArchiveMap(
                    hmap, settings['objectSite'], settings['objectMapName'],
                    settings['archiveFileName'])
                if not archiveMap or not archiveSite:
                    raise RuntimeError(
                        u'Не удалось создать карту удаляемых объектов: {0}'.format(
                            archiveFileName))
            if CopyAndDeleteObject(
                    hmap, settings['objectSite'], archiveMap, archiveSite, objectKey):
                movedCount += 1
        return movedCount, cancelled
    finally:
        if progress:
            mapapi.mapCloseProgressBar(progress)
        if objectSelect:
            seekapi.mapDeleteSelectContext(objectSelect)
        if containerSelect:
            seekapi.mapDeleteSelectContext(containerSelect)


def GetDialogSettings(hmap):
    mapItems = GetOpenMaps(hmap)
    WriteLog(u'GetDialogSettings: найдено карт: {0}'.format(len(mapItems)))
    if len(mapItems) < 2:
        ShowMessage(u'Для выполнения нужны как минимум две открытые векторные карты.', True)
        return None

    iniName = GetIniFileName(hmap)
    defaultContainerMap = mapItems[0][0]
    defaultObjectMap = mapItems[1][0]
    root = tkinter.Tk()
    root.title(TITLE)
    root.wm_attributes('-topmost', 1)

    containerMapName = tkinter.StringVar()
    objectMapName = tkinter.StringVar()
    containerFileName = tkinter.StringVar()
    objectFileName = tkinter.StringVar()
    containerFileText = tkinter.StringVar()
    objectFileText = tkinter.StringVar()
    archiveFileName = tkinter.StringVar()
    archiveFileText = tkinter.StringVar()
    containerModelName = tkinter.StringVar()
    objectModelName = tkinter.StringVar()
    result = {'value': None}
    dialogClosed = {'value': False}
    isRestoring = {'value': True}
    containerModels = []
    objectModels = []

    mapNames = [mapItem[0] for mapItem in mapItems]

    def SetFileName(fileVariable, textVariable, fileName):
        fileVariable.set(fileName)
        textVariable.set(ShortenPath(fileName))

    def SyncFileName(fileVariable, textVariable):
        shownFileName = textVariable.get()
        if shownFileName != ShortenPath(fileVariable.get()):
            fileVariable.set(shownFileName)
        textVariable.set(ShortenPath(fileVariable.get()))

    def SetDefaultFile(mapName, fileVariable, textVariable, savedKey):
        hsite = GetSiteByName(mapItems, mapName)
        defaultFile = GetDefaultModelFile(hmap, hsite) if hsite else u''
        if isRestoring['value']:
            defaultFile = ReadSetting(iniName, savedKey, defaultFile)
        SetFileName(fileVariable, textVariable, defaultFile)

    def RefreshModels(hsite, fileVariable, modelVariable, combo, modelList,
                      savedKey, refreshButton):
        models = LoadModels(hmap, hsite, fileVariable.get())
        modelList[:] = models
        names = [model[0] for model in models]
        combo.configure(values=names)
        refreshButton.configure(state='normal' if names else 'disabled')
        savedName = ReadSetting(iniName, savedKey, u'')
        if modelVariable.get() not in names:
            modelVariable.set(savedName if savedName in names else (names[0] if names else u''))

    def ContainerMapChanged(*unused):
        SetDefaultFile(
            containerMapName.get(), containerFileName, containerFileText,
            u'ContainerModelFile')
        RefreshModels(
            GetSiteByName(mapItems, containerMapName.get()), containerFileName,
            containerModelName, containerModelCombo,
            containerModels, u'ContainerModel', containerRefreshButton)

    def ObjectMapChanged(*unused):
        SetDefaultFile(
            objectMapName.get(), objectFileName, objectFileText,
            u'ObjectModelFile')
        if not isRestoring['value']:
            SetFileName(
                archiveFileName, archiveFileText, GetArchiveFileName(
                    hmap, GetSiteByName(mapItems, objectMapName.get()),
                    objectMapName.get()))
        RefreshModels(
            GetSiteByName(mapItems, objectMapName.get()), objectFileName,
            objectModelName, objectModelCombo,
            objectModels, u'ObjectModel', objectRefreshButton)

    def BrowseFile(hsite, fileVariable, textVariable, modelVariable, combo,
                   modelList, savedKey, refreshButton):
        fileName = askopenfilename(
            title=u'Выбор файла моделей',
            filetypes=[(u'Файлы моделей', u'*.vclx'), (u'Все файлы', u'*.*')])
        if fileName:
            SetFileName(fileVariable, textVariable, fileName)
            RefreshModels(
                hsite, fileVariable, modelVariable, combo, modelList, savedKey,
                refreshButton)

    def BrowseArchiveFile():
        fileName = asksaveasfilename(
            title=u'Карта удаленных объектов',
            defaultextension=u'.sitx',
            filetypes=[(u'Карта SITX', u'*.sitx'), (u'Все файлы', u'*.*')],
            initialfile=os.path.basename(archiveFileName.get()))
        if fileName:
            SetFileName(archiveFileName, archiveFileText, fileName)

    def OpenHelp():
        try:
            webbrowser.open(HELP_URL)
        except Exception as error:
            WriteLog(u'Не удалось открыть справку: {0}'.format(error))

    def SaveDialogSize():
        root.update_idletasks()
        WriteSettings(iniName, {
            u'DialogWidth': str(root.winfo_width()),
            u'DialogHeight': str(root.winfo_height())
        })

    def Run():
        SyncFileName(containerFileName, containerFileText)
        SyncFileName(objectFileName, objectFileText)
        SyncFileName(archiveFileName, archiveFileText)
        containerSite = GetSiteByName(mapItems, containerMapName.get())
        objectSite = GetSiteByName(mapItems, objectMapName.get())
        containerXml = GetModelXml(containerModels, containerModelName.get())
        objectXml = GetModelXml(objectModels, objectModelName.get())
        if not containerSite or not objectSite:
            ShowMessage(u'Выберите обе карты.', True, root)
            return
        if not containerXml or not objectXml:
            ShowMessage(u'Не найдены модели. Укажите существующий файл VCLX.', True, root)
            return
        if sitapi.mapGetSiteEditFlag(hmap, objectSite) == 0:
            ShowMessage(u'Редактируемая карта недоступна для редактирования.', True, root)
            return
        result['value'] = {
            'containerSite': containerSite,
            'objectSite': objectSite,
            'objectMapName': objectMapName.get(),
            'archiveFileName': archiveFileName.get(),
            'containerXml': containerXml,
            'objectXml': objectXml,
            'iniName': iniName,
            'iniValues': {
                u'ContainerMap': containerMapName.get(),
                u'ContainerModelFile': containerFileName.get(),
                u'ContainerModel': containerModelName.get(),
                u'ObjectMap': objectMapName.get(),
                u'ObjectModelFile': objectFileName.get(),
                u'ObjectModel': objectModelName.get(),
                u'ArchiveFileName': archiveFileName.get()
            }
        }
        SaveDialogSize()
        dialogClosed['value'] = True
        root.destroy()

    def Cancel():
        if dialogClosed['value']:
            return
        dialogClosed['value'] = True
        try:
            SaveDialogSize()
        finally:
            root.destroy()

    labels = (
        u'Анализируемая карта:',
        u'Файл моделей анализируемой карты:',
        u'Модель анализируемой карты:',
        u'Редактируемая карта:',
        u'Файл моделей редактируемой карты:',
        u'Модель редактируемой карты:',
        u'Карта удаленных объектов:'
    )
    for row, label in enumerate(labels):
        tkinter.Label(root, text=label).grid(
            row=row, column=0, sticky='w', padx=6, pady=3)

    containerMapCombo = tkinter.ttk.Combobox(
        root, textvariable=containerMapName, values=mapNames, width=58,
        state='readonly')
    containerMapCombo.grid(row=0, column=1, columnspan=2, padx=6, pady=3, sticky='ew')
    containerFileEntry = tkinter.Entry(root, textvariable=containerFileText, width=50)
    containerFileEntry.grid(row=1, column=1, padx=6, pady=3, sticky='ew')
    containerModelCombo = tkinter.ttk.Combobox(
        root, textvariable=containerModelName, width=58, state='readonly')
    containerModelCombo.grid(row=2, column=1, columnspan=2, padx=6, pady=3, sticky='ew')

    objectMapCombo = tkinter.ttk.Combobox(
        root, textvariable=objectMapName, values=mapNames, width=58,
        state='readonly')
    objectMapCombo.grid(row=3, column=1, columnspan=2, padx=6, pady=3, sticky='ew')
    objectFileEntry = tkinter.Entry(root, textvariable=objectFileText, width=50)
    objectFileEntry.grid(row=4, column=1, padx=6, pady=3, sticky='ew')
    objectModelCombo = tkinter.ttk.Combobox(
        root, textvariable=objectModelName, width=58, state='readonly')
    objectModelCombo.grid(row=5, column=1, columnspan=2, padx=6, pady=3, sticky='ew')

    tkinter.Button(
        root, text=u'Обзор...', command=lambda: BrowseFile(
            GetSiteByName(mapItems, containerMapName.get()), containerFileName,
            containerFileText,
            containerModelName, containerModelCombo,
            containerModels, u'ContainerModel', containerRefreshButton)).grid(
                row=1, column=2, padx=6, pady=3)
    tkinter.Button(
        root, text=u'Обзор...', command=lambda: BrowseFile(
            GetSiteByName(mapItems, objectMapName.get()), objectFileName,
            objectFileText,
            objectModelName, objectModelCombo,
            objectModels, u'ObjectModel', objectRefreshButton)).grid(
                row=4, column=2, padx=6, pady=3)
    containerRefreshButton = tkinter.Button(
        root, text=u'Обновить модели', command=lambda: RefreshModels(
        GetSiteByName(mapItems, containerMapName.get()), containerFileName,
        containerModelName, containerModelCombo,
        containerModels, u'ContainerModel', containerRefreshButton))
    containerRefreshButton.grid(row=2, column=3, padx=6, pady=3)
    objectRefreshButton = tkinter.Button(
        root, text=u'Обновить модели', command=lambda: RefreshModels(
        GetSiteByName(mapItems, objectMapName.get()), objectFileName,
        objectModelName, objectModelCombo,
        objectModels, u'ObjectModel', objectRefreshButton))
    objectRefreshButton.grid(row=5, column=3, padx=6, pady=3)
    archiveFileEntry = tkinter.Entry(root, textvariable=archiveFileText, width=50)
    archiveFileEntry.grid(row=6, column=1, padx=6, pady=3, sticky='ew')
    tkinter.Button(root, text=u'Обзор...', command=BrowseArchiveFile).grid(
        row=6, column=2, padx=6, pady=3)
    buttonFrame = tkinter.Frame(root)
    buttonFrame.grid(row=7, column=0, columnspan=4, padx=6, pady=8, sticky='w')
    tkinter.Button(buttonFrame, text=u'Выполнить', command=Run, width=10).pack(
        side='left')
    tkinter.Button(buttonFrame, text=u'Выход', command=Cancel, width=10).pack(
        side='left', padx=8)
    tkinter.Button(buttonFrame, text=u'Помощь', command=OpenHelp, width=10).pack(
        side='left')
    root.columnconfigure(1, weight=1)

    containerMapName.set(ReadSetting(iniName, u'ContainerMap', defaultContainerMap))
    if containerMapName.get() not in mapNames:
        containerMapName.set(defaultContainerMap)
    objectMapName.set(ReadSetting(iniName, u'ObjectMap', defaultObjectMap))
    if objectMapName.get() not in mapNames:
        objectMapName.set(defaultObjectMap)
    containerMapName.trace('w', ContainerMapChanged)
    objectMapName.trace('w', ObjectMapChanged)
    ContainerMapChanged()
    ObjectMapChanged()
    SetFileName(
        archiveFileName, archiveFileText, ReadSetting(
            iniName, u'ArchiveFileName', GetArchiveFileName(
                hmap, GetSiteByName(mapItems, objectMapName.get()),
                objectMapName.get())))
    isRestoring['value'] = False
    containerFileEntry.bind(
        '<FocusOut>', lambda unused: (
            SyncFileName(containerFileName, containerFileText),
            RefreshModels(
                GetSiteByName(mapItems, containerMapName.get()), containerFileName,
                containerModelName, containerModelCombo, containerModels,
                u'ContainerModel', containerRefreshButton)))
    objectFileEntry.bind(
        '<FocusOut>', lambda unused: (
            SyncFileName(objectFileName, objectFileText),
            RefreshModels(
                GetSiteByName(mapItems, objectMapName.get()), objectFileName,
                objectModelName, objectModelCombo, objectModels,
                u'ObjectModel', objectRefreshButton)))
    archiveFileEntry.bind(
        '<FocusOut>', lambda unused: SyncFileName(
            archiveFileName, archiveFileText))
    root.update_idletasks()
    minimumWidth = root.winfo_reqwidth()
    minimumHeight = root.winfo_reqheight()
    try:
        dialogWidth = max(minimumWidth, int(ReadSetting(
            iniName, u'DialogWidth', str(minimumWidth))))
        dialogHeight = max(minimumHeight, int(ReadSetting(
            iniName, u'DialogHeight', str(minimumHeight))))
    except ValueError:
        dialogWidth = minimumWidth
        dialogHeight = minimumHeight
    root.minsize(minimumWidth, minimumHeight)
    root.geometry(u'{0}x{1}'.format(dialogWidth, dialogHeight))
    root.protocol('WM_DELETE_WINDOW', Cancel)
    root.eval('tk::PlaceWindow . center')
    root.resizable(True, False)
    root.mainloop()
    return result['value']


def RunDeleteInnerObjects(hmap, hobj):
    WriteLog(
        u'Запуск DeleteInnerObjects: hmap={0}; hobj={1}'.format(hmap, hobj))
    settings = GetDialogSettings(hmap)
    if not settings:
        return 0
    try:
        WriteSettings(settings['iniName'], settings['iniValues'])
        movedCount, cancelled = ProcessDeleteInnerObjects(hmap, hobj, settings)
        mapapi.mapInvalidate()
        if cancelled:
            ShowMessage(u'Операция отменена. Перенесено объектов: {0}.'.format(movedCount))
            return 0
        ShowMessage(u'Перенесено на специальную карту и удалено объектов: {0}.'.format(movedCount))
        return 1
    except RuntimeError as error:
        ShowMessage(str(error), True)
    except Exception as error:
        ShowMessage(u'Ошибка выполнения: {0}'.format(error), True)
    return 0


def DeleteInnerObjectsScript(hmap, hobj):
    return RunDeleteInnerObjects(hmap, hobj)


def DeleteInnerObjects(hmap, hobj):  #caption:Удалить объекты внутри объектов другой карты
    """Точка входа скрипта Панорамы. Возвращает 1 при успехе, 0 при ошибке."""
    return RunDeleteInnerObjects(hmap, hobj)
