import os
import random
import unittest

from hec.heclib.dss import HecDss
from hec.heclib.grid import GridUtilities
from hec.heclib.util import Heclib
from jarray import zeros

this = "/app/tiffdss/tests/integration"


class TestGridInfo(unittest.TestCase):
    def setUp(self):
        Heclib.Hec_zsetMessageLevel(0, 0)
        status = zeros(1, "i")
        # dss6
        dss6path = os.path.join("/tmp", "test6.dss")
        self.dss6 = HecDss.open(dss6path)
        self.cat6 = self.dss6.getCatalogedPathnames(1)
        # dss7
        dss7path = os.path.join("/tmp", "test7.dss")
        self.dss7 = HecDss.open(dss7path)
        self.cat7 = self.dss7.getCatalogedPathnames(1)
        # catalog intersection
        dsspaths = set(self.cat6).intersection(self.cat7)
        dsspath = random.choice(list(dsspaths))

        self.grids6 = GridUtilities.retrieveGridFromDss(dss6path, dsspath, status)
        self.grids7 = GridUtilities.retrieveGridFromDss(dss7path, dsspath, status)

    def tearDown(self):
        self.dss6.close()
        self.dss7.close()
        self.grids6 = None
        self.grids7 = None

    def test_cataloged_pathnames(self):
        self.assertEqual(self.cat6, self.cat7, "Cataloged pathnames not equal")

    def test_lower_leftX(self):
        gi6 = self.grids6.getGridInfo().getLowerLeftCellX()
        gi7 = self.grids7.getGridInfo().getLowerLeftCellX()
        self.assertEqual(
            gi6,
            gi7,
            "Lower left X fail to equal: Grid6, {} != Grid7, {}".format(gi6, gi7),
        )

    def test_lower_leftY(self):
        gi6 = self.grids6.getGridInfo().getLowerLeftCellY()
        gi7 = self.grids7.getGridInfo().getLowerLeftCellY()
        self.assertEqual(
            gi6,
            gi7,
            "Lower left Y fail to equal: Grid6, {} != Grid7, {}".format(gi6, gi7),
        )

    def test_cellsize(self):
        gi6 = self.grids6.getGridInfo().getCellSize()
        gi7 = self.grids7.getGridInfo().getCellSize()
        self.assertEqual(
            gi6,
            gi7,
            "Cellsize: Grid6, {} != Grid7, {}".format(gi6, gi7),
        )

    def test_cells_x(self):
        gi6 = self.grids6.getGridInfo().getNumberOfCellsX()
        gi7 = self.grids7.getGridInfo().getNumberOfCellsX()
        self.assertEqual(
            gi6,
            gi7,
            "Number of Cells X: Grid6, {} != Grid7, {}".format(gi6, gi7),
        )

    def test_cells_y(self):
        gi6 = self.grids6.getGridInfo().getNumberOfCellsY()
        gi7 = self.grids7.getGridInfo().getNumberOfCellsY()
        self.assertEqual(
            gi6,
            gi7,
            "Number of Cells Y: Grid6, {} != Grid7, {}".format(gi6, gi7),
        )

    def test_data_min(self):
        gi6 = self.grids6.getGridInfo().getMinDataValue()
        gi7 = self.grids7.getGridInfo().getMinDataValue()
        self.assertEqual(
            gi6,
            gi7,
            "Min data value: Grid6, {} != Grid7, {}".format(gi6, gi7),
        )

    def test_data_max(self):
        gi6 = self.grids6.getGridInfo().getMaxDataValue()
        gi7 = self.grids7.getGridInfo().getMaxDataValue()
        self.assertEqual(
            gi6,
            gi7,
            "Max data value: Grid6, {} != Grid7, {}".format(gi6, gi7),
        )

    def test_data_min(self):
        gi6 = self.grids6.getGridInfo().getMinDataValue()
        gi7 = self.grids7.getGridInfo().getMinDataValue()
        self.assertEqual(
            gi6,
            gi7,
            "Mean data value: Grid6, {} != Grid7, {}".format(gi6, gi7),
        )

    def test_data_type(self):
        gi6 = self.grids6.getGridInfo().getDataTypeName()
        gi7 = self.grids7.getGridInfo().getDataTypeName()
        self.assertEqual(
            gi6,
            gi7,
            "Data Type: Grid6, {} != Grid7, {}".format(gi6, gi7),
        )

    def test_data_units(self):
        gi6 = self.grids6.getGridInfo().getDataUnits()
        gi7 = self.grids7.getGridInfo().getDataUnits()
        self.assertEqual(
            gi6,
            gi7,
            "Data units: Grid6, {} != Grid7, {}".format(gi6, gi7),
        )

    def test_start_time(self):
        gi6 = self.grids6.getGridInfo().getStartTime()
        gi7 = self.grids7.getGridInfo().getStartTime()
        self.assertEqual(
            gi6,
            gi7,
            "Start time: Grid6, {} != Grid7, {}".format(gi6, gi7),
        )

    def test_end_time(self):
        gi6 = self.grids6.getGridInfo().getEndTime()
        gi7 = self.grids7.getGridInfo().getEndTime()
        self.assertEqual(
            gi6,
            gi7,
            "Start time: Grid6, {} != Grid7, {}".format(gi6, gi7),
        )

    def test_srs(self):
        gi6 = self.grids6.getGridInfo().getSpatialReferenceSystem()
        gi7 = self.grids7.getGridInfo().getSpatialReferenceSystem()
        self.assertEqual(
            gi6,
            gi7,
            "Grid SRS: Grid6, {} != Grid7, {}".format(gi6, gi7),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
