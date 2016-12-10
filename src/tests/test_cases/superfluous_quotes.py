"""A valid module docstring."""

from .expected import Expectation

expectation = Expectation()
expect = expectation.expect


def correct_func():
    """Three quotes in both sides."""


@expect('D300: Use """triple double quotes""" (found """"-quotes)')
def extra_opening():
    """"Extra quote on the left."""


@expect('D300: Use """triple double quotes""" (found """""-quotes)')
def two_extra_opening():
    """""Two extra quotes on the left."""
