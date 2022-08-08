# Convert GeoTiff to DSS Grid Record

This repository contains a utility to read a GeoTiff (single band) and write the data to a DSS grid record.

# Local Development

## Start the Container

```
> ./docker_run.sh
```

Dockerfile uses `entrypoint` and `CMD` arguments:
- integration
- unit
- run

`integration` and `unit` run those tests, and `run` keeps the container running.  Arguments can be used in any combination.

## Build tiffdss

With an interactive container session

```
> /app/tiffdss/src/make.sh
```

# Usage: tiffdsss binary

```
tiffdss -p [-c] [-d] [-g] [-h] [-m] [-n] [-s] [-u] <input_Tiff> <output_DSS>
```

## Options

```
-c [UNDEFINED_COMPRESSION_METHOD | ZLIB_COMPRESSION]
    DSS compression method;  or  (default: ZLIB_COMPRESSION)

-d [PER-AVER | PER-CUM | INST-VAL | INST-CUM]
    DSS data type; (default: PER-AVER)

-g [HRAP | ALBERS | SHG | SPECIFIED_GRID_TYPE | UTM]
    DSS grid type; (default: ALBERS)

-h [N | S]
    Hemisphere N or S; use with -g UTM (default: N)

-n
    Time zone name (default: GMT)

-l
    zsetMessageLevel (default: 0 (None))

-m
    No data value (default: 9999)

-p "/a/b/c/d/e/f/"
    DSS pathname

-s [0 | 1]
    DSS grid record time stamped; (default: 1)

-u
    DSS grid record units (default: MM)

-z
    UTM Zone 1-60; use with -g UTM
```

## Python Unit Testing

### Integration Test
1. Converting GeoTiff(s) in `tests/integration/fixtures` to DSS7
2. Converting the DSS7 file to DSS6
3. GridInfo differences between DSS7/DSS6

### fixtures JSON setup:

This example will test each GeoTiff in the `fixtures/mrms` directory.  Each of the attributes must correspond to the GeoTiff metadata.

test_products.json
```json
{
    "mrms": {
        "apart": "",
        "bpart": "mrms",
        "cpart": "precip",
        "fpart": "qpe",
        "data_type": "per-cum",
        "data_unit": "mm",
        "data_interval": 3600
    },
    "hrrr": {
        "apart": "",
        "bpart": "hrrr",
        "cpart": "precip",
        "fpart": "qpe",
        "data_type": "inst-val",
        "data_unit": "mm",
        "data_interval": 3600
    }
}
```

### Unit Test
1. `libtiffdss.so` C function testing
2. Numpy arrays (zeros, ones, random, and missing) generated
3. Numpy array statistics (min, max, and mean) compared to shared object statistics

Unit testing against the `libtiffdss.so` shared object uses Python `ctypes` module.  The shared object is moved to `/usr/lib` during the build process to simplify loading the library.

