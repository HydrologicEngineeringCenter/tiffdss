# Compile DSS
FROM osgeo/gdal:ubuntu-small-3.5.0

RUN apt-get -y update && \
    apt-get install -y make git gcc gfortran python3-pip zlib1g-dev libffi-dev && \
    rm -rf /var/lib/apt/lists/*

RUN git clone --branch 7-IP https://github.com/HydrologicEngineeringCenter/hec-dss.git
RUN git clone --depth 1 https://github.com/HydrologicEngineeringCenter/hec-dssvue-linux.git

WORKDIR /hec-dss/heclib/heclib_c
RUN make

WORKDIR /hec-dss/heclib/heclib_f
RUN make

ENV HECFLAG="/hec-dss/heclib/heclib_c/Output/libhec_c.a /hec-dss/heclib/heclib_f/Output/libhec_f.a"

RUN mkdir -p /tiffdss

COPY . /tiffdss/

WORKDIR /tiffdss/src
RUN make && \
    mv -f libtiffdss.so /usr/lib/

ENTRYPOINT [ "/tiffdss/entrypoint.sh" ]

RUN useradd appuser
USER appuser

# Check the entrypoint.sh for these options: "integration", "unit", and/or "run" for testing
CMD [ "" ]
