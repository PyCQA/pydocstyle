pydocstyle - docstring style checker
====================================

(formerly pep257)

**pydocstyle** is a static analysis tool for checking compliance with Python
docstring conventions.

**pydocstyle** supports most of
`PEP 257 <http://www.python.org/dev/peps/pep-0257/>`_ out of the box, but it
should not be considered a reference implementation.

The framework for checking docstring style is flexible, and
custom checks can be easily added, for example to cover
NumPy `docstring conventions
<https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt>`_.

**pydocstyle** supports Python 2.6, 2.7, 3.3, 3.4, 3.5, pypy and pypy3.

Quick Start
-----------

Install
^^^^^^^

.. code::

    pip install pydocstyle

Run
^^^

.. code::

    $ pydocstyle test.py
    test.py:18 in private nested class `meta`:
            D101: Docstring missing
    test.py:22 in public method `method`:
            D102: Docstring missing
    ...


Links
-----

.. image:: https://travis-ci.org/PyCQA/pydocstyle.svg?branch=master
    :target: https://travis-ci.org/PyCQA/pydocstyle

.. image:: https://readthedocs.org/projects/pydocstyle/badge/?version=latest
    :target: https://readthedocs.org/projects/pydocstyle/?badge=latest
    :alt: Documentation Status

* `Read the full documentation here <http://pydocstyle.readthedocs.org>`_.

* `Fork pydocstyle on GitHub <http://github.com/PyCQA/pydocstyle>`_.

* `PyPI project page <https://pypi.python.org/pypi/pydocstyle>`_.
