"""A valid module docstring."""

from .expected import Expectation

expectation = Expectation()
expect = expectation.expect


_D213 = 'D213: Multi-line docstring summary should start at the second line'


@expect(_D213)
@expect("D405: Section name should be properly capitalized "
        "('Returns', not 'returns')")
def not_capitalized():
    """Valid headline.

    returns
    -------
    A value of some sort.

    """


@expect(_D213)
@expect("D406: Section name should end with a newline "
        "('Returns', not 'Returns:')")
def superfluous_suffix():
    """Valid headline.

    Returns:
    -------
    A value of some sort.

    """


@expect(_D213)
@expect("D407: Missing dashed underline after section ('Returns')")
def no_underline():
    """Valid headline.

    Returns
    A value of some sort.

    """


@expect(_D213)
@expect("D407: Missing dashed underline after section ('Returns')")
@expect("D410: Missing blank line after section ('Returns')")
def no_underline():
    """Valid headline.

    Returns
    """


@expect(_D213)
@expect("D408: Section underline should be in the line following the "
        "section's name ('Returns')")
def blank_line_before_underline():
    """Valid headline.

    Returns

    -------
    A value of some sort.

    """


@expect(_D213)
@expect("D409: Section underline should match the length of its name "
        "(Expected 7 dashes in section 'Returns', got 2)")
def bad_underline_length():
    """Valid headline.

    Returns
    --
    A value of some sort.

    """


@expect(_D213)
@expect("D410: Missing blank line after section ('Returns')")
def no_blank_line_after_section():
    """Valid headline.

    Returns
    -------
    A value of some sort.
    """


@expect(_D213)
@expect("D411: Missing blank line before section ('Returns')")
def no_blank_line_before_section():
    """Valid headline.

    The function's description.
    Returns
    -------
    A value of some sort.

    """


@expect(_D213)
@expect("D214: Section is over-indented ('Returns')")
def section_overindented():
    """Valid headline.

        Returns
    -------
    A value of some sort.

    """


@expect(_D213)
@expect("D215: Section underline is over-indented (in section 'Returns')")
def section_underline_overindented():
    """Valid headline.

    Returns
        -------
    A value of some sort.

    """


@expect(_D213)
@expect("D215: Section underline is over-indented (in section 'Returns')")
@expect("D410: Missing blank line after section ('Returns')")
def section_underline_overindented_and_contentless():
    """Valid headline.

    Returns
        -------
    """


@expect(_D213)
def ignore_non_actual_section():
    """Valid headline.

    This is the function's description, which will also specify what it
    returns

    """


@expect(_D213)
@expect("D401: First line should be in imperative mood "
        "('Return', not 'Returns')")
@expect("D400: First line should end with a period (not 's')")
@expect("D205: 1 blank line required between summary line and description "
        "(found 0)")
def section_name_in_first_line():
    """Returns
    -------
    A value of some sort.

    """


@expect(_D213)
@expect("D405: Section name should be properly capitalized "
        "('Short Summary', not 'Short summary')")
@expect("D412: Section content should be in the line following its header "
        "('Short Summary')")
@expect("D409: Section underline should match the length of its name "
        "(Expected 7 dashes in section 'Returns', got 6)")
@expect("D410: Missing blank line after section ('Returns')")
@expect("D411: Missing blank line before section ('Raises')")
@expect("D406: Section name should end with a newline "
        "('Raises', not 'Raises:')")
@expect("D407: Missing dashed underline after section ('Raises')")
def multiple_sections():
    """Valid headline.

    Short summary
    -------------

    This is the function's description, which will also specify what it
    returns.

    Returns
    ------
    Many many wonderful things.
    Raises:
    My attention.

    """
