#!/usr/bin/env python3

# ********************************************************************
# *                                                                  *
# *              Copyright (c) PANORAMA Group 1991-2026              *
# *                      All Rights Reserved                         *
# *                                                                  *
# ********************************************************************
# *                                                                  *
# *         Классификация параметров систем координат карты          *
# *                                                                  *
# ********************************************************************

import ctypes
import maptype

TOPOGRAPHIC  = 1      # Топографическая (СК42), требует осевой меридиан
CK_42        = 1      # Система координат 42 года, требует осевой меридиан (EPSG:28401-28460)
GEOGRAPHIC   = 2      # Обзорно-географическая (тип и эллипсоид зависят от параметров)
GLOBE        = 3      # Космонавигационная (ГЛОБУС, цилиндрическая на эллипсоиде Красовского)
CITYPLAN     = 4      # Топографический план города (СК42 с произвольными номенклатурами)
LARGESCALE   = 5      # Крупномасштабный план местности
AERONAUTIC   = 6      # Аэронавигационная
SEANAUTICOLD = 7      # Цилиндрическая Меркатора, имеет нестандартные коэффициенты пересчета
                      # плоских координат
AVIATION     = 8      # Авиационная (Цилиндрическая на эллипсоиде Красовского)
BLANK        = 9      # Бланковка (Цилиндрическая на эллипсоиде Красовского)
UTMNAD27     = 10     # UTM на North American Datum 1927, требует осевой меридиан
UTMWGS84     = 11     # UTM на WGS84, требует осевой меридиан (XXN - EPSG:32601-32660, XXS - EPSG:32701-32760)
UTMTYPE      = 12     # UTM, требует осевой меридиан
CK_63        = 13     # Система координат 63 года, требует осевой меридиан
CK_95        = 14     # Система координат 95 года, требует осевой меридиан (EPSG:20001-20060)
TOPOLOCAL    = 15     # Топографическая с произвольной главной точкой, требует осевой меридиан
MAPSPHERE    = 16     # Обзорно-географическая Широта/Долгота на "шаре",
                      # можно выбрать эллипсоид
WORLDMAP     = 17     # Карта Мира (Цилиндрическая Миллера), можно выбрать эллипсоид (EPSG:54003)
MCK_CK63     = 18     # Местная система координат на базе СК-63
MERCATOR     = 19     # Цилиндрическая Меркатора на шаре "World Mercator" (EPSG:3857, EPSG:3395)
                      # (аналог Google), можно выбрать эллипсоид
SEANAUTIC    = 20     # Морская навигационная (Mercator_2SP), можно выбрать эллипсоид
                      # (Цилиндрическая равноугольная Меркатора на эллипсоиде WGS84)
GCK_2011     = 21     # Система координат ГСК-2011, требует осевой меридиан (EPSG:80201101-80201160)
VN_2000      = 22     # Система координат VN-2000, требует осевой меридиан (EPSG:3405, EPSG:3406)
VN_2000_TM3  = 23     # Система координат VN-2000/TM-3, требует осевой меридиан (EPSG:6956-EPSG:6959)
Pulkovo2017  = 24     # Система координат на основе ПЗ-90.11, требует осевой меридиан (EPSG:80011001-80011060)


PACK_WIDTH = 1

#-----------------------------
class LISTREGISTER(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Nomenclature",ctypes.c_char*32),
                ("ListName",ctypes.c_char*32),
                ("FileName",ctypes.c_char*260),
                ("XSouthWest",ctypes.c_double),
                ("YSouthWest",ctypes.c_double),
                ("XNorthWest",ctypes.c_double),
                ("YNorthWest",ctypes.c_double),
                ("XNorthEast",ctypes.c_double),
                ("YNorthEast",ctypes.c_double),
                ("XSouthEast",ctypes.c_double),
                ("YSouthEast",ctypes.c_double),
                ("BSouthWestCoordinate",ctypes.c_double),
                ("LSouthWestCoordinate",ctypes.c_double),
                ("BNorthWestCoordinate",ctypes.c_double),
                ("LNorthWestCoordinate",ctypes.c_double),
                ("BNorthEastCoordinate",ctypes.c_double),
                ("LNorthEastCoordinate",ctypes.c_double),
                ("BSouthEastCoordinate",ctypes.c_double),
                ("LSouthEastCoordinate",ctypes.c_double),
                ("MaterialKind",ctypes.c_int),
                ("MaterialType",ctypes.c_int),
                ("ReliefHeight",ctypes.c_int),
                ("Date",ctypes.c_char*12),
                ("MagneticAngle",ctypes.c_double),
                ("YearMagneticAngle",ctypes.c_double),
                ("MeridianAngle",ctypes.c_double),
                ("DateAngle",ctypes.c_char*12),
                ("UpdateDate",ctypes.c_uint),
                ("UpdateTime",ctypes.c_uint),
                ("HeightSystem",ctypes.c_int),
                ("Limit63Data",ctypes.c_uint),
                ("Reserve",ctypes.c_char*12)]
#-----------------------------


