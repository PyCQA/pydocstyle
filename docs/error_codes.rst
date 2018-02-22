Error Codes
===========

Grouping
--------

.. include:: snippets/error_code_table.rst

Default conventions
-------------------

Not all error codes are checked for by default.  There are two
conventions that may be used by pydocstyle: pep257 and numpy.

The pep257 convention, which is enabled by default in pydocstyle,
checks for all of the above errors except for D203, D212, D213, D214,
D215, D404, D405, D406, D407, D408, D409, D410, and D411 (as specified
in `PEP257 <http://www.python.org/dev/peps/pep-0257/>`_).

The numpy convention checks for all of the above errors except for
D107, D203, D212, D213, D402, and D413.

These conventions may be specified using `--convention=<name>` when
running pydocstyle from the command line or by specifying the
convention in a configuration file.  See the :ref:`cli_usage` section
for more details.

Publicity
---------

.. include:: snippets/publicity.rst
