"""A valid module docstring."""

from .expected import Expectation

expectation = Expectation()
expect = expectation.expect


@expect("D403: First word of the first line should be properly capitalized "
        "('Do', not 'do')")
def not_capitalized():
    """do something."""


# Make sure empty docstrings don't generate capitalization errors.
@expect("D103: Missing docstring in public function")
def empty_docstring():
    """"""


@expect("D403: First word of the first line should be properly capitalized "
        "('Get', not 'GET')")
def all_caps():
    """GET the request."""
