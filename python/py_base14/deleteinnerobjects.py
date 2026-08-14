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
import mapselec
import mapsyst
import maptype
import rscapi
import seekapi
import sitapi


SECTION = u'DELETEINNEROBJECTS'
BUFFER_SIZE = 4096
LOG_PREFIX = u'TPythonScript::DeleteInnerObjects(): '
SERVICE_MODEL_NAMES = (u'SearchState', u'DialogsState')
HELP_URL_RU = u'https://help.gisserver.ru/v15/russian/mapscena/index.html?idn4.html'
HELP_URL_EN = u'https://help.gisserver.ru/v15/english/mapscena/index.html?idn4.html'


def DetectLang():
    """Определяет язык интерфейса ГИС Панорама."""
    try:
        code = mapapi.mapGetMapAccessLanguage()
        if code == getattr(maptype, 'ML_RUSSIAN', 2):
            return 'ru'
        return 'en'
    except Exception:
        return 'ru'


# Модуль в Панораме остаётся загруженным между запусками, поэтому язык
# нужно обновлять при каждом вызове скрипта, а не только при импорте.
_LANG = DetectLang()


def RefreshLang():
    """Обновляет язык интерфейса по текущим настройкам Панорамы."""
    global _LANG
    _LANG = DetectLang()
    return _LANG

