"""Unit tests for Sphinx-style parameter documentation rules.

Use tox or pytest to run the test suite.
"""
from pydocstyle.checker import ConventionChecker
import textwrap
import pytest

SPHINX_ARGS_REGEX = ConventionChecker.SPHINX_ARGS_REGEX

def test_parameter_found():
    """The regex matches a line with a parameter definition."""
    line = "        :param x: Lorem ipsum dolor sit amet\n"
    assert SPHINX_ARGS_REGEX.match(line) is not None


def test_parameter_name_extracted():
    """The first match group is the parameter name."""
    line = "        :param foo: Lorem ipsum dolor sit amet\n"
    assert SPHINX_ARGS_REGEX.match(line).group(1) == "foo"


def test_finding_params():
    """Sphinx-style parameter names are found."""
    docstring = """A description of a great function.

        :param foo: Lorem ipsum dolor sit amet
        :param bar: Ut enim ad minim veniam
        """

    lines = docstring.splitlines(keepends=True)
    assert ConventionChecker._find_sphinx_params(lines) == ['foo', 'bar']


def test_missing_params():
    """Missing parameters are reported."""
    source = textwrap.dedent('''\
        def thing(foo, bar, baz):
            """Do great things.

            :param foo: Lorem ipsum dolor sit amet
            :param baz: Ut enim ad minim veniam
            """
            pass
        ''')
    errors = ConventionChecker().check_source(source, '<test>')
    for error in errors:
        if error.code == "D417":
            break
    else:
        pytest.fail('did not find D417 error')

    assert error.parameters == ('bar', 'thing')
    assert error.message == (
        "D417: Missing argument descriptions in the docstring (argument(s) bar are"
        " missing descriptions in 'thing' docstring)")


def test_missing_description():
    """A parameter is considered missing if it has no description."""
    source = textwrap.dedent('''\
        def thing(foo, bar, baz):
            """Do great things.

            :param foo: Lorem ipsum dolor sit amet
            :param bar:
            :param baz: Ut enim ad minim veniam
            """
            pass
        ''')
    errors = ConventionChecker().check_source(source, '<test>')
    for error in errors:
        if error.code == "D417":
            break
    else:
        pytest.fail('did not find D417 error')

    assert error.parameters == ('bar', 'thing')
    assert error.message == (
        "D417: Missing argument descriptions in the docstring (argument(s) bar are"
        " missing descriptions in 'thing' docstring)")
