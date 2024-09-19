#include "hdr.h"

static void _getstr(FILE *f, int *nbytes, char string[]) {
  int nchar;
  chkfread(&nchar, sizeof(int), 1, f);
  *nbytes = sizeof(int);
  if (feof(f)) throw std::runtime_error("Reached EOF! Exiting...");
  if (nchar > 80 || nchar < 1) return;
  chkfread(string, nchar, 1, f);
  string[nchar] = '\0';
  *nbytes += nchar;
}

static void _sendstr(std::string string, FILE *f) {
  int len;
  len = strlen(string.c_str());
  chkfwrite(&len, sizeof(int), 1, f);
  chkfwrite(string.data(), sizeof(char), len, f);
}

static void _senddbl(std::string name, double double_precision, FILE *f) {
  _sendstr(name, f);
  chkfwrite(&double_precision, sizeof(double), 1, f);
}

static void _sendint(std::string name, int integer, FILE *f) {
  _sendstr(name, f);
  chkfwrite(&integer, sizeof(int), 1, f);
}

std::string _getteln(int telescope_id) {
  char telescope[80];
  switch (telescope_id) {
  case 0:
    strcpy(telescope, "Fake");
    break;
  case 1:
    strcpy(telescope, "Arecibo");
    break;
  case 2:
    strcpy(telescope, "Ooty");
    break;
  case 3:
    strcpy(telescope, "Nancay");
    break;
  case 4:
    strcpy(telescope, "Parkes");
    break;
  case 5:
    strcpy(telescope, "Jodrell");
    break;
  case 6:
    strcpy(telescope, "GBT");
    break;
  case 7:
    strcpy(telescope, "GMRT");
    break;
  case 8:
    strcpy(telescope, "Effelsberg");
    break;
  case 9:
    strcpy(telescope, "ATA");
    break;
  case 10:
    strcpy(telescope, "SRT");
    break;
  case 11:
    strcpy(telescope, "LOFAR");
    break;
  case 12:
    strcpy(telescope, "VLA");
    break;
  case 20:
    strcpy(telescope, "CHIME");
    break;
  case 21:
    strcpy(telescope, "FAST");
    break;
  case 30:
    strcpy(telescope, "MWA");
    break;
  case 64:
    strcpy(telescope, "MeerKAT");
    break;
  case 65:
    strcpy(telescope, "KAT-7");
    break;
  default:
    strcpy(telescope, "Unknown");
    break;
  }
  return telescope;
}

std::string _getmachn(int machine_id) {
  char *backend, string[80];
  switch (machine_id) {
  case 0:
    strcpy(string, "FAKE");
    break;
  case 1:
    strcpy(string, "PSPM");
    break;
  case 2:
    strcpy(string, "WAPP");
    break;
  case 3:
    strcpy(string, "AOFTM");
    break;
  case 4:
    strcpy(string, "BPP");
    break;
  case 5:
    strcpy(string, "OOTY");
    break;
  case 6:
    strcpy(string, "SCAMP");
    break;
  case 7:
    strcpy(string, "SPIGOT");
    break;
  case 11:
    strcpy(string, "BG/P");
    break;
  case 12:
    strcpy(string, "PDEV");
    break;
  case 20:
    strcpy(string, "CHIME+PSR");
    break;
  case 30:
    strcpy(string, "MWA-VCS");
    break;
  case 31:
    strcpy(string, "MWAX-VCS");
    break;
  case 32:
    strcpy(string, "MWAX-RTB");
    break;
  case 64:
    strcpy(string, "KAT");
    break;
  case 65:
    strcpy(string, "KAT-DC2");
    break;
  default:
    strcpy(string, "Unknown");
    break;
  }
  backend = (char *)calloc(strlen(string) + 1, 1);
  strcpy(backend, string);
  return backend;
}

