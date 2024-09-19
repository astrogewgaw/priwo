#ifndef COMMON
#define COMMON

#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <stdexcept>
#include <sys/types.h>
#include <tuple>

#ifdef __linux__
#include <sys/mman.h>
#endif

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

template <typename T>
nb::ndarray<nb::numpy, T, nb::c_contig> EmptyArr1D(size_t N) {
  T *data = new T[N];

#ifdef __linux__
  // Use madvise with MADV_HUGEPAGE to optimize memory usage on Linux
  const size_t hugepage_threshold = 1u << 22u; // 4MB threshold
  const size_t page_size = 4096u;

  if (N * sizeof(T) >= hugepage_threshold) {
    uintptr_t data_addr = reinterpret_cast<uintptr_t>(data);
    size_t offset = page_size - (data_addr % page_size);
    size_t length = N * sizeof(T) - offset;

    // Intentionally not checking for errors, following NumPy's approach
    madvise(reinterpret_cast<void *>(data_addr + offset), length,
            MADV_HUGEPAGE);
  }
#endif

  size_t shape[1] = {N};

  // Create and return the ndarray with the given shape and ownership capsule
  nb::capsule owner(data, [](void *p) noexcept { delete[] (T *)p; });
  return nb::ndarray<nb::numpy, T, nb::c_contig>(data, 1, shape, owner);
}

template <typename T>
nb::ndarray<nb::numpy, T, nb::c_contig> EmptyArr2D(size_t N, size_t M) {
  int totalsize = N * M;
  T *data = new T[totalsize];

#ifdef __linux__
  // Use madvise with MADV_HUGEPAGE to optimize memory usage on Linux
  const size_t hugepage_threshold = 1u << 22u; // 4MB threshold
  const size_t page_size = 4096u;

  if (totalsize * sizeof(T) >= hugepage_threshold) {
    uintptr_t data_addr = reinterpret_cast<uintptr_t>(data);
    size_t offset = page_size - (data_addr % page_size);
    size_t length = totalsize * sizeof(T) - offset;

    // Intentionally not checking for errors, following NumPy's approach
    madvise(reinterpret_cast<void *>(data_addr + offset), length,
            MADV_HUGEPAGE);
  }
#endif

  size_t shape[2] = {N, M};

  // Create and return the ndarray with the given shape and ownership capsule
  nb::capsule owner(data, [](void *p) noexcept { delete[] (T *)p; });
  return nb::ndarray<nb::numpy, T, nb::c_contig>(data, 2, shape, owner);
}

#endif
