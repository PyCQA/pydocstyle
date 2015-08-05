Release Notes
=============


Current Development Version
---------------------------

New Features

* Added the D104 error code - "Missing docstring in public package". This new
  error is turned on by default. Missing docstring in `__init__.py` files which
  previously resulted in D100 errors ("Missing docstring in public module")
  will now result in D104 (#105, #127).


0.6.0 - July 20th, 2015
---------------------------

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
