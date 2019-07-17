"""Unit test for pydocstyle utils.

Use tox or py.test to run the test suite.
"""
from pydocstyle import utils


__all__ = ()


def test_common_prefix():
    """We can find the common prefix of two strings."""
    assert utils.common_prefix_length('abcd', 'abce') == 3


def test_no_common_prefix():
    """If two strings have no common prefix, return the empty string."""
    assert utils.common_prefix_length('abcd', 'cdef') == 0


def test_differ_length():
    """We can find a common prefix of two strings differing in length."""
    assert utils.common_prefix_length('abcd', 'ab') == 2
