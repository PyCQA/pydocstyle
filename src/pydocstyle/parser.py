"""Python code parser."""

import ast
import logging
import textwrap
import tokenize as tk
from itertools import chain, dropwhile
from re import compile as re

import jedi
from jedi.parser.tree import is_node

try:
    from StringIO import StringIO
except ImportError:  # Python 3.0 and later
    from io import StringIO

try:
    next
except NameError:  # Python 2.5 and earlier
    nothing = object()

    def next(obj, default=nothing):
        if default == nothing:
            return obj.next()
        else:
            try:
                return obj.next()
            except StopIteration:
                return default


__all__ = ('Parser', 'Definition', 'Module', 'Package', 'Function',
           'NestedFunction', 'Method', 'Class', 'NestedClass', 'AllError',
           'StringIO', 'ParseError')


def humanize(string):
    return re(r'(.)([A-Z]+)').sub(r'\1 \2', string).lower()


class Value(object):
    """A generic object with a list of preset fields."""

    def __init__(self, *args, **kwargs):
        if all((args, kwargs)) or not any((args, kwargs)):
            raise ValueError("Must provide either args or kwargs.")
        elif args:
            if len(self._fields) != len(args):
                raise ValueError('got {} arguments for {} fields for {}: {}'
                                 .format(len(args),
                                         len(self._fields),
                                         self.__class__.__name__,
                                         self._fields))
            vars(self).update(zip(self._fields, args))
        else:
            if len(self._fields) != len(kwargs):
                raise ValueError('got {} arguments for {} fields for {}: {}'
                                 .format(len(kwargs),
                                         len(self._fields),
                                         self.__class__.__name__,
                                         self._fields))
            vars(self).update(kwargs)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return other and vars(self) == vars(other)

    def __repr__(self):
        kwargs = ', '.join('{}={!r}'.format(field, getattr(self, field))
                           for field in self._fields)
        return '{}({})'.format(self.__class__.__name__, kwargs)


class Definition(Value):
    """A Python source code definition (could be class, function, etc)."""

    _fields = ('name', 'start', 'end', 'decorators', 'docstring',
               'children', 'parent', 'skipped_error_codes')

    _human = property(lambda self: humanize(type(self).__name__))
    kind = property(lambda self: self._human.split()[-1])
    module = property(lambda self: self.parent.module)
    all = property(lambda self: self.module.all)
    _slice = property(lambda self: slice(self.start - 1, self.end))
    is_class = False

    def __iter__(self):
        return chain([self], *self.children)

    @property
    def _publicity(self):
        return {True: 'public', False: 'private'}[self.is_public]

    @property
    def source_lines(self):
        if '_source' in self._fields:
            return self._source
        else:
            return self.parent.source_lines

    @property
    def source(self):
        """Return the source code for the definition."""
        full_src = self.source_lines[self._slice]

        def is_empty_or_comment(line):
            return line.strip() == '' or line.strip().startswith('#')

        filtered_src = dropwhile(is_empty_or_comment, reversed(full_src))
        return ''.join(reversed(list(filtered_src)))

    def __str__(self):
        out = 'in {} {} `{}`'.format(self._publicity, self._human, self.name)
        if self.skipped_error_codes:
            out += ' (skipping {})'.format(self.skipped_error_codes)
        return out


class Module(Definition):
    """A Python source code module."""

    _fields = ('name', '_source', 'start', 'end', 'decorators', 'docstring',
               'children', 'parent', '_all', 'future_imports',
               'skipped_error_codes')
    _nest = staticmethod(lambda s: {'def': Function, 'class': Class}[s])
    module = property(lambda self: self)
    all = property(lambda self: self._all)

    @property
    def is_public(self):
        return not self.name.startswith('_') or self.name.startswith('__')

    def __str__(self):
        return 'at module level'


class Package(Module):
    """A package is a __init__.py module."""


class Function(Definition):
    """A Python source code function."""

    _nest = staticmethod(lambda s: {'def': NestedFunction,
                                    'class': NestedClass}[s])

    @property
    def is_public(self):
        """Return True iff this function should be considered public."""
        if self.all is not None:
            return self.name in self.all
        else:
            return not self.name.startswith('_')


class NestedFunction(Function):
    """A Python source code nested function."""

    is_public = False


class Method(Function):
    """A Python source code method."""

    @property
    def is_magic(self):
        """Return True iff this method is a magic method (e.g., `__str__`)."""
        return (self.name.startswith('__') and
                self.name.endswith('__') and
                self.name not in VARIADIC_MAGIC_METHODS)

    @property
    def is_public(self):
        """Return True iff this method should be considered public."""
        # Check if we are a setter/deleter method, and mark as private if so.
        for decorator in self.decorators:
            # Given 'foo', match 'foo.bar' but not 'foobar' or 'sfoo'
            if re(r"^{}\.".format(self.name)).match(decorator.name):
                return False
        name_is_public = (not self.name.startswith('_') or
                          self.name in VARIADIC_MAGIC_METHODS or
                          self.is_magic)
        return self.parent.is_public and name_is_public


