#!/bin/bash
# set -x

# do the compiling here
if "$2" == "true"
then
    # remove built objects
    rm -f ${SRC}/*.o

    # compile the heclib_c.a
    cd $HLIBSC
    make clean
    make

    # # compile the heclib_f.a
    cd $HLIBSF
    make clean
    make

    # compile tiff to dss
    cd $SRC

    gcc -c ${TIFFDSS}.c -I$HEADERSC -o ${TIFFDSS}.o
    gcc -shared -o lib${TIFFDSS}.so ${TIFFDSS}.o

    gcc $HLIBSC/Output/libhec_c.a $HLIBSF/Output/libhec_f.a ${SRC}/lib${TIFFDSS}.so -lgfortran -lm -lz -o ${TIFFDSS}
fi

# Keep container running
while $1
do
    sleep 10000
done
