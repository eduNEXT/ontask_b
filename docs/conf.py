# OnTask documentation build configuration file, created by
# sphinx-quickstart on Fri Nov 10 14:03:15 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

import sphinx_material

sys.path.insert(0, os.path.abspath('..'))

# -- General configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx_copybutton',
    'sphinx_search.extension',
    'sphinx.ext.ifconfig',
    'sphinx.ext.githubpages']

autosummary_generate = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The short X.Y version.
version = 'v10.1'
# The full version, including alpha/beta/rc tags.
release = version

# General information about the project.
project = 'OnTask'
copyright = 'Content Licensed under Creative Commons BY 4.0'
author = 'Abelardo Pardo'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    'Scenarios/scenario_04*',
    '**/include_*.rst',
    # 'Tutorial/Tasks*'
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# -- Options for HTML output ----------------------------------------------

html_show_sourcelink = True

extensions.append('sphinx_material')
html_theme_path = sphinx_material.html_theme_path()
html_context = sphinx_material.get_html_context()
html_theme = 'sphinx_material'

html_theme_options = {
    'nav_title': 'OnTask',

    # Set the repo location to get a badge with stats
    'repo_url': 'https://github.com/abelardopardo/ontask_b/',
    'repo_name': 'OnTask',

    # master doc
    'master_doc': 'index',
    
    # Set the color and the accent color
    'color_primary': 'teal',
    'color_accent': 'light-green',

    'html_minify': False,
    'html_prettify': True,
    'css_minify': True,

    # Visible levels of the global TOC; -1 means unlimited
    'globaltoc_depth': 3,
    # If False, expand all TOC entries
    'globaltoc_collapse': True,
    # If True, show hidden TOC entries
    'globaltoc_includehidden': False,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
html_sidebars = {
    '**': [
        'logo-text.html',
        'globaltoc.html',
        'localtoc.html',
        'searchbox.html']}

# -- Additional Options --------------------------------------------------

rst_prolog = '.. |ontask_version| replace:: %s\n' % version

# -- Add bootstrap 5 icons --------------------------------------------------
bootstrap_icons = [
    'fast-forward',
    'chevron-left',
    'chevron-right',
    'arrow-left',
    'journal-text',
    'calendar',
    'bar-chart-line-fill',
    'graph-up-arrow',
    'check',
    'check-circle-fill',
    'check-square-fill',
    'clock-fill',
    'files',
    'code-slash',
    'gear',
    'chat-right-quote-fill',
    'file-zip-fill',
    'download',
    'envelope-fill',
    'exclamation-triangle',
    'eye-fill',
    'file-earmark-text-fill',
    'file-earmark-zip-fill',
    'file-earmark-code-fill',
    'funnel-fill',
    'house-fill',
    'link-45deg',
    'dash-square-fill',
    'paperclip',
    'pencil-fill',
    'plus',
    'question-circle-fill',
    'rocket-takeoff-fill',
    'save-fill',
    'share-fill',
    'star-fill',
    'skip-start-fill',
    'skip-end-fill',
    'table',
    'list-task',
    'trash-fill',
    'upload',
    'person-square']

rst_prolog += '\n'.join([
    '.. |bi-{0}| raw:: html\n\n   <i class="bi-{0}"></i>\n'.format(icon_name)
    for icon_name in bootstrap_icons
])

rst_prolog += '\n.. |test-all-icons| raw:: html\n\n   <ul>'
rst_prolog += '\n'.join([
    '   <li><i class="bi-{0}"></i></li>'.format(icon_name)
    for icon_name in bootstrap_icons
])
rst_prolog += '\n   </ul>'


def setup(app):
    """Add additional stylesheets."""
    app.add_css_file('css/custom.css')  # may also be a URL
    app.add_css_file(
        'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.4/font/bootstrap-icons.css'
    )
