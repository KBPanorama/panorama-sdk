from tkinter import filedialog, ttk
import os
import re
import sys
from typing import Dict, List, Optional, Tuple
import mapsyst
import maptype
import rscapi
import mapapi

# -------------------------
# Диагностический протокол
# -------------------------
def write_diag_pair(msg_before: str, msg_after: str, msg_type: Optional[int] = None) -> None:
	"""Пишет в диагностический протокол запись вида:
	TPythonScript::RscToSql(): <msg_before>, <msg_after/param>"""
	try:
		if not mapapi.mapIsDiagnostics():
			return
		mtype = msg_type if isinstance(msg_type, int) else getattr(maptype, "MT_INFO", 0)
		prefix = "TPythonScript::RscToSql(): "
		mapapi.mapWriteToDiagnosticsLog(mapsyst.WTEXT(prefix + msg_before), mapsyst.WTEXT(msg_after or ""), mtype)
	except Exception:
		pass

# -----------------------
# Определение локализации
# -----------------------
def _detect_lang() -> str:
	"""Определяет язык интерфейса ГИС Панорама"""
	try:
		code = mapapi.mapGetMapAccessLanguage()
		if code == getattr(maptype, "ML_RUSSIAN", 2):
			return "ru"
		if code == getattr(maptype, "ML_ENGLISH", 1):
			return "en"
		return "en"
	except Exception:
		return "ru"

_LANG = _detect_lang()

_STR = {
	"ru": {
		"title": "Сформировать SQL-структуру базы данных по классификатору",
		"label_classifier": "Классификатор карты:",
		"label_sql": "Файл запросов SQL:",
		"browse_classifier_title": "Выберите классификатор",
		"browse_sql_title": "Сохранить как",
		"classifier_ft_desc": "Классификатор карты",
		"sql_ft_desc": "Язык структурированных запросов SQL",
		"warn": "Обработчик ошибок",
		"no_classifier": "Не выбран файл классификатора",
		"no_sql": "Не выбран файл для сохранения SQL",
		"no_write_perm": "Нет прав записи в выбранную папку — выберите другую директорию",
		"checkbox_log": "Формировать таблицу и триггеры для ведения журнала изменений",
		"checkbox_single_table": "Формировать одну таблицу по классификатору",
		"btn_run": "Выполнить",
		"btn_cancel": "Отменить",
		"btn_abort": "Прервать",
		"btn_help": "Помощь",
		"progress_read": "Чтение семантик",
		"progress_layers": "Формирование таблиц слоёв: {name}",
		"progress_single_table": "Формирование единой таблицы",
		"phase_codes": "коды",
		"phase_names": "имена",
		"phase_keys": "ключи",
		"phase_units": "единицы",
		"phase_types": "типы",
		"final_title": "Обработано семантик: {n}",
		"final_msg": "Сформирован файл SQL: {path}",
		"help_url": "https://help.gisserver.ru/v15/russian/mapscena/index.html?idn1.html",
		"err_open_rsc": "Не удалось открыть классификатор: {path}",
		"err_classif_struct": "Ошибка структуры классификатора",
		"err_runtime": "Сбой выполнения: {err}",
		"bad_classifier": "Выбран неверный файл классификатора",
	},
	"en": {
		"title": "Create an SQL database structure using a classifier",
		"label_classifier": "Map classifier:",
		"label_sql": "SQL output file:",
		"browse_classifier_title": "Select classifier",
		"browse_sql_title": "Save as",
		"classifier_ft_desc": "Map classifier",
		"sql_ft_desc": "Structured Query Language SQL",
		"warn": "Error Handler",
		"no_classifier": "Classifier file not selected",
		"no_sql": "SQL output file not selected",
		"no_write_perm": "No write permission for the selected folder — choose another directory",
		"checkbox_log": "Create changes log table and triggers",
		"checkbox_single_table": "Generate a single table according to the classifier",
		"btn_run": "Run",
		"btn_cancel": "Cancel",
		"btn_abort": "Abort",
		"btn_help": "Help",
		"progress_read": "Reading semantics",
		"progress_layers": "Building layer tables: {name}",
		"progress_single_table": "Building single table",
		"phase_codes": "codes",
		"phase_names": "names",
		"phase_keys": "keys",
		"phase_units": "units",
		"phase_types": "types",
		"final_title": "Semantics processed: {n}",
		"final_msg": "SQL file generated: {path}",
		"help_url": "https://help.gisserver.ru/v15/russian/mapscena/index.html?idn1.html",
		"err_open_rsc": "Failed to open classifier: {path}",
		"err_classif_struct": "Classifier structure error",
		"err_runtime": "Execution failed: {err}",
		"bad_classifier": "Selected file is not a valid classifier",
	},
}

