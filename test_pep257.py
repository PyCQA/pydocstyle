"""Test-suite uses py.test (pip install pytest)."""
# -*- coding: utf-8 -*-
import contextlib


FILES = ['pep257.py', 'test_pep257.py']


def test_pep257_conformance():
    from pep257 import check_files
    assert check_files(FILES) == []


def test_pep8_conformance():
    import pep8
    pep8style = pep8.StyleGuide()
    assert pep8style.check_files(FILES).total_errors == 0


def test_parse_docstring():
    from pep257 import parse_docstring as pd

    s1 = '''def foo():  # o hai comment
    """docstring"""
    2 + 2'''
    assert pd(s1) == '"""docstring"""'

    s2 = '''def foo():  # o hai comment
    2 + 2'''
    assert pd(s2) is None

    assert pd("def foo():pass") is None
    # TODO
    #assert pd("def bar():'doc';pass") == "'doc'"


def test_abs_pos():
    from pep257 import abs_pos as ap
    assert ap((1, 0), 'foo') == 0
    assert ap((1, 2), 'foo') == 2
    assert ap((2, 0), 'foo\nbar') == 4


def test_rel_pos():
    from pep257 import rel_pos as rp
    assert rp(0, 'foo') == (1, 0)
    assert rp(2, 'foo') == (1, 2)
    assert rp(4, 'foo\nbar') == (2, 0)
    assert rp(6, 'foo\nbar') == (2, 2)


def test_parse_functions():
    from pep257 import parse_functions as pf
    assert pf('') == []
    # TODO assert pf('def foo():pass') == ['def foo():pass']
    assert pf('def foo():\n    pass\n') == ['def foo():\n    pass\n']
    assert pf('def foo():\n  pass') == ['def foo():\n  pass']
    f1 = '''def foo():\n  pass\ndef bar():\n  pass'''
    assert pf(f1) == ['def foo():\n  pass\n',
                      'def bar():\n  pass']
    f2 = '''def foo():\n  pass\noh, hai\ndef bar():\n  pass'''
    assert pf(f2) == ['def foo():\n  pass\n',
                      'def bar():\n  pass']


def test_parse_methods():
    from pep257 import parse_methods as pm
    assert pm('') == []
    m1 = '''class Foo:
    def m1():
        pass
    def m2():
        pass'''
    assert pm(m1) == ['def m1():\n        pass\n    ',
                      'def m2():\n        pass']
    m2 = '''class Foo:
    def m1():
        pass
    attribute
    def m2():
        pass'''
    assert pm(m2) == ['def m1():\n        pass\n    ',
                      'def m2():\n        pass']


def test_check_triple_double_quotes():
    from pep257 import check_triple_double_quotes as check
    assert check("'''Not using triple douple quotes'''", None, None)
    assert not check('"""Using triple double quotes"""', None, None)
    assert not check('r"""Using raw triple double quotes"""', None, None)
    assert not check('u"""Using unicode triple double quotes"""', None, None)


def test_check_backslashes():
    from pep257 import check_backslashes as check
    assert check('"""backslash\\here""""', None, None)
    assert not check('r"""backslash\\here""""', None, None)


def test_check_unicode_docstring():
    from pep257 import check_unicode_docstring as check
    assert not check('"""No Unicode here."""', None, None)
    assert not check('u"""Здесь Юникод: øπΩ≈ç√∫˜µ≤"""', None, None)
    assert check('"""Здесь Юникод: øπΩ≈ç√∫˜µ≤"""', None, None)


def test_check_ends_with_period():
    from pep257 import check_ends_with_period as check
    assert check('"""Should end with a period"""', None, None)
    assert not check('"""Should end with a period."""', None, None)


def test_check_blank_before_after_class():
    from pep257 import check_blank_before_after_class as check
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


def test_check_blank_after_summary():
    from pep257 import check_blank_after_summary as check
    s1 = '''"""Blank line missing after one-line summary.
    ....................
    """'''
    s2 = '''"""Blank line missing after one-line summary.

    """'''
    assert check(s1, None, None)
    assert not check(s2, None, None)


def test_check_indent():
    from pep257 import check_indent as check
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


def test_check_blank_after_last_paragraph():
    from pep257 import check_blank_after_last_paragraph as check
    s1 = '''"""Multiline docstring should end with 1 blank line.

    Blank here:

    """'''
    s2 = '''"""Multiline docstring should end with 1 blank line.

    No blank here.
    """'''
    assert not check(s1, None, None)
    assert check(s2, None, None)


@contextlib.contextmanager
def capture_stdout(destination):
    import sys
    real_stdout = sys.stdout
    sys.stdout = destination
    yield
    sys.stdout = real_stdout


def test_failed_open():
    import os.path
    filename = "non-existent-file.py"
    assert not os.path.exists(filename)

    import StringIO
    captured = StringIO.StringIO()
    with capture_stdout(captured):
        import pep257
        pep257.main(*pep257.parse_options([filename]))

    captured_lines = captured.getvalue().split('\n')
    captured_lines = [line.strip() for line in captured_lines]
    assert len(captured_lines) == 4
    assert captured_lines[0] == ('=' * 80)
    assert captured_lines[1] == ('Note: checks are relaxed for scripts'
                                 ' (with #!) compared to modules')
    assert captured_lines[2] == 'Error opening file non-existent-file.py'
    assert captured_lines[3] == ''


def test_failed_read():
    import StringIO
    captured = StringIO.StringIO()

    import mock
    open_mock = mock.MagicMock()
    handle = mock.MagicMock()
    handle.read.side_effect = IOError('Stubbed read error')
    open_mock.__enter__.return_value = handle
    open_mock.return_value = handle

    with capture_stdout(captured):
        with mock.patch('__builtin__.open', open_mock, create=True):
            # Double nesting to support older versions of Python
            import pep257
            pep257.main(*pep257.parse_options(['dummy-file.py']))

    open_mock.assert_called_once_with(('dummy-file.py'))
    handle.close.assert_called_once_with()

    captured_lines = captured.getvalue().split('\n')
    captured_lines = [line.strip() for line in captured_lines]
    assert len(captured_lines) == 4

    assert captured_lines[0] == ('=' * 80)
    assert captured_lines[1] == ('Note: checks are relaxed for scripts'
                                 ' (with #!) compared to modules')
    assert captured_lines[2] == 'Error reading file dummy-file.py'
    assert captured_lines[3] == ''


def test_opened_files_are_closed():
    import mock
    files_opened = []
    real_open = open

    def open_wrapper(*args, **kw):
        opened_file = mock.MagicMock(wraps=real_open(*args, **kw))
        files_opened.append(opened_file)
        return opened_file
    open_mock = mock.MagicMock(side_effect=open_wrapper)
    open_mock.__enter__.side_effect = open_wrapper

    with mock.patch('__builtin__.open', open_mock, create=True):
        import pep257
        pep257.main(*pep257.parse_options(['pep257.py']))

    open_mock.assert_called_once_with(('pep257.py'))
    assert len(files_opened) == 1
    for opened_file in files_opened:
        opened_file.close.assert_called_once_with()
