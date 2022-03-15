#include "gdal_priv.h"
#include "cpl_conv.h" // for CPLMalloc()
#include "save_to_dss.h"

void PrintDataSetInfo(GDALDataset* ds );

int main(int argc, const char *args[] )
{

    if( argc != 4 )
    {
     printf("\nUsage: tiff2dss file.tiff file.dss dssPath\n");
     printf("\nExample\n\n tiff2dss /tmp/precip_12.tiff precip_12.dss \"/HRAP/MARFC/PRECIP/23JUL2003:0400/23JUL2003:0500/NEXRAD/\"\n");

     return -1;   
    }
    
    const char* tiffFilename=args[1];
    const char* dssFilename=args[2];
    const char* dssPathname=args[3];

    GDALAllRegister();
     GDALDataset* ds = (GDALDataset*) GDALOpenEx( tiffFilename,
                      GDAL_OF_READONLY | GDAL_OF_RASTER | GDAL_OF_VERBOSE_ERROR,
                      nullptr, //psOptionsForBinary->papszAllowInputDrivers,
                      nullptr , //psOptionsForBinary->papszOpenOptions, 
                      nullptr );

    
     if( ds == nullptr )
    {
        fprintf( stderr,
                 "gdalinfo failed - unable to open '%s'.\n", tiffFilename );
    } 
    PrintDataSetInfo(ds);
    GDALRasterBand* grid = ds->GetRasterBand(1);
    int xsize = grid->GetXSize();
    int ysize = grid->GetYSize();
    double nodata = grid->GetNoDataValue();

    printf("\nxsize = %d, ysize = %d",xsize,ysize);
    int data_size = xsize*ysize;
    printf("\nnodata = %lf",nodata);
    printf("\n");
    float* data = (float *) CPLMalloc(sizeof(float)*(data_size));
    int status = grid->RasterIO( GF_Read, 0, 0, xsize, ysize,
                data, xsize, ysize, GDT_Float32,  0, 0 );

    if(status == CE_Failure )
    {
        printf("\nError reading grid data");
    }
    else
    { //int save_to_dss(char* filename, char* dssPath, float* data,int data_size , int cols, int rows)
        save_to_dss(dssFilename,dssPathname,data,data_size,xsize,ysize);
    }
    int count =0;

    for(int i=0; i<xsize; i++)
    {
        if (data[i] !=0)
          printf("%f ",data[i]);

        count ++;

        if (count >10)
           break;
    }

    CPLFree(data);
    GDALClose(ds);

}

void PrintDataSetInfo(GDALDataset* ds ){
    double        adfGeoTransform[6];
printf( "Driver: %s/%s\n",
        ds->GetDriver()->GetDescription(),
        ds->GetDriver()->GetMetadataItem( GDAL_DMD_LONGNAME ) );
printf( "Size is %dx%dx%d\n",
        ds->GetRasterXSize(), ds->GetRasterYSize(),
        ds->GetRasterCount() );
if( ds->GetProjectionRef()  != NULL )
    printf( "Projection is `%s'\n", ds->GetProjectionRef() );
if( ds->GetGeoTransform( adfGeoTransform ) == CE_None )
{
    printf( "Origin = (%.6f,%.6f)\n",
            adfGeoTransform[0], adfGeoTransform[3] );
    printf( "Pixel Size = (%.6f,%.6f)\n",
            adfGeoTransform[1], adfGeoTransform[5] );
}
}