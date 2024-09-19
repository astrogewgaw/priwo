#ifndef DAT
#define DAT

#include <filesystem>

#include "common.h"
#include "inf.h"

void init_dat(nb::module_ m);
std::tuple<nb::dict, nb::ndarray<nb::numpy, float, nb::ndim<1>>>
readdat(std::string fn);
void writedat(nb::dict meta, nb::ndarray<nb::numpy, float, nb::ndim<1>> data,
              std::string fn);

#endif
