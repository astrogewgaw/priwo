#ifndef FIL
#define FIL

#include "common.h"

void init_fil(nb::module_ m);
std::tuple<nb::dict, nb::ndarray<nb::numpy, nb::ndim<2>>>
readfil(std::string fn);
void writefil(nb::dict meta, nb::ndarray<nb::numpy, float, nb::ndim<2>> data,
              std::string fn);

#endif
