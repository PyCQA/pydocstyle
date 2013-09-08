#! /usr/bin/env python
"""Static analysis tool for checking docstring conventions and style.

Implemented checks cover PEP257:
http://www.python.org/dev/peps/pep-0257/

Other checks can be added, e.g. NumPy docstring
conventions:

https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt

The main repository of this program is located at:
http://github.com/GreenSteam/pep257

Adding new checks
-----------------

In order to add your own check, create a function with name
that starts with `check_`. The function should take 3
parameters:

docstring : str or None
  Docstring (if present), as it is in file (with quotes).
context : str
  Docstring's context (e.g. function's source code).
public : bool Whether
  docstring belongs to a definition listed in __all__
  variable, or (if __all__ is not defined) if it does not
  start with underscore.

Depending on 1st parameter name, the function will be
called with different type of docstring:

 * module_docstring
 * class_docstring
 * method_docstring
 * function_docstring
 * def_docstring (i.e. function-docstrings + method-docstrings)
 * docstring (i.e. all above docstring types)

E.g. the following function will be fed only class-docstrings:

    def check_something(class_docstring, context, public):
        pass

If for a certain function, class, etc. a docstring does not
exist, then `None` will be passed, which should be taken
into account.

To signify that a check passed successfully simply `return`
from the check function.  If a check failed, return `True`.
If a check failed and you can provide the precise position
where it failed, return a tuple (start_position,
end_position), where start and end positions are integers
specifying where in `context` the failure occured.

Also, see examples in "Check functions" section.

"""
import inspect
import os
import sys
import tokenize as tk
from curses.ascii import isascii
from optparse import OptionParser
from re import compile as re


__version__ = '0.2.4'
__all__ = ['check', 'collect']


try:
    from StringIO import StringIO
except ImportError:  # Python 3.0 and later
    from io import StringIO


try:
    next
except NameError:  # Python 2.5 and earlier
    def next(obj):
        return obj.next()


#
# Helper functions
#

def cached(f):
    """Memoization decorator with no cache expiration."""
    cache = {}

    def cached_func(*args, **kwargs):
        key = (args, tuple(kwargs.items()))
        if key in cache:
            return cache[key]
        else:
            res = f(*args, **kwargs)
            cache[key] = res
            return res
    return cached_func


def yield_list(f):
    """Convert generator into list-returning function (decorator)."""
    return lambda *arg, **kw: list(f(*arg, **kw))


def remove_comments(s):
    return re('#[^\n]').sub('', s)


def abs_pos(marker, source):
    """Return absolute position in source given (line, character) marker."""
    line, char = marker
    lines = StringIO(source).readlines()
    return len(''.join(lines[:line - 1])) + char


def rel_pos(abs_pos, source):
    """Given absolute position, return relative (line, character) in source."""
    lines = StringIO(source).readlines()
    nchars = len(source)
    assert nchars >= abs_pos
    while nchars > abs_pos:
        assert nchars >= abs_pos
        nchars -= len(lines[-1])
        lines.pop()
    return len(lines) + 1, abs_pos - len(''.join(lines))


def get_summary_line_info(thedocstring):
    """Get the (summary_line, line_number) tuple for the given docstring.

    The returned 'summary_line' is the pep257 summary line and 'line_number' is
    the zero-based docstring line number containing the summary line, which
    will be either 0 (zeroth line) or 1 (first line). Any docstring checks
    relating to the summary line should use this method to ensure consistent
    treatment of the summary line.

    """
    lines = eval(thedocstring).split('\n')
    first_line = lines[0].strip()
    if len(lines) == 1 or len(first_line) > 0:
        return first_line, 0
    return lines[1].strip(), 1


#
# Parsing
#


def parse_module_docstring(source):
    for kind, value, _, _, _ in tk.generate_tokens(StringIO(source).readline):
        if kind in [tk.COMMENT, tk.NEWLINE, tk.NL]:
            continue
        elif kind == tk.STRING:  # first STRING should be docstring
            return value
        else:
            return None


