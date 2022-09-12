#!/bin/bash

IMAGE=tiff_dss
CONTAINER=tiff_dss

# build
printf "n\Building image: "
docker build -t $IMAGE .

# run
# - with arguments uses the entrypoint.sh
# - without arguments assumes interactive
if [ "$1" == "dev" ]; then
    printf "\nRunning the container interactively with a volume\n"
    docker run --rm -it --entrypoint /bin/bash -v $PWD/:/tiffdss/ --name $CONTAINER $IMAGE
else
    printf "\nRunning the container with arguments: $@\n"
    docker run --rm --name $CONTAINER $IMAGE "$@"
fi
