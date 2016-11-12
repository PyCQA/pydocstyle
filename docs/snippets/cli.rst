.. _cli_usage:

Usage
^^^^^

.. highlight:: none

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
      --format=<format>     override default error format (ignores --explain and
                            --source)
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


Error format
^^^^^^^^^^^^

The ``--format`` option allows to override the default error format, which
controls how each error found is printed to the standard output. The error
format uses the standard Python :ref:`format string syntax <formatstrings>` and
can include the following placeholders:

``code``
    the error code, e.g. D101, D304, etc.
``definition``
    the type and name of the code section where the error occured
``explanation``
    an explanation of the rule the error violated
``filename``
    the path of the file in which the error occured
``line``
    the line number at which the error occured
``lines``
    the source code which exhibits the error
``message``
    the ``short_desc`` prefixed by ``code`` and a colon and followed by
    additional error context, e.g. "D401: First line should be in imperative
    mood ('Return', not 'Returns')"
``short_desc``
    the error message corresponding to the error code, e.g., for D103,
    "Missing docstring in public function"

The default error format, if neither the ``--format`` nor the ``--explain`` or
``--source`` options are given, is ``'{filename}:{line} {definition}:\n
{message}'``.


Example usage
#############

Consider the following usage:

.. code:: console

    $ pydocstyle --format='{filename}#L{line:03}: {short_desc} ({code})' src/example.py

This would output output each error formatted like the following example:

.. code::

    src/example.py#L001: Missing docstring in public module (D100)

If you want to use a format string, which includes line-breaks or other
non-printable characters, you might have to do some shell trickery to pass it
correctly:

.. code:: console

    $ FMT=$(echo -e '\nFile:\t{filename}:{line}\nWhere:\t{definition}\nWhat:\t{message}')
    $ pydocstyle --format="$FMT" src/example.py

    File:	src/example.py:16
    Where:	in public function `main`
    What:	D103: Missing docstring in public function


.. highlight:: python


Return Code
^^^^^^^^^^^

+--------------+--------------------------------------------------------------+
| 0            | Success - no violations                                      |
+--------------+--------------------------------------------------------------+
| 1            | Some code violations were found                              |
+--------------+--------------------------------------------------------------+
| 2            | Illegal usage - see error message                            |
+--------------+--------------------------------------------------------------+
