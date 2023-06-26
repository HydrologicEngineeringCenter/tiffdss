# Compile DSS
FROM ghcr.io/osgeo/gdal:ubuntu-full-3.7.0

ENV HECDSS_VERSION=7-IQ-10
ENV DSSVUE_VERSION=main

RUN apt-get -y update && \
    apt-get install -y make git gcc gfortran python3-pip zlib1g-dev libffi-dev && \
    rm -rf /var/lib/apt/lists/*

RUN git clone --branch ${HECDSS_VERSION} https://github.com/HydrologicEngineeringCenter/hec-dss.git
RUN git clone --branch ${DSSVUE_VERSION} https://github.com/HydrologicEngineeringCenter/hec-dssvue-linux.git

RUN mkdir -p /tiffdss

COPY . /tiffdss/

WORKDIR /tiffdss

ENTRYPOINT [ "./entrypoint.sh" ]

# Check the entrypoint.sh for these options:
#   itest - integration testing
#   utest - unit testing
#   build - build tiffdss and dependencies (default)
#   alive - keep the container alive

CMD [ "build" ]
