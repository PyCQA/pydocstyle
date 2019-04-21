"""A valid module docstring."""

from .expected import Expectation

expectation = Expectation()
expect = expectation.expect


_D213 = 'D213: Multi-line docstring summary should start at the second line'
_D400 = "D400: First line should end with a period (not '!')"


@expect(_D213)
@expect("D405: Section name should be properly capitalized "
        "('Returns', not 'returns')")
def not_capitalized():  # noqa: D416
    """Toggle the gizmo.

    returns
    -------
    A value of some sort.

    """


@expect(_D213)
@expect("D406: Section name should end with a newline "
        "('Returns', not 'Returns:')")
def superfluous_suffix():  # noqa: D416
    """Toggle the gizmo.

    Returns:
    -------
    A value of some sort.

    """


@expect(_D213)
@expect("D407: Missing dashed underline after section ('Returns')")
def no_underline():  # noqa: D416
    """Toggle the gizmo.

    Returns
    A value of some sort.

    """


@expect(_D213)
@expect("D407: Missing dashed underline after section ('Returns')")
@expect("D414: Section has no content ('Returns')")
def no_underline_and_no_description():  # noqa: D416
    """Toggle the gizmo.

    Returns

    """


@expect(_D213)
@expect("D410: Missing blank line after section ('Returns')")
@expect("D414: Section has no content ('Returns')")
@expect("D411: Missing blank line before section ('Yields')")
@expect("D414: Section has no content ('Yields')")
def consecutive_sections():  # noqa: D416
    """Toggle the gizmo.

    Returns
    -------
    Yields
    ------

    Raises
    ------
    Questions.

    """


@expect(_D213)
@expect("D408: Section underline should be in the line following the "
        "section's name ('Returns')")
def blank_line_before_underline():  # noqa: D416
    """Toggle the gizmo.

    Returns

    -------
    A value of some sort.

    """


@expect(_D213)
@expect("D409: Section underline should match the length of its name "
        "(Expected 7 dashes in section 'Returns', got 2)")
def bad_underline_length():  # noqa: D416
    """Toggle the gizmo.

    Returns
    --
    A value of some sort.

    """


@expect(_D213)
@expect("D413: Missing blank line after last section ('Returns')")
def no_blank_line_after_last_section():  # noqa: D416
    """Toggle the gizmo.

    Returns
    -------
    A value of some sort.
    """


@expect(_D213)
@expect("D411: Missing blank line before section ('Returns')")
def no_blank_line_before_section():  # noqa: D416
    """Toggle the gizmo.

    The function's description.
    Returns
    -------
    A value of some sort.

    """


@expect(_D213)
@expect("D214: Section is over-indented ('Returns')")
def section_overindented():  # noqa: D416
    """Toggle the gizmo.

        Returns
    -------
    A value of some sort.

    """


@expect(_D213)
@expect("D215: Section underline is over-indented (in section 'Returns')")
def section_underline_overindented():  # noqa: D416
    """Toggle the gizmo.

    Returns
        -------
    A value of some sort.

    """


@expect(_D213)
@expect("D215: Section underline is over-indented (in section 'Returns')")
@expect("D413: Missing blank line after last section ('Returns')")
@expect("D414: Section has no content ('Returns')")
def section_underline_overindented_and_contentless():  # noqa: D416
    """Toggle the gizmo.

    Returns
        -------
    """


@expect(_D213)
def ignore_non_actual_section():  # noqa: D416
    """Toggle the gizmo.

    This is the function's description, which will also specify what it
    returns

    """


@expect(_D213)
@expect("D401: First line should be in imperative mood "
        "('Return', not 'Returns')")
@expect("D400: First line should end with a period (not 's')")
@expect("D415: First line should end with a period, question "
        "mark, or exclamation point (not 's')")
@expect("D205: 1 blank line required between summary line and description "
        "(found 0)")
def section_name_in_first_line():  # noqa: D416
    """Returns
    -------
    A value of some sort.

    """


@expect(_D213)
@expect("D405: Section name should be properly capitalized "
        "('Short Summary', not 'Short summary')")
@expect("D412: No blank lines allowed between a section header and its "
        "content ('Short Summary')")
@expect("D409: Section underline should match the length of its name "
        "(Expected 7 dashes in section 'Returns', got 6)")
@expect("D410: Missing blank line after section ('Returns')")
@expect("D411: Missing blank line before section ('Raises')")
@expect("D406: Section name should end with a newline "
        "('Raises', not 'Raises:')")
@expect("D407: Missing dashed underline after section ('Raises')")
def multiple_sections():  # noqa: D416
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


@expect(_D213)
def false_positive_section_prefix():  # noqa: D416
    """Toggle the gizmo.

    Parameters
    ----------
    attributes_are_fun: attributes for the function.

    """


@expect(_D213)
def section_names_as_parameter_names():  # noqa: D416
    """Toggle the gizmo.

    Parameters
    ----------
    notes : list
        A list of wonderful notes.
    examples: list
        A list of horrible examples.

    """


@expect(_D213)
@expect("D414: Section has no content ('Returns')")
def valid_google_style_section():  # noqa: D406, D407
    """Toggle the gizmo.

    Args:
        note: A random string.

    Returns:

    Raises:
        RandomError: A random error that occurs randomly.

    """


@expect(_D213)
@expect("D416: Section name should end with a semicolon "
        "('Args:', not 'Args')")
def missing_colon_google_style_section():  # noqa: D406, D407
    """Toggle the gizmo.

    Args
        note: A random string.

    """


@expect(_D213)
@expect("D417: Missing arguments in the function docstring "
        "(argument(s) 'y' missing in function "
        "'test_missing_args' docstring)")
def test_missing_args(x=1, y=2):  # noqa: D407, D407
    """Toggle the gizmo.

    Args:
        x (int): The greatest integer.

    """
