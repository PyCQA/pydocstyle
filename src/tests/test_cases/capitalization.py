"""A valid module docstring."""

from .expected import Expectation

expectation = Expectation()
expect = expectation.expect


@expect("D403: First word of the first line should be properly capitalized "
        "('Do', not 'do')")
def not_capitalized():
    """do something."""


# Make sure empty docstrings don't generate capitalization errors.
@expect("D103: Missing docstring in public function")
def empty_docstring():
    """"""


def all_caps():
    """GET the request."""


def non_letter_characters():
    """Create/Edit the doodli-do."""


def more_non_letter_characters():
    """(Un)register the user."""


def even_more_non_letter():
    """'laser' the planet."""


def dash():
    """git-push it."""


def digit_in_word():
    """sha1 the string."""


@expect("D403: First word of the first line should be properly capitalized "
        "(\"Don't\", not \"Don'T\")")
def partial_caps():
    """Don'T do that."""


@expect("D403: First word of the first line should be properly capitalized "
        "('Return', not 'ReTurn')")
def more_partial_caps():
    """ReTurn the field."""


@expect("D403: First word of the first line should be properly capitalized "
        "('Generate', not 'generate')")
def just_one_more_example():
    """generate a function."""
