#!/bin/bash
# set -x

KEEP_RUNNING=false

# remove temp dss files if they exist
rm -f /tmp/*.dss

for opt in "$@";do
    printf "Option: $opt\n"

    if [ "$opt" == "integration" ]; then
        /hec-dssvue-linux/hec-dssvue.sh /app/tiffdss/tests/integration/test_dss_convert_tiff.py
        /hec-dssvue-linux/hec-dssvue.sh /app/tiffdss/tests/integration/test_dss_convert_version.py
        /hec-dssvue-linux/hec-dssvue.sh /app/tiffdss/tests/integration/test_dss_grid_info.py
    fi

    if [ "$opt" == "unit" ]; then
        python /app/tiffdss/tests/unit/test_libtiffdss_stats.py
    fi

    if [ "$opt" == "run" ]; then
        KEEP_RUNNING=true
    fi
done

# Keep container running
while :
do
    if [ "$KEEP_RUNNING" == "false" ]; then
        exit
    fi
    sleep 10000
done

