#include <cstddef>
#include <cstdio>

namespace priwo {
  namespace base {
    FILE* safefopen(const char* filename, const char* mode);
    size_t safefread(void* ptr, size_t size, size_t n, FILE* s);
    size_t safefwrite(void* ptr, size_t size, size_t n, FILE* s);
    size_t safefseek(FILE* s, off_t off, size_t size, int whence);
    long long chkfilelen(FILE* s, size_t size);
  }  // namespace base
}  // namespace priwo
