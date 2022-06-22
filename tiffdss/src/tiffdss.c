#include <ctype.h>
#include <math.h>
#include <unistd.h>
#include <gdal.h>
#include <cpl_string.h>
#include <cpl_conv.h> /* for CPLMalloc() */

#include "heclib.h"
#include "zdssMessages.h"

#include "utils.h"

int writeRecord(long long *ifltab, char *tiff, char *dssfile, char *dsspath,
                char *gridType, int dss_grid_type, char *gridDef, char *dataType,
                int dss_data_type, char *units, char *tzname, int tzoffset,
                int compression_method, int timestamped, float nodata)
{
    int status;
    float _min = 0;
    float _max = 0;
    float _mean = 0;
    float range;

    // see if the record is_interval
    int interval = 0;
    char pathPart[65];
    int _interval = zpathnameGetPart(dsspath, 5, pathPart, sizeof(pathPart));
    if (_interval == 14)
        interval = 1;

    // register the drivers
    GDALAllRegister();

    // get the tiff dataset
    GDALDatasetH hDataset;
    hDataset = GDALOpen(tiff, GA_ReadOnly);

    // get the raster geotransform
    double adfGeoTransform[6];
    GDALGetGeoTransform(hDataset, adfGeoTransform);
    // if (GDALGetGeoTransform(hDataset, adfGeoTransform) == CE_None)
    // {
    //     printf("Origin = (%.6f,%.6f); ",
    //            adfGeoTransform[0], adfGeoTransform[3]);
    //     printf("Pixel Size = (%.6f,%.6f)\n",
    //            adfGeoTransform[1], adfGeoTransform[5]);
    // }

    // get the tiff shape
    int xsize = GDALGetRasterXSize(hDataset);
    int ysize = GDALGetRasterYSize(hDataset);
    int dataSize = xsize * ysize;
    float cellsize = adfGeoTransform[1];
    // printf("Xsize: %d\nYsize: %d\nData Size:%d\n", xsize, ysize, dataSize);

    // get raster band 1
    GDALRasterBandH raster = GDALGetRasterBand(hDataset, 1);

    int llx = (int)adfGeoTransform[0] / adfGeoTransform[1];
    int lly = (int)(adfGeoTransform[5] * ysize + adfGeoTransform[3]) / adfGeoTransform[1];
    // printf("Lower Left X: %i\n", llx);
    // printf("Lower Left Y: %i\n", lly);

    // get the tiff data array
    float *data = (float *)CPLMalloc(sizeof(float) * dataSize);
    GDALRasterIO(raster, GF_Read, 0, 0, xsize, ysize, data, xsize, ysize, GDT_Float32, 0, 0);

    // reversing the array values rotates it 180
    reverse_array(data, dataSize);
    // reverse each row to flip <--> 180
    reverse_rows(data, xsize, dataSize);
    // nodata -> UNDEFINED
    filter_nodata(data, dataSize, nodata);

    // statistics
    _min = minimum(data, dataSize, nodata);
    _max = maximum(data, dataSize, nodata);
    _mean = meanvalue(data, dataSize, nodata);
    // printf("Min: %f Max: %f Mean: %f NoData: %f\n", _min, _max, _mean, nodata);

    // histogram
    range = _max - _min;
    // printf("Data range: %f\n", range);

    int bins = 5;
    if (range == 0)
        bins = 1;

    static float *rangelimit;
    static int *histo;
    rangelimit = calloc(bins, sizeof(float));
    histo = calloc(bins, sizeof(float));

    float step = (float)range / bins;
    // printf("Data step: %f\n", step);

    rangelimit[0] = UNDEFINED_FLOAT;
    rangelimit[1] = _min;
    if (step != 0)
    {
        rangelimit[2] = _min + step * 2;
        rangelimit[3] = _min + step * 3;
        rangelimit[4] = _max;
    }
    for (int idx = 0; idx < dataSize; idx++)
    {
        for (int jdx = 0; jdx < bins; jdx++)
        {
            if (data[idx] >= rangelimit[jdx])
                histo[jdx]++;
        }
    }

    // Spatial Grid Struct
    zStructSpatialGrid *gridStructStore = zstructSpatialGridNew(dsspath);
    gridStructStore->_type = dss_grid_type;
    gridStructStore->_dataSource = "INTERNAL";
    gridStructStore->_version = 1;
    gridStructStore->_dataUnits = units;
    gridStructStore->_dataType = dss_data_type;
    gridStructStore->_numberOfCellsX = xsize;
    gridStructStore->_numberOfCellsY = ysize;
    gridStructStore->_lowerLeftCellX = llx;
    gridStructStore->_lowerLeftCellY = lly;
    gridStructStore->_cellSize = cellsize;
    gridStructStore->_compressionMethod = compression_method;

    gridStructStore->_rangeLimitTable = &rangelimit[0];
    gridStructStore->_numberEqualOrExceedingRangeLimit = &histo[0];
    gridStructStore->_numberOfRanges = bins;

    gridStructStore->_srsDefinitionType = 1;
    gridStructStore->_srsName = gridType;
    gridStructStore->_srsDefinition = gridDef;
    gridStructStore->_xCoordOfGridCellZero = 0;
    gridStructStore->_yCoordOfGridCellZero = 0;
    gridStructStore->_nullValue = nodata;
    gridStructStore->_timeZoneID = tzname;
    gridStructStore->_timeZoneRawOffset = tzoffset;
    gridStructStore->_isInterval = interval;
    gridStructStore->_isTimeStamped = timestamped;

    gridStructStore->_minDataValue = &_min;
    gridStructStore->_maxDataValue = &_max;
    gridStructStore->_meanDataValue = &_mean;

    if (data != NULL)
    {
        gridStructStore->_data = data;
        status = zspatialGridStore(ifltab, gridStructStore);
    }

    GDALClose(hDataset);
    CPLFree(data);

    free(rangelimit);
    free(histo);
    zstructFree(gridStructStore);

    return status;
}

