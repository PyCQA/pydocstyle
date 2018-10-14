# encoding: utf-8
# No docstring, so we can test D100
from functools import wraps
import os
import sys
from .expected import Expectation


expectation = Expectation()
expect = expectation.expect

expect('class_', 'D101: Missing docstring in public class')


class class_:

    expect('meta', 'D106: Missing docstring in public nested class')

    class meta:
        """"""

    @expect('D102: Missing docstring in public method')
    def method():
        pass

    def _ok_since_private():
        pass

    @expect('D102: Missing docstring in public method')
    def __new__(self=None):
        pass

    @expect('D107: Missing docstring in __init__')
    def __init__(self=None):
        pass

    @expect('D105: Missing docstring in magic method')
    def __str__(self=None):
        pass

    @expect('D102: Missing docstring in public method')
    def __call__(self=None, x=None, y=None, z=None):
        pass


@expect('D103: Missing docstring in public function')
def function():
    """ """
    def ok_since_nested():
        pass

    @expect('D103: Missing docstring in public function')
    def nested():
        ''


@expect('D200: One-line docstring should fit on one line with quotes '
        '(found 3)')
@expect('D212: Multi-line docstring summary should start at the first line')
def asdlkfasd():
    """
    Wrong.
    """


@expect('D201: No blank lines allowed before function docstring (found 1)')
def leading_space():

    """Leading space."""


@expect('D202: No blank lines allowed after function docstring (found 1)')
def trailing_space():
    """Leading space."""

    pass


@expect('D201: No blank lines allowed before function docstring (found 1)')
@expect('D202: No blank lines allowed after function docstring (found 1)')
def trailing_and_leading_space():

    """Trailing and leading space."""

    pass


expect('LeadingSpaceMissing',
       'D203: 1 blank line required before class docstring (found 0)')


class LeadingSpaceMissing:
    """Leading space missing."""


expect('WithLeadingSpace',
       'D211: No blank lines allowed before class docstring (found 1)')


class WithLeadingSpace:

    """With leading space."""


expect('TrailingSpace',
       'D204: 1 blank line required after class docstring (found 0)')
expect('TrailingSpace',
       'D211: No blank lines allowed before class docstring (found 1)')


class TrailingSpace:

    """TrailingSpace."""
    pass


expect('LeadingAndTrailingSpaceMissing',
       'D203: 1 blank line required before class docstring (found 0)')
expect('LeadingAndTrailingSpaceMissing',
       'D204: 1 blank line required after class docstring (found 0)')


class LeadingAndTrailingSpaceMissing:
    """Leading and trailing space missing."""
    pass


@expect('D205: 1 blank line required between summary line and description '
        '(found 0)')
@expect('D213: Multi-line docstring summary should start at the second line')
def multi_line_zero_separating_blanks():
    """Summary.
    Description.

    """


@expect('D205: 1 blank line required between summary line and description '
        '(found 2)')
@expect('D213: Multi-line docstring summary should start at the second line')
def multi_line_two_separating_blanks():
    """Summary.


    Description.

    """


@expect('D213: Multi-line docstring summary should start at the second line')
def multi_line_one_separating_blanks():
    """Summary.

    Description.

    """


@expect('D207: Docstring is under-indented')
@expect('D213: Multi-line docstring summary should start at the second line')
def asdfsdf():
    """Summary.

Description.

    """


@expect('D207: Docstring is under-indented')
@expect('D213: Multi-line docstring summary should start at the second line')
def asdsdfsdffsdf():
    """Summary.

    Description.

"""


@expect('D208: Docstring is over-indented')
@expect('D213: Multi-line docstring summary should start at the second line')
def asdfsdsdf24():
    """Summary.

       Description.

    """


@expect('D208: Docstring is over-indented')
@expect('D213: Multi-line docstring summary should start at the second line')
def asdfsdsdfsdf24():
    """Summary.

    Description.

        """


@expect('D208: Docstring is over-indented')
@expect('D213: Multi-line docstring summary should start at the second line')
def asdfsdfsdsdsdfsdf24():
    """Summary.

        Description.

    """


@expect('D209: Multi-line docstring closing quotes should be on a separate '
        'line')
@expect('D213: Multi-line docstring summary should start at the second line')
def asdfljdf24():
    """Summary.

    Description."""


