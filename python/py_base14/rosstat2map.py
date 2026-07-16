import calendar
import ctypes
import json
import logging
import os
import re
import shutil
import ssl
import subprocess
import sys
import time
import zipfile
import webbrowser
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, NamedTuple
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import tkinter as tk
from tkinter import colorchooser, messagebox, ttk
try:
    import mapsyst
    import mapapi
    import maptype
    import mapgdi
except Exception:
    mapsyst = None
    mapapi = None
    maptype = None
    mapgdi = None

_rscapi_module: Optional[Any] = None
_rscapi_import_tried = False

def _get_rscapi_optional():
    """Импорт rscapi"""
    global _rscapi_module, _rscapi_import_tried
    if _rscapi_import_tried:
        return _rscapi_module
    _rscapi_import_tried = True
    try:
        import rscapi
        _rscapi_module = rscapi
    except Exception:
        _rscapi_module = None
    return _rscapi_module

PORTAL_PAGE_URL = 'https://rosstat.gov.ru/folder/11109/document/13259'
_HELP_URL = 'https://help.gisserver.ru/v15/russian/mapscena/index.html?rosstatthematic.html'
MAP_SCALE_FOR_THEMATIC_MIN = 100
MAP_SCALE_FOR_THEMATIC_MAX = 200000000
MAP_REAL_SHOW_SCALE_DENOMINATOR = 40000000
THEMATIC_C_INT_MAX = 2147483647
ARCHIVE_URL_OVERRIDE: str = ''
SCRIPT_DIR = Path(__file__).resolve().parent
_pre = SCRIPT_DIR / '.rosstat2map_paths_pending'
DATA_DIR = _pre
DOWNLOAD_DIR = _pre / 'downloads'
EXTRACT_DIR = _pre / 'extracted'
_excel_code_index_cache: Optional[Tuple[float, Dict[str, Path]]] = None
_excel_search_roots: List[Path] = [EXTRACT_DIR]
_data_paths_initialized = False
_log_initialized = False

def init_data_paths() -> None:
    """Каталог данных Panorama.Cache"""
    global DATA_DIR, DOWNLOAD_DIR, EXTRACT_DIR, _excel_search_roots, _data_paths_initialized
    if _data_paths_initialized:
        return
    if mapapi is None:
        raise RuntimeError('rosstat2map: ошибка запуска. Используйте ГИС Панорама для запуска скрипта')
    try:
        ptr = mapapi.mapGetCachePathUn()
        if not ptr:
            raise RuntimeError('Не удалось получить путь к кэшу')
        text = ctypes.wstring_at(ptr)
        if not (text and text.strip()):
            raise RuntimeError('Пустая строка пути к кэшу')
        cache_root = Path(text.strip().rstrip('\\/'))
    except RuntimeError:
        raise
    except Exception as exc:
        raise RuntimeError(f'rosstat2map: ошибка инициализации: {exc}') from exc
    DATA_DIR = cache_root / 'rosstat2map'
    DOWNLOAD_DIR = DATA_DIR / 'downloads'
    EXTRACT_DIR = DATA_DIR / 'extracted'
    _excel_search_roots = [EXTRACT_DIR]
    _data_paths_initialized = True

def get_logger() -> logging.Logger:
    return logging.getLogger('rosstat2map')

def write_diag_pair(msg_before: str, msg_after: str, msg_type: Optional[int]=None) -> None:
    """Записать пару сообщений в диагностику Панорамы"""
    try:
        if mapapi is None or mapsyst is None:
            return
        if not hasattr(mapapi, 'mapIsDiagnostics') or not mapapi.mapIsDiagnostics():
            return
        mtype = msg_type if isinstance(msg_type, int) else getattr(maptype, 'MT_INFO', 0)
        prefix = 'TPythonScript::Rosstat2Map(): '
        b = msg_before or ''
        a = msg_after or ''
        line = b + ((' ' + a) if (b and a) else a)
        mapapi.mapWriteToDiagnosticsLog(mapsyst.WTEXT(prefix + line), mapsyst.WTEXT(''), mtype)
    except Exception:
        pass

def _log_thematic_title_keys_diag(title: str, detail: str) -> None:
    """Диагностика Панорамы при включённом режиме диагностики."""
    try:
        if mapapi is not None and mapsyst is not None:
            if hasattr(mapapi, 'mapIsDiagnostics') and mapapi.mapIsDiagnostics():
                write_diag_pair(title, detail, getattr(maptype, 'MT_INFO', 0))
    except Exception:
        pass

class _DiagLogHandler(logging.Handler):
    """Обработчик логов Python для записи в диагностику Панорамы"""
    def emit(self, record: logging.LogRecord) -> None:
        try:
            if record.levelno < logging.ERROR:
                return
            message = self.format(record)
            mtype = getattr(maptype, 'MT_ERROR', 1)
            write_diag_pair(message, '', mtype)
        except Exception:
            pass

def setup_script_logging() -> logging.Logger:
    """Настройка логирования Python для записи в диагностику Панорамы"""
    init_data_paths()
    global _log_initialized
    log = get_logger()
    log.setLevel(logging.ERROR)
    log.propagate = False
    if _log_initialized:
        return log
    _log_initialized = True
    handler = _DiagLogHandler()
    handler.setLevel(logging.ERROR)
    handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
    log.addHandler(handler)
    return log

def _run_subprocess_hidden(cmd: List[str], timeout: Optional[int]=None) -> subprocess.CompletedProcess:
    """Запуск процесса скрыто (без отображения окна)"""
    kwargs = {'capture_output': True, 'text': True, 'check': False}
    if timeout is not None:
        kwargs['timeout'] = timeout
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        kwargs['startupinfo'] = startupinfo
        kwargs['creationflags'] = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
    return subprocess.run(cmd, **kwargs)

@dataclass(frozen=True)
class MaterialType:
    code: str
    name: str
MATERIAL_TYPES: List[MaterialType] = [MaterialType('01-01', 'Индекс промышленного производства'), MaterialType('01-02', 'Индекс производства по виду экономической деятельности «Добыча полезных ископаемых»'), MaterialType('01-03', 'Индекс производства по виду экономической деятельности «Обрабатывающие производства»'), MaterialType('01-04', 'Индекс производства по виду экономической деятельности «Обеспечение электрической энергией, газом и паром; кондиционирование воздуха»'), MaterialType('01-05', 'Индекс производства по виду экономической деятельности "Водоснабжение; водоотведение, организация сбора и утилизация отходов, деятельность по ликвидации загрязнений"'), MaterialType('01-06', 'Отгружено товаров собственного производства, выполнено работ и услуг собственными силами'), MaterialType('01-07', 'Отгружено товаров собственного производства, выполнено работ и услуг собственными силами по виду экономической деятельности «Рыболовство, рыбоводство»'), MaterialType('01-08', 'Темпы роста (снижения) объемов производства рыбы морской живой, не являющейся продукцией рыбоводства'), MaterialType('01-09', 'Темпы роста (снижения) объемов производства рыбы морской свежей или охлажденной, не являющейся продукцией рыбоводства'), MaterialType('01-10', 'Темпы роста (снижения) объемов производства рыбы переработанной и консервированной, ракообразных и моллюсков'), MaterialType('01-11', 'Производство электроэнергии'), MaterialType('02-01', 'Индекс производства продукции сельского хозяйства'), MaterialType('03-01', 'Объем работ, выполненных по виду деятельности «Строительство»'), MaterialType('03-02', 'Строительство жилых домов'), MaterialType('04-01', 'Перевозки грузов автомобильным транспортом организаций всех видов экономической деятельности без субъектов малого предпринимательства'), MaterialType('05-01', 'Оборот розничной торговли'), MaterialType('05-02', 'Оборот розничной торговли пищевыми продуктами, включая напитки, и табачными изделиями'), MaterialType('05-03', 'Оборот розничной торговли непродовольственными товарами'), MaterialType('05-04', 'Экспорт'), MaterialType('05-05', 'Импорт'), MaterialType('06-01', 'Объем платных услуг населению'), MaterialType('07-01', 'Объем инвестиций в основной капитал (по полному кругу хозяйствующих субъектов)'), MaterialType('08-01', 'Сальдированный финансовый результат деятельности организаций'), MaterialType('08-02', 'Прибыль прибыльных организаций'), MaterialType('08-03', 'Доля прибыльных предприятий и организаций'), MaterialType('08-04', 'Доля убыточных предприятий и организаций'), MaterialType('08-05', 'Кредиторская задолженность организаций'), MaterialType('08-06', 'Дебиторская задолженность организаций'), MaterialType('09-01', 'Индексы потребительских цен на товары и услуги'), MaterialType('09-02', 'Индексы потребительских цен на продовольственные товары'), MaterialType('09-03', 'Индексы потребительских цен на непродовольственные товары'), MaterialType('09-04', 'Индексы потребительских цен на услуги'), MaterialType('09-05', 'Индексы потребительских тарифов на отдельные виды жилищно-коммунальных услуг'), MaterialType('09-06', 'Стоимость фиксированного набора потребительских товаров и услуг для межрегиональных сопоставлений покупательной способности населения'), MaterialType('10-01', 'Индексы цен производителей промышленных товаров'), MaterialType('10-02', 'Индексы цен производителей на реализованную сельскохозяйственную продукцию'), MaterialType('10-03', 'Индексы цен на продукцию (затраты, услуги) инвестиционного назначения'), MaterialType('10-04', 'Индексы цен (тарифов) на грузовые перевозки'), MaterialType('10-05', 'Средние цены на первичном рынке жилья'), MaterialType('11-01', 'Среднедушевые денежные доходы населения'), MaterialType('11-02', 'Динамика реальных денежных доходов'), MaterialType('12-01', 'Среднемесячная номинальная начисленная заработная плата работников'), MaterialType('12-02', 'Среднемесячная заработная плата работников сельского хозяйства'), MaterialType('12-03', 'Просроченная задолженность по заработной плате'), MaterialType('12-04', 'Просроченная задолженность по заработной плате по видам экономической деятельности'), MaterialType('12-05', 'Численность работников, перед которыми имеется просроченная задолженность по заработной плате'), MaterialType('13-01', 'Численность и состав рабочей силы в возрасте 15-72 лет'), MaterialType('14-01', 'Численность работников, выбывших из организаций'), MaterialType('14-02', 'Численность работников, принятых в организации'), MaterialType('14-03', 'Численность работников, намеченных к высвобождению в следующем месяце'), MaterialType('14-04', 'Численность требуемых работников на вакантные рабочие места'), MaterialType('14-05', 'Численность работников, работавших неполное рабочее время'), MaterialType('15-01', 'Среднесписочная численность работников на предприятиях малого и среднего бизнеса (оценка)')]
DISPLAY_TO_CODE: Dict[str, str] = {item.name: item.code for item in MATERIAL_TYPES}

def _detect_lang() -> str:
    """Определяет язык интерфейса ГИС Панорама"""
    try:
        if mapapi is None or maptype is None:
            return 'ru'
        code = mapapi.mapGetMapAccessLanguage()
        if code == getattr(maptype, 'ML_RUSSIAN', 2):
            return 'ru'
        if code == getattr(maptype, 'ML_ENGLISH', 1):
            return 'en'
        return 'en'
    except Exception:
        return 'ru'

_LANG = _detect_lang()

_STR_RU: Dict[str, str] = {'title': 'Росстат. Статистика', 'stats_title_base': 'Росстат. Статистика', 'stats_loaded_with_date': 'загружено {n} {word} {date}', 'stats_loaded_no_date': 'загружено {n} {word}', 'stats_headline_last_fetch': 'последняя загрузка с портала {date}', 'btn_refresh': 'Обновить', 'btn_get': 'Получить', 'status_ready_load': 'Готово к загрузке данных.', 'status_cached_tables': 'Найдены ранее подготовленные таблицы Excel: {ready} из {total}. Можно сразу выбирать таблицу; повторная загрузка не требуется.', 'label_material_type': 'Тип данных для ведения мониторинга социально-экономического положения субъектов Российской Федерации:', 'param_frame_title': 'Параметры построения тематической карты', 'label_value_column': 'Столбец со значениями:', 'label_values_in_column': 'Значения в столбце', 'label_of_n_columns': 'из {n}', 'label_min': 'Минимум:', 'label_max': 'Максимум:', 'status_label': 'Статус:', 'btn_thematic_map': 'Тематическая карта', 'btn_execute': 'Выполнить', 'btn_exit': 'Выход', 'btn_help': 'Помощь', 'preview_not_loaded': 'Данные еще не загружены.', 'preview_title': 'Предпросмотр: {name}', 'preview_mode_full': 'Вся таблица', 'preview_mode_value_column': 'Выбранный столбец значений', 'preview_column_oob': 'Столбец {col} недоступен (в предпросмотре не более {n} колонок).', 'preview_no_subject_rows': 'В прочитанном фрагменте таблицы нет строк субъектов РФ (без РФ и федеральных округов).', 'preview_col_subject_name': 'Название субъекта', 'status_fetch_refresh_cached': 'Идет актуализация данных: найдены ранее подготовленные ({ready} таблиц), выполняется повторное скачивание и распаковка данных...', 'status_fetch_get_url': 'Идет актуализация данных: получение актуальной ссылки на архив... ', 'status_fetch_download': 'Идет актуализация данных: скачивание архива с портала Росстата... ', 'status_fetch_unpack': 'Идет актуализация данных: архив {name} загружен, выполняется распаковка... ', 'status_fetch_pip': 'Идет установка зависимостей Python: {pkg}...', 'status_deps_warning': 'Внимание: не все зависимости Python для чтения Excel установлены', 'dlg_deps_title': 'Зависимости Python', 'status_fetch_prepare': 'Идет актуализация данных: подготовка данных для просмотра... ', 'status_fetch_done': 'Готово. Архив скачан с портала и распакован. Доступно Excel-файлов: {n}.', 'status_error': 'Ошибка: {err}', 'dlg_error': 'Ошибка', 'http_portal_transient': 'Портал Росстата временно недоступен (HTTP {code}: {detail}). Подождите и снова нажмите «Обновить». Если Excel-таблицы уже загружались ранее, ими можно пользоваться без повторной загрузки', 'status_execute_done': 'Построение завершено. Открыт результат: {name}', 'status_execute_error': 'Ошибка выполнения: {err}', 'dlg_execute_error': 'Ошибка выполнения', 'dlg_tk_error': 'Ошибка Tk', 'color_min_title': 'Цвет для минимума', 'color_max_title': 'Цвет для максимума', 'preview_table_not_found': 'Таблица для выбранного типа пока не найдена:\n{path}\n\nСначала выполните загрузку и распаковку данных.', 'preview_empty': 'Файл пустой:\n{path}', 'preview_file_line': 'Файл: {path}', 'preview_col_numbers_hint': 'Номера колонок (слева направо).', 'preview_read_error': 'Не удалось прочитать таблицу:\n{path}\n\n{err}', 'dep_notice': 'Перед распаковкой обнаружены отсутствующие зависимости для чтения Excel.\nPython: {python_exe}\n\nНе найдены: {missing}\n\nОткройте cmd/PowerShell от имени администратора и выполните:\n{commands}', 'app_short_name': 'Rosstat2Map'}
_STR_EN: Dict[str, str] = {'title': 'Rosstat. Statistics', 'stats_title_base': 'Rosstat. Statistics', 'stats_loaded_with_date': 'loaded {n} {word} {date}', 'stats_loaded_no_date': 'loaded {n} {word}', 'stats_headline_last_fetch': 'last download from portal {date}', 'btn_refresh': 'Refresh', 'btn_get': 'Get', 'status_ready_load': 'Ready to load data.', 'status_cached_tables': 'Previously prepared Excel tables found: {ready} of {total}. You can select a table; no need to download again.', 'label_material_type': 'Data type for monitoring the socio-economic situation of the constituent entities of the Russian Federation:', 'param_frame_title': 'Thematic map build parameters', 'label_value_column': 'Value column:', 'label_values_in_column': 'Values in column', 'label_of_n_columns': 'of {n}', 'label_min': 'Minimum:', 'label_max': 'Maximum:', 'status_label': 'Status:', 'btn_thematic_map': 'Thematic map', 'btn_execute': 'Execute', 'btn_exit': 'Exit', 'btn_help': 'Help', 'preview_not_loaded': 'Data has not been loaded yet.', 'preview_title': 'Preview: {name}', 'preview_mode_full': 'Full table', 'preview_mode_value_column': 'Selected value column', 'preview_column_oob': 'Column {col} is out of range (preview rows have at most {n} columns).', 'preview_no_subject_rows': 'No RF subject rows in the preview fragment (excluding Russia and federal districts).', 'preview_col_subject_name': 'Subject name', 'status_fetch_refresh_cached': 'Updating data: {ready} prepared table(s) found, re-downloading and unpacking...', 'status_fetch_get_url': 'Updating data: fetching archive link... ', 'status_fetch_download': 'Updating data: downloading archive from Rosstat... ', 'status_fetch_unpack': 'Updating data: archive {name} downloaded, unpacking... ', 'status_fetch_pip': 'Installing Python dependency: {pkg}...', 'status_deps_warning': 'Warning: not all Python dependencies for Excel are installed', 'dlg_deps_title': 'Python dependencies', 'status_fetch_prepare': 'Updating data: preparing preview... ', 'status_fetch_done': 'Done. Archive downloaded and unpacked. Excel files available: {n}.', 'status_error': 'Error: {err}', 'dlg_error': 'Error', 'http_portal_transient': 'Rosstat portal is temporarily unavailable (HTTP {code}: {detail}). Wait and click Refresh again', 'status_execute_done': 'Build finished. Result opened: {name}', 'status_execute_error': 'Execution error: {err}', 'dlg_execute_error': 'Execution error', 'dlg_tk_error': 'Tk error', 'color_min_title': 'Color for minimum', 'color_max_title': 'Color for maximum', 'preview_table_not_found': 'Table for the selected type is not found yet:\n{path}\n\nDownload and unpack data first.', 'preview_empty': 'File is empty:\n{path}', 'preview_file_line': 'File: {path}', 'preview_col_numbers_hint': 'Column numbers (left to right).', 'preview_read_error': 'Could not read table:\n{path}\n\n{err}', 'dep_notice': 'Missing dependencies for reading Excel were found before unpacking.\nPython: {python_exe}\n\nNot found: {missing}\n\nOpen cmd/PowerShell as administrator and run:\n{commands}', 'app_short_name': 'Rosstat2Map'}
_STR: Dict[str, Dict[str, str]] = {'ru': _STR_RU, 'en': _STR_EN}

_MONTH_NAMES_RU: Tuple[str, ...] = ('январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь')
_QUARTER_LABELS_RU: Tuple[str, ...] = ('I квартал', 'II квартал', 'III квартал', 'IV квартал')
_RU_MONTH_SUBSTRINGS: Tuple[Tuple[str, int], ...] = (
    ('сентябрь', 9),
    ('октябрь', 10),
    ('ноябрь', 11),
    ('декабрь', 12),
    ('феврал', 2),
    ('январ', 1),
    ('апрел', 4),
    ('август', 8),
    ('сентябр', 9),
    ('октябр', 10),
    ('ноябр', 11),
    ('декабр', 12),
    ('июль', 7),
    ('июнь', 6),
    ('март', 3),
    ('мая', 5),
    ('май', 5),
)

class ThematicPeriod(NamedTuple):
    """Период для подписи и имени карты: месяц, квартал, полугодие или диапазон месяцев; trusted — с шапки таблицы (не угадывание)"""
    year: int
    month: int
    quarter: Optional[int]
    trusted: bool
    month_from: int = 0
    half_year: Optional[int] = None

    def stem_month_part(self) -> int:
        """Вторая часть stem «.ГГГГ.MM»: квартал — последний месяц квартала; полугодие — 06/12; диапазон — последний месяц"""
        if self.half_year == 1:
            return 6
        if self.half_year == 2:
            return 12
        if self.quarter is not None and 1 <= self.quarter <= 4:
            return self.quarter * 3
        return max(0, min(12, int(self.month)))


def format_thematic_period_caption(period: ThematicPeriod) -> str:
    """Подпись периода у спинбокса: месяц, диапазон, квартал, полугодие или только год"""
    y = int(period.year)
    if not (1900 <= y <= 2100):
        return ''
    mf = int(period.month_from)
    mt = int(period.month)
    hy = period.half_year
    if hy == 1:
        if _LANG == 'ru':
            return f'(I полугодие {y} год)'
        return f'(H1 {y})'
    if hy == 2:
        if _LANG == 'ru':
            return f'(II полугодие {y} год)'
        return f'(H2 {y})'
    if period.quarter is not None and 1 <= period.quarter <= 4:
        q = int(period.quarter)
        if _LANG == 'ru':
            return f'({_QUARTER_LABELS_RU[q - 1]} {y} год)'
        return f'(Q{q} {y})'
    if 1 <= mf <= 12 and 1 <= mt <= 12 and mf != mt:
        if _LANG == 'ru':
            return f'({_MONTH_NAMES_RU[mf - 1]}–{_MONTH_NAMES_RU[mt - 1]} {y} год)'
        return f'({calendar.month_name[mf]}–{calendar.month_name[mt]} {y})'
    m = mt
    if 1 <= m <= 12:
        if _LANG == 'ru':
            return f'({_MONTH_NAMES_RU[m - 1]} {y} год)'
        return f'({calendar.month_name[m]} {y})'
    if m == 0:
        if _LANG == 'ru':
            return f'({y} год)'
        return f'({y})'
    return ''


def tr(key: str, **kwargs) -> str:
    """Возвращает локализованную строку по ключу и одновременно подставляет параметры через format"""
    s = _STR.get(_LANG, _STR['en']).get(key, key)
    if kwargs:
        try:
            return s.format(**kwargs)
        except Exception:
            return s
    return s

def build_selector_labels() -> List[str]:
    """Построение списка меток для выбора типа данных"""
    labels: List[str] = []
    for idx, item in enumerate(MATERIAL_TYPES, start=1):
        text = re.sub('\\s+', ' ', item.name).strip()
        labels.append(f'{idx:02d}. {text}')
    return labels

def ensure_dirs() -> None:
    """Создание необходимых каталогов для загрузки и распаковки данных"""
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)

def portal_fetch_meta_path() -> Path:
    return DATA_DIR / 'portal_fetch_meta.json'

def load_portal_fetch_meta() -> Optional[Dict[str, Any]]:
    path = portal_fetch_meta_path()
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        return data if isinstance(data, dict) else None
    except Exception:
        return None

