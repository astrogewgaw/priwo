#include "../include/priwo/base.h"

#include <sys/stat.h>

#include <stdexcept>

namespace priwo {
  namespace base {
    FILE* safefopen(const char* filename, const char* mode) {
      FILE* file;
      if ((file = fopen(filename, mode)) == NULL)
        throw std::runtime_error("UNOPENABLE FILE. ABORT.");
      return file;
    }

    size_t safefread(void* ptr, size_t size, size_t n, FILE* s) {
      size_t retcode = fread(ptr, size, n, s);
      if (retcode != n && ferror(s)) throw std::runtime_error("UNREADABLE FILE. ABORT.");
      return retcode;
    }

    size_t safefwrite(void* ptr, size_t size, size_t n, FILE* s) {
      size_t retcode = fwrite(ptr, size, n, s);
      if ((retcode != n) && ferror(s)) throw std::runtime_error("UNWRITABLE FILE. ABORT.");
      return retcode;
    }

    size_t safefseek(FILE* s, off_t off, size_t size, int whence) {
      int retcode = fseeko(s, off * size, whence);
      if (retcode == -1) throw std::runtime_error("UNSEEKABLE FILE. ABORT.");
      return retcode;
    }

    long long chkfilelen(FILE* s, size_t size) {
      struct stat buf;
      int fd = fileno(s);
      int retcode = fstat(fd, &buf);
      if (retcode == -1) throw std::runtime_error("CANNOT GET FILE LEN. ABORT.");
      return (long long)(buf.st_size / size);
    }
  }  // namespace base
}  // namespace priwo
