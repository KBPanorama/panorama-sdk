import ctypes

import maptype
import mapapi
import mapsyst
import seekapi
import mtrapi
import maperr
import logapi
import doforeach

#################################################################
# Добавить высоту в точки метрики из матричных данных
#################################################################
def AddObjectHValue(_hmap:maptype.HMAP, _hobj:maptype.HOBJ, _parm = 0) -> int:
    if _hobj == 0:
        return 0

    isupdate = 0
    mapapi.mapSetObjectKind(_hobj, maptype.IDDOUBLE3) # Добавить 3-е измерение в метрику
    subjects = mapapi.mapPolyCount(_hobj)
    for s in range(0, subjects): 
        points = mapapi.mapPointCount(_hobj, s) + 1
        for p in range(1, points): 
            point = maptype.DOUBLEPOINT(0, 0)
            mapapi.mapGetPlanePoint(_hobj, ctypes.byref(point), p, s)
            h = mtrapi.mapGetPrecisionHeightTriangleEx(_hmap, point.X, point.Y, 0)  # Вычисление высоты в точке по окружающим значениям
            mapapi.mapSetHPlane(_hobj, h, p, s)
            if h > maptype.ERRORHEIGHT:
                isupdate +=1
    if isupdate > 0:
        return mapapi.mapCommitObject(_hobj) 
    return 0

def AddHValue(_hmap:maptype.HMAP, _hobj:maptype.HOBJ) -> float: #caption:Добавить h по матрице высот
    if _hmap == 0:
        return 0

    if seekapi.mapIsTotalSeekObjectNotEmpty(_hmap) == 0:
        if _hobj == 0:
            mapapi.mapErrorMessageUn(maperr.IDS_OBJECTSNOTSELECTED, __name__)
            return 0
    else:
        _hobj = 0

    dofunction = doforeach.DoForEach('Добавление высоты:', logapi.TAC_MED_HIGHT)
    result = dofunction.run(AddObjectHValue, _hmap, _hobj)

    mapapi.mapShowMessage(mapsyst.WTEXT('Обработано объектов: ' + mapapi.IntToStr(result)), mapsyst.WTEXT('Добавление высоты в метрику'))
    return result

#################################################################
# Удалить высоту в точках метрики
#################################################################
def DeleteObjectHValue(_hmap:maptype.HMAP, _hobj:maptype.HOBJ, _parm = 0) -> int:
    if mapapi.mapIsObject3D(_hobj) == 0:
        return 0
    if mapapi.mapGetObjectKind(_hobj) == maptype.IDLONG3: 
        mapapi.mapSetObjectKind(_hobj, maptype.IDLONG2)
    else:
        mapapi.mapSetObjectKind(_hobj, maptype.IDDOUBLE2)
    return mapapi.mapCommitObject(_hobj) 

def DeleteHValue(_hmap:maptype.HMAP, _hobj:maptype.HOBJ) -> float: #caption:Удаление h из метрики объектов
    if _hmap == 0:
        return 0

    if seekapi.mapIsTotalSeekObjectNotEmpty(_hmap) == 0:
        if _hobj == 0:
            mapapi.mapErrorMessageUn(maperr.IDS_OBJECTSNOTSELECTED, __name__)
            return 0
    else:
        _hobj = 0

    dofunction = doforeach.DoForEach('Удаление высоты:', logapi.TAC_MED_HIGHT)
    result = dofunction.run(DeleteObjectHValue, _hmap, _hobj)

    mapapi.mapShowMessage(mapsyst.WTEXT('Обработано объектов: ' + mapapi.IntToStr(result)), mapsyst.WTEXT('Удаление высоты в метрике'))
    return result
