import ast
import re
from collections import namedtuple

from pydocstyle import violations
from pydocstyle.checkers.hooks import check_for
from pydocstyle.checkers.utils import (
    get_docstring_indent,
    get_leading_space,
    get_leading_words
)
from pydocstyle.parser import (
    Definition,
)
from pydocstyle.utils import log, is_blank, pairwise

NUMPY_SECTION_NAMES = [
    'Short Summary',
    'Extended Summary',
    'Parameters',
    'Returns',
    'Yields',
    'Other Parameters',
    'Raises',
    'See Also',
    'Notes',
    'References',
    'Examples',
    'Attributes',
    'Methods'
]


@check_for(Definition)
def check_starts_with_this(function, docstring):
    """D404: First word of the docstring should not be `This`.

    Docstrings should use short, simple language. They should not begin
    with "This class is [..]" or "This module contains [..]".

    """
    if docstring:
        first_word = ast.literal_eval(docstring).split()[0]
        if first_word.lower() == 'this':
            return violations.D404()


@check_for(Definition)
def check_docstring_sections(definition, docstring):
    """D21{4,5}, D4{05,06,07,08,09,10}: Docstring sections checks.

    Check the general format of a sectioned docstring:
        '''This is my one-liner.

        Short Summary
        -------------
        This is my summary.

        Returns
        -------
        None.

        '''

    Section names appear in `NUMPY_SECTION_NAMES`.
    """
    if not docstring:
        return

    lines = docstring.split("\n")
    if len(lines) < 2:
        return

    lower_section_names = set(s.lower() for s in NUMPY_SECTION_NAMES)

    def _suspected_as_section(_line, valid_names):
        result = get_leading_words(_line.lower())
        return result in valid_names

    # Finding our suspects.
    suspected_section_indices = [i for i, line in enumerate(lines) if
                                    _suspected_as_section(line, lower_section_names)]

    SectionContext = namedtuple('SectionContext', ('section_name',
                                                    'previous_line',
                                                    'line',
                                                    'following_lines',
                                                    'original_index',
                                                    'is_last_section'))

    # First - create a list of possible contexts. Note that the
    # `following_lines` member is until the end of the docstring.
    contexts = (SectionContext(get_leading_words(lines[i].strip()),
                                lines[i - 1],
                                lines[i],
                                lines[i + 1:],
                                i,
                                False)
                for i in suspected_section_indices)

    # Now that we have manageable objects - rule out false positives.
    contexts = (c for c in contexts if _is_a_docstring_section(c))

    # Now we shall trim the `following lines` field to only reach the
    # next section name.
    for a, b in pairwise(contexts, None):
        end = -1 if b is None else b.original_index
        new_ctx = SectionContext(a.section_name,
                                    a.previous_line,
                                    a.line,
                                    lines[a.original_index + 1:end],
                                    a.original_index,
                                    b is None)
        for err in _check_section(docstring, definition, new_ctx):
            yield err


def _check_section(docstring, definition, context):
    """D4{05,06,10,11,13}, D214: Section name checks.

    Check for valid section names. Checks that:
        * The section name is properly capitalized (D405).
        * The section is not over-indented (D214).
        * The section name has no superfluous suffix to it (D406).
        * There's a blank line after the section (D410, D413).
        * There's a blank line before the section (D411).

    Also yields all the errors from `_check_section_underline`.
    """
    capitalized_section = context.section_name.title()
    indentation = get_docstring_indent(definition, docstring)

    if (context.section_name not in NUMPY_SECTION_NAMES and
            capitalized_section in NUMPY_SECTION_NAMES):
        yield violations.D405(capitalized_section, context.section_name)

    if get_leading_space(context.line) > indentation:
        yield violations.D214(capitalized_section)

    suffix = context.line.strip().lstrip(context.section_name)
    if suffix:
        yield violations.D406(capitalized_section, context.line.strip())

    if (not context.following_lines or
            not is_blank(context.following_lines[-1])):
        if context.is_last_section:
            yield violations.D413(capitalized_section)
        else:
            yield violations.D410(capitalized_section)

    if not is_blank(context.previous_line):
        yield violations.D411(capitalized_section)

    for err in _check_section_underline(capitalized_section,
                                            context,
                                            indentation):
        yield err


