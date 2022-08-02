#!/bin/bash

docker build -t dss_tiff . && \
    docker run --rm --name dss_tiff dss_tiff
    # docker run --rm -it -v $PWD/:/app --name dss_tiff dss_tiff bash
