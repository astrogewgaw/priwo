#include <cerrno>
#include <climits>
#include <cmath>

#include "inf.h"

constexpr int NUMBANDS = 6;
constexpr int NUMSCOPES = 8;
constexpr int NUMFILTERS = 11;
constexpr int MAXNUMONOFF = 40;

constexpr char BANDS[NUMBANDS][40] = {"Radio", "IR",    "Optical",
                                      "UV",    "X-ray", "Gamma"};

constexpr char scopes[NUMSCOPES][40] = {
    "None (Artificial Data Set)", "Arecibo",          "Parkes", "VLA", "MMT",
    "Las Campanas 2.5m",          "Mt. Hopkins 48in", "Other"};

void _getval(FILE *f, char *val, const char *key) {
  int ii, slen;
  char line[250];
  char *sptr = NULL;

  sptr = fgets(line, 250, f);
  if (sptr != NULL && sptr[0] != '\n' && 0 != (ii = strlen(sptr))) {
    if (ii >= 40 && line[40] == '=')
      sptr = line + 41;
    else {
      while (--ii >= 0)
        if (sptr[ii] == '=') break;
      if (ii + 1 == 0) {
        sprintf(line,
                "No '=' to separate key/value while looking for '%s'! "
                "Exiting...",
                key);
        throw std::runtime_error(line);
      }
      sptr = line + ii + 1;
    }
    sptr = rmspace(sptr);
    slen = strlen(sptr);
    if (slen) {
      if ((strcmp(key, "name") == 0 && slen > 199) ||
          (strcmp(key, "telescope") == 0 && slen > 39) ||
          (strcmp(key, "band") == 0 && slen > 39) ||
          (strcmp(key, "name") != 0 && slen > 99)) {
        sprintf(line, "Value is too long (%d char) for '%s'! Exiting...", slen,
                key);
        throw std::runtime_error(line);
      }
      strcpy(val, sptr);
    } else
      strcpy(val, "Unknown");
    return;
  } else {
    if (feof(f))
      sprintf(line, "Reached EOF while looking for '%s'! Exiting...", key);
    else
      sprintf(line, "Found blank line while looking for '%s'! Exiting...", key);
    throw std::runtime_error(line);
  }
}

double _str2dbl(char *val, const char *key) {
  double retval;

  char *endptr;
  char err[100];
  char *sptr = val;

  retval = strtod(sptr, &endptr);
  if (retval == 0.0 && endptr == val) {
    sprintf(err, "Cannot convert '%s' to double (%s)! Exiting...", val, key);
    throw std::runtime_error(err);
  }
  return retval;
}

long _str2long(char *val, const char *key) {
  long retval;

  char *endptr;
  char err[100];
  char *sptr = val;

  errno = 0;
  retval = strtol(sptr, &endptr, 10);

  if ((errno == ERANGE && (retval == LONG_MAX || retval == LONG_MIN)) ||
      (errno != 0 && retval == 0)) {
    sprintf(err, "Cannot convert '%s' to long (%s)! Exiting...", val, key);
    throw std::runtime_error(err);
  }

  if (endptr == val) {
    sprintf(err, "No digits found in '%s' for %s! Exiting...", val, key);
    throw std::runtime_error(err);
  }

  return retval;
}

void _str2radec(char *radec, int *h_or_d, int *m, double *s) {
  int retval;
  radec = rmspace(radec);
  retval = sscanf(radec, "%d:%d:%lf\n", h_or_d, m, s);
  if (retval != 3) {
    char err[100];
    sprintf(err, "Cannot convert '%s' to RA or DEC! Exiting...", radec);
    throw std::runtime_error(err);
  }
  if (radec[0] == '-' && *h_or_d == 0) {
    *m = -*m;
    *s = -*s;
  }
}

void _radec2str(char *radec, int h_or_d, int m, double s) {
  int offset = 0;
  if (h_or_d == 0 && (m < 0 || s < 0.0)) {
    radec[0] = '-';
    offset = 1;
  }
  sprintf(radec + offset, "%.2d:%.2d:%07.4f", h_or_d, abs(m), fabs(s));
}

