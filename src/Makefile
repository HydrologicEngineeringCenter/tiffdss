CC = gcc
RM = rm -fr
CFLAGS = -m64 -c -fPIC -g -std=gnu99 -D__linux__
LDFLAGS = -lgdal -lgfortran -lm -lz
CWARNING = -Werror -Wno-unused-result

BUILD_DIR := ./output

# resulting archive locations
HECFLAG = /hec-dss/heclib/heclib_c/Output/libhec_c.a /hec-dss/heclib/heclib_f/Output/libhec_f.a

# define header paths to search in
export CPATH := /hec-dss/heclib/heclib_c/src/headers

OBJS = $(addprefix $(BUILD_DIR)/, tiffdss.o utils.o)

# make PHONY to run every time; not updated
.PHONY: clean

# this is first so only need to execute 'make'
build : tiffdss libtiffdss.so

# build the cli
tiffdss : hecdss $(OBJS)
	$(CC) $(filter-out $<, $^) $(HECFLAG) $(HECFLAG) $(LDFLAGS) -o $(BUILD_DIR)/$@

# build the shared object
libtiffdss.so: hecdss $(OBJS)
	$(CC) $(filter-out $<, $^) $(HECFLAG) $(HECFLAG) $(LDFLAGS) -shared -o $(BUILD_DIR)/$@

# enter the directory (-C) and then execute 'make' to build dependencies
hecdss:
	$(MAKE) -C /hec-dss/heclib/heclib_c
	$(MAKE) -C /hec-dss/heclib/heclib_f

$(BUILD_DIR)/%.o: %.c
	@mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(CWARNING) -o $@ -c $<

clean:
	$(RM) *.o
	$(RM) $(BUILD_DIR)
