PEP 257 docstring style checker
===========================================================

**pep257** is a static analysis tool for checking
compliance with Python `PEP 257
<http://www.python.org/dev/peps/pep-0257/>`_.

The framework for checking docstring style is flexible, and
custom checks can be easily added, for example to cover
NumPy `docstring conventions
<https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt>`_.

**pep257** supports Python 2.6, 2.7, 3.2, 3.3, 3.4, pypy and pypy3.

Quick Start
-----------

Install
^^^^^^^

.. code::

    pip install pep257

Run
^^^

.. code::

    $ pep257 test.py
    test.py:18 in private nested class `meta`:
            D101: Docstring missing
    test.py:22 in public method `method`:
            D102: Docstring missing
    ...


`Read the full documentation here <http://pep257.readthedocs.org>`_.

