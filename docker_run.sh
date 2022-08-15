#!/bin/bash

IMAGE=dss_tiff
CONTAINER=dss_tiff

# build
docker build -t dss_tiff .

# run
# - with arguments uses the entrypoint.sh
# - without arguments assumes interactive
if [ "$#" -eq 0 ]; then
    docker run --rm -it  --entrypoint /bin/bash -v $PWD/:/app/tiffdss/ --name $CONTAINER $IMAGE
else
    docker run --rm --name $CONTAINER $IMAGE "$@"
fi
