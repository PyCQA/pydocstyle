Usage
=====

Installation
------------

.. include:: snippets/install.rst


Command Line Interface
----------------------

.. include:: snippets/cli.rst

``--format`` supports the following keywords for replacement: ``filename``,
``line``, ``definition``, ``message``, ``explanation``, and ``lines``. For
example:

.. code::
    %(filename)s:%(line)3d: %(definition)s: %(message)s

Configuration Files
^^^^^^^^^^^^^^^^^^^

.. include:: snippets/config.rst
