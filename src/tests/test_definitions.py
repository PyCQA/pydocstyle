"""Old parser tests."""

import os
import re
import pytest
from pydocstyle.violations import Error, ErrorRegistry
from pydocstyle.checker import check
from pydocstyle.parser import (Parser, Module, Function, NestedFunction,
                               Method, Class, AllError, TokenStream, StringIO)

__all__ = ()
_ = type('', (), dict(__repr__=lambda *a: '_', __eq__=lambda *a: True))()


parse = Parser()


source_invalid_syntax = """
while True:
\ttry:
    pass
"""

source_token_error = '['

source_complex_all = '''
import foo
import bar

__all__ = (foo.__all__ +
           bar.__all)
'''


def test_import_parser():
    """Test invalid code input to the parser."""
    # These are invalid syntax, so there is no need to verify the result
    for i, source_ucli in enumerate((
            source_token_error,
            source_invalid_syntax,
            ), 1):
        module = parse(StringIO(source_ucli), 'file_invalid{}.py'.format(i))

        assert Module('file_invalid{}.py'.format(i), _, 1,
                      _, _, None, _, _,
                      _, _, '') == module


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


@pytest.mark.parametrize('test_case', [
    'test',
    'unicode_literals',
    'nested_class',
    'capitalization',
    'comment_after_def_bug',
    'multi_line_summary_start',
    'all_import',
    'all_import_as',
    'superfluous_quotes',
    'noqa',
])
def test_complex_file(test_case):
    """Run domain-specific tests from test.py file."""
    case_module = __import__('test_cases.{}'.format(test_case),
                             globals=globals(),
                             locals=locals(),
                             fromlist=['expectation'],
                             level=1)
    test_case_dir = os.path.normcase(os.path.dirname(__file__))
    test_case_file = os.path.join(test_case_dir,
                                  'test_cases',
                                  test_case + '.py')
    results = list(check([test_case_file],
                         select=set(ErrorRegistry.get_error_codes()),
                         ignore_decorators=re.compile('wraps')))
    for error in results:
        assert isinstance(error, Error)
    results = set([(e.definition.name, e.message) for e in results])
    assert case_module.expectation.expected == results
