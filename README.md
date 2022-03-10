
## DSS utilities within Docker.

This projects first goal is to convert a GeoTIFF to a DSS record.


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

docker build -f Dockerfile.develop  -t karl-dev


## run developer container with pwd mounted under /code

docker run -it -v$(pwd):/code:z karl-dev# dss-docker
