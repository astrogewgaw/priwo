#ifndef HDR
#define HDR

#include "common.h"

void init_hdr(nb::module_ m);
nb::dict readhdr(std::string fn);
void writehdr(nb::dict &dict, std::string fn);

#endif
