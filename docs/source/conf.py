project = "priwo"
author = "Ujjwal Panda"
exclude_patterns = [""]
html_static_path = ["static"]
templates_path = ["templates"]
html_theme = "sphinx_rtd_theme"
copyright = "2021-2022, Ujjwal Panda"
html_baseurl = "https://priwo.readthedocs.io"


extensions = extensions = [
    "nbsphinx",
    "myst_parser",
    "sphinx_sitemap",
    "sphinx_rtd_theme",
    "sphinx_copybutton",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx.ext.autosectionlabel",
]
