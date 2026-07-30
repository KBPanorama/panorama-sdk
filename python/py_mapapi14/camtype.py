#!/usr/bin/env python3

import ctypes

HVIDEO       = ctypes.c_void_p
HVIDEOSCREEN = ctypes.c_void_p
HCAM         = ctypes.c_void_p
HTOPIC       = ctypes.c_void_p
HEVENTDB     = ctypes.c_void_p
HEVENTFILT   = ctypes.c_void_p
HCAMEVENT    = ctypes.c_void_p

# Минимальный размер строковых полей
STRFIELDSIZE = 64

# Максимальный уровень вложенности для тем оповещений о событиях
MAXTOPICLEVEL = 4

# Размер строковых полей для тегов/атрибутов XML-документа
SOAP_TAGLEN = 1024

# Время ожидания ответа на запрос к камере (в миллисекундах)
SOAP_CONNECT_TIMEOUT = 5000

# Коды ошибок
SOAP_OK                         = 0   # Успешное выполнение
SOAP_CLI_FAULT                  = 1
SOAP_SVR_FAULT                  = 2
SOAP_TAG_MISMATCH               = 3   # Имя элемента не совпадает с требуемым
SOAP_TYPE                       = 4   # Тип элемента не совпадает с требуемым
SOAP_SYNTAX_ERROR               = 5   # Синтаксическая ошибка при разборе SOAP-сообщения
SOAP_NO_TAG                     = 6   # Требуемый элемент отсутствует в сообщении
SOAP_IOB                        = 7
SOAP_MUSTUNDERSTAND             = 8
SOAP_NAMESPACE                  = 9   # Пространство имен элемента не совпадает с требуемым
SOAP_USER_ERROR                 = 10
SOAP_FATAL_ERROR                = 11
SOAP_FAULT                      = 12  # Принято SOAP-сообщение с описанием ошибки
SOAP_NO_METHOD                  = 13  # Запрашиваемая функция/сервис не поддерживаются камерой
SOAP_NO_DATA                    = 14  # Отсутствуют запрашиваемые данные
SOAP_GET_METHOD                 = 15
SOAP_PUT_METHOD                 = 16
SOAP_PATCH_METHOD               = 17
SOAP_DEL_METHOD                 = 18
SOAP_HTTP_METHOD                = 19
SOAP_EOM                        = 20
SOAP_MOE                        = 21
SOAP_HDR                        = 22
SOAP_NULL                       = 23  # Нулевой указатель, отсутствуют данные
SOAP_DUPLICATE_ID               = 24
SOAP_MISSING_ID                 = 25
SOAP_HREF                       = 26
SOAP_UDP_ERROR                  = 27
SOAP_TCP_ERROR                  = 28
SOAP_HTTP_ERROR                 = 29  # Ошибка приема/посылки данных по протоколу HTTP
SOAP_SSL_ERROR                  = 30
SOAP_ZLIB_ERROR                 = 31
SOAP_DIME_ERROR                 = 32
SOAP_DIME_HREF                  = 33
SOAP_DIME_MISMATCH              = 34
SOAP_DIME_END                   = 35
SOAP_MIME_ERROR                 = 36
SOAP_MIME_HREF                  = 37
SOAP_MIME_END                   = 38
SOAP_VERSIONMISMATCH            = 39
SOAP_PLUGIN_ERROR               = 40
SOAP_DATAENCODINGUNKNOWN        = 41
SOAP_REQUIRED                   = 42
SOAP_PROHIBITED                 = 43
SOAP_OCCURS                     = 44
SOAP_LENGTH                     = 45
SOAP_PATTERN                    = 46
SOAP_FD_EXCEEDED                = 47
SOAP_UTF_ERROR                  = 48
SOAP_NTLM_ERROR                 = 49
SOAP_LEVEL                      = 50
SOAP_FIXED                      = 51
SOAP_EMPTY                      = 52
SOAP_END_TAG                    = 53
SOAP_ERR                        = 99  #  Авторизация не выполнена, введен некорретный код пользователя

# Коды ошибок HTTP
HTTP_BAD_REQUEST                = 400  # Некорретный HTTP-запрос
HTTP_UNAUTHORIZED               = 401  # Авторизация не выполнена
HTTP_FORBIDDEN                  = 403  # Доступ к ресурсу запрещен
HTTP_NOT_FOUND                  = 404  # Запрашиваемый ресурс не найден

# Битовые маски для определения сервисов, предоставляемых камерой
CAPABILITY_CATEGORY_ALL         = 0x3F  # Доступны все сервисы
CAPABILITY_CATEGORY_ANALYTICS   = 0x01  # Сервис видеоаналитики
CAPABILITY_CATEGORY_DEVICE      = 0x02  # Сервис управления базовыми настройками
CAPABILITY_CATEGORY_EVENTS      = 0x04  # Сервис подписки на события
CAPABILITY_CATEGORY_IMAGING     = 0x08  # Сервис для настройки параметров съемки
CAPABILITY_CATEGORY_MEDIA       = 0x10  # Сервис управления медиа-параметрами
CAPABILITY_CATEGORY_PTZ         = 0x20  # Сервис управления поворотной камерой

