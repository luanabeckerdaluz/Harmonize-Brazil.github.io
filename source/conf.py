# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Harmonize Brazil'
copyright = '2025, INPE'
author = 'INPE'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'

# Caminho do logo que será exibido no canto superior esquerdo
html_logo = '_static/harmonize.png'

# Caminho para arquivos estáticos (como imagens e CSS)
html_static_path = ['_static']

# Arquivo CSS adicional para personalizações visuais
html_css_files = [
    'custom.css',
]