def parse_docstring(source, what=''):
    """Parse docstring given `def` or `class` source."""
    module_docstring = parse_module_docstring(source)
    if what.startswith('module'):
        return module_docstring
    if module_docstring:
        return module_docstring
    token_gen = tk.generate_tokens(StringIO(source).readline)
    try:
        kind = None
        while kind != tk.INDENT:
            kind, _, _, _, _ = next(token_gen)
        kind, value, _, _, _ = next(token_gen)
        if kind == tk.STRING:  # STRING after INDENT is a docstring
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


@cached
def parse_functions(source):
    return parse_top_level(source, 'def')


@cached
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


@cached
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
        return ([parse_module_docstring(source)] + parse_functions(source) +
                parse_classes(source) + parse_methods(source))


#
# Framework
#


class Error(object):

    """Error in docstring style.

    * Stores relevant data about the error,
    * provides format for printing an error,
    * provides __lt__ method to sort errors.

    """

    # options that define how errors are printed
    explain = False
    range = False
    quote = False
    code = ''

    def __init__(self, filename, source, docstring, context,
                 explanation, code, start=None, end=None):
        self.filename = filename
        self.source = source
        self.docstring = docstring
        self.context = context
        self.explanation = explanation.strip()
        self.code = code

        if start is None:
            self.start = source.find(context) + context.find(docstring)
        else:
            self.start = source.find(context) + start
        self.line, self.char = rel_pos(self.start, self.source)

        if end is None:
            self.end = self.start + len(docstring)
        else:
            self.end = source.find(context) + end
        self.end_line, self.end_char = rel_pos(self.end, self.source)

    def __str__(self):
        s = self.filename + ':%d:%d' % (self.line, self.char)
        if self.range:
            s += '..%d:%d' % (self.end_line, self.end_char)
        if self.explain:
            s += ': ' + self.explanation + '\n'
        else:
            s += ': ' + self.explanation.split('\n')[0].strip()
        if self.quote:
            quote = self.source[self.start:self.end].strip()
            s += '\n>     ' + '\n> '.join(quote.split('\n')) + '\n'
        return s

    __repr__ = __str__

    def __lt__(self, other):
        return (self.filename, self.start) < (other.filename, other.start)


def find_checks(kind):
    mapping = {
        'module_docstring':   ['module_docstring'],
        'class_docstring':    ['class_docstring'],
        'method_docstring':   ['method_docstring'],
        'function_docstring': ['function_docstring'],
        'def_docstring':      ['method_docstring', 'function_docstring'],
        'docstring':          ['module_docstring', 'class_docstring',
                               'method_docstring', 'function_docstring']
    }
    for function in globals().values():
        if inspect.isfunction(function):
            if function.__name__.startswith('check_'):
                args = inspect.getargspec(function)[0]
                if args and kind in mapping.get(args[0], []):
                    yield function


find_alls = re('(?ms)^__all__[\t ]*=(.*?])').findall


class AllError(Exception):

    def __init__(self, message):
        Exception.__init__(
            self, message +
            'That means pep257 cannot decide which definitions are public. '
            'Variable __all__ should be present at most once in each file, '
            "in form `__all__ = ['a_public_function', 'APublicClass', ...]`. "
            'More info on __all__: http://stackoverflow.com/q/44834/. ')


def eval_all(source, filename):
    """Try to find and evaluate contents of __all__."""
    tokens = tk.generate_tokens(StringIO(source).readline)
    all_count = sum(1 for t in tokens if t[1] == '__all__')
    if all_count == 0:
        return None
    elif all_count == 1:
        alls = find_alls(source)
        if len(alls) == 1:
            try:
                return list(eval(alls[0], {}))
            except BaseException:
                pass
        raise AllError('Variable __all__ is found in file %s, but could '
                       'not be evaluated. ' % filename)
    else:
        raise AllError('Variable __all__ is found multiple times in file %s. '
                       % filename)


