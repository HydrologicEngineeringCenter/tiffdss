#!/bin/bash

docker build -t dss_tiff . && \
    docker run --rm --name dss_tiff dss_tiff
    # docker run --rm -it -v $PWD/src:/app/tiffdss/src --name dss_tiff dss_tiff bash
