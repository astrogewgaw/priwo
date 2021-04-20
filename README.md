# priwo

![Tests][tests]
[![Coverage Status][coveralls-badge]][coveralls]
[![Code style: black][black-badge]][black]

## I/O for common pulsar data formats

**priwo** (a.k.a. **p**ulsar **r**ead **i**n **w**rite **o**ut) ia a package written in pure Python hat implements simple functions to read in and write out pulsar data from common formats (such as those used by the [**presto**][presto] or [**sigproc**][sigproc] packages). I started making this package because not being able to read data from these formats in Python was a common problem that we ran into. I hope that **priwo** can help solve this probelm for y'all. Still in development.

[tests]: https://github.com/astrogewgaw/priwo/actions/workflows/tests.yaml/badge.svg
[black]: https://github.com/psf/black
[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[coveralls]: https://coveralls.io/github/astrogewgaw/priwo?branch=main
[coveralls-badge]: https://coveralls.io/repos/github/astrogewgaw/priwo/badge.svg?branch=main

[presto]: https://github.com/scottransom/presto
[sigproc]: http://sigproc.sourceforge.net/