void printUsage(char *name)
{
    printf("usage: %s  -p [-c] [-d] [-g] [-h] [-m] [-n] [-s] [-u] \n"
           "\t-c: DSS compression method; UNDEFINED_COMPRESSION_METHOD or ZLIB_COMPRESSION (default: ZLIB_COMPRESSION)\n"
           "\t-d: DSS data type; PER-AVER | PER-CUM | INST-VAL | INST-CUM (default: PER-AVER)\n"
           "\t-g: DSS grid type; HRAP | ALBERS | SHG | SPECIFIED_GRID_TYPE | UTM (default: ALBERS)\n"
           "\t-h: Hemisphere N or S; use with -g UTM (default: N)\n"
           "\t-n: Time zone name (default: GMT)\n"
           "\t-l: zsetMessageLevel (default: 0 (None))"
           "\t-m: No data value (default: 9999)\n"
           "\t-p: DSS pathname\n"
           "\t-s: DSS grid record time stamped; 0 | 1 (default: 1)\n"
           "\t-u: DSS grid record units (default: MM)\n"
           "\t-z: UTM Zone 1-60; use with -g UTM\n"
           "input_Tiff output_DSS",
           name);
    exit(0);
}

int main(int argc, char *argv[])
{
    int opt;
    int utmZone = 60;
    int status;
    int tzoffset = 0;
    int timestamped = 1;
    int lvl = 0;

    float nodata = 9999;

    char *dataType = "PER-AVER";
    char *gridType = "ALBERS";
    char *gridDef = SHG_SRC_DEFINITION;
    char *tiff;
    char *dssfile;
    char *dsspath = "///////";
    char *units = "MM";
    char *hemisphere = "N";
    char *tzname = "GMT";
    char *compressionMethod = "zlib";

    if (argc < 2)
    {
        printUsage(argv[0]);
    }

    while ((opt = getopt(argc, argv, ":c:d:g:h:l:m:n:p:su:z:")) != -1)
    {
        switch (opt)
        {
        case 'c':
            compressionMethod = optarg;
            break;
        case 'd':
            dataType = optarg;
            break;
        case 'g':
            gridType = optarg;
            break;
        case 'h':
            hemisphere = optarg;
            break;
        case 'l':
            lvl = atoi(optarg);
            break;
        case 'm':
            nodata = atoi(optarg);
            break;
        case 'n':
            tzname = optarg;
            break;
        case 'p':
            dsspath = optarg;
            break;
        case 's':
            timestamped = 0;
            break;
        case 'u':
            units = optarg;
            break;
        case 'z':
            utmZone = atoi(optarg);
            if (utmZone < 1 || utmZone > 60)
            {
                printf("UTM Zones: 1-60 but %i was given\n", utmZone);
                printUsage(argv[0]);
            }
            break;
        case ':':
            printf("option needs a value\n");
            printUsage(argv[0]);
            break;
        case '?':
            if (optopt == opt)
            {
                fprintf(stderr, "Option -%c requires an argument.\n", optopt);
            }
            else if (isprint(optopt))
            {
                fprintf(stderr, "Unknown option `-%c'.\n", optopt);
            }
            else
            {
                fprintf(stderr, "Unknown option character `\\x%x'.\n", optopt);
            }
            return 1;
        default:
            abort();
        }
    }
    // set DSS message level
    zsetMessageLevel(MESS_METHOD_GLOBAL_ID, lvl);

    // check dsspath
    if (strcmp(dsspath, "///////") == 0)
    {
        printf("Define DSS pathname parts: %s\n", dsspath);
        return -1;
    }
    else
    {
        printf("DSS pathname: %s\n", dsspath);
    }

    // get the time zone offset
    tzoffset = tzOffset(tzname);
    printf("Time Zone Name [offset]: %s[%d]\n", tzname, tzoffset);

    // get the grid definition
    int dss_grid_type = dssGridType(gridType);
    gridDef = dssGridDef(dss_grid_type);
    printf("DSS Grid Type: %s[%d]\n", gridType, dss_grid_type);

    // get the data type
    int dss_data_type = dssDataType(dataType);
    printf("DSS data type[type]: %s[%d]\n", dataType, dss_data_type);

    int compression_method = dssCompressionMethod(compressionMethod);
    printf("Compression method [val]: %s[%d]\n", compressionMethod, compression_method);

    // define UTM grid definition
    if (dss_grid_type == 430)
    {
        gridDef = utmGridDef(utmZone, hemisphere);
        printf("Hemisphere: %s", hemisphere);
        printf("UTM Def: %s", gridDef);
    }

    // last two non-optional arguments are input file (tiff) output file (dss)
    tiff = argv[argc - 2];
    printf("Tiff file: %s\n", tiff);
    dssfile = argv[argc - 1];
    printf("DSS file: %s\n", dssfile);

    // write record
    long long *ifltab = calloc(250, sizeof(long long) * 250);

    status = zopen7(ifltab, dssfile);
    if (status != STATUS_OKAY)
    {
        printf("Zopen Status: %d\n", status);
        return -1;
    }
    status = writeRecord(ifltab, tiff, dssfile, dsspath, gridType, dss_grid_type,
                         gridDef, dataType, dss_data_type, units, tzname, tzoffset,
                         compression_method, timestamped, nodata);
    if (status != STATUS_OKAY)
    {
        printf("Write Record: %d\n", status);
        return -1;
    }

    zclose(ifltab);
    return 1;
}