nb::dict readhdr(std::string fn) {
  nb::dict hdr;

  FILE *f = chkfopen(fn.c_str(), "rb");

  char string[80], message[80];
  int ix, nbytes = 0, totalbytes;
  int barycentric, pulsarcentric;
  int expecting_rawdatafile = 0, expecting_source_name = 0;

  _getstr(f, &nbytes, string);
  if (strcmp(string, "HEADER_START")) {
    rewind(f);
    throw std::runtime_error("SIGPROC header invalid! Exiting...");
  }
  totalbytes = nbytes;

  int datatype;
  char inpfile[80]; /* Input filename */
  char srcname[80]; /* Source name */
  long long N;      /* Number of points (in time) in the file */
  double tstart;    /* MJD start time */
  double tsamp;     /* Sampling time in sec */
  double src_raj;   /* Source RA  (J2000) in hhmmss.ss */
  double src_dej;   /* Source DEC (J2000) in ddmmss.ss */
  double az_start;  /* Starting azimuth in deg */
  double za_start;  /* Starting zenith angle in deg */
  double fch1;      /* Highest channel frequency (MHz) */
  double foff;      /* Channel stepsize (MHz) */
  double refdm;     /* Reference dispersion measure (pc/cm^3) */
  int machine_id;   /* Instrument ID (see backend_name() */
  int telescope_id; /* Telescope ID (see telescope_name() */
  int nchans;       /* Number of filterbank channels */
  int nsamples;     /* Number of filterbank samples */
  int nbits;        /* Number of bits in the filterbank samples */
  int nifs;         /* Number of IFs present */
  int nbeams;       /* Number of beams in the observing system */
  int ibeam;        /* Beam number used for this data */
  int sumifs;       /* Whether the IFs are summed or not */
  int signedints;   /* Whether the integer data is signed or not */

  ibeam = 1;
  sumifs = 1;
  signedints = 0;

  while (1) {
    _getstr(f, &nbytes, string);
    if (!strcmp(string, "HEADER_END")) break;
    totalbytes += nbytes;
    if (!strcmp(string, "rawdatafile")) {
      expecting_rawdatafile = 1;
    } else if (!strcmp(string, "source_name")) {
      expecting_source_name = 1;
    } else if (!strcmp(string, "az_start")) {
      chkfread(&(az_start), sizeof(double), 1, f);
      totalbytes += sizeof(double);
      hdr["az_start"] = az_start;
    } else if (!strcmp(string, "za_start")) {
      chkfread(&(za_start), sizeof(double), 1, f);
      totalbytes += sizeof(double);
      hdr["za_start"] = za_start;
    } else if (!strcmp(string, "src_raj")) {
      chkfread(&(src_raj), sizeof(double), 1, f);
      totalbytes += sizeof(double);
      hdr["src_raj"] = src_raj;
    } else if (!strcmp(string, "src_dej")) {
      chkfread(&(src_dej), sizeof(double), 1, f);
      totalbytes += sizeof(double);
      hdr["src_dej"] = src_dej;
    } else if (!strcmp(string, "tstart")) {
      chkfread(&(tstart), sizeof(double), 1, f);
      totalbytes += sizeof(double);
      hdr["tstart"] = tstart;
    } else if (!strcmp(string, "tsamp")) {
      chkfread(&(tsamp), sizeof(double), 1, f);
      totalbytes += sizeof(double);
      hdr["tsamp"] = tsamp;
    } else if (!strcmp(string, "fch1")) {
      chkfread(&(fch1), sizeof(double), 1, f);
      totalbytes += sizeof(double);
      hdr["fch1"] = fch1;
    } else if (!strcmp(string, "foff")) {
      chkfread(&(foff), sizeof(double), 1, f);
      totalbytes += sizeof(double);
      hdr["foff"] = foff;
    } else if (!strcmp(string, "refdm")) {
      chkfread(&(refdm), sizeof(double), 1, f);
      totalbytes += sizeof(double);
      hdr["refdm"] = refdm;
    } else if (!strcmp(string, "nchans")) {
      chkfread(&(nchans), sizeof(int), 1, f);
      totalbytes += sizeof(int);
      hdr["nchans"] = nchans;
    } else if (!strcmp(string, "telescope_id")) {
      chkfread(&(telescope_id), sizeof(int), 1, f);
      totalbytes += sizeof(int);
      hdr["telescope_id"] = telescope_id;
      hdr["telescope"] = _getteln(telescope_id);
    } else if (!strcmp(string, "machine_id")) {
      chkfread(&(machine_id), sizeof(int), 1, f);
      totalbytes += sizeof(int);
      hdr["machine_id"] = machine_id;
      hdr["machine"] = _getmachn(machine_id);
    } else if (!strcmp(string, "data_type")) {
      chkfread(&(datatype), sizeof(int), 1, f);
      totalbytes += sizeof(int);
      hdr["datatype"] = datatype;
    } else if (!strcmp(string, "nbits")) {
      chkfread(&(nbits), sizeof(int), 1, f);
      totalbytes += sizeof(int);
      hdr["nbits"] = nbits;
    } else if (!strcmp(string, "barycentric")) {
      chkfread(&barycentric, sizeof(int), 1, f);
      totalbytes += sizeof(int);
    } else if (!strcmp(string, "pulsarcentric")) {
      chkfread(&pulsarcentric, sizeof(int), 1, f);
      totalbytes += sizeof(int);
    } else if (!strcmp(string, "nsamples")) {
      chkfread(&(nsamples), sizeof(int), 1, f);
      totalbytes += sizeof(int);
      hdr["nsamples"] = nsamples;
    } else if (!strcmp(string, "nifs")) {
      chkfread(&(nifs), sizeof(int), 1, f);
      if (nifs > 1) sumifs = 0;
      totalbytes += sizeof(int);
      hdr["nifs"] = nifs;
      hdr["sumifs"] = sumifs;
    } else if (!strcmp(string, "nbeams")) {
      chkfread(&(nbeams), sizeof(int), 1, f);
      totalbytes += sizeof(int);
      hdr["nbeams"] = nbeams;
    } else if (!strcmp(string, "ibeam")) {
      chkfread(&(ibeam), sizeof(int), 1, f);
      totalbytes += sizeof(int);
      hdr["ibeam"] = ibeam;
    } else if (!strcmp(string, "signed")) {
      char tmp;
      chkfread(&(signedints), sizeof(char), 1, f);
      totalbytes += sizeof(char);
      hdr["signedints"] = signedints;
    } else if (expecting_rawdatafile) {
      strcpy(inpfile, string);
      hdr["rawdatafile"] = inpfile;
      expecting_rawdatafile = 0;
    } else if (expecting_source_name) {
      strcpy(srcname, string);
      hdr["source_name"] = srcname;
      expecting_source_name = 0;
    }
  }
  fclose(f);
  totalbytes += nbytes;
  hdr["hdrlen"] = totalbytes;
  return hdr;
}

