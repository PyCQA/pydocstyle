"""Use tox or py.test to run the test-suite."""
# -*- coding: utf-8 -*-
from __future__ import with_statement

from pytest import skip

import pep257


__all__ = []


@skip
def test_pep257_conformance():
    errors = list(pep257.check(['pep257.py', 'test_pep257.py']))
    print(errors)
    assert len(errors) == 0


def test_get_summary_line_info():
    s1 = '''"""First line summary."""'''
    s2 = '''"""First line summary.
    With subsequent line.
    """'''
    s3 = '''""""""'''
    s4 = '''"""
    Second line summary.
    """'''
    s5 = '''"""
    Second line summary.
    With subsquent line.
    """'''
    assert pep257.get_summary_line_info(s1) == ('First line summary.', 0)
    assert pep257.get_summary_line_info(s2) == ('First line summary.', 0)
    assert pep257.get_summary_line_info(s3) == ('', 0)
    assert pep257.get_summary_line_info(s4) == ('Second line summary.', 1)
    assert pep257.get_summary_line_info(s5) == ('Second line summary.', 1)


def test_parse_docstring():
    s1 = '''def foo():  # o hai comment
    """docstring"""
    2 + 2'''
    assert pep257.parse_docstring(s1) == '"""docstring"""'

    s2 = '''def foo():  # o hai comment
    2 + 2'''
    assert pep257.parse_docstring(s2) is None

    assert pep257.parse_docstring("def foo():pass") is None
    # TODO
    # assert pep257.parse_docstring("def bar():'doc';pass") == "'doc'"


def test_abs_pos():
    assert pep257.abs_pos((1, 0), 'foo') == 0
    assert pep257.abs_pos((1, 2), 'foo') == 2
    assert pep257.abs_pos((2, 0), 'foo\nbar') == 4


def test_rel_pos():
    assert pep257.rel_pos(0, 'foo') == (1, 0)
    assert pep257.rel_pos(2, 'foo') == (1, 2)
    assert pep257.rel_pos(4, 'foo\nbar') == (2, 0)
    assert pep257.rel_pos(6, 'foo\nbar') == (2, 2)


def test_parse_functions():
    parse = pep257.parse_functions
    assert parse('') == []
    # TODO assert pf('def foo():pass') == ['def foo():pass']
    assert parse('def foo():\n    pass\n') == ['def foo():\n    pass\n']
    assert parse('def foo():\n  pass') == ['def foo():\n  pass']
    f1 = '''def foo():\n  pass\ndef bar():\n  pass'''
    assert parse(f1) == ['def foo():\n  pass\n',
                         'def bar():\n  pass']
    f2 = '''def foo():\n  pass\noh, hai\ndef bar():\n  pass'''
    assert parse(f2) == ['def foo():\n  pass\n',
                         'def bar():\n  pass']


def test_parse_methods():
    parse = pep257.parse_methods
    assert parse('') == []
    m1 = '''class Foo:
    def m1():
        pass
    def m2():
        pass'''
    assert parse(m1) == ['def m1():\n        pass\n    ',
                         'def m2():\n        pass']
    m2 = '''class Foo:
    def m1():
        pass
    attribute
    def m2():
        pass'''
    assert parse(m2) == ['def m1():\n        pass\n    ',
                         'def m2():\n        pass']


def test_check_triple_double_quotes():
    check = pep257.check_triple_double_quotes
    assert check("'''Not using triple douple quotes'''", None, None)
    assert not check('"""Using triple double quotes"""', None, None)
    assert not check('r"""Using raw triple double quotes"""', None, None)
    assert not check('u"""Using unicode triple double quotes"""', None, None)


def test_check_backslashes():
    check = pep257.check_backslashes
    assert check('"""backslash\\here""""', None, None)
    assert not check('r"""backslash\\here""""', None, None)


def test_check_unicode_docstring():
    check = pep257.check_unicode_docstring
    assert not check('"""No Unicode here."""', None, None)
    assert not check('u"""Здесь Юникод: øπΩ≈ç√∫˜µ≤"""', None, None)
    assert check('"""Здесь Юникод: øπΩ≈ç√∫˜µ≤"""', None, None)


def test_check_ends_with_period():
    check = pep257.check_ends_with_period
    s1 = '"""Should end with a period"""'
    s2 = '"""Should end with a period."""'
    s3 = '''"""
        Should end with a period
        """'''
    s4 = '''"""
        Should end with a period.
        """'''
    assert check(s1, None, None)
    assert not check(s2, None, None)
    assert check(s3, None, None)
    assert not check(s4, None, None)


def test_check_blank_before_after_class():
    check = pep257.check_blank_before_after_class
    c1 = '''class Perfect(object):

    """This should work perfectly."""

    pass'''
    assert not check('"""This should work perfectly."""', c1, False)

    c2 = '''class BadTop(object):
    """This should fail due to a lack of whitespace above."""

    pass'''
    assert check('"""This should fail due to a lack of whitespace above."""',
                 c2, False)
    c3 = '''class BadBottom(object):

    """This should fail due to a lack of whitespace below."""
    pass'''
    assert check('"""This should fail due to a lack of whitespace below."""',
                 c3, False)
    c4 = '''class GoodWithNoFollowingWhiteSpace(object):

    """This should work."""'''
    assert not check('"""This should work."""',
                     c4, False)
    c5 = '''class GoodWithFollowingWhiteSpace(object):

    """This should work."""


'''
    assert not check('"""This should work."""', c5, False)

    c6 = '''class Perfect(object):

    """This should work perfectly."""

    def foo(self):
        """This should work perfectly."""
        pass

    '''
    assert not check('"""This should work perfectly."""', c6, False)


def test_check_blank_after_summary():
    check = pep257.check_blank_after_summary
    s1 = '''"""Blank line missing after one-line summary.
    ....................
    """'''
    s2 = '''"""Blank line missing after one-line summary.

    """'''
    s3 = '''"""
    Blank line missing after one-line summary.
    ....................
    """'''
    s4 = '''"""
    Blank line missing after one-line summary.

    """'''
    assert check(s1, None, None)
    assert not check(s2, None, None)
    assert check(s3, None, None)
    assert not check(s4, None, None)


def test_check_indent():
    check = pep257.check_indent
    context = '''def foo():
    """Docstring.

    Properly indented.

    """
    pass'''
    assert not check('"""%s"""' % context.split('"""')[1], context, None)
    context = '''def foo():
    """Docstring.

Not Properly indented.

    """
    pass'''
    assert check('"""%s"""' % context.split('"""')[1], context, None)
