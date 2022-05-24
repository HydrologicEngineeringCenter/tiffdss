#include <string.h>
#include <stdlib.h>

#include "heclib.h"

void compute_grid_statistics(zStructSpatialGrid* grid );

void print_grid_data(float* data, int size){

for(int i=0; i<size; i++)
    {
        if (data[i] !=0)
          printf("%f ",data[i]);
    }
}

int save_to_dss(const char* filename, const char* dssPath, float* data,int data_size , int cols, 
    int rows, double nodata)
{
	//print_grid_data(data,data_size);
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

    zStructSpatialGrid *gridStructStore;
	int idx;
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




	if (data != NULL) {
		gridStructStore->_data = data;
		printf("\nabout to compute stats...\n");
		compute_grid_statistics(gridStructStore);
		printf("\nreturn from compute stats...\n");
		printGridStruct(ifltab, 0, gridStructStore);
		zset("mlvl","",22);
		status = zspatialGridStore(ifltab, gridStructStore);
		if (status != STATUS_OKAY) {
			printf("Error storing grid: %d", status);
		}
		//printGridStruct(ifltab, 0, gridStructStore);
		zstructFree(gridStructStore);

	}
	zclose(ifltab);
	return status;
}

void compute_grid_statistics(zStructSpatialGrid* grid ){
    int numberOfRanges = 13;
	grid->_numberOfRanges = numberOfRanges;
	if( grid->_rangeLimitTable != 0)
	    free(grid->_rangeLimitTable);
	
	grid->_rangeLimitTable = (float *)calloc(grid->_numberOfRanges, 4);

	float* range = (float*)grid->_rangeLimitTable;

     if( grid->_numberEqualOrExceedingRangeLimit!=0)
	    free(grid->_numberEqualOrExceedingRangeLimit);

	grid->_numberEqualOrExceedingRangeLimit = (int *)calloc(grid->_numberOfRanges, 4);
	int* count = (int*)grid->_numberEqualOrExceedingRangeLimit;

     // set the default range
	if( UNDEFINED_FLOAT < 0.){
		range[0]  = UNDEFINED_FLOAT;
	}else{
		range[0]  = -UNDEFINED_FLOAT;
	}

	range[1]  =    0.0f;
	range[2]  =    0.0000001f;
	range[3]  =    5.0f;
	range[4]  =   10.0f;
	range[5]  =   20.0f;
	range[6]  =   50.0f;
	range[7]  =  100.0f;
	range[8]  =  200.0f;
	range[9]  =  500.0f;
	range[10] = 1000.0f;
	range[11] = 2000.0f;
	range[12] = 5000.0f;
	
  int x = grid->_numberOfCellsX;
  int y = grid->_numberOfCellsY;

  float* data = (float*)grid->_data;
  float max = -2.0e38f;
  float min = 2.0e38f;
  float mean = UNDEFINED_FLOAT;
  float sum = 0.0f;		
  int numDefined=0;

  for (int i = 0; i<x; i++) {
    for (int j = 0; j<y; j++) {
      int k = j * x + i;
	  //if( data[k] != 0.0)
		//  printf("\ndata[%d] %f",k,data[k]);

      if (data[k] != UNDEFINED_FLOAT) {
        numDefined++;
        sum += data[k];
        if (data[k] > max)  max = data[k];
        if (data[k] < min)  min = data[k];
      }

      for (int n = 0; n<numberOfRanges; n++)
        if (data[k] >= range[n]) count[n]++;

    }
  }
  if (numDefined > 0){
   mean = sum / numDefined;
  }
  else {
    max = UNDEFINED_FLOAT;
    min = UNDEFINED_FLOAT;
    mean = UNDEFINED_FLOAT;
  }
  	
	grid->_maxDataValue = calloc(1, sizeof(float));
	grid->_minDataValue = calloc(1, sizeof(float));
	grid->_meanDataValue = calloc(1, sizeof(float));

    *((float*)grid->_maxDataValue) = max;
	*((float*)grid->_minDataValue) = min;
	*((float*)grid->_meanDataValue) = mean;

}
