#!/bin/bash

docker build -t dss_tiff . && \
docker run -d --rm -v $(PWD)/:/app --name dss_tiff dss_tiff
