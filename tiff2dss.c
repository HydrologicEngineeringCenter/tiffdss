// Convert from GeoTiff to a DSS record

//#include <stdlib.h>
#include "gdal.h"
#include "gdal_utils.h"
#include "cpl_conv.h" /* for CPLMalloc() */

/*
gcc -Wall tiff2dss.c -o tiff2dss -lgdal  -lm -

#python.

system.exec('tiff2dss /tmp/abc.tif /tmp/xyz.dss ..... ')

*/
int tiff2dss(char* tiffFileName, char* dssFileName, char* dssPath,char* dss_type, char* grid_type)
{
    // https://github.com/USACE/cumulus-api/blob/stable/async_packager/packager/writers/dss7.py
    char* msg;
    GDALDatasetH  hDataset;
    GDALAllRegister();
    hDataset = GDALOpen( tiffFileName, GA_ReadOnly );
    if( hDataset != NULL )
    {
    msg = GDALInfo(hDataset, NULL);
    printf("\n%s",msg);
    }
    else{
     printf("\nError.... reading %s",tiffFileName);
    }
    
     CPLFree(msg);

    //return 1;
}

int main(){
    //https://gdal.org/user/virtual_file_systems.html
    ///vsis3/, /vsigs/, /vsiaz/, /vsioss/ or /vsiswift/.
     //tiff2dss("s3://myaws-east1.1255/a.tif","a.dss","/GRID/RECORD/DATA/01jan2019:1200/01jan2019:1300/Ex10a/","PER-AVER","specified");
    int rval = tiff2dss("a.tif","a.dss","/GRID/RECORD/DATA/01jan2019:1200/01jan2019:1300/Ex10a/","PER-AVER","specified");
    if(rval != 0)
    {
        printf("\nerrro... %d",rval);
    }
}
