

def test_parse_docstring():
    from pep257 import parse_docstring as pd

    d1 = '''def foo():  # o hai comment
    """docstring"""
    2 + 2'''
    assert pd(d1) == '"""docstring"""'

    d2 = '''def foo():  # o hai comment
    2 + 2'''
    assert pd(d2) == None

    assert pd("def foo():pass") == None
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
