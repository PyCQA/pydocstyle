Contributing
===============================================================================

Feel free to issue pull requests for code, or documentation, proposals.
If you are unsure if a feature is a good fit, you can always [create an
issue](https://github.com/GreenSteam/pep257/issues/new).

Executing tests
-------------------------------------------------------------------------------
To execute tests for your current Python environment you, issue

    python setup.py test

. To execute tests for all the Python enviroments that `pep257.py` is
supposed to support:

1. Install the Python application [tox](https://pypi.python.org/pypi/tox).
2. Invoke `tox` on the command line.

In case you are not sure you tested everything correct, a full test
suite will always be executed for every pull request. ;-)
