"""Test for warning about f-strings as docstrings."""

from .expected import Expectation

expectation = Expectation()
expect = expectation.expect


@expect("D303: f-strings are not valid as docstrings")
def fstring():
    f"""Toggle the gizmo."""
