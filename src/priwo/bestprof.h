#ifndef BESTPROF
#define BESTPROF

#include "common.h"

void init_bestprof(nb::module_ m);
nb::tuple readbestprof(std::string fn);
void writebestprof(nb::dict meta,
                   nb::ndarray<nb::numpy, double, nb::ndim<1>> data,
                   std::string fn);

#endif
