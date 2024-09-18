#include "bestprof.h"
#include "common.h"
#include <string>

nb::tuple readbestprof(std::string fn) {
  nb::object _bpf = nb::module_::import_("priwo._bpf").attr("_bpf");
  nb::tuple output = nb::cast<nb::tuple>(_bpf(fn));
  return output;
}

void writebestprof(nb::dict meta,
                   nb::ndarray<nb::numpy, double, nb::ndim<1>> data,
                   std::string fn) {
  FILE *f = chkfopen(fn.c_str(), "w");

  const char *filenm = nb::cast<const char *>(meta["filenm"]);
  const char *candnm = nb::cast<const char *>(meta["candnm"]);
  const char *telescope = nb::cast<const char *>(meta["telescope"]);

  fprintf(f, "# Input file       =  %-s\n", filenm);
  fprintf(f, "# Candidate        =  %-s\n", candnm);
  fprintf(f, "# Telescope        =  %-s\n", telescope);

  double tepoch;
  if (meta["tepoch"].is_none()) {
    tepoch = 0.0;
    fprintf(f, "# Epoch_topo       =  N/A\n");
  } else {
    tepoch = nb::cast<double>(meta["tepoch"]);
    fprintf(f, "# Epoch_topo       =  %-.12f\n", tepoch);
  }

  double bepoch;
  if (meta["bepoch"].is_none()) {
    bepoch = 0.0;
    fprintf(f, "# Epoch_bary       =  N/A\n");
  } else {
    bepoch = nb::cast<double>(meta["bepoch"]);
    fprintf(f, "# Epoch_bary (MJD) =  %-.12f\n", bepoch);
  }

  double N = nb::cast<double>(meta["N"]);
  double dt = nb::cast<double>(meta["dt"]);
  int proflen = nb::cast<int>(meta["proflen"]);
  double data_avg = nb::cast<double>(meta["data_avg"]);
  double data_std = nb::cast<double>(meta["data_std"]);
  double prof_avg = nb::cast<double>(meta["prof_avg"]);
  double prof_std = nb::cast<double>(meta["prof_std"]);

  fprintf(f, "# T_sample         =  %.6g\n", dt);
  fprintf(f, "# Data Folded      =  %-.0f\n", N);
  fprintf(f, "# Data Avg         =  %-17.15g\n", data_avg);
  fprintf(f, "# Data StdDev      =  %-17.15g\n", data_std);
  fprintf(f, "# Profile Bins     =  %d\n", proflen);
  fprintf(f, "# Profile Avg      =  %-17.15g\n", prof_avg);
  fprintf(f, "# Profile StdDev   =  %-17.15g\n", prof_std);

  char tmp[80];

  double redchi = nb::cast<double>(meta["redchi"]);
  double chi_sig = nb::cast<double>(meta["chi_sig"]);

  sprintf(tmp, "(~%.1f sigma)", chi_sig);
  fprintf(f, "# Reduced chi-sqr  =  %.3f\n", redchi);
  fprintf(f, "# Prob(Noise)      <  %.3g   %s\n", 0.0, tmp);

  if (!meta["bestdm"].is_none()) {
    double bestdm = nb::cast<double>(meta["bestdm"]);
    fprintf(f, "# Best DM          =  %.3f\n", bestdm);
  }

  if (tepoch != 0.0) {
    double p_topo = nb::cast<double>(meta["topo"]["p"]);
    double pd_topo = nb::cast<double>(meta["topo"]["pd"]);
    double pdd_topo = nb::cast<double>(meta["topo"]["pdd"]);
    double p_topo_err = nb::cast<double>(meta["topo"]["p_err"]);
    double pd_topo_err = nb::cast<double>(meta["topo"]["pd_err"]);
    double pdd_topo_err = nb::cast<double>(meta["topo"]["pdd_err"]);

    fprintf(f, "# P_topo (ms)      =  %-17.15g +/- %-.3g\n", p_topo,
            p_topo_err);
    fprintf(f, "# P'_topo (s/s)    =  %-17.15g +/- %-.3g\n", pd_topo,
            pd_topo_err);
    fprintf(f, "# P''_topo (s/s^2) =  %-17.15g +/- %-.3g\n", pdd_topo,
            pdd_topo_err);
  } else {
    fprintf(f, "# P_topo (ms)      =  N/A\n");
    fprintf(f, "# P'_topo (s/s)    =  N/A\n");
    fprintf(f, "# P''_topo (s/s^2) =  N/A\n");
  }

  if (bepoch != 0.0) {
    double p_bary = nb::cast<double>(meta["bary"]["p"]);
    double pd_bary = nb::cast<double>(meta["bary"]["pd"]);
    double pdd_bary = nb::cast<double>(meta["bary"]["pdd"]);
    double p_bary_err = nb::cast<double>(meta["bary"]["p_err"]);
    double pd_bary_err = nb::cast<double>(meta["bary"]["pd_err"]);
    double pdd_bary_err = nb::cast<double>(meta["bary"]["pdd_err"]);

    fprintf(f, "# P_bary (ms)      =  %-17.15g +/- %-.3g\n", p_bary,
            p_bary_err);
    fprintf(f, "# P'_bary (s/s)    =  %-17.15g +/- %-.3g\n", pd_bary,
            pd_bary_err);
    fprintf(f, "# P''_bary (s/s^2) =  %-17.15g +/- %-.3g\n", pdd_bary,
            pdd_bary_err);
  } else {
    fprintf(f, "# P_bary (ms)      =  N/A\n");
    fprintf(f, "# P'_bary (s/s)    =  N/A\n");
    fprintf(f, "# P''_bary (s/s^2) =  N/A\n");
  }

  if (meta["orb"]["p"].is_none()) {
    fprintf(f, "# P_orb (s)        =  N/A\n");
    fprintf(f, "# asin(i)/c (s)    =  N/A\n");
    fprintf(f, "# eccentricity     =  N/A\n");
    fprintf(f, "# w (rad)          =  N/A\n");
    fprintf(f, "# T_peri           =  N/A\n");
  } else {
    double orb_p = nb::cast<double>(meta["orb"]["p"]);
    double orb_x = nb::cast<double>(meta["orb"]["x"]);
    double orb_e = nb::cast<double>(meta["orb"]["e"]);
    double orb_w = nb::cast<double>(meta["orb"]["w"]);
    double orb_t = nb::cast<double>(meta["orb"]["t"]);

    fprintf(f, "# P_orb (s)        =  %-17.15g\n", orb_p);
    fprintf(f, "# asin(i)/c (s)    =  %-17.15g\n", orb_x);
    fprintf(f, "# eccentricity     =  %-17.15g\n", orb_e);
    fprintf(f, "# w (deg)          =  %-17.15g\n", orb_w);
    fprintf(f, "# T_peri           =  %-.12f\n", orb_t);
  }

  fprintf(f, "######################################################\n");
  for (int ii = 0; ii < data.size(); ii++)
    fprintf(f, "%4d  %.7g\n", ii, data(ii));
  fclose(f);
}

void init_bestprof(nb::module_ m) {
  m.def("readbestprof", &readbestprof, nb::rv_policy::copy);
  m.def("writebestprof", &writebestprof);
}