# Поддерживаемые видеокодеки
ENCODING_JPEG  = 1
ENCODING_H264  = 2
ENCODING_MPEG4 = 3

# Коды событий, получаемых от камеры
EVENT_UNDEFINED          = 0   # Тип события не определен
EVENT_MONITORING         = 1   # Информирование о состоянии камеры
EVENT_MOTION_ALARM       = 2   # Движение в кадре
EVENT_FIRE_ALARM         = 3   # Пожарная тревога
EVENT_SCENE_CHANGE       = 4   # Изменение сцены съемки 
EVENT_LINE_CROSSED       = 5   # Пересечение линии
EVENT_OBJECT_INSIDE      = 6   # Вторжение в зону
EVENT_OBJECT_ABANDONED   = 7   # Оставленный предмет
EVENT_OBJECT_MISSING     = 8   # Пропавший предмет
EVENT_FACE_DETECTED      = 9   # Обнаружено лицо в кадре
EVENT_TAMPER_DETECTED    = 10  # Закрытие объектива

# Битовые маски для определения режимов позиционирования, поддерживаемых камерой 
PTZ_NOT_SUPPORTED       = 0x00  # Позиционирование не поддерживается
PTZ_PANTILT_ABSOLUTE    = 0x01  # Панорамирование и наклон по абсолютным координатам
PTZ_PANTILT_RELATIVE    = 0x02  # Панорамирование и наклон по относительным координатам
PTZ_PANTILT_CONTINUOUS  = 0x04  # Непрерывное панорамирование и наклон
PTZ_ZOOM_ABSOLUTE       = 0x08  # Масштабирование (абсолютное)
PTZ_ZOOM_RELATIVE       = 0x10  # Масштабирование (относительное)
PTZ_ZOOM_CONTINUOUS     = 0x20  # Масштабирование (непрерывное)

# Макросы для определения состояния позиционирования
PTZ_STATUS_UNKNOWN      = 0     # Неизвестно
PTZ_STATUS_IDLE         = 1     # Простой
PTZ_STATUS_MOVING       = 2     # Движение


PACK_WIDTH = 1

#-----------------------------
class CAMERAINFO(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Manufacturer",ctypes.c_char*(STRFIELDSIZE)),
                ("Model",ctypes.c_char*(STRFIELDSIZE)),
                ("FirmwareVersion",ctypes.c_char*(STRFIELDSIZE)),
                ("SerialNumber",ctypes.c_char*(STRFIELDSIZE)),
                ("HardwareId",ctypes.c_char*(STRFIELDSIZE))]
#-----------------------------


#-----------------------------
class CAMERAEVENT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("DateCamera",ctypes.c_int),
                ("TimeCamera",ctypes.c_int),
                ("DateLocal",ctypes.c_int),
                ("TimeLocal",ctypes.c_int),
                ("IsActiveFlag",ctypes.c_int),
                ("State",ctypes.c_int),
                ("Code",ctypes.c_int),
                ("Reserve",ctypes.c_int),
                ("SubscriptionRef",ctypes.c_char*(2*STRFIELDSIZE)),
                ("ProducerRef",ctypes.c_char*(2*STRFIELDSIZE)),
                ("Topic",ctypes.c_char*(4*STRFIELDSIZE)),
                ("Source",ctypes.c_char*(4*STRFIELDSIZE)),
                ("Key",ctypes.c_char*(4*STRFIELDSIZE)),
                ("Data",ctypes.c_char*(4*STRFIELDSIZE)),
                ("Extension",ctypes.c_char*(4*STRFIELDSIZE))]
#-----------------------------


#-----------------------------
class TOPICSELECT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Index",ctypes.c_int*(MAXTOPICLEVEL))]
#-----------------------------


#-----------------------------
class DBCAMERAINFO(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("DbId",ctypes.c_int),
                ("Reserve",ctypes.c_int),
                ("Addr",ctypes.c_char*(4*STRFIELDSIZE)),
                ("Name",ctypes.c_char*(4*STRFIELDSIZE))]
#-----------------------------


#-----------------------------
class DBTOPICINFO(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("DbId",ctypes.c_int),
                ("Reserve",ctypes.c_int),
                ("Topic",ctypes.c_char*(4*STRFIELDSIZE))]
#-----------------------------


#-----------------------------
class PTZSTATUS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Pan",ctypes.c_double),
                ("Tilt",ctypes.c_double),
                ("Zoom",ctypes.c_double),
                ("MoveStatusPanTilt",ctypes.c_int),
                ("MoveStatusZoom",ctypes.c_int),
                ("DateCamera",ctypes.c_int),
                ("TimeCamera",ctypes.c_int),
                ("Error",ctypes.c_char*(4*STRFIELDSIZE))]
#-----------------------------


#-----------------------------
class PTZRANGE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("PanMin",ctypes.c_double),
                ("PanMax",ctypes.c_double),
                ("TiltMin",ctypes.c_double),
                ("TiltMax",ctypes.c_double),
                ("ZoomMin",ctypes.c_double),
                ("ZoomMax",ctypes.c_double)]
#-----------------------------


