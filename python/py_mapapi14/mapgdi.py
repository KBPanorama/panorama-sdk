#!/usr/bin/env python3

# ********************************************************************
# *                                                                  *
# *              Copyright (c) PANORAMA Group 1991-2026              *
# *                      All Rights Reserved                         *
# *                                                                  *
# ********************************************************************
# *                                                                  *
# *      Описание параметров функций визуализации произвольных       *
# *             графических объектов электронной карты               *
# *                                                                  *
# ********************************************************************

import ctypes
import maptype

IMG_LINE   = 128  # Линия
IMG_DOT    = 129  # Пунктир
IMG_SQUARE = 135  # Полигон
IMG_RECT   = 139  # Квадрат
IMG_CIRCLE = 140  # Окружность
IMG_TEXT   = 142  # Подпись

IMLPARMCOUNT = 32; # Число примитивов (переменное)
IMLLISTCOUNT = 64  # Число функций (переменное)


PACK_WIDTH = 1

#-----------------------------
class PAINTPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Image",ctypes.c_int),
                ("Mode",ctypes.c_int),
                ("Parm",ctypes.c_char_p)]
#-----------------------------


#-----------------------------
class TEXTRECORD(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Text",ctypes.c_char*256)]
#-----------------------------


#-----------------------------
class PLACEDATA(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Points",ctypes.POINTER(maptype.DOUBLEPOINT)),
                ("PolyCounts",ctypes.POINTER(ctypes.c_int)),
                ("Count",ctypes.c_int),
                ("Flags",ctypes.c_int),
                ("PolyText",ctypes.POINTER(TEXTRECORD))]
#-----------------------------


#-----------------------------
class PAINTEXAMPLEEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Hdc",maptype.HDC),
                ("Rect",ctypes.POINTER(maptype.RECT)),
                ("Data",ctypes.POINTER(maptype.POLYDATAEX)),
                ("Parm",ctypes.POINTER(ctypes.c_char)),
                ("Text",maptype.PWCHAR),
                ("Palette",ctypes.POINTER(maptype.COLORREF)),
                ("Func",ctypes.c_int),
                ("Local",ctypes.c_int),
                ("Factor",ctypes.c_float),
                ("Colors",ctypes.c_int),
                ("VisualType",ctypes.c_int),
                ("FillIntensity",ctypes.c_int),
                ("Reserve",ctypes.c_char*16)]
#-----------------------------


#-----------------------------
class IMGLINE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Color",ctypes.c_uint),
                ("Thick",ctypes.c_uint)]
#-----------------------------


#-----------------------------
class IMGTHICKENLINE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Color",ctypes.c_uint),
                ("Thick",ctypes.c_uint),
                ("Thick2",ctypes.c_uint)]
#-----------------------------


#-----------------------------
class IMGDOT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Color",ctypes.c_uint),
                ("Thick",ctypes.c_uint),
                ("Dash",ctypes.c_uint),
                ("Blank",ctypes.c_uint)]
#-----------------------------


#-----------------------------
class IMGSQUARE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Color",ctypes.c_uint)]
#-----------------------------


#-----------------------------
class IMGRECT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Color",ctypes.c_uint),
                ("Thick",ctypes.c_uint),
                ("BkgndColor",ctypes.c_uint),
                ("Side",ctypes.c_uint)]
#-----------------------------


#-----------------------------
class IMGCIRCLE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Color",ctypes.c_uint),
                ("Thick",ctypes.c_uint),
                ("Radius",ctypes.c_uint)]
#-----------------------------


#-----------------------------
class IMGTEXT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Color",ctypes.c_uint),
                ("BkgndColor",ctypes.c_uint),
                ("ShadowColor",ctypes.c_uint),
                ("Height",ctypes.c_uint),
                ("Weight",ctypes.c_ushort),
                ("Outline",ctypes.c_byte),
                ("Interval",ctypes.c_byte),
                ("Align",ctypes.c_ushort),
                ("Service",ctypes.c_ushort),
                ("Wide",ctypes.c_byte),
                ("Horizontal",ctypes.c_byte),
                ("Italic",ctypes.c_byte),
                ("Underline",ctypes.c_byte),
                ("StrikeOut",ctypes.c_byte),
                ("Type",ctypes.c_byte),
                ("CharSet",ctypes.c_byte),
                ("Flag",ctypes.c_byte)]
