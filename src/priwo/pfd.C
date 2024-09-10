#include <cstddef>
#include <cstring>

#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <nanobind/stl/string.h>

#include "common.h"
#include "priwo.h"

namespace nb = nanobind;

nb::dict readpfd(std::string fn) {
  nb::dict pfd;
  nb::dict orb;
  nb::dict topo;
  nb::dict bary;
  nb::dict fold;
  nb::dict stats;

  char temp[16];
  int tmp, byteswap = 0;
  FILE *f = chkfopen(fn.c_str(), "rb");

  int numdms = parseint(f, byteswap);
  int numperiods = parseint(f, byteswap);
  int numpdots = parseint(f, byteswap);
  int nsub = parseint(f, byteswap);
  int npart = parseint(f, byteswap);

  if (npart < 1 || npart > 10000) {
    byteswap = 1;

    nsub = swapint(nsub);
    npart = swapint(npart);
    numdms = swapint(numdms);
    numpdots = swapint(numpdots);
    numperiods = swapint(numperiods);
  }

  int proflen = parseint(f, byteswap);
  int numchan = parseint(f, byteswap);
  int pstep = parseint(f, byteswap);
  int pdstep = parseint(f, byteswap);
  int dmstep = parseint(f, byteswap);
  int ndmfact = parseint(f, byteswap);
  int npfact = parseint(f, byteswap);

  tmp = parseint(f, byteswap);
  char *filenm = (char *)calloc(tmp + 1, sizeof(char));
  chkfread(filenm, sizeof(char), tmp, f);

  tmp = parseint(f, byteswap);
  char *candnm = (char *)calloc(tmp + 1, sizeof(char));
  chkfread(candnm, sizeof(char), tmp, f);

  tmp = parseint(f, byteswap);
  char *telescope = (char *)calloc(tmp + 1, sizeof(char));
  chkfread(telescope, sizeof(char), tmp, f);

  tmp = parseint(f, byteswap);
  char *pgdev = (char *)calloc(tmp + 1, sizeof(char));
  chkfread(pgdev, sizeof(char), tmp, f);

  double dt, startT;
  char *rastr = (char *)calloc(16, sizeof(char));
  char *decstr = (char *)calloc(16, sizeof(char));
  {
    int ii, haspos = 1;
    chkfread(temp, sizeof(char), 16, f);
    for (ii = 0; ii < 16; ii++) {
      if (!isdigit(temp[ii]) && temp[ii] != ':' && temp[ii] != '.' &&
          temp[ii] != '-' && temp[ii] != '\0') {
        haspos = 0;
        break;
      }
    }
    if (haspos) {
      strcpy(rastr, temp);
      chkfread(decstr, sizeof(char), 16, f);
      dt = parsedouble(f, byteswap);
      startT = parsedouble(f, byteswap);
    } else {
      strcpy(rastr, "Unknown");
      strcpy(decstr, "Unknown");
      dt = *(double *)(temp + 0);
      if (byteswap) dt = swapdouble(dt);
      startT = *(double *)(temp + sizeof(double));
      if (byteswap) startT = swapdouble(startT);
    }
  }

  double endT = parsedouble(f, byteswap);
  double tepoch = parsedouble(f, byteswap);
  double bepoch = parsedouble(f, byteswap);
  double avgvoverc = parsedouble(f, byteswap);
  double lofreq = parsedouble(f, byteswap);
  double chan_wid = parsedouble(f, byteswap);
  double bestdm = parsedouble(f, byteswap);

  float topopow = parsefloat(f, byteswap);
  parsefloat(f, byteswap);
  double topop1 = parsedouble(f, byteswap);
  double topop2 = parsedouble(f, byteswap);
  double topop3 = parsedouble(f, byteswap);

  float barypow = parsefloat(f, byteswap);
  parsefloat(f, byteswap);
  double baryp1 = parsedouble(f, byteswap);
  double baryp2 = parsedouble(f, byteswap);
  double baryp3 = parsedouble(f, byteswap);

  float foldpow = parsefloat(f, byteswap);
  parsefloat(f, byteswap);
  double foldp1 = parsedouble(f, byteswap);
  double foldp2 = parsedouble(f, byteswap);
  double foldp3 = parsedouble(f, byteswap);

  double orbp = parsedouble(f, byteswap);
  double orbe = parsedouble(f, byteswap);
  double orbx = parsedouble(f, byteswap);
  double orbw = parsedouble(f, byteswap);
  double orbt = parsedouble(f, byteswap);
  double orbpd = parsedouble(f, byteswap);
  double orbwd = parsedouble(f, byteswap);

  double *dms = (double *)calloc(numdms, sizeof(double));
  chkfread(dms, sizeof(double), numdms, f);

  double *periods = (double *)calloc(numperiods, sizeof(double));
  chkfread(periods, sizeof(double), numperiods, f);

  double *pdots = (double *)calloc(numpdots, sizeof(double));
  chkfread(pdots, sizeof(double), numpdots, f);

  double *rawfolds = (double *)calloc(nsub * npart * proflen, sizeof(double));
  chkfread(rawfolds, sizeof(double), nsub * npart * proflen, f);

  double *foldstats = (double *)calloc(nsub * npart * 7, sizeof(double));
  chkfread(foldstats, sizeof(double), nsub * npart * 7, f);

  if (byteswap) {
    int ii;

    for (ii = 0; ii < numdms; ii++) dms[ii] = swapdouble(dms[ii]);
    for (ii = 0; ii < numpdots; ii++) pdots[ii] = swapdouble(pdots[ii]);
    for (ii = 0; ii < numperiods; ii++) periods[ii] = swapdouble(periods[ii]);

    for (ii = 0; ii < nsub * npart * proflen; ii++)
      rawfolds[ii] = swapdouble(rawfolds[ii]);

    for (ii = 0; ii < nsub * npart * 7; ii++) {
      foldstats[ii] = swapdouble(foldstats[ii]);
    }
  }

  pfd["numdms"] = numdms;
  pfd["numperiods"] = numperiods;
  pfd["numpdots"] = numpdots;
  pfd["nsub"] = nsub;
  pfd["npart"] = npart;

  pfd["proflen"] = proflen;
  pfd["numchan"] = numchan;
  pfd["pstep"] = pstep;
  pfd["pdstep"] = pdstep;
  pfd["dmstep"] = dmstep;
  pfd["ndmfact"] = ndmfact;
  pfd["npfact"] = npfact;

  pfd["filenm"] = filenm;
  pfd["candnm"] = candnm;
  pfd["telescope"] = telescope;
  pfd["pgdev"] = pgdev;

  pfd["rastr"] = rastr;
  pfd["decstr"] = decstr;
  pfd["dt"] = dt;
  pfd["startT"] = startT;
  pfd["endT"] = endT;
  pfd["tepoch"] = tepoch;
  pfd["bepoch"] = bepoch;
  pfd["avgvoverc"] = avgvoverc;
  pfd["lofreq"] = lofreq;
  pfd["chan_wid"] = chan_wid;
  pfd["bestdm"] = bestdm;

  topo["pow"] = topopow;
  topo["p1"] = topop1;
  topo["p2"] = topop2;
  topo["p3"] = topop3;
  pfd["topo"] = topo;

  bary["pow"] = barypow;
  bary["p1"] = baryp1;
  bary["p2"] = baryp2;
  bary["p3"] = baryp3;
  pfd["bary"] = bary;

  fold["pow"] = foldpow;
  fold["p1"] = foldp1;
  fold["p2"] = foldp2;
  fold["p3"] = foldp3;
  pfd["fold"] = fold;

  orb["p"] = orbp;
  orb["e"] = orbe;
  orb["x"] = orbx;
  orb["t"] = orbt;
  orb["pd"] = orbpd;
  orb["wd"] = orbwd;
  pfd["orb"] = orb;

  size_t dmx[1] = {static_cast<size_t>(numdms)};
  pfd["dms"] = nb::ndarray<nb::numpy, double>(dms, 1, dmx, nb::handle());

  size_t px[1] = {static_cast<size_t>(numperiods)};
  pfd["periods"] = nb::ndarray<nb::numpy, double>(periods, 1, px, nb::handle());

  size_t pdotx[1] = {static_cast<size_t>(numpdots)};
  pfd["pdots"] = nb::ndarray<nb::numpy, double>(pdots, 1, pdotx, nb::handle());

  size_t foldx[3] = {static_cast<size_t>(nsub), static_cast<size_t>(npart),
                     static_cast<size_t>(proflen)};
  pfd["rawfolds"] =
      nb::ndarray<nb::numpy, double>(rawfolds, 3, foldx, nb::handle());

  size_t statx[3] = {static_cast<size_t>(nsub), static_cast<size_t>(npart), 7};
  pfd["stats"] =
      nb::ndarray<nb::numpy, double>(foldstats, 3, statx, nb::handle());

  fclose(f);
  return pfd;
}

void init_pfd(nb::module_ m) { m.def("readpfd", &readpfd); }
