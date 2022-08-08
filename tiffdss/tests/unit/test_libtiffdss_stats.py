import unittest
from ctypes import (
    CDLL,
    POINTER,
    LibraryLoader,
    Structure,
    c_char_p,
    c_float,
    c_int,
    c_void_p,
    pointer,
)

import numpy as np

SHG_SRC_DEFINITION = 'PROJCS["USA_Contiguous_Albers_Equal_Area_Conic_USGS_version",\
GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",\
SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],\
UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],\
PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],\
PARAMETER["Central_Meridian",-96.0],PARAMETER["Standard_Parallel_1",29.5],\
PARAMETER["Standard_Parallel_2",45.5],PARAMETER["Latitude_Of_Origin",23.0],\
UNIT["Meter",1.0]]'


class zStructSpatialGrid(Structure):
    _fields_ = [
        ("structType", c_int),
        ("pathname", c_char_p),
        ("_structVersion", c_int),
        ("_type", c_int),
        ("_version", c_int),
        ("_dataUnits", c_char_p),
        ("_dataType", c_int),
        ("_dataSource", c_char_p),
        ("_lowerLeftCellX", c_int),
        ("_lowerLeftCellY", c_int),
        ("_numberOfCellsX", c_int),
        ("_numberOfCellsY", c_int),
        ("_cellSize", c_float),
        ("_compressionMethod", c_int),
        ("_sizeofCompressedElements", c_int),
        ("_compressionParameters", c_void_p),
        ("_srsName", c_char_p),
        ("_srsDefinitionType", c_int),
        ("_srsDefinition", c_char_p),
        ("_xCoordOfGridCellZero", c_float),
        ("_yCoordOfGridCellZero", c_float),
        ("_nullValue", c_float),
        ("_timeZoneID", c_char_p),
        ("_timeZoneRawOffset", c_int),
        ("_isInterval", c_int),
        ("_isTimeStamped", c_int),
        ("_numberOfRanges", c_int),
        ("_storageDataType", c_int),
        ("_maxDataValue", c_void_p),
        ("_minDataValue", c_void_p),
        ("_meanDataValue", c_void_p),
        ("_rangeLimitTable", c_void_p),
        ("_numberEqualOrExceedingRangeLimit", c_int),
        ("_data", c_void_p),
    ]


# libtiffdss.so is compiled and put in /usr/lib during image creation
tiffdss = LibraryLoader(CDLL).LoadLibrary("libtiffdss.so")


def get_maximum_value(data: np, datasize: int, nodata: float = 0):
    ND_POINTER_1 = np.ctypeslib.ndpointer(dtype=np.float32, ndim=1, flags="C")
    tiffdss.maximum.argtypes = (
        ND_POINTER_1,
        c_int,
        c_float,
    )
    tiffdss.maximum.restype = c_float
    max_value = tiffdss.maximum(
        data,
        datasize,
        nodata,
    )
    return max_value


def get_minimum_value(data: np, datasize: int, nodata: float = 0):
    ND_POINTER_1 = np.ctypeslib.ndpointer(dtype=np.float32, ndim=1, flags="C")
    tiffdss.minimum.argtypes = (
        ND_POINTER_1,
        c_int,
        c_float,
    )
    tiffdss.minimum.restype = c_float
    min_value = tiffdss.minimum(
        data,
        datasize,
        nodata,
    )
    return min_value


def get_meanvalue_value(data: np, datasize: int, nodata: float = 0):
    ND_POINTER_1 = np.ctypeslib.ndpointer(dtype=np.float32, ndim=1, flags="C")
    tiffdss.meanvalue.argtypes = (
        ND_POINTER_1,
        c_int,
        c_float,
    )
    tiffdss.meanvalue.restype = c_float
    mean_value = tiffdss.meanvalue(
        data,
        datasize,
        nodata,
    )
    return mean_value


def within_precision(a, b, p):
    return abs(a - b) < (1 / pow(10, p))


