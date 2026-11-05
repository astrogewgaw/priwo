#include "priwo/sigproc/hdr.h"

#include <cstring>
#include <stdexcept>

#include "priwo/base.h"

namespace priwo {
  namespace sigproc {
    void bytes2str(FILE* s, int* n, char str[]) {
      int len;
      *n = sizeof(int);
      base::safefread(&len, sizeof(int), 1, s);
      if (feof(s)) throw std::runtime_error("REACHED EOF. ABORT.");
      if (len > 80 || len < 1) return;
      base::safefread(str, len, 1, s);
      str[len] = '\0';
      *n += len;
    }

    void str2bytes(FILE* s, std::string str) {
      int len = str.length();
      base::safefwrite(&len, sizeof(int), 1, s);
      base::safefwrite(str.data(), sizeof(char), len, s);
    }

    void key2bytes(FILE* s, std::string key, std::string val) {
      str2bytes(s, key);
      str2bytes(s, val);
    }

    void int2bytes(FILE* s, std::string key, int val) {
      str2bytes(s, key);
      base::safefwrite(&val, sizeof(int), 1, s);
    }

    void dbl2bytes(FILE* s, std::string key, double val) {
      str2bytes(s, key);
      base::safefwrite(&val, sizeof(double), 1, s);
    }

    void readhdr(FILE* s, SIGPROCHeader* hdr) {
      int n = 0;
      char str[80], msg[80];

      bytes2str(s, &n, str);
      if (strcmp(str, "HEADER_START")) {
        rewind(s);
        throw std::runtime_error("NOT A SIGPROC HEADER. ABORT.");
      }

      int SRCFLAG = 0;
      int FILEFLAG = 0;
      while (1) {
        bytes2str(s, &n, str);
        if (!strcmp(str, "HEADER_END")) break;
        if (!strcmp(str, "source_name")) {
          bytes2str(s, &n, str);
          strcpy(hdr->rawfile, str);
        } else if (!strcmp(str, "rawdatafile")) {
          bytes2str(s, &n, str);
          strcpy(hdr->source, str);
        } else if (!strcmp(str, "az_start"))
          base::safefread(&(hdr->azimuth), sizeof(double), 1, s);
        else if (!strcmp(str, "za_start"))
          base::safefread(&(hdr->zenith), sizeof(double), 1, s);
        else if (!strcmp(str, "src_raj"))
          base::safefread(&(hdr->raj), sizeof(double), 1, s);
        else if (!strcmp(str, "src_dej"))
          base::safefread(&(hdr->decj), sizeof(double), 1, s);
        else if (!strcmp(str, "tstart"))
          base::safefread(&(hdr->mjd), sizeof(double), 1, s);
        else if (!strcmp(str, "tsamp"))
          base::safefread(&(hdr->dt), sizeof(double), 1, s);
        else if (!strcmp(str, "fch1"))
          base::safefread(&(hdr->f0), sizeof(double), 1, s);
        else if (!strcmp(str, "foff"))
          base::safefread(&(hdr->df), sizeof(double), 1, s);
        else if (!strcmp(str, "refdm"))
          base::safefread(&(hdr->refdm), sizeof(double), 1, s);
        else if (!strcmp(str, "nchans"))
          base::safefread(&(hdr->nf), sizeof(int), 1, s);
        else if (!strcmp(str, "telescope_id"))
          base::safefread(&(hdr->telid), sizeof(int), 1, s);
        else if (!strcmp(str, "machine_id"))
          base::safefread(&(hdr->macid), sizeof(int), 1, s);
        else if (!strcmp(str, "data_type"))
          base::safefread(&(hdr->datatype), sizeof(int), 1, s);
        else if (!strcmp(str, "nbits"))
          base::safefread(&(hdr->nbits), sizeof(int), 1, s);
        else if (!strcmp(str, "nsamples"))
          base::safefread(&(hdr->nt), sizeof(int), 1, s);
        else if (!strcmp(str, "nifs"))
          base::safefread(&(hdr->nifs), sizeof(int), 1, s);
        else if (!strcmp(str, "nbeams"))
          base::safefread(&(hdr->nbeams), sizeof(int), 1, s);
        else if (!strcmp(str, "ibeam"))
          base::safefread(&(hdr->ibeam), sizeof(int), 1, s);
        else if (!strcmp(str, "signed"))
          base::safefread(&(hdr->signedints), sizeof(int), 1, s);
      }

      switch (hdr->telid) {
        case 0:
          strcpy(hdr->telescope, "Fake");
          break;
        case 1:
          strcpy(hdr->telescope, "Arecibo");
          break;
        case 2:
          strcpy(hdr->telescope, "Ooty");
          break;
        case 3:
          strcpy(hdr->telescope, "Nancay");
          break;
        case 4:
          strcpy(hdr->telescope, "Parkes");
          break;
        case 5:
          strcpy(hdr->telescope, "Jodrell");
          break;
        case 6:
          strcpy(hdr->telescope, "GBT");
          break;
        case 7:
          strcpy(hdr->telescope, "GMRT");
          break;
        case 8:
          strcpy(hdr->telescope, "Effelsberg");
          break;
        case 9:
          strcpy(hdr->telescope, "ATA");
          break;
        case 10:
          strcpy(hdr->telescope, "SRT");
          break;
        case 11:
          strcpy(hdr->telescope, "LOFAR");
          break;
        case 12:
          strcpy(hdr->telescope, "VLA");
          break;
        case 20:
          strcpy(hdr->telescope, "CHIME");
          break;
        case 21:
          strcpy(hdr->telescope, "FAST");
          break;
        case 30:
          strcpy(hdr->telescope, "MWA");
          break;
        case 64:
          strcpy(hdr->telescope, "MeerKAT");
          break;
        case 65:
          strcpy(hdr->telescope, "KAT-7");
          break;
        default:
          strcpy(hdr->telescope, "Unknown");
          break;
      }

      switch (hdr->macid) {
        case 0:
          strcpy(hdr->machine, "FAKE");
          break;
        case 1:
          strcpy(hdr->machine, "PSPM");
          break;
        case 2:
          strcpy(hdr->machine, "WAPP");
          break;
        case 3:
          strcpy(hdr->machine, "AOFTM");
          break;
        case 4:
          strcpy(hdr->machine, "BPP");
          break;
        case 5:
          strcpy(hdr->machine, "OOTY");
          break;
        case 6:
          strcpy(hdr->machine, "SCAMP");
          break;
        case 7:
          strcpy(hdr->machine, "SPIGOT");
          break;
        case 11:
          strcpy(hdr->machine, "BG/P");
          break;
        case 12:
          strcpy(hdr->machine, "PDEV");
          break;
        case 20:
          strcpy(hdr->machine, "CHIME+PSR");
          break;
        case 30:
          strcpy(hdr->machine, "MWA-VCS");
          break;
        case 31:
          strcpy(hdr->machine, "MWAX-VCS");
          break;
        case 32:
          strcpy(hdr->machine, "MWAX-RTB");
          break;
        case 64:
          strcpy(hdr->machine, "KAT");
          break;
        case 65:
          strcpy(hdr->machine, "KAT-DC2");
          break;
        default:
          strcpy(hdr->machine, "Unknown");
          break;
      }
    }

