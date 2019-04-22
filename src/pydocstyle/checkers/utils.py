import re

_LEADING_SPACE_REGEX = re.compile("\s*")
_LEADING_WORDS_REGEX = re.compile("[\w ]+")

def get_leading_space(string):
    return _LEADING_SPACE_REGEX.match(string).group()


def get_docstring_indent(definition, docstring):
    """Return the indentation of the docstring's opening quotes."""
    before_docstring, _, _ = definition.source.partition(docstring)
    _, _, indent = before_docstring.rpartition('\n')
    return indent


def get_leading_words(line):
    """Return any leading set of words from `line`.

    For example, if `line` is "  Hello world!!!", returns "Hello world".
    """
    result = _LEADING_WORDS_REGEX.match(line.strip())
    if result:
        return result.group()
