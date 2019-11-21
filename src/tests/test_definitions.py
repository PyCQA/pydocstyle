"""Old parser tests."""

import sys
import os
import os.path
import re
import pytest
from pydocstyle.violations import Error, ErrorRegistry
from pydocstyle.checker import check


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
    'sections',
    'functions',
    'canonical_google_examples',
    'canonical_numpy_examples',
    'canonical_pep257_examples',
])
def test_all_interpreters(test_case):
    """Complex test cases that run under all interpreters."""
    run_case(test_case)


@pytest.mark.skipif(
    sys.version_info < (3, 6),
    reason="f-string support needed"
)
def test_fstrings():
    """Run the f-string test case under Python 3.6+ only."""
    # When run under Python 3.5, mypy reports a parse error for the test file,
    # because Python 3.5 doesn't support f-strings. It does not support
    # ignoring parse errors.
    #
    # To work around this, we put our code in a file that mypy cannot see. This
    # code reveals it to Python.
    from . import test_cases
    import importlib.machinery
    test_cases_dir = test_cases.__path__[0]
    loader = sys.path_importer_cache[test_cases_dir]
    loader._loaders.append(('.py36', importlib.machinery.SourceFileLoader))

    run_case('fstrings')


def run_case(test_case):
    """Run domain-specific tests from test.py file."""
    case_module = __import__(f'test_cases.{test_case}',
                             globals=globals(),
                             locals=locals(),
                             fromlist=['expectation'],
                             level=1)

    test_case_file = os.path.relpath(case_module.__file__)
    results = list(check([test_case_file],
                         select=set(ErrorRegistry.get_error_codes()),
                         ignore_decorators=re.compile(
                             'wraps|ignored_decorator')))
    for error in results:
        assert isinstance(error, Error)
    results = {(e.definition.name, e.message) for e in results}
    assert case_module.expectation.expected == results
