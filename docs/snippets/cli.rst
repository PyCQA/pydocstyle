Usage
^^^^^

.. code::

    Usage: pep257 [options] [<file|dir>...]

    Options:
    --version             show program's version number and exit
    -h, --help            show this help message and exit
    -e, --explain         show explanation of each error
    -s, --source          show source for each error
    --ignore=<codes>      ignore a list comma-separated error codes, for
                            example: --ignore=D101,D202
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

