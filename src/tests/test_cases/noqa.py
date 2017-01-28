"""Test case for "# noqa" comments."""
from .expected import Expectation


expectation = Expectation()
expect = expectation.expect


def docstring_bad_ignore_all():  # noqa
    """Runs something"""
    pass


def docstring_bad_ignore_one():  # noqa: D400,D401
    """Runs something"""
    pass


@expect("D401: First line should be in imperative mood ('Run', not 'Runs')")
def docstring_ignore_violations_of_pydocstyle_D400_and_PEP8_E501_but_catch_D401():  # noqa: E501,D400
    """Runs something"""
    pass
