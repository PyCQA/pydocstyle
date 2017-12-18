"""Parser tests."""

import six
import sys
import pytest
import textwrap
from pydocstyle.parser import Parser, ParseError


class CodeSnippet(six.StringIO):
    """A code snippet.

    Automatically wraps snippet as a file-like object and handles line wraps.

    """

    def __init__(self, code_string):
        """Initialize the object."""
        six.StringIO.__init__(self, textwrap.dedent(code_string))


def test_function():
    """Test parsing of a simple function."""
    parser = Parser()
    code = CodeSnippet("""\
        def do_something(pos_param0, pos_param1, kw_param0="default"):
            \"""Do something.\"""
            return None
    """)
    module = parser.parse(code, 'file_path')
    assert module.is_public
    assert module.all is None

    function, = module.children
    assert function.name == 'do_something'
    assert function.decorators == []
    assert function.children == []
    assert function.docstring == '"""Do something."""'
    assert function.docstring.start == 2
    assert function.docstring.end == 2
    assert function.kind == 'function'
    assert function.parent == module
    assert function.start == 1
    assert function.end == 3
    assert function.error_lineno == 2
    assert function.source == code.getvalue()
    assert function.is_public
    assert str(function) == 'in public function `do_something`'


def test_decorated_function():
    """Test parsing of a simple function with a decorator."""
    parser = Parser()
    code = CodeSnippet("""\
        @single_decorator
        def do_something():
            \"""Do something.\"""
            return None
    """)
    module = parser.parse(code, 'file_path')
    function, = module.children
    assert function.name == 'do_something'
    assert len(function.decorators) == 1
    assert function.decorators[0].name == 'single_decorator'
    assert function.children == []
    assert function.docstring == '"""Do something."""'
    assert function.kind == 'function'
    assert function.parent == module
    assert function.start == 2
    assert function.end == 4
    assert function.source == textwrap.dedent("""\
        def do_something():
            \"""Do something.\"""
            return None
    """)
    assert function.is_public
    assert str(function) == 'in public function `do_something`'


def test_nested_function():
    """Test parsing of a nested function."""
    parser = Parser()
    code = CodeSnippet("""\
        def outer_function():
            \"""This is the outer function.\"""
            def inner_function():
                '''This is the inner function.'''
                return None
            return None
    """)
    module = parser.parse(code, 'file_path')

    outer_function, = module.children
    assert outer_function.name == 'outer_function'
    assert outer_function.decorators == []
    assert outer_function.docstring == '"""This is the outer function."""'
    assert outer_function.kind == 'function'
    assert outer_function.parent == module
    assert outer_function.start == 1
    assert outer_function.end == 6
    assert outer_function.error_lineno == 2
    assert outer_function.source == code.getvalue()
    assert outer_function.is_public
    assert str(outer_function) == 'in public function `outer_function`'

    inner_function, = outer_function.children
    assert inner_function.name == 'inner_function'
    assert inner_function.decorators == []
    assert inner_function.docstring == "'''This is the inner function.'''"
    assert inner_function.kind == 'function'
    assert inner_function.parent == outer_function
    assert inner_function.start == 3
    assert inner_function.end == 5
    assert inner_function.error_lineno == 4
    assert textwrap.dedent(inner_function.source) == textwrap.dedent("""\
        def inner_function():
            '''This is the inner function.'''
            return None
    """)
    assert not inner_function.is_public
    assert str(inner_function) == 'in private nested function `inner_function`'


def test_conditional_nested_function():
    """Test parsing of a nested function inside a condition."""
    parser = Parser()
    code = CodeSnippet("""\
        def outer_function():
            \"""This is the outer function.\"""
            if True:
                def inner_function():
                    '''This is the inner function.'''
                    return None
            return None
    """)
    module = parser.parse(code, 'file_path')

    outer_function, = module.children
    assert outer_function.name == 'outer_function'
    assert outer_function.decorators == []
    assert outer_function.docstring == '"""This is the outer function."""'
    assert outer_function.kind == 'function'
    assert outer_function.parent == module
    assert outer_function.start == 1
    assert outer_function.end == 7
    assert outer_function.source == code.getvalue()
    assert outer_function.is_public
    assert str(outer_function) == 'in public function `outer_function`'

    inner_function, = outer_function.children
    assert inner_function.name == 'inner_function'
    assert inner_function.decorators == []
    assert inner_function.docstring == "'''This is the inner function.'''"
    assert inner_function.kind == 'function'
    assert inner_function.parent == outer_function
    assert inner_function.start == 4
    assert inner_function.end == 6
    assert textwrap.dedent(inner_function.source) == textwrap.dedent("""\
        def inner_function():
            '''This is the inner function.'''
            return None
    """)
    assert not inner_function.is_public
    assert str(inner_function) == 'in private nested function `inner_function`'


