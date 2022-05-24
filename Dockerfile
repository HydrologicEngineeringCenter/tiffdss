FROM osgeo/gdal:alpine-normal-3.4.1

RUN apk add gcc g++ gfortran zlib-dev gdb make
ARG UID=1000
RUN adduser -D karl -u $UID 
#USER karl