def parse_name(context, context_type):
    """Parse name of a class/function/method, fail if module."""
    if context_type in ['function_docstring', 'method_docstring']:
        return re('\s*def\s*(.*?)\(').findall(context)[0]
    if context_type == 'class_docstring':
        return re('\s*class\s*(.*?)\(').findall(context)[0]
    assert False


def is_public(context, kind, all):
    if kind == 'module_docstring':
        return True  # all modules are public
    name = parse_name(context, kind)
    if kind == 'method_docstring':
        return not name.startswith('_')
    return name in all if all is not None else not name.startswith('_')


def check_source(source, filename):
    kinds = ['module_docstring', 'function_docstring',
             'class_docstring', 'method_docstring']
            # TODO? 'nested_docstring']
    all = eval_all(source, filename)
    for kind in kinds:
        for check in find_checks(kind):
            for context in parse_contexts(source, kind):
                docstring = parse_docstring(context, kind)
                public = is_public(context, kind, all)
                result = check(docstring, context, public)
                if result:
                    positions = [] if result is True else result
                    error_code = check.__doc__[:4]
                    explanation = check.__doc__  # [5:]
                    yield Error(filename, source, docstring, context,
                                explanation, error_code, *positions)


def parse_options():
    parser = OptionParser(version=__version__,
                          usage='Usage: pep257 [options] [<file|dir>...]')
    option = parser.add_option
    option('-e', '--explain', action='store_true',
           help='show explanation of each error')
    option('-r', '--range', action='store_true',
           help='show error start..end positions')
    option('-q', '--quote', action='store_true',
           help='quote erroneous lines')
    option('--ignore', metavar='<codes>', default='',
           help='ignore a list comma-separated error codes, '
                'for example: --ignore=D101,D202')
    option('--match', metavar='<pattern>', default='(?!test_).*\.py',
           help="check only files that exactly match <pattern> regular "
                "expression; default is --match='(?!test_).*\.py' which "
                "matches files that don't start with 'test_' but end with "
                "'.py'")
    option('--match-dir', metavar='<pattern>', default='[^\.].*',
           help="search only dirs that exactly match <pattern> regular "
                "expression; default is --match-dir='[^\.].*', which matches "
                "all dirs that don't start with a dot")
    return parser.parse_args()


def collect(names, match=lambda name: True, match_dir=lambda name: True):
    """Walk dir trees under `names` and generate filnames that `match`.

    Example
    -------
    >>> sorted(collect(['non-dir.txt', './'],
    ...                match=lambda name: name.endswith('.py')))
    ['non-dir.txt', './pep257.py', './setup.py', './test_pep257.py']

    """
    for name in names:  # map(expanduser, names):
        if os.path.isdir(name):
            for root, dirs, filenames in os.walk(name):
                for dir in dirs:
                    if not match_dir(dir):
                        dirs.remove(dir)  # do not visit those dirs
                for filename in filenames:
                    if match(filename):
                        yield os.path.join(root, filename)
        else:
            yield name


def check(filenames, ignore=()):
    """Generate PEP 257 errors that exist in `filenames` iterable.

    Skips errors with error-codes defined in `ignore` iterable.

    Example
    -------
    >>> check(['pep257.py'], ignore=['D100'])
    <generator object check at 0x...>

    """
    for filename in filenames:
        try:
            with open(filename) as file:
                source = file.read()
            for error in check_source(source, filename):
                code = getattr(error, 'code', None)
                if code is not None and code not in ignore:
                    yield error
        except (EnvironmentError, AllError):
            yield sys.exc_info()[1]
        except tk.TokenError:
            yield SyntaxError('invalid syntax in file %s' % filename)


def main(options, arguments):
    Error.explain = options.explain
    Error.range = options.range
    Error.quote = options.quote
    collected = collect(arguments or ['.'],
                        match=re(options.match + '$').match,
                        match_dir=re(options.match_dir + '$').match)
    for error in check(collected, ignore=options.ignore.split(',')):
        sys.stderr.write('%s\n' % error)
    else:
        return 0
    return 1


#
# D1xx: Missing docstrings
#


