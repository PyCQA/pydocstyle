"""Use tox or py.test to run the test-suite."""
# -*- coding: utf-8 -*-
from __future__ import with_statement

import pep257
import mock


__all__ = ()


def test_pep257_conformance():
    errors = list(pep257.check(['pep257.py', 'test_pep257.py']))
    print(errors)
    assert errors == []


def test_ignore_list():
    function_to_check = """def function_with_bad_docstring(foo):
    \"\"\" does spacing without a period in the end
    no blank line after one-liner is bad. Also this - \"\"\"
    return foo
    """
    expected_error_codes = {'D100', 'D400', 'D401', 'D205', 'D209'}
    mock_open = mock.mock_open(read_data=function_to_check)
    with mock.patch('__builtin__.open', mock_open, create=True):
        errors = tuple(pep257.check(['filepath']))
        error_codes = set(error.code for error in errors)
        assert error_codes == expected_error_codes

        errors = tuple(pep257.check(['filepath'], ignore=['D100', 'D202']))
        error_codes = set(error.code for error in errors)
        assert error_codes == expected_error_codes - {'D100', 'D202'}
