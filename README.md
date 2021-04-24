# priwo

![Tests][tests]
[![Coverage Status][coveralls-badge]][coveralls]
[![Code style: black][black-badge]][black]
[![Gitmoji][gitmoji-badge]][gitmoji]

## I/O for common pulsar data formats

[**priwo**][priwo] (a.k.a. **p**ulsar **r**ead **i**n **w**rite **o**ut) is a package written in pure Python that aims to implement simple functions to read in/write out pulsar data (such as time series, spectra, or frequency-time arrays) from various formats, such as those used in the [**presto**][presto] or [**sigproc**][sigproc] packages. I started writing this package because I often needed ways to work with these data in Python, but I did not have the means to access them (especially when the data were in a raw, binary format). The following formats are available right now:

* [**presto**][presto] time series (`*.dat` files).
* [**sigproc**][sigproc] time series (`*.tim` files).
* [**presto**][presto] frequency/power spectra (`*.fft` files).
* [**sigproc**][sigproc] frequency/power spectra (`*.spec` files).

More formats (such as [**presto**][presto]'s `*.pfd` files for folded data, [**sigproc**][sigproc]'s filterbank files for frequency-time arrays, [**PSRFITS**][psrfits] format files for both *fold* and *search* modes, and so on) are on the way :grin: ! If you have any data formats in mind that you would like to see support for, do not hestitate to drop in to the [**discussions**][discussions] page for this very repository. This package is still very much in development, so the api may be subject to frequent breaking changes (at least until the first release, which is coming soon!).

[discussions]: https://github.com/astrogewgaw/priwo/discussions

[tests]: https://github.com/astrogewgaw/priwo/actions/workflows/tests.yaml/badge.svg
[black]: https://github.com/psf/black
[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[gitmoji]: https://gitmoji.dev
[gitmoji-badge]: https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg?style=flat-square
[coveralls]: https://coveralls.io/github/astrogewgaw/priwo?branch=main
[coveralls-badge]: https://coveralls.io/repos/github/astrogewgaw/priwo/badge.svg?branch=main

[priwo]: https://github.com/astrogewgaw/priwo
[presto]: https://github.com/scottransom/presto
[sigproc]: http://sigproc.sourceforge.net/
[psrfits]: https://www.atnf.csiro.au/research/pulsar/psrfits_definition/Psrfits.html
