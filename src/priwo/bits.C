#include <array>
#include <cstddef>
#include <cstdint>

#ifdef USE_OPENMP
#include <omp.h>
#endif

#include "bits.h"
#include "common.h"

#define LO2BITS 3
#define LO4BITS 15
#define HI2BITS 192
#define HI4BITS 240
#define LOMED2BITS 12
#define UPMED2BITS 48

template <bool parallel, bool bigEndian>
void unpack_1bit(const uint8_t *inbuffer, uint8_t *outbuffer, size_t nbytes) {
#ifdef USE_OPENMP
#pragma omp parallel for if (parallel)
#endif
  for (size_t ii = 0; ii < nbytes; ii++) {
    for (size_t jj = 0; jj < 8; jj++) {
      if constexpr (bigEndian) {
        outbuffer[(ii << 3) + (7 - jj)] = (inbuffer[ii] >> jj) & 1;
      } else {
        outbuffer[(ii << 3) + jj] = (inbuffer[ii] >> jj) & 1;
      }
    }
  }
}

template <bool parallel, bool bigEndian>
void unpack_2bit(const uint8_t *inbuffer, uint8_t *outbuffer, size_t nbytes) {
#ifdef USE_OPENMP
#pragma omp parallel for if (parallel)
#endif
  for (size_t ii = 0; ii < nbytes; ii++) {
    if constexpr (bigEndian) {
      outbuffer[(ii << 2) + 3] = inbuffer[ii] & LO2BITS;
      outbuffer[(ii << 2) + 2] = (inbuffer[ii] & LOMED2BITS) >> 2;
      outbuffer[(ii << 2) + 1] = (inbuffer[ii] & UPMED2BITS) >> 4;
      outbuffer[(ii << 2) + 0] = (inbuffer[ii] & HI2BITS) >> 6;
    } else {
      outbuffer[(ii << 2) + 0] = inbuffer[ii] & LO2BITS;
      outbuffer[(ii << 2) + 1] = (inbuffer[ii] & LOMED2BITS) >> 2;
      outbuffer[(ii << 2) + 2] = (inbuffer[ii] & UPMED2BITS) >> 4;
      outbuffer[(ii << 2) + 3] = (inbuffer[ii] & HI2BITS) >> 6;
    }
  }
}

template <bool parallel, bool bigEndian>
void unpack_4bit(const uint8_t *inbuffer, uint8_t *outbuffer, size_t nbytes) {
#ifdef USE_OPENMP
#pragma omp parallel for if (parallel)
#endif
  for (size_t ii = 0; ii < nbytes; ii++) {
    if constexpr (bigEndian) {
      outbuffer[(ii << 1) + 1] = inbuffer[ii] & LO4BITS;
      outbuffer[(ii << 1) + 0] = (inbuffer[ii] & HI4BITS) >> 4;
    } else {
      outbuffer[(ii << 1) + 0] = inbuffer[ii] & LO4BITS;
      outbuffer[(ii << 1) + 1] = (inbuffer[ii] & HI4BITS) >> 4;
    }
  }
}

template <bool parallel, bool bigEndian>
void pack_1bit(const uint8_t *inbuffer, uint8_t *outbuffer, size_t nbytes) {
  size_t pos;
#ifdef USE_OPENMP
#pragma omp parallel for if (parallel)
#endif
  for (size_t ii = 0; ii < nbytes / 8; ii++) {
    pos = ii * 8;
    if constexpr (bigEndian) {
      outbuffer[ii] = (inbuffer[pos + 0] << 7) | (inbuffer[pos + 1] << 6) |
                      (inbuffer[pos + 2] << 5) | (inbuffer[pos + 3] << 4) |
                      (inbuffer[pos + 4] << 3) | (inbuffer[pos + 5] << 2) |
                      (inbuffer[pos + 6] << 1) | inbuffer[pos + 7];
    } else {
      outbuffer[ii] = inbuffer[pos + 0] | (inbuffer[pos + 1] << 1) |
                      (inbuffer[pos + 2] << 2) | (inbuffer[pos + 3] << 3) |
                      (inbuffer[pos + 4] << 4) | (inbuffer[pos + 5] << 5) |
                      (inbuffer[pos + 6] << 6) | (inbuffer[pos + 7] << 7);
    }
  }
}

template <bool parallel, bool bigEndian>
void pack_2bit(const uint8_t *inbuffer, uint8_t *outbuffer, size_t nbytes) {
  size_t pos;
#ifdef USE_OPENMP
#pragma omp parallel for if (parallel)
#endif
  for (size_t ii = 0; ii < nbytes / 4; ii++) {
    pos = ii * 4;
    if constexpr (bigEndian) {
      outbuffer[ii] = (inbuffer[pos + 0] << 6) | (inbuffer[pos + 1] << 4) |
                      (inbuffer[pos + 2] << 2) | inbuffer[pos + 3];
    } else {
      outbuffer[ii] = inbuffer[pos + 0] | (inbuffer[pos + 1] << 2) |
                      (inbuffer[pos + 2] << 4) | (inbuffer[pos + 3] << 6);
    }
  }
}

