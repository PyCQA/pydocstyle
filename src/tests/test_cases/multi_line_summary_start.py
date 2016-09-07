"""Module to check different multi-line docstring flavors."""

from .expected import Expectation

expectation = Expectation()
expect = expectation.expect

_D212 = 'D212: Multi-line docstring summary should start at the first line'
_D213 = 'D213: Multi-line docstring summary should start at the second line'

_D300 = 'D300: Use """triple double quotes""" (found \'\'\'-quotes)'
_D301 = 'D301: Use r""" if any backslashes in a docstring'


@expect(_D212)
def multi_line_starts_second_line():
    """
    Summary.

    Description.

    """


@expect(_D212)
@expect(_D300)
def multi_line_starts_second_line_single_quote():
    '''
    Summary.

    Description.

    '''


@expect(_D212)
def multi_line_starts_second_line_raw():
    r"""
    Summary.

    Description with \backslash\.

    """


@expect(_D212)
@expect(_D301)
def multi_line_starts_second_line_upper_raw():
    R"""
    Summary.

    Description with \backslash\.

    """


@expect(_D212)
@expect(_D300)
def multi_line_starts_second_line_raw_single_quote():
    r'''
    Summary.

    Description with \backslash\.

    '''


@expect(_D212)
@expect(_D300)
@expect(_D301)
def multi_line_starts_second_line_upper_raw_single_quote():
    R'''
    Summary.

    Description with \backslash\.

    '''


@expect(_D213)
def multi_line_starts_first_line():
    """Summary.

    Description.

    """


@expect(_D213)
@expect(_D300)
def multi_line_starts_first_line_single_quote():
    '''Summary.

    Description.

    '''


@expect(_D213)
def multi_line_starts_first_line_raw():
    r"""Summary.

    Description with \backslash\.

    """


@expect(_D213)
@expect(_D301)
def multi_line_starts_first_line_upper_raw():
    R"""Summary.

    Description with \backslash\.

    """


@expect(_D213)
@expect(_D300)
def multi_line_starts_first_line_raw_single_quote():
    r'''Summary.

    Description with \backslash\.

    '''


@expect(_D213)
@expect(_D300)
@expect(_D301)
def multi_line_starts_first_line_upper_raw_single_quote():
    R'''Summary.

    Description with \backslash\.

    '''
