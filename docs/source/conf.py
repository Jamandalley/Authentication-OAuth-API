# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('C:\\API\\oauth\\sphinx_project'))



# The theme to use for HTML and HTML Help pages. See the documentation for a list of builtin themes.
html_theme = 'sphinx_rtd_theme'
project = 'AuthAPI'
copyright = '2024, Jamandalley'
author = 'Jamandalley'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest',
#               'sphinx.ext.intersphinx', 'sphinx.ext.todo',
#               'sphinx.ext.ifconfig', 'sphinx.ext.viewcode',
#               'sphinx.ext.inheritance_diagram', 'sphinx.ext.napoleon',
#               'sphinx.ext.autosummary', 'sphinx_autodoc_typehints',]

extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints',
]


templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
# html_theme = 'alabaster'
# html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']
