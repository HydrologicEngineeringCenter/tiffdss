#!/bin/bash

IMAGE=tiff_dss
CONTAINER=tiff_dss

# build
printf "n\Building image: "
docker build -t $IMAGE .

# run
# - with arguments uses the entrypoint.sh
# - without arguments assumes interactive
printf "\nRunning the container with arguments: $@\n"
docker run --rm --name $CONTAINER $IMAGE "$@"
