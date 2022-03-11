// Convert from GeoTiff to a DSS record
#include <stdio.h>
#include "tiff2dss.h"


int main(){
    int rval = tiff2dss("../dss-test-data/tiff/MRMS_MultiSensor_QPE_01H_Pass1_00.00_20220216-170000.tif",
    "a.dss","/GRID/RECORD/DATA/01jan2019:1200/01jan2019:1300/Ex10a/","PER-AVER","specified");
    if(rval != 0)
    {
        printf("\nerror processing ... %d",rval);
    }
    return rval;
}
