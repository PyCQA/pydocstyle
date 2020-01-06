"""A valid module docstring."""

from .expected import Expectation

expectation = Expectation()
expect = expectation.expect


def fake_decorator(decorated):
    """Fake decorator that does nothing."""
    return decorated


expect("ClassWithProperties", "D101: Missing docstring in public class")


class ClassWithProperties:
    @property
    def property_method(self):
        """Method with property decorator."""
        return "a property"

    expect(
        "undecorated_method",
        "D401: First line should be in imperative mood; "
        "try rephrasing (found 'Method')",
    )

    def undecorated_method(self):
        """Method without decorator."""
        print("doing something")

    expect(
        "decorated_method",
        "D401: First line should be in imperative mood; "
        "try rephrasing (found 'Method')",
    )

    @fake_decorator
    def decorated_method(self):
        """Method with decorator that is not property."""
        print("doing something decorated")
