"""Pytest utilities."""
from pydocstyle.parser import Module


def pytest_assertrepr_compare(op, left, right):
    """Add rich comparison in pytest tests for `Module` objects."""
    if isinstance(left, Module) and isinstance(right, Module) and op == "==":
        result = ["Comparing modules"]

        for f in Module._fields:
            left_f = getattr(left, f)
            right_f = getattr(right, f)
            if left_f != right_f:
                result.append("{}: {!r} != {!r}".format(f, left_f, right_f))

        return result
