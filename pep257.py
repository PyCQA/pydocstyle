#!/usr/bin/env python

import inspect
from StringIO import StringIO
from optparse import OptionParser
import tokenize as tk


def yield_list(f):
    return lambda *arg, **kw: list(f(*arg, **kw))


def abs_pos(marker, source):
    """Get absolute char position in source based on (line, char) marker."""
    line, char = marker
    lines = StringIO(source).readlines()
    return len(''.join(lines[:line - 1])) + char


def rel_pos(char, source):
    """Get relative (line, char) position in source based on absolute char."""
    lines = StringIO(source).readlines()
    assert len(''.join(lines)) >= char
    while len(''.join(lines)) > char:
        assert len(''.join(lines)) >= char
        lines.pop()
    return len(lines) + 1, char - len(''.join(lines))


def parse_module_docstring(source):
    for kind, value, _, _, _ in tk.generate_tokens(StringIO(source).readline):
        if kind in [tk.COMMENT, tk.NEWLINE, tk.NL]:
            continue
        elif kind == tk.STRING:
            docstring = value
            return docstring


def parse_docstring(source, what=''):
    """Parse docstring given `def` or `class` source."""
    if what.startswith('module'):
        return parse_module_docstring(source)
    token_gen = tk.generate_tokens(StringIO(source).readline)
    try:
        kind = None
        while kind != tk.INDENT:
            kind, _, _, _, _ = next(token_gen)
        kind, value, _, _, _ = next(token_gen)
        if kind == tk.STRING:
            return value
    except StopIteration:
        pass


@yield_list
def parse_top_level(source, keyword):
    """Parse top-level functions or classes."""
    token_gen = tk.generate_tokens(StringIO(source).readline)
    kind, value, char = None, None, None
    while True:
        start, end = None, None
        while not (kind == tk.NAME and value == keyword and char == 0):
            kind, value, (line, char), _, _ = next(token_gen)
        start = line, char
        while not (kind == tk.DEDENT and value == '' and char == 0):
            kind, value, (line, char), _, _ = next(token_gen)
        end = line, char
        yield source[abs_pos(start, source): abs_pos(end, source)]


def parse_functions(source):
    return parse_top_level(source, 'def')


def parse_classes(source):
    return parse_top_level(source, 'class')


def skip_indented_block(token_gen):
    kind, value, start, end, raw = next(token_gen)
    while kind != tk.INDENT:
        kind, value, start, end, raw = next(token_gen)
    indent = 1
    for kind, value, start, end, raw in token_gen:
        if kind == tk.INDENT:
            indent += 1
        elif kind == tk.DEDENT:
            indent -= 1
        if indent == 0:
            return kind, value, start, end, raw


@yield_list
def parse_methods(source):
    source = ''.join(parse_classes(source))
    token_gen = tk.generate_tokens(StringIO(source).readline)
    kind, value, char = None, None, None
    while True:
        start, end = None, None
        while not (kind == tk.NAME and value == 'def'):
            kind, value, (line, char), _, _ = next(token_gen)
        start = line, char
        kind, value, (line, char), _, _ = skip_indented_block(token_gen)
        end = line, char
        yield source[abs_pos(start, source): abs_pos(end, source)]


@yield_list
def find_checks(keyword):
    for function in globals().values():
        if not inspect.isfunction(function):
            continue
        arg = inspect.getargspec(function)[0]
        if arg and arg[0] == keyword:
            yield function


def parse_contexts(source, kind):
    if kind == 'module_docstring':
        return [source]
    if kind == 'function_docstring':
        return parse_functions(source)
    if kind == 'class_docstring':
        return parse_classes(source)
    if kind == 'method_docstring':
        return parse_methods(source)
    if kind == 'def_docstring':
        return parse_functions(source) + parse_methods(source)
    if kind == 'docstring':
        return ([source] + parse_functions(source) +
                parse_classes(source) + parse_methods(source))


@yield_list
def check_source(source, filename=''):
    keywords = ['module_docstring', 'function_docstring',
                'class_docstring', 'method_docstring',
                'def_docstring', 'docstring']  # TODO? 'nested_docstring']
    for keyword in keywords:
        for check in find_checks(keyword):
            for context in parse_contexts(source, keyword):
                docstring = parse_docstring(context, keyword)
                result = check(docstring, context)
                if result is not None:
                    yield Error(filename, source, docstring, context,
                                check.__doc__, *result)


class Error(object):

    options = None  # optparse options that define e.g. how errors are printed

    def __init__(self, filename, source, docstring, context,
                 explanation, message, start=None, end=None):
        self.filename = filename
        self.source = source
        self.docstring = docstring
        self.context = context
        self.message = message
        self.explanation = explanation

        if start is None:
            self.start = source.find(docstring)
        else:
            self.start = source.find(context) + start
        self.line, self.char = rel_pos(self.start, self.source)

        if end is None:
            self.end = self.start + len(docstring)
        else:
            self.end = source.find(context) + end
        self.end_line, self.end_char = rel_pos(self.end, self.source)

    def __str__(self):
        # pep8.py:203:5 Line break before docstring in function.
        # pep8.py:234:5 Summary not in imperative mood.
        # pep8.py:203:5..203:9 CE01 Line break before docstring in function.
        # pep8.py:234:5..235:10 DW01 Summary not in imperative mood.
        s = self.filename + ':%d:%d' % (self.line, self.char)
        if self.options.range:
            s += '..%d:%d' % (self.end_line, self.end_char)
        s += ': ' + self.message + '\n'
        if self.options.explain:
            s += self.explanation
        if self.options.quote:
            s += self.source[self.start:self.end]
        return s
    def __cmp__(self, other):
        return cmp((self.filename, self.start), (other.filename, other.start))


def parse_options():
    parser = OptionParser()
    parser.add_option('-e', '--explain', action='store_true',
                      help='show explanation of each error')
    parser.add_option('-r', '--range', action='store_true',
                      help='show error start..end positions')
    parser.add_option('-q', '--quote', action='store_true',
                      help='quote erroneous line(s)')
    return parser.parse_args()


def main(options, arguments):
    Error.options = options
    errors = []
    for filename in arguments:
        errors.append(check_source(''.join(open(filename)), filename))
    for error in sorted(errors):
        print error[0]


#
# Check functions
#


def check_raises(def_docstring, context):
    pass

def check_attributes(class_docstring, context):
    pass

def check_usage(module_docstring, context):
    pass

def check_tripple_double_quotes(docstring, context):
    '''PEP257 Use """tripple double quotes""".

    For consistency, always use """triple double quotes""" around
    docstrings. Use r"""raw triple double quotes""" if you use any
    backslashes in your docstrings. For Unicode docstrings, use
    u"""Unicode triple-quoted strings""".

    '''
    if not docstring:
        return
    if not (docstring.startswith('"""') or
            docstring.startswith('r"""') or
            docstring.startswith('u"""')):
        return 'PEP257 Use """tripple double quotes""".',


if __name__ == '__main__':
    try:
        main(*parse_options())
    except KeyboardInterrupt:
        pass
