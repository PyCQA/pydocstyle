``pep257`` looks for a config file in the root of the project (the common
prefix of all checked files) and goes up in the directory tree until it finds
one of the following files (in this order):

* ``setup.cfg``
* ``tox.ini``
* ``.pep257``

The first found file is read, and configurations in the ``[pep257]`` section
are used, if such a section exists.

Example
#######

.. code::

    [pep257]
    verbose = true
    ignore = D100,D203,D405
    explain = true

