#include "common.h"
#include "nanobind/nanobind.h"
#include "polycos.h"

#include <cfloat>

#define TEST_EQUAL(a, b)                                                       \
  (fabs(a) == 0.0 ? (fabs((a) - (b)) <= 2 * DBL_EPSILON ? 1 : 0)               \
                  : (fabs((a) - (b)) / fabs((a)) <= 2 * DBL_EPSILON ? 1 : 0))

double _str2dbl(char *val) {
  double retval;

  char *endptr;
  char err[100];
  char *sptr = val;

  retval = strtod(sptr, &endptr);
  if (retval == 0.0 && endptr == val) {
    sprintf(err, "Cannot convert %s to double! Exiting...", val);
    throw std::runtime_error(err);
  }
  return retval;
}

int readpolyco(nb::dict polyco, FILE *f) {
  char PSR[11];
  char DATE[10];
  double UTC;
  double TMID;
  double DM;
  double DOPPLER;
  double LOG10RMS;
  double RPHASE;
  double F0;
  int OBSNUM;
  double DATASPAN;
  int NUMCOEFF;
  double OBSFREQ;
  double BINPHASE = 0.0;

  ssize_t read;
  size_t len = 0;
  char *line = NULL;

  read = getline(&line, &len, f);
  if (read == -1) return -1;
  sscanf(line, "%10s %9s %12lf %20lf %21lf %6lf %7lf", PSR, DATE, &UTC, &TMID,
         &DM, &DOPPLER, &LOG10RMS);

  polyco["PSR"] = PSR;
  polyco["DATE"] = DATE;
  polyco["UTC"] = UTC;
  polyco["TMID"] = TMID;
  polyco["DM"] = DM;
  polyco["DOPPLER"] = DOPPLER;
  polyco["LOG10RMS"] = LOG10RMS;

  read = getline(&line, &len, f);
  if (read == -1) return -1;
  sscanf(line, "%20lf %18lf %5d %6lf %5d %21lf %5lf", &RPHASE, &F0, &OBSNUM,
         &DATASPAN, &NUMCOEFF, &OBSFREQ, &BINPHASE);

  polyco["RPHASE"] = RPHASE;
  polyco["F0"] = F0;
  polyco["OBSNUM"] = OBSNUM;
  polyco["DATASPAN"] = DATASPAN;
  polyco["NUMCOEFF"] = NUMCOEFF;
  polyco["OBSFREQ"] = OBSFREQ;
  if (TEST_EQUAL(BINPHASE, 0.0))
    polyco["BINPHASE"] = nb::none();
  else
    polyco["BINPHASE"] = BINPHASE;

  char tmp1[30], tmp2[30], tmp3[30];
  double *COEFFS = (double *)calloc(NUMCOEFF, sizeof(double));

  for (int ii = 0; ii < (int)(NUMCOEFF / 3); ii++) {
    read = getline(&line, &len, f);
    if (read == -1) return -1;
    sscanf(line, "%s %s %s", tmp1, tmp2, tmp3);
    COEFFS[ii * 3 + 0] = _str2dbl(tmp1);
    COEFFS[ii * 3 + 1] = _str2dbl(tmp2);
    COEFFS[ii * 3 + 2] = _str2dbl(tmp3);
  }

  size_t shape[1] = {static_cast<size_t>(NUMCOEFF)};
  polyco["COEFFS"] = nb::ndarray<nb::numpy, double, nb::ndim<1>>(
      COEFFS, 1, shape, nb::handle());

  return 0;
}

nb::list readpolycos(std::string fn) {
  nb::list polycos;

  FILE *f = chkfopen(fn.c_str(), "r");

  int status = 0;
  while (status == 0) {
    nb::dict polyco;
    status = readpolyco(polyco, f);
    if (!(polyco.size() == 0)) polycos.append(polyco);
  }

  fclose(f);
  return polycos;
}

void writepolyco(nb::dict polyco, FILE *f) {
  const char *PSR = nb::cast<const char *>(polyco["PSR"]);
  const char *DATE = nb::cast<const char *>(polyco["DATE"]);
  double UTC = nb::cast<double>(polyco["UTC"]);
  double TMID = nb::cast<double>(polyco["TMID"]);
  double DM = nb::cast<double>(polyco["DM"]);
  double DOPPLER = nb::cast<double>(polyco["DOPPLER"]);

  fprintf(f, "%10s", PSR);
  fprintf(f, "%10s", DATE);
  fprintf(f, "%11lf", UTC);
  fprintf(f, "%20.11lf", TMID);
  fprintf(f, "%21.6lf", DM);
  fprintf(f, "%7.3lf", DOPPLER);

  if (!polyco["LOG10RMS"].is_none()) {
    double LOG10RMS = nb::cast<double>(polyco["LOG10RMS"]);
    fprintf(f, "%7.3lf", LOG10RMS);
  }
  fprintf(f, "\n");

  double RPHASE = nb::cast<double>(polyco["RPHASE"]);
  double F0 = nb::cast<double>(polyco["F0"]);
  int OBSNUM = nb::cast<int>(polyco["OBSNUM"]);
  double DATASPAN = nb::cast<double>(polyco["DATASPAN"]);
  int NUMCOEFF = nb::cast<int>(polyco["NUMCOEFF"]);
  double OBSFREQ = nb::cast<double>(polyco["OBSFREQ"]);

  fprintf(f, "%20.6lf", RPHASE);
  fprintf(f, "%20.12lf", F0);
  fprintf(f, "%5d", OBSNUM);
  fprintf(f, "%5.0lf", DATASPAN);
  fprintf(f, "%4d", NUMCOEFF);
  fprintf(f, "%21.3lf", OBSFREQ);

  if (!polyco["BINPHASE"].is_none()) {
    double BINPHASE = nb::cast<double>(polyco["BINPHASE"]);
    fprintf(f, "%4.0lf", BINPHASE);
  }
  fprintf(f, "\n");

  nb::ndarray<nb::numpy, double, nb::ndim<1>> COEFFS =
      nb::cast<nb::ndarray<nb::numpy, double, nb::ndim<1>>>(polyco["COEFFS"]);
  for (int ii = 0; ii < (int)(NUMCOEFF / 3); ii++) {
    fprintf(f, "%25.16E %25.16E %25.16E\n", COEFFS(ii * 3 + 0),
            COEFFS(ii * 3 + 1), COEFFS(ii * 3 + 2));
  }
}

void writepolycos(nb::list polycos, std::string fn) {
  FILE *f = chkfopen(fn.c_str(), "w");
  for (auto object : polycos) {
    nb::dict polyco = nb::cast<nb::dict>(object);
    writepolyco(polyco, f);
  }
  fclose(f);
}

void init_polycos(nb::module_ m) {
  m.def("readpolycos", &readpolycos);
  m.def("writepolycos", &writepolycos);
}