def tr(key: str, **kwargs) -> str:
	"""Возвращает локализованную строку по ключу; подставляет параметры через format"""
	s = _STR.get(_LANG, _STR["en"]).get(key, key)
	if kwargs:
		try:
			return s.format(**kwargs)
		except Exception:
			return s
	return s

# -------------------------------------
# класс-модель семантики классификатора
# -------------------------------------
class SemanticDef:
	"""Контейнер для семантического определения, извлеченного из классификатора"""

	def __init__(
		self,
		code: int,
		name: str,
		data_type: Optional[str] = None,
		length: Optional[int] = None,
		unit: Optional[str] = None,
		note: Optional[str] = None,
		short_name: Optional[str] = None,
		key: Optional[str] = None,
	):
		self.code = code
		self.name = name.strip()
		self.data_type = (data_type or "").strip()
		self.length = length
		self.unit = (unit or "").strip() if unit else None
		self.note = (note or "").strip() if note else None
		self.short_name = (short_name or "").strip() if short_name else None
		self.key = (key or "").strip() if key else None

	def __repr__(self) -> str:
		return f"SemanticDef(code={self.code}, name={self.name!r}, type={self.data_type!r}, length={self.length}, unit={self.unit!r}, short_name={self.short_name!r}, key={self.key!r})"

# -------------------------
# Журналирование и сообщения
# -------------------------
class Reporter:
	def __init__(self, hmap: Optional[object] = None, popup: bool = False):
		self.hmap = hmap
		self.popup = popup
		self._mapapi = None
		self._logapi = None
		self._mapsyst = None
		try:
			self._mapapi = mapapi
			self._logapi = None
			try:
				import logapi as _logapi
				self._logapi = _logapi
			except Exception:
				self._logapi = None
			self._mapsyst = mapsyst
		except Exception:
			pass

	def error(self, msg: str) -> None:
		print(f"[ERROR] {msg}")
		if self._mapapi is not None:
			title = "TPythonScript::RscToSql(): ошибка" if _LANG == "ru" else "TPythonScript::RscToSql(): error"
			self._mapapi.mapShowMessage(self._mapsyst.WTEXT(msg), self._mapsyst.WTEXT(title))

	def start_action(self, action_type: Optional[int] = None) -> None:
		if self.hmap and self._logapi is not None:
			try:
				atype = action_type if action_type is not None else getattr(self._logapi, "TAC_MED_SCENARIO", 4025)
				self._logapi.mapLogCreateAction(self.hmap, self.hmap, int(atype))
			except Exception:
				pass

	def commit_action(self) -> None:
		if self.hmap and self._logapi is not None:
			try:
				self._logapi.mapLogCommitActionEx(self.hmap, self.hmap, None)
			except Exception:
				pass

	def show_message(self, title: str, message: str) -> None:
		if self._mapapi is not None:
			try:
				self._mapapi.mapShowMessage(self._mapsyst.WTEXT(message), self._mapsyst.WTEXT(title))
			except Exception:
				pass

def normalize_pg_identifier(name: str) -> str:
	"""Нормализует имя столбца под PostgreSQL: нижний регистр, небезопасные символы -> '_', обрезка"""
	ident = re.sub(r"[^0-9a-zA-Z_]", "_", name.strip())
	if re.match(r"^\d", ident):
		ident = f"f_{ident}"
	ident = ident.lower()
	ident = re.sub(r"_+", "_", ident).strip("_")
	return ident or "unnamed"

# Резервированные слова PostgreSQL (минимальный набор, чувствительность к регистру не важна)
PG_RESERVED = {
	"all","analyse","analyze","and","any","array","as","asc","asymmetric",
	"both","case","cast","check","collate","column","constraint","create",
	"current_catalog","current_date","current_role","current_time",
	"current_timestamp","current_user","default","deferrable","desc","distinct",
	"do","else","end","except","false","fetch","for","foreign","from","grant",
	"group","having","in","initially","intersect","into","is","leading",
	"limit","localtime","localtimestamp","natural","not","null","offset","on",
	"only","or","order","placing","primary","references","returning",
	"select","session_user","some","symmetric","table","then","to","trailing",
	"true","union","unique","user","using","variadic","when","where","window",
	"with"
}

def pg_quote_ident(ident: str) -> str:
	"""Оборачивает в кавычки идентификатор для PostgreSQL, если он зарезервирован или не соответствует шаблону"""
	if ident in PG_RESERVED or not re.match(r"^[a-z_][a-z0-9_]*$", ident):
		return '"' + ident.replace('"', '""') + '"'
	return ident