void writehdr(nb::dict &hdr, std::string fn) {
  FILE *f = chkfopen(fn.c_str(), "wb");

  _sendstr("HEADER_START", f);
  for (auto item : hdr) {
    std::string key = nb::cast<std::string>(item.first);
    if (!strcmp(key.c_str(), "rawdatafile")) {
      _sendstr(key, f);
      _sendstr(nb::cast<std::string>(item.second), f);
    } else if (!strcmp(key.c_str(), "source_name")) {
      _sendstr(key, f);
      _sendstr(nb::cast<std::string>(item.second), f);
    } else if (!strcmp(key.c_str(), "az_start")) {
      _senddbl(key, nb::cast<double>(item.second), f);
    } else if (!strcmp(key.c_str(), "za_start")) {
      _senddbl(key, nb::cast<double>(item.second), f);
    } else if (!strcmp(key.c_str(), "src_raj")) {
      _senddbl(key, nb::cast<double>(item.second), f);
    } else if (!strcmp(key.c_str(), "src_dej")) {
      _senddbl(key, nb::cast<double>(item.second), f);
    } else if (!strcmp(key.c_str(), "tstart")) {
      _senddbl(key, nb::cast<double>(item.second), f);
    } else if (!strcmp(key.c_str(), "tsamp")) {
      _senddbl(key, nb::cast<double>(item.second), f);
    } else if (!strcmp(key.c_str(), "fch1")) {
      _senddbl(key, nb::cast<double>(item.second), f);
    } else if (!strcmp(key.c_str(), "foff")) {
      _senddbl(key, nb::cast<double>(item.second), f);
    } else if (!strcmp(key.c_str(), "refdm")) {
      _senddbl(key, nb::cast<double>(item.second), f);
    } else if (!strcmp(key.c_str(), "nchans")) {
      _sendint(key, nb::cast<int>(item.second), f);
    } else if (!strcmp(key.c_str(), "telescope_id")) {
      _sendint(key, nb::cast<int>(item.second), f);
    } else if (!strcmp(key.c_str(), "machine_id")) {
      _sendint(key, nb::cast<int>(item.second), f);
    } else if (!strcmp(key.c_str(), "data_type")) {
      _sendint(key, nb::cast<int>(item.second), f);
    } else if (!strcmp(key.c_str(), "nbits")) {
      _sendint(key, nb::cast<int>(item.second), f);
    } else if (!strcmp(key.c_str(), "barycentric")) {
      _sendint(key, nb::cast<int>(item.second), f);
    } else if (!strcmp(key.c_str(), "pulsarcentric")) {
      _sendint(key, nb::cast<int>(item.second), f);
    } else if (!strcmp(key.c_str(), "nsamples")) {
      _sendint(key, nb::cast<int>(item.second), f);
    } else if (!strcmp(key.c_str(), "nifs")) {
      _sendint(key, nb::cast<int>(item.second), f);
    } else if (!strcmp(key.c_str(), "nbeams")) {
      _sendint(key, nb::cast<int>(item.second), f);
    } else if (!strcmp(key.c_str(), "ibeam")) {
      _sendint(key, nb::cast<int>(item.second), f);
    } else if (!strcmp(key.c_str(), "signed")) {
      _sendint(key, nb::cast<int>(item.second), f);
    }
  }
  _sendstr("HEADER_END", f);
  fclose(f);
}

void init_hdr(nb::module_ m) {
  m.def("readhdr", &readhdr);
  m.def("writehdr", &writehdr);
}
