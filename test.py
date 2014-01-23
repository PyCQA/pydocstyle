"""Docstring."""
# encoding: utf-8
errors = set([])


def expect(*args):
    """Decorator that expects a certain PEP 257 violation."""
    ignore = lambda a: None
    if len(args) == 1:
        return lambda f: errors.add((f.__name__, args[0])) or ignore(f()) or f
    errors.add(args)


@expect('D101: Docstring missing')
class class_:

    @expect('D101: Docstring missing')
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


@expect('D203: Expected 1 blank line *before* class docstring, found 0')
class LeadingSpaceMissing:
    """Leading space missing."""


@expect('D204: Expected 1 blank line *after* class docstring, found 0')
class TrailingSpace:

    """TrailingSpace."""
    pass


@expect('D203: Expected 1 blank line *before* class docstring, found 0')
@expect('D204: Expected 1 blank line *after* class docstring, found 0')
class LeadingAndTrailingSpaceMissing:
    """Leading and trailing space missing."""
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


@expect('D209: Multi-line docstring should end with 1 blank line, found 0')
def asdfljdf24():
    """Summary.

    Description."""


@expect('D209: Multi-line docstring should end with 1 blank line, found 0')
def asdljlfljdf24():
    """Summary.

    Description.
    """


@expect('D209: Multi-line docstring should end with 1 blank line, found 2')
def lklkjllkjl():
    """Summary.

    Description.


    """


@expect('D300: Expected """-quotes, got \'\'\'-quotes')
def lsfklkjllkjl():
    r'''Summary.'''


@expect('D300: Expected """-quotes, got \'-quotes')
def lalskklkjllkjl():
    r'Summary.'


@expect('D301: Use r""" if any backslashes in a docstring')
def lalsksdewnlkjl():
    """Sum\\mary."""


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


def run():
    """Run the functions above and check errors agains expected errors."""
    import pep257
    results = list(pep257.check([__file__]))
    assert set(map(type, results)) == set([pep257.Error]), results
    results = set([(e.definition.name, e.message) for e in results])
    print('\nmissing: %r' % (results - errors))
    print('\n  extra: %r' % (errors - results))
    assert errors == results