def parse_semantics_from_rsc(
	rsc_path: str,
	progress: Optional[callable] = None,
	is_cancelled: Optional[callable] = None,
) -> Dict[int, SemanticDef]:
	"""Читает классификатор напрямую через rscapi и собирает словарь семантик. Поддерживает прогресс/отмену"""
	wpath = mapsyst.WTEXT(rsc_path)
	prev_msg = 0
	try:
		prev_msg = mapapi.mapMessageEnable(0)
	except Exception:
		prev_msg = 0
	try:
		hrsc = rscapi.mapOpenRscEx(wpath, 0)
	finally:
		try:
			mapapi.mapMessageEnable(prev_msg)
		except Exception:
			pass
	if not hrsc:
		raise RuntimeError(tr("err_open_rsc", path=rsc_path))

	semantics: Dict[int, SemanticDef] = {}
	try:
		count = rscapi.mapGetRscSemanticCount(hrsc)
		if count < 0:
			count = 0
		for idx in range(count):
			if is_cancelled and is_cancelled():
				break
			code = rscapi.mapGetRscSemanticCodeByNumber(hrsc, idx)
			if progress and (idx % 50 == 0 or idx == count - 1):
				try:
					progress(idx + 1, count, tr("progress_read"))
				except Exception:
					pass
			
			name = ""
			name_buf = mapsyst.WTEXT(1024)
			rcn = rscapi.mapGetRscSemanticNameUn(hrsc, code, name_buf, 1024)
			if rcn != 0:
				name = name_buf.string()

			short_name = None
			short_buf = mapsyst.WTEXT(256)
			rcs = rscapi.mapGetRscSemanticShortNameUn(hrsc, code, short_buf, 256)
			if rcs != 0:
				short_name = short_buf.string() or None

			sem_key = None
			key_buf = mapsyst.WTEXT(256)
			rck = rscapi.mapGetRscSemanticKeyUn(hrsc, code, key_buf, 256)
			if rck != 0:
				sem_key = key_buf.string() or None

			unit = None
			unit_buf = mapsyst.WTEXT(512)
			rcu = rscapi.mapGetRscSemanticUnitUn(hrsc, code, unit_buf, 512)
			if rcu != 0:
				unit = unit_buf.string() or None

			type_code = rscapi.mapGetRscSemanticTypeByCode(hrsc, code)
			type_text = f"type={type_code}; size=0; dec=0"
			length: Optional[int] = None

			semantics[int(code)] = SemanticDef(
				code=int(code),
				name=name or f"SEM_{code}",
				data_type=type_text,
				length=length,
				unit=unit,
				note=None,
				short_name=short_name,
				key=sem_key,
			)
	finally:
		_ = rscapi.mapCloseRsc(hrsc)

	return semantics

def map_semantic_ex_to_pg_type(ex_type: int, ex_size: int, ex_decimal: int) -> str:
	"""Возвращает PostgreSQL-тип для поля семантики RSC. Если нельзя уверенно выбрать ограниченный тип, используется TEXT, чтобы избежать потери значений при импорте"""
	if isinstance(ex_decimal, int) and ex_decimal > 0:
		scale = min(max(ex_decimal, 0), 30)
		return f"numeric(38,{scale})"

	if isinstance(ex_size, int) and ex_size > 0:
		return f"varchar({min(ex_size, 65535)})"

	return "text"


def generate_single_table_sql(
	semantics: Dict[int, SemanticDef],
	table_name: str = "classifier_semantics",
	progress: Optional[callable] = None,
	is_cancelled: Optional[callable] = None,
) -> str:
	"""Генерирует одну таблицу со всеми семантиками классификатора (без разбиения на слои).
	Структура: id, objectkey, geom, excode, objtext + колонки по всем семантикам."""
	table_ident = pg_quote_ident(normalize_pg_identifier(table_name) or "classifier_semantics")

	cols: List[str] = []
	cols.append("    id bigserial PRIMARY KEY")
	cols.append("    objectkey integer")
	cols.append("    geom geometry")
	cols.append("    excode integer")
	cols.append("    objtext varchar(1024)")

	used_names: Dict[str, int] = {}
	for sem in sorted(semantics.values(), key=lambda s: s.code):
		if is_cancelled and is_cancelled():
			break
		base_name = sem.key or sem.short_name or sem.name or f"sem_{sem.code}"
		col_base = normalize_pg_identifier(base_name)
		if not col_base:
			col_base = f"sem_{sem.code}"
		col_name = f"{col_base}_{sem.code}" if col_base in used_names else col_base
		used_names[col_base] = used_names.get(col_base, 0) + 1

		ex_type = 0
		ex_size = sem.length or 0
		ex_decimal = 0
		m = re.search(r"type\s*=\s*(\d+)", sem.data_type or "", re.IGNORECASE)
		if m:
			try:
				ex_type = int(m.group(1))
			except Exception:
				ex_type = 0
		m = re.search(r"dec\s*=\s*(\d+)", sem.data_type or "", re.IGNORECASE)
		if m:
			try:
				ex_decimal = int(m.group(1))
			except Exception:
				ex_decimal = 0
		pgtype = map_semantic_ex_to_pg_type(ex_type, int(ex_size), int(ex_decimal))
		cols.append(f"    {pg_quote_ident(col_name)} {pgtype}")

	if progress:
		try:
			progress(1, 1, tr("progress_single_table"))
		except Exception:
			pass

	return f"CREATE TABLE IF NOT EXISTS {table_ident} (\n" + ",\n".join(cols) + "\n);\n"