#-----------------------------
class MAPREGISTER(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Name",ctypes.c_char*32),
                ("Scale",ctypes.c_int),
                ("EPSGCode",ctypes.c_int),
                ("EllipsoidKind",ctypes.c_int),
                ("HeightSystem",ctypes.c_int),
                ("MaterialProjection",ctypes.c_int),
                ("CoordinateSystem",ctypes.c_int),
                ("PlaneUnit",ctypes.c_int),
                ("HeightUnit",ctypes.c_int),
                ("FrameKind",ctypes.c_int),
                ("MapType",ctypes.c_int),
                ("DeviceCapability",ctypes.c_int),
                ("DataProjection",ctypes.c_int),
                ("ZoneIdent",ctypes.c_int),
                ("FlagRealPlace",ctypes.c_int),
                ("ZoneNumber",ctypes.c_int),
                ("FirstMainParallel",ctypes.c_double),
                ("SecondMainParallel",ctypes.c_double),
                ("AxisMeridian",ctypes.c_double),
                ("MainPointParallel",ctypes.c_double)]
#-----------------------------


#-----------------------------
class MAPREGISTEREX(MAPREGISTER):
    _pack_ = PACK_WIDTH
    _fields_ = [("PoleLatitude",ctypes.c_double),
                ("PoleLongitude",ctypes.c_double),
                ("FalseEasting",ctypes.c_double),
                ("FalseNorthing",ctypes.c_double),
                ("ScaleFactor",ctypes.c_double),
                ("TurnAngle",ctypes.c_double),
                ("DataAxis",ctypes.c_double),
                ("Reserv2",ctypes.c_double*3)]
#-----------------------------


#-----------------------------
class ELLIPSOIDPARAM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("SemiMajorAxis",ctypes.c_double),
                ("InverseFlattening",ctypes.c_double)]
#-----------------------------


#-----------------------------
class LOCALDATUMPARAM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("DX",ctypes.c_double),
                ("DY",ctypes.c_double),
                ("DZ",ctypes.c_double),
                ("RX",ctypes.c_double),
                ("RY",ctypes.c_double),
                ("RZ",ctypes.c_double),
                ("M",ctypes.c_double)]
#-----------------------------


#-----------------------------
class LOCALDATUMPARAMEX(LOCALDATUMPARAM):
    _pack_ = PACK_WIDTH
    _fields_ = [("X",ctypes.c_double),
                ("Y",ctypes.c_double),
                ("Z",ctypes.c_double)]
#-----------------------------


#-----------------------------
class DATUMPARAM(LOCALDATUMPARAM):
    _pack_ = PACK_WIDTH
    _fields_ = [("Count",ctypes.c_int),
                ("Reserve",ctypes.c_int)]
#-----------------------------


#-----------------------------
class DATUMPARAMEX(LOCALDATUMPARAMEX):
    _pack_ = PACK_WIDTH
    _fields_ = [("Count",ctypes.c_int),
                ("Reserve",ctypes.c_int)]
#-----------------------------


#-----------------------------
class SHEETNAMES(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Nomenclature",maptype.WCHAR1*(232*2)),
                ("Reserve1",maptype.WCHAR1*(24*2)),
                ("ListName",maptype.WCHAR1*(232*2)),
                ("Reserve2",maptype.WCHAR1*(24*2)),
                ("FileName",maptype.WCHAR1*(232*2)),
                ("Ident",ctypes.c_char*34),
                ("Reserve3",ctypes.c_char*14)]
#-----------------------------


#-----------------------------
class EPSGGEODSYS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("GeodSysCode",ctypes.c_int),
                ("UnitCode",ctypes.c_int),
                ("EllipsoidCode",ctypes.c_int),
                ("DatumCode",ctypes.c_int),
                ("GeodSysName",ctypes.c_char*256),
                ("EllipsoidName",ctypes.c_char*256),
                ("DatumName",ctypes.c_char*256)]
#-----------------------------


#-----------------------------
class EPSGRECTSYS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("RectSysCode",ctypes.c_int),
                ("GeodSysCode",ctypes.c_int),
                ("UnitCode",ctypes.c_int),
                ("ProjectionCode",ctypes.c_int),
                ("XDirection",ctypes.c_int),
                ("YDirection",ctypes.c_int),
                ("RectSysName",ctypes.c_char*256)]
#-----------------------------


#-----------------------------
class EPSGMEASUNIT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("UnitCode",ctypes.c_int),
                ("UnitType",ctypes.c_int),
                ("Factor",ctypes.c_double),
                ("Name",ctypes.c_char*128)]
#-----------------------------


#-----------------------------
class OFFSETSCALEROTATE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Angle",ctypes.c_double),
                ("Scale",ctypes.c_double),
                ("dX",ctypes.c_double),
                ("dY",ctypes.c_double)]
#-----------------------------


#-----------------------------
class LOCALTRANSFORM(ctypes.Union):
    _pack_ = PACK_WIDTH
    _fields_ = [("Rotate",OFFSETSCALEROTATE),
                ("Affine",maptype.AFFINCOEFBASE),
                ("Total",ctypes.c_double*10)]
#-----------------------------


#-----------------------------
class METAINFO(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Count",ctypes.c_int),
                ("RscName",maptype.WCHAR1*(256*2)),
                ("SheetName",maptype.WCHAR1*(256*2)),
                ("SecurityCode",ctypes.c_int),
                ("MatchingFlag",ctypes.c_int)]
#-----------------------------


def mapcreat_healthcheck(): 
    return 1