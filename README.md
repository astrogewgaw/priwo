<div style="font-family:JetBrainsMono Nerd Font">
<div align="center">
<img
    alt="priwo: I/O for common pulsar data formats."
    src=https://raw.githubusercontent.com/astrogewgaw/logos/main/rasters/priwo.png
/>
</div>
<br/>

![License][license-badge]
![Version][version-badge]
![Python versions][pyversions-badge]

![Tests][tests-badge]
[![Documentation Status][docs-badge]][docs]
[![Interrogate][interrogate-badge]][interrogate]

![Stars][stars-badge]
![Downloads][dm-badge]
[![Issues][issues-badge]][issues]

[![Gitmoji][gitmoji-badge]][gitmoji]
[![Code style: black][black-badge]][black]

<div align="justify">

<h2>What is this?</h2>

[**`priwo`**][priwo] is a library that allows you to read in and write out
pulsar data from the following data formats:

* [**`SIGPROC`**][sigproc] headers,
* [**`PRESTO`**][presto] FFT (`*.fft`) files,
* [**`TEMPO`**][tempo] parameter (`*.par`) files,
* [**`PRESTO`**][presto] infodata (`*.inf`) files,
* [**`PRESTO`**][presto] folded data (`*.pfd`) files,
* [**`PRESTO`**][presto] time series (`*.dat`) files,
* [**`SIGPROC`**][sigproc] filterbank (`*.fil`) files,
* [**`SIGPROC`**][sigproc] time series (`*.tim`) files,
* [**`PRESTO`**][presto] best pulse profile (`*.bestprof`) files,
* [**`TEMPO`**][tempo] polynomial ephemerides (`*.polycos`) files.

`priwo`'s API is deliberately *low-level*: each function in `priwo` deals with a
single file format and takes/returns a Python dictionary. This allows users to
design arbitrary high-level APIs on top of `priwo`'s functionality. This is
unlike most other contemporary libraries, such as [**`your`**][your]. `your` (to
which this library has been frequently compared to) provides a high-level API
for reading in pulsar data, while also providing modules to help process and
analyze it. This is makes the number of dependencies it uses is a bit high (as
of 05/10/22, that is a total of 9 dependencies). On the other hand, `priwo` has
just 2 dependencies, [**`numpy`**][numpy] and [**`pabo`**][pabo][^1]. This makes
it an ideal choice to drop into your projects, without worrying about
[**dependency hell**][dependency_hell].

`priwo` is well-tested (via [**`ward`**][ward]) and actively maintained. No
major changes to the API are expected before `v0.1.0`. Support for many more
formats, such as [`PSRFITS`][psrfits], is on the way. If you would like to
contribute, have a look at [`CONTRIBUTING.md`](CONTRIBUTING.md), and get in
touch! If you find a bug, feel free to open an [issue][issues]. If you would
like to suggest support for any data format(s) I have missed, suggest a feature,
or just chat, feel free to jump into the [discussions][discussions].

<h2>Installing</h2>

Installing `priwo` is as easy as:

```bash
pip install priwo
```

<br/>

[^1]: [**`pabo`**][pabo] is a package I made to make parsing binary data easier,
  and it *also* has just two dependencies : [**`attrs`**][attrs] and
  [**`numpy`**][numpy].

</div>

[numpy]: https://numpy.org
[attrs]: https://www.attrs.org
[gitmoji]: https://gitmoji.dev
[black]: https://github.com/psf/black
[just]: https://github.com/casey/just
[tempo]: https://tempo.sourceforge.net
[sigproc]: http://sigproc.sourceforge.net
[pabo]: https://github.com/astrogewgaw/pabo
[ward]: https://github.com/darrenburns/ward
[priwo]: https://github.com/astrogewgaw/priwo
[docs]: https://priwo.readthedocs.io/en/latest
[presto]: https://github.com/scottransom/presto
[your]: https://github.com/thepetabyteproject/your
[issues]: https://github.com/astrogewgaw/priwo/issues
[interrogate]: https://github.com/econchick/interrogate
[discussions]: https://github.com/astrogewgaw/priwo/discussions
[dependency_hell]: https://en.wikipedia.org/wiki/Dependency_hell
[psrfits]: https://www.atnf.csiro.au/research/pulsar/psrfits_definition/Psrfits.html

[interrogate-badge]: assets/docs_cov.svg
[dm-badge]: https://img.shields.io/pypi/dm/priwo?style=for-the-badge
[version-badge]: https://img.shields.io/pypi/v/priwo?style=for-the-badge
[wheel-badge]: https://img.shields.io/pypi/wheel/priwo?style=for-the-badge
[forks-badge]: https://img.shields.io/github/forks/astrogewgaw/priwo?style=for-the-badge
[stars-badge]: https://img.shields.io/github/stars/astrogewgaw/priwo?style=for-the-badge
[pyversions-badge]: https://img.shields.io/pypi/pyversions/priwo.svg?style=for-the-badge
[issues-badge]: https://img.shields.io/github/issues/astrogewgaw/priwo?style=for-the-badge
[license-badge]: https://img.shields.io/github/license/astrogewgaw/priwo?style=for-the-badge
[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[docs-badge]: https://readthedocs.org/projects/priwo/badge/?version=latest&style=for-the-badge
[gitmoji-badge]: https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg?style=for-the-badge
[tests-badge]: https://img.shields.io/github/actions/workflow/status/astrogewgaw/priwo/test.yml?branch=dev&style=for-the-badge 
