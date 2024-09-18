#include "dat.h"

namespace fs = std::filesystem;
using namespace nanobind::literals;

std::tuple<nb::dict, nb::ndarray<nb::numpy, float, nb::ndim<1>>>
readdat(std::string fn) {
  nb::dict meta = readinf(fs::path(fn).replace_extension("inf"));
  nb::object np = nb::module_::import_("numpy");
  return std::make_tuple(
      meta, nb::cast<nb::ndarray<nb::numpy, float, nb::ndim<1>>>(
                np.attr("fromfile")(fn, "dtype"_a = np.attr("float32"))));
}

void writedat(nb::dict meta, nb::ndarray<nb::numpy, float, nb::ndim<1>> data,
              std::string fn) {
  writeinf(meta, fs::path(fn).replace_extension("inf"));
  nb::object np = nb::module_::import_("numpy");
  np.attr("asarray")(data).attr("tofile")(fn);
}

void init_dat(nb::module_ m) {
  m.def("readdat", &readdat);
  m.def("writedat", &writedat);
}
