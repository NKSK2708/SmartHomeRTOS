import os
import sys

# Add project src to sys.path so autodoc can import modules
sys.path.insert(0, os.path.abspath('../src'))

project = 'SmartHomeRTOS'
author = 'SmartHomeRTOS'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'myst_parser',
]

# Allow markdown files via myst-parser
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Autodoc settings
autoclass_content = 'both'
autodoc_member_order = 'bysource'

# Suppress missing cross-reference warnings coming from third-party md files
# (example: mdit_py_plugins README referencing a local ./license.txt).
# This warning is harmless for our build and noisy in CI; keep other warnings.
suppress_warnings = ['myst.xref_missing']
