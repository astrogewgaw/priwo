# type: ignore

import pathlib
import versioneer

from setuptools import setup, find_packages


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

install_requires = [
    "rich",
    "click",
    "numpy",
    "schema",
    "construct",
]

extra_requires = {
    "dev": [
        "pytest",
        "deepdiff",
        "pytest-cov",
    ]
}


setup(
    name="priwo",
    version=versioneer.get_version(),
    description="I/O for common pulsar data formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/astrogewgaw/priwo",
    author="Ujjwal Panda",
    author_email="ujjwalpanda97@gmail.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
    keywords=(
        "i/o",
        "pulsars",
        "astronomy",
        "radio astronomy",
        "data processing",
    ),
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_package_data=True,
    python_requires=">=3.5, <4",
    install_requires=install_requires,
    extra_requires=extra_requires,
    entry_points={
        "console_scripts": ["priwo=priwo.cli:main"],
    },
    project_urls={
        "Source": "https://github.com/astrogewgaw/priwo",
        "Bug Reports": "https://github.com/astrogewgaw/priwo/issues",
    },
    cmd_class=versioneer.get_cmdclass(),
    zip_safe=False,
)