#-----------------------------


#-----------------------------
class IMGMARKCHAIN(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Color",ctypes.c_uint),
                ("Bits",ctypes.c_byte*128)]
#-----------------------------


#-----------------------------
class IMGMULTIMARKSIZE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Label",ctypes.c_uint),
                ("CopyLength",ctypes.c_uint),
                ("Left",ctypes.c_uint),
                ("Up",ctypes.c_uint),
                ("Rigth",ctypes.c_uint),
                ("Down",ctypes.c_uint),
                ("Zero",ctypes.c_uint*2)]
#-----------------------------


#-----------------------------
class IMGMULTIMARK(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_uint),
                ("Count",ctypes.c_uint),
                ("Size",ctypes.c_uint),
                ("PosV",ctypes.c_uint),
                ("PosH",ctypes.c_uint)]
#-----------------------------


#-----------------------------
class IMGMULTISQUAREMARK(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Kind",ctypes.c_ushort),
                ("FullMark",ctypes.c_byte),
                ("Weight",ctypes.c_byte),
                ("Mark",IMGMULTIMARK)]
#-----------------------------


#-----------------------------
class IMGDECOR(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_ushort),
                ("Number",ctypes.c_ushort)]
#-----------------------------


#-----------------------------
class IMGDRAW(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Ident",ctypes.c_uint),
                ("Length",ctypes.c_uint),
                ("Count",ctypes.c_ushort),
                ("Flags",ctypes.c_ushort),
                ("Image",IMGDECOR),
                ("Parm",ctypes.c_uint*1)]
#-----------------------------


#-----------------------------
class IMGDOTSHIFT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Dot",IMGDOT),
                ("Shift",ctypes.c_int)]
#-----------------------------


#-----------------------------
class IMGVECTPOINT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Hor",ctypes.c_int),
                ("Ver",ctypes.c_int)]
#-----------------------------


#-----------------------------
class IMGPOLYDESC(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Type",ctypes.c_byte),
                ("Image",ctypes.c_byte),
                ("Length",ctypes.c_ushort),
                ("Parm",ctypes.c_uint),
                ("Count",ctypes.c_uint),
                ("Point",IMGVECTPOINT*1)]
#-----------------------------


#-----------------------------
class IMGVECTOREX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("PosV",ctypes.c_int),
                ("PosH",ctypes.c_int),
                ("Base",ctypes.c_int),
                ("VLine1",ctypes.c_int),
                ("VLine2",ctypes.c_int),
                ("VSize",ctypes.c_int),
                ("HLine1",ctypes.c_int),
                ("HLine2",ctypes.c_int),
                ("HSize",ctypes.c_int),
                ("Static",ctypes.c_char),
                ("Mirror",ctypes.c_char),
                ("NoPress",ctypes.c_char),
                ("Scale",ctypes.c_char),
                ("Centre",ctypes.c_char),
                ("NoChangeColor",ctypes.c_char),
                ("Unicode",ctypes.c_char),
                ("TextNumber",ctypes.c_byte),
                ("Border",ctypes.c_int),
                ("Count",ctypes.c_int),
                ("Desc",IMGPOLYDESC)]
#-----------------------------


#-----------------------------
class TABLETEMPLATE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Order",ctypes.c_int*12),
                ("Origin",ctypes.c_int),
                ("Static",ctypes.c_int)]
#-----------------------------


#-----------------------------
class IMGTEMPLATE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Table",TABLETEMPLATE),
                ("Count",ctypes.c_int),
                ("Text",IMGDECOR),
                ("Parmtext",ctypes.c_uint*1),
                ("Line",IMGDECOR),
                ("Parmline",ctypes.c_uint*1),
                ("Mark",IMGDECOR),
                ("Parmmark",ctypes.c_uint*1)]
