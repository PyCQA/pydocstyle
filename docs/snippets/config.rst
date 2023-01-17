``pydocstyle`` supports *ini*-like and *toml* configuration files.
In order for ``pydocstyle`` to use a configuration file automatically, it must
be named one of the following options.

* ``setup.cfg``
* ``tox.ini``
* ``.pydocstyle``
* ``.pydocstyle.ini``
* ``.pydocstylerc``
* ``.pydocstylerc.ini``
* ``pyproject.toml``

When searching for a configuration file, ``pydocstyle`` looks for one of the
file specified above *in that exact order*. *ini*-like configuration files must
have a ``[pydocstyle]`` section while *toml* configuration files must have a
``[tool.pydocstyle]`` section. If a configuration file was not found,
``pydocstyle`` keeps looking for one up the directory tree until one is found
or uses the default configuration.

.. note::

    *toml* configuration file support is only enabled if the ``toml`` python
    package is installed. You can ensure that this is the case by installing
    the ``pydocstyle[toml]`` optional dependency.

.. note::

    For backwards compatibility purposes, **pydocstyle** supports configuration
    files named ``.pep257``, as well as section header ``[pep257]``. However,
    these are considered deprecated and support will be removed in the next
    major version.

Available Options
#################

Not all configuration options are available in the configuration files.
Available options are:

* ``convention``
* ``select``
* ``ignore``
* ``add_select``
* ``add_ignore``
* ``match``
* ``match_dir``
* ``ignore_decorators``
* ``property_decorators``
* ``ignore_self_only_init``

See the :ref:`cli_usage` section for more information.

Inheritance
###########

By default, when finding a configuration file, ``pydocstyle`` tries to inherit
the parent directory's configuration and merge them to the local ones.

The merge process is as follows:

* If one of ``select``, ``ignore`` or ``convention`` was specified in the child
  configuration - Ignores the parent configuration and set the new error codes
  to check. Otherwise, simply copies the parent checked error codes.
* If ``add-ignore`` or ``add-select`` were specified, adds or removes the
  specified error codes from the checked error codes list.
* If ``match`` or ``match-dir`` were specified - use them. Otherwise, use the
  parent's.

In order to disable this (useful for configuration files located in your repo's
root), simply add ``inherit=false`` to your configuration file.


.. note::

  If any of ``select``, ``ignore`` or ``convention`` were specified in
  the CLI, the configuration files will take no part in choosing which error
  codes will be checked. ``match`` and ``match-dir`` will still take effect.

Example
#######

.. code::

    [pydocstyle]
    inherit = false
    ignore = D100,D203,D405
    match = .*\.py

