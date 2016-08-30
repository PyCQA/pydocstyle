``pydocstyle`` inline commenting to skip specific checks on specific
functions or methods. The supported comments that can be added are:

1. ``"# noqa"`` or ``"# pydocstyle: noqa"`` skips all checks.

2. ``"# pydocstyle: D102,D203"`` can be used to skip specific checks.

For example, this will skip the check for a period at the end of a function
docstring::

    >>> def bad_function():  # pydocstyle: D400
    ...     """Omit a period in the docstring as an exception"""
    ...     pass
