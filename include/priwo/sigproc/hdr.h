#include <cstdio>

namespace priwo {
  namespace sigproc {
    struct SIGPROCHeader {
      char rawfile[80] = "";   /* Input filename */
      char source[80] = "";    /* Source name */
      double mjd = 0.0;        /* MJD start time */
      double dt = 0.0;         /* Sampling time in sec */
      double raj = 0.0;        /* Source RA  (J2000) in hhmmss.ss */
      double decj = 0.0;       /* Source DEC (J2000) in ddmmss.ss */
      double azimuth = 0.0;    /* Starting azimuth in deg */
      double zenith = 0.0;     /* Starting zenith angle in deg */
      double f0 = 0.0;         /* Highest channel frequency (MHz) */
      double df = 0.0;         /* Channel stepsize (MHz) */
      double refdm = 0.0;      /* Reference dispersion measure (pc/cm^3) */
      int macid = 0;           /* Instrument ID */
      char machine[80] = "";   /* Instrument name */
      int telid = 0;           /* Telescope ID */
      char telescope[80] = ""; /* Telescope name */
      int nf = 0;              /* Number of finterbank channels */
      int nt = 0;              /* Number of filterbank samples */
      int nbits = 8;           /* Number of bits in the filterbank samples */
      int nifs = 1;            /* Number of IFs present */
      int nbeams = 1;          /* Number of beams in the observing system */
      int ibeam = 0;           /* Beam number used for this data */
      int sumifs = 1;          /* Whether the IFs are summed or not */
      int signedints = 0;      /* Whether the integer data is signed or not */
      int datatype = 0;
      int barycentric = 0;
      int pulsarcentric = 0;
    };

    void readhdr(FILE* s, SIGPROCHeader* hdr);
    void writehdr(FILE* s, SIGPROCHeader* hdr);
  }  // namespace sigproc
}  // namespace priwo
