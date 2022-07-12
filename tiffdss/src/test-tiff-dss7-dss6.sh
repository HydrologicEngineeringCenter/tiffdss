#!/bin/bash
# test creation of DSS files 
# process: tiffdss -> dss7 --> dss6(java)

DSS_PATH="//grid-test/PRECIP/01FEB2022:0100/01FEB2022:0200/SHG-Default/"
TIFF_FILE=/app/dss-test-data/tiff/MRMS_MultiSensor_QPE_01H_Pass1_00.00_20220216-170000.tif
DSS7_FILE=/tmp/dss7-test1.dss
DSS6_FILE=/tmp/dss6-test1.dss

rm -f $DSS7_FILE $DSS6_FILE

# create DSS 7 file
./tiffdss -d INST-CUM -p $DSS_PATH  $TIFF_FILE $DSS7_FILE
# convert to DSS 6 file

/app/hec-dssvue-linux/hec-dssvue-headless.sh /app/dss-convert.py $DSS7_FILE $DSS6_FILE


#age: ./tiffdss  -p [-c] [-d] [-g] [-h] [-m] [-n] [-s] [-u] 
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
#