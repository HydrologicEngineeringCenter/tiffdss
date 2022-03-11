#include "gdal_priv.h"
#include "cpl_conv.h" // for CPLMalloc()

void PrintDataSetInfo(GDALDataset* ds );

int main()
{
    GDALAllRegister();
    const char* pszFilename="../dss-test-data/tiff/MRMS_MultiSensor_QPE_01H_Pass1_00.00_20220216-170000.tif";
     GDALDataset* ds = (GDALDataset*) GDALOpenEx( pszFilename,
                      GDAL_OF_READONLY | GDAL_OF_RASTER | GDAL_OF_VERBOSE_ERROR,
                      nullptr, //psOptionsForBinary->papszAllowInputDrivers,
                      nullptr , //psOptionsForBinary->papszOpenOptions, 
                      nullptr );

    
     if( ds == nullptr )
    {
        fprintf( stderr,
                 "gdalinfo failed - unable to open '%s'.\n", pszFilename );
    } 
    PrintDataSetInfo(ds);
    GDALRasterBand* grid = ds->GetRasterBand(1);
    int xsize = grid->GetXSize();
    int ysize = grid->GetYSize();
    double nodata = grid->GetNoDataValue();

    printf("\nxsize = %d, ysize = %d",xsize,ysize);
    int data_count = xsize*ysize;
    printf("\nnodata = %lf",nodata);
    printf("\n");
    float* data = (float *) CPLMalloc(sizeof(float)*(data_count));
    int status = grid->RasterIO( GF_Read, 0, 0, xsize, ysize,
                data, xsize, ysize, GDT_Float32,  0, 0 );

    if(status == CE_Failure )
    {
        printf("\nError reading grid data");
    }
    for(int i=0; i<xsize; i++)
    {
        if (data[i] !=0)
          printf("%f ",data[i]);
    }

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