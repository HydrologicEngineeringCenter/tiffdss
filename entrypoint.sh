#!/bin/bash
# set -x

usage(){ printf "\n$0 usage:\n\n" && grep " .*)\ #" $0; exit 0;}

KEEP_ALIVE=false

# remove temp dss files if they exist
rm -f /tmp/*.dss

for opt in "$@";do

    case $opt in
        itest) # Integration testing using hec-dssvue.sh; verbosity defined in each script
            /hec-dssvue-linux/hec-dssvue.sh /tiffdss/tests/integration/test_dss_convert_tiff.py
            /hec-dssvue-linux/hec-dssvue.sh /tiffdss/tests/integration/test_dss_convert_version.py
            /hec-dssvue-linux/hec-dssvue.sh /tiffdss/tests/integration/test_dss_grid_info.py
            ;;
        utest) # Unit testing the tiffdss shared object
            python -m unittest discover -v -s /tiffdss/tests/unit/
            ;;
        build) # make tiffdss
            cd /tiffdss/src
            make
            cp ./output/libtiffdss.so /usr/lib
            ;;
        alive) # Keep the container alive
            KEEP_ALIVE=true
            ;;
        * | help) # Print this message
            usage
            exit 1
            ;;
    esac
done

# Keep container running
while :
do
    if [ "$KEEP_ALIVE" == "false" ]; then
        exit
    fi
    sleep 10000
done
