"""Unit test for pydocstyle utils.

Use tox or py.test to run the test suite.
"""
from pydocstyle import utils


__all__ = ()


def test_common_prefix():
    """Test common prefix length of two strings."""
    assert utils.common_prefix_length('abcd', 'abce') == 3


def test_no_common_prefix():
    """Test common prefix length of two strings that have no common prefix."""
    assert utils.common_prefix_length('abcd', 'cdef') == 0


def test_differ_length():
    """Test common prefix length of two strings differing in length."""
    assert utils.common_prefix_length('abcd', 'ab') == 2


def test_empty_string():
    """Test common prefix length of two strings, one of them empty."""
    assert utils.common_prefix_length('abcd', '') == 0


def test_strip_non_alphanumeric():
    """Test strip of a string leaves only alphanumeric characters."""
    assert utils.strip_non_alphanumeric("  1abcd1...") == "1abcd1"
