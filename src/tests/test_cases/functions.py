""" Function docstrings """

from .expected import Expectation

expectation = Expectation()
expect = expectation.expect


@expect("D201: No blank lines allowed before docstring")
def func_with_space_before():

    """Func with space before."""
    pass


@expect("D202: No blank lines allowed after docstring")
def func_with_space_after():
    """Func with space after."""

    pass


def func_with_inner_func_after():
    """Func with inner after."""

    def inner():
        pass

    pass
