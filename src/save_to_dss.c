#include <string.h>
#include <stdlib.h>

#include "heclib.h"


int save_to_dss(const char* filename, const char* dssPath, float* data,int data_size , int cols, int rows)
{
	long long ifltab[250];
	memset(ifltab, 0, 250 * sizeof(long long));

	int status = zopen(ifltab, filename);
	if (status != STATUS_OKAY) {
		printf("Error opening file: '%s'\n error code=%d",filename, status);
		return status;
	}

		if (zgetVersion(ifltab) != 7) {
			printf("\nError. Dssfile must be dss version 7\n");
		return -2;
	}

    int range =2;
 
    zStructSpatialGrid *gridStructStore;
	int idx;

	static float *rangelimit;
	static int *histo;

	rangelimit =(float*)  calloc(range, sizeof(float));
	histo = (int*)calloc(range, sizeof(int));

	for (idx = 0; idx < range; idx++) {
		rangelimit[idx] = idx * 1.1;
		histo[idx] = idx * 2;
	}

	gridStructStore = zstructSpatialGridNew(dssPath);

	//   Gen data
	gridStructStore->_type = 420;
	gridStructStore->_dataSource = "INTERNAL";
	gridStructStore->_version = 1;
	gridStructStore->_dataUnits = "mm";
	gridStructStore->_dataType = PER_AVER;
	gridStructStore->_lowerLeftCellX = 0;
	gridStructStore->_lowerLeftCellY = 0;
	gridStructStore->_numberOfCellsX = cols;
	gridStructStore->_numberOfCellsY = rows;
	gridStructStore->_cellSize = 5.0;
	gridStructStore->_compressionMethod = ZLIB_COMPRESSION;

	gridStructStore->_rangeLimitTable = &(rangelimit[0]);
	gridStructStore->_numberEqualOrExceedingRangeLimit = &(histo[0]);
	gridStructStore->_numberOfRanges = range;
	gridStructStore->_srsDefinitionType = 1;
	gridStructStore->_srsName = "SRC_NAME";
	gridStructStore->_srsDefinition = "TEST";
	gridStructStore->_xCoordOfGridCellZero = 10.2;
	gridStructStore->_yCoordOfGridCellZero = 20.3;
	gridStructStore->_nullValue = 99999.999;
	gridStructStore->_timeZoneID = "PST";
	gridStructStore->_timeZoneRawOffset = 8;
	gridStructStore->_isInterval = 1;
	gridStructStore->_isTimeStamped = 0;

	float max = (rows * cols)*1.2, min = 0.001, mean = (rows * cols * 1.2) / 2.0;
	gridStructStore->_maxDataValue = &max;
	gridStructStore->_minDataValue = &min;
	gridStructStore->_meanDataValue = &mean;

	// Data
	data = (float*)calloc(gridStructStore->_numberOfCellsX * gridStructStore->_numberOfCellsY, sizeof(float));

	if (data != NULL) {
		for (idx = 0; idx < gridStructStore->_numberOfCellsX * gridStructStore->_numberOfCellsY; idx++)
			data[idx] = (idx * 1.2);
		gridStructStore->_data = data;

		status = zspatialGridStore(ifltab, gridStructStore);

		if (status != STATUS_OKAY) {
			printf("Error storing grid: %d", status);
		}

		//printGridStruct(ifltab, 0, gridStructStore);
		free(data);
		zstructFree(gridStructStore);

	}
	return status;
}
