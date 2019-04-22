import ast
import re
import string
import sys

from itertools import takewhile

from pydocstyle import violations
from pydocstyle.checkers.hooks import check_for
from pydocstyle.checkers.utils import (
    get_docstring_indent,
    get_leading_space
)
from pydocstyle.parser import (
    Class,
    Definition,
    Function,
    Method,
    Module,
    NestedClass,
    NestedFunction,
    Package,
)
from pydocstyle.utils import log, is_blank, pairwise
from pydocstyle.wordlists import IMPERATIVE_VERBS, IMPERATIVE_BLACKLIST, stem


TRIPLE_QUOTES_REGEX = re.compile(r"[uU]?[rR]?'''[^'].*")
TRIPLE_DOUBLE_QUOTES_REGEX = re.compile(r'[uU]?[rR]?"""[^"].*')
ILLEGAL_QUOTES_REGEX = re.compile(r"""[uU]?[rR]?("+|'+).*""")


# ===========
# D1XX Checks
# ===========


@check_for(Definition, terminal=True)
def check_docstring_missing(definition, docstring):
    """D10{0,1,2,3}: Public definitions should have docstrings.

    All modules should normally have docstrings.  [...] all functions and
    classes exported by a module should also have docstrings. Public
    methods (including the __init__ constructor) should also have
    docstrings.

    Note: Public (exported) definitions are either those with names listed
            in __all__ variable (if present), or those that do not start
            with a single underscore.

    """
    if (not docstring and definition.is_public or
            docstring and is_blank(ast.literal_eval(docstring))):
        codes = {Module: violations.D100,
                    Class: violations.D101,
                    NestedClass: violations.D106,
                    Method: (lambda: violations.D105() if definition.is_magic
                            else (violations.D107() if definition.is_init
                            else violations.D102())),
                    Function: violations.D103,
                    NestedFunction: violations.D103,
                    Package: violations.D104}
        return codes[type(definition)]()


# ===========
# D2XX Checks
# ===========


@check_for(Definition)
def check_one_liners(definition, docstring):
    """D200: One-liner docstrings should fit on one line with quotes.

    The closing quotes are on the same line as the opening quotes.
    This looks better for one-liners.

    """
    if docstring:
        lines = ast.literal_eval(docstring).split('\n')
        if len(lines) > 1:
            non_empty_lines = sum(1 for l in lines if not is_blank(l))
            if non_empty_lines == 1:
                return violations.D200(len(lines))



@check_for(Function)
def check_no_blank_before(function, docstring):  # def
    """D20{1,2}: No blank lines allowed around function/method docstring.

    There's no blank line either before or after the docstring.

    """
    if docstring:
        before, _, after = function.source.partition(docstring)
        blanks_before = list(map(is_blank, before.split('\n')[:-1]))
        blanks_after = list(map(is_blank, after.split('\n')[1:]))
        blanks_before_count = sum(takewhile(bool, reversed(blanks_before)))
        blanks_after_count = sum(takewhile(bool, blanks_after))
        if blanks_before_count != 0:
            yield violations.D201(blanks_before_count)
        if not all(blanks_after) and blanks_after_count != 0:
            yield violations.D202(blanks_after_count)


@check_for(Class)
def check_blank_before_after_class(class_, docstring):
    """D20{3,4}: Class docstring should have 1 blank line around them.

    Insert a blank line before and after all docstrings (one-line or
    multi-line) that document a class -- generally speaking, the class's
    methods are separated from each other by a single blank line, and the
    docstring needs to be offset from the first method by a blank line;
    for symmetry, put a blank line between the class header and the
    docstring.

    """
    # NOTE: this gives false-positive in this case
    # class Foo:
    #
    #     """Docstring."""
    #
    #
    # # comment here
    # def foo(): pass
    if docstring:
        before, _, after = class_.source.partition(docstring)
        blanks_before = list(map(is_blank, before.split('\n')[:-1]))
        blanks_after = list(map(is_blank, after.split('\n')[1:]))
        blanks_before_count = sum(takewhile(bool, reversed(blanks_before)))
        blanks_after_count = sum(takewhile(bool, blanks_after))
        if blanks_before_count != 0:
            yield violations.D211(blanks_before_count)
        if blanks_before_count != 1:
            yield violations.D203(blanks_before_count)
        if not all(blanks_after) and blanks_after_count != 1:
            yield violations.D204(blanks_after_count)


@check_for(Definition)
def check_blank_after_summary(definition, docstring):
    """D205: Put one blank line between summary line and description.

    Multi-line docstrings consist of a summary line just like a one-line
    docstring, followed by a blank line, followed by a more elaborate
    description. The summary line may be used by automatic indexing tools;
    it is important that it fits on one line and is separated from the
    rest of the docstring by a blank line.

    """
    if docstring:
        lines = ast.literal_eval(docstring).strip().split('\n')
        if len(lines) > 1:
            post_summary_blanks = list(map(is_blank, lines[1:]))
            blanks_count = sum(takewhile(bool, post_summary_blanks))
            if blanks_count != 1:
                return violations.D205(blanks_count)


