Release Notes
=============

**pydocstyle** version numbers follow the
`Semantic Versioning <http://semver.org/>`_ specification.

Current development version
---------------------------

Major Updates

* Support for Python 3.3 has been dropped (#315, #316).

New features

* Violations are now reported on the line where the docstring starts, not the
  line of the ``def``/``class`` it corresponds to (#238, #83).
* Updated description of pep257 and numpy conventions (#300).
* Added support for Python 3.7 (#324).

Bug Fixes

* Fixed a false-positive recognition of section names causing D405 to be
  reported (#311, #317).


2.1.1 - October 9th, 2017
-------------------------

Bug Fixes

* Changed wheel configuration to be NOT universal, as #281 added
  ``configparser`` as a dependency for Python 2.7.
* Updated usage documentation.


2.1.0 - October 8th, 2017
-------------------------

New Features

* Public nested classes missing a docstring are now reported as D106 instead
  of D101 (#198, #261).
* ``__init__`` methods missing a docstring are now reported as D107 instead of
  D102 (#273, #277).
* Added support for Python 3.6 (#270).
* Specifying an invalid error code prefix (e.g., ``--select=D9``) will print
  a warning message to ``stderr`` (#253, #279).
* Configuration files now support multiple-lined entries (#250, #281).
* Improved description of how error selection works in the help section
  (#231, #283).

Bug Fixes

* Fixed an issue where the ``--source`` flag would result in improperly
  spaced output (#256, #257, #260).
* Fixed an issue where if a first word in a docstring had Unicode characters
  and the docstring was not a unicode string, an exception would be raised
  (#258, #264).
* Configuration files that were specified by CLI and don't contain a valid
  section name will now issue a warning to ``stderr`` (#276, #280).
* Removed D107 from the numpy convention (#288).


2.0.0 - April 18th, 2017
------------------------

Major Updates

* Support for ``numpy`` conventions verification has been added (#129, #226).
* Support for Python 2.6 has been dropped (#206, #217).
* Support for PyPy3 has been temporarily dropped, until it will be
  equivalent to CPython 3.3+ and supported by ``pip`` (#223).
* Support for the ``pep257`` console script has been dropped. Only the
  ``pydocstyle`` console script should be used (#216, #218).
* Errors are now printed to ``stdout`` instead of ``stderr`` (#201, #210).

New Features

* Decorator-based skipping via ``--ignore-decorators`` has been added (#204).
* Support for using pycodestyle style wildcards has been added (#72, #209).
* Superfluous opening quotes are now reported as part of D300 (#166, #225).
* Fixed a false-positive recognition of `D410` and added `D412` (#230, #233).
* Added ``--config=<path>`` flag to override the normal config file discovery
  and choose a specific config file (#117, #247).
* Support for specifying error codes with partial prefix has been added, e.g.,
  ``--select=D101,D2`` (#72, #209).
* All configuration file can now have the ``.ini`` extension (#237).
* Added better imperative mood checks using third party stemmer (#235, #68).

Bug Fixes

* Made parser more robust to bad source files (#168, #214)
* Modules are now considered private if their name starts with a single
  underscore. This is a bugfix where "public module" (D100) was reported
  regardless of module name (#199, #222).
* Removed error when ``__all__`` is a list (#62, #227).
* Fixed a bug where the ``@`` sign was used as a matrix multiplication operator
  in Python 3.5, but was considered a decorator by the parser (#246, #191).


1.1.1 - October 4th, 2016
-------------------------

Bug Fixes

* Fixed an issue where the ``flake8-docstrings`` failed when accessing some
  public API from ``pydocstyle``.


1.1.0 - September 29th, 2016
----------------------------

Major Updates

* ``pydocstyle`` is no longer a single file. This might make it difficult for
  some users to just add it to their project, but the project has reached
  certain complexity where splitting it into modules was necessary (#200).

New Features

* Added the optional error codes D212 and D213, for checking whether
  the summary of a multi-line docstring starts at the first line,
  respectively at the second line (#174).

* Added D404 - First word of the docstring should not be "This". It is turned
  off by default (#183).

* Added the ability to ignore specific function and method docstrings with
  inline comments:

    1. "# noqa" skips all checks.

    2. "# noqa: D102,D203" can be used to skip specific checks.

Bug Fixes

* Fixed an issue where file paths were printed in lower case (#179, #181).

* The error code D300 is now also being reported if a docstring has
  uppercase literals (``R`` or ``U``) as prefix (#176).

* Fixed a bug where an ``__all__`` error was reported when ``__all__`` was
  imported from another module with a different name (#182, #187).

* Fixed a bug where ``raise X from Y`` syntax caused ``pydocstyle`` to crash
  (#196, #200).

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
