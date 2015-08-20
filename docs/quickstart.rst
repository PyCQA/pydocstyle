Quick Start
===========

1. Install

    .. code::

        pip install pep257

2. Run

    On Linux/Mac:
    .. code::

        $ pep257 test.py
        test.py:18 in private nested class `meta`:
                D101: Docstring missing
        test.py:22 in public method `method`:
                D102: Docstring missing
        ...

    On Windows:
    .. code::
    
        py -m pep257 test.py
        test.py:18 in private nested class `meta`:
                D101: Docstring missing
        test.py:22 in public method `method`:
                D102: Docstring missing
        ...

    Note: If you are on Windows and have more than one
    Python Environment, e.g. Python 2 and 3, you must run 
    .. code::
    
        py -2 -m pep257 test.py

    for use in Python 2, or
    .. code::
    
        py -3 -m pep257 test.py

    for us in Python 3
3. Fix your code :)

