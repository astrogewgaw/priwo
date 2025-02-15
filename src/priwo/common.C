#include "common.h"

#ifndef SWAP
#define SWAP(a, b)                                                             \
  tmpswap = (a);                                                               \
  (a) = (b);                                                                   \
  (b) = tmpswap;
#endif

static unsigned char tmpswap;

char *rmtrail(char *str) {
  int i;
  if (str && 0 != (i = strlen(str))) {
    while (--i >= 0) {
      if (!isspace(str[i])) break;
    }
    str[++i] = '\0';
  }
  return str;
}

char *rmlead(char *str) {
  char *obuf;
  if (str) {
    for (obuf = str; *obuf && isspace(*obuf); ++obuf);
    if (str != obuf) memmove(str, obuf, strlen(obuf) + 1);
  }
  return str;
}

char *rmspace(char *str) { return rmlead(rmtrail(str)); }

int swapint(int var) {
  unsigned char *buffer;
  int *iptr;

  buffer = (unsigned char *)(&var);
  SWAP(buffer[0], buffer[3]);
  SWAP(buffer[1], buffer[2]);
  iptr = (int *)buffer;
  return *iptr;
}

unsigned int swapuint(unsigned int var) {
  unsigned char *buffer;
  unsigned int *iptr;

  buffer = (unsigned char *)(&var);
  SWAP(buffer[0], buffer[3]);
  SWAP(buffer[1], buffer[2]);
  iptr = (unsigned int *)buffer;
  return *iptr;
}

short swapshort(short var) {
  unsigned char *buffer;
  short *sptr;

  buffer = (unsigned char *)(&var);
  SWAP(buffer[0], buffer[1]);
  sptr = (short *)buffer;
  return *sptr;
}

unsigned short swapushort(unsigned short var) {
  unsigned char *buffer;
  unsigned short *sptr;

  buffer = (unsigned char *)(&var);
  SWAP(buffer[0], buffer[1]);
  sptr = (unsigned short *)buffer;
  return *sptr;
}

float swapfloat(float var) {
  unsigned char *buffer;
  float *fptr;

  buffer = (unsigned char *)(&var);
  SWAP(buffer[0], buffer[3]);
  SWAP(buffer[1], buffer[2]);
  fptr = (float *)buffer;
  return *fptr;
}

double swapdouble(double var) {
  unsigned char *buffer;
  double *dptr;
  buffer = (unsigned char *)(&var);
  SWAP(buffer[0], buffer[7]);
  SWAP(buffer[1], buffer[6]);
  SWAP(buffer[2], buffer[5]);
  SWAP(buffer[3], buffer[4]);
  dptr = (double *)buffer;
  return *dptr;
}

long long swaplonglong(long long var) {
  unsigned char *buffer;
  long long *llptr;

  buffer = (unsigned char *)(&var);
  SWAP(buffer[0], buffer[7]);
  SWAP(buffer[1], buffer[6]);
  SWAP(buffer[2], buffer[5]);
  SWAP(buffer[3], buffer[4]);
  llptr = (long long *)buffer;
  return *llptr;
}

long double swaplongdouble(long double var) {
  unsigned char *buffer;
  long double *ldptr;

  buffer = (unsigned char *)(&var);
  SWAP(buffer[0], buffer[11]);
  SWAP(buffer[1], buffer[10]);
  SWAP(buffer[2], buffer[9]);
  SWAP(buffer[3], buffer[8]);
  SWAP(buffer[4], buffer[7]);
  SWAP(buffer[5], buffer[6]);
  ldptr = (long double *)buffer;
  return *ldptr;
}

int parseint(FILE *infile, int byteswap) {
  int itmp;
  chkfread(&itmp, sizeof(int), 1, infile);
  if (byteswap) itmp = swapint(itmp);
  return itmp;
}

float parsefloat(FILE *infile, int byteswap) {
  float ftmp;
  chkfread(&ftmp, sizeof(float), 1, infile);
  if (byteswap) ftmp = swapfloat(ftmp);
  return ftmp;
}

double parsedouble(FILE *infile, int byteswap) {
  double dtmp;
  chkfread(&dtmp, sizeof(double), 1, infile);
  if (byteswap) dtmp = swapdouble(dtmp);
  return dtmp;
}

FILE *chkfopen(const char *path, const char *mode) {
  FILE *file;
  if ((file = fopen(path, mode)) == NULL)
    throw std::runtime_error("Cannot open file! Exiting...");
  return (file);
}

size_t chkfread(void *data, size_t type, size_t number, FILE *stream) {
  size_t num;
  num = fread(data, type, number, stream);
  if (num != number && ferror(stream))
    throw std::runtime_error("Cannot read from file! Exiting...");
  return num;
}

size_t chkfwrite(void *data, size_t type, size_t number, FILE *stream) {
  size_t num;
  num = fwrite(data, type, number, stream);
  if (num != number && ferror(stream))
    throw std::runtime_error("Cannot write to file! Exiting...");
  return num;
}
