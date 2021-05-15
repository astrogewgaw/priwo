# priwo

![Tests][tests]
![License][license]
![Python versions][pyversions]
[![Gitmoji][gitmoji-badge]][gitmoji]
[![Code style: black][black-badge]][black]
[![Documentation Status][docs-badge]][docs]
[![Coverage Status][coveralls-badge]][coveralls]

## I/O for common pulsar data formats

[**priwo**][priwo] (a.k.a. **p**ulsar **r**ead **i**n **w**rite **o**ut) is a package written in pure Python that aims to implement simple functions to read in/write out pulsar data (such as time series, spectra, or frequency-time arrays) from various formats, such as those used in the [**presto**][presto] or [**sigproc**][sigproc] packages. I started writing this package because I often needed ways to work with these data in Python, but I did not have the means to access them (especially when the data were in a raw, binary format). The following formats (for both data and metadata) are available right now:

* [**sigproc**][sigproc] headers
* [**presto**][presto] metadata files (`*.inf`),
* [**presto**][presto] time series data files (`*.dat`),
* [**sigproc**][sigproc] time series data files (`*.tim`),
* [**presto**][presto] frequency/power spectra data files (`*.fft`),
* [**presto**][presto] folded data files (`*.pfd`),
* [**presto**][presto] best profile data files (`*.bestprof`),
* [**presto**][presto] polynomial coefficient data files (`*.polycos`).

The package provides simple functions for each data format, and outputs a dictionary with all the data and metadata. The data is read in as a n-dimensional [**numpy**][numpy] array. I will add some simple documentation pretty soon. More formats (such as [**sigproc**][sigproc]'s filterbank files for frequency-time arrays, [**PSRFITS**][psrfits] files for both *fold* and *search* modes, and so on) are on the way :grin: ! If you have any data formats in mind that you would like to see support for, do not hestitate to drop in to the [**discussions**][discussions] page for this very repository. This package is still very much in development, so the api may be subject to frequent breaking changes (at least until the first release, which is coming soon!).

## Installation

To install [**priwo**](https://github.com/astrogewgaw/priwo), all you have to do is:

```bash
pip install priwo
```

This will automatically install all dependencies that are required for priwo to work. If you want to try out the latest features, you can (at your own risk!) clone the repository directly from GitHub:

```bash
git clone https://github.com/astrogewgaw/priwo.git
cd priwo
git checkout dev
make install
```

The above series of commands will clone the repository to a folder named *priwo*, switches to it as the current working directory, and then checks out the *dev* branch, where all the development actually happens. The last command then installs the package in *development mode*; that is, the changes you make in the code will be immediately reflected in your install of the package. `make install` requires the build tool, [**make**][make], to be installed. If you don't have that, you can just do:

```bash
pip install -e .
```

This is exactly what `make install` runs for us.

## Contributing

If you would like to contribute to priwo, you have to first *fork* the repository from GitHub, and then carry out the same steps as above, but this time with the URL of *your fork* in the `git clone` command. After that, switch to the *priwo* directory and run `pip install -e .` for a development install. After you have done all the changes you wanted to do, you can push the changes to your fork, and then send along a pull request to me! Just remember to go through this checklist first:

* Lint code using [**black**][black]. You can do that using either [**make**][make]:

    ```bash
    make lint
    ```

    or [**nox**][nox]:

    ```bash
    nox -s lint
    ```

* Write tests in the *tests* directory. priwo uses [**nox**][nox] and [**pytest**][pytest] for its tests. You can also use [**deepdiff**][deepdiff] to help out if you are comparing two Python data structures (lists or dicts, for instance) and don't want to write a large number of assert statements. Check out the tests already written for inspiration.
* Run the tests to make sure everything is working, by doing:

    ```bash
    make tests
    ```

    Or if you don't have [**make**][make], you can instead just run [**nox**][nox] directly, using:

    ```bash
    nox -s tests
    ```

    This is exactly what `make tests` runs for us. [**nox**][nox] ensures that all test dependencies are installed, and automatically tests priwo over multiple Python versions. You should (ideally) test your fork over all the Python versions supported by priwo (that is, 3.6, 3.7, 3.8 and 3.9).

### Notes

1. priwo ensures that its functions return a dictionary for each particular pulsar data format they read, and the functions that write the files back out also accept dictionaries as inputs. This is a delibrate choice that I made, to ensure that other people (like you, for instance) can build your own abstractions on top of priwo's functionalities. priwo also likes to abide by the KISS and DRY principles as much as possible. Do keep this stuff in mind if you think of contributing.
2. All the above commands (involving `make` or `nox`) are run in the root directory of the package.
3. And, lastly, all contributions are welcome! This even includes PRs for spelling mistakes, if you spot any! If you are unsure, talk to me (via [**GitHub Discussions**][discussions] or [**email**](ujjwalpanda97@gmail.com)).

## Issues

If you find any bugs :bug: in priwo, feel free to drop into the [**issues**][issues] and let me know what's going on!

[priwo]: https://github.com/astrogewgaw/priwo
[issues]: https://github.com/astrogewgaw/priwo/issues
[license]: https://img.shields.io/badge/License-MIT-green.svg
[pyversions]: https://img.shields.io/pypi/pyversions/priwo.svg
[discussions]: https://github.com/astrogewgaw/priwo/discussions

[gitmoji]: https://gitmoji.dev
[black]: https://github.com/psf/black
[docs]: https://priwo.readthedocs.io/en/latest/?badge=latest
[coveralls]: https://coveralls.io/github/astrogewgaw/priwo?branch=main
[tests]: https://github.com/astrogewgaw/priwo/actions/workflows/tests.yaml/badge.svg

[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[docs-badge]: https://readthedocs.org/projects/priwo/badge/?version=latest
[coveralls-badge]: https://coveralls.io/repos/github/astrogewgaw/priwo/badge.svg?branch=main
[gitmoji-badge]: https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg?style=flat-square

[numpy]: https://numpy.org/
[nox]: https://nox.thea.codes/en/stable/
[make]: https://www.gnu.org/software/make/
[sigproc]: http://sigproc.sourceforge.net/
[presto]: https://github.com/scottransom/presto
[deepdiff]: https://github.com/seperman/deepdiff
[pytest]: https://docs.pytest.org/en/6.2.x/contents.html
[psrfits]: https://www.atnf.csiro.au/research/pulsar/psrfits_definition/Psrfits.html
