import json
import os
import re
import subprocess
import sys
import unittest
from datetime import datetime, timedelta

from hec.heclib.dss import HecDSSFileAccess

this = "/tiffdss/tests/integration"


class TestDssConvert(unittest.TestCase):
    @staticmethod
    def convert_to_dss(tif, dss, *args):
        _args = " ".join(args)
        cmd = " ".join(["/tiffdss/src/tiffdss", _args, tif, dss])
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
            shell=True,
        )
        stdout, stderr = proc.communicate()
        if stderr:
            return 0
        else:
            return 1

    @staticmethod
    def gdalinfo(tif):
        p = subprocess.Popen(
            "gdalinfo -json {}".format(tif),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
            shell=True,
        )
        stdout, stderr = p.communicate()
        return stdout

    @classmethod
    def meta_time(cls, attr):
        pattern = re.compile("^(\\d+).*")
        m = pattern.match(attr).group(1)
        dt = datetime.fromtimestamp(int(m))
        return dt

    def setUp(self):
        self.fixtures = os.path.join(this, "fixtures")
        self.dss7 = os.path.join("/tmp", "test7.dss")
        self.dss6 = os.path.join("/tmp", "test6.dss")
        if os.path.exists(self.dss7):
            os.remove(self.dss7)
        if os.path.exists(self.dss6):
            os.remove(self.dss6)
        test_products = os.path.join(this, "fixtures", "test_products.json")
        with open(test_products, "r") as f:
            self.products = json.load(f)

    def test_convert_tiff(self):
        for p, attr in self.products.items():
            self.p_path = os.path.join(self.fixtures, p)
            if os.path.exists(self.p_path):
                nrecords = 0
                for dirpath, dirnames, filenames in os.walk(self.p_path):
                    for filename in filenames:
                        tif = os.path.join(dirpath, filename)

                        stdout = self.gdalinfo(tif)
                        metadata_dict = json.loads(stdout)

                        vtime = self.meta_time(
                            metadata_dict["bands"][0]["metadata"][""]["GRIB_VALID_TIME"]
                        )
                        etime = vtime + timedelta(seconds=attr["data_interval"])
                        dsspath = "/{}/{}/{}/{}/{}/{}/".format(
                            attr["apart"],
                            attr["bpart"],
                            attr["cpart"],
                            vtime.strftime("%d%b%Y:%H%M").upper(),
                            etime.strftime("%d%b%Y:%H%M").upper(),
                            attr["fpart"],
                        )
                        # convert tiff to dss7
                        self.convert_to_dss(
                            tif,
                            self.dss7,
                            "-d {}".format(attr["data_type"].upper()),
                            "-u {}".format(attr["data_unit"].upper()),
                            "-p '{}'".format(dsspath),
                            "-m -999",
                        )
                        nrecords += 1
        file_access = HecDSSFileAccess(self.dss7)
        dss_records = file_access.getNumberRecords()
        self.assertEqual(nrecords, dss_records)


if __name__ == "__main__":
    unittest.main(verbosity=2)
