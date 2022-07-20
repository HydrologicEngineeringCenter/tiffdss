import sys
import subprocess
import unittest
from hec.heclib.dss import  HecDSSFileAccess
from dss_test_utility import compare_grids

from hec.heclib.util import Heclib
from hec.heclib.dss import HecDss, DSSPathname, HecDataManager,HecDSSUtilities

class dss_test(unittest.TestCase):

    @staticmethod
    def convertDSS7ToDss6(dss6,dss7):
        u = HecDSSUtilities()
        #HecDSSFileAccess.setMessageLevel(15)
        u.setDSSFileName(dss7)
        status = u.convertVersion(dss6)
        u.close()
        if status != 0:
            raise Exception("error converting from DSS7 to DSS6 ")
            

    # create DSS 7 file
    @staticmethod
    def tiffToDss7(test):
        dss7=test["name"]+"7.dss"

        args=["/app/tiffdss/src/tiffdss",test["tiff_dss_args"], test["tiffFile"],dss7]

        print(" ".join(args))
        cmd = " ".join(args)
        proc = subprocess.Popen(cmd ,stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True, shell=True)
        out = str(proc.communicate(proc.stdout))
        print(out)

    @staticmethod
    def checkResults(test):
        dss6=test["name"]+"6.dss"
        dss7=test["name"]+"7.dss"
        compare_grids(dss7,dss6,test["dssPath"])

    def testSimple(self):
        test ={
        "name": "simple",
        "dssPath" : "//grid-test/PRECIP/01FEB2022:0100/01FEB2022:0200/SHG-Default/",
        "tiffFile":"/app/dss-test-data/tiff/MRMS_MultiSensor_QPE_01H_Pass1_00.00_20220216-170000.tif",
        "tiff_dss_args":"-d INST-CUM -p '//grid-test/PRECIP/01FEB2022:0100/01FEB2022:0200/SHG-Default/'"
        }
        dss6=test["name"]+"6.dss"
        dss7=test["name"]+"7.dss"
        status = dss_test.tiffToDss7(test)
        if status !=0:
            print("Error creating "+dss7)
        dss_test.convertDSS7ToDss6(dss6,dss7)
        dss_test.checkResults(test)

if __name__ == '__main__':
    unittest.main()


#Usage: ./tiffdss  -p [-c] [-d] [-g] [-h] [-m] [-n] [-s] [-u] 
#	-c: DSS compression method; UNDEFINED_COMPRESSION_METHOD or ZLIB_COMPRESSION (default: ZLIB_COMPRESSION)
#	-d: DSS data type; PER-AVER | PER-CUM | INST-VAL | INST-CUM (default: PER-AVER)
#	-g: DSS grid type; HRAP | ALBERS | SHG | SPECIFIED_GRID_TYPE | UTM (default: ALBERS)
#	-h: Hemisphere N or S; use with -g UTM (default: N)
#	-n: Time zone name (default: GMT)
#	-l: zsetMessageLevel (default: 0 (None))
#	-m: No data value (default: 9999)
#	-p: DSS pathname
#	-s: DSS grid record time stamped; 0 | 1 (default: 1)
#	-u: DSS grid record units (default: MM)
#	-z: UTM Zone 1-60; use with -g UTM
#input_Tiff> <output_DSS>
#