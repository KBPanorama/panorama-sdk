import mapsyst
import maptype
import mapapi
import seekapi
import logapi
import maperr
import sitapi

#################################################################
# Выполнить обработку выделенных объектов в function -
# выполняется перебор выделенных объектов и вызов заданной функции 
# для каждого объекта. Если передается ненулевой _hobj, то
# функция выполняется только для него.
#
# def function(_hmap:maptype.HMAP, _hobj:maptype.HOBJ, _parm = 0) -> int:
#
# _parm - параметры, в зависимости от алгоритма обработки
#
# Например:
#    dofunction = doforeach.DoForEach('Добавление высоты:', logapi.TAC_MED_HIGHT)
#    result = dofunction.run(AddObjectHValue, _hmap, _hobj)
# 
#################################################################


# Do some function for each selected object
class DoForEach:
    __seekcount = 0
    __objcount = 0
    __readycount = 0
    __actiontype = 0
    __comment = ''

    def __init__(self, comment = '', actiontype = 0):
        if len(comment) > 0:
            self.__comment = comment + ' '
        self.__actiontype = actiontype

    def seekcount(self):
        return self.__seekcount    # Число выделенных объектов

    def readycount(self):
        return self.__readycount   # Число успешно обработанных объектов

    def objectcount(self):
        return self.__objcount  # Число объектов, попавших в обработку до завершения функции (может быть прервана оператором)

    def run(self, _function, hmap:maptype.HMAP, hobj:maptype.HOBJ, parm = 0):  # Выполнить обработку выделенных объектов в _function
        self.__objcount = 0
        self.__readycount = 0

        if hobj != 0:
            self.__objcount += 1 
            ret = _function(hmap, hobj, parm)
            if ret != 0:
                self.__readycount += 1
            return self.__readycount

        if hmap == 0:
            return 0

        self.__seekcount = seekapi.mapTotalSeekObjectCount(hmap)
        if self.__seekcount == 0:
            mapapi.mapErrorMessageUn(maperr.IDS_OBJECTSNOTSELECTED, _function.__name__)
            return 0

        hwork = mapapi.mapCreateObject(hmap, 1, maptype.IDDOUBLE2, 0)
        percent = int(0)
        hprogress = 0
        if self.__seekcount > 100:
            hprogress = mapapi.mapOpenProgressBar()

        flag = maptype.WO_FIRST

        if self.__actiontype != 0:
            seekapi.mapTotalSeekObject(hmap, hwork, flag)
            hsite = sitapi.mapGetObjectSiteIdent(hmap, hwork)
            if sitapi.mapGetSiteEditFlag(hmap, hsite) == 0:
                sitename = mapsyst.WTEXT(256)
                sitapi.mapGetSiteFileNameUn(hmap, hsite, sitename, sitename.size())
                mapapi.mapErrorMessageUn(maperr.IDS_NOTEDIT, sitename)
            logapi.mapLogCreateAction(hmap, hmap, self.__actiontype)

        while (seekapi.mapTotalSeekObject(hmap, hwork, flag) != 0):
            flag = maptype.WO_NEXT

            if _function(hmap, hwork, parm) != 0:
                self.__readycount += 1

            self.__objcount += 1
            newpercent = int(self.__objcount * 100 / self.__seekcount)
            if newpercent > percent:
                percent = newpercent
                if hprogress != 0:
                    ret = mapapi.mapProgressBar(hprogress, int(percent), mapsyst.WTEXT(self.__comment + mapapi.IntToStr(self.__objcount) + '/' + mapapi.IntToStr(self.__seekcount))) 
                    if ret == -1:     # Оператор требует завершить выполнение процедуры  (__objcount < __seekcount)
                        break
        if self.__actiontype != 0:
            logapi.mapLogCommitActionEx(hmap, hmap, None)
        if hprogress != 0:
            mapapi.mapCloseProgressBar(hprogress)
        if hwork != 0:
            mapapi.mapFreeObject(hwork)

        return self.__readycount