def test_doubly_nested_function():
    """Test parsing of a nested function inside a nested function."""
    parser = Parser()
    code = CodeSnippet("""\
        def outer_function():
            \"""This is the outer function.\"""
            def middle_function():
                def inner_function():
                    '''This is the inner function.'''
                    return None
            return None
    """)
    module = parser.parse(code, 'file_path')

    outer_function, = module.children
    assert outer_function.name == 'outer_function'
    assert outer_function.decorators == []
    assert outer_function.docstring == '"""This is the outer function."""'
    assert outer_function.kind == 'function'
    assert outer_function.parent == module
    assert outer_function.start == 1
    assert outer_function.end == 7
    assert outer_function.source == code.getvalue()
    assert outer_function.is_public
    assert str(outer_function) == 'in public function `outer_function`'

    middle_function, = outer_function.children
    assert middle_function.name == 'middle_function'
    assert middle_function.decorators == []
    assert middle_function.docstring is None
    assert middle_function.kind == 'function'
    assert middle_function.parent == outer_function
    assert middle_function.start == 3
    assert middle_function.end == 6
    assert textwrap.dedent(middle_function.source) == textwrap.dedent("""\
        def middle_function():
            def inner_function():
                '''This is the inner function.'''
                return None
    """)
    assert not middle_function.is_public
    assert (str(middle_function) ==
            'in private nested function `middle_function`')

    inner_function, = middle_function.children
    assert inner_function.name == 'inner_function'
    assert inner_function.decorators == []
    assert inner_function.docstring == "'''This is the inner function.'''"
    assert inner_function.kind == 'function'
    assert inner_function.parent == middle_function
    assert inner_function.start == 4
    assert inner_function.end == 6
    assert textwrap.dedent(inner_function.source) == textwrap.dedent("""\
        def inner_function():
            '''This is the inner function.'''
            return None
    """)
    assert not inner_function.is_public
    assert str(inner_function) == 'in private nested function `inner_function`'


def test_class():
    """Test parsing of a class."""
    parser = Parser()
    code = CodeSnippet("""\
        class TestedClass(object):

            "   an ugly docstring "
    """)
    module = parser.parse(code, 'file_path')

    klass, = module.children
    assert klass.name == 'TestedClass'
    assert klass.decorators == []
    assert klass.children == []
    assert klass.docstring == '"   an ugly docstring "'
    assert klass.kind == 'class'
    assert klass.parent == module
    assert klass.start == 1
    assert klass.end == 3
    assert klass.error_lineno == 3
    assert klass.source == code.getvalue()
    assert klass.is_public
    assert str(klass) == 'in public class `TestedClass`'


def test_public_method():
    """Test parsing of a public method."""
    parser = Parser()
    code = CodeSnippet("""\
        class TestedClass(object):
            def do_it(param):
                \"""Do the 'it'\"""
                # do nothing
                return None
    """)
    module = parser.parse(code, 'file_path')

    klass, = module.children
    assert klass.name == 'TestedClass'
    assert klass.decorators == []
    assert klass.docstring is None
    assert klass.kind == 'class'
    assert klass.parent == module
    assert klass.start == 1
    assert klass.end == 5
    assert klass.error_lineno == 1
    assert klass.source == code.getvalue()
    assert klass.is_public
    assert str(klass) == 'in public class `TestedClass`'

    method, = klass.children
    assert method.name == 'do_it'
    assert method.decorators == []
    assert method.docstring == '''"""Do the 'it'"""'''
    assert method.kind == 'method'
    assert method.parent == klass
    assert method.start == 2
    assert method.end == 5
    assert method.error_lineno == 3
    assert textwrap.dedent(method.source) == textwrap.dedent("""\
        def do_it(param):
            \"""Do the 'it'\"""
            # do nothing
            return None
    """)
    assert method.is_public
    assert not method.is_magic
    assert str(method) == 'in public method `do_it`'


