"""Check for a bug in parsing comments after definitions."""

from .expected import Expectation

expectation = Expectation()
expect = expectation.expect


def should_be_ok():
    """Just a function without violations."""


# This is a comment that triggers a bug that causes the previous function
# to generate a D202 error.
