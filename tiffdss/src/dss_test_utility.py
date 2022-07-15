
from hec.heclib.grid import GridData
from hec.heclib.grid import GridUtilities
from hec.heclib.dss import HecDSSFileAccess
from jarray import zeros

from hec.lang import DSSPathString
import unittest

class DssTestUtility(unittest.TestCase):
    def runTest(self):
        self.assertEqual

def ReadGrid(dssFile, path):
    status = zeros(1,'i')
   
    rval = GridUtilities.retrieveGridFromDss(dssFile, path, status)
    print("status:")
    print(status)
    
    return rval


def compare_grids(dssFile1, dssFile2, path):

        gd1 = ReadGrid(dssFile1, path)
        gd2 = ReadGrid(dssFile2, path)
        gd1.updateStatistics()
        gd2.updateStatistics()
        info1 = gd1.getGridInfo()
        info2 = gd2.getGridInfo()

        t = TestCase()
        t.assertEqual(info1.getGridType(), info2.getGridType(), "getGridType() " + path)
        TestCase.assertEqual(info1.getDataUnits(), info2.getDataUnits(), "getDataUnits" + path)
        TestCase.assertEqual(info1.getDataTypeName(), info2.getDataTypeName(), "getDataTypeName" + path)
        dssPath = DSSPathString(path)
        #// empty path in DSS6 defaults to  31 December 1899, 00:00,
        #// empty path in DSS7 is blank
        if (dssPath.getDPart().trim() != ""):
            TestCase.assertEqual(info1._endTime.value(), info2._endTime.value(), "_endTime()" + path)
        if (dssPath.getEPart().trim() != ""):
            TestCase.assertEqual(info1.getStartTime(), info2.getStartTime(), "getStartTime()" + path)

        TestCase.assertEqual(info1.getNumberOfCellsX(), info2.getNumberOfCellsX(), "getNumberOfCellsX()" + path)
        TestCase.assertEqual(info1.getNumberOfCellsY(), info2.getNumberOfCellsY(), "getNumberOfCellsY()" + path)
        TestCase.assertEqual(info1.getRangeNum(), info2.getRangeNum(), "getRangeNum()" + path)

        TestCase.assertEqual(info1.getMaxDataValue(), info2.getMaxDataValue(), 0.01, "getMaxDataValue()" + path)
        TestCase.assertEqual(info1.getMinDataValue(), info2.getMinDataValue(), 0.01, "getMinDataValue()" + path)
        TestCase.assertEqual(info1.getMeanDataValue(), info2.getMeanDataValue(), 0.01, "getMeanDataValue()" + path)
        TestCase.assertNotEquals(0,info1.getCellSize())
        TestCase.assertNotEquals(0,info2.getCellSize())
        TestCase.assertEqual(info1.getCellSize(), info2.getCellSize(), "getCellSize()" + path)
        TestCase.assertEqual(info1.getLowerLeftCellX(), info2.getLowerLeftCellX(), "getLowerLeftCellX()" + path)
        TestCase.assertEqual(info1.getLowerLeftCellY(), info2.getLowerLeftCellY(), "getLowerLeftCellY()" + path)
        TestCase.assertEqual(info1.getRangeNum(), info2.getRangeNum(), "getRangeNum" + path)

        for i in range(info1.getRangeNum() ):
            TestCase.assertEqual(info1.getRangeLimitTable()[i], info2.getRangeLimitTable()[i], 0.001, "getRangeLimitTable()[" + i + "]" + path)
        

        TestCase.assertEqual(info1.getSpatialReferenceSystem(), info2.getSpatialReferenceSystem(), "getSpatialReferenceSystem()" + path);

        data1 = gd1.getData()
        data2 = gd2.getData()

        tolerance = 0.001
        for i in range(data1.length):
            tolerance = 0.01 if data1[i]>10 else 0.001
            TestCase.assertEqual(data1[i], data2[i], tolerance, "comparing grid float values [" + i + "] " + path)