def _is_a_docstring_section(context):
    """Check if the suspected context is really a section header.

    Lets have a look at the following example docstring:
        '''Title.

        Some part of the docstring that specifies what the function
        returns. <----- Not a real section name. It has a suffix and the
                        previous line is not empty and does not end with
                        a punctuation sign.

        This is another line in the docstring. It describes stuff,
        but we forgot to add a blank line between it and the section name.
        Parameters  <-- A real section name. The previous line ends with
        ----------      a period, therefore it is in a new
                        grammatical context.
        param : int
        examples : list  <------- Not a section - previous line doesn't end
            A list of examples.   with punctuation.
        notes : list  <---------- Not a section - there's text after the
            A list of notes.      colon.

        Notes:  <--- Suspected as a context because there's a suffix to the
        -----        section, but it's a colon so it's probably a mistake.
        Bla.

        '''

    To make sure this is really a section we check these conditions:
        * There's no suffix to the section name or it's just a colon AND
        * The previous line is empty OR it ends with punctuation.

    If one of the conditions is true, we will consider the line as
    a section name.
    """
    section_name_suffix = \
        context.line.strip().lstrip(context.section_name.strip()).strip()

    section_suffix_is_only_colon = section_name_suffix == ':'

    punctuation = [',', ';', '.', '-', '\\', '/', ']', '}', ')']
    prev_line_ends_with_punctuation = \
        any(context.previous_line.strip().endswith(x) for x in punctuation)

    this_line_looks_like_a_section_name = \
        is_blank(section_name_suffix) or section_suffix_is_only_colon

    prev_line_looks_like_end_of_paragraph = \
        prev_line_ends_with_punctuation or is_blank(context.previous_line)

    return (this_line_looks_like_a_section_name and
            prev_line_looks_like_end_of_paragraph)


def _check_section_underline(section_name, context, indentation):
    """D4{07,08,09,12}, D215: Section underline checks.

    Check for correct formatting for docstring sections. Checks that:
        * The line that follows the section name contains
            dashes (D40{7,8}).
        * The amount of dashes is equal to the length of the section
            name (D409).
        * The section's content does not begin in the line that follows
            the section header (D412).
        * The indentation of the dashed line is equal to the docstring's
            indentation (D215).
    """
    blank_lines_after_header = 0

    for line in context.following_lines:
        if not is_blank(line):
            break
        blank_lines_after_header += 1
    else:
        # There are only blank lines after the header.
        yield violations.D407(section_name)
        return

    non_empty_line = context.following_lines[blank_lines_after_header]
    dash_line_found = ''.join(set(non_empty_line.strip())) == '-'

    if not dash_line_found:
        yield violations.D407(section_name)
        if blank_lines_after_header > 0:
            yield violations.D412(section_name)
    else:
        if blank_lines_after_header > 0:
            yield violations.D408(section_name)

        if non_empty_line.strip() != "-" * len(section_name):
            yield violations.D409(len(section_name),
                                    section_name,
                                    len(non_empty_line.strip()))

        if get_leading_space(non_empty_line) > indentation:
            yield violations.D215(section_name)

        line_after_dashes_index = blank_lines_after_header + 1
        # If the line index after the dashes is in range (perhaps we have
        # a header + underline followed by another section header).
        if line_after_dashes_index < len(context.following_lines):
            line_after_dashes = \
                context.following_lines[line_after_dashes_index]
            if is_blank(line_after_dashes):
                rest_of_lines = \
                    context.following_lines[line_after_dashes_index:]
                if not is_blank(''.join(rest_of_lines)):
                    yield violations.D412(section_name)
                else:
                    yield violations.D414(section_name)
        else:
            yield violations.D414(section_name)
