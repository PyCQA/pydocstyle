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


Links
-----

.. image:: https://travis-ci.org/GreenSteam/pep257.svg?branch=master
    :target: https://travis-ci.org/GreenSteam/pep257

.. image:: https://readthedocs.org/projects/pep257/badge/?version=latest
    :target: https://readthedocs.org/projects/pep257/?badge=latest
    :alt: Documentation Status

* `Read the full documentation here <http://pep257.readthedocs.org>`_.

* `Fork pep257 on GitHub <http://github.com/GreenSteam/pep257>`_.

* `PyPI project page <https://pypi.python.org/pypi/pep257>`_.
