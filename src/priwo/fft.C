#include "fft.h"
#include "inf.h"

void readfft() {}
void writefft() {}

void init_fft(nb::module_ m) {
  m.def("readfft", &readfft);
  m.def("writefft", &writefft);
}
