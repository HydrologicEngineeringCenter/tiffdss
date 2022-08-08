#!/usr/bin/bash

# add this dir to the stack
cd $(dirname $0)

# clean and build tiffdss
make clean
make tiffdss
make libtiffdss.so

mv -f /app/tiffdss/src/libtiffdss.so /usr/lib/
printf "libtiffdss.so moved to /usr/lib/\n"
