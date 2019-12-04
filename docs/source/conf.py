import os
import re
import sys

sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------

project = "mutapath"
copyright = "2019, 'matfax'"
author = "'matfax'"

release = re.sub("^v", "", os.popen("git describe").read().strip())
version = release

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "m2r",
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autosummary",
    "sphinx_rtd_theme",
    "sphinx.ext.linkcode",
    "sphinx.ext.intersphinx",
    "docs.attributes",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

html_css_files = [
    "style.css",
]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["static"]

master_doc = "index"

m2r_parse_relative_links = True
m2r_anonymous_references = True

autoclass_content = "both"
autodoc_mock_imports = ["shutil", "pathlib", "os", "filelock", "path"]
autosectionlabel_prefix_document = True
autosummary_generate = True
autosummary_imported_members = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "path": ("https://path.readthedocs.io/en/stable/", None),
    "filelock": ("https://filelock.readthedocs.io/en/latest/", None),
}


def linkcode_resolve(domain, info):
    if domain != "py":
        return None
    if not info["module"]:
        return None
    filename = info["module"].replace(".", "/")
    return "https://github.com/matfax/mutapath/blob/master/mutapath/%s.py" % filename