class Class(Definition):
    """A Python source code class."""

    _nest = staticmethod(lambda s: {'def': Method, 'class': NestedClass}[s])
    is_public = Function.is_public
    is_class = True


class NestedClass(Class):
    """A Python source code nested class."""

    @property
    def is_public(self):
        """Return True iff this class should be considered public."""
        return (not self.name.startswith('_') and
                self.parent.is_class and
                self.parent.is_public)


class Decorator(Value):
    """A decorator for function, method or class."""

    _fields = 'name'.split()


class DunderAll(Value):
    """A list of exported names in a module."""
    _fields = 'names'.split()


class FutureImport(Value):
    """A list of __future__ imports in a module."""
    _fields = 'name'.split()


VARIADIC_MAGIC_METHODS = ('__init__', '__call__', '__new__')


class ParseError(Exception):
    """Raised when the parsing fails for any reason"""


class AllError(Exception):
    """Raised when there is a problem with __all__ when parsing."""

    def __init__(self, message):
        """Initialize the error with a more specific message."""
        Exception.__init__(
            self, message + textwrap.dedent("""
                That means pydocstyle cannot decide which definitions are
                public. Variable __all__ should be present at most once in
                each file, in form
                `__all__ = ('a_public_function', 'APublicClass', ...)`.
                More info on __all__: http://stackoverflow.com/q/44834/. ')
                """))


class TokenStream(object):
    def __init__(self, filelike):
        self._generator = tk.generate_tokens(filelike.readline)
        self.current = Token(*next(self._generator, None))
        self.line = self.current.start[0]
        self.log = logging.getLogger()

    def move(self):
        previous = self.current
        current = self._next_from_generator()
        self.current = None if current is None else Token(*current)
        self.line = self.current.start[0] if self.current else self.line
        return previous

    def _next_from_generator(self):
        try:
            return next(self._generator, None)
        except (SyntaxError, tk.TokenError):
            self.log.warning('error generating tokens', exc_info=True)
            return None

    def __iter__(self):
        while True:
            if self.current is not None:
                yield self.current
            else:
                return
            self.move()


class TokenKind(int):
    def __repr__(self):
        return "tk.{}".format(tk.tok_name[self])


class Token(Value):
    _fields = 'kind value start end source'.split()

    def __init__(self, *args):
        super(Token, self).__init__(*args)
        self.kind = TokenKind(self.kind)


def verify_node(node, node_type, node_value=None):
    if not (is_node(node, node_type) or
            (node_value is not None and node_value != node.value)):
        msg = 'Node type: expected {}, got {}.'.format(node_type,
                                                       node.type)
        if node_value is not None:
            msg += '\nNode value: expected {}, got {}'.format(node_value,
                                                              node.value)
        raise ValueError(msg)
    return node


