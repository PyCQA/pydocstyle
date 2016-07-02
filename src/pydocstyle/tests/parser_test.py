import six
import textwrap
from pydocstyle.parser import Parser


class CodeSnippet(six.StringIO):
    def __init__(self, code_string):
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
    function, = module.children
    assert function.name == 'do_something'
    assert function.decorators == []
    assert function.children == []
    assert function.docstring == '"""Do something."""'
    assert function.kind == 'function'
    assert function.parent == module
    assert function.start == 1
    assert function.end == 3
    assert function.source == code.getvalue()
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
    assert textwrap.dedent(inner_class.source) == textwrap.dedent("""\
        class InnerClass(object):
            "An inner docstring."
    """)
    assert inner_class.is_public
    assert str(inner_class) == 'in public nested class `InnerClass`'


def test_raise_from():
    """Make sure 'raise x from y' doesn't trip the parser."""
    parser = Parser()
    code = CodeSnippet("raise ValueError from None")
    parser.parse(code, 'file_path')
