Usage
^^^^^

.. code::

    Usage: pep257 [options] [<file|dir>...]

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -e, --explain         show explanation of each error
      -s, --source          show source for each error
      --select=<codes>      choose the basic list of checked errors by specifying
                            which errors to check for (with a list of comma-
                            separated error codes). for example:
                            --select=D101,D202
      --ignore=<codes>      choose the basic list of checked errors by specifying
                            which errors to ignore (with a list of comma-separated
                            error codes). for example: --ignore=D101,D202
      --convention=<name>   choose the basic list of checked errors by specifying
                            an existing convention. for example:
                            --convention=pep257
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
      -d, --debug           print debug information
      -v, --verbose         print status information
      --count               print total number of errors to stdout

Return Code
^^^^^^^^^^^

+--------------+--------------------------------------------------------------+
| 0            | Success - no violations                                      |
+--------------+--------------------------------------------------------------+
| 1            | Some code violations were found                              |
+--------------+--------------------------------------------------------------+
| 2            | Illegal usage - see error message                            |
+--------------+--------------------------------------------------------------+
