"""A valid module docstrings."""

from .expected import Expectation

expectation = Expectation()
expect = expectation.expect


@expect("D201: No blank lines allowed before function docstring (found 1)")
def func_with_space_before():

    """Test a function with space before docstring."""
    pass


@expect("D202: No blank lines allowed after function docstring (found 1)")
def func_with_space_after():
    """Test a function with space after docstring."""

    pass


@expect()
def func_with_inner_func_after():
    """Test a function with inner function after docstring."""

    @expect("D193: Missing docstring in private function")
    def inner_func():
        pass

    pass



@expect()
def func_with_inner_async_func_after():
    """Test a function with inner async function after docstring."""

    @expect("D193: Missing docstring in private function")
    async def inner_async_func():
        pass

    pass


def fake_decorator(decorated):
    """Fake decorator used to test decorated inner func."""
    return decorated


@expect()
def func_with_inner_decorated_func_after():
    """Test a function with inner decorated function after docstring."""

    @fake_decorator
    @expect("D193: Missing docstring in private function")
    def inner_decorated_func():
        pass

    pass




@expect()
def func_with_inner_decorated_async_func_after():
    """Test a function with inner decorated async function after docstring."""

    @fake_decorator
    @expect("D193: Missing docstring in private function")
    async def inner_decorated_async_func():
        pass

    pass



@expect()
def func_with_inner_class_after():
    """Test a function with inner class after docstring."""
    expect("inner_class", "D196: Missing docstring in private nested class")

    class inner_class():
        pass

    pass


def func_with_weird_backslash():
    """Test a function with a weird backslash.\
"""
