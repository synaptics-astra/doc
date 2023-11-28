project = 'Synaptics Astra SDK User Guide'
copyright = '2023, Synaptics'
author = 'Synaptics'
release = '0.0.1'

exclude_patterns = ["README.rst"]

html_logo = "images/logo_full_white.png"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
  'sphinx_rtd_theme'
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']

html_theme_options = {
  'logo_only': True
}

html_context = {
  'display_github': True,
  'github_repo': 'syna-astra-dev/doc',
  'github_version': 'master',
  'conf_py_path': '/'
}
