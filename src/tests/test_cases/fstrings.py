"""Test for warning about f-strings as docstrings."""

from .expected import Expectation

expectation = Expectation()
expect = expectation.expect
_GIZMO = "gizmo"
D303 = expect("D303: f-strings are not valid as docstrings")


@D303
def fstring():
    f"""Toggle the gizmo."""


@D303
def another_fstring():
    F"""Toggle the gizmo."""


@D303
def fstring_with_raw():
    rF"""Toggle the gizmo."""


@D303
def fstring_with_raw_caps():
    RF"""Toggle the gizmo."""


@D303
def fstring_with_raw_variable():
    RF"""Toggle the {_GIZMO}."""


@D303
def fstring_with_variable():
    f"""Toggle the {_GIZMO.upper()}."""


@D303
def fstring_with_other_errors(arg=1, missing_arg=2):
    f"""Toggle the {_GIZMO.upper()}

    This should not raise any other errors since fstrings
    are a terminal check.
    """


@D303
def fstring_with_blank_doc_string():
    f"""  """
