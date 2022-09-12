CC = gcc
RM = rm -fr
CFLAGS = -m64 -c -fPIC -g -std=gnu99 -D__linux__
LDFLAGS = -lgdal -lgfortran -lm -lz
CWARNING = -Werror -Wno-unused-result

# resulting archive locations
HECFLAG = /hec-dss/heclib/heclib_c/Output/libhec_c.a /hec-dss/heclib/heclib_f/Output/libhec_f.a

# define header paths to search in
export CPATH := /hec-dss/heclib/heclib_c/src/headers

# make PHONY to run every time; not updated
.PHONY: hecdss clean

# this is first so only need to execute 'make'
all : tiffdss libtiffdss.so

# build the cli
tiffdss : tiffdss.o utils.o hecdss
	$(CC) tiffdss.o utils.o $(HECFLAG) $(HECFLAG) $(LDFLAGS) -o $@

# build the shared object
libtiffdss.so: tiffdss.o utils.o hecdss
	$(CC) tiffdss.o utils.o $(HECFLAG) $(HECFLAG) $(LDFLAGS) -shared -o $@

# enter the directory (-C) and then execute 'make' to build dependencies
hecdss:
	$(MAKE) -C /hec-dss/heclib/heclib_c
	$(MAKE) -C /hec-dss/heclib/heclib_f

%.o: %.c
	$(CC) $(CFLAGS) $(CWARNING) -o $@ -c $<

clean:
	$(RM) *.o