def check_modules_have_docstrings(module_docstring, context, public):
    """D100: All modules should have docstrings.

    All modules should normally have docstrings.

    """
    if not module_docstring:
        return 0, min(79, len(context))
    if not eval(module_docstring).strip():
        return True


def check_def_has_docstring(def_docstring, context, public):
    """D101: Exported definitions should have docstrings.

    ...all functions and classes exported by a module should also have
    docstrings. Public methods (including the __init__ constructor)
    should also have docstrings.

    Note: exported/public definitions are either those listed in
    __all__ variable, or those that do not start with undescore.

    """
    if not public:
        return
    if not def_docstring:
        return 0, len(context.split('\n')[0])
    if not eval(def_docstring).strip():
        return True


def check_class_has_docstring(class_docstring, context, public):
    """D102: Exported classes should have docstrings.

    ...all functions and classes exported by a module should also have
    docstrings.

    Note: exported/public definitions are either those listed in
    __all__ variable, or those that do not start with undescore.

    """
    if not public:
        return
    if not class_docstring:
        return 0, len(context.split('\n')[0])
    if not eval(class_docstring).strip():
        return True


#
# D2xx: Whitespace issues
#


def check_one_liners(docstring, context, public):
    """D200: One-liner docstrings should fit on one line with quotes.

    The closing quotes are on the same line as the opening quotes.
    This looks better for one-liners.

    """
    if not docstring:
        return
    lines = docstring.split('\n')
    if len(lines) > 1:
        non_empty = [l for l in lines if any([c.isalpha() for c in l])]
        if len(non_empty) == 1:
            return True


def check_no_blank_before(def_docstring, context, public):
    """D201: No blank line before docstring in definitions.

    There's no blank line either before or after the docstring.

    """
    if not def_docstring:
        return
    before = remove_comments(context.split(def_docstring)[0])
    if before.split(':')[-1].count('\n') > 1:
        return True


def check_blank_after_summary(docstring, context, public):
    """D202: Blank line missing after one-line summary.

    Multi-line docstrings consist of a summary line just like a one-line
    docstring, followed by a blank line, followed by a more elaborate
    description. The summary line may be used by automatic indexing tools;
    it is important that it fits on one line and is separated from the
    rest of the docstring by a blank line.

    """
    if not docstring:
        return
    lines = eval(docstring).split('\n')
    if len(lines) > 1:
        (summary_line, line_number) = get_summary_line_info(docstring)
        next_line = line_number + 1
        if len(lines) <= next_line or lines[next_line].strip() != '':
            return True


def check_indent(docstring, context, public):
    """D203: The entire docstring should be indented same as code.

    The entire docstring is indented the same as the quotes at its
    first line.

    """
    if (not docstring) or len(eval(docstring).split('\n')) == 1:
        return
    non_empty_lines = [line for line in eval(docstring).split('\n')[1:]
                       if line.strip()]
    if not non_empty_lines:
        return
    indent = min([len(l) - len(l.lstrip()) for l in non_empty_lines])
    if indent != len(context.split(docstring)[0].split('\n')[-1]):
        return True


def check_blank_before_after_class(class_docstring, context, public):
    """D204: Class docstring should have 1 blank line around them.

    Insert a blank line before and after all docstrings (one-line or
    multi-line) that document a class -- generally speaking, the class's
    methods are separated from each other by a single blank line, and the
    docstring needs to be offset from the first method by a blank line;
    for symmetry, put a blank line between the class header and the
    docstring.

    """
    if not class_docstring:
        return
    before, after = context.split(class_docstring)[:2]
    before_blanks = [not line.strip() for line in before.split('\n')]
    after_blanks = [not line.strip() for line in after.split('\n')]
    if before_blanks[-3:] != [False, True, True]:
        return True
    if not all(after_blanks) and after_blanks[:3] != [True, True, False]:
        return True


