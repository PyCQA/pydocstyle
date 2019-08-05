Error Codes
===========

Grouping
--------

.. include:: snippets/error_code_table.rst

Default conventions
-------------------

Not all error codes are checked for by default.

The ``pep257`` convention, which is enabled by default in pydocstyle,
checks for all of the above errors except for D203, D212, D213, D214,
D215, D404, D405, D406, D407, D408, D409, D410, and D411 (as specified
in `PEP257 <http://www.python.org/dev/peps/pep-0257/>`_).

The ``numpy`` convention added in v2.0.0 supports the `numpydoc docstring
<https://github.com/numpy/numpydoc>`_ standard. This checks all of of the
errors except for D107, D203, D212, D213, D402, D413, D415, D416, and D417.

The ``google`` convention added in v4.0.0 supports the `Google Python Style
Guide <https://google.github.io/styleguide/pyguide.html>`_. This checks for
all the errors except D203, D204, D213, D215, D400, D401, D404, D406, D407,
D408, D409.

These conventions may be specified using `--convention=<name>` when
running pydocstyle from the command line or by specifying the
convention in a configuration file.  See the :ref:`cli_usage` section
for more details.

Publicity
---------

.. include:: snippets/publicity.rst
