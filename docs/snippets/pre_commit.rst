**pydocstyle** can be included as a hook for `pre-commit`_.  The easiest way to get
started is to add this configuration to your ``.pre-commit-config.yaml``:

.. parsed-literal::

    -   repo: https://github.com/pycqa/pydocstyle
        rev: \ |version| \  # pick a git hash / tag to point to
        hooks:
        -   id: pydocstyle

See the `pre-commit docs`_ for how to customize this configuration.

Checked-in python files will be passed as positional arguments so no need to use ``--match=*.py``.
You can also use command line arguments instead of configuration files
to achieve the same effect with less files.

.. code-block:: yaml

    - id: pydocstyle
      args:
      - --ignore=D100,D203,D405
      # or multiline
      - |-
              --select=
              D101,
              D2

.. _pre-commit:
    https://pre-commit.com/
.. _pre-commit docs:
    https://pre-commit.com/#pre-commit-configyaml---hooks