#-----------------------------


#-----------------------------
class IMGTRUETYPE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Text",IMGTEXT),
                ("FontName",ctypes.c_char*32),
                ("Number",ctypes.c_int),
                ("MinV",ctypes.c_int),
                ("MinH",ctypes.c_int),
                ("MaxV",ctypes.c_int),
                ("MaxH",ctypes.c_int),
                ("PosV",ctypes.c_int),
                ("PosH",ctypes.c_int)]
#-----------------------------


#-----------------------------
class IMGTRUETEXT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Text",IMGTEXT),
                ("FontName",ctypes.c_char*32)]
#-----------------------------


#-----------------------------
class IMGSQUAREGLASS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Bright",ctypes.c_int),
                ("Contrast",ctypes.c_int)]
#-----------------------------


#-----------------------------
class IMGSQUAREVECTOR(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Kind",ctypes.c_ushort),
                ("FullMark",ctypes.c_byte),
                ("Reserv",ctypes.c_byte),
                ("StepHor",ctypes.c_int),
                ("StepVer",ctypes.c_int),
                ("Angle",ctypes.c_int),
                ("Mark",IMGVECTOREX)]
#-----------------------------


#-----------------------------
class IMGDECORHEAD(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_uint),
                ("Begin",ctypes.c_int),
                ("End",ctypes.c_int),
                ("Left",ctypes.c_int),
                ("Right",ctypes.c_int),
                ("First",ctypes.c_int),
                ("Second",ctypes.c_int),
                ("Equidistant",ctypes.c_char),
                ("Reserv",ctypes.c_char*3)]
#-----------------------------


#-----------------------------
class IMGDECORATE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Head",IMGDECORHEAD),
                ("Base",IMGDECOR),
                ("BaseParm",ctypes.c_uint*1),
                ("Begin",IMGDECOR),
                ("BeginParm",ctypes.c_uint*1),
                ("End",IMGDECOR),
                ("EndParm",ctypes.c_uint*1),
                ("Left",IMGDECOR),
                ("LeftParm",ctypes.c_uint*1),
                ("Rigth",IMGDECOR),
                ("RigthParm",ctypes.c_uint*1),
                ("First",IMGDECOR),
                ("FirstParm",ctypes.c_uint*1),
                ("Second",IMGDECOR),
                ("SecondParm",ctypes.c_uint*1)]
#-----------------------------


#-----------------------------
class IMGSECTION(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_uint),
                ("Number",ctypes.c_uint),
                ("Base",ctypes.c_uint),
                ("Parm",ctypes.c_uint*1)]
#-----------------------------


#-----------------------------
class IMGDASH(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Count",ctypes.c_int),
                ("Last",ctypes.c_int),
                ("Border",ctypes.c_int),
                ("Reserve",ctypes.c_int),
                ("Section",IMGSECTION*1)]
#-----------------------------


#-----------------------------
class IMGLINESHIFT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Shift",ctypes.c_int),
                ("Head",IMGDECOR),
                ("Parm",ctypes.c_int*1)]
#-----------------------------


#-----------------------------
class IMGVECTORTEXT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Text",IMGTEXT),
                ("Code",ctypes.c_int),
                ("Title",ctypes.c_char*32)]
#-----------------------------


#-----------------------------
class IMGVECTORTEXTUN(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Text",IMGTEXT),
                ("Code",ctypes.c_int),
                ("Title",maptype.WCHAR1*(128*2)),
                ("Reserve",ctypes.c_int)]
#-----------------------------


#-----------------------------
class IMGGRAPHICMARKEX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Ident",ctypes.c_int),
                ("Name",ctypes.c_char*256),
                ("Type",ctypes.c_int),
                ("Height",ctypes.c_int),
                ("Width",ctypes.c_int),
                ("PosH",ctypes.c_int),
                ("PosV",ctypes.c_int),
                ("Shift",ctypes.c_int),
                ("Contour",IMGLINE),
                ("ContourFlag",ctypes.c_char),
                ("ShadeFlag",ctypes.c_char),
                ("TransparentFlag",ctypes.c_char),
                ("Rotate",ctypes.c_char),
                ("Reserve",ctypes.c_char*12)]