def test_private_method():
    """Test parsing of a private method."""
    parser = Parser()
    code = CodeSnippet("""\
        class TestedClass(object):
            def _do_it(param):
                \"""Do the 'it'\"""
                # do nothing
                return None
    """)
    module = parser.parse(code, 'file_path')

    klass, = module.children
    assert klass.name == 'TestedClass'
    assert klass.decorators == []
    assert klass.docstring is None
    assert klass.kind == 'class'
    assert klass.parent == module
    assert klass.start == 1
    assert klass.end == 5
    assert klass.error_lineno == 1
    assert klass.source == code.getvalue()
    assert klass.is_public
    assert str(klass) == 'in public class `TestedClass`'

    method, = klass.children
    assert method.name == '_do_it'
    assert method.decorators == []
    assert method.docstring == '''"""Do the 'it'"""'''
    assert method.kind == 'method'
    assert method.parent == klass
    assert method.start == 2
    assert method.end == 5
    assert method.error_lineno == 3
    assert textwrap.dedent(method.source) == textwrap.dedent("""\
        def _do_it(param):
            \"""Do the 'it'\"""
            # do nothing
            return None
    """)
    assert not method.is_public
    assert not method.is_magic
    assert str(method) == 'in private method `_do_it`'


def test_magic_method():
    """Test parsing of a magic method."""
    parser = Parser()
    code = CodeSnippet("""\
        class TestedClass(object):
            def __str__(self):
                return "me"
    """)
    module = parser.parse(code, 'file_path')

    klass, = module.children
    assert klass.name == 'TestedClass'
    assert klass.decorators == []
    assert klass.docstring is None
    assert klass.kind == 'class'
    assert klass.parent == module
    assert klass.start == 1
    assert klass.end == 3
    assert klass.error_lineno == 1
    assert klass.source == code.getvalue()
    assert klass.is_public
    assert str(klass) == 'in public class `TestedClass`'

    method, = klass.children[0]
    assert method.name == '__str__'
    assert method.decorators == []
    assert method.docstring is None
    assert method.kind == 'method'
    assert method.parent == klass
    assert method.start == 2
    assert method.end == 3
    assert method.error_lineno == 2
    assert textwrap.dedent(method.source) == textwrap.dedent("""\
        def __str__(self):
            return "me"
    """)
    assert method.is_public
    assert method.is_magic
    assert str(method) == 'in public method `__str__`'


def test_nested_class():
    """Test parsing of a class."""
    parser = Parser()
    code = CodeSnippet("""\
        class OuterClass(object):
            '   an outer docstring'
            class InnerClass(object):
                "An inner docstring."
    """)
    module = parser.parse(code, 'file_path')

    outer_class, = module.children
    assert outer_class.name == 'OuterClass'
    assert outer_class.decorators == []
    assert outer_class.docstring == "'   an outer docstring'"
    assert outer_class.kind == 'class'
    assert outer_class.parent == module
    assert outer_class.start == 1
    assert outer_class.end == 4
    assert outer_class.error_lineno == 2
    assert outer_class.source == code.getvalue()
    assert outer_class.is_public
    assert str(outer_class) == 'in public class `OuterClass`'

    inner_class, = outer_class.children
    assert inner_class.name == 'InnerClass'
    assert inner_class.decorators == []
    assert inner_class.children == []
    assert inner_class.docstring == '"An inner docstring."'
    assert inner_class.kind == 'class'
    assert inner_class.parent == outer_class
    assert inner_class.start == 3
    assert inner_class.end == 4
    assert inner_class.error_lineno == 4
    assert textwrap.dedent(inner_class.source) == textwrap.dedent("""\
        class InnerClass(object):
            "An inner docstring."
    """)
    assert inner_class.is_public
    assert str(inner_class) == 'in public nested class `InnerClass`'


@pytest.mark.skipif(six.PY2, reason='`raise from` is invalid in Python 2.x')
def test_raise_from():
    """Make sure 'raise x from y' doesn't trip the parser."""
    parser = Parser()
    code = CodeSnippet("raise ValueError() from None")
    parser.parse(code, 'file_path')


@pytest.mark.skipif(six.PY2, reason='Matrix multiplication operator is '
                                    'invalid in Python 2.x')
def test_simple_matrix_multiplication():
    """Make sure 'a @ b' doesn't trip the parser."""
    if sys.version_info.minor < 5:
        return
    parser = Parser()
    code = CodeSnippet("""
        def foo():
            a @ b
    """)
    parser.parse(code, 'file_path')


@pytest.mark.skipif(six.PY2, reason='Matrix multiplication operator is '
                                    'invalid in Python 2.x')
