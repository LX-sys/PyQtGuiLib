# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
from os.path import abspath,dirname

sys.path.insert(0,dirname(dirname(abspath(__file__))))

project = 'PyQtGuiLib'
copyright = '2023, LX'
author = 'LX'
release = '2.4.18.11'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

language = 'zh_CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'bizstyle'
html_static_path = ['_static']


source_parsers = {'.md': 'recommonmark.parser.CommonMarkParser'}
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}