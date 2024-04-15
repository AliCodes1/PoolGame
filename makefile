CC=clang
CFLAGS=-std=c99 -Wall -pedantic -fpic
SWIG=swig
PYTHON_INCLUDE_PATH=/usr/include/python3.11
PYTHON_LIB_PATH=/usr/lib/python3.11
PYTHON_LIB=python3.11

all: libphylib.so _phylib.so

# Compile phylib.c to position-independent code
phylib.o: phylib.c
	$(CC) $(CFLAGS) -c phylib.c -o phylib.o

# Create shared library from phylib.o
libphylib.so: phylib.o
	$(CC) -shared phylib.o -o libphylib.so

# Generate Python interface files using SWIG
phylib_wrap.c phylib.py: phylib.i
	$(SWIG) -python phylib.i

# Compile Python interface to position-independent object code
phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -I$(PYTHON_INCLUDE_PATH) -o phylib_wrap.o

# Create shared library for Python interface
_phylib.so: phylib_wrap.o
	$(CC) -shared phylib_wrap.o -L. -L$(PYTHON_LIB_PATH) -l$(PYTHON_LIB) -lphylib -o _phylib.so

clean:
	rm -f *.o *.so *.svg phylib_wrap.c phylib.py
