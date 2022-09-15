# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

import setuptools_scm

project = 'Manrododex'
copyright = '2022, Charbel Assaad'
author = 'Charbel Assaad'

# https://github.com/qtile/qtile/blob/master/docs/conf.py
# The short X.Y version.
version = setuptools_scm.get_version(root="..")
# The full version, including alpha/beta/rc tags.
release = version

# Add module to sys path
sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(1, os.path.abspath('../../'))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.napoleon',
        'sphinx_rtd_theme',
        'sphinxarg.ext'
]

napoleon_numpy_docstring = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_favicon = '_static/favicon.ico'