_STR = {
    'ru': {
        'title': u'Удаление объектов внутри объектов другой карты',
        'label_analyze_map': u'Анализируемая карта:',
        'label_edit_map': u'Редактируемая карта:',
        'label_model_file': u'Файл моделей:',
        'label_model': u'Модель:',
        'check_save_archive': u'Удалённые объекты сохранять в карту',
        'label_archive_map': u'Карта удаленных объектов:',
        'btn_browse': u'Выбрать',
        'btn_add': u'Добавить',
        'btn_run': u'Выполнить',
        'btn_exit': u'Выход',
        'btn_help': u'Помощь',
        'dlg_select_models': u'Выбор файла моделей',
        'dlg_select_archive': u'Карта удаленных объектов',
        'dlg_filter_title': u'Условия поиска объектов',
        'dlg_model_name': u'Имя новой модели',
        'dlg_model_name_prompt': u'Введите имя модели:',
        'filetype_models': u'Файлы моделей',
        'filetype_sitx': u'Карта SITX',
        'filetype_all': u'Все файлы',
        'map_fallback': u'Карта {number}',
        'model_fallback': u'Модель {number}',
        'need_two_maps': u'Для выполнения нужны как минимум две открытые векторные карты.',
        'select_both_maps': u'Выберите обе карты.',
        'models_not_found': u'Не найдены модели. Укажите существующий файл VCLX.',
        'different_rsc': u'Анализируемая и редактируемая карты должны быть созданы по одному классификатору.',
        'map_not_editable': u'Редактируемая карта недоступна для редактирования.',
        'err_add_model': u'Не удалось добавить модель в файл VCLX.',
        'err_filter_dialog': u'Не удалось открыть диалог условий поиска.',
        'cancelled': u'Операция отменена. Обработано объектов: {count}.',
        'done': u'Перенесено на специальную карту и удалено объектов: {count}.',
        'done_delete': u'Удалено объектов: {count}.',
        'exec_error': u'Ошибка выполнения: {error}',
        'progress': u'Поиск объектов внутри контуров',
        'err_select_context': u'Не удалось создать контекст условий поиска.',
        'err_load_model': u'Не удалось загрузить модель условий поиска.',
        'err_seek_object': u'Не удалось создать объект для поиска.',
        'err_archive_map': u'Не удалось создать карту удаляемых объектов: {name}',
        'log_user_message': u'Сообщение пользователю: {text}',
        'log_get_maps': u'Получение списка карт',
        'log_map_by_number': u'Карта по номеру {number}',
        'log_map_main_name': u'Запрошено основное имя карты {number}',
        'log_map_added': u'Добавлена карта {number}',
        'log_maps_ready': u'Список карт сформирован',
        'log_maps_count': u'Количество карт: {count}',
        'log_classifier': u'Классификатор: {rsc}; файл моделей по умолчанию: {model}',
        'log_models_missing': u'Файл моделей не найден: {name}',
        'log_models_vclx': u'Загружено моделей VCLX: {count}; файл: {name}',
        'log_models_loaded': u'Загружено моделей: {count}; файл: {name}',
        'log_model_api': u'Модель "{model}" загружена в HSELECT через API; файл: {name}; hsite={hsite}',
        'log_model_xml': u'Модель "{model}" загружена в HSELECT из XML; файл: {name}; hsite={hsite}',
        'log_keys': u'Отобрано объектов: анализируемая={container}; редактируемая={edited}',
        'log_common_keys': u'Объектов редактируемой карты с совпадающим ключом классификатора: {count}',
        'log_copy_fail': u'Не удалось создать копию объекта {key}.',
        'log_change_map_fail': u'Не удалось назначить карту-приемник объекту {key}.',
        'log_commit_fail': u'Не удалось записать копию объекта {key}.',
        'log_delete_fail': u'Не удалось удалить исходный объект {key}.',
        'log_moved': u'Перенесен и удален объект {key}.',
        'log_deleted': u'Удален объект {key}.',
        'log_archive_fail': u'Не создана карта архива {name}; error={error}',
        'log_archive_ok': u'Создана карта удаленных объектов: {name}; hmap={hmap}; hsite={hsite}',
        'log_archive_open': u'Открыта существующая карта удаленных объектов для дозаписи: {name}; hsite={hsite}',
        'log_archive_open_fail': u'Не удалось открыть карту удаленных объектов: {name}',
        'log_dialog_maps': u'GetDialogSettings: найдено карт: {count}',
        'log_help_fail': u'Не удалось открыть справку: {error}',
        'log_start': u'Запуск DeleteInnerObjects: hmap={hmap}; hobj={hobj}',
    },
    'en': {
        'title': u'Delete objects inside objects of another map',
        'label_analyze_map': u'Analyzed map:',
        'label_edit_map': u'Editable map:',
        'label_model_file': u'Model file:',
        'label_model': u'Model:',
        'check_save_archive': u'Save deleted objects to a map',
        'label_archive_map': u'Map of deleted objects:',
        'btn_browse': u'Select',
        'btn_add': u'Add',
        'btn_run': u'Execute',
        'btn_exit': u'Exit',
        'btn_help': u'Help',
        'dlg_select_models': u'Select model file',
        'dlg_select_archive': u'Map of deleted objects',
        'dlg_filter_title': u'Object search conditions',
        'dlg_model_name': u'New model name',
        'dlg_model_name_prompt': u'Enter model name:',
        'filetype_models': u'Model files',
        'filetype_sitx': u'SITX map',
        'filetype_all': u'All files',
        'map_fallback': u'Map {number}',
        'model_fallback': u'Model {number}',
        'need_two_maps': u'At least two open vector maps are required to run.',
        'select_both_maps': u'Select both maps.',
        'models_not_found': u'Models not found. Specify an existing VCLX file.',
        'different_rsc': u'The analyzed and editable maps must be created using the same classifier.',
        'map_not_editable': u'The editable map is not available for editing.',
        'err_add_model': u'Failed to add the model to the VCLX file.',
        'err_filter_dialog': u'Failed to open the object search conditions dialog.',
        'cancelled': u'Operation cancelled. Objects processed: {count}.',
        'done': u'Objects moved to a special map and deleted: {count}.',
        'done_delete': u'Objects deleted: {count}.',
        'exec_error': u'Execution error: {error}',
        'progress': u'Searching for objects inside contours',
        'err_select_context': u'Failed to create a search conditions context.',
        'err_load_model': u'Failed to load the search conditions model.',
        'err_seek_object': u'Failed to create an object for search.',
        'err_archive_map': u'Failed to create the map of deleted objects: {name}',
        'log_user_message': u'User message: {text}',
        'log_get_maps': u'Getting map list',
        'log_map_by_number': u'Map by number {number}',
        'log_map_main_name': u'Requested main map name {number}',
        'log_map_added': u'Added map {number}',
        'log_maps_ready': u'Map list prepared',
        'log_maps_count': u'Map count: {count}',
        'log_classifier': u'Classifier: {rsc}; default model file: {model}',
        'log_models_missing': u'Model file not found: {name}',
        'log_models_vclx': u'Loaded VCLX models: {count}; file: {name}',
        'log_models_loaded': u'Loaded models: {count}; file: {name}',
        'log_model_api': u'Model "{model}" loaded into HSELECT via API; file: {name}; hsite={hsite}',
        'log_model_xml': u'Model "{model}" loaded into HSELECT from XML; file: {name}; hsite={hsite}',
        'log_keys': u'Selected objects: analyzed={container}; editable={edited}',
        'log_common_keys': u'Editable-map objects with a matching classifier key: {count}',
        'log_copy_fail': u'Failed to create a copy of object {key}.',
        'log_change_map_fail': u'Failed to assign destination map for object {key}.',
        'log_commit_fail': u'Failed to write a copy of object {key}.',
        'log_delete_fail': u'Failed to delete source object {key}.',
        'log_moved': u'Moved and deleted object {key}.',
        'log_deleted': u'Deleted object {key}.',
        'log_archive_fail': u'Archive map was not created {name}; error={error}',
        'log_archive_ok': u'Created map of deleted objects: {name}; hmap={hmap}; hsite={hsite}',
        'log_archive_open': u'Opened existing deleted-objects map for append: {name}; hsite={hsite}',
        'log_archive_open_fail': u'Failed to open the deleted-objects map: {name}',
        'log_dialog_maps': u'GetDialogSettings: maps found: {count}',
        'log_help_fail': u'Failed to open help: {error}',
        'log_start': u'Start DeleteInnerObjects: hmap={hmap}; hobj={hobj}',
    },
}


def tr(stringId, **kwargs):
    """Возвращает локализованную строку по идентификатору."""
    # Имя первого аргумента не должно быть key: иначе вызовы вида
    # tr('log_moved', key=objectKey) дают "multiple values for argument 'key'".
    text = _STR.get(_LANG, _STR['en']).get(stringId, stringId)
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text


def GetHelpUrl():
    if _LANG == 'ru':
        return HELP_URL_RU
    return HELP_URL_EN


