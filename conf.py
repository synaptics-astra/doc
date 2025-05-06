import os

# setup documentation metadata
project = 'Synaptics Astra SDK User Guide'
copyright = '2023 - 2025, Synaptics'
author = 'Synaptics'
release = os.environ.get('RELEASE_VER', 'git-main')

html_static_path = ['_static']

exclude_patterns = ["README.rst", "org-docs/**"]

extensions = [
    'sphinx_rtd_theme'
]

html_theme = "sphinx_rtd_theme"

html_logo = "images/logo_full_white.png"

html_theme_options = {
  'logo_only': True,
  'style_nav_header_background': '#007dc3'
}

html_context = {
  'display_github': True,
  'github_repo': 'syna-astra-dev/doc',
  'github_version': 'main',
  'conf_py_path': '/',
  'version': release
}


# this code is used to substitute #xx# variables anywhere in the source, even
# inside literal blocks and code blocks

def preprocess_variables(app, docname, source):
    for varname, value in app.config.preprocessor_variables.items():
        source[0] = source[0].replace(varname, value)


preprocessor_variables = {
    "#release#": release
}


def setup(app):

    # add support for pre-processing
    app.add_config_value('preprocessor_variables', {}, True)
    app.connect('source-read', preprocess_variables)

    # add custom theme overrides and javascript
    app.add_css_file('css/synaptics.css')
    app.add_js_file('js/synaptics.js')