def check_blank_after_last_paragraph(docstring, context, public):
    """D205: Multiline docstring should end with 1 blank line.

    The BDFL recommends inserting a blank line between the last
    paragraph in a multi-line docstring and its closing quotes,
    placing the closing quotes on a line by themselves.

    """
    if (not docstring) or len(eval(docstring).split('\n')) == 1:
        return
    blanks = [not line.strip() for line in eval(docstring).split('\n')]
    if blanks[-3:] != [False, True, True]:
        return True


#
# D3xx: Docstring formatting
#


def check_triple_double_quotes(docstring, context, public):
    r'''D300: Use """triple double quotes""".

    For consistency, always use """triple double quotes""" around
    docstrings. Use r"""raw triple double quotes""" if you use any
    backslashes in your docstrings. For Unicode docstrings, use
    u"""Unicode triple-quoted strings""".

    '''
    if docstring and '"""' in eval(docstring) and docstring.startswith(
            ("'''", "r'''", "u'''")):
        # Allow ''' quotes if docstring contains """, because otherwise
        # """ quotes could not be expressed inside docstring.  Not in PEP 257.
        return
    if docstring and not docstring.startswith(('"""', 'r"""', 'u"""')):
        return True


def check_backslashes(docstring, context, public):
    r'''D301: Use r""" if any backslashes in your docstrings.

    Use r"""raw triple double quotes""" if you use any backslashes
    (\) in your docstrings.

    '''
    # Check that docstring is raw, check_triple_double_quotes
    # ensures the correct quotes.
    if docstring and '\\' in docstring and not docstring.startswith('r'):
        return True


def check_unicode_docstring(docstring, context, public):
    r'''D302: Use u""" for Unicode docstrings.

    For Unicode docstrings, use u"""Unicode triple-quoted stringsr""".

    '''
    is_ascii = lambda string: all(isascii(char) for char in string)
    # Check that docstring is unicode, check_triple_double_quotes
    # ensures the correct quotes.
    if docstring and not is_ascii(docstring) and not docstring.startswith('u'):
        return True


#
# D4xx: Docstring content issues
#


def check_ends_with_period(docstring, context, public):
    """D400: First line should end with a period.

    The [first line of a] docstring is a phrase ending in a period.

    """
    if not docstring:
        return
    summary_line, line_number = get_summary_line_info(docstring)
    if not summary_line.endswith('.'):
        return True


def check_imperative_mood(def_docstring, context, public):
    """D401: First line should be in imperative mood ('Do', not 'Does').

    [Docstring] prescribes the function or method's effect as a command:
    ("Do this", "Return that"), not as a description; e.g. don't write
    "Returns the pathname ...".

    """
    if def_docstring and eval(def_docstring).strip():
        first_word = eval(def_docstring).strip().split()[0]
        if first_word.endswith('s') and not first_word.endswith('ss'):
            return True


def check_no_signature(def_docstring, context, public):
    """D402: First line should not be function's or method's "signature".

    The one-line docstring should NOT be a "signature" reiterating
    the function/method parameters (which can be obtained by introspection).

    """
    if not def_docstring:
        return
    def_name = context.split(def_docstring)[0].split()[1].split('(')[0]
    first_line = eval(def_docstring).split('\n')[0]
    if def_name + '(' in first_line.replace(' ', ''):
        return True


# Silence for time being, since too many false positives.
def SKIP_check_return_type(def_docstring, context, public):
    """D403: Return value type should be mentioned.

    However, the nature of the return value cannot be determined by
    introspection, so it should be mentioned.

    """
    if (not def_docstring) or not public:
        return
    if 'return' not in def_docstring.lower():
        tokens = list(tk.generate_tokens(StringIO(context).readline))
        after_return = [tokens[i + 1][0] for i, token in enumerate(tokens)
                        if token[1] == 'return']
        # Not very precise (tk.OP ';' is not taken into account).
        # Does this take into account nested functions?
        if set(after_return) - set([tk.COMMENT, tk.NL, tk.NEWLINE]) != set([]):
            return True


if __name__ == '__main__':
    try:
        sys.exit(main(*parse_options()))
    except KeyboardInterrupt:
        pass
