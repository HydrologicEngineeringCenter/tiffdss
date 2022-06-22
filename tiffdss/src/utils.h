typedef struct
{
    /* data */
    float minimum;
    float maximum;
    float meanval;
} GridStats;

typedef struct
{
    char *tiff;
    char *dssfile;
    char *dsspath;
    char *gridtype;
    int dssgridtype;
    char *gridDef;
    char *datatype;
    int dssdatatype;
    char *units;
    char *tzname;
    int tzoffset;
    int compression;
    int is_stamped;
} zStructSpatialGridWrite;

void reverse_array(float *arr, int zsize);

void reverse_rows(float *arr, int cols, int datasize);

void filter_zeros(float *arr, int datasize, const char *cpart);

void filter_nodata(float *arr, int datasize, float nodata);

float maximum(float *arr, int n, float nodata);

float minimum(float *arr, int n, float nodata);

float meanvalue(float *arr, int n, float nodata);

int dssDataType(const char *dType);

int dssCompressionMethod(const char *compressMethod);

int tzOffset(const char *tz);

int dssGridType(const char *gtype);

char *dssGridDef(int gtype);

char *utmGridDef(int zone, char *utmHemi);
