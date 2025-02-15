#include <nanobind/nanobind.h>

#include "priwo.h"

NB_MODULE(_internals, m) {
  init_bits(m);
  init_hdr(m);
  init_tim(m);
  init_fil(m);
  init_inf(m);
  init_dat(m);
  init_pfd(m);
  init_fft(m);
  init_polycos(m);
  init_bestprof(m);
}
