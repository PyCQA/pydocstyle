import os
import pytest
from ..pep257 import (StringIO, TokenStream, Parser, Error, check,
                      Module, Class, Method, Function, NestedFunction,
                      ErrorRegistry, AllError)


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
source_alt_nl_at_bracket = '''
__all__ = [

    # Inconvenient comment.
    'a', 'b' 'c',]
'''
source_unicode_literals1 = """
from __future__ import unicode_literals
"""
source_unicode_literals2 = """
from __future__ import unicode_literals;
"""
source_unicode_literals3 = """
from \
__future__ \
import \
unicode_literals
"""
source_unicode_literals4 = """
from __future__ \
import unicode_literals \
;
"""
source_unicode_literals5 = """
from __future__ import unicode_literals as foo;
"""
source_unicode_literals6 = """
from __future__ import unicode_literals as foo; import string
"""
source_multiple_future_imports1 = """
from __future__ import (nested_scopes as ns,
                        unicode_literals)
"""
source_multiple_future_imports2 = """
from __future__ import nested_scopes as ns
from __future__ import unicode_literals
"""
source_multiple_future_imports3 = """
from __future__ import nested_scopes, unicode_literals
"""
source_multiple_future_imports4 = """
from __future__ import (nested_scopes as ns, )
from __future__ import (unicode_literals)
"""
source_multiple_future_imports5 = """
from __future__ \
import nested_scopes
from __future__ \
import unicode_literals
"""
source_multiple_future_imports6 = """
from __future__ import nested_scopes; from __future__ import unicode_literals
"""
# pep257 does not detect that 'import string' prevents
# unicode_literals from being a valid __future__.
# That is detected by pyflakes.
source_multiple_future_imports7 = """
from __future__ import nested_scopes; import string; from __future__ import \
    unicode_literals
"""

source_future_import_invalid1 = """
from __future__ import unicode_literals as;
"""
source_future_import_invalid2 = """
from __future__ import unicode_literals as \
;
"""
source_future_import_invalid3 = """
from __future__ import
"""
source_future_import_invalid4 = """
from __future__ import \

"""
source_future_import_invalid5 = """
from __future__ import \
;
"""
source_future_import_invalid6 = """
from __future__ import \
;
"""
source_future_import_invalid7 = """
from __future__ import unicode_literals, (\
nested_scopes)
"""
source_future_import_invalid8 = """
from __future__ import (, )
"""

source_complex_all = '''
import foo
import bar

__all__ = (foo.__all__ +
           bar.__all)
'''


def test_parser():
    dunder_all = ('a', 'bc')
    module = parse(StringIO(source), 'file.py')
    assert len(list(module)) == 8
    assert Module('file.py', _, 1, len(source.split('\n')),
                  _, '"""Module."""', _, _, dunder_all, {}) == \
        module

    function, class_ = module.children
    assert Function('function', _, _, _, _, '"Function."', _,
                    module) == function
    assert Class('class_', _, _, _, _, '"""Class."""', _, module) == class_

    nested_1, nested_2 = function.children
    assert NestedFunction('nested_1', _, _, _, _,
                          '"""Nested."""', _, function) == nested_1
    assert NestedFunction('nested_2', _, _, _, _, None, _,
                          function) == nested_2
    assert nested_1.is_public is False

    method_1, method_2 = class_.children
    assert method_1.parent == method_2.parent == class_
    assert Method('method_1', _, _, _, _, '"""Method."""', _,
                  class_) == method_1
    assert Method('method_2', _, _, _, _, None, _, class_) == method_2

    nested_3, = method_2.children
    assert NestedFunction('nested_3', _, _, _, _,
                          '"""Nested."""', _, method_2) == nested_3
    assert nested_3.module == module
    assert nested_3.all == dunder_all

    module = parse(StringIO(source_alt), 'file_alt.py')
    assert Module('file_alt.py', _, 1, len(source_alt.split('\n')),
                  _, None, _, _, dunder_all, {}) == module

    module = parse(StringIO(source_alt_nl_at_bracket), 'file_alt_nl.py')
    assert Module('file_alt_nl.py', _, 1,
                  len(source_alt_nl_at_bracket.split('\n')), _, None, _, _,
                  dunder_all, {}) == module

    with pytest.raises(AllError):
        parse(StringIO(source_complex_all), 'file_complex_all.py')


def test_import_parser():
    for i, source_ucl in enumerate((
            source_unicode_literals1,
            source_unicode_literals2,
            source_unicode_literals3,
            source_unicode_literals4,
            source_unicode_literals5,
            source_unicode_literals6,
            ), 1):
        module = parse(StringIO(source_ucl), 'file_ucl{0}.py'.format(i))

        assert Module('file_ucl{0}.py'.format(i), _, 1,
                      _, _, None, _, _,
                      _, {'unicode_literals': True}) == module
        assert module.future_imports['unicode_literals']

    for i, source_mfi in enumerate((
            source_multiple_future_imports1,
            source_multiple_future_imports2,
            source_multiple_future_imports3,
            source_multiple_future_imports4,
            source_multiple_future_imports5,
            source_multiple_future_imports6,
            source_multiple_future_imports7,
            ), 1):
        module = parse(StringIO(source_mfi), 'file_mfi{0}.py'.format(i))
        assert Module('file_mfi{0}.py'.format(i), _, 1,
                      _, _, None, _, _,
                      _, {'unicode_literals': True, 'nested_scopes': True}) \
            == module
        assert module.future_imports['unicode_literals']

    # These are invalid syntax, so there is no need to verify the result
    for i, source_ucli in enumerate((
            source_future_import_invalid1,
            source_future_import_invalid2,
            source_future_import_invalid3,
            source_future_import_invalid4,
            source_future_import_invalid5,
            source_future_import_invalid6,
            source_future_import_invalid7,
            source_future_import_invalid8,
            ), 1):
        module = parse(StringIO(source_ucl), 'file_invalid{0}.py'.format(i))

        assert Module('file_invalid{0}.py'.format(i), _, 1,
                      _, _, None, _, _,
                      _, _) == module


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


def test_token_stream():
    stream = TokenStream(StringIO('hello#world'))
    assert stream.current.value == 'hello'
    assert stream.line == 1
    assert stream.move().value == 'hello'
    assert stream.current.value == '#world'
    assert stream.line == 1


def test_pep257():
    """Run domain-specific tests from test.py file."""
    test_cases = ('test', 'unicode_literals', 'nested_class', 'capitalization')
    for test_case in test_cases:
        case_module = __import__('test_cases.{0}'.format(test_case),
                                 globals=globals(),
                                 locals=locals(),
                                 fromlist=['expectation'],
                                 level=1)
        # from .test_cases import test
        results = list(check([os.path.join(os.path.dirname(__file__),
                                           'test_cases', test_case + '.py')],
                             select=set(ErrorRegistry.get_error_codes())))
        for error in results:
            assert isinstance(error, Error)
        results = set([(e.definition.name, e.message) for e in results])
        assert case_module.expectation.expected == results
