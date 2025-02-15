#include "hdr.h"
#include "tim.h"

using namespace nanobind::literals;

std::tuple<nb::dict, nb::ndarray<nb::numpy, nb::ndim<1>>>
readtim(std::string fn) {
  nb::dict meta = readhdr(fn);
  int nbits = nb::cast<int>(meta["nbits"]);
  int nskip = nb::cast<int>(meta["hdrlen"]);

  const char *dtype;
  switch (nbits) {
  case 1:
    dtype = "uint8";
    break;
  case 2:
    dtype = "uint8";
    break;
  case 4:
    dtype = "uint8";
    break;
  case 8:
    dtype = "uint8";
    break;
  case 16:
    dtype = "uint16";
    break;
  case 32:
    dtype = "float32";
    break;
  }

  nb::object np = nb::module_::import_("numpy");
  nb::object dobj =
      np.attr("fromfile")(fn, "dtype"_a = np.attr(dtype), "offset"_a = nskip);
  if (nbits == 1 || nbits == 2 || nbits == 4) {
    nb::object priwo = nb::module_::import_("priwo");
    dobj = priwo.attr("_internals")
               .attr("unpack")(dobj, "nbits"_a = nbits, "bitorder"_a = "little",
                               "parallel"_a = true);
  }
  nb::ndarray<nb::numpy, nb::ndim<1>> data =
      nb::cast<nb::ndarray<nb::numpy, nb::ndim<1>>>(dobj);
  return std::make_tuple(meta, data);
}

void writetim(nb::dict meta, nb::ndarray<nb::numpy, float, nb::ndim<1>> data,
              std::string fn) {
  writehdr(meta, fn);
  nb::object np = nb::module_::import_("numpy");
  nb::object dobj = np.attr("asarray")(data);
  int nbits = nb::cast<int>(meta["nbits"]);
  if (nbits == 1 || nbits == 2 || nbits == 4) {
    nb::object priwo = nb::module_::import_("priwo");
    dobj = priwo.attr("_internals")
               .attr("pack")(dobj, "nbits"_a = nbits, "bitorder"_a = "little",
                             "parallel"_a = true);
  }
  dobj.attr("tofile")(fn);
}

void init_tim(nb::module_ m) {
  m.def("readtim", &readtim);
  m.def("writetim", &writetim);
}