template <bool parallel, bool bigEndian>
void pack_4bit(const uint8_t *inbuffer, uint8_t *outbuffer, size_t nbytes) {
  size_t pos;
#ifdef USE_OPENMP
#pragma omp parallel for if (parallel)
#endif
  for (size_t ii = 0; ii < nbytes / 2; ii++) {
    pos = ii * 2;
    if constexpr (bigEndian) {
      outbuffer[ii] = (inbuffer[pos] << 4) | inbuffer[pos + 1];
    } else {
      outbuffer[ii] = inbuffer[pos] | (inbuffer[pos + 1] << 4);
    }
  }
}

using PackUnpackFunc = void (*)(const uint8_t *, uint8_t *, size_t);

constexpr std::array<std::array<std::array<PackUnpackFunc, 2>, 2>, 3>
    unpackDispatcher = {
        {{{
             {unpack_1bit<false, false>, unpack_1bit<true, false>}, // little
             {unpack_1bit<false, true>, unpack_1bit<true, true>}    // big
         }},
         {{
             {unpack_2bit<false, false>, unpack_2bit<true, false>}, // little
             {unpack_2bit<false, true>, unpack_2bit<true, true>}    // big
         }},
         {{
             {unpack_4bit<false, false>, unpack_4bit<true, false>}, // little
             {unpack_4bit<false, true>, unpack_4bit<true, true>}    // big
         }}}};

constexpr std::array<std::array<std::array<PackUnpackFunc, 2>, 2>, 3>
    packDispatcher = {
        {{{
             {pack_1bit<false, false>, pack_1bit<true, false>}, // little
             {pack_1bit<false, true>, pack_1bit<true, true>}    // big
         }},
         {{
             {pack_2bit<false, false>, pack_2bit<true, false>}, // little
             {pack_2bit<false, true>, pack_2bit<true, true>}    // big
         }},
         {{
             {pack_4bit<false, false>, pack_4bit<true, false>}, // little
             {pack_4bit<false, true>, pack_4bit<true, true>}    // big
         }}}};

size_t get_bitorder_index(const std::string &bitorder) {
  if (bitorder.empty() || (bitorder[0] != 'l' && bitorder[0] != 'b')) {
    throw std::invalid_argument(
        "Invalid bitorder. Must begin with 'l' or 'b'.");
  }
  return (bitorder[0] == 'b') ? 1 : 0;
}

nb::ndarray<nb::numpy, uint8_t, nb::c_contig>
unpack(const nb::ndarray<nb::numpy, uint8_t, nb::c_contig> &x, size_t nbits,
       const std::string &bitorder, bool parallel = false) {
  if (nbits != 1 && nbits != 2 && nbits != 4) {
    throw std::invalid_argument(
        "Invalid number of bits. Supported values are 1, 2, and 4.");
  }
  size_t bitorder_idx = get_bitorder_index(bitorder);
  size_t nbits_idx = nbits >> 1;
  size_t nbytes = x.size();
  auto y = EmptyArr1D<uint8_t>(nbytes * 8 / nbits);

  PackUnpackFunc unpackFunc =
      unpackDispatcher[nbits_idx][bitorder_idx][parallel ? 1 : 0];
  unpackFunc(x.data(), y.data(), nbytes);
  return y;
}

nb::ndarray<nb::numpy, uint8_t, nb::c_contig>
pack(const nb::ndarray<nb::numpy, uint8_t, nb::c_contig> &x, size_t nbits,
     const std::string &bitorder, bool parallel = false) {
  if (nbits != 1 && nbits != 2 && nbits != 4) {
    throw std::invalid_argument(
        "Invalid number of bits. Supported values are 1, 2, and 4.");
  }
  size_t bitorder_idx = get_bitorder_index(bitorder);
  size_t nbits_idx = nbits >> 1;
  size_t nbytes = x.size();
  auto y = EmptyArr1D<uint8_t>(nbytes * nbits / 8);

  PackUnpackFunc packFunc =
      packDispatcher[nbits_idx][bitorder_idx][parallel ? 1 : 0];
  packFunc(x.data(), y.data(), nbytes);
  return y;
}

void init_bits(nb::module_ m) {
  m.def("unpack", &unpack,
        "Unpack 1, 2 and 4-bit data from an 8-bit numpy array", nb::arg("x"),
        nb::arg("nbits"), nb::arg("bitorder") = "big",
        nb::arg("parallel") = false);
  m.def("pack", &pack, "Pack 1, 2 and 4-bit data into an 8-bit numpy array",
        nb::arg("x"), nb::arg("nbits"), nb::arg("bitorder") = "big",
        nb::arg("parallel") = false);
}
