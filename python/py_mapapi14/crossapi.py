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
    *                Библиотека геометрических функций                 *
    *                      и оверлейных операций                       *
    *                                                                  *
    *  Функции поиска точек пересечения отрезков:                      *
    *                                                                  *
    *    ovlGetCrossPoint           - Определение точек пересечения    *
    *                                 отрезков                         *
    *    ovlGetCrossPointRealCut    - Определение точек пересечения    *
    *                                 отрезков ненулевой длины         *
    *    ovlCrossTestFrame          - Тест пересечения отрезка         *
    *                                 с прямоугольной рамкой           *
    *    ovlDistance                - Вычисление расстояния между      *
    *                                 точкой и прямой                  *
    *    ovlDistance2               - Вычисление квадрата расстояния   *
    *                                 между точкой и прямой            *
    *    ovlSeekNearPointOnLine     - Поиск точки на линии, ближайшей  *
    *                                 к заданной                       *
    *                                                                  *
    *  Функции запроса положения точки:                                *
    *                                                                  *
    *    ovlGetLocationPoint        - Определение расположения точки   *
    *                                 относительно замкнутого объекта  *
    *                                                                  *
    *  Функции пересечения объектов:                                   *
    *                                                                  *
    *    ovlCreate            - Создать объект оверлейных операций     *
    *    ovlFree              - Освободить объект оверлейных операций  *
    *                                                                  *
    *    ovlSetTemplet        - Установить шаблон для оверлейных       *
    *                           операций                               *
    *    ovlSetObjectCross    - Установить обрабатываемый объект       *
    *                           и метод обработки                      *
    *    ovlGetNextObject     - Запросить очередную часть разрезаемого *
    *                           объекта                                *
    *                                                                  *
    *    ovlIsEditTemplet     - Запросить признак изменения метрики    *
    *                           шаблона                                *
    *    ovlIsEditObject      - Запросить признак изменения метрики    *
    *                           объекта                                *
    *    ovlGetAdjustTemplet  - Запросить метрику шаблона,             *
    *                           согласованную метрикой объекта         *
    *    ovlGetAdjustObject   - Запросить метрику объекта,             *
    *                           согласованную метрикой шаблона         *
    *    ovlGetCheckObject    - Запросить метрику проверенного объекта *
    *                           с удалением двойных точек              *
    *    ovlGetCrossPoints    - Запросить все точки пересечения        *
    *                           шаблона и объекта                      *
    *                                                                  *
    *  Функции запроса описания ошибок:                                *
    *                                                                  *
    *    ovlCreateCheckObject - Создать объект оверлейных операций     *
    *                           для выполения контроля метрики объекта *
    *    ovlGetErrorCode      - Запросить код ошибки                   *
    *    ovlGetError          - Запросить описание ошибки              *
    *    ovlGetErrorUn        - Запросить описание ошибки              *
    *    ovlGetErrorPointX    - Запросить координату X точки,          *
    *                           содержащей ошибку                      *
    *    ovlGetErrorPointY    - Запросить координату Y точки,          *
    *                           содержащей ошибку                      *
    *                                                                  *
    *    ovlGetErrorCount     - Запросить число ошибок                 *
    *                                                                  *
    *    ovlGetErrorCodeN     - Запросить код ошибки по номеру         *
    *    ovlGetErrorN         - Запросить описание ошибки по номеру    *
    *    ovlGetErrorNUn       - Запросить описание ошибки              *
    *    ovlGetErrorPointXN   - Запросить координаты точки,            *
    *    ovlGetErrorPointYN     содержащей ошибку по номеру            *
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
# CROSS-коды, возвращаемые функцией ovlGetCrossPoint

CROSS_0          = 0  # Пересечений нет
CROSS_1          = 1  # 1 ТП (одна точка пересечения/вхождения)
CROSS_2          = 2  # 2 ТП (две точки пересечения/вхождения)
CROSS_A1A2_EQUAL = 4  # Точки отрезка A равны (отрезок нулевой длины)
CROSS_B1B2_EQUAL = 8  # Точки отрезка B равны (отрезок нулевой длины)
CROSS_A1B1_EQUAL = 16  # Точки A1 и B1 равны
CROSS_A2B2_EQUAL = 32  # Точки A2 и B2 равны
CROSS_A1B2_EQUAL = 64  # Точки A1 и B2 равны
CROSS_A2B1_EQUAL = 128  # Точки A2 и B1 равны

# Производные CROSS-коды, возвращаемые функцией ovlGetCrossPoint

CROSS_A1A2_EQUAL_1   = 5  # Точки отрезка A равны + 1 ТП (1+4)
CROSS_B1B2_EQUAL_1   = 9  # Точки отрезка B равны + 1 ТП (1+8)
CROSS_AB_NULL        = 12  # Oтрезки A и B нулевой длины (4+8)
CROSS_A1B1_EQUAL_1   = 17  # Точки A1 и B1 равны + 1 ТП (1+16)
CROSS_A2B2_EQUAL_1   = 33  # Точки A2 и B2 равны + 1 ТП (1+32)
CROSS_A1B2_EQUAL_1   = 65  # Точки A1 и B2 равны + 1 ТП (1+64)
CROSS_A2B1_EQUAL_1   = 129  # Точки A2 и B1 равны + 1 ТП (1+128)
CROSS_A1B1_EQUAL_2   = 18  # Точки A1 и B1 равны + 2 ТП (2+16)
CROSS_A2B2_EQUAL_2   = 34  # Точки A2 и B2 равны + 2 ТП (2+32)
CROSS_A1B2_EQUAL_2   = 66  # Точки A1 и B2 равны + 2 ТП (2+64)
CROSS_A2B1_EQUAL_2   = 130  # Точки A2 и B1 равны + 2 ТП (2+128)
CROSS_A1A2B1_EQUAL_1 = 149  # Точки A1,A2,B1 равны + 1 ТП (1+4+16+128)
CROSS_A1A2B2_EQUAL_1 = 101  # Точки A1,A2,B2 равны + 1 ТП (1+4+32+64)
CROSS_B1B2A1_EQUAL_1 = 89  # Точки B1,B2,A1 равны + 1 ТП (1+8+16+64)
CROSS_B1B2A2_EQUAL_1 = 169  # Точки B1,B2,A2 равны + 1 ТП (1+8+32+128)
CROSS_AB_EQUAL_2     = 50  # Отрезки совпадают + 2 ТП (2+16+32)
CROSS_BA_EQUAL_2     = 194  # Отрезки совпадают + 2 ТП (2+64+128)
CROSS_ALL_EQUAL_1    = 253  # Все точки равны + 1 ТП (1+4+8+16+32+64+128)
CROSS_EQUAL_1        = 240  # Флаг определения наличия общей точки (16+32+64+128)

