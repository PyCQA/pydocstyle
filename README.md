PEP 257 docstring style checker
===============================================================================

**pep257** is a static analysis tool for checking compliance with
Python PEP 257: <http://www.python.org/dev/peps/pep-0257/>.

The framework for checking docstring style is flexible, and custom checks
can be easily added, for example to cover NumPy docstring conventions:
<https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt>.

Adding new checks is described in docstring of pep257.py file.

Installation
-------------------------------------------------------------------------------

Use [pip](http://pip-installer.org) or easy_install:

    pip install pep257

Alternatively, you can use `pep257.py` source file directly--it is
self-contained.

**pep257** is tested with Python 2.5, 2.6, 2.7, 3.2, 3.3

Example
-------------------------------------------------------------------------------

```bash
$ pep257 --help
Usage: pep257 [options]

Options:
  -h, --help     show this help message and exit
  -e, --explain  show explanation of each error
  -r, --range    show error start..end positions
  -q, --quote    quote erroneous lines

$ pep257 *.py
docopt.py:1:0: PEP257 Modules should have docstrings.
docopt.py:14:4: PEP257 Class docstring should have 1 blank line around them.
docopt.py:27:0: PEP257 Exported classes should have docstrings.
docopt.py:43:4: PEP257 Exported definitions should have docstrings.
...

$ pep257 *.py --explain
docopt.py:1:0: PEP257 Modules should have docstrings.
PEP257 Modules should have docstrings.

    All modules should normally have docstrings.

docopt.py:14:4: PEP257 Class docstring should have 1 blank line around them.
PEP257 Class docstring should have 1 blank line around them.

    Insert a blank line before and after all docstrings (one-line or
    multi-line) that document a class -- generally speaking, the class's
    methods are separated from each other by a single blank line, and the
    docstring needs to be offset from the first method by a blank line;
    for symmetry, put a blank line between the class header and the
    docstring.

...

$ pep257 --quote *.py
docopt.py:1:0: PEP257 Modules should have docstrings.
    import sys
    import re


    # Python 3 Compatibility
    try:
        basestring
    except NameError:
docopt.py:14:4: PEP257 Class docstring should have 1 blank line around them.
    """Error in construction of usage-message."""
docopt.py:27:0: PEP257 Exported classes should have docstrings.
    class Pattern(object):
docopt.py:43:4: PEP257 Exported definitions should have docstrings.
    def flat(self):
...
```

Python API
-------------------------------------------------------------------------------

**pep257** Python API is useful when you want to include PEP 257 checks into
your test-suite.

```python
>>> import pep257
>>> pep257.check_files(['one.py', 'two.py'])
['one.py:23:1 PEP257 Use u\"\"\" for Unicode docstrings.']
```

A [pytest](http://pytest.org/)-style test can look like this:

```python
import pep257

test_pep257():
    errors = pep257.check_files(['one.py', 'two.py'])
    assert len(errors) == 0
```

Errors
-------------------------------------------------------------------------------

All **pep257** errors have unique codes. All codes start with a capital D and
are grouped as follows:

| Code | Group                                                                |
|------|----------------------------------------------------------------------|
| D1xx | Missing docstrings                                                   |
| D2xx | Whitespace issues                                                    |
| D3xx | Docstring formatting                                                 |
| D4xx | Docstring content issues                                             |



| Code | Explanation                                                          |
|------|----------------------------------------------------------------------|
| D100 | All modules should have docstrings.                                  |
| D101 | Exported definitions should have docstrings.                         |
| D102 | Exported classes should have docstrings                              |
| D200 | One-line docstrings should fit on one line with quotes.              |
| D201 | No blank line before docstring in definitions.                       |
| D202 | Blank line missing after one-line summary.                           |
| D203 | The entire docstring should be indented same as code.                |
| D204 | Class docstring should have 1 blank line around them.                |
| D205 | Multiline docstring should end with 1 blank line.                    |
| D300 | Use """triple double quotes""".                                      |
| D301 | Use r""" if any backslashes in your docstring.                       |
| D302 | Use u""" for Unicode docstrings.                                     |
| D400 | First line should end with a period.                                 |
| D401 | First line should be in imperative mood.                             |
| D402 | First line should not be the function's or method's "signature".     |
| D403 | Return value type should be mentioned.                               |
