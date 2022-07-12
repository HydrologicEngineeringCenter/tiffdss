import sys
import subprocess
from hec.heclib.util import Heclib
from hec.heclib.dss import HecDss, DSSPathname, HecDataManager,HecDSSUtilities


def convertDSS7ToDss6(dss6,dss7):
    u = HecDSSUtilities()
    u.setDSSFileName(dss7)
    status = u.convertVersion(dss6)
    u.close()
    if status != 0:
        print("error convertind from DSS7 to DSS6 ")

# create DSS 7 file
def tiffToDss7(test):

    args=["/app/tiffdss/src/tiffdss"]
    args=args+test.tiff_dss_args
    CompletedProcess = subprocess.run(args)
    print(CompletedProcess.stdout)
    return CompletedProcess.returncode


def checkResults(test):
    print("checking")

def runTest(test):
    dss6=test.name+"6.dss"
    dss7=test.name+".dss"
    status = tiffToDss7(test)
    if status !=0:
        print("Error creating "+dss7)
    convertDSS7ToDss6(test)
    checkResults(test)

runTest({
    "name": "simple",
    "dssPath" : "//grid-test/PRECIP/01FEB2022:0100/01FEB2022:0200/SHG-Default/",
    "tiffFile":"/app/dss-test-data/tiff/MRMS_MultiSensor_QPE_01H_Pass1_00.00_20220216-170000.tif",
    "tiff_dss_args":["-d INST-CUM"],
    "expected": {"min":1.0, "max":3.4, "avg":6.0}
})


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