
from hec.heclib.grid import GridData
from hec.heclib.grid import GridUtilities
from hec.heclib.dss import HecDSSFileAccess
from jarray import zeros

from hec.lang import DSSPathString

def assertFloatEqual(o1, o2,tolerance, msg):
    if abs(o2-o2) > tolerance:
         raise Exception(msg+" \n"+str(o1)+" is not equal to "+str(o2))

def assertNotEquals(o1, o2,msg):
    if o1 == o2:
        raise Exception(msg+" \n"+str(o1)+" is not equal to "+str(o2))

def assertEqual(o1, o2,msg):
  if o1 != o2:
    raise Exception(msg+" \n"+str(o1)+" is not equal to "+str(o2))

def ReadGrid(dssFile, path):
    status = zeros(1,'i')
   
    rval = GridUtilities.retrieveGridFromDss(dssFile, path, status)
    if status[0] !=0:
      print("error reading grid "+path+" in file '"+dssFile)
    
    return rval


def compare_grids(dssFile1, dssFile2, path):

        gd1 = ReadGrid(dssFile1, path)
        gd2 = ReadGrid(dssFile2, path)
        gd1.updateStatistics()
        gd2.updateStatistics()
        info1 = gd1.getGridInfo()
        info2 = gd2.getGridInfo()

        assertEqual(info1.getGridType(), info2.getGridType(), "getGridType() " + path)
        assertEqual(info1.getDataUnits(), info2.getDataUnits(), "getDataUnits" + path)
        assertEqual(info1.getDataTypeName(), info2.getDataTypeName(), "getDataTypeName" + path)
        dssPath = DSSPathString(path)
        #// empty path in DSS6 defaults to  31 December 1899, 00:00,
        #// empty path in DSS7 is blank
        if dssPath.getDPart().strip() != "":
            assertEqual(info1.getEndTime(), info2.getEndTime(), "getEndTime()" + path)
        if dssPath.getEPart().strip() != "":
            assertEqual(info1.getStartTime(), info2.getStartTime(), "getStartTime()" + path)

        assertEqual(info1.getNumberOfCellsX(), info2.getNumberOfCellsX(), "getNumberOfCellsX()" + path)
        assertEqual(info1.getNumberOfCellsY(), info2.getNumberOfCellsY(), "getNumberOfCellsY()" + path)
        assertEqual(info1.getRangeNum(), info2.getRangeNum(), "getRangeNum()" + path)

        assertFloatEqual(info1.getMaxDataValue(), info2.getMaxDataValue(), 0.01, "getMaxDataValue()" + path)
        assertFloatEqual(info1.getMinDataValue(), info2.getMinDataValue(), 0.01, "getMinDataValue()" + path)
        assertFloatEqual(info1.getMeanDataValue(), info2.getMeanDataValue(), 0.01, "getMeanDataValue()" + path)
        assertNotEquals(0,info1.getCellSize(),"cellSize record 1")
        assertNotEquals(0,info2.getCellSize(),"cellSize record 2")
        assertEqual(info1.getCellSize(), info2.getCellSize(), "getCellSize()" + path)
        assertEqual(info1.getLowerLeftCellX(), info2.getLowerLeftCellX(), "getLowerLeftCellX()" + path)
        assertEqual(info1.getLowerLeftCellY(), info2.getLowerLeftCellY(), "getLowerLeftCellY()" + path)
        assertEqual(info1.getRangeNum(), info2.getRangeNum(), "getRangeNum" + path)

        for i in range(info1.getRangeNum() ):
            assertFloatEqual(info1.getRangeLimitTable()[i], info2.getRangeLimitTable()[i], 0.001, "getRangeLimitTable()[" + str(i) + "]" + path)
        

        assertEqual(info1.getSpatialReferenceSystem(), info2.getSpatialReferenceSystem(), "getSpatialReferenceSystem()" + path)

        data1 = gd1.getData()
        data2 = gd2.getData()

        tolerance = 0.001
        print("len of data = "+str(len(data1)))
#        for i in range(len(data1)):
        i=0
        while( i<len(data1)):
            tolerance = 0.01 if data1[i]>10 else 0.001
            assertFloatEqual(data1[i], data2[i], tolerance, "comparing grid float values [" + str(i) + "] " + path)
            i+=1

