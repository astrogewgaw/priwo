#ifndef COMMON
#define COMMON

#include <cstdio>
#include <cstdlib>
#include <exception>

class EOFError : public std::exception {
  virtual const char *what() const throw() { return "Reached EOF! Exiting..."; }
};

class CannotOpenFileError : public std::exception {
  virtual const char *what() const throw() {
    return "Cannot open file! Exiting...";
  }
};

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

#endif