nb::dict readinf(std::string fn) {
  nb::dict inf;

  char *sptr;
  int ii, retval, noteslen = 0;
  char tmp1[100], tmp2[100], tmp3[100];

  FILE *f = chkfopen(fn.c_str(), "r");

  double ra_s;                   /* Right ascension seconds (J2000)       */
  double dec_s;                  /* Declination seconds (J2000)           */
  double N;                      /* Number of bins in the time series     */
  double dt;                     /* Width of each time series bin (sec)   */
  double fov;                    /* Diameter of Beam or FOV in arcsec     */
  double mjd_f;                  /* Epoch of observation (MJD) frac part  */
  double dm;                     /* Radio -- Dispersion Measure (cm-3 pc) */
  double freq;                   /* Radio -- Low chan central freq (Mhz)  */
  double freqband;               /* Radio -- Total Bandwidth (Mhz)        */
  double chan_wid;               /* Radio -- Channel Bandwidth (Mhz)      */
  double wavelen;                /* IR,Opt,UV -- central wavelength (nm)  */
  double waveband;               /* IR,Opt,UV -- bandpass (nm)            */
  double energy;                 /* x-ray,gamma -- central energy (kev)   */
  double energyband;             /* x-ray,gamma -- energy bandpass (kev)  */
  double onoff[MAXNUMONOFF * 2]; /* Bin number pairs where obs is "on"    */
  int num_chan;                  /* Radio -- Number Channels              */
  int mjd_i;                     /* Epoch of observation (MJD) int part   */
  int ra_h;                      /* Right ascension hours (J2000)         */
  int ra_m;                      /* Right ascension minutes (J2000)       */
  int dec_d;                     /* Declination degrees (J2000)           */
  int dec_m;                     /* Declination minutes (J2000)           */
  int bary;                      /* Barycentered?  1=yes, 0=no            */
  int numonoff;                  /* The number of onoff pairs in the data */
  char notes[500];               /* Any additional notes                  */
  char name[200];                /* Data file name without suffix         */
  char object[100];              /* Object being observed                 */
  char instrument[100];          /* Instrument used                       */
  char observer[100];            /* Observer[s] for the data set          */
  char analyzer[100];            /* Who analyzed the data                 */
  char telescope[40];            /* Telescope used                        */
  char band[40];                 /* Type of observation (EM band)         */
  char filt[7];                  /* IR,Opt,UV -- Photometric Filter       */

  _getval(f, name, "name");
  _getval(f, telescope, "telescope");

  inf["name"] = name;
  inf["telescope"] = telescope;

  int isfake = strcmp(telescope, scopes[0]) == 0;

  if (!isfake) {
    _getval(f, instrument, "instrument");
    _getval(f, object, "object");
    _getval(f, tmp1, "RA string");
    _str2radec(tmp1, &ra_h, &ra_m, &ra_s);
    _getval(f, tmp1, "DEC string");
    _str2radec(tmp1, &dec_d, &dec_m, &dec_s);
    _getval(f, observer, "observer");
    _getval(f, tmp1, "MJD string");
    retval = sscanf(tmp1, "%d.%s", &mjd_i, tmp2);
    if (retval != 2) {
      sprintf(tmp3, "Cannot parse MJD string '%s'! Exiting...", tmp1);
      throw std::runtime_error(tmp3);
    }
    sprintf(tmp3, "0.%s", tmp2);
    mjd_f = _str2dbl(tmp3, "mjd_f");
    _getval(f, tmp1, "bary");
    bary = _str2long(tmp1, "bary");

    inf["bary"] = bary;
    inf["object"] = object;
    inf["observer"] = observer;
    inf["instrument"] = instrument;
    inf["mjd"] = nb::make_tuple(mjd_i, mjd_f);
    inf["ra"] = nb::make_tuple(ra_h, ra_m, ra_s);
    inf["dec"] = nb::make_tuple(dec_d, dec_m, dec_s);

  } else {
    strcpy(object, "fake pulsar");
    inf["object"] = object;
  }

  _getval(f, tmp1, "N");
  N = _str2dbl(tmp1, "N");
  _getval(f, tmp1, "dt");
  dt = _str2dbl(tmp1, "dt");
  _getval(f, tmp1, "numonoff");
  numonoff = _str2long(tmp1, "numonoff");

  inf["N"] = N;
  inf["dt"] = dt;
  inf["numonoff"] = numonoff;

  if (numonoff) {
    ii = 0;
    do {
      _getval(f, tmp1, "on-off pairs");
      retval = sscanf(tmp1, "%lf %*[ ,] %lf", &onoff[ii], &onoff[ii + 1]);
      if (retval != 2) {
        sprintf(tmp3, "Cannot parse on-off pair (%d)! Exiting...", ii / 2);
        throw std::runtime_error(tmp3);
      }
      ii += 2;
    } while (onoff[ii - 1] < N - 1 && ii < 2 * MAXNUMONOFF);
    numonoff = ii / 2;
    if (numonoff >= MAXNUMONOFF) {
      sprintf(tmp3,
              "Number of onoff pairs (%d) >= MAXNUMONOFF (%d)! Exiting...",
              numonoff, MAXNUMONOFF);
      throw std::runtime_error(tmp3);
    }
  } else {
    numonoff = 1;
    onoff[0] = 0;
    onoff[1] = N - 1;
  }
  inf["numonoff"] = numonoff;

  nb::list onofflist;
  if (numonoff) {
    for (ii = 0; ii < numonoff; ii++) {
      onofflist.append(nb::make_tuple(onoff[2 * ii], onoff[2 * ii + 1]));
    }
  }
  inf["onoff"] = onofflist;

  if (!isfake) {
    _getval(f, band, "band");
    inf["band"] = band;

    if (strcmp(band, BANDS[0]) == 0) {
      _getval(f, tmp1, "fov");
      fov = _str2dbl(tmp1, "fov");
      _getval(f, tmp1, "dm");
      dm = _str2dbl(tmp1, "dm");
      _getval(f, tmp1, "freq");
      freq = _str2dbl(tmp1, "freq");
      _getval(f, tmp1, "freqband");
      freqband = _str2dbl(tmp1, "freqband");
      _getval(f, tmp1, "num_chan");
      num_chan = _str2long(tmp1, "num_chan");
      _getval(f, tmp1, "chan_wid");
      chan_wid = _str2dbl(tmp1, "chan_wid");

      inf["dm"] = dm;
      inf["fov"] = fov;
      inf["freq"] = freq;
      inf["num_chan"] = num_chan;
      inf["freqband"] = freqband;
      inf["chan_wid"] = chan_wid;

    } else if ((strcmp(band, BANDS[4]) == 0) || (strcmp(band, BANDS[5]) == 0)) {
      _getval(f, tmp1, "fov");
      fov = _str2dbl(tmp1, "fov");
      _getval(f, tmp1, "energy");
      energy = _str2dbl(tmp1, "energy");
      _getval(f, tmp1, "energyband");
      energyband = _str2dbl(tmp1, "energyband");

      inf["fov"] = fov;
      inf["energy"] = energy;
      inf["energyband"] = energyband;

    } else {
      _getval(f, filt, "filt");
      _getval(f, tmp1, "fov");
      fov = _str2dbl(tmp1, "fov");
      _getval(f, tmp1, "wavelen");
      wavelen = _str2dbl(tmp1, "wavelen");
      _getval(f, tmp1, "waveband");
      waveband = _str2dbl(tmp1, "waveband");

      inf["fov"] = fov;
      inf["filt"] = filt;
      inf["wavelen"] = wavelen;
      inf["waveband"] = waveband;
    }
  }
  _getval(f, analyzer, "analyzer");
  inf["analyzer"] = analyzer;

  sptr = fgets(tmp1, 100, f);
  while (1) {
    sptr = fgets(tmp1, 100, f);
    if (noteslen + strlen(tmp1) > 500) break;
    if (sptr) {
      if (noteslen == 0)
        strcpy(notes + noteslen, rmlead(tmp1));
      else
        strcpy(notes + noteslen, tmp1);
      noteslen += strlen(notes);
    } else {
      if (feof(f)) break;
    }
  }
  inf["notes"] = notes;

  fclose(f);
  return inf;
}

