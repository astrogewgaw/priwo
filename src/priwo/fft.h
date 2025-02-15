#ifndef FFT
#define FFT

#include <filesystem>

#include "common.h"
#include "inf.h"

void init_fft(nb::module_ m);
std::tuple<nb::dict, nb::ndarray<nb::numpy, float, nb::ndim<1>>>
readfft(std::string fn);
void writefft(nb::dict meta, nb::ndarray<nb::numpy, float, nb::ndim<1>> data,
              std::string fn);

#endif
