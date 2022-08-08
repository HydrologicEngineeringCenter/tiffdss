#!/bin/bash
# set -x

if [ "$1" == "test" ]; then
    /app/tiffdss/tests/dss-test.sh
fi

# Keep container running
while "$1" == "test"
do
    sleep 10000
done