void writeinf(nb::dict inf, std::string fn) {

  int ii, itmp;
  char tmp1[100], tmp2[100];

  FILE *f = chkfopen(fn.c_str(), "w");

  const char *name = nb::cast<const char *>(inf["name"]);
  const char *telescope = nb::cast<const char *>(inf["telescope"]);
  fprintf(f, " Data file name without suffix          =  %s\n", name);
  fprintf(f, " Telescope used                         =  %s\n", telescope);

  int isfake = strcmp(telescope, scopes[0]) == 0;

  if (!isfake) {
    int bary = nb::cast<int>(inf["bary"]);
    const char *object = nb::cast<const char *>(inf["object"]);
    const char *observer = nb::cast<const char *>(inf["observer"]);
    const char *instrument = nb::cast<const char *>(inf["instrument"]);

    nb::tuple ra = inf["ra"];
    nb::tuple dec = inf["dec"];
    nb::tuple mjd = inf["mjd"];

    int ra_h = nb::cast<int>(ra[0]);
    int ra_m = nb::cast<int>(ra[1]);
    double ra_s = nb::cast<double>(ra[2]);

    int dec_d = nb::cast<int>(dec[0]);
    int dec_m = nb::cast<int>(dec[1]);
    double dec_s = nb::cast<double>(dec[2]);

    int mjd_i = nb::cast<int>(mjd[0]);
    double mjd_f = nb::cast<double>(mjd[1]);

    fprintf(f, " Instrument used                        =  %s\n", instrument);
    fprintf(f, " Object being observed                  =  %s\n", object);
    _radec2str(tmp1, ra_h, ra_m, ra_s);
    fprintf(f, " J2000 Right Ascension (hh:mm:ss.ssss)  =  %s\n", tmp1);
    _radec2str(tmp1, dec_d, dec_m, dec_s);
    fprintf(f, " J2000 Declination     (dd:mm:ss.ssss)  =  %s\n", tmp1);
    fprintf(f, " Data observed by                       =  %s\n", observer);
    sprintf(tmp1, "%.15f", mjd_f);
    sscanf(tmp1, "%d.%s", &itmp, tmp2);
    fprintf(f, " Epoch of observation (MJD)             =  %d.%s\n", mjd_i,
            tmp2);
    fprintf(f, " Barycentered?           (1 yes, 0 no)  =  %d\n", bary);
  }
  nb::list onoffs = inf["onoff"];
  double N = nb::cast<double>(inf["N"]);
  double dt = nb::cast<double>(inf["dt"]);
  int numonoff = nb::cast<int>(inf["numonoff"]);

  fprintf(f, " Number of bins in the time series      =  %-11.0f\n", N);
  fprintf(f, " Width of each time series bin (sec)    =  %.15g\n", dt);
  fprintf(f, " Any breaks in the data? (1 yes, 0 no)  =  %d\n",
          numonoff > 1 ? 1 : 0);

  if (numonoff > 1) {
    for (ii = 0; ii < numonoff; ii++) {
      fprintf(f,
              " On/Off bin pair #%3d                   =  %-11.0f, %-11.0f\n",
              ii + 1, nb::cast<double>(onoffs[ii][0]),
              nb::cast<double>(onoffs[ii][1]));
    }
  }

  if (!isfake) {
    const char *band = nb::cast<const char *>(inf["band"]);
    fprintf(f, " Type of observation (EM band)          =  %s\n", band);
    if (strcmp(band, BANDS[0]) == 0) {
      double fov = nb::cast<double>(inf["fov"]);
      double dm = nb::cast<double>(inf["dm"]);
      double freq = nb::cast<double>(inf["freq"]);
      int num_chan = nb::cast<int>(inf["num_chan"]);
      double freqband = nb::cast<double>(inf["freqband"]);
      double chan_wid = nb::cast<double>(inf["chan_wid"]);

      fprintf(f, " Beam diameter (arcsec)                 =  %.0f\n", fov);
      fprintf(f, " Dispersion measure (cm-3 pc)           =  %.12g\n", dm);
      fprintf(f, " Central freq of low channel (MHz)      =  %.12g\n", freq);
      fprintf(f, " Total bandwidth (MHz)                  =  %.12g\n",
              freqband);
      fprintf(f, " Number of channels                     =  %d\n", num_chan);
      fprintf(f, " Channel bandwidth (MHz)                =  %.12g\n",
              chan_wid);
    } else if ((strcmp(band, BANDS[4]) == 0) || (strcmp(band, BANDS[5]) == 0)) {
      double fov = nb::cast<double>(inf["fov"]);
      double energy = nb::cast<double>(inf["energy"]);
      double energyband = nb::cast<double>(inf["energyband"]);

      fprintf(f, " Field-of-view diameter (arcsec)        =  %.2f\n", fov);
      fprintf(f, " Central energy (kev)                   =  %.1f\n", energy);
      fprintf(f, " Energy bandpass (kev)                  =  %.1f\n",
              energyband);
    } else {
      double fov = nb::cast<double>(inf["fov"]);
      double wavelen = nb::cast<double>(inf["wavelen"]);
      double waveband = nb::cast<double>(inf["waveband"]);
      const char *filt = nb::cast<const char *>(inf["filt"]);

      fprintf(f, " Photometric filter used                =  %s\n", filt);
      fprintf(f, " Field-of-view diameter (arcsec)        =  %.2f\n", fov);
      fprintf(f, " Central wavelength (nm)                =  %.1f\n", wavelen);
      fprintf(f, " Bandpass (nm)                          =  %.1f\n", waveband);
    }
  }
  const char *notes = nb::cast<const char *>(inf["notes"]);
  const char *analyzer = nb::cast<const char *>(inf["analyzer"]);

  fprintf(f, " Data analyzed by                       =  %s\n", analyzer);
  fprintf(f, " Any additional notes:\n    %s\n\n", notes);
  fclose(f);
}

void init_inf(nb::module_ m) {
  m.def("readinf", &readinf);
  m.def("writeinf", &writeinf);
}
