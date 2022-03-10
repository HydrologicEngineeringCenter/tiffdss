FROM osgeo/gdal:alpine-normal-3.4.1

RUN apk add gcc
RUN apk add g++


# These commands copy your files into the specified directory in the image
# and set that as the working location
COPY . /usr/src/myapp
WORKDIR /usr/src/myapp

# This command compiles your app using GCC, adjust for your source code
RUN g++ -o myapp main.cpp

# This command runs your application, comment out this line to compile only
CMD ["./myapp"]

LABEL Name=dss-docker Version=0.0.1
