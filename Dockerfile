# Compile DSS
FROM ubuntu:18.04 AS cbuilder

RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install -y gcc gfortran zlib1g-dev make git && \
    rm -rf /var/lib/apt/lists/*

COPY Makefile /

RUN git clone --branch 7-IP https://github.com/HydrologicEngineeringCenter/hec-dss.git

RUN make

# tiffdss image
FROM osgeo/gdal:ubuntu-small-3.5.0 as tiffdss

# update, install and clean up
# apt-get -y upgrade && \
RUN apt-get -y update && \
    apt-get install -y git gcc gfortran python3-pip libffi-dev gdb && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/tiffdss

COPY ./tiffdss /app/tiffdss/

RUN git clone --depth 1 https://github.com/HydrologicEngineeringCenter/hec-dssvue-linux.git

RUN git clone --depth 1 https://github.com/jeffsuperglide/gribdownload.git

WORKDIR /app/tiffdss

# Copy archives and headers from cbuilder
COPY --from=cbuilder --chown=root:root /hec-dss/heclib/heclib_c/Output/libhec_c.a /usr/lib
COPY --from=cbuilder --chown=root:root /hec-dss/heclib/heclib_f/Output/libhec_f.a /usr/lib
COPY --from=cbuilder --chown=root:root /hec-dss/heclib/heclib_c/src/headers /hec-dss/heclib/heclib_c/src/headers

RUN bash /app/tiffdss/src/make.sh

# RUN useradd appuser
# USER appuser

# keep the container running
CMD [ "/app/tiffdss/tests/dss-test.sh" ]