def IsServiceModel(name):
    return name in SERVICE_MODEL_NAMES


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
        tr('log_user_message', text=text), u'',
        maptype.MT_WARNING if warning else maptype.MT_INFO)
    style = maptype.MB_WARNING if warning else maptype.MB_OK
    window = 0
    try:
        if parent is not None and parent.winfo_exists():
            # Главное окно больше не перекрывает модальное сообщение.
            parent.wm_attributes('-topmost', 0)
            window = parent.winfo_id()
        mapapi.mapMessageBoxUn(
            window, mapsyst.WTEXT(text), mapsyst.WTEXT(tr('title')), style)
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
    WriteLog(tr('log_get_maps'),
             u'hmap={0}; mapGetSiteCount={1}'.format(hmap, siteCount))
    # В документе базовая векторная карта имеет номер 0, а добавленные
    # пользовательские карты имеют номера от 1 до siteCount включительно.
    # Поэтому для двух карт в одном документе при siteCount == 1 нужны
    # оба индекса: 0 и 1.
    for siteNumber in range(0, siteCount + 1):
        hsite = sitapi.mapGetSiteIdent(hmap, siteNumber)
        WriteLog(tr('log_map_by_number', number=siteNumber),
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
            WriteLog(tr('log_map_main_name', number=siteNumber),
                     u'result={0}; name={1}'.format(siteResult, mapName))
        if not mapName:
            mapName = tr('map_fallback', number=siteNumber)
        WriteLog(tr('log_map_added', number=siteNumber),
                 u'sheetResult={0}; name={1}'.format(sheetResult, mapName))
        mapItems.append((mapName, hsite))
    WriteLog(tr('log_maps_ready'), tr('log_maps_count', count=len(mapItems)))
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


def GetClassifierBaseName(hmap, hsite):
    """Возвращает имя классификатора без пути."""
    hrsc = rscapi.mapGetRscIdent(hmap, hsite)
    if not hrsc:
        return u''
    rscName = mapsyst.WTEXT(BUFFER_SIZE)
    if rscapi.mapGetRscNameUn(hrsc, rscName, rscName.size()):
        return rscName.string()
    return os.path.basename(GetClassifierFileName(hmap, hsite))


def IsSameClassifier(hmap, firstSite, secondSite):
    firstName = GetClassifierBaseName(hmap, firstSite).lower()
    secondName = GetClassifierBaseName(hmap, secondSite).lower()
    return bool(firstName) and firstName == secondName


def GetDefaultModelFile(hmap, hsite):
    rscFileName = GetClassifierFileName(hmap, hsite)
    if not rscFileName:
        return u''
    # Формат VCLX именуется по полному имени классификатора, включая
    # расширение: map5000m.rscz.vclx, 100otkr.rsc.vclx.
    modelFileName = rscFileName + u'.vclx'
    WriteLog(tr('log_classifier', rsc=rscFileName, model=modelFileName))
    return modelFileName


def ShortenPath(fileName, maximumLength=60):
    """Сокращает путь только для отображения, полный путь хранится отдельно."""
    if len(fileName) <= maximumLength:
        return fileName
    drive, tail = os.path.splitdrive(fileName)
    return drive + u'\\...\\' + os.path.basename(tail)


def NormalizeArchiveFileName(hmap, sourceSite, archiveFileName):
    """Приводит путь карты архива к полному имени файла .sitx."""
    if not archiveFileName:
        return u''
    archiveFileName = archiveFileName.strip().strip(u'"')
    if not archiveFileName or u'...' in archiveFileName:
        return u''
    if not os.path.isabs(archiveFileName):
        siteName = mapsyst.WTEXT(BUFFER_SIZE)
        if sourceSite and sitapi.mapGetSiteFileNameUn(
                hmap, sourceSite, siteName, siteName.size()):
            directory = os.path.dirname(siteName.string())
            if directory:
                archiveFileName = os.path.join(directory, archiveFileName)
    if not archiveFileName.lower().endswith(u'.sitx'):
        archiveFileName += u'.sitx'
    try:
        return os.path.normpath(archiveFileName)
    except Exception:
        return archiveFileName


def GetModelName(element, number):
    for attributeName in (u'name', u'Name', u'title', u'Title'):
        value = element.attrib.get(attributeName)
        if value:
            return value
    for child in list(element):
        tag = child.tag.split(u'}')[-1].lower()
        if tag in (u'name', u'title') and child.text:
            return child.text.strip()
    return tr('model_fallback', number=number)


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
        if IsServiceModel(name):
            continue
        if name in names:
            name = u'{0} ({1})'.format(name, number)
        names.add(name)
        models.append((name, xmlRecord))
    return models


def LoadModels(hmap, hsite, fileName):
    """Читает имена моделей штатным API Panorama (в т.ч. для VCLX)."""
    if not fileName or not os.path.isfile(fileName):
        WriteLog(tr('log_models_missing', name=fileName))
        return []
    models = []
    names = set()
    modelFile = seekapi.mapOpenModelFileUn(
        mapsyst.WTEXT(fileName), maptype.GENERIC_READ)
    if modelFile:
        try:
            modelCount = int(seekapi.mapModelCount(modelFile) or 0)
            # Нумерация в разных версиях API встречается с 0 и с 1.
            for number in range(0, modelCount + 1):
                name = mapsyst.WTEXT(BUFFER_SIZE)
                if seekapi.mapModelNameUn(
                        modelFile, number, name, name.size()) == 0:
                    continue
                modelName = name.string().strip()
                if not modelName or IsServiceModel(modelName) or modelName in names:
                    continue
                names.add(modelName)
                # XML здесь не обязателен: HSELECT формируется из файла по имени.
                models.append((modelName, None))
        finally:
            seekapi.mapModelFree(modelFile)
    if not models:
        models = LoadXmlModels(fileName)
        WriteLog(tr('log_models_vclx', count=len(models), name=fileName))
    else:
        WriteLog(tr('log_models_loaded', count=len(models), name=fileName))
    return models


def CreateSelectContextFromModelFile(hmap, hsite, fileName, modelName):
    """Создаёт HSELECT для карты и загружает в него модель из файла."""
    if not hsite or not fileName or not modelName or not os.path.isfile(fileName):
        raise RuntimeError(tr('err_load_model'))
    hselect = sitapi.mapCreateSiteSelectContext(hmap, hsite)
    if not hselect:
        raise RuntimeError(tr('err_select_context'))
    modelFile = 0
    try:
        modelFile = seekapi.mapOpenModelFileUn(
            mapsyst.WTEXT(fileName), maptype.GENERIC_READ)
        if modelFile and seekapi.mapGetModelByNameUn(
                modelFile, mapsyst.WTEXT(modelName), hselect):
            WriteLog(tr(
                'log_model_api', model=modelName, name=fileName, hsite=hsite))
            result = hselect
            hselect = 0
            return result
        for name, xmlRecord in LoadXmlModels(fileName):
            if name != modelName or not xmlRecord:
                continue
            xmlBuffer = ctypes.create_string_buffer(xmlRecord, len(xmlRecord))
            if seekapi.mapPutSelectRecordXML(
                    hselect, xmlBuffer, len(xmlRecord)) == 0:
                continue
            WriteLog(tr(
                'log_model_xml', model=modelName, name=fileName, hsite=hsite))
            result = hselect
            hselect = 0
            return result
        raise RuntimeError(tr('err_load_model'))
    finally:
        if modelFile:
            seekapi.mapModelFree(modelFile)
        if hselect:
            seekapi.mapDeleteSelectContext(hselect)


def GetObjectFrame(hobj):
    """Возвращает габариты объекта (X1, Y1, X2, Y2) в метрах документа."""
    dframe = maptype.DFRAME()
    if mapapi.mapObjectFrame(hobj, ctypes.byref(dframe)) == 0:
        return None
    return (dframe.X1, dframe.Y1, dframe.X2, dframe.Y2)


def FramesOverlap(first, second):
    return not (
        first[2] < second[0] or second[2] < first[0] or
        first[3] < second[1] or second[3] < first[1])


def CollectContainerIndex(hmap, hsite, hselect):
    """Индекс контейнеров: ключ классификатора -> [(номер, frame), ...]."""
    index = {}
    count = 0
    hobj = sitapi.mapCreateSiteObject(hmap, hsite, maptype.IDDOUBLE2, 0)
    if not hobj:
        raise RuntimeError(tr('err_seek_object'))
    try:
        hfound = sitapi.mapSeekSiteSelectObjectEx(
            hmap, hsite, hobj, hselect, maptype.WO_FIRST, 0)
        while hfound:
            objectKey = mapapi.mapObjectKey(hobj)
            excode = mapapi.mapObjectExcode(hobj)
            frame = GetObjectFrame(hobj)
            if objectKey and frame is not None:
                index.setdefault(excode, []).append((objectKey, frame))
                count += 1
            hfound = sitapi.mapSeekSiteSelectObjectEx(
                hmap, hsite, hobj, hselect, maptype.WO_NEXT, 0)
    finally:
        mapapi.mapFreeObject(hobj)
    return index, count


def CollectEditableObjects(hmap, hsite, hselect):
    """Список удаляемых объектов: (номер, ключ классификатора, frame)."""
    objects = []
    hobj = sitapi.mapCreateSiteObject(hmap, hsite, maptype.IDDOUBLE2, 0)
    if not hobj:
        raise RuntimeError(tr('err_seek_object'))
    try:
        hfound = sitapi.mapSeekSiteSelectObjectEx(
            hmap, hsite, hobj, hselect, maptype.WO_FIRST, 0)
        while hfound:
            objectKey = mapapi.mapObjectKey(hobj)
            excode = mapapi.mapObjectExcode(hobj)
            frame = GetObjectFrame(hobj)
            if objectKey and frame is not None:
                objects.append((objectKey, excode, frame))
            hfound = sitapi.mapSeekSiteSelectObjectEx(
                hmap, hsite, hobj, hselect, maptype.WO_NEXT, 0)
    finally:
        mapapi.mapFreeObject(hobj)
    return objects


def IsDegenerateSubject(hobj):
    """Проверяет, что объект имеет метрику, пригодную для анализа вхождения."""
    return mapapi.mapPolyCount(hobj) <= 0


def IsObjectInsideSameKeyContainers(
        hmap, objectSite, objectKey, objectFrame, containerSite, containerItems):
    """Проверяет вхождение объекта в контейнер с тем же ключом классификатора.

    containerItems — список (номер объекта контейнера, frame) уже отобранных
    по одинаковому mapObjectExcode.
    """
    hobject = sitapi.mapCreateSiteObject(hmap, objectSite, maptype.IDDOUBLE2, 0)
    hcontainer = sitapi.mapCreateSiteObject(
        hmap, containerSite, maptype.IDDOUBLE2, 0)
    if not hobject or not hcontainer:
        if hobject:
            mapapi.mapFreeObject(hobject)
        if hcontainer:
            mapapi.mapFreeObject(hcontainer)
        return False
    try:
        if not sitapi.mapSeekSiteObject(hmap, objectSite, hobject, objectKey):
            return False
        if IsDegenerateSubject(hobject):
            return False
        for containerKey, containerFrame in containerItems:
            if (objectFrame is not None and containerFrame is not None and
                    not FramesOverlap(objectFrame, containerFrame)):
                continue
            if not sitapi.mapSeekSiteObject(
                    hmap, containerSite, hcontainer, containerKey):
                continue
            if IsDegenerateSubject(hcontainer):
                continue
            # 1 — проверяемый объект полностью внутри хотя бы одного внешнего
            # контура мультиполигона-контейнера.
            if seekapi.mapCheckInsideObjectAndSubject(hobject, hcontainer) == 1:
                return True
        return False
    finally:
        mapapi.mapFreeObject(hobject)
        mapapi.mapFreeObject(hcontainer)


def DeleteObject(hmap, sourceSite, objectKey):
    """Удаляет объект редактируемой карты без копирования."""
    sourceObject = sitapi.mapCreateSiteObject(
        hmap, sourceSite, maptype.IDDOUBLE2, 0)
    if not sourceObject:
        return False
    try:
        if not sitapi.mapSeekSiteObject(hmap, sourceSite, sourceObject, objectKey):
            return False
        if mapapi.mapDeleteObject(sourceObject) == 0:
            WriteLog(tr('log_delete_fail', key=objectKey))
            return False
        WriteLog(tr('log_deleted', key=objectKey))
        return True
    finally:
        mapapi.mapFreeObject(sourceObject)


def CopyAndDeleteObject(hmap, sourceSite, archiveMap, archiveSite, objectKey):
    sourceObject = sitapi.mapCreateSiteObject(
        hmap, sourceSite, maptype.IDDOUBLE2, 0)
    archiveObject = 0
    if not sourceObject:
        return False
    try:
        if not sitapi.mapSeekSiteObject(hmap, sourceSite, sourceObject, objectKey):
            return False
        archiveObject = mapapi.mapCreateCopyObjectAsNew(archiveMap, sourceObject)
        if not archiveObject:
            WriteLog(tr('log_copy_fail', key=objectKey))
            return False
        if sitapi.mapChangeObjectMap(archiveObject, archiveMap, archiveSite) == 0:
            WriteLog(tr('log_change_map_fail', key=objectKey))
            return False
        if mapapi.mapCommitObject(archiveObject) == 0:
            WriteLog(tr('log_commit_fail', key=objectKey))
            return False
        if mapapi.mapDeleteObject(sourceObject) == 0:
            WriteLog(tr('log_delete_fail', key=objectKey))
            return False
        WriteLog(tr('log_moved', key=objectKey))
        return True
    finally:
        mapapi.mapFreeObject(sourceObject)
        if archiveObject:
            mapapi.mapFreeObject(archiveObject)


def GetArchiveFileName(hmap, sourceSite, sourceName):
    """Всегда формирует новое имя карты удаленных объектов."""
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


def FindOpenSiteByFileName(hmap, fileName):
    """Ищет уже открытую в документе карту по полному пути файла."""
    if not fileName:
        return 0
    try:
        normalized = os.path.normcase(os.path.abspath(fileName))
    except Exception:
        return 0
    siteCount = sitapi.mapGetSiteCount(hmap)
    for siteNumber in range(0, siteCount + 1):
        hsite = sitapi.mapGetSiteIdent(hmap, siteNumber)
        if not hsite:
            continue
        siteName = mapsyst.WTEXT(BUFFER_SIZE)
        if sitapi.mapGetSiteFileNameUn(
                hmap, hsite, siteName, siteName.size()) == 0:
            continue
        try:
            currentName = os.path.normcase(os.path.abspath(siteName.string()))
        except Exception:
            continue
        if currentName == normalized:
            return hsite
    return 0


def CreateArchiveMap(hmap, sourceSite, sourceName, archiveFileName):
    """Создаёт карту архива или открывает существующую для дозаписи.

    Возвращает (archiveMap, archiveSite, archiveFileName).
    """
    rscFileName = GetClassifierFileName(hmap, sourceSite)
    if not rscFileName:
        return 0, 0, u''
    if not archiveFileName:
        archiveFileName = GetArchiveFileName(hmap, sourceSite, sourceName)
    archiveFileName = NormalizeArchiveFileName(
        hmap, sourceSite, archiveFileName)
    if not archiveFileName:
        return 0, 0, u''

    # Если карта уже открыта в документе — дописываем в неё.
    existingSite = FindOpenSiteByFileName(hmap, archiveFileName)
    if existingSite:
        WriteLog(tr(
            'log_archive_open', name=archiveFileName, hsite=existingSite))
        return hmap, existingSite, archiveFileName

    # Если файл уже есть на диске — открываем и дописываем, не создаём заново.
    if os.path.isfile(archiveFileName):
        archiveSite = sitapi.mapOpenSiteForMapUn(
            hmap, mapsyst.WTEXT(archiveFileName), maptype.GENERIC_WRITE)
        if not archiveSite:
            WriteLog(tr('log_archive_open_fail', name=archiveFileName))
            return 0, 0, archiveFileName
        WriteLog(tr(
            'log_archive_open', name=archiveFileName, hsite=archiveSite))
        return hmap, archiveSite, archiveFileName

    directory = os.path.dirname(archiveFileName)
    if directory and not os.path.isdir(directory):
        try:
            os.makedirs(directory)
        except Exception as error:
            WriteLog(tr(
                'log_archive_fail', name=archiveFileName, error=error))
            return 0, 0, archiveFileName

    error = ctypes.c_long(0)
    archiveMap = mapapi.mapCreateSiteForMapEx(
        mapsyst.WTEXT(archiveFileName),
        mapsyst.WTEXT(os.path.splitext(os.path.basename(archiveFileName))[0]),
        mapsyst.WTEXT(rscFileName), 0, hmap, sourceSite, ctypes.byref(error))
    if not archiveMap:
        WriteLog(tr('log_archive_fail', name=archiveFileName, error=error.value))
        return 0, 0, archiveFileName
    archiveSite = sitapi.mapGetSiteIdent(archiveMap, 0)
    WriteLog(tr(
        'log_archive_ok', name=archiveFileName, hmap=archiveMap, hsite=archiveSite))
    return archiveMap, archiveSite, archiveFileName


def ProcessDeleteInnerObjects(hmap, hobj, settings):
    containerSelect = 0
    objectSelect = 0
    progress = 0
    try:
        # Одна и та же модель из файла загружается в HSELECT обеих карт.
        # "Одинаковый ключ" — ключ классификатора (mapObjectExcode), а не
        # уникальный номер объекта на карте (mapObjectKey): номера на разных
        # картах независимы и почти никогда не совпадают.
        containerSelect = CreateSelectContextFromModelFile(
            hmap, settings['containerSite'],
            settings['modelFileName'], settings['modelName'])
        objectSelect = CreateSelectContextFromModelFile(
            hmap, settings['objectSite'],
            settings['modelFileName'], settings['modelName'])

        containerIndex, containerCount = CollectContainerIndex(
            hmap, settings['containerSite'], containerSelect)
        objectInfos = CollectEditableObjects(
            hmap, settings['objectSite'], objectSelect)
        WriteLog(tr(
            'log_keys', container=containerCount, edited=len(objectInfos)))
        if not containerIndex or not objectInfos:
            return 0, False

        commonCount = 0
        for unusedKey, objectExcode, unusedFrame in objectInfos:
            if objectExcode in containerIndex:
                commonCount += 1
        WriteLog(tr('log_common_keys', count=commonCount))
        if commonCount == 0:
            return 0, False

        progress = mapapi.mapOpenProgressBar()
        archiveMap = 0
        archiveSite = 0
        saveToArchive = settings.get('saveToArchive', True)
        movedCount = 0
        cancelled = False
        totalCount = len(objectInfos)
        for index, objectInfo in enumerate(objectInfos, 1):
            objectKey, objectExcode, objectFrame = objectInfo
            percent = int(index * 100 / totalCount)
            if mapapi.mapProgressBar(
                    progress, percent, mapsyst.WTEXT(tr('progress'))) == -1:
                cancelled = True
                break
            containerItems = containerIndex.get(objectExcode)
            if not containerItems:
                continue
            if not IsObjectInsideSameKeyContainers(
                    hmap, settings['objectSite'], objectKey, objectFrame,
                    settings['containerSite'], containerItems):
                continue
            if saveToArchive:
                if not archiveMap:
                    archiveMap, archiveSite, archiveFileName = CreateArchiveMap(
                        hmap, settings['objectSite'], settings['objectMapName'],
                        settings['archiveFileName'])
                    if not archiveMap or not archiveSite:
                        raise RuntimeError(
                            tr('err_archive_map', name=archiveFileName))
                if CopyAndDeleteObject(
                        hmap, settings['objectSite'], archiveMap, archiveSite,
                        objectKey):
                    movedCount += 1
            elif DeleteObject(hmap, settings['objectSite'], objectKey):
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
    WriteLog(tr('log_dialog_maps', count=len(mapItems)))
    if len(mapItems) < 2:
        ShowMessage(tr('need_two_maps'), True)
        return None

    iniName = GetIniFileName(hmap)
    defaultContainerMap = mapItems[0][0]
    defaultObjectMap = mapItems[1][0]
    root = tkinter.Tk()
    root.title(tr('title'))
    root.wm_attributes('-topmost', 1)

    containerMapName = tkinter.StringVar()
    objectMapName = tkinter.StringVar()
    modelFileName = tkinter.StringVar()
    modelFileText = tkinter.StringVar()
    archiveFileName = tkinter.StringVar()
    archiveFileText = tkinter.StringVar()
    modelName = tkinter.StringVar()
    saveToArchive = tkinter.IntVar()
    result = {'value': None}
    dialogClosed = {'value': False}
    isRestoring = {'value': True}
    models = []

    mapNames = [mapItem[0] for mapItem in mapItems]

    def SetFileName(fileVariable, textVariable, fileName):
        fileVariable.set(fileName)
        textVariable.set(ShortenPath(fileName))

    def SyncFileName(fileVariable, textVariable):
        shownFileName = textVariable.get().strip().strip(u'"')
        fullFileName = fileVariable.get()
        if shownFileName == ShortenPath(fullFileName):
            textVariable.set(ShortenPath(fullFileName))
            return
        # При правке сокращённого пути сохраняем каталог полного имени.
        if u'...' in shownFileName and fullFileName:
            directory = os.path.dirname(fullFileName)
            baseName = os.path.basename(shownFileName)
            if directory and baseName:
                fileVariable.set(os.path.join(directory, baseName))
            else:
                fileVariable.set(shownFileName)
        else:
            fileVariable.set(shownFileName)
        textVariable.set(ShortenPath(fileVariable.get()))

    def RefreshModels():
        hsite = GetSiteByName(mapItems, containerMapName.get())
        if not hsite:
            hsite = GetSiteByName(mapItems, objectMapName.get())
        loadedModels = LoadModels(hmap, hsite, modelFileName.get())
        models[:] = [model[0] for model in loadedModels]
        modelCombo.configure(values=models)
        savedName = ReadSetting(
            iniName, u'Model', ReadSetting(iniName, u'ContainerModel', u''))
        if modelName.get() not in models:
            modelName.set(
                savedName if savedName in models else (
                    models[0] if models else u''))

    def ContainerMapChanged(*unused):
        hsite = GetSiteByName(mapItems, containerMapName.get())
        defaultFile = GetDefaultModelFile(hmap, hsite) if hsite else u''
        if isRestoring['value']:
            defaultFile = ReadSetting(
                iniName, u'ModelFile',
                ReadSetting(iniName, u'ContainerModelFile', defaultFile))
        SetFileName(modelFileName, modelFileText, defaultFile)
        RefreshModels()

    def ObjectMapChanged(*unused):
        if isRestoring['value']:
            return
        SetFileName(
            archiveFileName, archiveFileText, GetArchiveFileName(
                hmap, GetSiteByName(mapItems, objectMapName.get()),
                objectMapName.get()))

    def BrowseModelFile():
        fileName = askopenfilename(
            title=tr('dlg_select_models'),
            filetypes=[
                (tr('filetype_models'), u'*.vclx'),
                (tr('filetype_all'), u'*.*')])
        if fileName:
            SetFileName(modelFileName, modelFileText, fileName)
            RefreshModels()

    def BrowseArchiveFile():
        if not saveToArchive.get():
            return
        fileName = asksaveasfilename(
            title=tr('dlg_select_archive'),
            defaultextension=u'.sitx',
            filetypes=[
                (tr('filetype_sitx'), u'*.sitx'),
                (tr('filetype_all'), u'*.*')],
            initialfile=os.path.basename(archiveFileName.get()))
        if fileName:
            SetFileName(archiveFileName, archiveFileText, fileName)

    def UpdateArchiveControls(*unused):
        # Поле только для отображения (сокращённый путь), правка — через «Выбрать».
        entryState = 'readonly' if saveToArchive.get() else 'disabled'
        buttonState = 'normal' if saveToArchive.get() else 'disabled'
        archiveFileEntry.configure(state=entryState)
        archiveBrowseButton.configure(state=buttonState)
        archiveLabel.configure(state=buttonState)

    def AddModel():
        SyncFileName(modelFileName, modelFileText)
        hsite = GetSiteByName(mapItems, containerMapName.get())
        if not hsite:
            hsite = GetSiteByName(mapItems, objectMapName.get())
        parm = maptype.TASKPARMEX()
        parm.Handle = mapapi.mapGetHandleForMessage()
        activePage = ctypes.c_long(0)
        root.wm_attributes('-topmost', 0)
        try:
            mapselec.selSetSearchFilterUn(
                hmap, ctypes.byref(parm), ctypes.byref(activePage),
                mapsyst.WTEXT(tr('dlg_filter_title')))
        except Exception as error:
            WriteLog(tr('err_filter_dialog') + u': {0}'.format(error))
            ShowMessage(tr('err_filter_dialog'), True, root)
            return
        finally:
            root.wm_attributes('-topmost', 1)
        # После диалога перечитываем файл моделей и обновляем список.
        if hsite and not modelFileName.get():
            SetFileName(
                modelFileName, modelFileText,
                GetDefaultModelFile(hmap, hsite))
        selectedName = modelName.get()
        RefreshModels()
        if selectedName in models:
            modelName.set(selectedName)

    def OpenHelp():
        try:
            webbrowser.open(GetHelpUrl())
        except Exception as error:
            WriteLog(tr('log_help_fail', error=error))

    def SaveDialogSize():
        root.update_idletasks()
        WriteSettings(iniName, {
            u'DialogWidth': str(root.winfo_width())
        })

    def Run():
        SyncFileName(modelFileName, modelFileText)
        containerSite = GetSiteByName(mapItems, containerMapName.get())
        objectSite = GetSiteByName(mapItems, objectMapName.get())
        selectedModel = modelName.get()
        selectedModelFile = modelFileName.get()
        selectedArchiveFile = archiveFileName.get()
        if not containerSite or not objectSite:
            ShowMessage(tr('select_both_maps'), True, root)
            return
        if not IsSameClassifier(hmap, containerSite, objectSite):
            ShowMessage(tr('different_rsc'), True, root)
            return
        if (not selectedModel or selectedModel not in models or
                not selectedModelFile or not os.path.isfile(selectedModelFile)):
            ShowMessage(tr('models_not_found'), True, root)
            return
        if sitapi.mapGetSiteEditFlag(hmap, objectSite) == 0:
            ShowMessage(tr('map_not_editable'), True, root)
            return
        if saveToArchive.get() and not selectedArchiveFile:
            ShowMessage(tr('err_archive_map', name=u''), True, root)
            return
        result['value'] = {
            'containerSite': containerSite,
            'objectSite': objectSite,
            'objectMapName': objectMapName.get(),
            'archiveFileName': selectedArchiveFile,
            'saveToArchive': bool(saveToArchive.get()),
            'modelFileName': selectedModelFile,
            'modelName': selectedModel,
            'iniName': iniName,
            'iniValues': {
                u'ContainerMap': containerMapName.get(),
                u'ObjectMap': objectMapName.get(),
                u'ModelFile': selectedModelFile,
                u'Model': selectedModel,
                u'SaveToArchive': u'1' if saveToArchive.get() else u'0'
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
        tr('label_analyze_map'),
        tr('label_edit_map'),
        tr('label_model_file'),
        tr('label_model')
    )
    for row, label in enumerate(labels):
        tkinter.Label(root, text=label).grid(
            row=row, column=0, sticky='w', padx=6, pady=3)

    containerMapCombo = tkinter.ttk.Combobox(
        root, textvariable=containerMapName, values=mapNames, width=58,
        state='readonly')
    containerMapCombo.grid(row=0, column=1, columnspan=2, padx=6, pady=3, sticky='ew')

    objectMapCombo = tkinter.ttk.Combobox(
        root, textvariable=objectMapName, values=mapNames, width=58,
        state='readonly')
    objectMapCombo.grid(row=1, column=1, columnspan=2, padx=6, pady=3, sticky='ew')

    actionButtonWidth = max(len(tr('btn_browse')), len(tr('btn_add')))

    modelFileEntry = tkinter.Entry(
        root, textvariable=modelFileText, width=50, state='readonly')
    modelFileEntry.grid(row=2, column=1, padx=6, pady=3, sticky='ew')
    tkinter.Button(
        root, text=tr('btn_browse'), command=BrowseModelFile,
        width=actionButtonWidth).grid(row=2, column=2, padx=6, pady=3)

    modelCombo = tkinter.ttk.Combobox(
        root, textvariable=modelName, width=50, state='readonly')
    modelCombo.grid(row=3, column=1, padx=6, pady=3, sticky='ew')
    tkinter.Button(
        root, text=tr('btn_add'), command=AddModel,
        width=actionButtonWidth).grid(row=3, column=2, padx=6, pady=3)

    saveArchiveCheck = tkinter.Checkbutton(
        root, text=tr('check_save_archive'), variable=saveToArchive,
        command=UpdateArchiveControls)
    saveArchiveCheck.grid(
        row=4, column=0, columnspan=3, sticky='w', padx=6, pady=3)

    archiveLabel = tkinter.Label(root, text=tr('label_archive_map'))
    archiveLabel.grid(row=5, column=0, sticky='w', padx=6, pady=3)
    archiveFileEntry = tkinter.Entry(
        root, textvariable=archiveFileText, width=50, state='readonly')
    archiveFileEntry.grid(row=5, column=1, padx=6, pady=3, sticky='ew')
    archiveBrowseButton = tkinter.Button(
        root, text=tr('btn_browse'), command=BrowseArchiveFile,
        width=actionButtonWidth)
    archiveBrowseButton.grid(row=5, column=2, padx=6, pady=3)

    buttonFrame = tkinter.Frame(root)
    buttonFrame.grid(row=6, column=0, columnspan=3, padx=6, pady=6, sticky='w')
    tkinter.Button(buttonFrame, text=tr('btn_run'), command=Run, width=10).pack(
        side='left')
    tkinter.Button(buttonFrame, text=tr('btn_exit'), command=Cancel, width=10).pack(
        side='left', padx=8)
    tkinter.Button(buttonFrame, text=tr('btn_help'), command=OpenHelp, width=10).pack(
        side='left')
    root.columnconfigure(1, weight=1)

    containerMapName.set(ReadSetting(iniName, u'ContainerMap', defaultContainerMap))
    if containerMapName.get() not in mapNames:
        containerMapName.set(defaultContainerMap)
    objectMapName.set(ReadSetting(iniName, u'ObjectMap', defaultObjectMap))
    if objectMapName.get() not in mapNames:
        objectMapName.set(defaultObjectMap)
    saveToArchive.set(
        1 if ReadSetting(iniName, u'SaveToArchive', u'1') != u'0' else 0)
    containerMapName.trace('w', ContainerMapChanged)
    objectMapName.trace('w', ObjectMapChanged)
    ContainerMapChanged()
    # Имя карты удаленных объектов всегда новое: не читаем и не пишем в INI.
    SetFileName(
        archiveFileName, archiveFileText, GetArchiveFileName(
            hmap, GetSiteByName(mapItems, objectMapName.get()),
            objectMapName.get()))
    UpdateArchiveControls()
    isRestoring['value'] = False
    root.update_idletasks()
    minimumWidth = root.winfo_reqwidth()
    # Высота — ровно по содержимому с небольшим запасом, без восстановления
    # старого значения из INI (оно могло остаться от прежней разметки).
    dialogHeight = root.winfo_reqheight() + 8
    try:
        dialogWidth = max(minimumWidth, int(ReadSetting(
            iniName, u'DialogWidth', str(minimumWidth))))
    except ValueError:
        dialogWidth = minimumWidth
    root.minsize(minimumWidth, dialogHeight)
    root.geometry(u'{0}x{1}'.format(dialogWidth, dialogHeight))
    root.protocol('WM_DELETE_WINDOW', Cancel)
    root.eval('tk::PlaceWindow . center')
    root.resizable(True, False)
    root.mainloop()
    return result['value']


def RunDeleteInnerObjects(hmap, hobj):
    RefreshLang()
    WriteLog(tr('log_start', hmap=hmap, hobj=hobj))
    settings = GetDialogSettings(hmap)
    if not settings:
        return 0
    try:
        WriteSettings(settings['iniName'], settings['iniValues'])
        movedCount, cancelled = ProcessDeleteInnerObjects(hmap, hobj, settings)
        mapapi.mapInvalidate()
        if cancelled:
            ShowMessage(tr('cancelled', count=movedCount))
            return 0
        if settings.get('saveToArchive', True):
            ShowMessage(tr('done', count=movedCount))
        else:
            ShowMessage(tr('done_delete', count=movedCount))
        return 1
    except RuntimeError as error:
        ShowMessage(str(error), True)
    except Exception as error:
        ShowMessage(tr('exec_error', error=error), True)
    return 0


def DeleteInnerObjectsScript(hmap, hobj):
    return RunDeleteInnerObjects(hmap, hobj)


def DeleteInnerObjects(hmap, hobj):  #caption:Удалить объекты внутри объектов другой карты
    """Точка входа скрипта Панорамы. Возвращает 1 при успехе, 0 при ошибке."""
    return RunDeleteInnerObjects(hmap, hobj)