def generate_layer_tables_sql(
	hrsc,
	semantics: Dict[int, SemanticDef],
	progress: Optional[callable] = None,
	is_cancelled: Optional[callable] = None,
) -> str:
	"""Генерирует таблицы по каждому слою классификатора. Имя таблицы берётся из ключа слоя (short name), при его отсутствии — из имени слоя. Колонки: id, objectkey, geom, excode, objtext + колонки по семантикам слоя"""
	
	def get_layer_infos() -> List[Dict[str, str]]:
		layer_count = rscapi.mapGetRscSegmentCount(hrsc)
		if layer_count < 0:
			layer_count = 0
		result: List[Dict[str, str]] = []
		for incode in range(layer_count):
			
			name = ""
			name_buf = mapsyst.WTEXT(512)
			rcn = rscapi.mapGetRscSegmentNameUn(hrsc, incode, name_buf, 512)
			if rcn != 0:
				name = name_buf.string()
			
			shortname = ""
			short_buf = mapsyst.WTEXT(256)
			rcs = rscapi.mapGetRscSegmentShortNameUn(hrsc, incode, short_buf, 256)
			if rcs != 0:
				shortname = short_buf.string() or ""

			result.append({"index": str(incode), "name": name or f"SEG_{incode}", "shortname": shortname})
		return result

	def get_layer_semantic_codes(layer_index: int) -> List[int]:
		"""Возвращает список кодов семантик для указанного слоя"""
		count = rscapi.mapGetRscSegmentSemanticCount(hrsc, layer_index)
		if count < 0:
			count = 0
		codes: List[int] = []
		for i in range(count):
			code = rscapi.mapGetRscSegmentSemanticCode(hrsc, layer_index, i)
			if code > 0:
				codes.append(code)
		return codes

	sql_parts: List[str] = []
	layer_infos = get_layer_infos()
	total_layers = len(layer_infos)
	for idx, layer in enumerate(layer_infos):
		if is_cancelled and is_cancelled():
			break
		layer_index = int(layer["index"])
		layer_name = layer["name"]
		layer_short = layer["shortname"] or layer_name

		table_base = normalize_pg_identifier(layer_short or layer_name)
		if not table_base:
			table_base = f"layer_{layer_index}"
		table_ident = pg_quote_ident(table_base)

		cols: List[str] = []
		cols.append("    id bigserial PRIMARY KEY")
		cols.append("    objectkey integer")
		cols.append("    geom geometry")
		cols.append("    excode integer")
		cols.append("    objtext varchar(1024)")

		layer_codes = get_layer_semantic_codes(layer_index)
		used_names: Dict[str, int] = {}
		for sem_code in layer_codes:
			if is_cancelled and is_cancelled():
				break
			sem = semantics.get(sem_code)
			if not sem:
				continue
			base_name = sem.key or sem.short_name or sem.name or f"sem_{sem.code}"
			col_base = normalize_pg_identifier(base_name)
			if not col_base:
				col_base = f"sem_{sem.code}"
			col_name = f"{col_base}_{sem.code}" if col_base in used_names else col_base
			used_names[col_base] = used_names.get(col_base, 0) + 1

			ex_type = 0
			ex_size = sem.length or 0
			ex_decimal = 0
			m = re.search(r"type\s*=\s*(\d+)", sem.data_type or "", re.IGNORECASE)
			if m:
				try:
					ex_type = int(m.group(1))
				except Exception:
					ex_type = 0
			m = re.search(r"dec\s*=\s*(\d+)", sem.data_type or "", re.IGNORECASE)
			if m:
				try:
					ex_decimal = int(m.group(1))
				except Exception:
					ex_decimal = 0
			pgtype = map_semantic_ex_to_pg_type(ex_type, int(ex_size), int(ex_decimal))
			cols.append(f"    {pg_quote_ident(col_name)} {pgtype}")

		sql_parts.append(f"CREATE TABLE IF NOT EXISTS {table_ident} (\n" + ",\n".join(cols) + "\n);")

		if progress:
			try:
				progress(idx + 1, total_layers, (layer_short or layer_name))
			except Exception:
				pass

	return "\n\n".join(sql_parts) + ("\n" if sql_parts else "")

def generate_layer_tables_sql_from_rsc_path(
	rsc_path: str,
	semantics: Dict[int, SemanticDef],
	progress: Optional[callable] = None,
	is_cancelled: Optional[callable] = None,
) -> str:
	"""Открывает RSC, генерирует SQL таблиц слоёв и закрывает RSC"""
	wpath = mapsyst.WTEXT(rsc_path)
	hrsc = 0
	try:
		hrsc = rscapi.mapOpenRscEx(wpath, 0)
		if not hrsc:
			raise RuntimeError(tr("err_open_rsc", path=rsc_path))
		return generate_layer_tables_sql(hrsc, semantics, progress=progress, is_cancelled=is_cancelled)
	finally:
		if hrsc:
			_ = rscapi.mapCloseRsc(hrsc)


