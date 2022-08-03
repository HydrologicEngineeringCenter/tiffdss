#!/bin/bash

# integration tests
if [ "$1" == "integration" ]; then
    /hec-dssvue-linux/hec-dssvue.sh /app/tiffdss/tests/integration/test_dss_convert_tiff.py
    /hec-dssvue-linux/hec-dssvue.sh /app/tiffdss/tests/integration/test_dss_convert_version.py
    /hec-dssvue-linux/hec-dssvue.sh /app/tiffdss/tests/integration/test_dss_grid_info.py
fi

# unit tests
if [ "$1" == "unit" ]; then
    python /app/tiffdss/tests/unit/test_libtiffdss_stats.py
fi
