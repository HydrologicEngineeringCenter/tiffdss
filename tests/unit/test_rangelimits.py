import math
import unittest
from ctypes import CDLL, LibraryLoader, c_float, c_int, c_void_p
from wsgiref.util import request_uri

import numpy as np

UNDEFINED_FLOAT = -3.4028234663852886e38

# libtiffdss.so is compiled and put in /usr/lib during image creation
tiffdss = LibraryLoader(CDLL).LoadLibrary("libtiffdss.so")


class TestRangeLimitTable(unittest.TestCase):
    @classmethod
    def range_limit_table(
        self, minval, maxval, range, bins, datasize, rangelimit, histo, data
    ):
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

    @classmethod
    def internal_rangelimits(self, _min, _max, bin_range, bins):
        _step = bin_range / bins
        _rangelimits = np.zeros((bins), dtype=np.float32)
        _rangelimits[0] = UNDEFINED_FLOAT
        _rangelimits[1] = _min
        for i in range(2, bins - 1):
            if _step != 0:
                _rangelimits[i] = _min + _step * i
        _rangelimits[-1] = _max

        return _rangelimits

    @classmethod
    def internal_histo(self, aflat, datasize, bins, _rangelimits):
        _histo = np.zeros((bins), dtype=np.int32)
        for idx in range(datasize):
            for jdx in range(bins):
                if aflat[idx] >= _rangelimits[jdx]:
                    _histo[jdx] += 1

        return _histo

    def test_rangelimit_table(self):
        a = np.array([r for r in range(1, 100000)]).astype(np.float32)
        # flatten here used to simulate what happens in package writters
        aflat = a.flatten()
        _min = aflat.min()
        _max = aflat.max()
        datasize = aflat.shape[0]

        bins = 3
        bin_range = int(math.ceil(_max) - math.floor(_min))
        if bin_range > 0:
            bins = min(15, math.floor(1 + 3.322 * math.log10((datasize))) + 1)

        # Compute range limits and histogram to compare
        _rangelimits = self.internal_rangelimits(_min, _max, bin_range, bins)
        _histo = self.internal_histo(aflat, datasize, bins, _rangelimits)

        self.range_limit_table(
            _min,
            _max,
            bin_range,
            bins,
            datasize,
            rangelimits := np.zeros((bins), dtype=np.float32),
            histo := np.zeros((bins), dtype=np.int32),
            aflat,
        )

        # Iterate through range limit values making sure they are equal
        # Both arrays are numpy.float32 but value precision is a bit different
        # between Python float and C float.  Creating numpy.float64 and rounding
        # to one decimal precision eliminates errors when values are equal.
        for rl1, rl2 in zip(
            np.array(_rangelimits, dtype=np.float64),
            np.array(rangelimits, dtype=np.float64),
        ):
            _rl1 = round(rl1, 1)
            _rl2 = round(rl2, 1)
            with self.subTest(rl1=rl1, rl2=rl2):
                self.assertEqual(
                    _rl1,
                    _rl2,
                    f"Rang limit values not equal: {_rl1} != {_rl2}",
                )

        # Iterate through histogram values
        for h1, h2 in zip(_histo, histo):
            with self.subTest(h1=h1, h2=h2):
                self.assertEqual(h1, h2, f"Histogram counts not equal: {h1} != {h2}")


if __name__ == "__main__":
    unittest.main()
