

def test_parse_docstring():
    from pep257 import parse_docstring as pd

    d1 = '''def foo():  # o hai comment
    """docstring"""
    2 + 2'''
    assert pd(d1) == '"""docstring"""'

    d2 = '''def foo():  # o hai comment
    2 + 2'''
    assert pd(d2) is None

    assert pd("def foo():pass") is None
    # TODO
    #assert pd("def bar():'doc';pass") == "'doc'"


def test_abs_pos():
    from pep257 import abs_pos as ac
    assert ac((1, 0), 'foo') == 0
    assert ac((1, 2), 'foo') == 2
    assert ac((2, 0), 'foo\nbar') == 4


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
    d1 = """\'\'\'Not using triple douple quotes\'\'\'"""
    d2 = """\"\"\"Using triple double quotes\"\"\""""
    d3 = """r\"\"\"Using raw triple double quotes\"\"\""""
    d4 = """u\"\"\"Using unicode triple double quotes\"\"\""""
    assert check(d1, None, None) is not None
    assert check(d2, None, None) is None
    assert check(d3, None, None) is None
    assert check(d4, None, None) is None


def test_check_backslashes():
    from pep257 import check_backslashes as check
    d1 = """\"\"\"ABC\\DEF"\"\"\""""
    d2 = """r\"\"\"ABC\\DEF"\"\"\""""
    assert check(d1, None, None) is not None
    assert check(d2, None, None) is None


def test_check_unicode_docstring():
    # TODO
    pass


def test_check_ends_with_period():
    from pep257 import check_ends_with_period as check
    d1 = """\"\"\"PEP257 First line should end with a period\"\"\""""
    d2 = """\"\"\"PEP257 First line should end with a period.\"\"\""""
    assert check(d1, None, None) is not None
    assert check(d2, None, None) is None


def test_check_blank_after_summary():
    from pep257 import check_blank_after_summary as check
    d1 = """\"\"\"PEP257 Blank line missing after one-line summary.
    ....................
    \"\"\""""
    d2 = """\"\"\"PEP257 Blank line missing after one-line summary.

    \"\"\""""
    assert check(d1, None, None) is not None
    assert check(d2, None, None) is None


def test_check_indent():
    # TODO
    pass


def test_check_blank_after_last_paragraph():
    from pep257 import check_blank_after_last_paragraph as check
    d1 = """\"\"\"PEP257 Multiline docstring should end with 1 blank line.

    The BDFL recommends inserting a blank line between the last
    paragraph in a multi-line docstring and its closing quotes,
    placing the closing quotes on a line by themselves.

    \"\"\""""

    d2 = """\"\"\"PEP257 Multiline docstring should end with 1 blank line.

    The BDFL recommends inserting a blank line between the last
    paragraph in a multi-line docstring and its closing quotes,
    placing the closing quotes on a line by themselves.
    \"\"\""""
    assert check(d1, None, None) is None
    assert check(d2, None, None) is not None


def test_pep257():
    from pep257 import check_files
    assert [] == check_files(['pep257.py'])
