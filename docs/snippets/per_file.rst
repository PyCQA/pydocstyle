``pydocstyle`` supports inline commenting to skip specific checks on
specific functions or methods. The supported comments that can be added are:

1. ``"# noqa"`` skips all checks.

2. ``"# noqa: D102,D203"`` can be used to skip specific checks. Note that
   this is compatible with skips from `flake8 <http://flake8.pycqa.org/>`_,
   e.g. ``# noqa: D102,E501,D203``.

For example, this will skip the check for a period at the end of a function
docstring::

    >>> def bad_function():  # noqa: D400
    ...     """Omit a period in the docstring as an exception"""
    ...     pass
