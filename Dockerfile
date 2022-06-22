# Compile DSS
FROM ubuntu:18.04 AS cbuilder

RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install -y gcc gfortran zlib1g-dev make git && \
    rm -rf /var/lib/apt/lists/*

COPY ./hec-dss /hec-dss

COPY ./dss-test-data /dss-test-data

COPY Makefile /

RUN make

# tiffdss image
FROM osgeo/gdal:ubuntu-small-3.5.0 as tiffdss

# update, install and clean up
# apt-get -y upgrade && \
RUN apt-get -y update && \
    apt-get install -y gcc gfortran python3-pip libffi-dev gdb && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/tiffdss

COPY ./tiffdss /app/tiffdss/

WORKDIR /app/tiffdss

# Copy archives and headers from cbuilder
COPY --from=cbuilder --chown=root:root /hec-dss/heclib/heclib_c/Output/libhec_c.a /usr/lib
COPY --from=cbuilder --chown=root:root /hec-dss/heclib/heclib_f/Output/libhec_f.a /usr/lib
COPY --from=cbuilder --chown=root:root /hec-dss/heclib/heclib_c/src/headers /hec-dss/heclib/heclib_c/src/headers

COPY --from=cbuilder --chown=root:root /dss-test-data/tiff/*.tif /dss-test-data/tiff/

RUN bash /app/tiffdss/src/make.sh

# RUN useradd appuser
# USER appuser

# keep the container running
CMD [ "tail", "-f", "/dev/null" ]