#-----------------------------


#-----------------------------
class IMGHATCHSQUARESHIFT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Angle",ctypes.c_int),
                ("Step",ctypes.c_int),
                ("Number",ctypes.c_int),
                ("Shift",ctypes.c_int)]
#-----------------------------


#-----------------------------
class IMGPOLYGONGLASS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Color",ctypes.c_int),
                ("Bright",ctypes.c_int),
                ("Contrast",ctypes.c_int),
                ("Transparency",ctypes.c_int)]
#-----------------------------


#-----------------------------
class IMGLINEGLASS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Color",ctypes.c_int),
                ("Thick",ctypes.c_uint),
                ("Bright",ctypes.c_int),
                ("Contrast",ctypes.c_int),
                ("Transparency",ctypes.c_int)]
#-----------------------------


#-----------------------------
class IMGDOTGLASS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Color",ctypes.c_int),
                ("Thick",ctypes.c_uint),
                ("Dash",ctypes.c_uint),
                ("Blank",ctypes.c_uint),
                ("Bright",ctypes.c_int),
                ("Contrast",ctypes.c_int),
                ("Transparency",ctypes.c_int)]
#-----------------------------


#-----------------------------
class IMGMULTIMARKGLASS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Bright",ctypes.c_int),
                ("Contrast",ctypes.c_int),
                ("Transparency",ctypes.c_int),
                ("Mark",IMGMULTIMARK)]
#-----------------------------


#-----------------------------
class IMGPICTURE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_uint),
                ("Height",ctypes.c_uint),
                ("Width",ctypes.c_uint),
                ("PosH",ctypes.c_int),
                ("PosV",ctypes.c_int),
                ("Shift",ctypes.c_int),
                ("PixelHeight",ctypes.c_int),
                ("PixelWidth",ctypes.c_int),
                ("Contour",IMGLINE),
                ("ContourFlag",ctypes.c_char),
                ("ShadeFlag",ctypes.c_char),
                ("TransparentFlag",ctypes.c_char),
                ("Type",ctypes.c_char),
                ("Rotate",ctypes.c_char),
                ("Reserve",ctypes.c_char*15)]
#-----------------------------


#-----------------------------
class IMGVARIABLEDASH(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Color",ctypes.c_uint),
                ("Thick",ctypes.c_uint),
                ("Dash",ctypes.c_uint),
                ("Blank",ctypes.c_uint),
                ("Dash2",ctypes.c_uint)]
#-----------------------------


#-----------------------------
class IMGGRAPHICFILE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("ImgPicture",IMGPICTURE),
                ("Alfa",ctypes.c_byte),
                ("Flags",ctypes.c_byte),
                ("SemCode",ctypes.c_ushort),
                ("Color",ctypes.c_uint),
                ("Scale",ctypes.c_uint),
                ("PathLength",ctypes.c_uint),
                ("FileIdent",ctypes.c_uint)]
#-----------------------------


#-----------------------------
class IMGCELL(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Font",IMGTEXT),
                ("Line",IMGLINE),
                ("Width",ctypes.c_uint),
                ("Height",ctypes.c_uint),
                ("Color",ctypes.c_uint),
                ("Color1",ctypes.c_uint),
                ("Color2",ctypes.c_uint),
                ("FigureSize",ctypes.c_uint),
                ("Indent",ctypes.c_uint),
                ("Align",ctypes.c_ushort),
                ("ChildCount",ctypes.c_byte),
                ("Column",ctypes.c_byte),
                ("TitleType",ctypes.c_byte),
                ("Style",ctypes.c_byte),
                ("Type",ctypes.c_byte),
                ("Fitting",ctypes.c_byte),
                ("Precision",ctypes.c_byte),
                ("Source",ctypes.c_byte),
                ("Figure",ctypes.c_byte),
                ("ScaleMode",ctypes.c_byte),
                ("FixedWidth",ctypes.c_byte),
                ("ViewFrame",ctypes.c_byte),
                ("Select",ctypes.c_byte),
                ("MultiColumn",ctypes.c_byte),
                ("Reserve",ctypes.c_byte*40),
                ("TitleSize",ctypes.c_ushort),
                ("FormulaSize",ctypes.c_ushort)]
