#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <stdexcept>
#include <tuple>

#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/tuple.h>

namespace nb = nanobind;

char *rmlead(char *str);
char *rmtrail(char *str);
char *rmspace(char *str);

int swapint(int var);
short swapshort(short var);
float swapfloat(float var);
double swapdouble(double vari);
long long swaplonglong(long long var);
unsigned int swapuint(unsigned int var);
long double swaplongdouble(long double var);
unsigned short swapushort(unsigned short var);

int parseint(FILE *infile, int byteswap);
float parsefloat(FILE *infile, int byteswap);
double parsedouble(FILE *infile, int byteswap);

FILE *chkfopen(const char *path, const char *mode);
size_t chkfread(void *data, size_t type, size_t number, FILE *stream);
size_t chkfwrite(void *data, size_t type, size_t number, FILE *stream);