    void writehdr(FILE* s, SIGPROCHeader* hdr) {
      str2bytes(s, "HEADER_START");
      key2bytes(s, "rawdatafile", hdr->rawfile);
      key2bytes(s, "source_name", hdr->source);
      dbl2bytes(s, "az_start", hdr->azimuth);
      dbl2bytes(s, "za_start", hdr->zenith);
      dbl2bytes(s, "src_raj", hdr->raj);
      dbl2bytes(s, "src_dej", hdr->decj);
      dbl2bytes(s, "tstart", hdr->mjd);
      dbl2bytes(s, "tsamp", hdr->dt);
      dbl2bytes(s, "fch1", hdr->f0);
      dbl2bytes(s, "foff", hdr->df);
      dbl2bytes(s, "refdm", hdr->refdm);
      int2bytes(s, "nchans", hdr->nf);
      int2bytes(s, "telescope_id", hdr->telid);
      int2bytes(s, "machine_id", hdr->macid);
      int2bytes(s, "data_type", hdr->datatype);
      int2bytes(s, "nbits", hdr->nbits);
      int2bytes(s, "barycentric", hdr->barycentric);
      int2bytes(s, "pulsarcentric", hdr->pulsarcentric);
      int2bytes(s, "nsamples", hdr->nt);
      int2bytes(s, "nifs", hdr->nifs);
      int2bytes(s, "nbeams", hdr->nbeams);
      int2bytes(s, "ibeam", hdr->ibeam);
      int2bytes(s, "signed", hdr->signedints);
      str2bytes(s, "HEADER_END");
    }
  }  // namespace sigproc
}  // namespace priwo
