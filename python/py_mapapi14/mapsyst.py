#!/usr/bin/env python3

import os
import sys
import ctypes

# для корректной инициализации tkinter в python 3.5
if not hasattr(sys, 'argv'):
    sys.argv = ['']

def setuppanlib(syspath):
    os.environ.setdefault('gisaccesdll', syspath + 'mapacces64.dll')
    os.environ.setdefault('gismathdll', syspath + 'mapmath64.dll')
    os.environ.setdefault('gismtrexdll', syspath + 'mapmtrex64.dll')
    os.environ.setdefault('gispaspdll', syspath + 'mappasp64.dll')
    os.environ.setdefault('gispicexdll', syspath + 'mappicex64.dll')
    os.environ.setdefault('gisselecdll', syspath + 'mapselec64.dll')
    os.environ.setdefault('gisvecexdll', syspath + 'mapvecex64.dll')
    os.environ.setdefault('gisrsctoolsdll', syspath + 'rsctools64.dll')
    os.environ.setdefault('gisvectrdll', syspath + 'mapvectr64.dll')
    os.environ.setdefault('gisdlgsdll', syspath + 'mapscena64.dll')

def setupgislib(syspath):
    os.environ.setdefault('gisaccesdll', syspath + 'gis64acces.dll')
    os.environ.setdefault('gismathdll', syspath + 'gis64math.dll')
    os.environ.setdefault('gismtrexdll', syspath + 'gis64mtrex.dll')
    os.environ.setdefault('gispaspdll', syspath + 'gis64pasp.dll')
    os.environ.setdefault('gispicexdll', syspath + 'gis64picex.dll')
    os.environ.setdefault('gisselecdll', syspath + 'gis64selec.dll')
    os.environ.setdefault('gisvecexdll', syspath + 'gis64vecex.dll')
    os.environ.setdefault('gisrsctoolsdll', syspath + 'gis64rsctools.dll')
    os.environ.setdefault('gisvectrdll', syspath + 'gis64vectr.dll')
    os.environ.setdefault('gisdlgsdll', syspath + 'gis64dlgs.dll')

def LoadLibrary(maplibname):
    if sys.platform == "win32":
        return ctypes.WinDLL(maplibname)
    elif sys.platform in ("linux", "linux2"):
        return ctypes.CDLL(maplibname)
    return 0

def GetProcAddressBase(_lib, _restype, _func, _types):
    pfun = _lib[_func]
    pfun.restype = _restype
    pfun.argtypes = _types
    return pfun

def GetProcAddress(_lib, _restype, _func, *_types):
    try:
        pfun = GetProcAddressBase(_lib, _restype, _func, _types)
    except Exception as exc:
        raise RuntimeError('GetProcAddress error', _lib, _func) from exc
    return pfun

# класс буфера WCHAR ядра
class WTEXT:
    __buffer = None
    __dllbuffer = None
    __bytes = 0

    # инициализация количеством символов или питоновской строкой
    def __init__(self, num_or_str = 1):
        if isinstance(num_or_str,int):
            self.__buffer = bytearray(num_or_str*2)
        elif isinstance(num_or_str,str):
            self.__buffer = bytearray((num_or_str+'\0').encode('utf-16LE')) # little endian по умолчанию
        elif isinstance(num_or_str,WTEXT):
            self.__buffer = bytearray(num_or_str.__buffer)

        if isinstance(self.__buffer,bytearray):
            self.__bytes = self.__buffer.__len__()
            t = ctypes.c_char * self.__bytes
            self.__dllbuffer = t.from_buffer(self.__buffer)

    def string(self): # для работы в питоне
        if isinstance(self.__buffer,bytearray):
            s = self.__buffer.decode('utf-16LE', 'ignore') # little endian по умолчанию
            return s[0:s.find('\0')] # обрезка строки по первому \0
        return ''

    def buffer(self): # для передачи в дллку
        return self.__dllbuffer

    def size(self): # размер буфера в байтах
        return self.__bytes

    def asUtf16(self):
        return bytes(self.__buffer)

    def asUtf8(self):
        return bytes(self.__buffer.decode('utf-16LE', 'ignore').encode('utf-8'))