def zwrite_record(
    dssfilename: str,
    gridStructStore: zStructSpatialGrid,
    data_flat: np,
):
    """Write the data array to DSS record using the 'writeRecord' C function

    Parameters
    ----------
    dssfilename : str
        DSS file name and path
    gridStructStore : zStructSpatialGrid
        ctypes structure
    data_flat : numpy
        1D numpy array
    gridStats : GridStats
        ctypes structure

    Returns
    -------
    int
        Response from the C function
    """
    ND_POINTER_1 = np.ctypeslib.ndpointer(dtype=np.float32, ndim=1, flags="C")
    tiffdss.writeRecord.argtypes = (
        c_char_p,
        POINTER(zStructSpatialGrid),
        ND_POINTER_1,
    )
    tiffdss.writeRecord.restype = c_int
    _ = tiffdss.writeRecord(
        c_char_p(dssfilename.encode()),
        pointer(gridStructStore),
        data_flat,
    )


class TestGenDss(unittest.TestCase):
    def setUp(self):
        self.ot = "Float32"
        self.of = "GTiff"
        self.cellsize = 2000
        self.xmin = 456000
        self.ymin = 182000
        self.xmax = 2112000
        self.ymax = 2058000

        self.nrows = int((self.ymax - self.ymin) / self.cellsize)
        self.ncols = int((self.xmax - self.xmin) / self.cellsize)

        self.nodata = -999
        self.precision = 5

        self.spatialGridStruct = zStructSpatialGrid()
        self.spatialGridStruct.pathname = c_char_p(
            str.encode("/a/b/c/01JAN2000:0000/01JAN2000:0100/f/")
        )
        self.spatialGridStruct._structVersion = c_int(-100)
        self.spatialGridStruct._type = c_int(1)
        self.spatialGridStruct._version = c_int(1)
        self.spatialGridStruct._dataUnits = c_char_p(str.encode("MM"))
        self.spatialGridStruct._dataType = c_int(2)
        self.spatialGridStruct._dataSource = c_char_p("INTERNAL".encode())
        self.spatialGridStruct._lowerLeftCellX = c_int(self.xmin)
        self.spatialGridStruct._lowerLeftCellY = c_int(self.ymin)
        self.spatialGridStruct._numberOfCellsX = c_int(self.ncols)
        self.spatialGridStruct._numberOfCellsY = c_int(self.nrows)
        self.spatialGridStruct._cellSize = c_float(self.cellsize)
        self.spatialGridStruct._compressionMethod = c_int(26)
        self.spatialGridStruct._srsName = c_char_p(str.encode("SHG"))
        self.spatialGridStruct._srsDefinitionType = c_int(1)
        self.spatialGridStruct._srsDefinition = c_char_p(SHG_SRC_DEFINITION.encode())
        self.spatialGridStruct._xCoordOfGridCellZero = c_float(0)
        self.spatialGridStruct._yCoordOfGridCellZero = c_float(0)
        self.spatialGridStruct._nullValue = c_float(0)
        self.spatialGridStruct._timeZoneID = c_char_p(str.encode("GMT"))
        self.spatialGridStruct._timeZoneRawOffset = c_int(0)
        self.spatialGridStruct._isInterval = c_int(1)
        self.spatialGridStruct._isTimeStamped = c_int(1)

    def tearDown(self):
        pass

    def test_zeros_min(self):
        a = np.zeros((100, 100), np.float32)
        aflat = a.flatten()

        precision = 5

        min_val = round(get_minimum_value(aflat, len(aflat), self.nodata), precision)
        np_min = round(np.min(a), precision)
        min_precision = within_precision(np_min, min_val, precision)
        self.assertTrue(min_precision, "Minimum value not equal")

    def test_zeros_max(self):
        a = np.zeros((100, 100), np.float32)
        aflat = a.flatten()

        precision = 5

        max_val = round(get_maximum_value(aflat, len(aflat), self.nodata), precision)
        np_max = round(np.max(a), precision)
        max_precision = within_precision(np_max, max_val, precision)
        self.assertTrue(max_precision, "Maximum value not equal")

    def test_zeros_mean(self):
        a = np.zeros((100, 100), np.float32)
        aflat = a.flatten()

        precision = 5

        mean_val = round(get_meanvalue_value(aflat, len(aflat), self.nodata), precision)
        np_mean = round(np.mean(a), precision)
        mean_precision = within_precision(np_mean, mean_val, precision)
        self.assertTrue(mean_precision, "Mean value not equal")

    def test_ones_min(self):
        a = np.ones((100, 100), np.float32)
        aflat = a.flatten()

        precision = 5

        min_val = round(get_minimum_value(aflat, len(aflat), self.nodata), precision)
        np_min = round(np.min(a), precision)
        min_precision = within_precision(np_min, min_val, precision)
        self.assertTrue(min_precision, "Minimum value not equal")

    def test_ones_max(self):
        a = np.ones((100, 100), np.float32)
        aflat = a.flatten()

        precision = 5

        max_val = round(get_maximum_value(aflat, len(aflat), self.nodata), precision)
        np_max = round(np.max(a), precision)
        max_precision = within_precision(np_max, max_val, precision)

        self.assertTrue(max_precision, "Maximum value not equal")

    def test_ones_mean(self):
        a = np.ones((100, 100), np.float32)
        aflat = a.flatten()

        precision = 5

        mean_val = round(get_meanvalue_value(aflat, len(aflat), self.nodata), precision)
        np_mean = round(np.mean(a), precision)
        mean_precision = within_precision(np_mean, mean_val, precision)

        self.assertTrue(mean_precision, "Mean value not equal")

    def test_random_min(self):
        a = np.random.rand(100, 100).astype(np.float32)
        aflat = a.flatten()

        precision = 5

        min_val = round(get_minimum_value(aflat, len(aflat), self.nodata), precision)
        np_min = round(np.min(a), precision)
        min_precision = abs(np_min - min_val) < (1 / pow(10, precision))
        
        self.assertTrue(min_precision, "Minimum value not equal")

    def test_random_max(self):
        a = np.random.rand(100, 100).astype(np.float32)
        aflat = a.flatten()

        precision = 5

        max_val = round(get_maximum_value(aflat, len(aflat), self.nodata), precision)
        np_max = round(np.max(a), precision)
        max_precision = abs(np_max - max_val) < (1 / pow(10, precision))

        self.assertTrue(max_precision, "Maximum value not equal")

    def test_random_mean(self):
        a = np.random.rand(100, 100).astype(np.float32)
        aflat = a.flatten()

        precision = 5

        mean_val = round(get_meanvalue_value(aflat, len(aflat), self.nodata), precision)
        np_mean = round(np.mean(a), precision)
        mean_precision = abs(np_mean - mean_val) < (1 / pow(10, precision))

        self.assertTrue(mean_precision, "Mean value not equal")

    def test_missing_min(self):
        a = np.ones((100, 100), np.float32)
        a[a == 1] = self.nodata
        aflat = a.flatten()

        precision = 5

        min_val = round(get_minimum_value(aflat, len(aflat), self.nodata), precision)

        self.assertEqual(min_val, 1.9999999360571385e38, "Minimum value not equal")

    def test_missing_max(self):
        a = np.ones((100, 100), np.float32)
        a[a == 1] = self.nodata
        aflat = a.flatten()

        precision = 5

        max_val = round(get_maximum_value(aflat, len(aflat), self.nodata), precision)

        self.assertEqual(max_val, -1.9999999360571385e38, "Maximum value not equal")

    def test_missing_mean(self):
        a = np.ones((100, 100), np.float32)
        a[a == 1] = self.nodata
        aflat = a.flatten()

        precision = 5

        mean_val = round(get_meanvalue_value(aflat, len(aflat), self.nodata), precision)

        self.assertEqual(mean_val, -3.4028234663852886e38, "Mean value not equal")

    def test_filter_nodata(self):
        a = np.ones((100, 100), np.float32)
        aflat = a.flatten()
        

if __name__ == "__main__":
    unittest.main()
