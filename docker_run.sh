#!/bin/bash

IMAGE=dss_tiff
CONTAINER=dss_tiff

# build
printf "n\Building image: "
docker build -t $IMAGE .

# run
# - with arguments uses the entrypoint.sh
# - without arguments assumes interactive
if [ "$#" -eq 0 ]; then
    printf "\nRunning the container interactively with a volume\n"
    docker run --rm -it --entrypoint /bin/bash -v $PWD/:/app/tiffdss/ --name $CONTAINER $IMAGE
else
    printf "\nRunning the container with arguments: $@\n"
    docker run --rm --name $CONTAINER $IMAGE "$@"
fi
