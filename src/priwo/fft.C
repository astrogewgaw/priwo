#include "fft.h"

namespace fs = std::filesystem;
using namespace nanobind::literals;

std::tuple<nb::dict, nb::ndarray<nb::numpy, float, nb::ndim<1>>>
readfft(std::string fn) {
  nb::dict meta = readinf(fs::path(fn).replace_extension("inf"));
  nb::object np = nb::module_::import_("numpy");
  return std::make_tuple(
      meta, nb::cast<nb::ndarray<nb::numpy, float, nb::ndim<1>>>(
                np.attr("fromfile")(fn, "dtype"_a = np.attr("complex64"))));
}

void writefft(nb::dict meta, nb::ndarray<nb::numpy, float, nb::ndim<1>> data,
              std::string fn) {
  writeinf(meta, fs::path(fn).replace_extension("inf"));
  nb::object np = nb::module_::import_("numpy");
  np.attr("asarray")(data).attr("tofile")(fn);
}

void init_fft(nb::module_ m) {
  m.def("readfft", &readfft);
  m.def("writefft", &writefft);
}