def test_matrix_multiplication_with_decorators():
    """Make sure 'a @ b' doesn't trip the parser."""
    if sys.version_info.minor < 5:
        return
    parser = Parser()
    code = CodeSnippet("""
        def foo():
            a @ b
            (a
            @b)
            @a
            def b():
                pass
    """)
    module = parser.parse(code, 'file_path')

    outer_function, = module.children
    assert outer_function.name == 'foo'

    inner_function, = outer_function.children
    assert len(inner_function.decorators) == 1
    assert inner_function.decorators[0].name == 'a'


def test_module_publicity():
    """Test that a module that has a single leading underscore is private."""
    parser = Parser()
    code = CodeSnippet("")

    module = parser.parse(code, "filepath")
    assert module.is_public

    module = parser.parse(code, "_filepath")
    assert not module.is_public

    module = parser.parse(code, "__filepath")
    assert module.is_public


def test_complex_module():
    """Test that a complex module is parsed correctly."""
    parser = Parser()
    code = CodeSnippet('''\
        """Module."""
        __all__ = ('a', 'b'
                   'c',)
        def function():
            "Function."
            def nested_1():
                """Nested."""
            if True:
                def nested_2():
                    pass
        class class_(object):
            """Class."""
            def method_1(self):
                """Method."""
            def method_2(self):
                def nested_3(self):
                    """Nested."""
    ''')

    module = parser.parse(code, "filepath")
    assert list(module)[0] == module
    assert len(list(module)) == 8


@pytest.mark.parametrize("code", (
    CodeSnippet("""\
        __all__ = ['foo', 'bar']
    """),
    CodeSnippet("""\
        __all__ = ['foo', 'ba'
                   'r',]
    """),
    CodeSnippet("""\
        __all__ = ('foo',
                   'bar'
        )
    """),
    CodeSnippet("""\
        __all__ = ['foo',
            # Inconvenient comment
                   'bar'
        ]
    """),
))
def test_dunder_all(code):
    """Test that __all__ is parsed correctly."""
    parser = Parser()
    module = parser.parse(code, "filepath")
    assert module.all == ('foo', 'bar')


@pytest.mark.parametrize("code", (
    CodeSnippet("""\
        from __future__ import unicode_literals, nested_scopes
    """),
    CodeSnippet("""\
        from __future__ import unicode_literals, nested_scopes;
    """),
    CodeSnippet("""\
        from __future__ import unicode_literals
        from __future__ import nested_scopes;
    """),
    CodeSnippet("""\
        from __future__ import unicode_literals
        from __future__ import nested_scopes as ns
    """),
    CodeSnippet("""\
        from __future__ import (unicode_literals as nl,
                                nested_scopes)
    """),
    CodeSnippet("""\
        from __future__ import (unicode_literals as nl,)
        from __future__ import (nested_scopes)
    """),
    CodeSnippet("""\
        from __future__ \\
        import unicode_literals
        from __future__ \\
        import nested_scopes
    """),

    # The following code snippet fails for PyPy, see:
    # "Future statements are considered illegal if they are separated
    # by a semicolon"
    # https://bitbucket.org/pypy/pypy/issues/2526/

    # CodeSnippet("""\
    #     from __future__ import unicode_literals; from __future__ import \
    #     nested_scopes
    # """),
))
def test_future_import(code):
    """Test that __future__ imports are properly parsed and collected."""
    parser = Parser()
    module = parser.parse(code, "filepath")
    assert module.future_imports == {'unicode_literals', 'nested_scopes'}


def test_noqa_function():
    """Test that "# noqa" comments are correctly collected for definitions."""
    code = CodeSnippet("""\
    def foo():  # noqa: D100,D101
        pass
    """)
    parser = Parser()
    module = parser.parse(code, "filepath")
    function, = module.children
    assert function.skipped_error_codes == 'D100,D101'


@pytest.mark.parametrize("code", (
    CodeSnippet("""\
        while True:
            try:
                pass
    """),
    CodeSnippet("[\n"),
    # Should result in `SyntaxError: from __future__ imports must occur
    # at the beginning of the file`
    CodeSnippet("""\
        from __future__ import unicode_literals; import string; from \
        __future__ import nested_scopes
    """),
))
def test_invalid_syntax(code):
    """Test invalid code input to the parser."""
    parser = Parser()
    with pytest.raises(ParseError):
        module = parser.parse(code, "filepath")
