# encoding: utf-8
# No docstring, so we can test D100
import sys


expected = set([])


def expect(*args):
    """Decorator that expects a certain PEP 257 violation."""
    none = lambda a: None
    if len(args) == 1:
        return lambda f: expected.add((f.__name__, args[0])) or none(f()) or f
    expected.add(args)


expect('class_', 'D101: Docstring missing')


class class_:

    expect('meta', 'D101: Docstring missing')

    class meta:
        """"""

    @expect('D102: Docstring missing')
    def method():
        pass

    def _ok_since_private():
        pass

    @expect('D102: Docstring missing')
    def __init__(self=None):
        pass


@expect('D103: Docstring missing')
def function():
    """ """
    def ok_since_nested():
        pass

    @expect('D103: Docstring missing')
    def nested():
        ''


@expect('D200: One-line docstring should not occupy 3 lines')
def asdlkfasd():
    """
    Wrong.
    """


@expect('D201: No blank lines allowed *before* function docstring, found 1')
def leading_space():

    """Leading space."""


@expect('D202: No blank lines allowed *after* function docstring, found 1')
def trailing_space():
    """Leading space."""

    pass


@expect('D201: No blank lines allowed *before* function docstring, found 1')
@expect('D202: No blank lines allowed *after* function docstring, found 1')
def trailing_and_leading_space():

    """Trailing and leading space."""

    pass


expect('LeadingSpace',
       'D203: No blank lines allowed *before* class docstring, found 1')


class LeadingSpace:

    """No Leading space."""


expect('TrailingSpace',
       'D204: Expected 1 blank line *after* class docstring, found 0')


class TrailingSpace:
    """TrailingSpace."""
    pass

expect('LeadingSpaceAndTrailingSpaceMissing',
       'D203: No blank lines allowed *before* class docstring, found 1')
expect('LeadingSpaceAndTrailingSpaceMissing',
       'D204: Expected 1 blank line *after* class docstring, found 0')


class LeadingSpaceAndTrailingSpaceMissing:

    """Extra Leading and trailing space missing."""
    pass


@expect('D205: Blank line missing between one-line summary and description')
def asdfasdf():
    """Summary.
    Description.

    """


@expect('D207: Docstring is under-indented')
def asdfsdf():
    """Summary.

Description.

    """


@expect('D207: Docstring is under-indented')
def asdsdfsdffsdf():
    """Summary.

    Description.

"""


@expect('D208: Docstring is over-indented')
def asdfsdsdf24():
    """Summary.

       Description.

    """


@expect('D208: Docstring is over-indented')
def asdfsdsdfsdf24():
    """Summary.

    Description.

        """


@expect('D208: Docstring is over-indented')
def asdfsdfsdsdsdfsdf24():
    """Summary.

        Description.

    """


@expect('D209: Put multi-line docstring closing quotes on separate line')
def asdfljdf24():
    """Summary.

    Description."""


@expect('D300: Expected """-quotes, got \'\'\'-quotes')
def lsfklkjllkjl():
    r'''Summary.'''


@expect('D300: Expected """-quotes, got \'-quotes')
def lalskklkjllkjl():
    r'Summary.'


@expect('D301: Use r""" if any backslashes in a docstring')
def lalsksdewnlkjl():
    """Sum\\mary."""


if sys.version_info[0] <= 2:
    @expect('D302: Use u""" for docstrings with Unicode')
    def lasewnlkjl():
        """Юникод."""


@expect("D400: First line should end with '.', not 'y'")
def lwnlkjl():
    """Summary"""


@expect("D401: First line should be imperative: 'Return', not 'Returns'")
def liouiwnlkjl():
    """Returns foo."""


@expect("D402: First line should not be function's signature")
def foobar():
    """Signature: foobar()."""


def new_209():
    """First line.

    More lines.
    """
    pass


def old_209():
    """One liner.

    Multi-line comments. OK to have extra blank line

    """


@expect("D103: Docstring missing")
def oneliner_d102(): return


@expect("D400: First line should end with '.', not 'r'")
def oneliner_withdoc(): """One liner"""


@expect("D207: Docstring is under-indented")
def docstring_start_in_same_line(): """First Line.

    Second Line
    """


def function_with_lambda_arg(x=lambda y: y):
    """A valid docstring."""


def a_following_valid_function(x):
    """Check for a bug where the previous function caused an assertion.

    The assertion was caused in the next function, so this one is necessary.

    """

expect('test.py', 'D100: Docstring missing')
