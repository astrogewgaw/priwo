#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>

#include "priwo/base.h"
#include "priwo/sigproc/hdr.h"

namespace nb = nanobind;

NB_MODULE(core, m) {
  m.def("readhdr", [](std::string fn) {
    FILE* s = priwo::base::safefopen(fn.c_str(), "rb");
    priwo::sigproc::SIGPROCHeader H;
    priwo::sigproc::readhdr(s, &H);

    nb::dict hdr;
    hdr["rawfile"] = H.rawfile;
    hdr["source"] = H.source;
    hdr["azimuth"] = H.azimuth;
    hdr["zenith"] = H.zenith;
    hdr["raj"] = H.raj;
    hdr["decj"] = H.decj;
    hdr["mjd"] = H.mjd;
    hdr["dt"] = H.dt;
    hdr["f0"] = H.f0;
    hdr["df"] = H.df;
    hdr["refdm"] = H.refdm;
    hdr["nf"] = H.nf;
    hdr["macid"] = H.macid;
    hdr["machine"] = H.machine;
    hdr["telid"] = H.telid;
    hdr["telescope"] = H.telescope;
    hdr["datatype"] = H.datatype;
    hdr["nbits"] = H.nbits;
    hdr["nt"] = H.nt;
    hdr["nifs"] = H.nifs;
    hdr["nbeams"] = H.nbeams;
    hdr["ibeam"] = H.ibeam;
    hdr["sumifs"] = H.sumifs;
    hdr["signedints"] = H.signedints;
    hdr["barycentric"] = H.barycentric;
    hdr["pulsarcentric"] = H.pulsarcentric;
    return hdr;
  });
}
