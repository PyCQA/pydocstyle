.. _cli_usage:

Usage
^^^^^

.. code::

    Usage: pydocstyle [options] [<file|dir>...]

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -e, --explain         show explanation of each error
      -s, --source          show source for each error
      -d, --debug           print debug information
      -v, --verbose         print status information
      --count               print total number of errors to stdout
      --select=<codes>      choose the basic list of checked errors by specifying
                            which errors to check for (with a list of comma-
                            separated error codes or prefixes). for example:
                            --select=D101,D2
      --ignore=<codes>      choose the basic list of checked errors by specifying
                            which errors to ignore (with a list of comma-separated
                            error codes or prefixes). for example:
                            --ignore=D101,D2
      --convention=<name>   choose the basic list of checked errors by specifying
                            an existing convention. Possible conventions: pep257
      --add-select=<codes>  amend the list of errors to check for by specifying
                            more error codes to check.
      --add-ignore=<codes>  amend the list of errors to check for by specifying
                            more error codes to ignore.
      --match=<pattern>     check only files that exactly match <pattern> regular
                            expression; default is --match='(?!test_).*\.py' which
                            matches files that don't start with 'test_' but end
                            with '.py'
      --match-dir=<pattern>
                            search only dirs that exactly match <pattern> regular
                            expression; default is --match-dir='[^\.].*', which
                            matches all dirs that don't start with a dot
      --ignore-decorators=<decorators>
                            ignore any functions or methods that are decorated by
                            a function with a name fitting the <decorators>
                            regular expression; default is --ignore-decorators=''
                            which does not ignore any decorated functions.

.. note::

    When using any of the ``--select``, ``--ignore``, ``--add-select``, or
    ``--add-ignore`` command line flags, it is possible to pass a prefix for an
    error code. It will be expanded so that any code begining with that prefix
    will match. For example, running the command ``pydocstyle --ignore=D4``
    will ignore all docstring content issues as their error codes begining with
    "D4" (i.e. D400, D401, D402, D403, and D404).

Return Code
^^^^^^^^^^^

+--------------+--------------------------------------------------------------+
| 0            | Success - no violations                                      |
+--------------+--------------------------------------------------------------+
| 1            | Some code violations were found                              |
+--------------+--------------------------------------------------------------+
| 2            | Illegal usage - see error message                            |
+--------------+--------------------------------------------------------------+
