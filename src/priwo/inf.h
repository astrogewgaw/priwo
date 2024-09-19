#ifndef INF
#define INF

#include "common.h"

void init_inf(nb::module_ m);
nb::dict readinf(std::string fn);
void writeinf(nb::dict inf, std::string fn);

#endif
