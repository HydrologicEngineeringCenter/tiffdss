ARG GDAL_VERSION=ubuntu-full-3.7.0

# ~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
# builder
# ~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
FROM ghcr.io/osgeo/gdal:${GDAL_VERSION} AS builder

ARG HECDSS_VERSION=master
ARG DSSVUE_VERSION=main

# # solving possible issue of ATP behind a proxy
RUN cat <<EOF > /etc/apt/apt.conf.d/99proxy
Acquire::http::Pipeline-Depth 0;
Acquire::http::No-Cache true;
Acquire::BrokenProxy true;
EOF

# && apt-get -y install build-essential gfortran zlib1g-dev\
RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get -y install make gcc gfortran zlib1g-dev libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ADD --keep-git-dir=false https://github.com/HydrologicEngineeringCenter/hec-dss.git#${HECDSS_VERSION}:heclib /heclib

# compile dss c
WORKDIR /heclib/heclib_c
RUN make

# compile dss fortran
WORKDIR /heclib/heclib_f
RUN make

# compile tiffdss
WORKDIR /tiffdss/src

COPY ./src .

COPY --chmod=755 ./entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