# Тестовые CROSS-коды (используются после вызова ovlGetCrossPoint)

CROSS_GETCOUNT = 3  # Для определения числа точек пересечения

# Флаги формирования высоты в точках трехмерной метрики

FLAG3D_NONE    = 0  # Результат не содержит трехмерной метрики
FLAG3D_TEMPLET = 2  # Третья координата выбирается из контура

# шаблона

FLAG3D_MATRIX = 8  # Третья координата выбирается из карты
FLAG3D_LINE   = 32  # Третья координата вычисляется по крайним

# точкам участка (методом линейной интерполяции)

FLAG3D_ALL = 42  # Совместное использование всех флагов

# Флаги типа результирующих контуров - флаги метода обработки

METHOD_LINE   = 0  # Замкнутые и незамкнутые контура линейных объектов
METHOD_SQUARE = 1  # Замкнутые контура (части object) площадных объектов
METHOD_FAST   = 16  # Быстрый способ обработки - используется только

# Флаги размещения результирующих контуров (используются в ovlSetObjectCross)

ANYOBJECT  = 0x000  # Поиск всех контуров
ANYOBJECT2 = 0x360  # Поиск всех контуров, включая отрезки

# контура равные отрезкам шаблона

OBJECTINSIDE  = 0x020  # Поиск контуров внутри шаблона
OBJECTINSIDE2 = 0x120  # Поиск контуров внутри шаблона, включая

# отрезки контура равные отрезкам шаблона

OBJECTOUTSIDE  = 0x040  # Поиск контуров вне шаблона
OBJECTOUTSIDE2 = 0x240  # Поиск контуров вне шаблона, включая
OBJECTOVERLAP  = 0x100  # Поиск совпадающих участков контуров

# Коды ошибок пересечений объектов, возвращаемые функцией ovlGetErrorCode

OVL_ERR_NONE                    = 0  # "Ошибок нет"
OVL_ERR_UNKNOWN                 = 1  # "Неизвестная ошибка"
OVL_ERR_PARAM                   = 2  # "Ошибка входных параметров"
OVL_ERR_LOCAL                   = 3  # "Ошибка локализации объекта"
OVL_ERR_STRUCT                  = 4  # "Ошибка структуры объекта"
OVL_ERR_LESSCOUNT               = 5  # "Число точек контура объекта меньше допустимого"
OVL_ERR_LESSCOUNT2              = 6  # "Число несовпадающих точек контура объекта меньше допустимого"
OVL_ERR_OVERCOUNT               = 7  # "Общее число точек объекта больше допустимого"
OVL_ERR_UNLOCKED                = 8  # "Контур площадного объекта незамкнут"
OVL_ERR_METHOD                  = 9  # "Контур объекта незамкнут. Ошибка заданного типа обработки"
OVL_ERR_MEMORY                  = 10  # "Ошибка при выделении памяти"
OVL_ERR_OVERCROSS               = 11  # "Число пересечений больше допустимого (буфер мал)"
OVL_ERR_ADDSUBJECT              = 12  # "Ошибка добавления подобъекта"
OVL_ERR_ADDPOINT                = 13  # "Ошибка добавления точки"
OVL_ERR_DELPOINT                = 14  # "Ошибка удаления точки"
OVL_ERR_SELFCROSSING            = 15  # "Обнаружено самопересечение контура объекта"
OVL_ERR_SELFCROSSING2           = 16  # "Обнаружено пересечение контуров объекта"
OVL_ERR_NOCROSS_OBJECTINSIDE    = 17  # "Пересечений нет. Объект находится внутри шаблона"
OVL_ERR_NOCROSS_OBJECTOUTSIDE   = 18  # "Пересечений нет. Объект находится вне шаблона"
OVL_ERR_TEMPLETOWNED            = 19  # "Контур объекта принадлежит контуру шаблона"
OVL_ERR_NOCROSS                 = 20  # "Ошибка обработки. Пересечений нет"
OVL_ERR_SUBJECT                 = 21  # "Входные параметры содержат ошибочный номер подобъекта шаблона"
OVL_ERR_SQUARE_LESSCOUNT        = 22  # "Площадной метод обработки. Число неравных точек контура шаблона менее 4"
OVL_ERR_SQUARE_UNLOCKEDTEMPLET  = 23  # "Площадной метод обработки. Контур шаблона незамкнут"
OVL_ERR_SQUARE_UNLOCKEDOBJECT   = 24  # "Площадной метод обработки. Контур объекта или подобъекта незамкнут"
OVL_ERR_INSIDE_LESSCOUNT        = 25  # "Поиск внутри области. Число неравных точек контура шаблона менее 4"
OVL_ERR_INSIDE_UNLOCKEDTEMPLET  = 26  # "Поиск внутри области. Контур шаблона незамкнут"
OVL_ERR_OUTSIDE_LESSCOUNT       = 27  # "Поиск вне области. Число неравных точек контура шаблона менее 4"
OVL_ERR_OUTSIDE_UNLOCKEDTEMPLET = 28  # "Поиск вне области. Контур шаблона незамкнут"
OVL_ERR_GETSIDE_LESSCOUNT       = 29  # "Определение положения. Число неравных точек контура шаблона менее 4"
OVL_ERR_GETSIDE_UNLOCKEDTEMPLET = 30  # "Определение положения. Контур шаблона незамкнут"
OVL_ERR_SUBJECTNUMBER           = 31  # "Запрос контура шаблона. Задан ошибочный номер подобъекта"
OVL_ERR_NOTEMPLET               = 32  # "Шаблон не установлен. Неправильный порядок вызова функций"
OVL_ERR_NOTEMPLET2              = 33  # "Шаблон не установлен. При проверке шаблона обнаружена ошибка"
OVL_ERR_NOOBJECT                = 34  # "Обрабатываемый объект не установлен. Неправильный порядок вызова функций"
OVL_ERR_NOOBJECT2               = 35  # "Обрабатываемый объект не установлен. При проверке объекта обнаружена ошибка"
OVL_ERR_SELFCROSSING_OFF        = 36  # "Ошибка обработки. Отключена проверка на самопересечение"
OVL_ERR_OVERCROSS_TEMPLET       = 37  # "Ошибка обработки. Превышено максимальное число точек шаблона"
OVL_ERR_OVERCROSS_OBJECT        = 38  # "Ошибка обработки. Превышено максимальное число точек объекта"
OVL_ERR_OVERCROSS_RESULT        = 39  # "Ошибка обработки. Превышено максимальное число точек формируемого объекта"
OVL_ERR_EXCEEDS_MAXIMUM         = 40  # "Число ошибок превышает максимальное"
OVL_ERR_SELFCROSSING_OVERLAY    = 41  # "Обнаружены частично совпадающие отрезки контура объекта"
OVL_ERR_SELFCROSSING_OVERLAY2   = 42  # "Обнаружены частично совпадающие отрезки контуров объекта"
OVL_ERR_SELFCROSSING_ADJACENT   = 43  # "Обнаружены примыкающие отрезки контура объекта"
OVL_ERR_SELFCROSSING_ADJACENT2  = 44  # "Обнаружены примыкающие отрезки контуров объекта"
OVL_ERR_CHECKING_NEARPOINT      = 45  # "Точки контура слишком близки"
OVL_ERR_CHECKING_NEARPOINT2     = 46  # "Точки контуров слишком близки"
OVL_ERR_CHECKING_PEAK           = 47  # "Выброс в точке контура"
OVL_ERR_CHECKING_DOUBLEPOINT    = 48  # "Обнаружены двойные точки"
OVL_ERR_CHECKING_DOUBLEPOINT2   = 49  # "Обнаружены двойные точки в допуске"
OVL_ERR_CHECKING_OBJECTINSIDE   = 50  # "Площадной объект внутри подобъекта"
OVL_ERR_CHECKING_SUBJECTINSIDE  = 51  # "Подобъект площадного объекта внутри подобъекта"
OVL_ERR_CHECKING_SUBJECTOUTSIDE = 52  # "Подобъект вне площадного объекта"
OVL_ERR_SELFCROSSING_EQUAL_AB   = 53  # "Обнаружены совпадающие отрезки контура объекта"
OVL_ERR_SELFCROSSING_EQUAL_AB2  = 54  # "Обнаружены совпадающие отрезки контуров объекта"
OVL_ERR_SELFCROSSING_EQUAL_BA   = 55  # "Обнаружены обратно совпадающие отрезки контура объекта"
OVL_ERR_SELFCROSSING_EQUAL_BA2  = 56  # "Обнаружены обратно совпадающие отрезки контуров объекта"
OVL_ERR_SELFCROSSING_EQUAL_LINE = 57  # "Обнаружены идентичные контура"
OVL_ERR_NOT_MULTIPOLYGON        = 58  # "Объект не является мультиполигоном"
OVL_ERR_MULTIPOLYGON_FLAG       = 59  # "Ошибочный флаг входимости контура мультиполигона"
OVL_ERR_MULTIPOLYGON_ORDER      = 60  # "Ошибочный порядок контуров мультиполигона"
OVL_ERR_MULTIPOLYGON_LEVEL      = 61  # "Превышен уровень вложенности контура (больше 2)"
OVL_ERR_END                     = 61  # Последний код штатных ошибок

