#include "pfd.h"

nb::dict readpfd(std::string fn) {
  nb::dict pfd;

  char temp[16];
  int tmp, byteswap = 0;
  FILE *f = chkfopen(fn.c_str(), "rb");

  int numdms;        /* Number of 'dms' */
  int numperiods;    /* Number of 'periods' */
  int numpdots;      /* Number of 'pdots' */
  int nsub;          /* Number of frequency subbands folded */
  int npart;         /* Number of folds in time over integration */
  int proflen;       /* Number of bins per profile */
  int numchan;       /* Number of channels for radio data */
  int pstep;         /* Minimum period stepsize in profile phase bins */
  int pdstep;        /* Minimum p-dot stepsize in profile phase bins */
  int dmstep;        /* Minimum DM stepsize in profile phase bins */
  int ndmfact;       /* 2*ndmfact*proflen+1 DMs to search */
  int npfact;        /* 2*npfact*proflen+1 periods and p-dots to search */
  char *filenm;      /* Filename of the folded data */
  char *candnm;      /* String describing the candidate */
  char *telescope;   /* Telescope where observation took place */
  char *pgdev;       /* PGPLOT device to use */
  char rastr[16];    /* J2000 RA  string in format hh:mm:ss.ssss */
  char decstr[16];   /* J2000 DEC string in format dd:mm:ss.ssss */
  double dt;         /* Sampling interval of the data */
  double startT;     /* Fraction of observation file to start folding */
  double endT;       /* Fraction of observation file to stop folding */
  double tepoch;     /* Topocentric eopch of data in MJD */
  double bepoch;     /* Barycentric eopch of data in MJD */
  double avgvoverc;  /* Average topocentric velocity */
  double lofreq;     /* Center of low frequency radio channel */
  double chan_wid;   /* Width of each radio channel in MHz */
  double bestdm;     /* Best DM */
  nb::dict topo;     /* Best topocentric p, pd, and pdd */
  nb::dict bary;     /* Best barycentric p, pd, and pdd */
  nb::dict fold;     /* f, fd, and fdd used to fold the initial data */
  nb::dict orb;      /* Barycentric orbital parameters used in folds */
  double *dms;       /* DMs used in the trials */
  double *periods;   /* Periods used in the trials */
  double *pdots;     /* P-dots used in the trials */
  double *rawfolds;  /* Raw folds (nsub * npart * proflen points) */
  double *foldstats; /* Statistics for the raw folds */

  numdms = parseint(f, byteswap);
  numperiods = parseint(f, byteswap);
  numpdots = parseint(f, byteswap);
  nsub = parseint(f, byteswap);
  npart = parseint(f, byteswap);

  if (npart < 1 || npart > 10000) {
    byteswap = 1;

    nsub = swapint(nsub);
    npart = swapint(npart);
    numdms = swapint(numdms);
    numpdots = swapint(numpdots);
    numperiods = swapint(numperiods);
  }

  proflen = parseint(f, byteswap);
  numchan = parseint(f, byteswap);
  pstep = parseint(f, byteswap);
  pdstep = parseint(f, byteswap);
  dmstep = parseint(f, byteswap);
  ndmfact = parseint(f, byteswap);
  npfact = parseint(f, byteswap);

  tmp = parseint(f, byteswap);
  filenm = (char *)calloc(tmp + 1, sizeof(char));
  chkfread(filenm, sizeof(char), tmp, f);

  tmp = parseint(f, byteswap);
  candnm = (char *)calloc(tmp + 1, sizeof(char));
  chkfread(candnm, sizeof(char), tmp, f);

  tmp = parseint(f, byteswap);
  telescope = (char *)calloc(tmp + 1, sizeof(char));
  chkfread(telescope, sizeof(char), tmp, f);

  tmp = parseint(f, byteswap);
  pgdev = (char *)calloc(tmp + 1, sizeof(char));
  chkfread(pgdev, sizeof(char), tmp, f);

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

  endT = parsedouble(f, byteswap);
  tepoch = parsedouble(f, byteswap);
  bepoch = parsedouble(f, byteswap);
  avgvoverc = parsedouble(f, byteswap);
  lofreq = parsedouble(f, byteswap);
  chan_wid = parsedouble(f, byteswap);
  bestdm = parsedouble(f, byteswap);

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

  dms = (double *)calloc(numdms, sizeof(double));
  chkfread(dms, sizeof(double), numdms, f);

  periods = (double *)calloc(numperiods, sizeof(double));
  chkfread(periods, sizeof(double), numperiods, f);

  pdots = (double *)calloc(numpdots, sizeof(double));
  chkfread(pdots, sizeof(double), numpdots, f);

  rawfolds = (double *)calloc(nsub * npart * proflen, sizeof(double));
  chkfread(rawfolds, sizeof(double), nsub * npart * proflen, f);

  foldstats = (double *)calloc(nsub * npart * 7, sizeof(double));
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
  orb["w"] = orbw;
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

void writepfd(nb::dict pfd, std::string fn) {
  FILE *f = chkfopen(fn.c_str(), "wb");
  int itmp;

  int numdms = nb::cast<int>(pfd["numdms"]);
  int numperiods = nb::cast<int>(pfd["numperiods"]);
  int numpdots = nb::cast<int>(pfd["numpdots"]);
  int nsub = nb::cast<int>(pfd["nsub"]);
  int npart = nb::cast<int>(pfd["npart"]);
  int proflen = nb::cast<int>(pfd["proflen"]);
  int numchan = nb::cast<int>(pfd["numchan"]);
  int pstep = nb::cast<int>(pfd["pstep"]);
  int pdstep = nb::cast<int>(pfd["pdstep"]);
  int dmstep = nb::cast<int>(pfd["dmstep"]);
  int ndmfact = nb::cast<int>(pfd["ndmfact"]);
  int npfact = nb::cast<int>(pfd["npfact"]);

  std::string filenm = nb::cast<std::string>(pfd["filenm"]);
  std::string candnm = nb::cast<std::string>(pfd["candnm"]);
  std::string telescope = nb::cast<std::string>(pfd["telescope"]);
  std::string pgdev = nb::cast<std::string>(pfd["pgdev"]);

  std::string rastr = nb::cast<std::string>(pfd["rastr"]);
  std::string decstr = nb::cast<std::string>(pfd["decstr"]);

  double dt = nb::cast<double>(pfd["dt"]);
  double startT = nb::cast<double>(pfd["startT"]);
  double endT = nb::cast<double>(pfd["endT"]);
  double tepoch = nb::cast<double>(pfd["tepoch"]);
  double bepoch = nb::cast<double>(pfd["bepoch"]);
  double avgvoverc = nb::cast<double>(pfd["avgvoverc"]);
  double lofreq = nb::cast<double>(pfd["lofreq"]);
  double chan_wid = nb::cast<double>(pfd["chan_wid"]);
  double bestdm = nb::cast<double>(pfd["bestdm"]);

  chkfwrite(&numdms, sizeof(int), 1, f);
  chkfwrite(&numperiods, sizeof(int), 1, f);
  chkfwrite(&numpdots, sizeof(int), 1, f);
  chkfwrite(&nsub, sizeof(int), 1, f);
  chkfwrite(&npart, sizeof(int), 1, f);
  chkfwrite(&proflen, sizeof(int), 1, f);
  chkfwrite(&numchan, sizeof(int), 1, f);
  chkfwrite(&pstep, sizeof(int), 1, f);
  chkfwrite(&pdstep, sizeof(int), 1, f);
  chkfwrite(&dmstep, sizeof(int), 1, f);
  chkfwrite(&ndmfact, sizeof(int), 1, f);
  chkfwrite(&npfact, sizeof(int), 1, f);

  itmp = strlen(filenm.c_str());
  chkfwrite(&itmp, sizeof(int), 1, f);
  chkfwrite(filenm.data(), sizeof(char), itmp, f);

  itmp = strlen(candnm.c_str());
  chkfwrite(&itmp, sizeof(int), 1, f);
  chkfwrite(candnm.data(), sizeof(char), itmp, f);

  itmp = strlen(telescope.c_str());
  chkfwrite(&itmp, sizeof(int), 1, f);
  chkfwrite(telescope.data(), sizeof(char), itmp, f);

  itmp = strlen(pgdev.c_str());
  chkfwrite(&itmp, sizeof(int), 1, f);
  chkfwrite(pgdev.data(), sizeof(char), itmp, f);

  double topopow = nb::cast<double>(pfd["topo"]["pow"]);
  double topop1 = nb::cast<double>(pfd["topo"]["p1"]);
  double topop2 = nb::cast<double>(pfd["topo"]["p2"]);
  double topop3 = nb::cast<double>(pfd["topo"]["p3"]);

  double barypow = nb::cast<double>(pfd["bary"]["pow"]);
  double baryp1 = nb::cast<double>(pfd["bary"]["p1"]);
  double baryp2 = nb::cast<double>(pfd["bary"]["p2"]);
  double baryp3 = nb::cast<double>(pfd["bary"]["p3"]);

  double foldpow = nb::cast<double>(pfd["fold"]["pow"]);
  double foldp1 = nb::cast<double>(pfd["fold"]["p1"]);
  double foldp2 = nb::cast<double>(pfd["fold"]["p2"]);
  double foldp3 = nb::cast<double>(pfd["fold"]["p3"]);

  double orbp = nb::cast<double>(pfd["orb"]["p"]);
  double orbe = nb::cast<double>(pfd["orb"]["e"]);
  double orbx = nb::cast<double>(pfd["orb"]["x"]);
  double orbw = nb::cast<double>(pfd["orb"]["w"]);
  double orbt = nb::cast<double>(pfd["orb"]["t"]);
  double orbpd = nb::cast<double>(pfd["orb"]["pd"]);
  double orbwd = nb::cast<double>(pfd["orb"]["wd"]);

  chkfwrite(rastr.data(), sizeof(char), 16, f);
  chkfwrite(decstr.data(), sizeof(char), 16, f);
  chkfwrite(&dt, sizeof(double), 1, f);
  chkfwrite(&startT, sizeof(double), 1, f);
  chkfwrite(&endT, sizeof(double), 1, f);
  chkfwrite(&tepoch, sizeof(double), 1, f);
  chkfwrite(&bepoch, sizeof(double), 1, f);
  chkfwrite(&avgvoverc, sizeof(double), 1, f);
  chkfwrite(&lofreq, sizeof(double), 1, f);
  chkfwrite(&chan_wid, sizeof(double), 1, f);
  chkfwrite(&bestdm, sizeof(double), 1, f);
  chkfwrite(&topopow, sizeof(double), 1, f);
  chkfwrite(&topop1, sizeof(double), 1, f);
  chkfwrite(&topop2, sizeof(double), 1, f);
  chkfwrite(&topop3, sizeof(double), 1, f);
  chkfwrite(&barypow, sizeof(double), 1, f);
  chkfwrite(&baryp1, sizeof(double), 1, f);
  chkfwrite(&baryp2, sizeof(double), 1, f);
  chkfwrite(&baryp3, sizeof(double), 1, f);
  chkfwrite(&foldpow, sizeof(double), 1, f);
  chkfwrite(&foldp1, sizeof(double), 1, f);
  chkfwrite(&foldp2, sizeof(double), 1, f);
  chkfwrite(&foldp3, sizeof(double), 1, f);
  chkfwrite(&orbp, sizeof(double), 1, f);
  chkfwrite(&orbe, sizeof(double), 1, f);
  chkfwrite(&orbx, sizeof(double), 1, f);
  chkfwrite(&orbw, sizeof(double), 1, f);
  chkfwrite(&orbt, sizeof(double), 1, f);
  chkfwrite(&orbpd, sizeof(double), 1, f);
  chkfwrite(&orbwd, sizeof(double), 1, f);

  nb::ndarray<nb::numpy, double> dms =
      nb::cast<nb::ndarray<nb::numpy, double>>(pfd["dms"]);

  nb::ndarray<nb::numpy, double> periods =
      nb::cast<nb::ndarray<nb::numpy, double>>(pfd["periods"]);

  nb::ndarray<nb::numpy, double> pdots =
      nb::cast<nb::ndarray<nb::numpy, double>>(pfd["pdots"]);

  nb::ndarray<nb::numpy, double> rawfolds =
      nb::cast<nb::ndarray<nb::numpy, double>>(pfd["rawfolds"]);

  nb::ndarray<nb::numpy, double> stats =
      nb::cast<nb::ndarray<nb::numpy, double>>(pfd["stats"]);

  chkfwrite(dms.data(), sizeof(double), numdms, f);
  chkfwrite(periods.data(), sizeof(double), numperiods, f);
  chkfwrite(pdots.data(), sizeof(double), numpdots, f);
  chkfwrite(rawfolds.data(), sizeof(double), nsub * npart * proflen, f);
  chkfwrite(stats.data(), sizeof(double), nsub * npart * 7, f);
  fclose(f);
}

void init_pfd(nb::module_ m) {
  m.def("readpfd", &readpfd);
  m.def("writepfd", &writepfd);
}
