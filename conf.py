import os

project = 'Synaptics Astra SDK User Guide'
copyright = '2023, Synaptics'
author = 'Synaptics'
release = '0.0.2'

exclude_patterns = ["README.rst", "org-docs/**"]

# render private pages only when the private tag is set
if not tags.tags.get('private', False):
    exclude_patterns.append("private/**")

html_logo = "images/logo_full_white.png"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
  'sphinx_rtd_theme'
]

templates_path = ['_templates']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"

html_theme_options = {
  'logo_only': True
}

# enable edit links only on the internal builds
if tags.tags.get('private', False):
    html_context = {
      'display_github': True,
      'github_repo': 'syna-astra-dev/doc',
      'github_version': 'master',
      'conf_py_path': '/'
    }

html_copy_source = False


# this code is used to substitute #xx# variables anywhere in the source, even
# inside literal blocks and code blocks

def preprocess_variables(app, docname, source):
    for varname, value in app.config.preprocessor_variables.items():
        source[0] = source[0].replace(varname, value)


preprocessor_variables = {
    "#release#": release
}


def setup(app):
    app.add_config_value('preprocessor_variables', {}, True)
    app.connect('source-read', preprocess_variables)
