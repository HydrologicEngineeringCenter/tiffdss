import subprocess
import os
import random
import csv

import unittest

class TestGenDss(unittest.TestCase):
    def setUp(self):
        self.ot = "Float32"
        self.of = "GTiff"
        self.cellsize = 2000
        self.xmin = 456000
        self.ymin = 182000
        self.xmax = 2112000
        self.ymax = 2058000
    
        self.nrows = (self.ymax - self.ymin) / self.cellsize
        self.ncols = (self.xmax - self.xmin) / self.cellsize


        with open("/tmp/demo.csv", "w") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["easting", "northing", "value"])
            for r in range(self.ncols):
                for c in range(self.nrows):
                    csvwriter.writerow([self.xmin, self.ymax, random.random()])
                    self.ymax -= self.cellsize
                self.xmin += self.cellsize

        with open("/tmp/demo.vrt", "w") as vrtfile:
            vrtfile.write('<OGRVRTDataSource>')
            vrtfile.write('\t<OGRVRTLayer name="demo">')
            vrtfile.write('\t\t<SrcDataSource>/tmp/demo.csv</SrcDataSource>')
            vrtfile.write('\t\t<GeometryType>wkbPoint</GeometryType>')
            vrtfile.write('\t\t<GeometryField encoding="PointFromColumns" x="easting" y="northing" z="value"/>')
            vrtfile.write('\t</OGRVRTLayer>')
            vrtfile.write('</OGRVRTDataSource>')
            
        args = [
            "gdal_grid",
            "-ot Float32",
            "-of GTiff",
            "-txe {} {}".format(self.xmin, self.xmax),
            "-tye {} {}".format(self.ymin, self.ymax),
            "-tr {} {}".format(self.cellsize, self.cellsize),
            "-a_srs EPSG:5070",
            "-l demo",
            "/tmp/demo.vrt",
            "/tmp/demo.tiff"
        ]

        p = subprocess.Popen(
            " ".join(args),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
            shell=True,
        )
        
        out, err = p.communicate()
        print(out, err)

    def tearDown(self):
        pass

    def test_test(self):
        pass


if __name__ == "__main__":
    unittest.main()