#-----------------------------


#-----------------------------
class IMGTABLE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_uint),
                ("RowHeight",ctypes.c_uint),
                ("Font",IMGTEXT),
                ("VerLine",IMGLINE),
                ("HorLine",IMGLINE),
                ("Border",IMGLINE),
                ("Frame",IMGLINE),
                ("Color1",ctypes.c_uint),
                ("Color2",ctypes.c_uint),
                ("PageIndent",ctypes.c_uint),
                ("TextIndent",ctypes.c_uint),
                ("ImageIndent",ctypes.c_uint),
                ("CaptionIndent",ctypes.c_uint),
                ("Reserve",ctypes.c_byte*30),
                ("ViewFrame",ctypes.c_byte),
                ("ViewTitle",ctypes.c_byte),
                ("Title",IMGCELL)]
#-----------------------------


#-----------------------------
class IMGLIBRARY(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Code",ctypes.c_int),
                ("Index",ctypes.c_int),
                ("Function",ctypes.c_int),
                ("Draw",IMGDRAW)]
#-----------------------------


#-----------------------------
class IMGDOUBLE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Value",ctypes.c_double)]
#-----------------------------


#-----------------------------
class IMGLONG(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Value",ctypes.c_int)]
#-----------------------------


#-----------------------------
class IMGOBJECT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Color",ctypes.c_uint),
                ("Incode",ctypes.c_uint),
                ("Excode",ctypes.c_uint),
                ("Local",ctypes.c_uint)]
#-----------------------------


#-----------------------------
class IMGVECTORGRADIENT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Color",ctypes.c_uint),
                ("Left",ctypes.c_uint),
                ("Right",ctypes.c_uint),
                ("Bright",ctypes.c_uint)]
#-----------------------------


#-----------------------------
class VECTORMIX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Color",ctypes.c_uint),
                ("Bright",ctypes.c_int),
                ("Contrast",ctypes.c_int),
                ("Transparency",ctypes.c_int),
                ("Exclusion",ctypes.c_uint),
                ("Scale",ctypes.c_uint)]
#-----------------------------


#-----------------------------
class IMGVECTORMIX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Vector",ctypes.POINTER(IMGVECTOREX)),
                ("Mixing",VECTORMIX)]
#-----------------------------


#-----------------------------
class IMGDRAWMIX(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Draw",ctypes.POINTER(IMGDRAW)),
                ("Mixing",VECTORMIX)]
#-----------------------------


#-----------------------------
class LEGENDESC(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("FillColor",maptype.COLORREF),
                ("ContourColor",maptype.COLORREF),
                ("ColumnCount",ctypes.c_int),
                ("ElHeight",ctypes.c_int),
                ("ElWidth",ctypes.c_int),
                ("ElHeightImage",ctypes.c_int),
                ("ElWidthImage",ctypes.c_int),
                ("Reserve",ctypes.c_int),
                ("ImageFont",IMGTRUETEXT)]
#-----------------------------


#-----------------------------
class TABCTR(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_uint),
                ("LabelText",ctypes.c_uint),
                ("Width",ctypes.c_uint),
                ("Height",ctypes.c_uint),
                ("Count",ctypes.c_uint),
                ("Maximum",ctypes.c_uint),
                ("Scale",ctypes.c_ushort),
                ("ScaleLimit",ctypes.c_ushort),
                ("PressLimit",ctypes.c_ushort),
                ("Bottom",ctypes.c_byte),
                ("Top",ctypes.c_byte),
                ("Flags",ctypes.c_uint),
                ("Reserve",ctypes.c_uint*3),
                ("Name",maptype.WCHAR1*(128*2)),
                ("Draw",IMGDRAW)]
