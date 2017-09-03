"""Tests for the violations.Error class."""

import pytest
import collections
import textwrap
from pydocstyle.violations import Error


MockDefinition = collections.namedtuple('MockDefinition', ['source', 'start'])


def test_message_without_context():
    """Test a simple error message without parameters."""
    error = Error('CODE', 'an error', None)
    assert error.message == 'CODE: an error'


def test_message_with_context():
    """Test an error message with parameters."""
    error = Error('CODE', 'an error', 'got {}', 0)
    assert error.message == 'CODE: an error (got 0)'


def test_message_with_insufficient_parameters():
    """Test an error message with invalid parameter invocation."""
    error = Error('CODE', 'an error', 'got {}')
    with pytest.raises(IndexError):
        assert error.message


def test_lines():
    """Test proper printing of source lines, including blank line trimming."""
    error = Error('CODE', 'an error', None)
    definition = MockDefinition(source=['def foo():\n',
                                        '    """A docstring."""\n',
                                        '\n',
                                        '    pass\n',
                                        '\n',
                                        '\n'],
                                start=424)
    error.set_context(definition, None)
    print(error.lines)
    assert error.lines == textwrap.dedent('''\
        424: def foo():
        425:     """A docstring."""
        426:
        427:     pass
    ''')
