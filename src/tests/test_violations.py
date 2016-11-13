# -*- coding: utf-8 -*-
"""Unit tests for the pydocstyle.violations module.

Use tox or py.test to run the test-suite.
"""

from __future__ import with_statement

import pytest
from mock import MagicMock

from pydocstyle import violations
from pydocstyle.exceptions import InvalidErrorFormat


MockModule = MagicMock(
    start=1,
    end=999,
    _slice=slice(0, None),
    _source=["My hovercraft is full of eels"],
    __str__=MagicMock(return_value="at module level"))
MockModule.name = 'hovercraft.py'
MockModule.module = MockModule


def test_default_error_format():
    """Test that if Error.format is None the default output format is used."""
    err = violations.D100()
    err.set_context(MockModule, '')

    assert err.format is None
    assert str(err) == ("hovercraft.py:1 at module level:\n"
                        "        D100: Missing docstring in public module")


def test_default_error_format_explain():
    """Test that if Error.explain is True the output includes explanantion."""
    err = violations.D100()
    err.set_context(MockModule, "Thou shalt have module docstrings!")
    err.explain = True

    assert err.format is None
    assert err.source is False
    assert str(err) == ("hovercraft.py:1 at module level:\n"
                        "        D100: Missing docstring in public module\n\n"
                        "Thou shalt have module docstrings!\n\n")


def test_default_error_format_source():
    """Test that if Error.source is True the output includes source lines."""
    err = violations.D100()
    err.set_context(MockModule, '')
    err.source = True

    assert err.format is None
    assert err.explain is False
    assert str(err) == ("hovercraft.py:1 at module level:\n"
                        "        D100: Missing docstring in public module\n\n"
                        "16: My hovercraft is full of eels    "
                        " 1: My hovercraft is full of eels\n")


def test_default_error_format_explain_and_source():
    """Test that Error.explain and Error.source can be combined."""
    err = violations.D100()
    err.set_context(MockModule, "Thou shalt have module docstrings!")
    err.explain = True
    err.source = True

    assert err.format is None
    assert str(err) == ("hovercraft.py:1 at module level:\n"
                        "        D100: Missing docstring in public module\n\n"
                        "Thou shalt have module docstrings!\n\n"
                        "16: My hovercraft is full of eels    "
                        " 1: My hovercraft is full of eels\n")


@pytest.mark.parametrize('error,format,output,explanation', [
    (violations.D100, "{filename}#L{line:03}: {short_desc} ({code})",
     "hovercraft.py#L001: Missing docstring in public module (D100)", ""),
    (violations.D100, "{code}", "D100", ""),
    (violations.D100, "{definition}", "at module level", ""),
    (violations.D100, "{explanation}", "Docstrings please.",
     "Docstrings please."),
    (violations.D100, "{filename}", "hovercraft.py", ""),
    (violations.D100, "{line}", "1", ""),
    (violations.D100, "{lines}",
     "16: My hovercraft is full of eels     1: My hovercraft is full of eels",
     ""),
    (violations.D100, "{message}", "D100: Missing docstring in public module",
     ""),
    (violations.D100, "{short_desc}", "Missing docstring in public module", "")
])
def test_error_format(error, explanation, format, output):
    """Test that setting Error.format defines output format correctly."""
    err = error()
    err.set_context(MockModule, explanation)
    err.format = format

    assert str(err) == output


@pytest.mark.parametrize('format,msg', [
    ('{foo}', "'foo'"),
    ('{message.foo}', "'str' object has no attribute 'foo'"),
    ('{line:s}', "Unknown format code 's' for object of type 'int'"),
])
def test_error_format_key_error(format, msg):
    """Test that errors in Error.format are turned into InvalidErrorFormat."""
    err = violations.D100()
    err.set_context(MockModule, '')
    err.format = format

    with pytest.raises(InvalidErrorFormat) as excinfo:
        str(err)

    expected = "Invalid error format '{}': {}".format(format, msg)
    assert str(excinfo.value) == expected
