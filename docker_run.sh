#!/bin/bash

usage(){ printf "\n$0 usage:\n\n" && grep " .*)\ #" $0; exit 0;}

for opt in "$@";do

    case $opt in
        itest) # Integration testing using hec-dssvue.sh; verbosity defined in each script
            echo $opt;;
        utest) # Unit testing the tiffdss shared object
            echo $opt;;
        build) # make tiffdss
            echo $opt;;
        alive) # Keep the container alive
            echo $opt;;
        * | help) # Print this message
            usage
            exit 1
            ;;
    esac
done

IMAGE=tiff_dss
CONTAINER=tiff_dss

# build
printf "n\Building image: "
docker build -t $IMAGE .

# run
# - with arguments uses the entrypoint.sh
# - without arguments assumes interactive
printf "\nRunning the container with arguments: $@\n"
docker run --rm -v /Users/rdcrljsg/projects/tiffdss/tests/integration:/tiffdss/tests/integration:rw --name $CONTAINER $IMAGE "$@"
