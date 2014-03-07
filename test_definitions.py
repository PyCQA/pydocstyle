from pep257 import (StringIO, TokenStream, Parser,
                    Module, Class, Method, Function, NestedFunction)


_ = type('', (), dict(__repr__=lambda *a: '_', __eq__=lambda *a: True))()


parse = Parser()
source = '''
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
'''
source_alt = '''
__all__ = ['a', 'b'
           'c',]
'''


def test_parser():
    all = ('a', 'bc')
    module = parse(StringIO(source), 'file.py')
    assert len(list(module)) == 8
    assert Module('file.py', _, 1, len(source.split('\n')),
                  '"""Module."""', _, _, all) == module

    function, class_ = module.children
    assert Function('function', _, _, _, '"Function."', _, module) == function
    assert Class('class_', _, _, _, '"""Class."""', _, module) == class_

    nested_1, nested_2 = function.children
    assert NestedFunction('nested_1', _, _, _,
                          '"""Nested."""', _, function) == nested_1
    assert NestedFunction('nested_2', _, _, _, None, _, function) == nested_2
    assert nested_1.is_public is False

    method_1, method_2 = class_.children
    assert method_1.parent == method_2.parent == class_
    assert Method('method_1', _, _, _, '"""Method."""', _, class_) == method_1
    assert Method('method_2', _, _, _, None, _, class_) == method_2

    nested_3, = method_2.children
    assert NestedFunction('nested_3', _, _, _,
                          '"""Nested."""', _, method_2) == nested_3
    assert nested_3.module == module
    assert nested_3.all == all

    module = parse(StringIO(source_alt), 'file_alt.py')
    assert Module('file_alt.py', _, 1, len(source_alt.split('\n')),
                  None, _, _, all) == module


def _test_module():

    module = Module(source, 'module.py')
    assert module.source == source
    assert module.parent is None
    assert module.name == 'module'
    assert module.docstring == '"""Module docstring."""'
    assert module.is_public

    function, = module.children
    assert function.source.startswith('def function')
    assert function.source.endswith('pass\n')
    assert function.parent is module
    assert function.name == 'function'
    assert function.docstring == '"""Function docstring."""'

    #nested_function, = function.children
    #assert nested_function.source.startswith('def nested_function')
    #assert nested_function.source.endswith('pass\n')


def test_token_stream():
    stream = TokenStream(StringIO('hello#world'))
    assert stream.current.value == 'hello'
    assert stream.line == 1
    assert stream.move().value == 'hello'
    assert stream.current.value == '#world'
    assert stream.line == 1


def test_pep257():
    """Run domain-specific tests from test.py file."""
    import test
    test.run()