# Типы контроля (используются в ovlCreateCheckObject)

OVL_TEST_STANDARD  = 1  # Поиск самопересечений и примыканий контуров (0-44,53-56)
OVL_TEST_NEARPOINT = 2  # Поиск близких точек и выбросов    (45-49)
OVL_TEST_LOCATION  = 4  # Определение расположения контуров (50-52)
OVL_TEST_ALL       = 7  # OVL_TEST_STANDARD | OVL_TEST_NEARPOINT | OVL_TEST_LOCATION


#-----------------------------
class ERRORDESC(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Point",maptype.DOUBLEPOINT),
                ("Code",ctypes.c_int),
                ("Object",ctypes.c_int),
                ("SubjectA",ctypes.c_int),
                ("SubjectB",ctypes.c_int),
                ("NumberA",ctypes.c_int),
                ("NumberB",ctypes.c_int)]
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
    ovlGetCrossPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'ovlGetCrossPoint', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double, ctypes.c_long)
    def ovlGetCrossPoint(_a1: ctypes.POINTER(maptype.DOUBLEPOINT), _a2: ctypes.POINTER(maptype.DOUBLEPOINT), _b1: ctypes.POINTER(maptype.DOUBLEPOINT), _b2: ctypes.POINTER(maptype.DOUBLEPOINT), _cp1: ctypes.POINTER(maptype.DOUBLEPOINT), _cp2: ctypes.POINTER(maptype.DOUBLEPOINT), _precision: float, _force: int) -> int:
        """
        Найти точку пересечения двух отрезков
        
        a1, a2    - точки первого отрезка (A)
        b1, b2    - точки второго отрезка (B)
        
        :param _cp1: первая точка пересечения
        
        :param _cp2: вторая точка пересечения
        
        :param _precision: точность, используемая для проверки равенства точек (рекомендуется ``DOUBLENULL``)
        
        :param _force: флаг выполнения дополнительного поиска (если равно ``1``, то учесть наличие отрезков нулевой длины)
        
        :returns: Возвращает CROSS-коды (code: CROSS_0, CROSS_1, CROSS_2 и другие). Число пересечений = (code & CROSS_GETCOUNT) ``= 0``,1,2 При ошибке параметров возвращает 0
        :rtype: int
        """
        return ovlGetCrossPoint_t (_a1, _a2, _b1, _b2, _cp1, _cp2, _precision, _force)

    ovlGetCrossPointReal_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'ovlGetCrossPointReal', ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.c_double)
    def ovlGetCrossPointReal(_crossCode: int, _a1: ctypes.POINTER(maptype.DOUBLEPOINT), _a2: ctypes.POINTER(maptype.DOUBLEPOINT), _b1: ctypes.POINTER(maptype.DOUBLEPOINT), _b2: ctypes.POINTER(maptype.DOUBLEPOINT), _cp1: ctypes.POINTER(maptype.DOUBLEPOINT), _cp2: ctypes.POINTER(maptype.DOUBLEPOINT), _precision: float) -> int:
        """
        Найти точку пересечения двух отрезков ненулевой длины
        
        :param _crossCode: код пересечения a1, a2    - точки первого отрезка (A) b1, b2    - точки второго отрезка (B)
        
        :param _cp1: первая точка пересечения
        
        :param _cp2: вторая точка пересечения
        
        :param _precision: точность, используемая для проверки равенства точек (рекомендуется ``DOUBLENULL`` для карты с максимальной точностью, ``0.01`` - сантиметровой точности, ``0.001`` - миллиметровой точности) Вызывать только если отсутствует равенство точек a1=a2 и b1=b2
        
        :returns: Возвращает CROSS-коды (code: CROSS_0, CROSS_1, CROSS_2 и другие). Число пересечений = (code & CROSS_GETCOUNT) ``= 0``,1,2 При ошибке параметров возвращает 0
        :rtype: int
        """
        return ovlGetCrossPointReal_t (_crossCode, _a1, _a2, _b1, _b2, _cp1, _cp2, _precision)

    ovlCrossTestFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'ovlCrossTestFrame', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DFRAME), ctypes.c_double)
    def ovlCrossTestFrame(_p1: ctypes.POINTER(maptype.DOUBLEPOINT), _p2: ctypes.POINTER(maptype.DOUBLEPOINT), _dframe: ctypes.POINTER(maptype.DFRAME), _precision: float) -> int:
        """
        Определить наличие пересечения отрезка p1p2 с прямоугольной рамкой dframe
        
        p1, p2    - точки отрезка
        
        :param _dframe: прямоугольная рамка
        
        :param _precision: точность, используемая для проверки равенства точек (позднее можно оптимизировать: при пересечении габаритов и если все точки рамки справа или все точки слева относительно линии, то пересечений нет)
        
        :returns: Возвращает: ``0`` - пересечений нет, ``1`` - пересечения есть При ошибке параметров возвращает 0
        :rtype: int
        """
        return ovlCrossTestFrame_t (_p1, _p2, _dframe, _precision)

    ovlDistance_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'ovlDistance', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def ovlDistance(_point: ctypes.POINTER(maptype.DOUBLEPOINT), _p1: ctypes.POINTER(maptype.DOUBLEPOINT), _p2: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        """
        Вычисление расстояния между точкой и прямой, заданной двумя точками
        
        :param _point: заданная точка p1, p2 - точки отрезка, определяющие линию
        
        :returns: При ошибке параметров возвращает 0
        :rtype: float
        """
        return ovlDistance_t (_point, _p1, _p2)

    ovlDistance2_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'ovlDistance2', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def ovlDistance2(_point: ctypes.POINTER(maptype.DOUBLEPOINT), _p1: ctypes.POINTER(maptype.DOUBLEPOINT), _p2: ctypes.POINTER(maptype.DOUBLEPOINT)) -> float:
        """
        Вычисление квадрата расстояния между точкой и прямой, заданной двумя точками
        
        :param _point: заданная точка p1, p2 - точки отрезка, определяющие линию Более быстрая функция по сравнению с ovlDistance
        
        :returns: При ошибке параметров возвращает 0
        :rtype: float
        """
        return ovlDistance2_t (_point, _p1, _p2)

    ovlSeekNearPointOnLine_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'ovlSeekNearPointOnLine', ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT), ctypes.POINTER(maptype.DOUBLEPOINT))
    def ovlSeekNearPointOnLine(_point: ctypes.POINTER(maptype.DOUBLEPOINT), _p1: ctypes.POINTER(maptype.DOUBLEPOINT), _p2: ctypes.POINTER(maptype.DOUBLEPOINT), _pres: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Найти точку на линии, ближайшую к заданной
        
        :param _point: заданная точка p1, p2 - точки отрезка, определяющие линию
        
        :param _pres: точка на линии (p1, p2), ближайшая к заданной (p)
        
        :returns: При ошибке параметров возвращает 0
        :rtype: int
        """
        return ovlSeekNearPointOnLine_t (_point, _p1, _p2, _pres)

    ovlGetLocationPoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'ovlGetLocationPoint', ctypes.POINTER(maptype.DOUBLEPOINT), maptype.HOBJ, ctypes.c_double)
    def ovlGetLocationPoint(_point: ctypes.POINTER(maptype.DOUBLEPOINT), _hobj: maptype.HOBJ, _precision: float) -> int:
        """
        Запросить расположение точки относительно замкнутого объекта (с учетом подобъектов)
        
        :param _point: координаты точки (в метрах)
        
        :param _hobj: замктутый площадной или линейный объект
        
        :param _precision: точность, используемая для проверки равенства точек. При precision <``= 0`` устанавливается ``DOUBLENULL``
        
        :returns: Возвращает: ``1`` - точка внутри объекта ``2`` - точка вне объекта ``3`` - точка лежит на контуре объекта При ошибке возвращает 0
        :rtype: int
        """
        return ovlGetLocationPoint_t (_point, _hobj, _precision)

    ovlCreate_t = mapsyst.GetProcAddress(acceslib,maptype.HOVL,'ovlCreate', maptype.HMAP, ctypes.c_long, ctypes.c_double)
    def ovlCreate(_hmap: maptype.HMAP, _flag: int, _precision: float) -> maptype.HOVL:
        """
        Создать объект оверлейных операций
        
        :param _hmap: идентификатор открытых данных (используется для запроса высоты при разрезании объекта с 3D-метрикой)
        
        :param _flag: флаг проверки контуров исходных объектов на самопересечение: ``1`` - проверка на самопересечение выполняется (рекомендуется) ``0`` - проверка на самопересечение отключена (используется для ускорения обработки в задачах визуализации).
        
        :param _precision: точность, используемая для проверки равенства точек При precision <``= 0`` устанавливается ``DOUBLENULL`` Объект позволяет: ``1`` Запросить расположение метрики объекта любой локализации относительно шаблона ``2`` Согласовать точки контура объекта с точками контура шаблона перед поиском пересечений (в пределах допуска) ``3`` Запросить метрику шаблона, топологически согласованную с частями разрезаемого объекта ``4`` Запросить все точки пересечения объектов ``5`` Запросить очередную часть разрезаемого объекта: ``5.1`` Рассечение контуров объектов по замкнутому контуру ``5.2`` Рассечение контуров объектов по незамкнутому контуру ``5.3`` Рассечение площадных объектов по замкнутому контуру При сохранении объектов в карту с точностью хуже precision результирующие контура могут содержать петли При округлении координат точек близко расположенные точки могут совпасть Разрезаемый объект карты и объект-шаблон должны быть в одной системе координат
        
        :returns: При использовании данного флага при обработке объектов, содержащих ошибки самопересечения, возвращается ошибка ``"Ошибка обработки. Отключена проверка на самопересечение"`` Возвращает идентификатор объекта оверлейных операций Для выгрузки из памяти вызывать функцию ovlFree При ошибке возвращает 0
        :rtype: maptype.HOVL
        """
        return ovlCreate_t (_hmap, _flag, _precision)

    ovlCreateCheckObject_t = mapsyst.GetProcAddress(acceslib,maptype.HOVL,'ovlCreateCheckObject', maptype.HOBJ, ctypes.c_long, ctypes.c_double)
    def ovlCreateCheckObject(_hobj: maptype.HOBJ, _test: int, _precision: float) -> maptype.HOVL:
        """
        Создать объект оверлейных операций для выполения контроля метрики объекта
        
        :param _hobj: обрабатываемый объект
        
        :param _test: тип контроля (допустимо совместное использование флагов): ``OVL_TEST_STANDARD`` (``1`` или ``0``) - поиск самопересечений и примыканий контуров: ``OVL_ERR_NONE``                      ``0`` - ``"Ошибок нет"`` ... ``OVL_ERR_SELFCROSSING_ADJACENT2``   ``44`` - ``"Обнаружены примыкающие отрезки контуров объекта"`` ``OVL_TEST_NEARPOINT`` (``2``) - поиск близких точек и выбросов: ``OVL_ERR_CHECKING_NEARPOINT``       ``45`` - ``"Точки контура слишком близки"`` ``OVL_ERR_CHECKING_NEARPOINT2``      ``46`` - ``"Точки контуров слишком близки"`` ``OVL_ERR_CHECKING_PEAK``            ``47`` - ``"Выброс в точке контура"`` ``OVL_ERR_CHECKING_DOUBLEPOINT``     ``48`` - ``"Обнаружены двойные точки"`` ``OVL_ERR_CHECKING_DOUBLEPOINT2``    ``49`` - ``"Обнаружены двойные точки в допуске"`` ``OVL_TEST_LOCATION`` (``4``) - определение расположения контуров: ``OVL_ERR_CHECKING_OBJECTINSIDE``    ``50`` - ``"Площадной объект внутри подобъекта"`` ``OVL_ERR_CHECKING_SUBJECTINSIDE``   ``51`` - ``"Подобъект площадного объекта внутри подобъекта"`` ``OVL_ERR_CHECKING_SUBJECTOUTSIDE``  ``52`` - ``"Подобъект вне площадного объекта"``
        
        :param _precision: точность, используемая для проверки равенства точек. При precision <``= 0`` устанавливается ``DOUBLENULL`` Обрабатываются только линейные или площадные объекты. Разрезаемый объект карты и объект-шаблон должны быть в одной системе координат. Для запроса результатов контроля использовать функции: ovlGetErrorCount, ovlGetErrorN, ovlGetErrorPointXN, ovlGetErrorPointYN Для выгрузки из памяти вызывать функцию ovlFree
        
        :returns: Возвращает идентификатор объекта оверлейных операций При ошибке возвращает ноль
        :rtype: maptype.HOVL
        """
        return ovlCreateCheckObject_t (_hobj, _test, _precision)

    ovlFree_t = mapsyst.GetProcAddress(acceslib,ctypes.c_void_p,'ovlFree', maptype.HOVL)
    def ovlFree(_hovl: maptype.HOVL) -> ctypes.c_void_p:
        """
        Освободить объект оверлейных операций
        
        :param _hovl: идентификатор объекта оверлейных операций
        """
        return ovlFree_t (_hovl)

    ovlSetTemplet_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'ovlSetTemplet', maptype.HOVL, maptype.HOBJ, ctypes.c_long, ctypes.c_long)
    def ovlSetTemplet(_hovl: maptype.HOVL, _templet: maptype.HOBJ, _subject: int, _adjust: int) -> int:
        """
        Установить шаблон для оверлейных операций
        
        :param _hovl: идентификатор объекта оверлейных операций
        
        :param _templet: шаблон, объект по контуру которого выполняются оверлейные операции
        
        :param _subject: номер контура, используемого в качестве шаблона (лекала) ``0`` - основной контур объекта templet, от ``1`` и более - подобъект объекта templet -``1`` - все контура объекта templet (используется только при обработке пересечений методом ``METHOD_LINE``, подробнее при описании  ovlSetObjectCross)
        
        :param _adjust: флаг согласования метрики контура шаблона с пересекаемыми объектами (``0``, ``1``). Выполняется вставка точек пересечений в контур Разрезаемый объект карты и объект-шаблон должны быть в одной системе координат Для запроса описания ошибок вызывать функции ovlGetErrorCount и ovlGetErrorN
        
        :returns: При ошибке возвращает ноль
        :rtype: int
        """
        return ovlSetTemplet_t (_hovl, _templet, _subject, _adjust)

    ovlSetTempletByFrame_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'ovlSetTempletByFrame', maptype.HOVL, ctypes.POINTER(maptype.DFRAME))
    def ovlSetTempletByFrame(_hovl: maptype.HOVL, _templet: ctypes.POINTER(maptype.DFRAME)) -> int:
        """
        Установить шаблон для оверлейных операций по габаритам прямоугольника
        
        :param _hovl: идентификатор объекта оверлейных операций
        
        :param _templet: шаблон, объект по контуру которого выполняются оверлейные операции Разрезаемый объект карты и шаблон должны быть в одной системе координат Для запроса описания ошибок вызывать функции ovlGetErrorCount и ovlGetErrorN
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return ovlSetTempletByFrame_t (_hovl, _templet)

    ovlSetObjectCross_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'ovlSetObjectCross', maptype.HOVL, maptype.HOBJ, ctypes.c_long, ctypes.c_double, ctypes.c_long, ctypes.c_long, ctypes.c_long)
    def ovlSetObjectCross(_hovl: maptype.HOVL, _hobj: maptype.HOBJ, _subject: int, _precision: float, _flag3d: int, _method: int, _location: int) -> int:
        """
        Установить обрабатываемый объект и метод обработки
        
        :param _hovl: идентификатор объекта оверлейных операций
        
        :param _hobj: обрабатываемый объект
        
        :param _subject: номер обрабатываемого контура: -``1`` - обработать все контура ``0`` - основной контур объекта, от ``1`` и более - подобъект объекта
        
        :param _precision: точность согласования точек объекта с точками шаблона (``DOUBLENULL`` и выше). Выполняется обновление точек объекта. Используется для сохранения контуров близлежащих объектов.
        
        :param _flag3d: флаг формирования высоты в точках трехмерной метрики, соответствующих участкам контуров шаблона: ``FLAG3D_NONE``    ``0`` - результат не содержит трехмерной метрики ``FLAG3D_TEMPLET`` ``2`` - третья координата выбирается из контура шаблона ``FLAG3D_MATRIX``  ``8`` - третья координата выбирается из карты (по наиболее точной открытой матрице высот) ``FLAG3D_LINE``   ``32`` - третья координата вычисляется по крайним точкам участка, не содержащего высоты (методом линейной интерполяции) ``FLAG3D_ALL``    ``42`` - совместное использование всех флагов ``FLAG3D_TEMPLET``|``FLAG3D_MATRIX``|``FLAG3D_LINE`` Допускается совместное использование флагов: ``FLAG3D_TEMPLET``|``FLAG3D_MATRIX``, ``FLAG3D_MATRIX``|``FLAG3D_LINE``, ``FLAG3D_TEMPLET``|``FLAG3D_LINE`` При совместном использовании используется приоритет выполнения: ``FLAG3D_TEMPLET`` -> ``FLAG3D_MATRIX`` -> ``FLAG3D_LINE``
        
        :param _method: флаг типа результирующих контуров (флаги метода обработки): ``METHOD_LINE``   ``0`` - замкнутые и незамкнутые контура линейных объектов ``METHOD_SQUARE`` ``1`` - замкнутые контура (части hobj) площадных объектов ``METHOD_FAST``  ``16`` - быстрый способ обработки - используется только для объектов, которые не содержат самопересечений
        
        :param _location: флаги размещения результирующих контуров: ``ANYOBJECT`` или ``0`` - поиск всех контуров ``ANYOBJECT2`` - поиск всех контуров, включая отрезки контура равные отрезкам шаблона ``OBJECTINSIDE`` - поиск контуров внутри шаблона ``OBJECTINSIDE2`` - поиск контуров внутри шаблона, включая отрезки контура равные отрезкам шаблона ``OBJECTOUTSIDE`` - поиск контуров вне шаблона ``OBJECTOUTSIDE2`` - поиск контуров вне шаблона, включая отрезки контура равные отрезкам шаблона ``OBJECTOVERLAP`` - поиск совпадающих участков контуров Допускается совместное использование флагов: ``OBJECTINSIDE``|``OBJECTOUTSIDE``, ``OBJECTINSIDE2``|``OBJECTOUTSIDE``, ``OBJECTINSIDE``|``OBJECTOUTSIDE2``, ``OBJECTINSIDE2``|``OBJECTOUTSIDE2``
        
        :returns: по первой точке первого подобъекта, а функция ovlSetObjectCross возвращает: ``1`` - объект внутри шаблона ``2`` - объект вне шаблона (ovlGetNextObject не вызывать) Если контур шаблона НЕ ЗАМКНУТ, то ovlSetObjectCross возвращает: ``1`` - все контура объекта совпадают с шаблоном (лежат на шаблоне) ``2`` - все контура объекта вне шаблона ``3`` - один или несколько контуров объекта пересекаются с шаблоном При возврате 3 вызывать ovlGetNextObject в цикле Если контур шаблона ЗАМКНУТ и method =``= 0``, то ovlSetObjectCross возвращает: ``1`` - все контура объекта внутри шаблона либо совпадают ``2`` - все контура объекта вне шаблона ``3`` - один или несколько контуров объекта пересекаются с шаблоном, либо обнаружены внутренние и внешние контура (относительно шаблона) Если контур шаблона ЗАМКНУТ и method =``= 1``, то ovlSetObjectCross возвращает: ``1`` - все контура объекта внутри шаблона либо совпадают ``2`` - все контура объекта вне шаблона ``3`` - один или несколько контуров объекта пересекаются с шаблоном, либо обнаружены внутренние и внешние контура (относительно шаблона) ``4`` - контур шаблона внутри контура объекта При возврате 3 и 4 вызывать ovlGetNextObject в цикле Если location == OBJECTOVERLAP, то ovlSetObjectCross возвращает: ``0`` - число несовпадающих точек контура объекта ``< 2`` (проверка не выполняется) ``1`` - все контура объекта совпадают с шаблоном (лежат на шаблоне) ``2`` - все контура объекта вне шаблона ``3`` - один или несколько контуров объекта пересекаются с шаблоном Для запроса кода ошибки вызывать функции GetErrorCode и GetError При ошибке возвращает 0
        :rtype: int
        
        .. note::

           Рекомендуется precision = ``0.001`` (метров на местности)
           Если исходный объект не содержит трехмерную метрику, то допустим только метод 0
           Если контур шаблона не замкнут, то допустим только метод METHOD_LINE.
           Допускается совместное использование флагов:
           METHOD_LINE|METHOD_FAST, METHOD_SQUARE|METHOD_FAST
           Если объект точечный, векторный, подпись или шаблон, то параметры
           precision, method, location игнорируются. Положение объекта определяется
        """
        return ovlSetObjectCross_t (_hovl, _hobj, _subject, _precision, _flag3d, _method, _location)

    ovlGetNextObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'ovlGetNextObject', maptype.HOVL, maptype.HOBJ)
    def ovlGetNextObject(_hovl: maptype.HOVL, _hobj: maptype.HOBJ) -> int:
        """
        Запросить очередную часть разрезаемого объекта
        
        :param _hovl: идентификатор объекта оверлейных операций
        
        :param _hobj: объект для возврата результата. Для получения наилучших результатов тип метрики объекта должен быть равен ``IDDOUBLE2`` или ``IDDOUBLE3`` Вызывать после ovlSetObjectCross в цикле до тех пор, пока не вернет ``0`` Для запроса описания ошибок вызывать функции ovlGetErrorCount и ovlGetErrorN
        
        :returns: Если контур шаблона ЗАМКНУТ, то ovlGetNextObject возвращает: ``1`` - контур объекта внутри шаблона (часть контура может совпадать с контуром шаблона), либо совпадает с контуром шаблона ``2`` - контур объекта вне шаблона (часть контура может совпадать с контуром шаблона) ``0`` - контуров больше нет, либо при ошибке Если контур шаблона НЕ ЗАМКНУТ, то ovlGetNextObject возвращает: ``1`` - контур объекта совпадает с контуром шаблона (лежит на шаблоне) ``2`` - контур объекта вне шаблона (контур может касаться шаблона одной или двумя точками) ``0`` - контуров больше нет, либо при ошибке Если в функции ovlSetObjectCross установлено location == OBJECTOVERLAP, то ovlGetNextObject возвращает: ``1`` - контур совпадает (Поиск совпадающих участков контуров) ``2`` - контур не совпадает ``0`` - контуров больше нет, либо при ошибке При возврате 0 необходимо проверить код ошибки. Для запроса описания ошибок вызывать функции ovlGetErrorCount и ovlGetErrorN
        :rtype: int
        """
        return ovlGetNextObject_t (_hovl, _hobj)

    ovlIsEditTemplet_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'ovlIsEditTemplet', maptype.HOVL)
    def ovlIsEditTemplet(_hovl: maptype.HOVL) -> int:
        """
        Запросить признак изменения метрики шаблона, согласованного с метрикой объекта
        
        :param _hovl: идентификатор объекта оверлейных операций При вызове функции ovlSetObjectCross в метрику шаблона вставляются точки пересечения контуров шаблона и объекта
        
        :returns: Возвращает: ``1`` - метрика изменена, ``0`` - метрика не изменена
        :rtype: int
        """
        return ovlIsEditTemplet_t (_hovl)

    ovlIsEditObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'ovlIsEditObject', maptype.HOVL)
    def ovlIsEditObject(_hovl: maptype.HOVL) -> int:
        """
        Запросить признак изменения метрики объекта, согласованного с метрикой шаблона
        
        :param _hovl: идентификатор объекта оверлейных операций При вызове функции ovlSetObjectCross в метрику объекта вставляются точки пересечения контуров шаблона и объекта
        
        :returns: Возвращает: ``1`` - метрика изменена, ``0`` - метрика не изменена
        :rtype: int
        """
        return ovlIsEditObject_t (_hovl)

    ovlGetAdjustTemplet_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'ovlGetAdjustTemplet', maptype.HOVL, maptype.HOBJ, ctypes.c_long)
    def ovlGetAdjustTemplet(_hovl: maptype.HOVL, _templet: maptype.HOBJ, _subject: int) -> int:
        """
        Запросить метрику шаблона, согласованную с метрикой объекта
        
        :param _hovl: идентификатор объекта оверлейных операций
        
        :param _templet: объект для возврата результата
        
        :param _subject: номер сохраняемого подобъекта: ``0`` или больше - записать только один контур шаблона -``1`` - записать все контура шаблона При вызове функции ovlSetObjectCross в метрику шаблона вставляются точки пересечения контуров шаблона и объекта Для запроса кода ошибки вызывать функции ovlGetErrorCode и ovlGetError
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return ovlGetAdjustTemplet_t (_hovl, _templet, _subject)

    ovlGetAdjustObject_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'ovlGetAdjustObject', maptype.HOVL, maptype.HOBJ, ctypes.c_long)
    def ovlGetAdjustObject(_hovl: maptype.HOVL, _hobj: maptype.HOBJ, _subject: int) -> int:
        """
        Запросить метрику объекта, согласованную с метрикой шаблона
        
        :param _hovl: идентификатор объекта оверлейных операций
        
        :param _hobj: объект для возврата результата
        
        :param _subject: номер сохраняемого подобъекта: ``0`` или больше - записать только один контур объекта -``1`` - записать все контура объекта При вызове функции ovlSetObjectCross в метрику объекта вставляются точки пересечения контуров шаблона и объекта Для запроса кода ошибки вызывать функции ovlGetErrorCode и ovlGetError
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return ovlGetAdjustObject_t (_hovl, _hobj, _subject)

    ovlGetCrossPoints_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'ovlGetCrossPoints', maptype.HOVL, maptype.HOBJ)
    def ovlGetCrossPoints(_hovl: maptype.HOVL, _hobj: maptype.HOBJ) -> int:
        """
        Запросить все точки пересечения объектов
        
        :param _hovl: идентификатор объекта оверлейных операций
        
        :param _hobj: объект для возврата результата Точки пересечения записываются в объект. Точки пересечения каждого контура обрабатываемого объекта записываются в отдельные контура Для запроса кода ошибки вызывать функции ovlGetErrorCode и ovlGetError
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return ovlGetCrossPoints_t (_hovl, _hobj)

    ovlGetErrorCode_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'ovlGetErrorCode', maptype.HOVL)
    def ovlGetErrorCode(_hovl: maptype.HOVL) -> int:
        """
        Запросить код ошибки
        
        :param _hovl: идентификатор объекта оверлейных операций
        
        :returns: Возвращает код ошибки (OVL_ERR_NONE, ...)
        :rtype: int
        """
        return ovlGetErrorCode_t (_hovl)

    ovlGetErrorUn_t = mapsyst.GetProcAddress(acceslib,maptype.PWCHAR,'ovlGetErrorUn', maptype.HOVL)
    def ovlGetErrorUn(_hovl: maptype.HOVL) -> mapsyst.WTEXT:
        """
        Запросить описание ошибки
        
        :param _hovl: идентификатор объекта оверлейных операций Ошибка обнуляется для дальнейшего использования объекта оверлейных операций
        
        :returns: Возвращает описание ошибки
        :rtype: mapsyst.WTEXT
        """
        return ovlGetErrorUn_t (_hovl)

    ovlGetErrorTextUn_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'ovlGetErrorTextUn', ctypes.c_long, maptype.PWCHAR, ctypes.c_long)
    def ovlGetErrorTextUn(_ovlerror: int, _text: mapsyst.WTEXT, _size: int) -> int:
        """
        Запросить описание ошибки оверлейных операций по коду ошибки
        
        :param _ovlerror: код ошибки, полученный из функции ovlGetErrorCode
        
        :param _text: указатель на буфер для записи описания ошибки
        
        :param _size: размер буфера в байтах
        
        :returns: Возвращает описание ошибки
        :rtype: int
        """
        return ovlGetErrorTextUn_t (_ovlerror, _text.buffer(), _size)

    ovlGetErrorCount_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'ovlGetErrorCount', maptype.HOVL)
    def ovlGetErrorCount(_hovl: maptype.HOVL) -> int:
        """
        Запросить число ошибок
        
        :param _hovl: идентификатор объекта оверлейных операций
        
        :returns: Возвращает число ошибок
        :rtype: int
        """
        return ovlGetErrorCount_t (_hovl)

    ovlGetErrorCodeN_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'ovlGetErrorCodeN', maptype.HOVL, ctypes.c_long)
    def ovlGetErrorCodeN(_hovl: maptype.HOVL, _number: int) -> int:
        """
        Запросить код ошибки
        
        :param _hovl: идентификатор объекта оверлейных операций
        
        :param _number: порядковый номер ошибки (от ``1`` до ovlGetErrorCount)
        
        :returns: Возвращает код ошибки (OVL_ERR_NONE, ...)
        :rtype: int
        """
        return ovlGetErrorCodeN_t (_hovl, _number)

    ovlGetErrorNUn_t = mapsyst.GetProcAddress(acceslib,ctypes.POINTER(maptype.WCHAR),'ovlGetErrorNUn', maptype.HOVL, ctypes.c_long)
    def ovlGetErrorNUn(_hovl: maptype.HOVL, _number: int) -> ctypes.POINTER(maptype.WCHAR):
        """
        Запросить описание ошибки
        
        :param _hovl: идентификатор объекта оверлейных операций
        
        :param _number: порядковый номер ошибки (от ``1`` до ovlGetErrorCount) Ошибка обнуляется для дальнейшего использования объекта оверлейных операций
        
        :returns: Возвращает описание ошибки на русском языке
        :rtype: ctypes.POINTER(maptype.WCHAR)
        """
        return ovlGetErrorNUn_t (_hovl, _number)

    ovlGetErrorMapPlanePoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'ovlGetErrorMapPlanePoint', maptype.HOVL, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT))
    def ovlGetErrorMapPlanePoint(_hovl: maptype.HOVL, _number: int, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Запросить координаты точки, содержащей ошибку в системе координат карты
        
        :param _hovl: идентификатор объекта оверлейных операций
        
        :param _number: порядковый номер ошибки (от ``1`` до ovlGetErrorCount)
        
        :param _point: буфер для записи координат
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return ovlGetErrorMapPlanePoint_t (_hovl, _number, _point)

    ovlGetErrorPlanePoint_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'ovlGetErrorPlanePoint', maptype.HOVL, ctypes.c_long, ctypes.POINTER(maptype.DOUBLEPOINT))
    def ovlGetErrorPlanePoint(_hovl: maptype.HOVL, _number: int, _point: ctypes.POINTER(maptype.DOUBLEPOINT)) -> int:
        """
        Запросить координаты точки, содержащей ошибку в системе координат документа
        
        :param _hovl: идентификатор объекта оверлейных операций
        
        :param _number: порядковый номер ошибки (от ``1`` до ovlGetErrorCount)
        
        :param _point: буфер для записи координат
        
        :returns: При ошибке возвращает 0
        :rtype: int
        """
        return ovlGetErrorPlanePoint_t (_hovl, _number, _point)

    ovlGetErrorPointXN_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'ovlGetErrorPointXN', maptype.HOVL, ctypes.c_long)
    def ovlGetErrorPointXN(_hovl: maptype.HOVL, _number: int) -> float:
        """
        Запросить координату X точки, содержащей ошибку в системе координат документа
        
        :param _hovl: идентификатор объекта оверлейных операций
        
        :param _number: порядковый номер ошибки (от ``1`` до ovlGetErrorCount)
        
        :returns: При обнаружении самопересечения контура возвращает точку, содержащую ошибку. При обнаружении ошибки при обработке шаблона возвращает первую точку шаблона. В остальных случаях возвращает первую точку обрабатываемого объекта При ошибке возвращает ``0.0``
        :rtype: float
        """
        return ovlGetErrorPointXN_t (_hovl, _number)

    ovlGetErrorPointYN_t = mapsyst.GetProcAddress(acceslib,ctypes.c_double,'ovlGetErrorPointYN', maptype.HOVL, ctypes.c_long)
    def ovlGetErrorPointYN(_hovl: maptype.HOVL, _number: int) -> float:
        """
        Запросить координату Y точки, содержащей ошибку в системе координат документа
        
        :param _hovl: идентификатор объекта оверлейных операций
        
        :param _number: порядковый номер ошибки (от ``1`` до ovlGetErrorCount)
        
        :returns: При обнаружении самопересечения контура возвращает точку, содержащую ошибку. При обнаружении ошибки при обработке шаблона возвращает первую точку шаблона. В остальных случаях возвращает первую точку обрабатываемого объекта При ошибке возвращает ``0.0``
        :rtype: float
        """
        return ovlGetErrorPointYN_t (_hovl, _number)

    ovlGetErrorDesc_t = mapsyst.GetProcAddress(acceslib,ctypes.c_long,'ovlGetErrorDesc', maptype.HOVL, ctypes.c_long, ctypes.POINTER(ERRORDESC))
    def ovlGetErrorDesc(_hovl: maptype.HOVL, _number: int, _errordesc: ctypes.POINTER(ERRORDESC)) -> int:
        """
        Запросить данные об ошибке
        
        :param _hovl: идентификатор объекта оверлейных операций
        
        :param _number: порядковый номер ошибки (от ``1`` до ovlGetErrorCount)
        
        :param _errordesc: данные об ошибке (заполняются только при обнаружении ошибки)
        
        :returns: Возвращает код ошибки (OVL_ERR_NONE, ...) При ошибке возвращает 0
        :rtype: int
        """
        return ovlGetErrorDesc_t (_hovl, _number, _errordesc)



def crossapi_healthcheck():
    return 1
