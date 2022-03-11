// Convert from GeoTiff to a DSS record

#include "gdal.h"
#include "gdal_utils.h"
#include "cpl_conv.h" /* for CPLMalloc() */

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
     return -1;
    }
    
     CPLFree(msg);

    return 0;
}

