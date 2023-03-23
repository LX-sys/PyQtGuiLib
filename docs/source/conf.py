# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sphinx_rtd_theme
from recommonmark.parser import CommonMarkParser

project = 'PyQtGuiLib'
copyright = '2023, LX'
author = 'LX'
release = '2.4.18.11'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


templates_path = [sphinx_rtd_theme.get_html_theme_path()]
exclude_patterns = []

source_parsers = {
  '.md': CommonMarkParser,
}
source_suffix = ['.rst', '.md']
extensions = ['recommonmark']

language = 'zh_CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
