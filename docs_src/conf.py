# -*- coding: utf-8 -*-
#
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

sys.path.insert(0, os.path.abspath('..'))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.todo',
              'sphinx.ext.mathjax',
              'sphinx.ext.ifconfig',
              'sphinx.ext.githubpages']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = u'B.6.0'
# The full version, including alpha/beta/rc tags.
release = version

# General information about the project.
project = u'OnTask (' + version + ')'
copyright = u'Content Licensed under Creative Commons BY 4.0'
author = u'Abelardo Pardo'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

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

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}
html_theme_options = {
    'show_related': True,
    'show_powered_by': False,
    'show_relbars': True,
    'fixed_sidebar': False,
    'github_banner': True,
    'github_button': True,
    'github_user': 'abelardopardo',
    'github_repo': 'ontask_b',
    'logo': 'ontask-logo-1.png'
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
        'donate.html',
    ]
}

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'OnTaskdoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'OnTask.tex', u'OnTask Documentation',
     u'Abelardo Pardo', 'manual'),
]

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'ontask', u'OnTask Documentation',
     [author], 1)
]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'OnTask', u'OnTask Documentation',
     author, 'OnTask', 'One line description of project.',
     'Miscellaneous'),
]

# -- Additional Options --------------------------------------------------

rst_prolog = '.. |ontask_version| replace:: %s\n' % version
rst_prolog += """
.. |fa-book| raw:: html

   <span class="fa fa-book"></span>
   
.. |fa-pencil| raw:: html

   <span class="fa fa-pencil"></span>
   
.. |fa-clone| raw:: html

   <span class="fa fa-clone"></span>
   
.. |fa-minus-square| raw:: html

   <span class="fa fa-minus-square"></span>
   
.. |fa-trash| raw:: html

   <span class="fa fa-trash"></span>
   
.. |fa-plus| raw:: html

   <span class="fa fa-plus"></span>
   
.. |fa-eye| raw:: html

   <span class="fa fa-eye"></span>
   
.. |fa-dashboard| raw:: html

   <span class="fa fa-dashboard"></span>

.. |fa-download| raw:: html

   <span class="fa fa-download"></span>

.. |fa-upload| raw:: html

   <span class="fa fa-upload"></span>

.. |fa-bar-chart| raw:: html

   <span class="fa fa-bar-chart"></span>

.. |fa-calendar| raw:: html

   <span class="fa fa-calendar"></span>

.. |fa-home| raw:: html

   <span class="fa fa-home"></span>

.. |fa-table| raw:: html

   <span class="fa fa-table"></span>

.. |fa-comments| raw:: html

   <span class="fa fa-comments"></span>

.. |fa-rocket| raw:: html

   <span class="fa fa-rocket"></span>

.. |fa-link| raw:: html

   <span class="fa fa-link"></span>

.. |fa-file-archive-o| raw:: html

   <span class="fa fa-file-archive-o"></span>

.. |fa-floppy-o| raw:: html

   <span class="fa fa-floppy-o"></span>

.. |fa-check| raw:: html

   <span class="fa fa-check"></span>

.. |fa-cog| raw:: html

   <span class="fa fa-cog"></span>

.. |fa-compress| raw:: html

   <span class="fa fa-compress"></span>

.. |fa-step-forward| raw:: html

   <span class="fa fa-step-forward"></span>

.. |fa-step-backward| raw:: html

   <span class="fa fa-step-backward"></span>

.. |fa-user| raw:: html

   <span class="fa fa-user"></span>

.. |fa-database| raw:: html

   <span class="fa fa-database"></span>

.. |fa-cogs| raw:: html

   <span class="fa fa-cogs"></span>
"""

def setup(app):
    app.add_stylesheet('css/custom.css')  # may also be an URL
    app.add_stylesheet(
        "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
    )
