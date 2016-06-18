Release Notes
=============

**pydocstyle** version numbers follow the
`Semantic Versioning <http://semver.org/>`_ specification.

Current Development Version
---------------------------

New Features

* Added the optional error codes D212 and D213, for checking whether
  the summary of a multi-line docstring starts at the first line,
  respectively at the second line (#174).

* Added D404 - First word of the docstring should not be "This". It is turned
  off by default (#183).

Bug Fixes

* The error code D300 is now also being reported if a docstring has
  uppercase literals (``R`` or ``U``) as prefix (#176).

* Fixed a bug where an ``__all__`` error was reported when ``__all__`` was
  imported from another module with a different name (#182, #187).

1.0.0 - January 30th, 2016
--------------------------

Major Updates

* The project was renamed to **pydocstyle** and the new release will be 1.0.0!

New Features

* Added support for Python 3.5 (#145).

* Classes nested inside classes are no longer considered private. Nested
  classes are considered public if their names are not prepended with an
  underscore and if their parent class is public, recursively (#13, #146).

* Added the D403 error code - "First word of the first line should be
  properly capitalized". This new error is turned on by default (#164, #165,
  #170).

* Added support for ``.pydocstylerc`` and as configuration file name
  (#140, #173).

Bug Fixes

* Fixed an issue where a ``NameError`` was raised when parsing complex
  definitions of ``__all__`` (#142, #143).

* Fixed a bug where D202 was falsely reported when a function with just a
  docstring and no content was followed by a comment (#165).

* Fixed wrong ``__all__`` definition in main module (#150, #156).

* Fixed a bug where an ``AssertionError`` could occur when parsing
  ``__future__`` imports (#154).


Older Versions
==============

.. note::

    Versions documented below are before renaming the project from **pep257**
    to **pydocstyle**.


0.7.0 - October 9th, 2015
-------------------------

New Features

* Added the D104 error code - "Missing docstring in public package". This new
  error is turned on by default. Missing docstring in ``__init__.py`` files which
  previously resulted in D100 errors ("Missing docstring in public module")
  will now result in D104 (#105, #127).

* Added the D105 error code - "Missing docstring in magic method'. This new
  error is turned on by default. Missing docstrings in magic method which
  previously resulted in D102 error ("Missing docstring in public method")
  will now result in D105. Note that exceptions to this rule are variadic
  magic methods - specifically ``__init__``, ``__call__`` and ``__new__``, which
  will be considered non-magic and missing docstrings in them will result
  in D102 (#60, #139).

* Support the option to exclude all error codes. Running pep257 with
  ``--select=`` (or ``select=`` in the configuration file) will exclude all errors
  which could then be added one by one using ``add-select``. Useful for projects
  new to pep257 (#132, #135).

* Added check D211: No blank lines allowed before class docstring. This change
  is a result of a change to the official PEP257 convention. Therefore, D211
  will now be checked by default instead of D203, which required a single
  blank line before a class docstring (#137).

* Configuration files are now handled correctly. The closer a configuration file
  is to a checked file the more it matters.
  Configuration files no longer support ``explain``, ``source``, ``debug``,
  ``verbose`` or ``count`` (#133).

Bug Fixes

* On Python 2.x, D302 ("Use u""" for Unicode docstrings") is not reported
  if `unicode_literals` is imported from `__future__` (#113, #134).

* Fixed a bug where there was no executable for `pep257` on Windows (#73,
  #136).


0.6.0 - July 20th, 2015
-----------------------

New Features

* Added support for more flexible error selections using ``--ignore``,
  ``--select``, ``--convention``, ``--add-ignore`` and ``--add-select``
  (#96, #123).

Bug Fixes

* Property setter and deleter methods are now treated as private and do not
  require docstrings separate from the main property method (#69, #107).

* Fixed an issue where pep257 did not accept docstrings that are both
  unicode and raw in Python 2.x (#116, #119).

* Fixed an issue where Python 3.x files with Unicode encodings were
  not read correctly (#118).


0.5.0 - March 14th, 2015
------------------------

New Features

* Added check D210: No whitespaces allowed surrounding docstring text (#95).

* Added real documentation rendering using Sphinx (#100, #101).

Bug Fixes

* Removed log level configuration from module level (#98).

* D205 used to check that there was *a* blank line between the one line summary
  and the description. It now checks that there is *exactly* one blank line
  between them (#79).

* Fixed a bug where ``--match-dir`` was not properly respected (#108, #109).

0.4.1 - January 10th, 2015
--------------------------

Bug Fixes

* Getting ``ImportError`` when trying to run pep257 as the installed script
  (#92, #93).


0.4.0 - January 4th, 2015
-------------------------

.. warning::

    A fatal bug was discovered in this version (#92). Please use a newer
    version.

New Features

* Added configuration file support (#58, #87).

* Added a ``--count`` flag that prints the number of violations found (#86,
  #89).

* Added support for Python 3.4, PyPy and PyPy3 (#81).

Bug Fixes

* Fixed broken tests (#74).

* Fixed parsing various colon and parenthesis combinations in definitions
  (#82).

* Allow for greater flexibility in parsing ``__all__`` (#67).

* Fixed handling of one-liner definitions (#77).


0.3.2 - March 11th, 2014
------------------------

First documented release!
