# noqa: D400,D415
"""Test case for "# noqa" comments"""
from .expected import Expectation


expectation = Expectation()
expect = expectation.expect


def docstring_bad_ignore_all():  # noqa
    """Runs something"""
    pass


def docstring_bad_ignore_one():  # noqa: D400,D401,D415
    """Runs something"""
    pass


@expect("D401: First line should be in imperative mood "
        "(perhaps 'Run', not 'Runs')")
def docstring_ignore_some_violations_but_catch_D401():  # noqa: E501,D400,D415
    """Runs something"""
    pass