def generate_changes_log_sql() -> str:
	"""Генерирует таблицу для журнала транзакций"""
	
	return''' DROP TABLE IF EXISTS public.pgis2map_dbchanges_log;
CREATE /*UNLOGGED*/ TABLE public.pgis2map_dbchanges_log
(
  schemaname  name        NOT NULL,
  tablename   name        NOT NULL,
  tableident  oid         NOT NULL,
  idrecord    integer     NOT NULL,
  changestype integer     NOT NULL,
  userid      text        NOT NULL DEFAULT user,
  stamp       timestamptz NOT NULL DEFAULT clock_timestamp(),
  sessionident text       DEFAULT current_setting('application_name'),
  tranident   bigint      NOT NULL DEFAULT txid_current(),
  CONSTRAINT pk_pgis2map_dbchanges_log PRIMARY KEY (tablename, idrecord)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.pgis2map_dbchanges_log
  OWNER TO postgres;
CREATE INDEX "IX_spdblog_stamp"
  ON public.pgis2map_dbchanges_log
  USING btree
  (stamp DESC NULLS LAST);
CREATE INDEX "IX_spdblog_tableident"
  ON pgis2map_dbchanges_log
  USING btree
  (tableident);
CREATE INDEX "IX_spdblog_tranident"
  ON public.pgis2map_dbchanges_log
  USING btree (tranident);  
CREATE OR REPLACE FUNCTION pgis2map_dbchanges_log_insert() RETURNS TRIGGER AS $pgis2map_dbchanges_log$
BEGIN
  NEW.tableident = ('"' || NEW.schemaname || '"."' || NEW.tablename || '"')::regclass::oid;
  NEW.tranident  = txid_current();
  IF EXISTS (SELECT * FROM public.pgis2map_dbchanges_log 
             WHERE idrecord=NEW.idrecord AND tableident=NEW.tableident)
  THEN
     UPDATE public.pgis2map_dbchanges_log SET           
       changestype  = NEW.changestype,
       userid       = user,
       stamp        = clock_timestamp(),
       sessionident = current_setting('application_name'),
       tranident    = NEW.tranident
     WHERE (idrecord=NEW.idrecord AND tableident=NEW.tableident);
     RETURN NULL; 
  ELSE 
     RETURN NEW;      
  END IF;             
  RETURN NULL; 
END;
$pgis2map_dbchanges_log$ LANGUAGE plpgsql VOLATILE SECURITY DEFINER;  
DROP TRIGGER IF EXISTS trigger_pgis2map_dbchanges_log_insert ON public.pgis2map_dbchanges_log;
CREATE TRIGGER trigger_pgis2map_dbchanges_log_insert
    BEFORE INSERT ON pgis2map_dbchanges_log
    FOR EACH ROW
    EXECUTE PROCEDURE pgis2map_dbchanges_log_insert();
DO LANGUAGE plpgsql $$
 DECLARE
   vr record;
   sql text;
BEGIN
FOR vr IN 
 select f.table_schema, f.table_name, f.column_name 
  from information_schema.TABLE_CONSTRAINTS c
  inner join information_schema.CONSTRAINT_COLUMN_USAGE f
  on f.constraint_schema = c.constraint_schema and 
     f.table_name = c.table_name and
     f.constraint_name = c.constraint_name
  inner join information_schema.columns g
  on f.constraint_schema = g.table_schema and 
     f.table_name = g.table_name and g.udt_name = 'geometry'
     and c.constraint_type='PRIMARY KEY'
 LOOP
   sql = 'CREATE OR REPLACE FUNCTION "save_' || vr.column_name || '_pgis2map_dbchanges_log"() RETURNS TRIGGER AS $tr_audit$' ||
    'BEGIN
       IF    (TG_OP = ''DELETE'') 
         THEN 
           INSERT INTO pgis2map_dbchanges_log(schemaname, tablename, idrecord, changestype) 
                SELECT  TG_TABLE_SCHEMA, TG_TABLE_NAME, OLD."' || vr.column_name || '", 3;
       ELSIF (TG_OP = ''UPDATE'') 
         THEN 
           INSERT INTO pgis2map_dbchanges_log(schemaname, tablename, idrecord, changestype) 
                SELECT  TG_TABLE_SCHEMA, TG_TABLE_NAME, NEW."' || vr.column_name || '", 2;
       ELSIF (TG_OP = ''INSERT'') 
         THEN 
           INSERT INTO pgis2map_dbchanges_log(schemaname, tablename, idrecord, changestype) 
                SELECT  TG_TABLE_SCHEMA, TG_TABLE_NAME, NEW."' || vr.column_name || '",  1;      
       END IF;
       RETURN NULL;
    END;
    $tr_audit$ LANGUAGE plpgsql  VOLATILE SECURITY DEFINER
    COST 100;';
    
   EXECUTE sql;

   sql = 'DROP TRIGGER IF EXISTS trigger_pgis2map_dbchanges_log_insert ON "' || vr.table_schema || '"."' || vr.table_name || '";';
   EXECUTE sql;

   sql = 'CREATE TRIGGER trigger_pgis2map_dbchanges_log_insert 
    AFTER INSERT OR UPDATE OR DELETE ON "' || vr.table_schema || '"."' || vr.table_name || '"    
    FOR EACH ROW
    EXECUTE PROCEDURE "save_' || vr.column_name || '_pgis2map_dbchanges_log"();';
   EXECUTE sql;
   
 END LOOP;
END
$$;
'''
# Главная функция для вызова из ГИС Панорама
def GenerateSemanticsTable(hmap, hobj) -> float: #caption:Сформировать SQL-структуру базы данных по классификатору 
	"""Формирует SQL файл по классификатору RSC/RSCZ"""
	report = Reporter(hmap, popup=False)
	report.start_action()
	try:
		selected_rsc_path = {"value": ""}
		output_sql_path = {"value": ""}
		cancelled = {"value": False}
		flags = {"with_log": False, "single_table": False}

		def run_dialog() -> None:
			import tkinter
			from tkinter import filedialog, ttk, messagebox as mb
			import os as _os
			import webbrowser

			root = tkinter.Tk()
			root.title(tr("title"))
			root.geometry("670x180")
			root.resizable(False, False)
			root.protocol("WM_DELETE_WINDOW", lambda: on_cancel())
			try:
				root.eval('tk::PlaceWindow . center')
			except Exception:
				root.update_idletasks()
				ws = root.winfo_screenwidth()
				hs = root.winfo_screenheight()
				w = 670
				h = 180
				x = (ws // 2) - (w // 2)
				y = (hs // 2) - (h // 2)
				root.geometry(f"{w}x{h}+{x}+{y}")

			try:
				root.grid_columnconfigure(0, weight=0, minsize=180)
				root.grid_columnconfigure(1, weight=1, minsize=420)
				root.grid_columnconfigure(2, weight=0, minsize=72)
			except Exception:
				pass

			def ellipsize_path(full_path: str, entry_widget) -> str:
				"""Сокращает путь, убирая среднюю часть: C:\\Users\\..\\data\\file.rsc"""
				if not full_path:
					return ""
				try:
					entry_widget.update_idletasks()
					avail_px = entry_widget.winfo_width() - 8
					if avail_px <= 0:
						avail_px = 400
					import tkinter.font as tkfont
					font = tkfont.nametofont(str(entry_widget.cget("font") or "TkDefaultFont"))
					if font.measure(full_path) <= avail_px:
						return full_path
					drive, tail = _os.path.splitdrive(full_path)
					parts = tail.replace("/", "\\").strip("\\").split("\\")
					if len(parts) <= 2:
						return full_path
					head = drive + "\\" + parts[0]
					end_parts = [parts[-1]]
					for i in range(len(parts) - 2, 0, -1):
						candidate = head + "\\..\\" + "\\".join(parts[i:])
						if font.measure(candidate) <= avail_px:
							end_parts.insert(0, parts[i])
						else:
							break
					return head + "\\..\\" + "\\".join(end_parts)
				except Exception:
					return full_path

			rsc_full_path = {"value": ""}
			out_full_path = {"value": ""}

			tkinter.Label(root, text=tr("label_classifier")).grid(row=0, column=0, sticky="w", padx=8, pady=(10, 4))
			rsc_display_var = tkinter.StringVar()
			rsc_entry = ttk.Entry(root, textvariable=rsc_display_var, state="readonly")
			rsc_entry.grid(row=0, column=1, sticky="we", padx=4, pady=(10, 4))
			def browse_rsc():
				_prev = rsc_full_path["value"]
				init_dir = _os.path.dirname(_prev) if _prev else ""
				path = filedialog.askopenfilename(
					title=tr("browse_classifier_title"),
					filetypes=[(tr("classifier_ft_desc"), "*.rsc *.rscz"), ("All files" if _LANG=="en" else "Все файлы", "*.*")],
					initialdir=init_dir or None
				)
				if path:
					path = _os.path.normpath(path)
					rsc_full_path["value"] = path
					rsc_display_var.set(ellipsize_path(path, rsc_entry))
					out_full_path["value"] = ""
					out_display_var.set("")
			tkinter.Button(root, text="...", width=5, command=browse_rsc).grid(row=0, column=2, padx=(8, 8), pady=(10, 4))

			tkinter.Label(root, text=tr("label_sql")).grid(row=1, column=0, sticky="w", padx=8, pady=4)
			out_display_var = tkinter.StringVar()
			out_entry = ttk.Entry(root, textvariable=out_display_var, state="readonly")
			out_entry.grid(row=1, column=1, sticky="we", padx=4, pady=4)
			def browse_out():
				_out = out_full_path["value"]
				_rsc = rsc_full_path["value"]
				init_dir = _os.path.dirname(_out) if _out else (_os.path.dirname(_rsc) if _rsc else _os.getcwd())
				base = _os.path.splitext(_os.path.basename(_rsc))[0] if _rsc else "classifier_semantics"
				init_file = base + ".sql"
				path = filedialog.asksaveasfilename(
					title=tr("browse_sql_title"),
					defaultextension=".sql",
					filetypes=[(tr("sql_ft_desc"), "*.sql"), ("All files" if _LANG=="en" else "Все файлы", "*.*")],
					initialdir=init_dir,
					initialfile=init_file
				)
				if path:
					path = _os.path.normpath(path)
					target_dir = _os.path.dirname(path) or "."
					try:
						writable = _os.path.isdir(target_dir) and _os.access(target_dir, _os.W_OK | _os.X_OK)
					except Exception:
						writable = False
					if not writable:
						mapapi.mapShowMessage(mapsyst.WTEXT(tr("no_write_perm")), mapsyst.WTEXT("rsc2sql"))
						return
					out_full_path["value"] = path
					out_display_var.set(ellipsize_path(path, out_entry))
			tkinter.Button(root, text="...", width=5, command=browse_out).grid(row=1, column=2, padx=(8, 8), pady=4)

			log_var = tkinter.BooleanVar(value=False)
			single_table_var = tkinter.BooleanVar(value=False)
			tkinter.Checkbutton(root, text=tr("checkbox_log"), variable=log_var).grid(row=2, column=1, sticky="w", padx=4, pady=(0, 2))
			tkinter.Checkbutton(root, text=tr("checkbox_single_table"), variable=single_table_var).grid(row=3, column=1, sticky="w", padx=4, pady=(0, 2))

			btn_frame = tkinter.Frame(root)
			btn_frame.grid(row=4, column=0, columnspan=3, sticky="e", padx=(8, 12), pady=12)

			state = {"running": False}
			def on_help():
				try:
					webbrowser.open(tr("help_url"))
				except Exception:
					try:
						mb.showinfo(tr("btn_help"))
					except Exception:
						pass
			def on_cancel():
				if state["running"]:
					cancelled["value"] = True
				else:
					cancelled["value"] = True
					try: root.destroy()
					except Exception: pass
			def on_execute():
				if not rsc_full_path["value"]:
					try:
						mb.showwarning(tr("warn"), tr("no_classifier"))
					except Exception:
						pass
					return
				if not out_full_path["value"]:
					try:
						mb.showwarning(tr("warn"), tr("no_sql"))
					except Exception:
						pass
					return
				_candidate = rsc_full_path["value"]
				if not _candidate.lower().endswith((".rsc", ".rscz")):
					write_diag_pair("input parameters error - ", _candidate, getattr(maptype, "MT_ERROR", 1))
					try: mb.showwarning(tr("warn"), tr("bad_classifier"))
					except Exception: pass
					return
				prev_msg = 0
				try:
					prev_msg = mapapi.mapMessageEnable(0)
				except Exception:
					prev_msg = 0
				try:
					_hr = rscapi.mapOpenRscEx(mapsyst.WTEXT(_candidate), 0)
				finally:
					try:
						mapapi.mapMessageEnable(prev_msg)
					except Exception:
						pass
				if not _hr:
					msg = f"{tr('err_classif_struct')} - {_candidate}"
					mapapi.mapShowMessage(mapsyst.WTEXT(msg), mapsyst.WTEXT("rsc2sql"))
					write_diag_pair("invalid classifier format, file - ", _candidate, getattr(maptype, "MT_ERROR", 1))
					try: mb.showwarning(tr("warn"), msg)
					except Exception: pass
					return
				is_ok = True
				_semn = rscapi.mapGetRscSemanticCount(_hr)
				_segn = rscapi.mapGetRscSegmentCount(_hr)
				if (_semn <= 0) and (_segn <= 0):
					is_ok = False
				_ = rscapi.mapCloseRsc(_hr)
				if not is_ok:
					msg = f"{tr('err_classif_struct')} - {_candidate}"
					mapapi.mapShowMessage(mapsyst.WTEXT(msg), mapsyst.WTEXT("rsc2sql"))
					write_diag_pair("invalid classifier format, file - ", _candidate, getattr(maptype, "MT_ERROR", 1))
					try: mb.showwarning(tr("warn"), msg)
					except Exception: pass
					return
				selected_rsc_path["value"] = _candidate
				output_sql_path["value"] = out_full_path["value"]
				flags["with_log"] = bool(log_var.get())
				flags["single_table"] = bool(single_table_var.get())
				state["running"] = True
				exec_btn.config(text=tr("btn_abort"))

			exec_btn = tkinter.Button(btn_frame, text=tr("btn_run"), width=10, command=on_execute)
			exec_btn.grid(row=0, column=0, padx=4)
			cancel_btn = tkinter.Button(btn_frame, text=tr("btn_cancel"), width=10, command=on_cancel)
			cancel_btn.grid(row=0, column=1, padx=4)
			help_btn = tkinter.Button(btn_frame, text=tr("btn_help"), width=10, command=on_help)
			help_btn.grid(row=0, column=2, padx=4)

			try:
				root.update_idletasks()
				try:
					root.eval('tk::PlaceWindow . center')
				except Exception:
					ws = root.winfo_screenwidth()
					hs = root.winfo_screenheight()
					w = root.winfo_width() or 860
					h = root.winfo_height() or 130
					x = (ws // 2) - (w // 2)
					y = (hs // 2) - (h // 2)
					root.geometry(f"{w}x{h}+{x}+{y}")
			except Exception:
				pass

			while not state["running"] and not cancelled["value"]:
				try: root.update()
				except Exception: break

			selected_rsc_path["root"] = root

		run_dialog()
		if cancelled["value"]:
			return 0.0

		rsc_path = selected_rsc_path["value"]
		out_sql = output_sql_path["value"] or (os.path.splitext(rsc_path)[0] + ".sql")
		with_log = bool(flags.get("with_log"))
		single_table = bool(flags.get("single_table"))

		hprogress = 0
		try:
			hprogress = mapapi.mapOpenProgressBar()

			def set_progress(current: int, total: int, title: str) -> int:
				"""Обновляет прогресс-бар Панорамы; возвращает код ответа (0 — ок, -1 — отмена пользователем)"""
				if hprogress == 0 or total <= 0:
					return 0
				percent = int(max(0, min(100, (current * 100) // total)))
				ret = mapapi.mapProgressBar(hprogress, percent, mapsyst.WTEXT(f" {title}: {current}/{total}"))
				if ret == -1:
					cancelled["value"] = True
				try:
					rt = selected_rsc_path.get("root")
					if rt:
						rt.update()
				except Exception:
					pass
				return ret

			def ui_is_cancelled() -> bool:
				"""Проверяет прерывание процесса и обновляет UI для отзывчивости"""
				try:
					rt = selected_rsc_path.get("root")
					if rt:
						rt.update()
				except Exception:
					pass
				return bool(cancelled["value"])

			semantics = parse_semantics_from_rsc(
				rsc_path,
				progress=lambda c, t, title: set_progress(c, max(t, 1), title),
				is_cancelled=ui_is_cancelled,
			)
			if cancelled["value"]:
				return 0.0

			if single_table:
				layers_sql = generate_single_table_sql(
					semantics,
					progress=lambda c, t, name: set_progress(c, max(t, 1), name),
					is_cancelled=ui_is_cancelled,
				)
			else:
				layers_sql = generate_layer_tables_sql_from_rsc_path(
					rsc_path,
					semantics,
					progress=lambda c, t, name: set_progress(c, max(t, 1), tr("progress_layers", name=name)),
					is_cancelled=ui_is_cancelled,
				)
			if cancelled["value"]:
				return 0.0

			header = (
				f"SET client_encoding = 'UTF8';\n\n"
				f"CREATE EXTENSION IF NOT EXISTS postgis;\n"
				f"CREATE EXTENSION IF NOT EXISTS postgis_topology;\n\n"
			)
			with open(out_sql, "w", encoding="utf-8") as f:
				f.write(header)
				f.write(layers_sql)
				if with_log:
					f.write("\n\n")
					f.write(generate_changes_log_sql())

			ready = len(semantics)
			mapapi.mapShowMessage(
				mapsyst.WTEXT(tr("final_msg", path=out_sql)),
				mapsyst.WTEXT(tr("final_title", n=ready))
			)
			write_diag_pair("SQL file generated - ", out_sql, getattr(maptype, "MT_INFO", 0))

			return 1.0

		finally:
			if hprogress != 0:
				mapapi.mapCloseProgressBar(hprogress)
			try:
				rt = selected_rsc_path.get("root")
				if rt:
					try: rt.quit()
					except Exception: pass
					try: rt.update_idletasks()
					except Exception: pass
					try: rt.destroy()
					except Exception: pass
					selected_rsc_path["root"] = None
					try:
						import gc as _gc
						_gc.collect()
						import tkinter as _tk
						_tk._default_root = None
					except Exception:
						pass
			except Exception:
				pass

	except Exception as exc:
		report.error(tr("err_runtime", err=str(exc)))
		return 0.0
	finally:
		report.commit_action()