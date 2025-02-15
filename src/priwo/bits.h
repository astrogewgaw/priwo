#ifndef BITS
#define BITS

#include "common.h"

void init_bits(nb::module_ m);

nb::ndarray<nb::numpy, uint8_t, nb::c_contig>
unpack(const nb::ndarray<nb::numpy, uint8_t, nb::c_contig> &x, size_t nbits,
       const std::string &bitorder, bool parallel);

nb::ndarray<nb::numpy, uint8_t, nb::c_contig>
pack(const nb::ndarray<nb::numpy, uint8_t, nb::c_contig> &x, size_t nbits,
     const std::string &bitorder, bool parallel);

#endif