#-----------------------------


#-----------------------------
class IMGLINEDOT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Line",IMGLINE),
                ("Dot",IMGDOT)]
#-----------------------------


#-----------------------------
class IMGDOUBLELINE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("OneLine",IMGLINE),
                ("TwoLine",IMGLINE)]
#-----------------------------


#-----------------------------
class IMGDOTDLINE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Dot",IMGDOT),
                ("Double",IMGDOUBLELINE)]
#-----------------------------


#-----------------------------
class IMGDOUBLEDOT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("OneDot",IMGDOT),
                ("TwoDot",IMGDOT)]
#-----------------------------


#-----------------------------
class IMGSHIFTLINEDOT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Line",IMGLINE),
                ("Dot",IMGDOT)]
#-----------------------------


#-----------------------------
class IMGSQUARECROSS(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Color",ctypes.c_uint),
                ("Kind",ctypes.c_uint),
                ("Thick",ctypes.c_uint),
                ("Blank",ctypes.c_uint)]
#-----------------------------


#-----------------------------
class IMGMARK(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Color",ctypes.c_uint),
                ("Size",ctypes.c_uint),
                ("PosV",ctypes.c_uint),
                ("PosH",ctypes.c_uint),
                ("Bits",ctypes.c_byte*128)]
#-----------------------------


#-----------------------------
class IMGSQUAREMARK(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Color",ctypes.c_uint),
                ("Kind",ctypes.c_ushort),
                ("FullMark",ctypes.c_byte),
                ("Weight",ctypes.c_byte),
                ("Mark",IMGMARK)]
#-----------------------------


#-----------------------------
class IMGLEFTLINEDOT(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Line",IMGLINE),
                ("Dot",IMGDOT)]
#-----------------------------


#-----------------------------
class IMGDECHEAD(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_uint),
                ("Distance",ctypes.c_int)]
#-----------------------------


#-----------------------------
class IMGDECORATELINE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Head",IMGDECHEAD),
                ("Base",IMGDECOR),
                ("BaseParm",ctypes.c_uint*1),
                ("First",IMGDECOR),
                ("FirstParm",ctypes.c_uint*1),
                ("End",IMGDECOR),
                ("EndParm",ctypes.c_uint*1),
                ("Left",IMGDECOR),
                ("LeftParm",ctypes.c_uint*1),
                ("Rigth",IMGDECOR),
                ("RigthParm",ctypes.c_uint*1),
                ("Middle1",IMGDECOR),
                ("Mid1Parm",ctypes.c_uint*1),
                ("Middle2",IMGDECOR),
                ("Mid2Parm",ctypes.c_uint*1)]
#-----------------------------


#-----------------------------
class IMGHATCHSQUARE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Length",ctypes.c_int),
                ("Angle",ctypes.c_int),
                ("Step",ctypes.c_int),
                ("Number",ctypes.c_int)]
#-----------------------------


#-----------------------------
class IMGHATCHSQUARELINE(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Hatch",IMGHATCHSQUARE),
                ("Line",IMGLINE)]
#-----------------------------


#-----------------------------
class IMGSQUAREGLASSCOLOR(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [("Color",ctypes.c_int),
                ("Bright",ctypes.c_int),
                ("Contrast",ctypes.c_int)]
#-----------------------------


#-----------------------------
class IMLPARM(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [
        ("Ident", ctypes.c_int),
        ("Count", ctypes.c_int),
        ("Semantic", ctypes.c_char),
        ("Show4D", ctypes.c_char),
        ("Reserv2", ctypes.c_char),
        ("Reserv3", ctypes.c_char),
        ("Element", ctypes.c_char * IMLPARMCOUNT)]
#-----------------------------


#-----------------------------
class IMLLIST(ctypes.Structure):
    _pack_ = PACK_WIDTH
    _fields_ = [
        ("Ident", ctypes.c_int),
        ("Count", ctypes.c_int),
        ("Element", ctypes.c_char * IMLLISTCOUNT)]
#-----------------------------


def mapgdi_healthcheck(): 
    return 1