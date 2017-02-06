"""A valid module docstring."""

from .expected import Expectation

expectation = Expectation()
expect = expectation.expect


_D213 = 'D213: Multi-line docstring summary should start at the second line'


@expect(_D213)
@expect("D405: Section name should be properly capitalized "
        "('Returns', not 'returns')")
def not_capitalized():
    """Toggle the gizmo.

    returns
    -------

    """


@expect(_D213)
@expect("D406: Section name should end with a newline "
        "('Returns', not 'Returns:')")
def superfluous_suffix():
    """Toggle the gizmo.

    Returns:
    -------

    """


@expect(_D213)
@expect("D407: Missing dashed underline after section ('Returns')")
def no_underline():
    """Toggle the gizmo.

    Returns

    """


@expect(_D213)
@expect("D408: Section underline should be in the line following the "
        "section's name ('Returns')")
def blank_line_before_underline():
    """Toggle the gizmo.

    Returns

    -------

    """


@expect(_D213)
@expect("D409: Section underline should match the length of its name "
        "(Expected 7 dashes in section 'Returns', got 2)")
def bad_underline_length():
    """Toggle the gizmo.

    Returns
    --

    """


@expect(_D213)
@expect("D410: Missing blank line after section ('Returns')")
def no_blank_line_after_section():
    """Toggle the gizmo.

    Returns
    -------
    A whole lot of values.
    """


@expect(_D213)
@expect("D411: Missing blank line before section ('Returns')")
def no_blank_line_before_section():
    """Toggle the gizmo.

    The function's description.
    Returns
    -------

    """


@expect(_D213)
@expect("D214: Section is over-indented ('Returns')")
def section_overindented():
    """Toggle the gizmo.

        Returns
    -------

    """


@expect(_D213)
@expect("D215: Section underline is over-indented (in section 'Returns')")
def section_underline_overindented():
    """Toggle the gizmo.

    Returns
        -------

    """


@expect(_D213)
def ignore_non_actual_section():
    """Toggle the gizmo.

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

    """


@expect(_D213)
@expect("D405: Section name should be properly capitalized "
        "('Short Summary', not 'Short summary')")
@expect("D409: Section underline should match the length of its name "
        "(Expected 7 dashes in section 'Returns', got 6)")
@expect("D410: Missing blank line after section ('Returns')")
@expect("D411: Missing blank line before section ('Raises')")
@expect("D406: Section name should end with a newline "
        "('Raises', not 'Raises:')")
@expect("D407: Missing dashed underline after section ('Raises')")
@expect("D410: Missing blank line after section ('Raises')")
def multiple_sections():
    """Toggle the gizmo.

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