class Parser(object):
    """A Python source code parser."""

    def __call__(self, *args, **kwargs):
        return self.parse(*args, **kwargs)

    def parse(self, filelike, filename):
        """Parse the given file-like object and return its Module object."""
        # TODO: fix log
        self.log = logging.getLogger()
        self.source = filelike.readlines()
        grammar = jedi.parser.load_grammar()

        source_for_jedi = u''.join(self.source)
        jedi_parser = jedi.parser.Parser(grammar=grammar,
                                         source=source_for_jedi)
        module_node = jedi_parser.module

        module_docstring = None
        if (is_node(module_node.children[0], 'simple_stmt') and
                is_node(module_node.children[0].children[0], 'string')):
            module_docstring = module_node.children[0].children[0].value

        module_children = self.get_children(module_node)
        definitions = [c for c in module_children if isinstance(c, Definition)]
        # If there are several __all__ statements, use the last one.
        dunder_all_stmts = [c for c in module_children
                            if isinstance(c, DunderAll)]
        dunder_all_names = (tuple(dunder_all_stmts[-1].names)
                            if dunder_all_stmts
                            else None)
        future_imports = tuple(c.name for c in module_children
                               if isinstance(c, FutureImport))

        cls = Package if filename.endswith('__init__.py') else Module
        module = cls(name=filename,
                     _source=self.source,
                     start=1,
                     end=len(self.source) + 1,
                     decorators=[],
                     docstring=module_docstring,
                     children=definitions,
                     parent=None,
                     _all=dunder_all_names,
                     future_imports=future_imports,
                     skipped_error_codes='')

        for child in definitions:
            child.parent = module

        return module

    def get_docstring(self, node):
        docstring = None

        docstring_node = node.children[node.children.index(':') + 1]
        # Normally a suite
        if is_node(docstring_node, 'suite'):
            # NEWLINE INDENT stmt
            docstring_node = docstring_node.children[2]

        if is_node(docstring_node, 'simple_stmt'):
            docstring_node = docstring_node.children[0]

        if docstring_node.type == 'string':
            docstring = docstring_node.get_code().strip()

        return docstring

    def handle_function(self, node, nested=False, method=False,
                        *args, **kwargs):
        if nested and not method:
            cls = NestedFunction
        else:
            cls = Method if method else Function

        docstring = self.get_docstring(node)
        children = self.get_children(node, nested=True)

        start = node.start_pos[0]
        end = node.end_pos[0]
        if start != end:
            end -= 1

        function = cls(name=str(node.name),
                       start=start,
                       end=end,
                       decorators=self.get_decorators(node),
                       docstring=docstring,
                       children=children,
                       parent=None,
                       skipped_error_codes=self.parse_skip_comment(node))

        for child in function.children:
            child.parent = function

        return [function]

    def handle_class(self, node, nested=False, *args, **kwargs):
        cls = NestedClass if nested else Class

        docstring = self.get_docstring(node)
        children = self.get_children(node, nested=True, method=True)

        start = node.start_pos[0]
        end = node.end_pos[0]
        if start != end:
            end -= 1

        klass = cls(name=str(node.name),
                    start=start,
                    end=end,
                    decorators=self.get_decorators(node),
                    docstring=docstring,
                    children=children,
                    parent=None,
                    skipped_error_codes=self.parse_skip_comment(node))

        for child in klass.children:
            child.parent = klass

        return [klass]

    def parse_skip_comment(self, node):
        """Parse a "# noqa" comment for definitions."""
        for child in node.children:
            if is_node(child, 'operator') and child.value == ':':
                break
        else:
            return ''
        line_number = child.start_pos[0]
        line = self.source[line_number - 1]
        line_stream = StringIO(line)
        # The line always ends with an NEWLINE and ENDMARKER, so we take
        # the third one from the end and check if it's a comment.
        try:
            token = list(tk.generate_tokens(line_stream.readline))[-3]
        except tk.TokenError:
            return ''
        if token[0] != tk.COMMENT:
            return ''
        comment = token[1]
        skipped_error_codes = ''
        if 'noqa: ' in comment:
            skipped_error_codes = ''.join(
                comment.split('noqa: ')[1:])
        elif comment.startswith('# noqa'):
            skipped_error_codes = 'all'
        return skipped_error_codes

    def get_children(self, node, *args, **kwargs):
        children = []
        for child in node.children:
            result = self.handle_node(child, *args, **kwargs)
            if result is not None:
                children.extend(result)
        return children

    def get_decorators(self, node):
        return [Decorator(name=d.children[1].get_code())
                for d in node.get_decorators()]

    def handle_unknown_type(self, node, *args, **kwargs):
        try:
            node.children
        except AttributeError:
            pass
        else:
            return self.get_children(node, *args, **kwargs)

    def handle_statement(self, node, nested=False, *args, **kwargs):
        if nested:
            return

        name_node, op_node, value_node = node.children
        if not (is_node(name_node, 'name') and
                str(name_node) == '__all__' and
                is_node(op_node, 'operator') and
                op_node.value == '=' and
                is_node(value_node.children[0], 'operator') and
                value_node.children[0].value in ['(', '[']):
            return

        try:
            name_list = verify_node(value_node.children[1], 'testlist_comp')
        except ValueError:
            return

        dunder_all_names = []
        for n in name_list.children:
            if is_node(n, 'string'):
                dunder_all_names.append(ast.literal_eval(n.value))
            if is_node(n, 'atom'):
                if all(is_node(c, 'string') for c in n.children):
                    dunder_all_names.append(''.join(ast.literal_eval(c.value)
                                                    for c in n.children))

        return [DunderAll(names=tuple(dunder_all_names))]

    def handle_import_from(self, node, nested=False, *args, **kwargs):
        if nested:
            return

        verify_node(node.children[0], 'keyword', 'from')

        try:
            # The next node might be an operator for relative imports, but then
            # it won't be a legal __future__ import, so we just return in that
            # case.
            package = verify_node(node.children[1], 'name')
        except ValueError:
            return
        verify_node(node.children[2], 'keyword', 'import')

        if package.value != '__future__':
            return

        for child in node.children[3:]:
            if not(is_node(child, 'operator')):
                next_node = child
                break

        class FutureImportParser(object):
            def handle_name(self, node):
                verify_node(node, 'name')
                return [FutureImport(name=node.value)]

            def handle_import_as_name(self, node):
                original_name_node = verify_node(node.children[0], 'name')
                verify_node(node.children[1], 'keyword', 'as')
                verify_node(node.children[2], 'name')
                return [FutureImport(name=original_name_node.value)]

            def handle_import_as_names(self, node):
                return sum((self.handle(child) for child in node.children), [])

            def handle(self, node):
                handlers = {
                    'import_as_name': self.handle_import_as_name,
                    'import_as_names': self.handle_import_as_names,
                    'name': self.handle_name,
                }

                handler = handlers.get(node.type, lambda node: [])
                return handler(node)

        return FutureImportParser().handle(next_node)

    def handle_node(self, node, *args, **kwargs):
        handlers = {
            'funcdef': self.handle_function,
            'classdef': self.handle_class,
            'suite': self.get_children,
            'decorated': self.get_children,
            'expr_stmt': self.handle_statement,
            'import_from': self.handle_import_from,
        }

        handler = handlers.get(node.type, self.handle_unknown_type)
        return handler(node, *args, **kwargs)
