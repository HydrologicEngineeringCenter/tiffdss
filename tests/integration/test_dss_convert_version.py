import json
import os
import unittest

from hec.heclib.dss import HecDSSUtilities
from hec.heclib.util import Heclib

this = "/tiffdss/tests/integration"


class TestDssConvert(unittest.TestCase):
    def setUp(self):
        Heclib.Hec_zsetMessageLevel(0, 0)
        self.fixtures = os.path.join(this, "fixtures")
        self.dss7 = os.path.join("/tmp", "test7.dss")
        self.dss6 = os.path.join("/tmp", "test6.dss")
        test_products = os.path.join(this, "fixtures", "test_products.json")
        with open(test_products, "r") as f:
            self.products = json.load(f)

    def test_convert_version(self):
        if os.path.exists(self.dss7):
            # dss7
            u = HecDSSUtilities()
            u.setDSSFileName(self.dss7)
            dss7_version = u.getDssFileVersion()
            status = u.convertVersion(self.dss6)
            u.close()
            # dss6
            u.setDSSFileName(self.dss6)
            dss6_version = u.getDssFileVersion()
            u.close()
            # compare versions
            self.assertNotEqual(dss6_version, dss7_version)


if __name__ == "__main__":
    unittest.main(verbosity=2)
