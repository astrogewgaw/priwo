#include "nanobind/nanobind.h"
#include "priwo.h"

NB_MODULE(_internals, m) {
  init_hdr(m);
  init_pfd(m);
}
