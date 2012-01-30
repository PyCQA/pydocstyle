import re
import inspect
from io import StringIO
import tokenize as tk

def yield_list(f):
    return lambda *arg, **kw: list(f(*arg, **kw))


def abs_char(marker, source):
    """Get absolute char position in source based on (line, char) marker."""
    line, char = marker
    lines = StringIO(source).readlines()
    return len(''.join(lines[:line - 1])) + char


def parse_module_docstrings(source):
    for kind, value, _, _, _ in tk.generate_tokens(StringIO(source).readline):
        if kind in [tk.COMMENT, tk.NEWLINE, tk.NL]:
            continue
        elif kind == tk.STRING:
            docstring = value
            return [(docstring, source)]
        else:
            return [(None, source)]


def parse_docstring(source):
    """Parse docstring given `def` or `class` source."""
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
        yield source[abs_char(start, source): abs_char(end, source)]


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
        yield source[abs_char(start, source): abs_char(end, source)]


@yield_list
def parse_docstrings(source, scope):
    token_gen = tk.generate_tokens(StringIO(source).readline)
    kind = None
    while kind != tk.ENDMARKER:
        kind, value, _, _, _ = skip_til_scope(token_gen, scope)
        if kind != tk.ENDMARKER:
            for kind, value, _, _, _ in token_gen:
                if kind in [tk.COMMENT, tk.NEWLINE, tk.NL, tk.INDENT]:
                    continue
                elif kind == tk.STRING:
                    docstring = value
                    context = source[:source.find(docstring) + len(docstring)]
                    #yield (context, docstring)
                    yield docstring
                    break
                else:
                    break
        if scope == 'module':
            return


def skip_til_scope(token_gen, scope):
    kind, value, start, end, line = next(token_gen)
    if scope == 'module':
        return kind, value, start, end, line
    while kind != tk.NAME or value != scope: # and kind != tk.ENDMARKER:
        kind, value, start, end, line = next(token_gen)
    while kind != tk.OP or value != ':': # and kind != tk.ENDMARKER:
        kind, value, start, end, line = next(token_gen)
    return kind, value, start, end, line


def next_docstring(token_gen):
    kind, value, start, end, line = next(token_gen)
    while kind in [tk.COMMENT, tk.NEWLINE, tk.NL]:
        kind, value, start, end, line = next(token_gen)

def parse_class_docstrings(source):
    g = tk.generate_tokens(StringIO(source).readline)
    for t in g:
        print t
    g = tk.generate_tokens(StringIO(source).readline)
    kind, value, _, _, _ = next(g)
    while kind != tk.ENDMARKER:
        while kind != tk.NAME and value != 'class' or kind != tk.ENDMARKER:
            kind, value, _, _, _ = next(g)
        while kind != tk.OP and value != ':' or kind != tk.ENDMARKER:
            kind, value, _, _, _ = next(g)
        while kind not in [tk.COMMENT, tk.NEWLINE, tk.NL] or \
                                           kind != tk.ENDMARKER:
            kind, value, _, _, _ = next(g)
            if kind in [tk.COMMENT, tk.NEWLINE, tk.NL]:
                continue
            elif kind == tk.STRING:
                docstring = value
                context = source[:source.find(docstring) + len(docstring)]
                yield (context, docstring)


def parse_def_docstrings(s):
    return docstring, context

keywords = ['docstring', 'module_docstring',
            'class_docstring', 'function_docstring',
            'context', 'module_context',
            'class_context', 'function_context']

def checks(keyword):
    checks = []
    for function in globals().values():
        if not inspect.isfunction(function):
            continue
        args = inspect.getargspec(function)[0]
        if len(args) == 1 and args[0] == keyword:
            checks.append(function)
    return sorted(checks)


def char_line(char, file):
    return line, char


class Error(object):
    def __init__(self, filename, file, start, end, code, message, description):
        self.filename
        self.start
        self.line
        self.char
        self.end
        self.end_line
        self.end_char
        self.code
        self.message
        self.description
    def __str__(self):
        # pep8.py:203:5 Line break before docstring in function.
        # pep8.py:234:5 Summary not in imperative mood.
        # pep8.py:203:5..203:9 CE01 Line break before docstring in function.
        # pep8.py:234:5..235:10 DW01 Summary not in imperative mood.
        pass
    def __cmp__(self):
        pass


keywords = ['docstring', 'module_docstring',
            'class_docstring', 'def_docstring',
            'context', 'module_context',
            'class_context', 'def_context']


def check_source(source, name=''):

    module_contexts, module_docstrings = zip(*parse_module_docstrings(source))
    class_contexts, class_docstrings = zip(*parse_class_docstrings(source))
    def_contexts, def_docstrings = zip(*parse_def_docstrings(source))

    docstrings = module_docstrings + class_docstrings + def_docstrings
    contexts = module_contexts + class_contexts + def_contexts

    errors = []
    errors += run_checks('docstring', docstrings, source, name)
    errors += run_checks('module_docstring', module_docstrings, source, name)
    errors += run_checks('class_docstring', class_docstrings, source, name)
    errors += run_checks('def_docstring', def_docstrings, source, name)
    errors += run_checks('context', contexts, source, name)
    errors += run_checks('module_context', module_contexts, source, name)
    errors += run_checks('class_context', class_contexts, source, name)
    errors += run_checks('def_context', def_contexts, source, name)

    return sorted(errors)


def run_checks(keyword, docstrings, source, name):
    for check in checks(keyword):
        for docstring in docstrings:
            if docstring and check(docstring):
                start, end, code, message = check(docstring)
                yield Error(source, name, pos + start, pos + end,
                            code, message, check.__doc__)






#
# Check functions (on docstring context)
#



#
# Check functions (on docstrings themselves)
#


def check_raises(def_docstring, context):
    pass

def check_attributes(class_docstring, context):
    pass

def check_usage(module_docstring, context):
    pass

def check_delimiters(docstring):
    pass


if __name__ == '__main__':
    main(options, arguments)
