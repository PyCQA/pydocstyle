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


def func_with_inner_func_after():
    """Test a function with inner function after docstring."""

    def public_inner():
        pass

    def _private_inner():
        pass

    pass

expect("public_inner", "D123: Missing docstring in inaccessible public function")
expect("_private_inner", "D173: Missing docstring in inaccessible private function")


def func_with_inner_async_func_after():
    """Test a function with inner async function after docstring."""

    async def public_inner_async():
        pass

    async def _private_inner_async():
        pass

    pass

expect("public_inner_async", "D123: Missing docstring in inaccessible public function")
expect("_private_inner_async", "D173: Missing docstring in inaccessible private function")


def fake_decorator(decorated):
    """Fake decorator used to test decorated inner func."""
    return decorated


def func_with_inner_decorated_func_after():
    """Test a function with inner decorated function after docstring."""

    @fake_decorator
    def public_inner_decorated():
        pass

    @fake_decorator
    def _private_inner_decorated():
        pass

    pass

expect("public_inner_decorated", "D123: Missing docstring in inaccessible public function")
expect("_private_inner_decorated", "D173: Missing docstring in inaccessible private function")


def func_with_inner_decorated_async_func_after():
    """Test a function with inner decorated async function after docstring."""

    @fake_decorator
    async def public_inner_decorated_async():
        pass

    @fake_decorator
    async def _prviate_inner_decorated_async():
        pass

    pass

expect("public_inner_decorated_async", "D123: Missing docstring in inaccessible public function")
expect("_prviate_inner_decorated_async", "D173: Missing docstring in inaccessible private function")


def func_with_inner_class_after():
    """Test a function with inner class after docstring."""

    class public_inner_class():
        pass

    class _private_inner_class():
        pass

    pass

expect("public_inner_class", "D121: Missing docstring in inaccessible public class")
expect("_private_inner_class", "D171: Missing docstring in inaccessible private class")


def func_with_weird_backslash():
    """Test a function with a weird backslash.\
"""