def save_portal_fetch_meta(file_count: int) -> None:
    """Сохранение метаданных о загрузке портала Росстата"""
    ensure_dirs()
    payload = {'fetched_at': date.today().isoformat(), 'file_count': int(file_count)}
    portal_fetch_meta_path().write_text(json.dumps(payload, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')

def _files_word_declension(n: int) -> str:
    """Возвращает слово «файл», «файла» или «файлов» в зависимости от числа"""
    if _LANG != 'ru':
        return 'file' if n == 1 else 'files'
    k = abs(int(n)) % 100
    if k % 10 == 1 and k != 11:
        return 'файл'
    if k % 10 in (2, 3, 4) and k not in (12, 13, 14):
        return 'файла'
    return 'файлов'

def format_statistics_headline(file_count: int, fetched_iso_date: Optional[str]) -> str:
    """Форматирование заголовка статистики: количество файлов и дата последней загрузки"""
    base = tr('stats_title_base')
    disp = fetched_iso_date.replace('-', '/') if fetched_iso_date else ''
    if file_count > 0:
        word = _files_word_declension(file_count)
        if disp:
            detail = tr('stats_loaded_with_date', n=file_count, word=word, date=disp)
        else:
            detail = tr('stats_loaded_no_date', n=file_count, word=word)
        return f'{base} ({detail})'
    if disp:
        return f'{base} ({tr("stats_headline_last_fetch", date=disp)})'
    return base

def _is_ssl_or_tls_handshake_failure(exc: BaseException) -> bool:
    """True, если сбой похож на проблему TLS/SSL (в т.ч. когда reason не типизирован как ssl.SSLError)."""
    if isinstance(exc, ssl.SSLError):
        return True
    if isinstance(exc, URLError):
        r = exc.reason
        if isinstance(r, ssl.SSLError):
            return True
        if isinstance(r, BaseException) and _is_ssl_or_tls_handshake_failure(r):
            return True
    msg = str(exc).lower()
    if 'eof occurred' in msg or 'violation of protocol' in msg:
        return True
    if 'certificate verify failed' in msg or 'ssl routines' in msg:
        return True
    if 'wrong version number' in msg or 'tlsv1' in msg:
        return True
    if '[ssl:' in msg or ' _ssl.c:' in msg:
        return True
    return False


def _ssl_context_tls12_only() -> ssl.SSLContext:
    """Жёстко TLS 1.2 — иногда снимает сбои совместимости при «ломаных» переговорах версии."""
    proto = getattr(ssl, 'PROTOCOL_TLS_CLIENT', None)
    if proto is None:
        proto = getattr(ssl, 'PROTOCOL_TLS', ssl.PROTOCOL_SSLv23)
    try:
        ctx = ssl.SSLContext(proto)
    except Exception:
        return ssl.create_default_context()
    try:
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2
        ctx.maximum_version = ssl.TLSVersion.TLSv1_2
    except (AttributeError, ValueError):
        return ssl.create_default_context()
    return ctx


def _ssl_context_unverified_seclevel1() -> ssl.SSLContext:
    """Снижение SECLEVEL для OpenSSL 3+ при отказе сервера на строгих наборах шифров."""
    ctx = ssl._create_unverified_context()
    try:
        ctx.set_ciphers('DEFAULT:@SECLEVEL=1')
    except Exception:
        pass
    try:
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    except (AttributeError, ValueError):
        pass
    return ctx


def _http_status_retryable(code: int) -> bool:
    """Коды ответа, при которых имеет смысл повторить запрос (перегрузка шлюза, таймаут upstream)."""
    return code in (408, 429, 500, 502, 503, 504)


def _urlopen_with_http_retries(req: Request, timeout: int, ctx: Optional[ssl.SSLContext], *, attempts: int=5, delay_sec: float=2.5):
    """urlopen с повторами при временных HTTP-ошибках (в т.ч. 502 Bad Gateway у портала)."""
    last_http: Optional[HTTPError] = None
    for i in range(int(attempts)):
        try:
            if ctx is None:
                return urlopen(req, timeout=timeout)
            return urlopen(req, context=ctx, timeout=timeout)
        except HTTPError as exc:
            last_http = exc
            if _http_status_retryable(exc.code) and i < attempts - 1:
                time.sleep(delay_sec * (i + 1))
                continue
            raise
    if last_http is not None:
        raise last_http
    raise RuntimeError('urlopen: внутренняя ошибка повторов HTTP')


def _urlopen_with_ssl_fallback(url: str, timeout: int=60):
    """HTTPS: несколько стратегий SSL/TLS (Панорама / старый OpenSSL / особенности портала)."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.5'}
    req = Request(url, headers=headers)
    strategies: List[Tuple[str, Optional[ssl.SSLContext]]] = [('по умолчанию', None)]
    try:
        ctx12 = _ssl_context_tls12_only()
        strategies.append(('TLS 1.2', ctx12))
    except Exception:
        pass
    try:
        import certifi
        strategies.append(('certifi', ssl.create_default_context(cafile=certifi.where())))
    except Exception:
        pass
    strategies.append(('без проверки сертификата', ssl._create_unverified_context()))
    strategies.append(('без проверки, SECLEVEL=1', _ssl_context_unverified_seclevel1()))
    last: Optional[BaseException] = None
    for name, ctx in strategies:
        try:
            response = _urlopen_with_http_retries(req, timeout, ctx)
            note = None if ctx is None and name == 'по умолчанию' else f'SSL: использован режим «{name}».'
            return (response, note)
        except HTTPError:
            raise
        except (URLError, OSError) as exc:
            last = exc
            if not _is_ssl_or_tls_handshake_failure(exc):
                raise
            continue
    if last is not None:
        raise last
    raise RuntimeError('urlopen: не удалось установить HTTPS-соединение')

def _pick_latest_info_stat_rar_url(candidates: List[str]) -> Optional[str]:
    """Выбор последней ссылки на архив"""
    scored: List[Tuple[int, int, str]] = []
    for raw in candidates:
        u = raw.strip()
        if not u:
            continue
        name = u.split('/')[-1].split('?')[0]
        m = re.match('info-stat-(\\d+)-(\\d+)\\.rar$', name, re.IGNORECASE)
        if m:
            month_s, year_s = (m.group(1), m.group(2))
            scored.append((int(year_s), int(month_s), u))
    if scored:
        scored.sort(reverse=True)
        return scored[0][2]
    return candidates[-1] if candidates else None

def find_latest_archive_url() -> Tuple[str, Optional[str]]:
    """Поиск последней ссылки на архив"""
    log = get_logger()
    override = (ARCHIVE_URL_OVERRIDE or '').strip()
    if override:
        return (override, None)
    response, ssl_note = _urlopen_with_ssl_fallback(PORTAL_PAGE_URL, timeout=30)
    with response:
        html = response.read().decode('utf-8', errors='ignore')
    abs_matches = re.findall('https?://[^\\"\'<> ]+/storage/mediabank/[^\\"\'<> ]+\\.rar', html, flags=re.IGNORECASE)
    rel_matches = re.findall('/storage/mediabank/[^\\"\'<> ]+\\.rar', html, flags=re.IGNORECASE)
    all_urls: List[str] = list(abs_matches)
    for rel in rel_matches:
        all_urls.append(urljoin(PORTAL_PAGE_URL, rel))
    seen: Set[str] = set()
    unique: List[str] = []
    for u in all_urls:
        if u not in seen:
            seen.add(u)
            unique.append(u)
    if not unique:
        log.error('На странице не найдена ссылка .rar (длина HTML=%s)', len(html))
        raise RuntimeError('На странице не найдена ссылка на архив .rar')
    url = _pick_latest_info_stat_rar_url(unique)
    if not url:
        raise RuntimeError('Не удалось выбрать ссылку на архив .rar')
    return (url, ssl_note)

def archive_local_path_from_url(url: str) -> Path:
    """Построение локального пути для сохранения архива"""
    local_name = url.split('/')[-1].split('?')[0]
    return DOWNLOAD_DIR / local_name

def download_archive(url: str) -> Tuple[Path, Optional[str]]:
    """Скачивание архива с портала Росстата"""
    archive_path = archive_local_path_from_url(url)
    response, ssl_note = _urlopen_with_ssl_fallback(url, timeout=60)
    with response:
        with open(archive_path, 'wb') as out_file:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                if chunk:
                    out_file.write(chunk)
    return (archive_path, ssl_note)

def detect_archive_kind(path: Path) -> str:
    """Определение типа архива"""
    with open(path, 'rb') as f:
        sig = f.read(8)
    if sig.startswith(b'Rar!\x1a\x07'):
        return 'rar'
    if sig.startswith(b'PK\x03\x04'):
        return 'zip'
    return 'unknown'

def invalidate_excel_index_cache() -> None:
    """Сброс кэша индекса Excel"""
    global _excel_code_index_cache
    _excel_code_index_cache = None

def set_excel_search_roots(roots: List[Path]) -> None:
    """Установка корневых каталогов для поиска Excel-файлов"""
    global _excel_search_roots
    unique: List[Path] = []
    seen = set()
    for root in roots:
        rp = root.resolve()
        if str(rp) in seen:
            continue
        seen.add(str(rp))
        unique.append(rp)
    _excel_search_roots = unique or [EXTRACT_DIR]
    invalidate_excel_index_cache()

def list_excel_files(roots: List[Path]) -> List[Path]:
    """Поиск всех Excel-файлов в указанных каталогах"""
    result: List[Path] = []
    for root in roots:
        if not root.exists() or not root.is_dir():
            continue
        for p in root.rglob('*'):
            if not p.is_file():
                continue
            if p.name.startswith('~$'):
                continue
            if p.suffix.lower() in ('.xlsx', '.xls'):
                result.append(p)
    return result

def auto_detect_excel_roots() -> List[Path]:
    """Автоматическое определение корневых каталогов для поиска Excel-файлов"""
    candidates = [EXTRACT_DIR, DATA_DIR, DOWNLOAD_DIR]
    excels = list_excel_files(candidates)
    if not excels:
        return [EXTRACT_DIR]
    roots = sorted({p.parent for p in excels}, key=lambda x: str(x))
    return roots

def extract_rar(archive_path: Path) -> None:
    """Распаковка архива"""
    log = get_logger()
    invalidate_excel_index_cache()
    if EXTRACT_DIR.exists():
        shutil.rmtree(EXTRACT_DIR)
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    kind = detect_archive_kind(archive_path)
    if kind == 'zip':
        with zipfile.ZipFile(archive_path, 'r') as zf:
            zf.extractall(EXTRACT_DIR)
        return
    if kind == 'unknown':
        log.error('Файл не RAR/ZIP: %s', archive_path)
        raise RuntimeError(f'Скачанный файл не является архивом RAR/ZIP. Файл: {archive_path.name}, размер: {archive_path.stat().st_size} байт.')
    program_files = os.environ.get('ProgramFiles', 'C:\\Program Files')
    program_files_x86 = os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)')
    seven_zip_paths = [str(Path(program_files) / '7-Zip' / '7z.exe'), str(Path(program_files_x86) / '7-Zip' / '7z.exe')]
    winrar_paths = [str(Path(program_files) / 'WinRAR' / 'UnRAR.exe'), str(Path(program_files_x86) / 'WinRAR' / 'UnRAR.exe'), str(Path(program_files) / 'WinRAR' / 'WinRAR.exe'), str(Path(program_files_x86) / 'WinRAR' / 'WinRAR.exe')]
    candidates = []
    for exe in seven_zip_paths:
        candidates.append([exe, 'x', '-y', f'-o{EXTRACT_DIR}', str(archive_path)])
    candidates.append(['7z', 'x', '-y', f'-o{EXTRACT_DIR}', str(archive_path)])
    candidates.append(['unrar', 'x', '-o+', str(archive_path), str(EXTRACT_DIR)])
    for exe in winrar_paths:
        candidates.append([exe, 'x', '-o+', str(archive_path), str(EXTRACT_DIR)])
    last_error: Optional[str] = None
    for cmd in candidates:
        exe = cmd[0]
        if not shutil.which(exe) and (not Path(exe).exists()):
            continue
        try:
            run = _run_subprocess_hidden(cmd)
            if run.returncode == 0:
                return
            last_error = (run.stderr or run.stdout or 'Неизвестная ошибка распаковки').strip()
        except Exception as exc:
            last_error = str(exc)
    log.error('Распаковка архива не удалась: %s', last_error)
    raise RuntimeError(f"Не удалось распаковать архив .rar. Установите 7-Zip или WinRAR. Подробности: {last_error or 'команда распаковки не найдена'}")

def normalize_stem_for_code_match(stem: str) -> str:
    """Нормализация имени файла для сопоставления кодов"""
    s = stem
    for ch in ('–', '—', '−', '－'):
        s = s.replace(ch, '-')
    s = s.replace('\xa0', ' ')
    s = re.sub('\\s+', ' ', s.strip())
    return s.lower()

def _pick_best_excel(paths: List[Path]) -> Path:
    """Выбор лучшего Excel-файла из списка"""
    def sort_key(p: Path) -> Tuple[int, int, int, str]:
        ext_rank = 0 if p.suffix.lower() == '.xlsx' else 1
        dup_rank = 1 if '(1)' in p.name else 0
        return (ext_rank, dup_rank, len(p.name), p.name.lower())
    return sorted(paths, key=sort_key)[0]

def _group_code_sequence() -> Dict[str, List[str]]:
    """Группировка кодов по префиксу"""
    grouped: Dict[str, List[str]] = {}
    for item in MATERIAL_TYPES:
        prefix = item.code.split('-')[0]
        grouped.setdefault(prefix, []).append(item.code)
    for prefix in grouped:
        grouped[prefix] = sorted(grouped[prefix])
    return grouped

def _sort_by_leading_range(path: Path) -> Tuple[int, str]:
    """Сортировка файлов по префиксу кода"""
    norm = normalize_stem_for_code_match(path.stem)
    m = re.match('^(\\d+)', norm)
    lead = int(m.group(1)) if m else 10 ** 9
    return (lead, norm)

def build_fallback_index_by_order(files: List[Path]) -> Dict[str, Path]:
    """Построение индекса последовательности кодов"""
    grouped_codes = _group_code_sequence()
    grouped_files: Dict[str, List[Path]] = {}
    for path in files:
        rel_parts = path.parts
        folder_code = None
        for part in rel_parts:
            m = re.match('^(\\d{2})\\b', part.strip())
            if m:
                folder_code = m.group(1)
                break
        if folder_code is None:
            continue
        grouped_files.setdefault(folder_code, []).append(path)
    out: Dict[str, Path] = {}
    for folder_code, code_list in grouped_codes.items():
        files_for_group = grouped_files.get(folder_code, [])
        if not files_for_group:
            continue
        files_sorted = sorted(files_for_group, key=_sort_by_leading_range)
        limit = min(len(code_list), len(files_sorted))
        for idx in range(limit):
            out[code_list[idx]] = files_sorted[idx]
    return out

def build_excel_code_index() -> Dict[str, Path]:
    """Построение индекса Excel-файлов"""
    all_excels = list_excel_files(_excel_search_roots)
    buckets: Dict[str, List[Path]] = {}
    for path in all_excels:
        norm = normalize_stem_for_code_match(path.stem)
        m = re.match('^(\\d{2}-\\d{2})(?![0-9])', norm)
        if not m:
            continue
        code_key = m.group(1)
        buckets.setdefault(code_key, []).append(path)
    index = {c: _pick_best_excel(lst) for c, lst in buckets.items()}
    fallback = build_fallback_index_by_order(all_excels)
    for code, path in fallback.items():
        index.setdefault(code, path)
    return index

def get_excel_code_index() -> Dict[str, Path]:
    """Получение индекса Excel-файлов"""
    global _excel_code_index_cache
    mtime = 0.0
    for root in _excel_search_roots:
        try:
            mtime += root.stat().st_mtime
        except OSError:
            continue
    if _excel_code_index_cache is not None and _excel_code_index_cache[0] == mtime:
        return _excel_code_index_cache[1]
    built = build_excel_code_index()
    _excel_code_index_cache = (mtime, built)
    return built

def find_excel_by_code(code: str) -> Optional[Path]:
    """Поиск Excel-файла по коду"""
    canon = code.strip().lower()
    idx = get_excel_code_index()
    hit = idx.get(canon)
    if hit is not None:
        return hit
    patterns = [f'{canon}*.xlsx', f'{canon}*.xls']
    for pattern in patterns:
        for root in _excel_search_roots:
            if not root.exists() or not root.is_dir():
                continue
            for candidate in root.rglob(pattern):
                if candidate.name.startswith('~$'):
                    continue
                return candidate
    return None

def _python_module_available(python_exe: str, module_name: str) -> bool:
    """Проверка доступности Python-модуля"""
    probe = _run_subprocess_hidden([python_exe, '-c', f'import {module_name}'], timeout=30)
    return probe.returncode == 0

def _install_python_package_silent(python_exe: str, package_name: str) -> bool:
    """Установка Python-пакета без отображения окна"""
    cmd = [python_exe, '-m', 'pip', 'install', package_name, '-i', 'https://pypi.tuna.tsinghua.edu.cn/simple', '--timeout', '100']
    try:
        run = _run_subprocess_hidden(cmd, timeout=300)
        if run.returncode == 0:
            return _python_module_available(python_exe, package_name)
        return False
    except Exception:
        return False

def _build_dependency_notice(python_exe: str) -> Tuple[List[str], str]:
    """Построение уведомления о зависимостях"""
    missing: List[str] = []
    for mod in ('openpyxl', 'xlrd'):
        if not _python_module_available(python_exe, mod):
            missing.append(mod)
    if not missing:
        return (missing, '')
    cmd_lines_admin = [f'"{python_exe}" -m pip install {pkg} -i https://pypi.tuna.tsinghua.edu.cn/simple --timeout 100' for pkg in missing]
    text = tr('dep_notice', python_exe=python_exe, missing=', '.join(missing), commands='\n'.join(cmd_lines_admin))
    return (missing, text)

def _col_to_idx(ref: str) -> int:
    """Преобразование буквенного обозначения столбца в числовой индекс"""
    col = ''.join((ch for ch in ref or '' if ch.isalpha())).upper()
    if not col:
        return 0
    n = 0
    for ch in col:
        n = n * 26 + (ord(ch) - 64)
    return max(0, n - 1)

def _xlsx_rows_stdlib(path: Path, limit_rows: Optional[int]=None) -> List[List[str]]:
    """Чтение xlsx по физическим номерам строк (атрибут r у row), а не по порядку узлов в XML"""
    ns = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with zipfile.ZipFile(path, 'r') as zf:
        sst: List[str] = []
        if 'xl/sharedStrings.xml' in zf.namelist():
            root = ET.fromstring(zf.read('xl/sharedStrings.xml'))
            for si in root.findall('m:si', ns):
                parts = []
                for t in si.findall('.//m:t', ns):
                    parts.append(t.text or '')
                sst.append(''.join(parts))
        wb = ET.fromstring(zf.read('xl/workbook.xml'))
        rels = ET.fromstring(zf.read('xl/_rels/workbook.xml.rels'))
        rel_map: Dict[str, str] = {}
        for rel in rels.findall('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
            rel_map[rel.attrib.get('Id', '')] = rel.attrib.get('Target', '')
        first_sheet = wb.find('m:sheets/m:sheet', ns)
        rid = first_sheet.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id') if first_sheet is not None else None
        target = rel_map.get(rid or '', 'worksheets/sheet1.xml').lstrip('/').replace('\\', '/')
        sheet_path = 'xl/' + target if not target.startswith('xl/') else target
        root = ET.fromstring(zf.read(sheet_path))
        rows_map: Dict[int, List[str]] = {}
        for row in root.findall('.//m:sheetData/m:row', ns):
            r_attr = row.attrib.get('r')
            if r_attr is not None and str(r_attr).isdigit():
                ri = int(r_attr) - 1
            else:
                ri = max(rows_map.keys(), default=-1) + 1
            vals: Dict[int, str] = {}
            max_i = -1
            for c in row.findall('m:c', ns):
                i = _col_to_idx(c.attrib.get('r', ''))
                t = c.attrib.get('t', '')
                v = c.find('m:v', ns)
                if t == 'inlineStr':
                    ts = c.findall('.//m:t', ns)
                    val = ''.join((x.text or '' for x in ts))
                elif t == 's' and v is not None and (v.text is not None):
                    try:
                        val = sst[int(v.text)]
                    except Exception:
                        val = v.text or ''
                else:
                    val = v.text if v is not None and v.text is not None else ''
                vals[i] = str(val)
                if i > max_i:
                    max_i = i
            if max_i >= 0:
                rows_map[ri] = [vals.get(j, '') for j in range(max_i + 1)]
            else:
                rows_map[ri] = []
        if not rows_map:
            return []
        max_ri = max(rows_map.keys())
        if limit_rows is not None:
            n_out = min(max_ri + 1, int(limit_rows))
        else:
            n_out = max_ri + 1
        return [rows_map.get(i, [])[:] for i in range(n_out)]

def _read_table_rows(table_path: Path, limit_rows: Optional[int]=None) -> List[List[str]]:
    """Чтение строк из таблицы"""
    ext = table_path.suffix.lower()
    if ext == '.xlsx':
        return _xlsx_rows_stdlib(table_path, limit_rows=limit_rows)
    if ext == '.xls':
        try:
            import xlrd
        except Exception as exc:
            raise RuntimeError('Для чтения .xls требуется xlrd (запустите установку от имени администратора).') from exc
        wb = xlrd.open_workbook(str(table_path))
        sh = wb.sheet_by_index(0)
        rows: List[List[str]] = []
        for rr in range(sh.nrows):
            rows.append(['' if sh.cell_value(rr, c) is None else str(sh.cell_value(rr, c)) for c in range(sh.ncols)])
            if limit_rows is not None and len(rows) >= limit_rows:
                break
        return rows
    raise RuntimeError(f'Неподдерживаемый формат таблицы: {table_path.suffix}')

def _table_max_column_count(table_path: Path) -> int:
    """Максимальное количество столбцов в таблице"""
    try:
        rows = _read_table_rows(table_path, limit_rows=12)
        if not rows:
            return 1
        return max((len(r) for r in rows), default=1)
    except Exception:
        return 1

def _parse_quarter_index_from_text(text: str) -> Optional[int]:
    """Номер квартала 1..4 по подписи (I–IV квартал, 1–4 квартал, Q1)"""
    if not (text or '').strip():
        return None
    low = text.lower().replace('ё', 'е')
    m = re.search('\\bq([1-4])\\b', low)
    if m:
        return int(m.group(1))
    m = re.search('([1-4])\\s*[-−]?\\s*квартал', low)
    if m:
        return int(m.group(1))
    m = re.search('([1-4])\\s*[-−]?\\s*й\\s*квартал', low)
    if m:
        return int(m.group(1))
    if 'квартал' in low or 'кв.' in low or re.search('\\b[1-4]\\s*кв\\b', low):
        if re.search('\\biv\\b', low):
            return 4
        if re.search('\\biii\\b', low):
            return 3
        if re.search('\\bii\\b', low):
            return 2
        if re.search('\\bi\\b', low):
            return 1
    return None

def _month_index_from_ru_fragment(frag: str) -> Optional[int]:
    """Номер месяца 1..12 по фрагменту текста (подстрока названия месяца)"""
    low = (frag or '').lower().replace('ё', 'е')
    for needle, mo in _RU_MONTH_SUBSTRINGS:
        if needle in low:
            return mo
    return None

def _parse_ru_month_range_ordered(low: str) -> Optional[Tuple[int, int]]:
    """Диапазон месяцев в порядке «слева — начало, справа — конец» (январь-сентябрь, январь по март)"""
    s = (low or '').strip().lower().replace('ё', 'е')
    if not s:
        return None
    for delim in (' по ', ' — ', ' – ', ' - ', '/', '—', '–', '-'):
        if delim in s:
            left, right = s.split(delim, 1)
            ma = _month_index_from_ru_fragment(left)
            mb = _month_index_from_ru_fragment(right)
            if ma is not None and mb is not None:
                return (ma, mb)
    return None

def _parse_half_year_index_from_text(text: str) -> Optional[int]:
    """1 или 2 полугодие по подписи (I полугодие, 1 полугодие, второе полугодие, H2)"""
    if not (text or '').strip():
        return None
    low = text.lower().replace('ё', 'е')
    if 'полугод' not in low and 'half' not in low and not re.search('\\bh[12]\\b', low):
        return None
    if re.search('(ii|2\\s*[-−]?\\s*й?\\s*полугод|втор(ое|ого)\\s+полугод|полугод[иея]*\\s*2\\b)', low):
        return 2
    if re.search('(\\bi\\s*[-−]?\\s*полугод|1\\s*[-−]?\\s*й?\\s*полугод|перв(ое|ого)\\s+полугод|полугод[иея]*\\s*1\\b)', low):
        return 1
    m = re.search('полугод[иея]*\\s*[:\s]*([12])\\b', low)
    if m:
        return int(m.group(1))
    m = re.search('\\bh([12])\\b', low)
    if m:
        return int(m.group(1))
    return None

def _period_tuple_from_parts(year: int, month: int, quarter: Optional[int], month_from: int=0, half_year: Optional[int]=None) -> Tuple[int, int, Optional[int], int, Optional[int]]:
    """(year, month_for_stem, quarter, month_from, half_year); month_from>0 и month>0 задают диапазон месяцев"""
    if half_year is not None and 1 <= half_year <= 2:
        end_m = 6 if half_year == 1 else 12
        return (year, end_m, None, 0, half_year)
    if quarter is not None and 1 <= quarter <= 4:
        return (year, quarter * 3, quarter, 0, None)
    mf = max(0, min(12, int(month_from)))
    m = max(0, min(12, int(month)))
    if mf and m and mf != m:
        return (year, m, None, mf, None)
    return (year, m, None, 0, None)

def _guess_period_from_table(table_path: Path) -> Optional[ThematicPeriod]:
    """Предполагаемый период по имени таблицы или её содержимому"""
    blob = ''
    try:
        rows = _read_table_rows(table_path, limit_rows=12)
        for row in rows:
            blob += ' ' + ' '.join((str(c) for c in row))
    except Exception:
        pass
    blob += ' ' + table_path.stem
    blob_low = blob.lower().replace('ё', 'е')
    m = re.search('(20\\d{2})[./\\-](0?[1-9]|1[0-2])\\b', blob)
    if m:
        try:
            yy = int(m.group(1))
            mo = int(m.group(2))
            if 1990 <= yy <= 2100 and 1 <= mo <= 12:
                y, mo2, q, mf, hy = _period_tuple_from_parts(yy, mo, None)
                return ThematicPeriod(y, mo2, q, False, mf, hy)
        except Exception:
            pass
    q = _parse_quarter_index_from_text(blob_low)
    if q is not None:
        my = re.search('(20\\d{2})', blob)
        if my:
            yy = int(my.group(1))
            if 1990 <= yy <= 2100:
                y, mo2, qq, mf, hy = _period_tuple_from_parts(yy, 0, q)
                return ThematicPeriod(y, mo2, qq, False, mf, hy)
    h = _parse_half_year_index_from_text(blob_low)
    if h is not None:
        my = re.search('(20\\d{2})', blob)
        if my:
            yy = int(my.group(1))
            if 1990 <= yy <= 2100:
                y, mo2, qq, mf, hy = _period_tuple_from_parts(yy, 0, None, 0, h)
                return ThematicPeriod(y, mo2, qq, False, mf, hy)
    my = re.search('(20\\d{2})', blob)
    if my:
        try:
            yy = int(my.group(1))
            if 1990 <= yy <= 2100:
                rng = _parse_ru_month_range_ordered(blob_low)
                if rng:
                    ma, mb = rng
                    if ma != mb:
                        y, mo2, qq, mf, hy = _period_tuple_from_parts(yy, mb, None, ma, None)
                        return ThematicPeriod(y, mo2, qq, False, mf, hy)
        except Exception:
            pass
    m2 = re.search('\\b(20\\d{2})\\b', blob)
    if m2:
        try:
            yy = int(m2.group(1))
            if 1990 <= yy <= 2100:
                return ThematicPeriod(yy, 0, None, False)
        except Exception:
            pass
    return None

def _parse_period_from_header_text(text: str) -> Optional[Tuple[int, int, Optional[int], int, Optional[int]]]:
    """Период из строки заголовка: год + месяц, квартал, полугодие или диапазон месяцев"""
    s = (text or '').strip()
    if not s:
        return None
    low = s.lower().replace('ё', 'е')
    m = re.search('(20\\d{2})[./\\-](0?[1-9]|1[0-2])\\b', s)
    if m:
        try:
            yy, mo = int(m.group(1)), int(m.group(2))
            if 1990 <= yy <= 2100 and 1 <= mo <= 12:
                return _period_tuple_from_parts(yy, mo, None)
        except Exception:
            pass
    myy = re.search('(20\\d{2})', s)
    yy: Optional[int] = None
    if myy:
        try:
            yc = int(myy.group(1))
            if 1990 <= yc <= 2100:
                yy = yc
        except Exception:
            pass
    q = _parse_quarter_index_from_text(s)
    if yy is not None and q is not None:
        return _period_tuple_from_parts(yy, 0, q)
    if yy is not None:
        h = _parse_half_year_index_from_text(s)
        if h is not None:
            return _period_tuple_from_parts(yy, 0, None, 0, h)
        rng = _parse_ru_month_range_ordered(low)
        if rng:
            ma, mb = rng
            if ma != mb:
                return _period_tuple_from_parts(yy, mb, None, ma, None)
        mo_one = _month_index_from_ru_fragment(low)
        if mo_one is not None:
            return _period_tuple_from_parts(yy, mo_one, None)
    return None

def _forward_fill_row_for_merged_cells(row: List[str]) -> List[str]:
    """Пустые ячейки справа от объединённой в Excel — то же значение, что у крайней левой ячейки блока"""
    out: List[str] = []
    carry = ''
    for c in row:
        t = (str(c).strip() if c is not None else '')
        if t:
            carry = t
        out.append(carry)
    return out

def _parse_period_from_year_and_month_cells(year_cell: str, month_cell: str) -> Optional[Tuple[int, int, Optional[int], int, Optional[int]]]:
    """Год из строки 3, месяц, квартал, полугодие или диапазон из строки 4 (после протяжки объединений)"""
    combo = f'{year_cell} {month_cell}'.strip()
    if combo:
        p = _parse_period_from_header_text(combo)
        if p is not None:
            return p
    yy_m = re.search('(20\\d{2})', year_cell or '')
    if not yy_m:
        yy_m = re.search('(20\\d{2})', month_cell or '')
    if not yy_m:
        return None
    try:
        yy = int(yy_m.group(1))
    except Exception:
        return None
    if not (1990 <= yy <= 2100):
        return None
    q = _parse_quarter_index_from_text(month_cell or '')
    if q is not None:
        return _period_tuple_from_parts(yy, 0, q)
    h = _parse_half_year_index_from_text(month_cell or '')
    if h is not None:
        return _period_tuple_from_parts(yy, 0, None, 0, h)
    low = (month_cell or '').lower().replace('ё', 'е')
    rng = _parse_ru_month_range_ordered(low)
    if rng:
        ma, mb = rng
        if ma != mb:
            return _period_tuple_from_parts(yy, mb, None, ma, None)
    mo_one = _month_index_from_ru_fragment(low)
    if mo_one is not None:
        return _period_tuple_from_parts(yy, mo_one, None)
    dm = re.search('\\b(0?[1-9]|1[0-2])\\b', month_cell or '')
    if dm:
        mo = int(dm.group(1))
        if 1 <= mo <= 12:
            return _period_tuple_from_parts(yy, mo, None)
    return None

def _read_period_from_sheet_period_headers(table_path: Path, value_col: int) -> Optional[ThematicPeriod]:
    """Строка 3 — год (часто с объединением), строка 4 — месяц или квартал; value_col — 1-based"""
    try:
        rows = _read_table_rows(table_path, limit_rows=4)
    except Exception:
        return None
    if len(rows) < 4:
        return None
    vi = max(0, int(value_col) - 1)
    yrow = _forward_fill_row_for_merged_cells([str(x) for x in rows[2]])
    mrow = _forward_fill_row_for_merged_cells([str(x) for x in rows[3]])
    if vi >= len(yrow) or vi >= len(mrow):
        return None
    ys = yrow[vi].strip()
    ms = mrow[vi].strip()
    t = _parse_period_from_year_and_month_cells(ys, ms)
    if t is None:
        return None
    y, m, q, mf, hy = t
    return ThematicPeriod(y, m, q, True, mf, hy)

def _thematic_period_for_map_name(table_path: Path, value_col: int) -> ThematicPeriod:
    """Период для имени карты и UI: шапка строк 3–4, затем заголовок столбца, затем эвристика по тексту (без месяца из даты портала)"""
    p = _read_period_from_sheet_period_headers(table_path, value_col)
    if p is not None:
        return p
    try:
        _, vh = _table_header_row_for_thematic(table_path, value_col)
    except Exception:
        vh = ''
    parsed = _parse_period_from_header_text(vh)
    if parsed is not None:
        y, m, q, mf, hy = parsed
        return ThematicPeriod(y, m, q, True, mf, hy)
    g = _guess_period_from_table(table_path)
    if g is not None:
        return g
    return ThematicPeriod(date.today().year, 0, None, False)

def _short_material_slug(display_name: str) -> str:
    """Краткое название материала: первое слово или первая часть до запятой или точки"""
    part = re.split('[,;]', display_name, maxsplit=1)[0].strip()
    part = part.replace('«', ' ').replace('»', ' ').replace('"', ' ')
    part = re.sub('\\s+', ' ', part).lower()
    if 'индекс промышленного производства' in part:
        part = part.replace('индекс промышленного производства', 'индекс промышленности')
    return part[:80]

def _sanitize_windows_filename_stem(stem: str) -> str:
    """Очистка имени файла от недопустимых символов"""
    s = stem
    for c in '<>:"/\\|?*\x00':
        s = s.replace(c, '_')
    s = s.strip(' .')
    return s or 'rosstat'

def build_thematic_output_stem(report_code: str, material_display_name: str, value_col_one_based: int, table_path: Path) -> str:
    """Построение имени файла для выходной карты: код отчёта + краткое название материала + период"""
    per = _thematic_period_for_map_name(table_path, value_col_one_based)
    slug = _short_material_slug(material_display_name)
    mm = per.stem_month_part()
    raw = f'{report_code} {slug}.{per.year:04d}.{mm:02d}'
    return _sanitize_windows_filename_stem(raw)

def resolve_python_executable() -> str:
    """Поиск исполняемого файла Python среди системных и локальных установок"""
    candidates: List[Path] = []
    if sys.executable:
        candidates.append(Path(sys.executable))
    if getattr(sys, 'base_prefix', None):
        candidates.append(Path(sys.base_prefix) / 'python.exe')
    if getattr(sys, 'exec_prefix', None):
        candidates.append(Path(sys.exec_prefix) / 'python.exe')
    local_app = Path.home() / 'AppData' / 'Local' / 'Programs' / 'Python'
    if local_app.exists():
        for pydir in sorted(local_app.glob('Python*'), reverse=True):
            candidates.append(pydir / 'python.exe')
    for name in ('python',):
        found = shutil.which(name)
        if found:
            candidates.append(Path(found))
    seen = set()
    for c in candidates:
        c = c.resolve()
        key = str(c).lower()
        if key in seen:
            continue
        seen.add(key)
        if not c.exists():
            continue
        low_name = c.name.lower()
        if 'mapscena' in low_name or 'panorama' in low_name or low_name.endswith('.dll'):
            continue
        return str(c)
    raise RuntimeError('Не найден python.exe.')

def table_path_for_material(display_name: str) -> Path:
    """Поиск таблицы материала по имени из файла thematic.xml"""
    code = DISPLAY_TO_CODE[display_name]
    p = find_excel_by_code(code)
    if p is None:
        return EXTRACT_DIR / f'{code}.xlsx'
    return p
THEMATIC_XML_DEFAULT = os.environ.get('gisthematicxml', 'C:\\Program Files\\Panorama\\Panorama15\\thematic.xml')
RU_REGIONS_SITZ = 'ru_regions.sitz'
THEMATIC_CONNECT_COLUMN = max(1, int(os.environ.get('ROSSTAT2MAP_THEMATIC_CONNECT_COLUMN', '1'), 0))
THEMATIC_DATA_FIRST_ROW_INDEX = 4

def _table_row_has_no_cell_data(row: List[Any]) -> bool:
    """Проверка строки таблицы на наличие данных: нет ни одной непустой ячейки"""
    if not row:
        return True
    return not any((str(c).strip() for c in row))

def _analyze_pre_body_empty_rows(table_path: Path, body_start: int=THEMATIC_DATA_FIRST_ROW_INDEX) -> Tuple[int, List[int]]:
    """(число пустых строк, их индексы 0..) среди строк шапки с индексами 0..body_start-1"""
    if not table_path.is_file():
        return (0, [])
    try:
        rows = _read_table_rows(table_path, limit_rows=max(0, int(body_start)))
    except Exception:
        return (0, [])
    idxs: List[int] = []
    cap = min(int(body_start), len(rows))
    for i in range(cap):
        if _table_row_has_no_cell_data(rows[i]):
            idxs.append(i)
    return (len(idxs), idxs)

def _default_thematic_region_title_object_keys(preferred_sample: Optional[Path]=None, *, actual_value_count: Optional[int]=None, reference_subject_count: Optional[int]=None) -> Set[int]:
    """Диапазон ключей подписей регионов: база (по умолчанию 171) минус пустые строки шапки, плюс START_OFFSET"""
    base = max(1, int(os.environ.get('ROSSTAT2MAP_THEMATIC_TITLE_KEY_BASE', '171'), 0))
    start_off = int(os.environ.get('ROSSTAT2MAP_THEMATIC_TITLE_KEY_START_OFFSET', '0'), 0)
    auto_shift = int(os.environ.get('ROSSTAT2MAP_THEMATIC_TITLE_KEY_AUTO_SHIFT', '1'), 0) != 0
    _pair_raw = (os.environ.get('ROSSTAT2MAP_THEMATIC_TITLE_KEY_AUTO_PAIR_FACTOR') or '2').strip()
    try:
        pair_factor = max(1, int(_pair_raw, 0))
    except ValueError:
        pair_factor = 2
    end_excl = max(base + 1, int(os.environ.get('ROSSTAT2MAP_THEMATIC_TITLE_KEY_END', '256'), 0))
    sample: Optional[Path] = None
    if preferred_sample is not None and preferred_sample.is_file():
        sample = preferred_sample
    else:
        for item in MATERIAL_TYPES:
            p = table_path_for_material(item.name)
            if p.is_file():
                sample = p
                break
    bs = int(THEMATIC_DATA_FIRST_ROW_INDEX)
    delta_counts = 0
    raw_delta = 0
    if auto_shift and actual_value_count is not None and reference_subject_count is not None:
        ref_n = int(reference_subject_count)
        act_n = int(actual_value_count)
        if ref_n > 0:
            raw_delta = act_n - ref_n
            delta_counts = pair_factor * raw_delta
    if sample is not None:
        empty_hdr, empty_idx = _analyze_pre_body_empty_rows(sample, bs)
        start = max(1, base - empty_hdr + start_off + delta_counts)
    else:
        empty_hdr, empty_idx = (0, [])
        start = max(1, base + start_off + delta_counts)
    keys = set(range(start, end_excl))
    kmin = min(keys) if keys else 0
    kmax = max(keys) if keys else 0
    det = (f'файл={sample}; строка_данных_с_индекса={bs}; пустые_строки_шапки={empty_hdr} (индексы {empty_idx}); '
           f'база={base}; start_offset={start_off}; auto_shift_по_числу_значений={auto_shift}; '
           f'множитель_пара_площадь_подпись={pair_factor}; эталон_субъектов={reference_subject_count!s}; с_значениями={actual_value_count!s}; '
           f'разница_значений={raw_delta}; delta_start={delta_counts}; start={start}; конец_range_не_вкл={end_excl}; ключей={len(keys)}; min={kmin} max={kmax}')
    _log_thematic_title_keys_diag('rosstat2map: THEMATIC_REGION_TITLE_OBJECT_KEYS', det)
    return keys

LEGEND_TEXT_X = 10383971.29
LEGEND_TEXT_Y = 3556220.1
LEGEND_TEXT_LAYER_NAME = 'Названия и подписи'
LABEL_VISIBILITY_TOP_SCALE = max(1, int(os.environ.get('ROSSTAT2MAP_LABEL_TOP_SCALE', '1'), 0))
LABEL_VISIBILITY_BOT_SCALE = max(1, min(40000000, int(os.environ.get('ROSSTAT2MAP_LABEL_BOT_SCALE', str(40000000)), 0)))
GRAPHIC_CLASSIFIER_LAYER = int(os.environ.get('ROSSTAT2MAP_GRAPHIC_CLASSIFIER_LAYER', '0'))
_leg_cap_key_env = os.environ.get('ROSSTAT2MAP_LEGEND_CAPTION_KEY')
LEGEND_CAPTION_OBJECT_KEY = 'ПОДПИСЬ' if _leg_cap_key_env is None else str(_leg_cap_key_env).strip()
LEGEND_CAPTION_OBJECT_EXCODE = int(os.environ.get('ROSSTAT2MAP_LEGEND_CAPTION_EXCODE', '0'), 0)
LEGEND_CAPTION_TRUETYPE_NAME = (os.environ.get('ROSSTAT2MAP_LEGEND_FONT_NAME', 'Tahoma') or 'Tahoma').strip()
LEGEND_CAPTION_IMG_TRUETEXT = int(os.environ.get('ROSSTAT2MAP_IMG_TRUETEXT', '143'), 0)
LEGEND_CAPTION_TEXT_COLOR_BGR = int(os.environ.get('ROSSTAT2MAP_LEGEND_TEXT_COLOR_BGR', '0'), 0)
LEGEND_CAPTION_TEXT_HEIGHT_MKM = int(os.environ.get('ROSSTAT2MAP_LEGEND_TEXT_HEIGHT_MKM', '50000'))
LEGEND_CAPTION_TEXT_INTERVAL_PCT = max(0, min(255, int(os.environ.get('ROSSTAT2MAP_LEGEND_TEXT_INTERVAL', '100'))))
LEGEND_CAPTION_FONT_WEIGHT = int(os.environ.get('ROSSTAT2MAP_LEGEND_FONT_WEIGHT', '500'))
LEGEND_CAPTION_FONT_HORIZONTAL = int(os.environ.get('ROSSTAT2MAP_LEGEND_FONT_HORIZONTAL', '1'))
LEGEND_CAPTION_FONT_TYPE = int(os.environ.get('ROSSTAT2MAP_LEGEND_FONT_TYPE', '0'))
LEGEND_CAPTION_FONT_NUMBER = int(os.environ.get('ROSSTAT2MAP_LEGEND_FONT_NUMBER', '0'))
LEGEND_CAPTION_TEXT_CHARSET = int(os.environ.get('ROSSTAT2MAP_LEGEND_TEXT_CHARSET', '204'))
LEGEND_CAPTION_FA_LEFT = int(os.environ.get('ROSSTAT2MAP_LEGEND_FA_LEFT', '0'))
LEGEND_CAPTION_FA_BOTTOM = int(os.environ.get('ROSSTAT2MAP_LEGEND_FA_BOTTOM', '8'))
LEGEND_CAPTION_IMGTEXT_ALIGN = int(os.environ.get('ROSSTAT2MAP_LEGEND_IMGTEXT_ALIGN', '8'))
IMGC_TRANSPARENT = 4294967295
_LEG_BKGND_RAW = (os.environ.get('ROSSTAT2MAP_LEGEND_BKGND') or '').strip()
_LEG_BKGND_BGR_LEGACY = (os.environ.get('ROSSTAT2MAP_LEGEND_BKGND_BGR') or '').strip()
if _LEG_BKGND_RAW:
    LEGEND_CAPTION_BKGND_COLOR = int(_LEG_BKGND_RAW, 0) & 4294967295
elif _LEG_BKGND_BGR_LEGACY:
    LEGEND_CAPTION_BKGND_COLOR = int(_LEG_BKGND_BGR_LEGACY, 0) & 16777215
else:
    LEGEND_CAPTION_BKGND_COLOR = IMGC_TRANSPARENT
LEGEND_CAPTION_SHADOW_COLOR = int(os.environ.get('ROSSTAT2MAP_LEGEND_SHADOW', str(IMGC_TRANSPARENT)), 0) & 4294967295
LEGEND_CAPTION_OUTLINE = int(os.environ.get('ROSSTAT2MAP_LEGEND_OUTLINE', '0'), 0) & 255
LEGEND_CAPTION_TEXT_SERVICE = int(os.environ.get('ROSSTAT2MAP_LEGEND_TEXT_SERVICE', '0'), 0)
LEGEND_CAPTION_TEXT_FLAG = int(os.environ.get('ROSSTAT2MAP_LEGEND_TEXT_FLAG', '0'), 0)
_LEGEND_TT_IDS_RAW = (os.environ.get('ROSSTAT2MAP_LEGEND_TRUETEXT_IDS') or '').strip()
LEGEND_CAPTION_TRUETEXT_FALLBACK_IDS: Tuple[int, ...] = tuple((int(x.strip(), 0) for x in _LEGEND_TT_IDS_RAW.split(',') if x.strip()))
if not LEGEND_CAPTION_TRUETEXT_FALLBACK_IDS:
    LEGEND_CAPTION_TRUETEXT_FALLBACK_IDS = (143, 142, 141, 144, 145, 140, 146)
LEGEND_CAPTION_ALLOW_IMG_TEXT_FALLBACK = int(os.environ.get('ROSSTAT2MAP_LEGEND_IMG_TEXT_FALLBACK', '1'), 0)
LEGEND_CAPTION_IMGTEXT_TYPE = int(os.environ.get('ROSSTAT2MAP_LEGEND_IMGTEXT_TYPE', '1'), 0) & 255
LEGEND_CAPTION_IMGTEXT_TYPE_TRUETEXT = int(os.environ.get('ROSSTAT2MAP_LEGEND_IMGTEXT_TYPE_TRUETEXT', '0'), 0) & 255
MAP_PUT_TEXT_DRAW_TYPE = int(os.environ.get('ROSSTAT2MAP_MAP_PUT_TEXT_DRAW_TYPE', '1'), 0)
THEMATIC_RANGEITEM_TYPE = int(os.environ.get('ROSSTAT2MAP_RANGEITEM_TYPE', '1'), 0)
THEMATIC_TITLE_ALIGN_ENABLE = int(os.environ.get('ROSSTAT2MAP_THEMATIC_TITLE_ALIGN_ENABLE', '1'), 0)
_THEMATIC_TITLE_KEYS_RAW = (os.environ.get('ROSSTAT2MAP_THEMATIC_TITLE_OBJECT_KEYS') or '').strip()
THEMATIC_REGION_TITLE_OBJECT_KEYS: Set[int] = {int(x.strip(), 0) for x in _THEMATIC_TITLE_KEYS_RAW.split(',') if x.strip()}
if not THEMATIC_REGION_TITLE_OBJECT_KEYS:
    THEMATIC_REGION_TITLE_OBJECT_KEYS = _default_thematic_region_title_object_keys()

def _refresh_thematic_region_title_keys_if_default(sample_table: Optional[Path]=None, *, actual_value_count: Optional[int]=None, reference_subject_count: Optional[int]=None) -> None:
    """Пересчитать ключи по умолчанию (если не задан ROSSTAT2MAP_THEMATIC_TITLE_OBJECT_KEYS), например после появления таблиц в кэше"""
    global THEMATIC_REGION_TITLE_OBJECT_KEYS
    if (_THEMATIC_TITLE_KEYS_RAW or '').strip():
        _log_thematic_title_keys_diag('rosstat2map: THEMATIC_REGION_TITLE_OBJECT_KEYS', 'пересчёт пропущен: задан ROSSTAT2MAP_THEMATIC_TITLE_OBJECT_KEYS')
        return
    THEMATIC_REGION_TITLE_OBJECT_KEYS = _default_thematic_region_title_object_keys(sample_table, actual_value_count=actual_value_count, reference_subject_count=reference_subject_count)

def _log_thematic_title_keys_session_summary(table_abs: Path, *, actual_value_count: Optional[int]=None, reference_subject_count: Optional[int]=None) -> None:
    """Краткая строка в журнал диагностики при построении тематики (когда mapIsDiagnostics уже активен)"""
    if table_abs.is_file():
        empty_hdr, empty_idx = _analyze_pre_body_empty_rows(table_abs)
    else:
        empty_hdr, empty_idx = (0, [])
    ks = THEMATIC_REGION_TITLE_OBJECT_KEYS
    env_explicit = bool((_THEMATIC_TITLE_KEYS_RAW or '').strip())
    extra = ''
    if actual_value_count is not None or reference_subject_count is not None:
        extra = f'; сопоставлено_значений={actual_value_count!s}; эталон_субъектов={reference_subject_count!s}'
    if not ks:
        _log_thematic_title_keys_diag('rosstat2map: итог ключей перед align/сдвигом', f'таблица={table_abs}; набор ключей пуст; явный список в ENV={"да" if env_explicit else "нет"}{extra}')
        return
    kmin, kmax = (min(ks), max(ks))
    det = (f'таблица={table_abs}; пустые строки шапки={empty_hdr} (индексы {empty_idx}); '
           f'ключей={len(ks)}; min={kmin} max={kmax}; явный список в ENV={"да" if env_explicit else "нет"}{extra}')
    _log_thematic_title_keys_diag('rosstat2map: итог ключей перед align/сдвигом', det)

if 'ROSSTAT2MAP_THEMATIC_TITLE_ALIGN_SUBJECT' in os.environ:
    THEMATIC_TITLE_ALIGN_SUBJECTS: Tuple[int, ...] = (int(os.environ['ROSSTAT2MAP_THEMATIC_TITLE_ALIGN_SUBJECT'], 0),)
else:
    _tss = (os.environ.get('ROSSTAT2MAP_THEMATIC_TITLE_ALIGN_SUBJECTS') or '-1,0').strip()
    THEMATIC_TITLE_ALIGN_SUBJECTS = tuple((int(x.strip(), 0) for x in _tss.split(',') if x.strip())) or (-1, 0)
SUBJECT_LABEL_OFFSET_EAST_M = float(os.environ.get('ROSSTAT2MAP_SUBJECT_LABEL_OFFSET_EAST_M', '600000'))
_SUBJECT_OFF_EXTRA_RAW = (os.environ.get('ROSSTAT2MAP_SUBJECT_LABEL_OFFSET_EXTRA_KEYS') or '').strip()
SUBJECT_LABEL_OFFSET_EXTRA_KEYS: Set[int] = {int(x.strip(), 0) for x in _SUBJECT_OFF_EXTRA_RAW.split(',') if x.strip()}
_SL_METRIC_SUBJ_RAW = (os.environ.get('ROSSTAT2MAP_SUBJECT_LABEL_METRIC_SUBJECTS') or '0,-1,1').strip()
SUBJECT_LABEL_METRIC_SUBJECTS: Tuple[int, ...] = tuple((int(x.strip(), 0) for x in _SL_METRIC_SUBJ_RAW.split(',') if x.strip())) or (0, -1, 1)
GRADATION_RECT_LAYER_NAME = 'Системный'
GRADATION_RECT_WIDTH_M = 100000.0
GRADATION_RECT_HEIGHT_M = 400000.0
GRADATION_RECT_ORIGIN_X = 10196014.23
GRADATION_RECT_ORIGIN_Y = 3515957.21
GRADATION_RECT_STEP_X = 150000.0
GRADATION_RECT_OBJECT_KEY = (os.environ.get('ROSSTAT2MAP_GRAD_RECT_KEY', '') or '').strip()
GRADATION_RECT_OBJECT_EXCODE = int(os.environ.get('ROSSTAT2MAP_GRAD_RECT_EXCODE', '0'))
GRADATION_RECT_OBJECT_INCODE = int(os.environ.get('ROSSTAT2MAP_GRAD_RECT_INCODE', '0'))
GRADATION_GLASS_BRIGHTNESS = 20
GRADATION_GLASS_CONTRAST = 50
GRADATION_GLASS_TRANSPARENCY = 80
GRADATION_POLYGON_GLASS_IMAGE = int(os.environ.get('ROSSTAT2MAP_POLYGON_GLASS_IMG', '0'))
GRADATION_RANGE_TEXT_HEIGHT_MKM = int(os.environ.get('ROSSTAT2MAP_GRAD_RANGE_TEXT_HEIGHT_MKM', '25000'))
GRADATION_RANGE_TEXT_COLOR_BGR = int(os.environ.get('ROSSTAT2MAP_GRAD_RANGE_TEXT_BGR', '0'), 0) & 16777215
GRADATION_RANGE_TEXT_FA_H = int(os.environ.get('ROSSTAT2MAP_GRAD_RANGE_FA_H', '6'))
GRADATION_RANGE_TEXT_FA_V = int(os.environ.get('ROSSTAT2MAP_GRAD_RANGE_FA_V', '4120'))
GRADATION_RANGE_IMGTEXT_ALIGN = int(os.environ.get('ROSSTAT2MAP_GRAD_RANGE_IMGTEXT_ALIGN', '4126'))
GRADATION_RANGE_TEXT_OUTLINE = int(os.environ.get('ROSSTAT2MAP_GRAD_RANGE_TEXT_OUTLINE', '3'), 0) & 255
GRADATION_RANGE_TEXT_OUTLINE_BGR = int(os.environ.get('ROSSTAT2MAP_GRAD_RANGE_TEXT_OUTLINE_BGR', str(16777215)), 0) & 16777215
GRADATION_RANGE_FONT_NAME = ((os.environ.get('ROSSTAT2MAP_GRAD_RANGE_FONT_NAME') or '').strip() or LEGEND_CAPTION_TRUETYPE_NAME)
GRADATION_RANGE_REGISTER_LEGEND_CLASSIFIER = int(os.environ.get('ROSSTAT2MAP_GRAD_RANGE_REGISTER_LEGEND_CLASSIFIER', '0'), 0)

def resolve_ru_regions_sitz_path() -> Path:
    """Поиск карты регионов РФ по имени из файла thematic.xml"""
    xml_path = Path(THEMATIC_XML_DEFAULT)
    if not xml_path.is_file():
        raise RuntimeError(f'Не найден файл настроек тематики: {xml_path}')
    tree = ET.parse(xml_path)
    troot = tree.getroot()
    total_el = troot.find('total')
    if total_el is None or not total_el.get('dir'):
        raise RuntimeError('В thematic.xml отсутствует элемент <total dir="..."/>')
    thematic_dir = Path(total_el.get('dir', '').strip())
    found = False
    for reg in troot.findall('region'):
        if reg.get('file') == RU_REGIONS_SITZ:
            found = True
            break
    if not found:
        raise RuntimeError(f'В thematic.xml нет <region file="{RU_REGIONS_SITZ}" .../>')
    sitz = (thematic_dir / RU_REGIONS_SITZ).resolve()
    if not sitz.is_file():
        raise RuntimeError(f'Не найдена карта регионов РФ для тематики: {sitz}')
    return sitz

def resolve_ru_regions_subject_key() -> str:
    """Поиск ключа субъекта по имени из файла thematic.xml"""
    xml_path = Path(THEMATIC_XML_DEFAULT)
    if not xml_path.is_file():
        raise RuntimeError(f'Не найден файл настроек тематики: {xml_path}')
    tree = ET.parse(xml_path)
    troot = tree.getroot()
    for reg in troot.findall('region'):
        if reg.get('file') == RU_REGIONS_SITZ:
            key = (reg.get('key') or '').strip()
            if not key:
                raise RuntimeError(f'В thematic.xml у region file="{RU_REGIONS_SITZ}" отсутствует атрибут key')
            return key
    raise RuntimeError(f'В thematic.xml нет <region file="{RU_REGIONS_SITZ}" .../>')

def resolve_ru_regions_name_sem_code() -> int:
    """Поиск кода семантического имени субъекта по имени из файла thematic.xml"""
    xml_path = Path(THEMATIC_XML_DEFAULT)
    if not xml_path.is_file():
        return 0
    try:
        tree = ET.parse(xml_path)
        troot = tree.getroot()
        for reg in troot.findall('region'):
            if reg.get('file') != RU_REGIONS_SITZ:
                continue
            raw = (reg.get('namesem') or '').strip()
            if not raw:
                return 0
            return int(raw)
    except Exception:
        return 0

def _hmap_as_int(hmap) -> int:
    """Преобразование указателя на карту в целое число (код карты)"""
    try:
        return int(ctypes.cast(hmap, ctypes.c_void_p).value or 0)
    except Exception:
        return 0

def _table_a1_a2_cells(table_abs: Path) -> Tuple[str, str]:
    """Первая и вторая ячейки столбца A (название показателя и единицы/пояснение) из таблицы"""
    try:
        rows = _read_table_rows(table_abs, limit_rows=2)
        a1 = (rows[0][0] if len(rows) > 0 and len(rows[0]) > 0 else '').strip()
        a1 = re.sub('\\s*[-+]?\\d+(?:[.,]\\d+)?\\s*$', '', a1).strip()
        a2 = (rows[1][0] if len(rows) > 1 and len(rows[1]) > 0 else '').strip()
        return (a1, a2)
    except Exception:
        return ('', '')

def _table_a1_a2_text(table_abs: Path) -> str:
    """Получение текста из таблицы для заголовка Легенды: A1 + A2"""
    a1, a2 = _table_a1_a2_cells(table_abs)
    return f'{a1} {a2}'.strip()

def _caption_first_upper_rest_lower(text: str) -> str:
    """Преобразование текста в заголовок Легенды: первая буква заглавная, остальные строчные"""
    s = (text or '').strip()
    if not s:
        return ''
    return s[:1].upper() + s[1:].lower()

def _preview_headline_name(selected_material_name: str, table_abs: Path) -> str:
    """Заголовок предпросмотра: выбранный тип + только строка единиц (A2), без повтора A1 и без « — » из таблицы"""
    sn = (selected_material_name or '').strip()
    if not table_abs.is_file():
        return _caption_first_upper_rest_lower(sn)
    _, a2 = _table_a1_a2_cells(table_abs)
    raw = f'{sn} {a2}'.strip() if a2 else sn
    return _caption_first_upper_rest_lower(raw)

def _format_value_range_label_int(vmin: float, vmax: float) -> str:
    """Форматирование текста для заголовка Легенды: диапазон значений в виде «123456-789012»"""
    return f'{int(round(float(vmin)))}-{int(round(float(vmax)))}'

def _try_map_put_text_draw_type(info, log, log_tag: str) -> None:
    """Установка типа текста для заголовка Легенды"""
    if mapapi is None or int(MAP_PUT_TEXT_DRAW_TYPE) < 0:
        return
    fn = getattr(mapapi, 'mapPutTextDrawType', None)
    if not callable(fn):
        return
    try:
        v = int(MAP_PUT_TEXT_DRAW_TYPE)
        int(fn(info, v) or 0)
    except Exception:
        pass

def _fa_vertical_middle_value() -> int:
    """Значение вертикального выравнивания для Легенды"""
    try:
        if mapgdi is not None:
            m = getattr(mapgdi, 'FA_MIDDLE', None)
            if isinstance(m, int):
                return int(m)
    except Exception:
        pass
    return int(os.environ.get('ROSSTAT2MAP_THEMATIC_TITLE_FA_MIDDLE', os.environ.get('ROSSTAT2MAP_FA_MIDDLE_FALLBACK', '4120')), 0)

def _apply_vertical_align_to_thematic_title_objects(hmap_doc, log, seekapi, sitapi, object_keys: Set[int], *, fa_vertical: int, subjects: Tuple[int, ...]) -> int:
    """Применение вертикального выравнивания к объектам Легенды"""
    if mapapi is None or maptype is None:
        return 0
    if not object_keys or not subjects:
        return 0
    put_v = getattr(mapapi, 'mapPutTextVerticalAlign', None)
    read_by_num = getattr(seekapi, 'mapReadObjectByNumberEx', None)
    if not callable(put_v):
        return 0
    if not callable(read_by_num):
        return 0
    get_v = getattr(mapapi, 'mapGetTextVerticalAlign', None)
    seek_info = mapapi.mapCreateObject(hmap_doc, 1, maptype.IDDOUBLE2, 0)
    if not seek_info:
        return 0
    targets: List[Tuple[int, int, int]] = []
    seen_lo: Set[Tuple[int, int]] = set()
    updated = 0
    try:
        try:
            main_site = sitapi.mapGetSiteIdent(hmap_doc, 0)
        except Exception:
            main_site = 0
        flag = maptype.WO_FIRST
        while seekapi.mapTotalSeekObject(hmap_doc, seek_info, flag):
            flag = maptype.WO_NEXT
            try:
                if sitapi.mapGetObjectSiteIdent(hmap_doc, seek_info) != main_site:
                    continue
            except Exception:
                pass
            try:
                key = int(mapapi.mapObjectKey(seek_info) or 0)
            except Exception:
                continue
            if key not in object_keys:
                continue
            list_no = int(mapapi.mapGetListNumber(seek_info) or 1)
            obj_no = int(mapapi.mapGetObjectNumber(seek_info) or 0)
            if obj_no <= 0:
                continue
            sig = (list_no, obj_no)
            if sig in seen_lo:
                continue
            seen_lo.add(sig)
            targets.append((list_no, obj_no, key))
    finally:
        try:
            mapapi.mapFreeObject(seek_info)
        except Exception:
            pass
    site_try: List[int] = []
    try:
        s0 = int(sitapi.mapGetSiteIdent(hmap_doc, 0) or 0)
        if s0 != 0:
            site_try.append(s0)
    except Exception:
        pass
    site_try.append(0)
    for list_no, obj_no, key in targets:
        ed = None
        try:
            ed = mapapi.mapCreateObject(hmap_doc, 1, maptype.IDDOUBLE2, 0)
            if not ed:
                continue
            loaded = False
            for hsite in site_try:
                try:
                    ro = read_by_num(hmap_doc, hsite, ed, int(list_no), int(obj_no))
                    if ro == 2:
                        loaded = True
                        break
                except Exception:
                    continue
            if not loaded:
                continue
            last_rv = 0
            for subj in subjects:
                try:
                    last_rv = int(put_v(ed, int(fa_vertical), int(subj)) or 0)
                except Exception:
                    pass
            gv = None
            if callable(get_v):
                try:
                    gv = int(get_v(ed, int(subjects[-1])) or 0)
                except Exception:
                    gv = None
            rc = int(mapapi.mapCommitObject(ed) or 0)
            if rc <= 0:
                rc2 = int(mapapi.mapCommitObjectAsNew(ed) or 0)
                if rc2 > 0:
                    rc = rc2
            if rc > 0:
                updated += 1
        except Exception:
            pass
        finally:
            if ed:
                try:
                    mapapi.mapFreeObject(ed)
                except Exception:
                    pass
    return updated

def _shift_metric_points_east_for_subject(ed, delta_east_m: float, subj: int) -> bool:
    """Сдвиг точек метрики одного субъекта на восток (+ к Y в таблице «Восток»)"""
    n = int(mapapi.mapPointCount(ed, subj) or 0)
    if n <= 0:
        return False
    gmp = getattr(mapapi, 'mapGetMapPlanePoint', None)
    ump = getattr(mapapi, 'mapUpdateMapPointPlane', None)
    gpp = getattr(mapapi, 'mapGetPlanePoint', None)
    upp = getattr(mapapi, 'mapUpdatePointPlane', None)
    up_inmap = getattr(mapapi, 'mapUpdatePointPlaneInMap', None)
    ok_any = False
    for num in range(1, n + 1):
        pt = maptype.DOUBLEPOINT()
        if callable(gmp) and int(gmp(ed, ctypes.byref(pt), num, subj) or 0) > 0:
            nx, ny = float(pt.X), float(pt.Y) + delta_east_m
            if callable(ump) and int(ump(ed, nx, ny, num, subj) or 0) > 0:
                ok_any = True
                continue
        pt = maptype.DOUBLEPOINT()
        if callable(gpp) and int(gpp(ed, ctypes.byref(pt), num, subj) or 0) > 0:
            nx, ny = float(pt.X), float(pt.Y) + delta_east_m
            if callable(up_inmap) and int(up_inmap(ed, nx, ny, num, subj) or 0) > 0:
                ok_any = True
                continue
            if callable(upp) and int(upp(ed, nx, ny, num, subj) or 0) > 0:
                ok_any = True
                continue
    return ok_any


def _shift_metric_points_east(ed, delta_east_m: float) -> bool:
    """Сдвиг точек метрики на восток: перебор субъектов (у подписей часто не 0)"""
    ok_any = False
    for subj in SUBJECT_LABEL_METRIC_SUBJECTS:
        if _shift_metric_points_east_for_subject(ed, delta_east_m, int(subj)):
            ok_any = True
    return ok_any

def _offset_subject_labels_east_m(hmap_doc, seekapi, sitapi, object_keys: Set[int], delta_east_m: float) -> int:
    """Сдвиг подписей субъектов по восточной координате (в таблице метрики — столбец Y «Восток»)"""
    if mapapi is None or maptype is None:
        return 0
    if not object_keys or abs(delta_east_m) < 1e-09:
        return 0
    read_by_num = getattr(seekapi, 'mapReadObjectByNumberEx', None)
    pc = getattr(mapapi, 'mapPointCount', None)
    if not all((callable(read_by_num), callable(pc))):
        return 0
    seek_info = mapapi.mapCreateObject(hmap_doc, 1, maptype.IDDOUBLE2, 0)
    if not seek_info:
        return 0
    targets: List[Tuple[int, int, int]] = []
    seen_lo: Set[Tuple[int, int]] = set()
    try:
        try:
            main_site = sitapi.mapGetSiteIdent(hmap_doc, 0)
        except Exception:
            main_site = 0
        flag = maptype.WO_FIRST
        while seekapi.mapTotalSeekObject(hmap_doc, seek_info, flag):
            flag = maptype.WO_NEXT
            try:
                if sitapi.mapGetObjectSiteIdent(hmap_doc, seek_info) != main_site:
                    continue
            except Exception:
                pass
            try:
                key = int(mapapi.mapObjectKey(seek_info) or 0)
            except Exception:
                continue
            if key not in object_keys:
                continue
            list_no = int(mapapi.mapGetListNumber(seek_info) or 1)
            obj_no = int(mapapi.mapGetObjectNumber(seek_info) or 0)
            if obj_no <= 0:
                continue
            sig = (list_no, obj_no)
            if sig in seen_lo:
                continue
            seen_lo.add(sig)
            targets.append((list_no, obj_no, key))
    finally:
        try:
            mapapi.mapFreeObject(seek_info)
        except Exception:
            pass
    site_try: List[int] = []
    try:
        s0 = int(sitapi.mapGetSiteIdent(hmap_doc, 0) or 0)
        if s0 != 0:
            site_try.append(s0)
    except Exception:
        pass
    site_try.append(0)
    updated = 0
    for list_no, obj_no, key in targets:
        ed = None
        try:
            ed = mapapi.mapCreateObject(hmap_doc, 1, maptype.IDDOUBLE2, 0)
            if not ed:
                continue
            loaded = False
            for hsite in site_try:
                try:
                    ro = read_by_num(hmap_doc, hsite, ed, int(list_no), int(obj_no))
                    if ro == 2:
                        loaded = True
                        break
                except Exception:
                    continue
            if not loaded:
                continue
            if not _shift_metric_points_east(ed, delta_east_m):
                continue
            rc = int(mapapi.mapCommitObject(ed) or 0)
            if rc <= 0:
                rc2 = int(mapapi.mapCommitObjectAsNew(ed) or 0)
                if rc2 > 0:
                    rc = rc2
            if rc > 0:
                updated += 1
        except Exception:
            pass
        finally:
            if ed:
                try:
                    mapapi.mapFreeObject(ed)
                except Exception:
                    pass
    try:
        if mapapi is not None and mapsyst is not None:
            if hasattr(mapapi, 'mapIsDiagnostics') and mapapi.mapIsDiagnostics():
                subj_s = ','.join((str(s) for s in SUBJECT_LABEL_METRIC_SUBJECTS))
                msg = 'сдвиг подписей субъектов на восток %g м: найдено=%s, обновлено=%s; субъекты метрики [%s]. Ключи: %s' % (delta_east_m, len(targets), updated, subj_s, ','.join((str(k) for k in sorted(object_keys)[:30])) + ('…' if len(object_keys) > 30 else ''))
                if not targets:
                    msg += ' — объекты с заданными ключами не найдены; задайте ROSSTAT2MAP_THEMATIC_TITLE_OBJECT_KEYS / ROSSTAT2MAP_SUBJECT_LABEL_OFFSET_EXTRA_KEYS / ROSSTAT2MAP_THEMATIC_TITLE_KEY_START_OFFSET / ROSSTAT2MAP_THEMATIC_TITLE_KEY_REFERENCE_COUNT / ROSSTAT2MAP_THEMATIC_TITLE_KEY_AUTO_SHIFT=0 / ROSSTAT2MAP_THEMATIC_TITLE_KEY_AUTO_PAIR_FACTOR.'
                elif updated <= 0:
                    msg += ' — метрика не сдвинута или mapCommitObject не прошёл; при необходимости ROSSTAT2MAP_SUBJECT_LABEL_METRIC_SUBJECTS.'
                write_diag_pair(msg, '', getattr(maptype, 'MT_INFO', 0))
    except Exception:
        pass
    return updated

def _reapply_map_put_text_align(info, fa_h: int, fa_v: int, log, log_tag: str) -> None:
    """Применение горизонтального и вертикального выравнивания к объектам Легенды"""
    if mapapi is None:
        return
    subj = 0
    try:
        ha = int(mapapi.mapPutTextHorizontalAlign(info, int(fa_h), subj) or 0)
        va = int(mapapi.mapPutTextVerticalAlign(info, int(fa_v), subj) or 0)
        gh = gv = None
        get_h = getattr(mapapi, 'mapGetTextHorizontalAlign', None)
        get_v = getattr(mapapi, 'mapGetTextVerticalAlign', None)
        if callable(get_h):
            try:
                gh = int(get_h(info, subj) or 0)
            except Exception:
                gh = None
        if callable(get_v):
            try:
                gv = int(get_v(info, subj) or 0)
            except Exception:
                gv = None
    except Exception:
        pass

def _apply_label_visibility_scales(info, log, context: str='label') -> None:
    """Применение горизонтального и вертикального выравнивания к объектам Легенды"""
    if mapapi is None or maptype is None or mapsyst is None:
        return
    top = int(LABEL_VISIBILITY_TOP_SCALE)
    bot = int(LABEL_VISIBILITY_BOT_SCALE)
    if top <= 0 or bot <= 0:
        return
    if top > bot:
        top, bot = (bot, top)
    val_for_api_top = bot
    val_for_api_bot = top
    lib = getattr(mapapi, 'acceslib', 0)

    def _read_diag() -> Tuple[int, int, int]:
        try:
            t = int(mapapi.mapObjectTopScale(info) or 0)
        except Exception:
            t = 0
        try:
            b = int(mapapi.mapObjectBotScale(info) or 0)
        except Exception:
            b = 0
        try:
            unq = int(mapapi.mapObjectBotTopUniqueness(info) or 0)
        except Exception:
            unq = 0
        return (t, b, unq)
    rc_top = 0
    try:
        rc_top = int(mapapi.mapSetObjectTopScale(info, val_for_api_top) or 0)
    except Exception:
        pass
    if rc_top <= 0 and lib:
        try:
            fn_t = mapsyst.GetProcAddress(lib, ctypes.c_int, 'mapSetObjectTopScale', maptype.HOBJ, ctypes.c_int)
            if fn_t:
                rc_top = int(fn_t(info, val_for_api_top) or 0)
        except Exception:
            pass
    rc_bot = 0
    try:
        rc_bot = int(mapapi.mapSetObjectBotScale(info, val_for_api_bot) or 0)
    except Exception:
        pass
    if rc_bot <= 0 and lib:
        try:
            fn_b = mapsyst.GetProcAddress(lib, ctypes.c_int, 'mapSetObjectBotScale', maptype.HOBJ, ctypes.c_int)
            if fn_b:
                rc_bot = int(fn_b(info, val_for_api_bot) or 0)
        except Exception:
            pass
    _read_diag()

def _register_legend_caption_classifier(info, log) -> bool:
    """Регистрация классификатора для заголовка Легенды"""
    if mapapi is None or maptype is None or mapsyst is None:
        return False
    lt = int(maptype.LOCAL_TITLE)
    key = (LEGEND_CAPTION_OBJECT_KEY or '').strip()

    def _log_ok(rc: int, fn: str) -> bool:
        if rc > 0:
            return True
        return False
    if key:
        raw_cp = key.encode('cp1251', errors='replace')
        buf = ctypes.create_string_buffer(raw_cp + b'\x00')
        key_ptr_variants = (buf, ctypes.cast(buf, ctypes.POINTER(ctypes.c_char)))
        by_key_un = getattr(mapapi, 'mapRegisterObjectByKeyUn', None)
        if by_key_un:
            for arg2 in key_ptr_variants:
                for args in ((info, arg2, lt), (info, arg2)):
                    try:
                        if _log_ok(int(by_key_un(*args) or 0), 'mapRegisterObjectByKeyUn'):
                            return True
                    except TypeError:
                        continue
                    except Exception as exc:
                        break
            try:
                wkey = mapsyst.WTEXT(key)
                for args in ((info, wkey, lt), (info, wkey)):
                    try:
                        if _log_ok(int(by_key_un(*args) or 0), 'mapRegisterObjectByKeyUn'):
                            return True
                    except TypeError:
                        continue
                    except Exception as exc:
                        break
            except Exception:
                pass
        by_key = getattr(mapapi, 'mapRegisterObjectByKey', None)
        if by_key:
            for arg2 in key_ptr_variants:
                for args in ((info, arg2, lt), (info, arg2)):
                    try:
                        if _log_ok(int(by_key(*args) or 0), 'mapRegisterObjectByKey'):
                            return True
                    except TypeError:
                        continue
                    except Exception as exc:
                        break
    excode = int(LEGEND_CAPTION_OBJECT_EXCODE)
    if excode > 0:
        try:
            if _log_ok(int(mapapi.mapRegisterObject(info, excode, lt) or 0), 'mapRegisterObject'):
                return True
        except Exception:
            pass
        lib = getattr(mapapi, 'acceslib', 0)
        if lib:
            try:
                register_fb = mapsyst.GetProcAddress(lib, ctypes.c_int, 'mapRegisterObject', maptype.HOBJ, ctypes.c_int, ctypes.c_int)
                if register_fb:
                    if _log_ok(int(register_fb(info, excode, lt) or 0), 'mapRegisterObject(GetProcAddress)'):
                        return True
            except Exception:
                pass
    return False

def _legend_caption_pack_truetype_font_name(truetext_struct, name: str) -> None:
    """Упаковка имени шрифта для заголовка Легенды"""
    ctypes.memset(ctypes.addressof(truetext_struct.FontName), 0, 32)
    enc = ((name or '').strip() or 'Tahoma').encode('cp1251', errors='replace')[:31]
    if enc:
        ctypes.memmove(ctypes.addressof(truetext_struct.FontName), enc, len(enc))

def _legend_caption_font_type_byte(info, rscapi_mod, log) -> int:
    """Тип шрифта для заголовка Легенды"""
    ft = int(LEGEND_CAPTION_FONT_TYPE) & 255
    if ft > 0:
        return ft
    num = int(LEGEND_CAPTION_FONT_NUMBER)
    if num <= 0 or rscapi_mod is None or mapapi is None:
        return 0
    try:
        hrsc = mapapi.mapGetRscIdentByObject(info)
        if _hmap_as_int(hrsc) == 0:
            return 0
        code = int(rscapi_mod.mapGetFontCode(hrsc, num) or 0)
        return code & 255
    except Exception as exc:
        return 0

def _apply_legend_caption_draw_parameters(info, log, rscapi_mod, *, height_mkm: Optional[int]=None, color_bgr: Optional[int]=None, bkgnd_bgr: Optional[int]=None, fa_horizontal: Optional[int]=None, fa_vertical: Optional[int]=None, imgtext_align: Optional[int]=None, truetype_name: Optional[str]=None, log_tag: str='legend_caption', ctypes_keepalive: Optional[List[Any]]=None, outline: Optional[int]=None, shadow_color_bgr: Optional[int]=None) -> int:
    """Применение параметров рисования для заголовка Легенды"""
    if mapapi is None or mapgdi is None or maptype is None:
        return 0
    hm = int(LEGEND_CAPTION_TEXT_HEIGHT_MKM if height_mkm is None else height_mkm)
    tc = int(LEGEND_CAPTION_TEXT_COLOR_BGR if color_bgr is None else color_bgr) & 16777215
    if bkgnd_bgr is None:
        tb = int(LEGEND_CAPTION_BKGND_COLOR) & 4294967295
    else:
        tb = int(bkgnd_bgr) & 4294967295
    fa_h = int(LEGEND_CAPTION_FA_LEFT if fa_horizontal is None else fa_horizontal)
    fa_v = int(LEGEND_CAPTION_FA_BOTTOM if fa_vertical is None else fa_vertical)
    ialign = int(LEGEND_CAPTION_IMGTEXT_ALIGN if imgtext_align is None else imgtext_align) & 65535
    ttn = ((truetype_name or LEGEND_CAPTION_TRUETYPE_NAME) or 'Tahoma').strip() or 'Tahoma'
    subj = 0
    try:
        ha = int(mapapi.mapPutTextHorizontalAlign(info, fa_h, subj) or 0)
        va = int(mapapi.mapPutTextVerticalAlign(info, fa_v, subj) or 0)
    except Exception:
        pass
    _try_map_put_text_draw_type(info, log, log_tag)
    font_type_fb = _legend_caption_font_type_byte(info, rscapi_mod, log)
    img = mapgdi.IMGTEXT()
    try:
        ctypes.memset(ctypes.byref(img), 0, ctypes.sizeof(img))
    except Exception:
        pass
    img.Color = tc
    img.BkgndColor = tb
    sh_raw = int(LEGEND_CAPTION_SHADOW_COLOR if shadow_color_bgr is None else shadow_color_bgr) & 4294967295
    img.ShadowColor = sh_raw
    img.Height = max(1, hm) & 4294967295
    img.Weight = max(1, min(65535, int(LEGEND_CAPTION_FONT_WEIGHT))) & 65535
    img.Outline = int(LEGEND_CAPTION_OUTLINE if outline is None else outline) & 255
    img.Interval = int(LEGEND_CAPTION_TEXT_INTERVAL_PCT) & 255
    img.Align = ialign
    img.Service = int(LEGEND_CAPTION_TEXT_SERVICE) & 65535
    img.Wide = 0
    img.Horizontal = 1 if int(LEGEND_CAPTION_FONT_HORIZONTAL) != 0 else 0
    img.Italic = 0
    img.Underline = 0
    img.StrikeOut = 0
    img.Type = int(LEGEND_CAPTION_IMGTEXT_TYPE_TRUETEXT) & 255
    img.CharSet = int(LEGEND_CAPTION_TEXT_CHARSET) & 255
    if hasattr(img, 'Flag'):
        img.Flag = int(LEGEND_CAPTION_TEXT_FLAG) & 65535
    if ctypes_keepalive is not None:
        ctypes_keepalive.append(img)
    rc_draw = 0
    if not hasattr(mapapi, 'mapAppendDraw'):
        return 0
    id_candidates: List[int] = []
    gdi_tt = int(getattr(mapgdi, 'IMG_TRUETEXT', 0) or 0)
    if gdi_tt > 0:
        id_candidates.append(gdi_tt)
    env_tt = int(LEGEND_CAPTION_IMG_TRUETEXT)
    if env_tt > 0 and env_tt not in id_candidates:
        id_candidates.append(env_tt)
    for fid in LEGEND_CAPTION_TRUETEXT_FALLBACK_IDS:
        if fid > 0 and fid not in id_candidates:
            id_candidates.append(fid)
    winning_img_id = 0
    if hasattr(mapgdi, 'IMGTRUETEXT'):
        for img_truetext in id_candidates:
            try:
                tt = mapgdi.IMGTRUETEXT()
                ctypes.memset(ctypes.byref(tt), 0, ctypes.sizeof(tt))
                try:
                    ctypes.memmove(ctypes.byref(tt.Text), ctypes.byref(img), ctypes.sizeof(img))
                except Exception:
                    tt.Text = img
                _legend_caption_pack_truetype_font_name(tt, ttn)
                rc_draw = 0
                for pay in (ctypes.cast(ctypes.byref(tt), ctypes.c_char_p), ctypes.cast(ctypes.byref(tt), ctypes.c_void_p)):
                    try:
                        rc_draw = int(mapapi.mapAppendDraw(info, int(img_truetext), pay) or 0)
                    except TypeError:
                        rc_draw = 0
                        continue
                    except Exception as exc_in:
                        rc_draw = 0
                        break
                    if rc_draw > 0:
                        break
                if rc_draw > 0:
                    winning_img_id = int(img_truetext)
                    break
            except Exception as exc:
                rc_draw = 0
    else:
        rc_draw = 0
    if rc_draw <= 0 and hasattr(mapgdi, 'IMGTRUETYPE'):
        for img_id in id_candidates:
            try:
                big = mapgdi.IMGTRUETYPE()
                ctypes.memset(ctypes.byref(big), 0, ctypes.sizeof(big))
                try:
                    ctypes.memmove(ctypes.byref(big.Text), ctypes.byref(img), ctypes.sizeof(img))
                except Exception:
                    big.Text = img
                _legend_caption_pack_truetype_font_name(big, ttn)
                for pay in (ctypes.cast(ctypes.byref(big), ctypes.c_char_p), ctypes.cast(ctypes.byref(big), ctypes.c_void_p)):
                    try:
                        rc_try = int(mapapi.mapAppendDraw(info, int(img_id), pay) or 0)
                    except TypeError:
                        continue
                    except Exception as exc_big:
                        break
                    if rc_try > 0:
                        rc_draw = rc_try
                        winning_img_id = int(img_id)
                        break
                if rc_draw > 0:
                    break
            except Exception as exc:
                rc_draw = 0
    if rc_draw <= 0 and int(LEGEND_CAPTION_ALLOW_IMG_TEXT_FALLBACK) != 0:
        img.Type = int(LEGEND_CAPTION_IMGTEXT_TYPE) & 255
        if int(font_type_fb) > 0:
            img.Type = int(font_type_fb) & 255
        try:
            img_txt_id = int(mapgdi.IMG_TEXT)
            rc_draw = 0
            for pay in (ctypes.cast(ctypes.byref(img), ctypes.c_char_p), ctypes.cast(ctypes.byref(img), ctypes.c_void_p)):
                try:
                    rc_draw = int(mapapi.mapAppendDraw(info, img_txt_id, pay) or 0)
                except TypeError:
                    rc_draw = 0
                    continue
                except Exception as exc_fb:
                    rc_draw = 0
                    break
                if rc_draw > 0:
                    break
            if rc_draw > 0:
                winning_img_id = img_txt_id
        except Exception:
            pass
    elif rc_draw <= 0:
        pass
    return rc_draw

def _add_legend_caption_object(result_sitx: Path, text: str, log) -> None:
    """Добавление объекта заголовка Легенды"""
    if not text or mapapi is None or mapsyst is None or (maptype is None):
        return
    caption_text = _caption_first_upper_rest_lower(text)
    if not caption_text:
        return
    empty_pass = mapsyst.WTEXT("") 
    err = ctypes.c_int(0)
    hres = mapapi.mapOpenAnyDataPro(mapsyst.WTEXT(str(result_sitx)), 0, ctypes.byref(err), empty_pass, 0)
    if _hmap_as_int(hres) == 0:
        return
    info = None
    try:
        sheet_no = 1
        try:
            sn = int(mapapi.mapGetListNumberByNomenclatureUn(hres, mapsyst.WTEXT(LEGEND_TEXT_LAYER_NAME)) or 0)
            if sn > 0:
                sheet_no = sn
        except Exception:
            pass
        info = mapapi.mapCreateObject(hres, sheet_no, maptype.IDDOUBLE2, 1)
        if not info:
            return
        rc_pt = int(mapapi.mapAppendPointPlane(info, float(LEGEND_TEXT_X), float(LEGEND_TEXT_Y), 0) or 0)
        w_caption = mapsyst.WTEXT(caption_text)
        rc_txt = int(mapapi.mapPutTextUn(info, w_caption, 0) or 0)
        _cap_keepalive: List[Any] = [w_caption]
        cls_ok = _register_legend_caption_classifier(info, log)
        if not cls_ok and ((LEGEND_CAPTION_OBJECT_KEY or '').strip() or int(LEGEND_CAPTION_OBJECT_EXCODE) > 0):
            pass
        clayer = int(GRAPHIC_CLASSIFIER_LAYER)
        if clayer >= 0 and mapapi is not None and (maptype is not None):
            try:
                rc_rdo = int(mapapi.mapRegisterDrawObject(info, clayer, int(maptype.LOCAL_TITLE)) or 0)
            except Exception:
                pass
        rscapi_mod = _get_rscapi_optional()
        rc_draw = _apply_legend_caption_draw_parameters(info, log, rscapi_mod, ctypes_keepalive=_cap_keepalive)
        if rc_draw > 0:
            try:
                rc_re = int(mapapi.mapPutTextUn(info, w_caption, 0) or 0)
            except Exception:
                pass
            _reapply_map_put_text_align(info, int(LEGEND_CAPTION_FA_LEFT), int(LEGEND_CAPTION_FA_BOTTOM), log, 'legend_caption')
        try:
            mapapi.mapSetObjectViewSemantic(info, 1)
        except Exception:
            pass
        _apply_label_visibility_scales(info, log, context='legend_caption')
        label_num = 1
        rc = int(mapapi.mapCommitObject(info) or 0)
        if rc <= 0:
            int(mapapi.mapCommitObjectAsNew(info) or 0)
    finally:
        try:
            if info:
                mapapi.mapFreeObject(info)
        except Exception:
            pass
        try:
            mapapi.mapCloseData(hres)
        except Exception:
            pass

def _register_gradation_polygon_area(info, log, idx: int) -> Tuple[int, int, int]:
    """Регистрация объектов с градиентом области"""
    rc_key = 0
    rc_reg = 0
    rc_desc = 0
    if mapapi is None or maptype is None:
        return (rc_key, rc_reg, rc_desc)
    key = (GRADATION_RECT_OBJECT_KEY or '').strip()
    if key:
        try:
            register_key_fn = getattr(mapapi, 'mapRegisterObjectByKey', None)
            if register_key_fn:
                rc_key = int(register_key_fn(info, key.encode('ascii', errors='ignore')) or 0)
                if rc_key > 0:
                    return (rc_key, rc_reg, rc_desc)
        except Exception:
            pass
    excode = int(GRADATION_RECT_OBJECT_EXCODE)
    if excode > 0:
        try:
            rc_reg = int(mapapi.mapRegisterObject(info, excode, int(maptype.LOCAL_SQUARE)) or 0)
            if rc_reg > 0:
                return (rc_key, rc_reg, rc_desc)
        except Exception:
            pass
    incode = int(GRADATION_RECT_OBJECT_INCODE)
    if incode > 0:
        try:
            rc_desc = int(mapapi.mapDescribeObject(info, incode) or 0)
            if rc_desc > 0:
                return (rc_key, rc_reg, rc_desc)
        except Exception:
            pass
    return (rc_key, rc_reg, rc_desc)

def _append_gradation_polygon_glass_draw(info, color_bgr: int, log, idx: int, draw_layer: int) -> Tuple[int, int, int]:
    """Добавление объектов с градиентом области"""
    rc_rdo = 0
    rc_draw = 0
    rc_sem = 0
    col = int(color_bgr) & 16777215
    if mapapi is None or maptype is None:
        return (rc_rdo, rc_draw, rc_sem)
    layer = int(draw_layer)
    if layer >= 0:
        try:
            rc_rdo = int(mapapi.mapRegisterDrawObject(info, layer, int(maptype.LOCAL_SQUARE)) or 0)
        except Exception:
            pass
    img_id = int(GRADATION_POLYGON_GLASS_IMAGE)
    if img_id <= 0 and mapgdi is not None:
        img_id = int(getattr(mapgdi, 'IMG_POLYGON_GLASS', 0) or 0)
    if mapgdi is not None and img_id > 0 and hasattr(mapapi, 'mapAppendDraw'):
        try:
            pg = mapgdi.IMGPOLYGONGLASS()
            pg.Color = col
            pg.Bright = int(GRADATION_GLASS_BRIGHTNESS)
            pg.Contrast = int(GRADATION_GLASS_CONTRAST)
            pg.Transparency = int(GRADATION_GLASS_TRANSPARENCY)
            rc_draw = int(mapapi.mapAppendDraw(info, img_id, ctypes.cast(ctypes.byref(pg), ctypes.c_char_p)) or 0)
        except Exception:
            pass
    if rc_draw <= 0:
        try:
            rc_sem = int(mapapi.mapAppendSemanticLong(info, int(maptype.SEMIMAGECOLOR), col) or 0)
        except Exception:
            pass
    return (rc_rdo, rc_draw, rc_sem)

def _add_gradation_range_label_object(hres, sheet_no: int, cx: float, cy: float, label_text: str, draw_layer: int, idx: int, log) -> None:
    """Добавление объектов с градиентом области"""
    if not (label_text or '').strip():
        return
    if mapapi is None or mapsyst is None or maptype is None or (mapgdi is None):
        return
    rscapi_mod = _get_rscapi_optional()
    info = None
    try:
        info = mapapi.mapCreateObject(hres, sheet_no, maptype.IDDOUBLE2, 1)
        if not info:
            return
        rc_pt = int(mapapi.mapAppendPointPlane(info, float(cx), float(cy), 0) or 0)
        t = label_text.strip()
        w_range = mapsyst.WTEXT(t)
        rc_txt = int(mapapi.mapPutTextUn(info, w_range, 0) or 0)
        _range_keepalive: List[Any] = [w_range]
        cls_ok = False
        if int(GRADATION_RANGE_REGISTER_LEGEND_CLASSIFIER) != 0:
            cls_ok = _register_legend_caption_classifier(info, log)
        if not cls_ok and ((LEGEND_CAPTION_OBJECT_KEY or '').strip() or int(LEGEND_CAPTION_OBJECT_EXCODE) > 0):
            pass
        if draw_layer >= 0:
            try:
                rc_rdo = int(mapapi.mapRegisterDrawObject(info, draw_layer, int(maptype.LOCAL_TITLE)) or 0)
            except Exception:
                pass
        rc_draw = _apply_legend_caption_draw_parameters(info, log, rscapi_mod, height_mkm=int(GRADATION_RANGE_TEXT_HEIGHT_MKM), color_bgr=int(GRADATION_RANGE_TEXT_COLOR_BGR), fa_horizontal=int(GRADATION_RANGE_TEXT_FA_H), fa_vertical=int(GRADATION_RANGE_TEXT_FA_V), imgtext_align=int(GRADATION_RANGE_IMGTEXT_ALIGN), truetype_name=str(GRADATION_RANGE_FONT_NAME), log_tag='gradation_range', ctypes_keepalive=_range_keepalive, outline=int(GRADATION_RANGE_TEXT_OUTLINE), shadow_color_bgr=int(GRADATION_RANGE_TEXT_OUTLINE_BGR))
        if rc_draw > 0:
            try:
                rc_re = int(mapapi.mapPutTextUn(info, w_range, 0) or 0)
            except Exception:
                pass
            _reapply_map_put_text_align(info, int(GRADATION_RANGE_TEXT_FA_H), int(GRADATION_RANGE_TEXT_FA_V), log, f'gradation_range_{idx}')
        try:
            mapapi.mapSetObjectViewSemantic(info, 1)
        except Exception:
            pass
        _apply_label_visibility_scales(info, log, context=f'gradation_range_{idx}')
        rc = int(mapapi.mapCommitObject(info) or 0)
        if rc <= 0:
            rc = int(mapapi.mapCommitObjectAsNew(info) or 0)
        if rc <= 0:
            pass
    finally:
        try:
            if info:
                mapapi.mapFreeObject(info)
        except Exception:
            pass

def _add_gradation_color_rectangles(result_sitx: Path, colors_bgr: List[int], log, range_labels: Optional[List[str]]=None) -> None:
    """Добавление объектов с градиентом области"""
    if len(colors_bgr) != 10:
        return
    if mapapi is None or mapsyst is None or maptype is None:
        return
    empty_pass = mapsyst.WTEXT("")
    err = ctypes.c_int(0)
    hres = mapapi.mapOpenAnyDataPro(mapsyst.WTEXT(str(result_sitx)), 0, ctypes.byref(err), empty_pass, 0)
    if _hmap_as_int(hres) == 0:
        return
    sheet_no = 1
    try:
        sn = int(mapapi.mapGetListNumberByNomenclatureUn(hres, mapsyst.WTEXT(GRADATION_RECT_LAYER_NAME)) or 0)
        if sn > 0:
            sheet_no = sn
    except Exception:
        pass
    if not (GRADATION_RECT_OBJECT_KEY or '').strip() and int(GRADATION_RECT_OBJECT_EXCODE) <= 0 and (int(GRADATION_RECT_OBJECT_INCODE) <= 0):
        pass
    w = float(GRADATION_RECT_WIDTH_M)
    h = float(GRADATION_RECT_HEIGHT_M)
    x_base = float(GRADATION_RECT_ORIGIN_X)
    y0 = float(GRADATION_RECT_ORIGIN_Y)
    step_x = float(GRADATION_RECT_STEP_X)
    delta_close = float(maptype.DELTANULL)
    draw_layer = int(GRAPHIC_CLASSIFIER_LAYER)
    labels_ok = bool(range_labels and len(range_labels) == 10)
    if range_labels is not None and (not labels_ok):
        pass
    for i in range(10):
        x0 = x_base - i * step_x
        corners = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]
        col = int(colors_bgr[i]) & 16777215
        info = None
        try:
            info = mapapi.mapCreateObject(hres, sheet_no, maptype.IDDOUBLE2, 0)
            if not info:
                continue
            for px, py in corners:
                mapapi.mapAppendPointPlane(info, float(px), float(py), 0)
            rc_ab = int(mapapi.mapAbridge(info, delta_close) or 0)
            rc_key, rc_reg, rc_desc = _register_gradation_polygon_area(info, log, i + 1)
            try:
                mapapi.mapSetObjectViewSemantic(info, 1)
            except Exception:
                pass
            rc_rdo, rc_draw, rc_col = _append_gradation_polygon_glass_draw(info, col, log, i + 1, draw_layer)
            rc = int(mapapi.mapCommitObject(info) or 0)
            if rc <= 0:
                rc = int(mapapi.mapCommitObjectAsNew(info) or 0)
            obj_key = int(mapapi.mapObjectKey(info) or 0) if rc > 0 else 0
        finally:
            try:
                if info:
                    mapapi.mapFreeObject(info)
            except Exception:
                pass
        if labels_ok:
            cx = x0 + w * 0.5
            cy = y0 + h * 0.5
            _add_gradation_range_label_object(hres, sheet_no, cx, cy, range_labels[i], draw_layer, i + 1, log)
    try:
        mapapi.mapCloseData(hres)
    except Exception:
        pass

def _try_close_previous_mpt(path: Optional[Path]) -> None:
    """Попытка закрыть ранее открытый проект тематики перед открытием нового"""
    if path is None or mapapi is None or mapsyst is None:
        return
    try:
        p = path.resolve()
        if not p.is_file():
            return
    except Exception:
        return
    w = mapsyst.WTEXT(str(p))
    for name in ('mapCloseDocumentUn', 'mapCloseFileUn', 'mapCloseProjectUn'):
        fn = getattr(mapapi, name, None)
        if not callable(fn):
            continue
        try:
            fn(w)
            return
        except TypeError:
            try:
                fn(w.buffer())
                return
            except Exception:
                pass
        except Exception:
            pass

def _map_set_real_show_scale(hmap) -> None:
    """Масштаб отображения карты 1:MAP_REAL_SHOW_SCALE_DENOMINATOR (mapSetRealShowScale)"""
    if mapapi is None or _hmap_as_int(hmap) == 0:
        return
    try:
        fn = getattr(mapapi, 'mapSetRealShowScale', None)
        if callable(fn):
            fn(hmap, float(MAP_REAL_SHOW_SCALE_DENOMINATOR))
    except Exception:
        pass

def _map_save_project_scale(hmap, project_mpt: Path) -> None:
    """Сохранить проект после смены масштаба (чтобы Панорама открыла с 1:N)"""
    if mapapi is None or mapsyst is None or _hmap_as_int(hmap) == 0:
        return
    try:
        p = Path(project_mpt)
        if not p.is_file():
            return
        mapapi.mapSaveProjectUn(hmap, mapsyst.WTEXT(str(p.resolve())))
    except Exception:
        pass

def _panorama_invalidate_map_view() -> None:
    """Запрос перерисовки окна карты после открытия .mpt/.sitx"""
    if mapapi is None:
        return
    try:
        inv = getattr(mapapi, 'mapInvalidate', None)
        if callable(inv):
            inv()
            return
        if maptype is not None:
            mt = int(getattr(maptype, 'MT_MAPWINPORT', 0x660))
            mw = int(getattr(maptype, 'MWP_INVALIDATE', 0x105))
            mapapi.mapSendMessage(ctypes.c_int(mt), ctypes.c_longlong(mw), 0)
    except Exception:
        pass

def _open_document_in_panorama_and_refresh(path: Path) -> bool:
    """Открыть документ в Панораме и запросить перерисовку окна карты"""
    ok = _open_document_in_panorama(path)
    if ok:
        _panorama_invalidate_map_view()
    return ok

def _open_document_in_panorama(path: Path) -> bool:
    """Открытие созданного документа в ГИС Панорама"""
    if mapapi is None or mapsyst is None:
        return False
    try:
        aw_opendocun = 1571
        wpath = mapsyst.WTEXT(str(path))
        mapapi.mapSendMessage(aw_opendocun, ctypes.addressof(wpath.buffer()), 0)
        return True
    except Exception:
        return False

def import_math_modules():
    """Импорт mathapi/seekapi/sitapi/rscapi для mathCreateThematicMap"""
    try:
        import mathapi
        import seekapi
        import sitapi
        import rscapi
        return (mathapi, seekapi, sitapi, rscapi)
    except Exception:
        return (None, None, None, None)

def _rgb_color(r: int, g: int, b: int) -> int:
    """Преобразование RGB-значений в целое число"""
    return r & 255 | (g & 255) << 8 | (b & 255) << 16

def _split_rgb(color: int) -> Tuple[int, int, int]:
    """Разделение RGB-значения на компоненты"""
    return (color >> 16 & 255, color >> 8 & 255, color & 255)

def _interpolate_rgb(c1: int, c2: int, t: float) -> int:
    """Интерполяция RGB-значений"""
    r1, g1, b1 = _split_rgb(int(c1))
    r2, g2, b2 = _split_rgb(int(c2))
    r = int(round(r1 + (r2 - r1) * t))
    g = int(round(g1 + (g2 - g1) * t))
    b = int(round(b1 + (b2 - b1) * t))
    return _rgb_color(r, g, b)

def _collect_map_object_keys(hmap, seekapi, sitapi, object_code_filter: int=0, excluded_object_codes: Optional[Set[int]]=None) -> List[int]:
    """Сбор ключей объектов на карте"""
    info = mapapi.mapCreateObject(hmap, 1, maptype.IDDOUBLE2, 0)
    if not info:
        raise RuntimeError('Не удалось создать объект')
    try:
        main_site = sitapi.mapGetSiteIdent(hmap, 0)
        keys: List[int] = []
        flag = maptype.WO_FIRST
        while seekapi.mapTotalSeekObject(hmap, info, flag):
            flag = maptype.WO_NEXT
            try:
                if sitapi.mapGetObjectSiteIdent(hmap, info) != main_site:
                    continue
            except Exception:
                continue
            local = mapapi.mapObjectLocal(info)
            if local not in (maptype.LOCAL_SQUARE, maptype.LOCAL_LINE):
                continue
            if object_code_filter > 0:
                try:
                    obj_code = int(mapapi.mapObjectCode(info) or 0)
                except Exception:
                    continue
                if obj_code != int(object_code_filter):
                    continue
            else:
                try:
                    obj_code = int(mapapi.mapObjectCode(info) or 0)
                except Exception:
                    obj_code = 0
            if excluded_object_codes and obj_code in excluded_object_codes:
                continue
            key = int(mapapi.mapObjectKey(info) or 0)
            if key > 0:
                keys.append(key)
        return keys
    finally:
        try:
            mapapi.mapFreeObject(info)
        except Exception:
            pass

def _normalize_link_text(value: str) -> str:
    """Нормализация текста ссылки"""
    text = (value or '').strip().lower()
    text = text.replace('\xa0', ' ').replace('\u2009', ' ').replace('\u202f', ' ')
    text = text.replace('ё', 'е')
    text = re.sub('\\s+', ' ', text)
    text = text.strip(' \'"`.,;:()[]{}')
    return text

def _thematic_connect_col_index() -> int:
    """Определение индекса столбца соединения для тематических данных"""
    return THEMATIC_CONNECT_COLUMN - 1

def _value_column_min_1based() -> int:
    """Минимальный номер столбца значений (1-based): первый после столбца связи столбец"""
    return int(THEMATIC_CONNECT_COLUMN) + 1

def _row_link_text_for_thematic(row: List[str]) -> str:
    """Определение текста ссылки для тематических данных"""
    ci = _thematic_connect_col_index()
    if not row or ci >= len(row):
        return ''
    return (row[ci] or '').strip()

def _is_excluded_federal_row(link_text: str) -> bool:
    """Проверка на исключение строки с федеральными округами"""
    norm = _normalize_link_text(link_text)
    if not norm:
        return False
    if norm in {'российская федерация', 'рф', 'россия'}:
        return True
    if norm.startswith('российская федерация'):
        return True
    return False
_FED_DISTRICT_NAME_RE = re.compile('\\b(центральный|северо[-\\s]?западный|южный|приволжский|уральский|сибирский|дальневосточный|северо[-\\s]?кавказский)\\s+федеральный(\\s+округ)?\\b')

def _is_excluded_federal_district_row(link_text: str) -> bool:
    """Проверка на исключение строки с федеральными округами"""
    norm = _normalize_link_text(link_text)
    if not norm:
        return False
    if 'федеральный округ' in norm:
        return True
    if _FED_DISTRICT_NAME_RE.search(norm):
        return True
    if norm in {'цфо', 'сзфо', 'юфо', 'пфо', 'уфо', 'сфо', 'дфо', 'скфо'}:
        return True
    return False

def _preview_subject_rows_slice(rows: List[List[str]], max_visible: int, body_start: int=THEMATIC_DATA_FIRST_ROW_INDEX) -> List[List[str]]:
    """Строки предпросмотра: с первой строки субъекта РФ (не РФ целиком, не федеральные округа), с той же строки, что и данные тематики"""
    out: List[List[str]] = []
    for ridx, row in enumerate(rows):
        if ridx < body_start:
            continue
        link = _row_link_text_for_thematic(row)
        if not link:
            continue
        if _is_excluded_federal_row(link) or _is_excluded_federal_district_row(link):
            continue
        out.append(row)
        if len(out) >= max_visible:
            break
    return out

def _trimmed_link_text_for_match(link_text: str) -> str:
    """Определение текста ссылки для сопоставления"""
    t = (link_text or '').strip()
    tl = re.sub('\\s+', ' ', t.lower().replace('ё', 'е'))
    m = re.match('^(?:в\\s+том\\s+числе|в\\s*т\\.?\\s*ч\\.?)\\s*', tl)
    if m:
        return tl[m.end():].strip()
    return t

def _longest_map_name_in_row(row_norm: str, norm_to_keys: Dict[str, List[int]], min_len: int=4) -> Optional[Tuple[List[int], str]]:
    """Определение самого длинного имени карты в строке"""
    if not row_norm:
        return None
    best_keys: Optional[List[int]] = None
    best_name = ''
    best_len = 0
    for name_map, keys in norm_to_keys.items():
        nm = (name_map or '').strip()
        if len(nm) < min_len:
            continue
        if nm in row_norm and len(nm) > best_len:
            best_len = len(nm)
            best_keys = keys
            best_name = nm
    if best_keys:
        return (best_keys, best_name)
    return None

def _best_substring_match_for_row(norm_full: str, norm_trimmed: str, norm_to_keys: Dict[str, List[int]]) -> Optional[Tuple[List[int], str, str]]:
    """Определение лучшего совпадения подстроки для строки"""
    candidates = [norm_full]
    if norm_trimmed and norm_trimmed != norm_full:
        candidates.append(norm_trimmed)
    best: Optional[Tuple[List[int], str, str]] = None
    best_mlen = 0
    for cand in candidates:
        hit = _longest_map_name_in_row(cand, norm_to_keys)
        if not hit:
            continue
        keys, mname = hit
        if len(mname) > best_mlen:
            best_mlen = len(mname)
            best = (keys, mname, cand)
    return best

def _shortest_map_name_containing_row(row_norm: str, norm_to_keys: Dict[str, List[int]], min_row_len: int=12, min_map_len: int=4) -> Optional[Tuple[List[int], str]]:
    """Определение самого короткого имени карты в строке"""
    if not row_norm or len(row_norm) < min_row_len:
        return None
    best_keys: Optional[List[int]] = None
    best_nm = ''
    best_len = 10 ** 9
    for name_map, keys in norm_to_keys.items():
        nm = (name_map or '').strip()
        if len(nm) < min_map_len:
            continue
        if row_norm not in nm:
            continue
        if len(nm) < best_len:
            best_len = len(nm)
            best_keys = keys
            best_nm = nm
    if best_keys:
        return (best_keys, best_nm)
    return None

def _best_row_inside_map_match(norm_full: str, norm_trimmed: str, norm_to_keys: Dict[str, List[int]]) -> Optional[Tuple[List[int], str, str]]:
    """Определение лучшего совпадения строки внутри карты"""
    candidates = [norm_full]
    if norm_trimmed and norm_trimmed != norm_full:
        candidates.append(norm_trimmed)
    best: Optional[Tuple[List[int], str, str]] = None
    best_map_len = 10 ** 9
    for cand in candidates:
        hit = _shortest_map_name_containing_row(cand, norm_to_keys)
        if not hit:
            continue
        keys, mname = hit
        if len(mname) < best_map_len:
            best_map_len = len(mname)
            best = (keys, mname, cand)
    return best

def _set_wchar_array(field, text: str) -> None:
    """Установка массива символов в поле"""
    try:
        raw = (text or '').encode('utf-16-le', errors='ignore') + b'\x00\x00'
        cap = ctypes.sizeof(field)
        ctypes.memset(ctypes.byref(field), 0, cap)
        ctypes.memmove(ctypes.byref(field), raw, min(len(raw), cap))
    except Exception:
        pass

def _set_dialog_ansi_field(field_buf, text: str) -> None:
    """Установка массива символов в поле"""
    try:
        raw = (text or '').encode('cp1251', errors='replace')[:255]
        ctypes.memset(ctypes.addressof(field_buf), 0, ctypes.sizeof(field_buf))
        if raw:
            ctypes.memmove(ctypes.addressof(field_buf), raw, len(raw))
    except Exception:
        pass

def _table_header_row_for_thematic(table_abs: Path, value_col: int) -> Tuple[str, str]:
    """Определение заголовков строк для тематических данных"""
    try:
        rows = _read_table_rows(table_abs, limit_rows=4)
        hdr: List[str] = rows[3] if len(rows) > 3 else []
        ci = _thematic_connect_col_index()
        ch = (hdr[ci] if ci < len(hdr) else '').strip()
        vi = max(0, int(value_col) - 1)
        vh = (hdr[vi] if vi < len(hdr) else '').strip()
        return (ch, vh)
    except Exception:
        return ('', '')

def _preview_sheet_column_period_labels(table_abs: Path, ncols: int) -> List[str]:
    """Подписи столбцов по шапке: строка 3 (год) + строка 4 (месяц/квартал), с протяжкой объединённых ячеек"""
    try:
        rows = _read_table_rows(table_abs, limit_rows=4)
    except Exception:
        rows = []
    yrow: List[str] = []
    mrow: List[str] = []
    if len(rows) >= 4:
        yrow = _forward_fill_row_for_merged_cells([str(x) for x in rows[2]])
        mrow = _forward_fill_row_for_merged_cells([str(x) for x in rows[3]])
    out: List[str] = []
    for c in range(ncols):
        ys = yrow[c].strip() if c < len(yrow) else ''
        ms = mrow[c].strip() if c < len(mrow) else ''
        out.append(f'{ys} {ms}'.strip())
    return out

def _legend_place_xy_from_map_border(hmap) -> Tuple[float, float]:
    """Определение координат для размещения заголовка Легенды"""
    if mapapi is None or maptype is None:
        return (0.0, 0.0)
    border = maptype.DFRAME()
    try:
        rc = int(mapapi.mapGetTotalBorder(hmap, ctypes.byref(border), maptype.PP_PLANE) or 0)
        if rc <= 0:
            return (0.0, 0.0)
        x1, x2 = sorted([float(border.X1), float(border.X2)])
        y1, y2 = sorted([float(border.Y1), float(border.Y2)])
        w = x2 - x1
        h = y2 - y1
        margin = max(w, h) * 0.03
        if margin <= 0.0:
            margin = 1.0
        place_x = x1 + margin
        place_y = y2 - margin
        return (place_x, place_y)
    except Exception:
        return (0.0, 0.0)

def _build_objname_index(hmap, connect_sem: int, seekapi, sitapi, allowed_keys: Optional[Set[int]]=None) -> Tuple[Dict[str, List[int]], Dict[str, List[int]]]:
    """Построение индекса объектов по имени"""
    exact: Dict[str, List[int]] = {}
    normalized: Dict[str, List[int]] = {}
    info = mapapi.mapCreateObject(hmap, 1, maptype.IDDOUBLE2, 0)
    if not info:
        return (exact, normalized)
    try:
        main_site = sitapi.mapGetSiteIdent(hmap, 0)
        flag = maptype.WO_FIRST
        while seekapi.mapTotalSeekObject(hmap, info, flag):
            flag = maptype.WO_NEXT
            try:
                if sitapi.mapGetObjectSiteIdent(hmap, info) != main_site:
                    continue
            except Exception:
                continue
            key = int(mapapi.mapObjectKey(info) or 0)
            if key <= 0:
                continue
            if allowed_keys is not None and key not in allowed_keys:
                continue
            buf = mapsyst.WTEXT(1024)
            try:
                mapapi.mapSemanticCodeValuePro(info, int(connect_sem), buf, buf.size(), 0, 0)
                raw = (buf.string() or '').strip()
            except Exception:
                raw = ''
            if not raw:
                continue
            exact.setdefault(raw, []).append(key)
            norm = _normalize_link_text(raw)
            if norm:
                normalized.setdefault(norm, []).append(key)
    finally:
        try:
            mapapi.mapFreeObject(info)
        except Exception:
            pass
    return (exact, normalized)

def _map_table_rows_to_values_with_fallback(table_abs: Path, value_col: int, objname_exact: Dict[str, List[int]], objname_norm: Dict[str, List[int]], admname_exact: Dict[str, List[int]], admname_norm: Dict[str, List[int]]) -> Dict[int, float]:
    """Сопоставление строк таблицы с значениями на карте"""
    obj_exact_count = 0
    obj_norm_count = 0
    adm_exact_count = 0
    adm_norm_count = 0
    obj_partial_count = 0
    adm_partial_count = 0
    obj_row_in_map_count = 0
    adm_row_in_map_count = 0
    miss_count = 0
    empty_count = 0
    no_value_count = 0
    mapped_values: Dict[int, float] = {}
    col_idx = max(0, int(value_col) - 1)
    rows = _read_table_rows(table_abs)
    for row_no, row in enumerate(rows, start=1):
        link_text = _row_link_text_for_thematic(row)
        value_text = row[col_idx].strip() if col_idx < len(row) else ''
        parsed = _parse_float_guess(value_text)
        if not link_text:
            empty_count += 1
            continue
        if _is_excluded_federal_row(link_text):
            continue
        if _is_excluded_federal_district_row(link_text):
            continue
        if parsed is None:
            no_value_count += 1
            continue
        keys = objname_exact.get(link_text)
        if keys:
            obj_exact_count += 1
            for k in keys:
                mapped_values[int(k)] = float(parsed)
            continue
        norm = _normalize_link_text(link_text)
        nkeys = objname_norm.get(norm, [])
        if nkeys:
            obj_norm_count += 1
            for k in nkeys:
                mapped_values[int(k)] = float(parsed)
            continue
        akeys = admname_exact.get(link_text, [])
        if akeys:
            adm_exact_count += 1
            for k in akeys:
                mapped_values[int(k)] = float(parsed)
            continue
        ankeys = admname_norm.get(norm, [])
        if ankeys:
            adm_norm_count += 1
            for k in ankeys:
                mapped_values[int(k)] = float(parsed)
            continue
        norm_trim = _normalize_link_text(_trimmed_link_text_for_match(link_text))
        sub_obj = _best_substring_match_for_row(norm, norm_trim, objname_norm)
        if sub_obj:
            pkeys, pmap, pcand = sub_obj
            obj_partial_count += 1
            for k in pkeys:
                mapped_values[int(k)] = float(parsed)
            continue
        sub_obj_in_map = _best_row_inside_map_match(norm, norm_trim, objname_norm)
        if sub_obj_in_map:
            pkeys, pmap, pcand = sub_obj_in_map
            obj_row_in_map_count += 1
            for k in pkeys:
                mapped_values[int(k)] = float(parsed)
            continue
        sub_adm = _best_substring_match_for_row(norm, norm_trim, admname_norm)
        if sub_adm:
            akeys2, amap, acand = sub_adm
            adm_partial_count += 1
            for k in akeys2:
                mapped_values[int(k)] = float(parsed)
            continue
        sub_adm_in_map = _best_row_inside_map_match(norm, norm_trim, admname_norm)
        if sub_adm_in_map:
            akeys2, amap, acand = sub_adm_in_map
            adm_row_in_map_count += 1
            for k in akeys2:
                mapped_values[int(k)] = float(parsed)
            continue
        miss_count += 1
    return mapped_values
    
def run_thematic_with_mathapi(table_path: Path, report_code: str, value_col: int, min_value: float, max_value: float, color_min: int, color_max: int, *, previous_mpt: Optional[Path]=None, output_stem: Optional[str]=None) -> Tuple[int, Path, Path]:
    """Построение тематической карты с использованием mathapi"""
    log = get_logger()
    mathapi, seekapi, sitapi, rscapi = import_math_modules()
    if any((x is None for x in (mathapi, seekapi, sitapi, rscapi))):
        raise RuntimeError('Не удалось импортировать модули mathapi/seekapi/sitapi/rscapi из py_mapapi14')
    if mapapi is None or mapsyst is None or maptype is None:
        raise RuntimeError('Нужны mapapi/mapsyst/maptype (запуск из ГИС Панорама)')

    def _resolve_mapmath_lib():
        """Определение пути к библиотеке mathapi"""
        lib = getattr(mathapi, 'mathlib', 0)
        if lib:
            return lib
        dll_candidates = ['C:\\Program Files\\Panorama\\Panorama15\\mapmath64.dll', 'C:\\Program Files\\Panorama\\Panorama15\\mapmath.dll', 'mapmath64.dll', 'mapmath.dll']
        for dll_name in dll_candidates:
            try:
                lib = mapsyst.LoadLibrary(dll_name)
                if lib:
                    return lib
            except Exception:
                continue
        raise RuntimeError('Не удалось загрузить mapmath64.dll')
    mapmath_lib = _resolve_mapmath_lib()

    def _call_math_create_thematic_map(sitename_w, legend_w, options_p, values_arr, obj_arr, obj_count: int) -> int:
        """Вызов функции mathCreateThematicMap"""
        fn = getattr(mathapi, 'mathCreateThematicMap', None)
        if callable(fn):
            return int(fn(sitename_w, legend_w, options_p, values_arr, obj_arr, obj_count) or 0)
        fn_ptr = mapsyst.GetProcAddress(mapmath_lib, ctypes.c_int, 'mathCreateThematicMap', maptype.PWCHAR, maptype.PWCHAR, ctypes.POINTER(mathapi.THEMATICPARM), ctypes.POINTER(mathapi.RANGEITEM), ctypes.POINTER(mathapi.OBJVALUE), ctypes.c_int)
        return int(fn_ptr(sitename_w.buffer(), legend_w.buffer(), options_p, values_arr, obj_arr, obj_count) or 0)

    def _call_math_set_thematic_data(path_w, options_p, param_p, obj_arr, obj_count: int) -> int:
        """Вызов функции mathSetThematicData"""
        fn = getattr(mathapi, 'mathSetThematicData', None)
        if callable(fn):
            return int(fn(path_w, options_p, param_p, obj_arr, obj_count) or 0)
        fn_ptr = mapsyst.GetProcAddress(mapmath_lib, ctypes.c_int, 'mathSetThematicData', maptype.PWCHAR, ctypes.POINTER(mathapi.THEMATICPARM), ctypes.POINTER(mathapi.THEMDIALOGPARM), ctypes.POINTER(mathapi.OBJVALUE), ctypes.c_int)
        return int(fn_ptr(path_w.buffer(), options_p, param_p, obj_arr, obj_count) or 0)
    table_abs = table_path.resolve()
    if not table_abs.is_file():
        raise RuntimeError(f'Таблица не найдена: {table_abs}')
    _try_close_previous_mpt(previous_mpt)
    try:
        table_size = table_abs.stat().st_size
    except Exception:
        table_size = 0
    source_map = resolve_ru_regions_sitz_path()
    empty_pass = mapsyst.WTEXT("")
    err = ctypes.c_int(0)
    hmap = mapapi.mapOpenAnyDataPro(mapsyst.WTEXT(str(source_map)), 0, ctypes.byref(err), empty_pass, 0)
    if _hmap_as_int(hmap) == 0:
        raise RuntimeError(f'Не удалось открыть исходную карту {source_map}, код={err.value}')
    _map_set_real_show_scale(hmap)
    try:
        hrsc = rscapi.mapGetRscIdent(hmap, hmap)
        if not hrsc:
            raise RuntimeError('Не удалось определить классификатор карты')
        subject_key = resolve_ru_regions_subject_key()
        subject_obj_code = int(rscapi.mapGetRscObjectCodeByKeyUn(hrsc, mapsyst.WTEXT(subject_key)) or 0)
        if subject_obj_code <= 0:
            raise RuntimeError(f"Не найден код объекта по ключу субъектов '{subject_key}' в классификаторе")
        excluded_codes: Set[int] = set()
        admin3_code = int(rscapi.mapGetRscObjectCodeByKeyUn(hrsc, mapsyst.WTEXT('a_admin-3')) or 0)
        if admin3_code > 0:
            excluded_codes.add(admin3_code)
        keys = _collect_map_object_keys(hmap, seekapi, sitapi, object_code_filter=subject_obj_code, excluded_object_codes=excluded_codes)
        if not keys:
            raise RuntimeError('В исходной карте не найдены объекты субъектов РФ для построения тематической карты')
        allowed_keys = set(keys)
        sem_obj = int(rscapi.mapGetRscSemanticCodeByKeyUn(hrsc, mapsyst.WTEXT('ObjName')) or 0)
        sem_adm = int(rscapi.mapGetRscSemanticCodeByKeyUn(hrsc, mapsyst.WTEXT('AdmName')) or 0)
        if sem_obj <= 0 and sem_adm <= 0:
            raise RuntimeError("Не найдены семантики связи ни по ключу 'ObjName', ни по 'AdmName'")
        obj_exact: Dict[str, List[int]] = {}
        obj_norm: Dict[str, List[int]] = {}
        adm_exact: Dict[str, List[int]] = {}
        adm_norm: Dict[str, List[int]] = {}
        if sem_obj > 0:
            obj_exact, obj_norm = _build_objname_index(hmap, sem_obj, seekapi, sitapi, allowed_keys=allowed_keys)
        if sem_adm > 0:
            adm_exact, adm_norm = _build_objname_index(hmap, sem_adm, seekapi, sitapi, allowed_keys=allowed_keys)
        mapped_values = _map_table_rows_to_values_with_fallback(table_abs=table_abs, value_col=value_col, objname_exact=obj_exact, objname_norm=obj_norm, admname_exact=adm_exact, admname_norm=adm_norm)
        if not mapped_values:
            raise RuntimeError('В выбранном столбце нет значений для тематического картографирования')
        found = len(mapped_values)
        _ref_count_raw = (os.environ.get('ROSSTAT2MAP_THEMATIC_TITLE_KEY_REFERENCE_COUNT') or '').strip()
        reference_subject_count_for_keys = max(1, int(_ref_count_raw, 0)) if _ref_count_raw else len(allowed_keys)
        obj_arr = (mathapi.OBJVALUE * found)()
        for idx, (key, val) in enumerate(mapped_values.items()):
            obj_arr[idx].Key = int(key)
            obj_arr[idx].Value = float(val)
            obj_arr[idx].Color = 0
        connect_sem_for_options = sem_obj if sem_obj > 0 else sem_adm
        options = mathapi.THEMATICPARM()
        legend_place_x, legend_place_y = (0.0, 0.0)
        options.Hmap = hmap
        options.Hsite = hmap
        options.Handle = mapapi.mapGetHandleForMessage()
        options.ImageType = 0
        options.ConnectType = 2
        options.SearchMode = 1
        options.LegendToDiagram = 1
        options.MakeNumberCheck = 0
        options.DiaLabelColor = _rgb_color(0, 0, 0)
        options.LegendLabelColor = _rgb_color(0, 0, 0)
        options.DiaShadowColor = _rgb_color(255, 255, 255)
        options.LegendLabelShadowColor = _rgb_color(255, 255, 255)
        options.DiaCircleColor = -1
        options.ContourColor = _rgb_color(168, 168, 168)
        options.ContourThick = 250
        options.Transparent = 80
        options.EmptyCreate = 0
        options.FlagTerritory = 1
        options.RegionColCount = 5
        options.RegionX = 0
        options.RegionY = 0
        name_sem_legend = resolve_ru_regions_name_sem_code()
        if name_sem_legend > 0:
            options.NameSem = name_sem_legend
            if sem_obj > 0 and int(name_sem_legend) == int(sem_obj):
                pass
        else:
            options.NameSem = connect_sem_for_options
        options.ItemsCount = 10
        options.LegendColCount = 1
        map_name_from_table = table_abs.stem
        legend_name = _table_a1_a2_text(table_abs) or map_name_from_table
        file_stem = _sanitize_windows_filename_stem(output_stem) if (output_stem and str(output_stem).strip()) else _sanitize_windows_filename_stem(map_name_from_table)
        _set_wchar_array(options.ResMapName, file_stem)
        _set_wchar_array(options.LegendName, file_stem)
        scale = 20000000
        try:
            if hasattr(mapapi, 'mapGetMapScale'):
                scale_val = int(mapapi.mapGetMapScale(hmap) or 0)
                if scale_val > 0:
                    scale = scale_val
        except Exception:
            pass
        scale = int(max(MAP_SCALE_FOR_THEMATIC_MIN, min(int(scale), MAP_SCALE_FOR_THEMATIC_MAX)))
        lbw = max(1, scale // 20)
        lbh = max(1, scale // 40)
        lbi = max(1, scale // 200)
        lfh = max(1, scale // 80)
        options.LegendBarWide = min(lbw, THEMATIC_C_INT_MAX)
        options.LegendBarHeight = min(lbh, THEMATIC_C_INT_MAX)
        options.LegendInterval = min(lbi, THEMATIC_C_INT_MAX)
        options.LegendFontHeight = min(lfh, THEMATIC_C_INT_MAX)
        options.DiaFontHeight = options.LegendFontHeight
        try:
            options.Scale = min(scale, THEMATIC_C_INT_MAX)
        except Exception:
            pass
        lx, ly = _legend_place_xy_from_map_border(hmap)
        if lx != 0.0 or ly != 0.0:
            legend_place_x, legend_place_y = (lx, ly)
            options.PlaceX = lx
            options.PlaceY = ly
        else:
            options.PlaceX = 0.0
            options.PlaceY = 0.0
        param = mathapi.THEMDIALOGPARM()
        param.DataType = 1
        param.ConnectFieldType = 0
        param.ConnectSem = connect_sem_for_options
        param.NumberConnectField = _thematic_connect_col_index()
        param.NumberValueField = max(0, int(value_col) - 1)
        param.Delimiter = ord(';')
        param.Quote = ord('"')
        param.LinesBegin = 4
        hdr_connect, hdr_value = _table_header_row_for_thematic(table_abs, value_col)
        _set_dialog_ansi_field(param.ConnectField, hdr_connect)
        _set_dialog_ansi_field(param.ValueField, legend_name or hdr_value or map_name_from_table)
        work_dir = DATA_DIR / 'thematic_map'
        work_dir.mkdir(parents=True, exist_ok=True)
        result_sitx = work_dir / f'{file_stem}.sitx'
        min_v = float(min_value)
        max_v = float(max_value)
        if max_v <= min_v:
            max_v = min_v + 1e-09
        segment_count = 10
        step_v = (max_v - min_v) / float(segment_count)
        values = (mathapi.RANGEITEM * segment_count)()
        legend_prefix = legend_name.strip() if legend_name.strip() else map_name_from_table
        for i in range(segment_count):
            t = 0.0 if segment_count <= 1 else i / float(segment_count - 1)
            vmin = min_v + i * step_v
            vmax = min_v + (i + 1) * step_v if i < segment_count - 1 else max_v
            values[i].Min = vmin
            values[i].Max = vmax
            values[i].Color = int(_interpolate_rgb(int(color_min), int(color_max), t))
            values[i].Step = 2
            values[i].Thick = 1
            values[i].Type = int(THEMATIC_RANGEITEM_TYPE)
            label_text = f'{legend_prefix}: {_format_value_range_label_int(vmin, vmax)}'
            _set_wchar_array(values[i].RealName, label_text)
        gradation_colors = [int(values[i].Color) & 16777215 for i in range(segment_count)]
        gradation_range_labels = [_format_value_range_label_int(float(values[i].Min), float(values[i].Max)) for i in range(segment_count)]

        def _reapply_thematic_titles() -> None:
            """Применение заголовков к тематической карте"""
            _set_wchar_array(options.ResMapName, file_stem)
            _set_wchar_array(options.LegendName, file_stem)
            try:
                options.Scale = min(int(scale), THEMATIC_C_INT_MAX)
            except Exception:
                pass
            if legend_place_x != 0.0 or legend_place_y != 0.0:
                options.PlaceX = legend_place_x
                options.PlaceY = legend_place_y
        if table_abs.suffix.lower() in {'.dbf', '.csv', '.txt'}:
            obj_backup = [(int(obj_arr[i].Key), float(obj_arr[i].Value), int(obj_arr[i].Color)) for i in range(found)]
            try:
                sd = _call_math_set_thematic_data(mapsyst.WTEXT(str(table_abs)), ctypes.byref(options), ctypes.byref(param), obj_arr, found)
            except Exception:
                pass
            for i in range(found):
                obj_arr[i].Key = obj_backup[i][0]
                obj_arr[i].Value = obj_backup[i][1]
                obj_arr[i].Color = obj_backup[i][2]
            _reapply_thematic_titles()
        created = _call_math_create_thematic_map(mapsyst.WTEXT(str(result_sitx)), mapsyst.WTEXT(str(result_sitx)), ctypes.byref(options), values, obj_arr, found)
        if created <= 0:
            raise RuntimeError(f'mathCreateThematicMap вернула {created}.')
        if not result_sitx.is_file():
            raise RuntimeError(f'После mathCreateThematicMap не найден файл результата: {result_sitx}')
        try:
            result_size = result_sitx.stat().st_size
        except Exception:
            result_size = 0
        _refresh_thematic_region_title_keys_if_default(table_abs, actual_value_count=found, reference_subject_count=reference_subject_count_for_keys)
        _log_thematic_title_keys_session_summary(table_abs, actual_value_count=found, reference_subject_count=reference_subject_count_for_keys)
        if THEMATIC_REGION_TITLE_OBJECT_KEYS:
            need_align = THEMATIC_TITLE_ALIGN_ENABLE != 0
            need_east = abs(SUBJECT_LABEL_OFFSET_EAST_M) > 1e-09
            if need_align or need_east:
                err_al = ctypes.c_int(0)
                hres_al = mapapi.mapOpenAnyDataPro(mapsyst.WTEXT(str(result_sitx)), 0, ctypes.byref(err_al), empty_pass, 0)
                if _hmap_as_int(hres_al) != 0:
                    try:
                        if need_align:
                            fa_mid = _fa_vertical_middle_value()
                            _apply_vertical_align_to_thematic_title_objects(hres_al, log, seekapi, sitapi, THEMATIC_REGION_TITLE_OBJECT_KEYS, fa_vertical=fa_mid, subjects=THEMATIC_TITLE_ALIGN_SUBJECTS)
                        if need_east:
                            _keys_east = set(THEMATIC_REGION_TITLE_OBJECT_KEYS) | SUBJECT_LABEL_OFFSET_EXTRA_KEYS
                            _offset_subject_labels_east_m(hres_al, seekapi, sitapi, _keys_east, -SUBJECT_LABEL_OFFSET_EAST_M)
                    finally:
                        try:
                            mapapi.mapCloseData(hres_al)
                        except Exception:
                            pass
        label_text = _table_a1_a2_text(table_abs)
        _add_legend_caption_object(result_sitx, label_text, log)
        _add_gradation_color_rectangles(result_sitx, gradation_colors, log, gradation_range_labels)
        project_mpt = result_sitx.with_suffix('.mpt')
        opened_project = False
        try:
            hsite = sitapi.mapOpenSiteForMapUn(hmap, mapsyst.WTEXT(str(result_sitx)), 0)
            if _hmap_as_int(hsite) != 0:
                saved = int(mapapi.mapSaveProjectUn(hmap, mapsyst.WTEXT(str(project_mpt))) or 0)
                if saved > 0 and project_mpt.is_file():
                    hprj = mapapi.mapOpenProjectUn(mapsyst.WTEXT(str(project_mpt)))
                    if _hmap_as_int(hprj) != 0:
                        opened_project = True
                        _map_set_real_show_scale(hprj)
                        _map_save_project_scale(hprj, project_mpt)
                        if _open_document_in_panorama_and_refresh(project_mpt):
                            pass
        except Exception:
            pass
        if not opened_project and project_mpt.is_file():
            try:
                hprj = mapapi.mapOpenProjectUn(mapsyst.WTEXT(str(project_mpt)))
                if _hmap_as_int(hprj) != 0:
                    opened_project = True
                    _map_set_real_show_scale(hprj)
                    _map_save_project_scale(hprj, project_mpt)
                    if _open_document_in_panorama_and_refresh(project_mpt):
                        pass
            except Exception:
                pass
        if not opened_project and project_mpt.is_file():
            try:
                hprj2 = mapapi.mapOpenAnyDataPro(mapsyst.WTEXT(str(project_mpt)), 0, ctypes.byref(err), empty_pass, 0)
                if _hmap_as_int(hprj2) != 0:
                    opened_project = True
                    _map_set_real_show_scale(hprj2)
                    _map_save_project_scale(hprj2, project_mpt)
                    if _open_document_in_panorama_and_refresh(project_mpt):
                        pass
            except Exception:
                pass
        if not opened_project:
            hres = mapapi.mapOpenAnyDataPro(mapsyst.WTEXT(str(result_sitx)), 0, ctypes.byref(err), empty_pass, 0)
            if _hmap_as_int(hres) == 0:
                pass
            else:
                _map_set_real_show_scale(hres)
                if _open_document_in_panorama_and_refresh(result_sitx):
                    pass
        return (created, result_sitx, project_mpt)
    finally:
        try:
            mapapi.mapCloseData(hmap)
        except Exception:
            pass

def _parse_float_guess(text: str) -> Optional[float]:
    """Преобразование текста в число"""
    s = (text or '').strip()
    if not s:
        return None
    s = s.replace('\xa0', ' ').replace(' ', '')
    s = s.replace(',', '.')
    s = re.sub('[^0-9.\\-+eE]', '', s)
    if not s:
        return None
    try:
        return float(s)
    except Exception:
        return None

class RosstatDialog:
    """Фиксированная высота блока предпросмотра (не меняется при открытии списка типов)"""
    PREVIEW_BLOCK_HEIGHT_PX = 308
    PREVIEW_TEXT_LINES = 12

    def __init__(self, root: tk.Tk, document_hmap=None) -> None:
        """Инициализация диалога"""
        setup_script_logging()
        self.root = root
        self.root.report_callback_exception = self._tk_callback_exception
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        self.root.title(tr('stats_title_base'))
        sw = max(1, self.root.winfo_screenwidth())
        sh = max(1, self.root.winfo_screenheight())
        col_w = max(320, sw // 3) + 50
        col_h_full = max(400, sh - 72)
        col_h = max(240, col_h_full // 2)
        gx = max(0, (sw - col_w) // 2)
        gy = max(0, (sh - col_h) // 2)
        self.root.geometry(f'{col_w}x{col_h}+{gx}+{gy}')
        self.root.minsize(col_w, col_h)
        self.root.resizable(True, True)
        self.root.bind('<Configure>', self._on_root_configure, add='+')
        ensure_dirs()
        self.document_hmap = document_hmap
        self.selected_material = tk.StringVar(value=MATERIAL_TYPES[0].name)
        self.preview_title_text = tk.StringVar(value=tr('preview_title', name=_preview_headline_name(MATERIAL_TYPES[0].name, table_path_for_material(MATERIAL_TYPES[0].name))))
        self.table_period_var = tk.StringVar(value='')
        self._last_thematic_mpt: Optional[Path] = None
        self.material_enabled = False
        self.material_dropdown_expanded = False
        self.selector_labels = build_selector_labels()
        self.material_visible_count = 7
        self.material_offset = 0
        self.material_row_var = tk.IntVar(value=0)
        self.material_row_to_index: Dict[int, int] = {}
        self.preview_rows = 10
        self.preview_mode_var = tk.StringVar(value='full')
        self.value_column_var = tk.StringVar(value=str(_value_column_min_1based()))
        self._value_col_spin_bounds: Optional[Tuple[int, int]] = None
        self.min_value_var = tk.StringVar(value='')
        self.max_value_var = tk.StringVar(value='')
        self.min_color_int = 9498256
        self.max_color_int = 16711680
        self.dependencies_ready = False
        self.dependencies_missing: List[str] = []
        self.is_refreshing_data = False
        self._build_ui()
        self.root.after_idle(self._sync_dialog_wraplength)
        self.root.after_idle(self._fit_window_height_to_content)
        self._refresh_dependency_state()
        self._init_from_cached_data()
        self._update_execute_button_state()
        self._refresh_stats_headline()
        self._update_value_column_hints()

    def _stats_file_count(self) -> int:
        try:
            idx = get_excel_code_index()
            if idx:
                return len(idx)
        except Exception:
            pass
        return self._existing_tables_count()

    def _refresh_stats_headline(self) -> None:
        meta = load_portal_fetch_meta()
        fetched: Optional[str] = None
        if meta and isinstance(meta.get('fetched_at'), str):
            fetched = meta['fetched_at']
        n = self._stats_file_count()
        if n <= 0 and meta is not None:
            stored = meta.get('file_count')
            if isinstance(stored, (int, float)) and int(stored) > 0:
                n = int(stored)
        headline = format_statistics_headline(n, fetched)
        hl = getattr(self, 'stats_headline_label', None)
        if hl is not None:
            try:
                hl.configure(text=headline)
            except Exception:
                pass
        try:
            self.root.title(headline)
        except Exception:
            pass

    def _sync_dialog_wraplength(self) -> None:
        """Синхронизация ширины текста в заголовках и кнопках"""
        try:
            w = self.root.winfo_width()
            if w <= 1:
                return
            hl = getattr(self, 'stats_headline_label', None)
            if hl is not None:
                hl.configure(wraplength=max(160, w - 100))
            mtl = getattr(self, 'material_type_label', None)
            if mtl is not None:
                mtl.configure(wraplength=max(200, w - 40))
            ptl = getattr(self, 'preview_title_label', None)
            if ptl is not None:
                ptl.configure(wraplength=max(200, w - 40))
            wrap_rb = max(160, w - 88)
            for rb in getattr(self, 'material_row_buttons', None) or []:
                rb.configure(wraplength=wrap_rb)
        except Exception:
            pass

    def _on_root_configure(self, event) -> None:
        """Обработка изменения размеров окна"""
        if event.widget is not self.root:
            return
        self._sync_dialog_wraplength()

    def _fit_window_height_to_content(self) -> None:
        """Подогнать высоту окна под содержимое (список из 7 строк открыт или свёрнут); ширина не уменьшается"""
        try:
            self.root.update_idletasks()
            req_h = int(self.root.winfo_reqheight())
            w = max(int(self.root.winfo_width()), int(self.root.winfo_reqwidth()))
            sw = max(1, int(self.root.winfo_screenwidth()))
            sh = max(1, int(self.root.winfo_screenheight()))
            m_top = 8
            m_bot = 48
            if not getattr(self, '_rosstat_window_placed', False):
                x = max(0, (sw - w) // 2)
                slack = max(0, sh - req_h)
                y = max(m_top, slack // 3)
                self._rosstat_window_placed = True
            else:
                x = int(self.root.winfo_x())
                y = int(self.root.winfo_y())
            if x + w > sw - 8:
                x = max(0, sw - w - 8)
            if y + req_h > sh - m_bot:
                y = max(m_top, sh - req_h - m_bot)
            if y < m_top:
                y = m_top
            self.root.geometry(f'{w}x{req_h}+{x}+{y}')
        except Exception:
            pass

    def _clamp_value_column_to_table(self, ncols: int) -> int:
        """Привести номер столбца значений к допустимому диапазону [min..ncols], min — после столбца связи"""
        vmin = _value_column_min_1based()
        vmax = max(vmin, ncols)
        try:
            vc = int(self.value_column_var.get())
        except Exception:
            vc = vmin
        if vc < vmin:
            vc = vmin
        if vc > vmax:
            vc = vmax
        self.value_column_var.set(str(vc))
        return vc

    def _apply_table_period_caption(self, table_path: Path, vc: int) -> None:
        """Применение периода из таблицы к заголовку"""
        if not table_path.is_file():
            self.table_period_var.set('')
            return
        per = _thematic_period_for_map_name(table_path, vc)
        cap = format_thematic_period_caption(per) if per.trusted else ''
        self.table_period_var.set(cap if cap else '—')

    def _update_value_column_hints(self) -> None:
        """Обновление подсказок для выбора столбца значений"""
        selected_name = self.selected_material.get()
        table_path = table_path_for_material(selected_name)
        if not table_path.is_file():
            self._value_col_spin_bounds = None
            try:
                self.value_col_count_label.configure(text='')
            except Exception:
                pass
            self.table_period_var.set('')
            try:
                self.value_col_spin.configure(from_=_value_column_min_1based(), to=999)
            except Exception:
                pass
            return
        ncols = _table_max_column_count(table_path)
        vmin = _value_column_min_1based()
        vmax = max(vmin, ncols)
        try:
            self.value_col_count_label.configure(text=tr('label_of_n_columns', n=ncols))
        except Exception:
            pass
        bounds = (vmin, vmax)
        if self._value_col_spin_bounds != bounds:
            self._value_col_spin_bounds = bounds
            try:
                self.value_col_spin.configure(from_=vmin, to=vmax)
            except Exception:
                pass
        vc = self._clamp_value_column_to_table(ncols)
        self._apply_table_period_caption(table_path, vc)

    def _existing_tables_count(self) -> int:
        """Определение количества существующих таблиц"""
        cnt = 0
        for item in MATERIAL_TYPES:
            if table_path_for_material(item.name).is_file():
                cnt += 1
        return cnt

    def _init_from_cached_data(self) -> None:
        """Инициализация данных из кэша"""
        ready = self._existing_tables_count()
        if ready <= 0:
            return
        self.material_enabled = True
        self.material_dropdown_btn.configure(state='normal')
        self._update_preview_for_selected()
        self._recalc_min_max_from_selected_table()
        _refresh_thematic_region_title_keys_if_default(table_path_for_material(self.selected_material.get()))
        self._update_value_column_hints()
        self._update_execute_button_state()

    def _refresh_dependency_state(self) -> None:
        """Обновление состояния зависимостей"""
        try:
            idx = get_excel_code_index()
            has_xls = any((str(p).lower().endswith('.xls') for p in idx.values()))
            if not has_xls:
                self.dependencies_missing = []
                self.dependencies_ready = True
                return
            python_exe = resolve_python_executable()
            missing: List[str] = []
            if not _python_module_available(python_exe, 'xlrd'):
                missing.append('xlrd')
            self.dependencies_missing = missing
            self.dependencies_ready = len(missing) == 0
        except Exception:
            self.dependencies_missing = ['python']
            self.dependencies_ready = False

    def _tables_ready(self) -> bool:
        """Проверка готовности таблиц"""
        return self._existing_tables_count() > 0

    def _update_execute_button_state(self) -> None:
        """Обновление состояния кнопки выполнения"""
        tables_ok = self._tables_ready()
        deps_ok = self.dependencies_ready
        state = 'normal' if tables_ok and deps_ok and (not self.is_refreshing_data) else 'disabled'
        refresh_state = 'disabled' if self.is_refreshing_data else 'normal'
        try:
            self.execute_btn.configure(state=state)
        except Exception:
            pass
        try:
            self.refresh_stats_btn.configure(state=refresh_state)
        except Exception:
            pass
        try:
            self.refresh_stats_btn.configure(text=tr('btn_refresh') if self._tables_ready() else tr('btn_get'))
        except Exception:
            pass

    def _build_ui(self) -> None:
        """Построение интерфейса"""
        header_bar = ttk.Frame(self.root, padding=(12, 10, 12, 0))
        header_bar.pack(fill=tk.X)
        header_row = ttk.Frame(header_bar)
        header_row.pack(fill=tk.X)
        self.stats_headline_label = ttk.Label(header_row, text=tr('stats_title_base'), justify=tk.LEFT, anchor='w')
        self.stats_headline_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.refresh_stats_btn = ttk.Button(header_row, text=tr('btn_get'), command=self.on_fetch_data)
        self.refresh_stats_btn.pack(side=tk.RIGHT, padx=(8, 0))
        footer = ttk.Frame(self.root, padding=(12, 6, 12, 10))
        param_frame = ttk.LabelFrame(footer, text=tr('param_frame_title'), padding=(8, 6))
        param_frame.pack(fill=tk.X)
        ttk.Label(param_frame, text=tr('label_values_in_column')).grid(row=0, column=0, sticky='w')
        self.value_col_spin = tk.Spinbox(param_frame, from_=_value_column_min_1based(), to=999, textvariable=self.value_column_var, width=5, command=self._on_value_column_changed)
        self.value_col_spin.grid(row=0, column=1, sticky='w', padx=(6, 4))
        self.value_col_spin.bind('<FocusOut>', lambda _e: self._on_value_column_changed())
        self.value_col_spin.bind('<Return>', lambda _e: self._on_value_column_changed())
        self.value_col_count_label = ttk.Label(param_frame, text='')
        self.value_col_count_label.grid(row=0, column=2, sticky='w', padx=(0, 8))
        ttk.Label(param_frame, textvariable=self.table_period_var).grid(row=0, column=3, sticky='w', padx=(6, 0))
        ttk.Label(param_frame, text=tr('label_min')).grid(row=1, column=0, sticky='w')
        ttk.Entry(param_frame, textvariable=self.min_value_var, width=14).grid(row=1, column=1, sticky='w', padx=(6, 12))
        self.min_color_btn = tk.Button(param_frame, text='', width=4, command=self._pick_min_color)
        self.min_color_btn.grid(row=1, column=2, sticky='w')
        ttk.Label(param_frame, text=tr('label_max')).grid(row=2, column=0, sticky='w')
        ttk.Entry(param_frame, textvariable=self.max_value_var, width=14).grid(row=2, column=1, sticky='w', padx=(6, 12))
        self.max_color_btn = tk.Button(param_frame, text='', width=4, command=self._pick_max_color)
        self.max_color_btn.grid(row=2, column=2, sticky='w')
        self._refresh_color_buttons()
        btn_row = ttk.Frame(footer)
        btn_row.pack(fill=tk.X, pady=(8, 0))
        self.execute_btn = ttk.Button(btn_row, text=tr('btn_execute'), command=self.on_execute, state='disabled')
        self.execute_btn.pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(btn_row, text=tr('btn_exit'), command=self.on_close).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(btn_row, text=tr('btn_help'), command=self.on_help).pack(side=tk.LEFT)
        self._footer_frame = footer
        self._main_center = ttk.Frame(self.root)
        self._main_center.grid_columnconfigure(0, weight=1)
        self._main_center.grid_rowconfigure(0, weight=0, minsize=0)
        self._main_center.grid_rowconfigure(1, weight=0, minsize=self.PREVIEW_BLOCK_HEIGHT_PX)
        upper_pw = ttk.Frame(self._main_center)
        upper_pw.grid(row=0, column=0, sticky='ew')
        lower_pw = tk.Frame(self._main_center, height=self.PREVIEW_BLOCK_HEIGHT_PX, highlightthickness=0, borderwidth=0)
        try:
            lower_pw.configure(bg=self.root.cget('bg'))
        except Exception:
            pass
        lower_pw.grid(row=1, column=0, sticky='ew')
        try:
            lower_pw.grid_propagate(False)
        except Exception:
            pass
        top_frame = ttk.Frame(upper_pw, padding=12)
        top_frame.pack(fill=tk.X, anchor=tk.N)
        self.material_type_label = ttk.Label(top_frame, text=tr('label_material_type'), justify=tk.LEFT, anchor='w')
        self.material_type_label.pack(fill=tk.X, anchor=tk.W, pady=(0, 4))
        selector_frame = ttk.Frame(top_frame)
        selector_frame.pack(fill=tk.X)
        self.material_entry = ttk.Entry(selector_frame, textvariable=self.selected_material, state='readonly')
        self.material_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.material_dropdown_btn = ttk.Button(selector_frame, text='▼', width=3, command=self._toggle_material_popup, state='disabled')
        self.material_dropdown_btn.pack(side=tk.LEFT, padx=(4, 0))
        self.material_inline_frame = ttk.Frame(top_frame)
        self.material_rows_frame = ttk.Frame(self.material_inline_frame)
        self.material_rows_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.material_nav_frame = ttk.Frame(self.material_inline_frame)
        self.material_nav_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(4, 0))
        self.material_up_btn = ttk.Button(self.material_nav_frame, text='▲', width=3, command=self._scroll_material_up)
        self.material_up_btn.pack(side=tk.TOP, pady=(0, 2))
        self.material_down_btn = ttk.Button(self.material_nav_frame, text='▼', width=3, command=self._scroll_material_down)
        self.material_down_btn.pack(side=tk.TOP)
        self.material_row_buttons: List[tk.Radiobutton] = []
        for row_idx in range(self.material_visible_count):
            rb = tk.Radiobutton(self.material_rows_frame, text='', anchor='w', justify=tk.LEFT, wraplength=400, variable=self.material_row_var, value=row_idx, command=self._on_material_popup_pick)
            rb.pack(fill=tk.X, anchor='w')
            rb.bind('<MouseWheel>', self._on_material_mousewheel)
            self.material_row_buttons.append(rb)
        preview_frame = ttk.Frame(lower_pw, padding=(12, 0, 12, 4))
        preview_frame.pack(fill=tk.BOTH, expand=True)
        self.preview_title_label = ttk.Label(preview_frame, textvariable=self.preview_title_text, justify=tk.LEFT, anchor='w')
        self.preview_title_label.pack(anchor=tk.W)
        preview_mode_row = ttk.Frame(preview_frame)
        preview_mode_row.pack(fill=tk.X, anchor=tk.W, pady=(2, 4))
        ttk.Radiobutton(preview_mode_row, text=tr('preview_mode_full'), variable=self.preview_mode_var, value='full', command=self._on_preview_mode_changed).pack(side=tk.LEFT, padx=(0, 14))
        ttk.Radiobutton(preview_mode_row, text=tr('preview_mode_value_column'), variable=self.preview_mode_var, value='column', command=self._on_preview_mode_changed).pack(side=tk.LEFT)
        self.preview_text = tk.Text(preview_frame, height=self.PREVIEW_TEXT_LINES, wrap='none')
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        self.preview_xscale = ttk.Scale(preview_frame, orient=tk.HORIZONTAL, from_=0.0, to=1.0, command=self._on_preview_xscale)
        self.preview_xscale_visible = False
        self.preview_text.configure(state='disabled')
        self._set_preview_text(tr('preview_not_loaded'))
        self._footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self._main_center.pack(side=tk.TOP, fill=tk.X, expand=False)

    def _set_preview_text(self, text: str, show_scroll: bool=False) -> None:
        """Установка текста для предварительного просмотра"""
        if show_scroll and (not self.preview_xscale_visible):
            self.preview_xscale.pack(fill=tk.X, side=tk.BOTTOM)
            self.preview_xscale_visible = True
        if not show_scroll and self.preview_xscale_visible:
            self.preview_xscale.pack_forget()
            self.preview_xscale_visible = False
        self.preview_text.configure(state='normal')
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert('1.0', text)
        self.preview_text.xview_moveto(0.0)
        self.preview_xscale.set(0.0)
        self.preview_text.configure(state='disabled')

    def _refresh_color_buttons(self) -> None:
        """Обновление цветов кнопок выбора цветов"""
        self.min_color_btn.configure(bg=f'#{self.min_color_int & 16777215:06x}')
        self.max_color_btn.configure(bg=f'#{self.max_color_int & 16777215:06x}')

    def _pick_min_color(self) -> None:
        """Выбор цвета для минимального значения"""
        rgb, _hex = colorchooser.askcolor(color=f'#{self.min_color_int & 16777215:06x}', title=tr('color_min_title'))
        if rgb:
            r, g, b = [int(v) for v in rgb]
            self.min_color_int = r << 16 | g << 8 | b
            self._refresh_color_buttons()

    def _pick_max_color(self) -> None:
        """Выбор цвета для максимального значения"""
        rgb, _hex = colorchooser.askcolor(color=f'#{self.max_color_int & 16777215:06x}', title=tr('color_max_title'))
        if rgb:
            r, g, b = [int(v) for v in rgb]
            self.max_color_int = r << 16 | g << 8 | b
            self._refresh_color_buttons()

    def _on_value_column_changed(self) -> None:
        """Обработка изменения индекса столбца значений"""
        selected_name = self.selected_material.get()
        table_path = table_path_for_material(selected_name)
        if table_path.is_file():
            ncols = _table_max_column_count(table_path)
            vc = self._clamp_value_column_to_table(ncols)
            self._apply_table_period_caption(table_path, vc)
        else:
            self.table_period_var.set('')
        self._recalc_min_max_from_selected_table()
        self._update_preview_for_selected()

    def _on_preview_mode_changed(self) -> None:
        """Переключение режима предпросмотра (вся таблица / столбец значений)"""
        self._update_preview_for_selected()

    def _preview_text_full_table(self, shown_rows: List[List[Any]], table_path: Path) -> Tuple[str, bool]:
        """Текст предпросмотра всех колонок и нужна ли горизонтальная прокрутка"""
        ncols = max((len(r) for r in shown_rows), default=0)
        ci = _thematic_connect_col_index()
        period_lbls = _preview_sheet_column_period_labels(table_path, ncols)
        col_labels: List[str] = []
        for c in range(ncols):
            if c == ci:
                col_labels.append(tr('preview_col_subject_name'))
            else:
                pl = period_lbls[c] if c < len(period_lbls) else ''
                col_labels.append(pl if pl else str(c + 1))
        widths: List[int] = []
        for cidx in range(ncols):
            w = len(col_labels[cidx])
            for row in shown_rows:
                cell = str(row[cidx] if cidx < len(row) else '')
                w = max(w, len(cell))
            widths.append(w)
        lines: List[str] = []
        head_pad = [col_labels[cidx].ljust(widths[cidx]) for cidx in range(ncols)]
        lines.append(' | '.join(head_pad).rstrip())
        sep = '-+-'.join(('-' * w for w in widths))
        lines.append(sep)
        for row in shown_rows:
            padded = []
            for cidx, width in enumerate(widths):
                cell = str(row[cidx] if cidx < len(row) else '')
                padded.append(cell.ljust(width))
            lines.append(' | '.join(padded).rstrip())
        if widths:
            lines.append('')
            num_cells = []
            for cidx, width in enumerate(widths, start=1):
                num_cells.append(str(cidx).ljust(width))
            lines.append(' | '.join(num_cells).rstrip())
            lines.append(tr('preview_col_numbers_hint'))
        wide = any((len(ln) > 96 for ln in lines))
        return ('\n'.join(lines), wide)

    def _preview_text_value_column(self, shown_rows: List[List[Any]], value_col_1based: int, table_path: Path) -> Tuple[str, bool]:
        """Предпросмотр: столбец связи (как в тематике) и выбранный столбец значений"""
        try:
            vc = int(value_col_1based) - 1
        except Exception:
            return (tr('preview_column_oob', col=value_col_1based, n=0), False)
        ci = _thematic_connect_col_index()
        ncols = max((len(r) for r in shown_rows), default=0)
        if vc < 0 or vc >= ncols:
            return (tr('preview_column_oob', col=value_col_1based, n=ncols), False)
        period_lbls = _preview_sheet_column_period_labels(table_path, ncols)
        val_hdr = period_lbls[vc] if vc < len(period_lbls) else ''
        if not val_hdr:
            _, vh = _table_header_row_for_thematic(table_path, value_col_1based)
            val_hdr = (vh or '').strip() or str(value_col_1based)
        h0 = tr('preview_col_subject_name')
        pairs: List[Tuple[str, str]] = []
        for row in shown_rows:
            a = str(row[ci] if ci < len(row) else '').strip()
            b = str(row[vc] if vc < len(row) else '').strip()
            pairs.append((a, b))
        w0 = max(len(h0), max((len(p[0]) for p in pairs), default=0))
        w1 = max(len(val_hdr), max((len(p[1]) for p in pairs), default=0))
        lines: List[str] = []
        lines.append(f'{h0.ljust(w0)} | {val_hdr.ljust(w1)}'.rstrip())
        lines.append(f'{"-" * w0}-+-{"-" * w1}')
        for a, b in pairs:
            lines.append(f'{a.ljust(w0)} | {b.ljust(w1)}'.rstrip())
        wide = (w0 + w1 + 3) > 96
        return ('\n'.join(lines), wide)

    def _recalc_min_max_from_selected_table(self) -> None:
        """Пересчет минимального и максимального значений для выбранной таблицы"""
        selected_name = self.selected_material.get()
        table_path = table_path_for_material(selected_name)
        if not table_path.is_file():
            return
        try:
            col_idx = int(self.value_column_var.get()) - 1
        except Exception:
            return
        if col_idx < 0:
            return
        min_v: Optional[float] = None
        max_v: Optional[float] = None
        rows = _read_table_rows(table_path)
        for ridx, row in enumerate(rows):
            if ridx < 4:
                continue
            if col_idx >= len(row):
                continue
            link_text = _row_link_text_for_thematic(row)
            if not link_text:
                continue
            if _is_excluded_federal_row(link_text) or _is_excluded_federal_district_row(link_text):
                continue
            val = _parse_float_guess(row[col_idx])
            if val is None:
                continue
            min_v = val if min_v is None else min(min_v, val)
            max_v = val if max_v is None else max(max_v, val)
        if min_v is not None and max_v is not None:
            self.min_value_var.set(f'{min_v:g}')
            self.max_value_var.set(f'{max_v:g}')

    def _on_preview_xscale(self, value: str) -> None:
        """Горизонтальная прокрутка предпросмотра (ползунок)"""
        try:
            pos = float(value)
        except Exception:
            pos = 0.0
        if pos < 0.0:
            pos = 0.0
        if pos > 1.0:
            pos = 1.0
        self.preview_text.xview_moveto(pos)

    def _update_preview_for_selected(self) -> None:
        """Обновление предварительного просмотра для выбранной таблицы"""
        selected_name = self.selected_material.get()
        table_path = table_path_for_material(selected_name)
        self.preview_title_text.set(tr('preview_title', name=_preview_headline_name(selected_name, table_path)))
        self.root.after_idle(self._sync_dialog_wraplength)
        if not table_path.is_file():
            self._set_preview_text(tr('preview_table_not_found', path=table_path))
            return
        try:
            read_cap = max(400, self.preview_rows * 40)
            rows = _read_table_rows(table_path, limit_rows=read_cap)
            if not rows:
                self._set_preview_text(tr('preview_empty', path=table_path), show_scroll=False)
                return
            shown_rows = _preview_subject_rows_slice(rows, self.preview_rows)
            if not shown_rows:
                self._set_preview_text(tr('preview_no_subject_rows'), show_scroll=False)
                return
            if self.preview_mode_var.get() == 'column':
                try:
                    vcol = int(self.value_column_var.get())
                except Exception:
                    vcol = 2
                text, wide = self._preview_text_value_column(shown_rows, vcol, table_path)
                self._set_preview_text(text, show_scroll=wide)
            else:
                text, wide = self._preview_text_full_table(shown_rows, table_path)
                self._set_preview_text(text, show_scroll=wide)
        except Exception as exc:
            self._set_preview_text(tr('preview_read_error', path=table_path, err=exc), show_scroll=False)

    def on_fetch_data(self) -> None:
        """Загрузка данных из архива"""
        try:
            self.is_refreshing_data = True
            self._update_execute_button_state()
            self.root.update_idletasks()
            archive_url, ssl_note_page = find_latest_archive_url()
            self.root.update_idletasks()
            archive_path, ssl_note_file = download_archive(archive_url)
            self.root.update_idletasks()
            try:
                python_exe = resolve_python_executable()
                missing, dep_notice = _build_dependency_notice(python_exe)
                if missing:
                    for pkg in missing:
                        self.root.update_idletasks()
                        _install_python_package_silent(python_exe, pkg)
                    missing, dep_notice = _build_dependency_notice(python_exe)
                if missing:
                    self.dependencies_missing = missing
                    self.dependencies_ready = False
                    self.root.update_idletasks()
                    messagebox.showwarning(tr('dlg_deps_title'), dep_notice)
                else:
                    self.dependencies_missing = []
                    self.dependencies_ready = True
            except Exception:
                self.dependencies_missing = ['python']
                self.dependencies_ready = False
            extract_rar(archive_path)
            roots = auto_detect_excel_roots()
            set_excel_search_roots(roots)
            excel_index = get_excel_code_index()
            if not excel_index:
                roots_text = '\n'.join((str(r) for r in roots[:10]))
                raise RuntimeError(f'После распаковки не найдено ни одного файла .xlsx/.xls.\nПроверены каталоги:\n{roots_text}\nПроверьте содержимое архива или способ распаковки')
            self.root.update_idletasks()
            self.material_enabled = True
            self.material_dropdown_btn.configure(state='normal')
            self._refresh_dependency_state()
            self._update_preview_for_selected()
            self._recalc_min_max_from_selected_table()
            _refresh_thematic_region_title_keys_if_default(table_path_for_material(self.selected_material.get()))
            self._update_value_column_hints()
            self._update_execute_button_state()
            save_portal_fetch_meta(len(excel_index))
            self._refresh_stats_headline()
        except HTTPError as exc:
            detail = str(exc.reason).strip() if getattr(exc, 'reason', None) else str(exc)
            messagebox.showerror(tr('dlg_error'), tr('http_portal_transient', code=int(exc.code), detail=detail))
        except Exception as exc:
            messagebox.showerror(tr('dlg_error'), str(exc))
        finally:
            self.is_refreshing_data = False
            self._update_execute_button_state()

    def on_execute(self) -> None:
        """Построение тематической карты"""
        try:
            self._refresh_dependency_state()
            self._update_execute_button_state()
            if not self.dependencies_ready:
                raise RuntimeError('отсутствуют зависимости Python (' + ', '.join(self.dependencies_missing) + ').')
            if not self._tables_ready():
                raise RuntimeError('таблицы еще не распакованы')
            selected_name = self.selected_material.get()
            selected_code = DISPLAY_TO_CODE.get(selected_name, 'UNKNOWN')
            table_file = table_path_for_material(selected_name)
            if not table_file.is_file():
                raise RuntimeError(f'Таблица для выбранного типа данных не найдена: {table_file}')
            value_col = self._clamp_value_column_to_table(_table_max_column_count(table_file))
            min_value = _parse_float_guess(self.min_value_var.get())
            max_value = _parse_float_guess(self.max_value_var.get())
            if min_value is None or max_value is None:
                raise RuntimeError('Минимум/максимум не заданы или не являются числом')
            if max_value < min_value:
                raise RuntimeError('Максимум меньше минимума')
            out_stem = build_thematic_output_stem(selected_code, selected_name, value_col, table_file)
            rc, result_sitx, project_mpt = run_thematic_with_mathapi(table_path=table_file, report_code=selected_code, value_col=value_col, min_value=min_value, max_value=max_value, color_min=self.min_color_int, color_max=self.max_color_int, previous_mpt=self._last_thematic_mpt, output_stem=out_stem)
            if rc <= 0:
                raise RuntimeError(f'mathCreateThematicMap завершилась с кодом {rc}')
            if project_mpt.is_file():
                self._last_thematic_mpt = project_mpt
            try:
                self.root.deiconify()
                self.root.lift()
                self.root.update_idletasks()
            except Exception:
                pass
        except Exception as exc:
            messagebox.showerror(tr('dlg_execute_error'), str(exc))

    def on_help(self) -> None:
        """Открытие справки"""
        webbrowser.open(_HELP_URL, new=2)

    def _toggle_material_popup(self) -> None:
        """Переключение состояния выпадающего списка типов данных"""
        if self.material_dropdown_expanded:
            self._close_material_popup()
        else:
            self._open_material_popup()

    def _open_material_popup(self) -> None:
        """Открытие выпадающего списка типов данных"""
        if not self.material_enabled:
            return
        current = self.selected_material.get()
        values = [item.name for item in MATERIAL_TYPES]
        if current in values:
            idx = values.index(current)
            self.material_offset = max(0, min(idx, max(0, len(values) - self.material_visible_count)))
        else:
            self.material_offset = 0
        self._refresh_material_rows(current)
        self.material_inline_frame.pack(fill=tk.X, pady=(4, 0))
        self.root.after_idle(self._sync_dialog_wraplength)
        self.root.after_idle(self._fit_window_height_to_content)
        self.material_dropdown_expanded = True
        self.material_dropdown_btn.configure(text='▲')
        if self.material_row_buttons:
            self.material_row_buttons[0].focus_set()

    def _refresh_material_rows(self, current_name: str) -> None:
        """Обновление строк выпадающего списка типов данных"""
        total = len(MATERIAL_TYPES)
        self.material_row_to_index = {}
        selected_row = 0
        for row_idx in range(self.material_visible_count):
            global_idx = self.material_offset + row_idx
            rb = self.material_row_buttons[row_idx]
            if global_idx < total:
                label = self.selector_labels[global_idx]
                rb.configure(text=label, state='normal')
                self.material_row_to_index[row_idx] = global_idx
                if MATERIAL_TYPES[global_idx].name == current_name:
                    selected_row = row_idx
            else:
                rb.configure(text='', state='disabled')
        self.material_row_var.set(selected_row)

    def _scroll_material_up(self) -> None:
        """Скроллинг выпадающего списка типов данных вверх"""
        self._scroll_material_by(-1)

    def _scroll_material_down(self) -> None:
        """Скроллинг выпадающего списка типов данных вниз"""
        self._scroll_material_by(1)

    def _on_material_mousewheel(self, event) -> None:
        """Обработка колеса мыши для выпадающего списка типов данных"""
        delta = -1 if event.delta > 0 else 1
        self._scroll_material_by(delta)

    def _scroll_material_by(self, delta: int) -> None:
        """Скроллинг выпадающего списка типов данных на заданное количество строк"""
        total = len(MATERIAL_TYPES)
        max_offset = max(0, total - self.material_visible_count)
        new_offset = max(0, min(max_offset, self.material_offset + delta))
        if new_offset == self.material_offset:
            return
        self.material_offset = new_offset
        self._refresh_material_rows(self.selected_material.get())

    def _on_material_popup_pick(self, _event=None) -> None:
        """Выбор типа данных из выпадающего списка"""
        row_idx = int(self.material_row_var.get())
        if row_idx not in self.material_row_to_index:
            return
        idx = self.material_row_to_index[row_idx]
        full_name = MATERIAL_TYPES[idx].name
        self.selected_material.set(full_name)
        self._update_preview_for_selected()
        self._recalc_min_max_from_selected_table()
        self._update_value_column_hints()
        self._close_material_popup()

    def _close_material_popup(self) -> None:
        """Закрытие выпадающего списка типов данных"""
        self.material_inline_frame.pack_forget()
        self.material_dropdown_expanded = False
        self.material_dropdown_btn.configure(text='▼')
        self.root.after_idle(self._fit_window_height_to_content)

    def _tk_callback_exception(self, exc, val, tb) -> None:
        """Обработка исключений в диалоге"""
        messagebox.showerror(tr('dlg_tk_error'), f'{exc.__name__}: {val}')

    def on_close(self) -> None:
        self.root.destroy()

def _configure_ttk_theme(root: tk.Tk) -> None:
    """Настройка темы"""
    style = ttk.Style(root)
    if 'vista' in style.theme_names():
        style.theme_use('vista')

def main() -> int:
    setup_script_logging()
    root = tk.Tk()
    _configure_ttk_theme(root)
    RosstatDialog(root, document_hmap=None)
    root.mainloop()
    return 0
if __name__ == '__main__':
    sys.exit(main())

def run_rosstat_monitor(document_hmap) -> float:
    """Запуск диалога мониторинга Росстата"""
    setup_script_logging()
    try:
        ensure_dirs()
        root = tk.Tk()
        _configure_ttk_theme(root)
        RosstatDialog(root, document_hmap=document_hmap)
        root.mainloop()
        return 1.0
    except Exception as exc:
        err = str(exc)
        if mapapi is not None and mapsyst is not None:
            try:
                mapapi.mapShowMessage(mapsyst.WTEXT(err), mapsyst.WTEXT(tr('app_short_name')))
            except Exception:
                pass
        return 0.0