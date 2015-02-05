Release Notes
=============


Current Development Version
--------------------------

New Features

* Added check D210: No whitespaces allowed surrounding docstring text (#95)

Bug Fixes

* Removed log level configuration from module level (#98)


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

* Added a `--count` flag that prints the number of violations found (#86, #89).

* Added support for Python 3.4, PyPy and PyPy3 (#81).

Bug Fixes

* Fixed broken tests (#74).

* Fixed parsing various colon and parenthesis combinations in definitions
  (#82).

* Allow for greater flexibility in parsing __all__ (#67).

* Fixed handling of one-liner definitions (#77).


0.3.2 - March 11th, 2014
------------------------

First documented release!

