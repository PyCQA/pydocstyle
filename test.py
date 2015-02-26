# encoding: utf-8
# No docstring, so we can test D100
import sys


expected = set([])


def expect(*args):
    """Decorator that expects a certain PEP 257 violation."""
    def none(a):
        return None

    if len(args) == 1:
        return lambda f: expected.add((f.__name__, args[0])) or none(f()) or f
    expected.add(args)


expect('class_', 'D101: Missing docstring in public class')


class class_:

    expect('meta', 'D101: Missing docstring in public class')

    class meta:
        """"""

    @expect('D102: Missing docstring in public method')
    def method():
        pass

    def _ok_since_private():
        pass

    @expect('D102: Missing docstring in public method')
    def __init__(self=None):
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


expect('TrailingSpace',
       'D204: 1 blank line required after class docstring (found 0)')


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
def multi_line_zero_separating_blanks():
    """Summary.
    Description.

    """


@expect('D205: 1 blank line required between summary line and description '
        '(found 2)')
def multi_line_two_separating_blanks():
    """Summary.


    Description.

    """


def multi_line_one_separating_blanks():
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


@expect('D209: Multi-line docstring closing quotes should be on a separate '
        'line')
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
def multiline():
    """ Whitespace at the begining.

    This is the end.
    """


@expect('D300: Use """triple double quotes""" (found \'\'\'-quotes)')
def lsfklkjllkjl():
    r'''Summary.'''


@expect('D300: Use """triple double quotes""" (found \'-quotes)')
def lalskklkjllkjl():
    r'Summary.'


@expect('D301: Use r""" if any backslashes in a docstring')
def lalsksdewnlkjl():
    """Sum\\mary."""


if sys.version_info[0] <= 2:
    @expect('D302: Use u""" for Unicode docstrings')
    def lasewnlkjl():
        """Юникод."""


@expect("D400: First line should end with a period (not 'y')")
def lwnlkjl():
    """Summary"""


@expect("D401: First line should be in imperative mood ('Return', not "
        "'Returns')")
def liouiwnlkjl():
    """Returns foo."""


@expect('D402: First line should not be the function\'s "signature"')
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


@expect("D103: Missing docstring in public function")
def oneliner_d102(): return


@expect("D400: First line should end with a period (not 'r')")
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

expect('test.py', 'D100: Missing docstring in public module')
