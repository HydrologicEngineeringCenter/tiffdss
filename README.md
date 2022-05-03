
## DSS utilities within Docker.

This projects first goal is to convert a GeoTIFF to a DSS record.

clone with 
```bash
git clone https://github.com/HydrologicEngineeringCenter/dss-container.git
git submodule update --init --recursive
```


Design expressed below as a feature list by example:


```bash
# import geotiff file into a DSS grid record
docker run -v $(pwd):/data hec/dss tiff2dss /data/test.tif data/test.dss  "/GRID/RECORD/DATA/01jan2019:1200/01jan2019:1300/Ex10a/" --data-type PER-AVER --grid-type specified --wkt="..."

# convert from dss version 7 to dss version 6
docker run -v $(pwd):/data hec/dss convert-version  data/input-test6.dss   data/output-test7.dss

# print catalog of a dss file
docker run -v $(pwd):/data hec/dss print-catalog data/test.dss  

#print data-set inside a dss file to the console
docker run -v $(pwd):/data hec/dss print-dataset data/test.dss  "//SACRAMENTO/PRECIP-INC/01Jan1877/1Day/OBS/"

```


## Build container for development

docker build . -t karl-dev


## run developer container with pwd mounted under /code

docker run -it -v$(pwd):/code:z karl-dev

# some gdal examples

 docker run --rm -v $PWD:/karl osgeo/gdal:alpine-small-latest gdal_translate -of AAIGrid karl/dss-test-data/tiff/MRMS_MultiSensor_QPE_01H_Pass1_00.00_20220216-190000.tif   karl/a.txt

docker run --rm -v $PWD:/karl osgeo/gdal:alpine-small-latest gdalinfo  karl/dss-test-data/tiff/MRMS_MultiSensor_QPE_01H_Pass1_00.00_20220216-190000.tif  


# references

https://github.com/USACE/pydsstools/blob/testing/2.1.1/tests/test1.py

https://github.com/USACE/cumulus-api/blob/stable/async_packager/packager/writers/dss7.py