@expect('D210: No whitespaces allowed surrounding docstring text')
def endswith():
    """Whitespace at the end. """


@expect('D210: No whitespaces allowed surrounding docstring text')
def around():
    """ Whitespace at everywhere. """


@expect('D210: No whitespaces allowed surrounding docstring text')
@expect('D213: Multi-line docstring summary should start at the second line')
def multiline():
    """ Whitespace at the beginning.

    This is the end.
    """


@expect('D300: Use """triple double quotes""" (found \'\'\'-quotes)')
def triple_single_quotes_raw():
    r'''Summary.'''


@expect('D300: Use """triple double quotes""" (found \'\'\'-quotes)')
def triple_single_quotes_raw_uppercase():
    R'''Summary.'''


@expect('D300: Use """triple double quotes""" (found \'-quotes)')
def single_quotes_raw():
    r'Summary.'


@expect('D300: Use """triple double quotes""" (found \'-quotes)')
def single_quotes_raw_uppercase():
    R'Summary.'


@expect('D300: Use """triple double quotes""" (found \'-quotes)')
@expect('D301: Use r""" if any backslashes in a docstring')
def single_quotes_raw_uppercase_backslash():
    R'Sum\mary.'


@expect('D301: Use r""" if any backslashes in a docstring')
def double_quotes_backslash():
    """Sum\\mary."""


@expect('D301: Use r""" if any backslashes in a docstring')
def double_quotes_backslash_uppercase():
    R"""Sum\\mary."""


if sys.version_info[0] <= 2:
    @expect('D302: Use u""" for Unicode docstrings')
    def unicode_unmarked():
        """Юникод."""

    @expect('D302: Use u""" for Unicode docstrings')
    def first_word_has_unicode_byte():
        """あy."""


@expect("D400: First line should end with a period (not 'y')")
def lwnlkjl():
    """Summary"""


@expect("D401: First line should be in imperative mood ('Return', not "
        "'Returns')")
def liouiwnlkjl():
    """Returns foo."""


@expect("D401: First line should be in imperative mood; try rephrasing "
        "(found 'Constructor')")
def sdgfsdg23245():
    """Constructor for a foo."""


@expect('D402: First line should not be the function\'s "signature"')
def foobar():
    """Signature: foobar()."""


@expect('D213: Multi-line docstring summary should start at the second line')
def new_209():
    """First line.

    More lines.
    """
    pass


@expect('D213: Multi-line docstring summary should start at the second line')
def old_209():
    """One liner.

    Multi-line comments. OK to have extra blank line

    """


@expect("D103: Missing docstring in public function")
def oneliner_d102(): return


@expect("D400: First line should end with a period (not 'r')")
def oneliner_withdoc(): """One liner"""


@expect("D207: Docstring is under-indented")
@expect('D213: Multi-line docstring summary should start at the second line')
def docstring_start_in_same_line(): """First Line.

    Second Line
    """


def function_with_lambda_arg(x=lambda y: y):
    """Wrap the given lambda."""


@expect('D213: Multi-line docstring summary should start at the second line')
def a_following_valid_function(x=None):
    """Check for a bug where the previous function caused an assertion.

    The assertion was caused in the next function, so this one is necessary.

    """


def outer_function():
    """Do something."""
    def inner_function():
        """Do inner something."""
        return 0


@expect("D400: First line should end with a period (not 'g')")
@expect("D401: First line should be in imperative mood ('Run', not 'Runs')")
def docstring_bad():
    """Runs something"""
    pass


def docstring_bad_ignore_all():  # noqa
    """Runs something"""
    pass


def docstring_bad_ignore_one():  # noqa: D400,D401
    """Runs something"""
    pass


@expect("D401: First line should be in imperative mood ('Run', not 'Runs')")
def docstring_ignore_violations_of_pydocstyle_D400_and_PEP8_E501_but_catch_D401():  # noqa: E501,D400
    """Runs something"""
    pass


@wraps(docstring_bad_ignore_one)
def bad_decorated_function():
    """Bad (E501) but decorated"""
    pass


expect(os.path.normcase(__file__ if __file__[-1] != 'c' else __file__[:-1]),
       'D100: Missing docstring in public module')
