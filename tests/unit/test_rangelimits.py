import math
from operator import mod
import unittest
from ctypes import (
    CDLL,
    LibraryLoader,
    c_float,
    c_int,
    c_void_p,
)

import numpy as np

# libtiffdss.so is compiled and put in /usr/lib during image creation
tiffdss = LibraryLoader(CDLL).LoadLibrary("libtiffdss.so")


def range_limit_table(minval, maxval, range, bins, datasize, rangelimit, histo, data):
    tiffdss.rangelimit_table.argtypes = (
        c_float,
        c_float,
        c_int,
        c_int,
        c_int,
        np.ctypeslib.ndpointer(dtype=np.float32, ndim=1, flags="C"),
        np.ctypeslib.ndpointer(dtype=np.int32, ndim=1, flags="C"),
        np.ctypeslib.ndpointer(dtype=np.float32, ndim=1, flags="C"),
    )
    tiffdss.rangelimit_table.restype = c_void_p

    retval = tiffdss.rangelimit_table(
        c_float(minval),
        c_float(maxval),
        c_int(range),
        c_int(bins),
        c_int(datasize),
        rangelimit,
        histo,
        data,
    )
    return retval


class TestRangeLimitTable(unittest.TestCase):
    # def setUp(self):
    #     ...
    # def tearDown(self):
    #     ...

    def test_rangelimit_table(self):
        a = 1 * np.random.rand(100, 100).astype(np.float32)
        # flatten here used to simulate what happens in package writters
        aflat = a.flatten()
        _min = aflat.min()
        _max = aflat.max()
        bin_range = int(math.ceil(_max) - math.floor(_min))

        datasize = aflat.shape[0]

        bins = 3
        if bin_range > 0:
            bins = math.floor(1 + 3.322 * math.log10((datasize))) + 1

        rangelimits = np.zeros((bins), dtype=np.float32)
        histo = np.zeros((bins), dtype=np.int32)

        range_limit_table(
            _min,
            _max,
            bin_range,
            bins,
            datasize,
            rangelimits,
            histo,
            aflat,
        )


if __name__ == "__main__":
    unittest.main()