@check_for(Definition)
def check_indent(definition, docstring):
    """D20{6,7,8}: The entire docstring should be indented same as code.

    The entire docstring is indented the same as the quotes at its
    first line.

    """
    if docstring:
        indent = get_docstring_indent(definition, docstring)
        lines = docstring.split('\n')
        if len(lines) > 1:
            lines = lines[1:]  # First line does not need indent.
            indents = [get_leading_space(l) for l in lines if not is_blank(l)]
            if set(' \t') == set(''.join(indents) + indent):
                yield violations.D206()
            if (len(indents) > 1 and min(indents[:-1]) > indent or
                    indents[-1] > indent):
                yield violations.D208()
            if min(indents) < indent:
                yield violations.D207()


@check_for(Definition)
def check_newline_after_last_paragraph(definition, docstring):
    """D209: Put multi-line docstring closing quotes on separate line.

    Unless the entire docstring fits on a line, place the closing
    quotes on a line by themselves.

    """
    if docstring:
        lines = [l for l in ast.literal_eval(docstring).split('\n')
                    if not is_blank(l)]
        if len(lines) > 1:
            if docstring.split("\n")[-1].strip() not in ['"""', "'''"]:
                return violations.D209()


@check_for(Definition)
def check_surrounding_whitespaces(definition, docstring):
    """D210: No whitespaces allowed surrounding docstring text."""
    if docstring:
        lines = ast.literal_eval(docstring).split('\n')
        if lines[0].startswith(' ') or \
                len(lines) == 1 and lines[0].endswith(' '):
            return violations.D210()


# ===========
# D3XX Checks
# ===========


@check_for(Definition)
def check_triple_double_quotes(definition, docstring):
    r'''D300: Use """triple double quotes""".

    For consistency, always use """triple double quotes""" around
    docstrings. Use r"""raw triple double quotes""" if you use any
    backslashes in your docstrings. For Unicode docstrings, use
    u"""Unicode triple-quoted strings""".

    Note: Exception to this is made if the docstring contains
            """ quotes in its body.

    '''
    if docstring:
        if '"""' in ast.literal_eval(docstring):
            # Allow ''' quotes if docstring contains """, because
            # otherwise """ quotes could not be expressed inside
            # docstring. Not in PEP 257.
            regex = TRIPLE_QUOTES_REGEX
        else:
            regex = TRIPLE_DOUBLE_QUOTES_REGEX

        if not regex.match(docstring):
            illegal_quotes = ILLEGAL_QUOTES_REGEX.match(docstring).group(1)
            return violations.D300(illegal_quotes)



@check_for(Definition)
def check_backslashes(definition, docstring):
    r'''D301: Use r""" if any backslashes in a docstring.

    Use r"""raw triple double quotes""" if you use any backslashes
    (\) in your docstrings.

    '''
    # Just check that docstring is raw, check_triple_double_quotes
    # ensures the correct quotes.
    if docstring and '\\' in docstring and not docstring.startswith(
            ('r', 'ur')):
        return violations.D301()


@check_for(Definition)
def check_unicode_docstring(definition, docstring):
    r'''D302: Use u""" for docstrings with Unicode.

    For Unicode docstrings, use u"""Unicode triple-quoted strings""".

    '''
    if 'unicode_literals' in definition.module.future_imports:
        return

    # Just check that docstring is unicode, check_triple_double_quotes
    # ensures the correct quotes.
    if docstring and sys.version_info[0] <= 2:
        if not is_ascii(docstring) and not docstring.startswith(
                ('u', 'ur')):
            return violations.D302()


# ===========
# D4XX Checks
# ===========


@check_for(Definition)
def check_ends_with_period(definition, docstring):
    """D400: First line should end with a period.

    The [first line of a] docstring is a phrase ending in a period.

    """
    if docstring:
        summary_line = ast.literal_eval(docstring).strip().split('\n')[0]
        if not summary_line.endswith('.'):
            return violations.D400(summary_line[-1])


@check_for(Function)
def check_imperative_mood(function, docstring):  # def context
    """D401: First line should be in imperative mood: 'Do', not 'Does'.

    [Docstring] prescribes the function or method's effect as a command:
    ("Do this", "Return that"), not as a description; e.g. don't write
    "Returns the pathname ...".

    """
    if docstring and not function.is_test:
        stripped = ast.literal_eval(docstring).strip()
        if stripped:
            first_word = stripped.split()[0]
            check_word = first_word.lower()

            if check_word in IMPERATIVE_BLACKLIST:
                return violations.D401b(first_word)

            try:
                correct_form = IMPERATIVE_VERBS.get(stem(check_word))
            except UnicodeDecodeError:
                # This is raised when the docstring contains unicode
                # characters in the first word, but is not a unicode
                # string. In which case D302 will be reported. Ignoring.
                return

            if correct_form and correct_form != check_word:
                return violations.D401(
                    correct_form.capitalize(),
                    first_word
                )


@check_for(Function)
def check_no_signature(function, docstring):  # def context
    """D402: First line should not be function's or method's "signature".

    The one-line docstring should NOT be a "signature" reiterating the
    function/method parameters (which can be obtained by introspection).

    """
    if docstring:
        first_line = ast.literal_eval(docstring).strip().split('\n')[0]
        if function.name + '(' in first_line.replace(' ', ''):
            return violations.D402()


@check_for(Function)
def check_capitalized(function, docstring):
    """D403: First word of the first line should be properly capitalized.

    The [first line of a] docstring is a phrase ending in a period.

    """
    if docstring:
        first_word = ast.literal_eval(docstring).split()[0]
        if first_word == first_word.upper():
            return
        for char in first_word:
            if char not in string.ascii_letters and char != "'":
                return
        if first_word != first_word.capitalize():
            return violations.D403(first_word.capitalize(), first_word)
