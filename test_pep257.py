import tokenize as tk
from io import StringIO

def pytest_funcarg__file_1(request):
    return ''.join(open('test_file_1.py'))



def test_parse_module_docstring(file_1):
    from pep257 import parse_module_docstrings as pmd
    out = pmd(file_1)
    #assert out[0][1] == r"'''Module docstring.\n\t'''"


def test_parse_class_docstring(file_1):
    from pep257 import parse_class_docstrings as pcd
    out = pcd(file_1)


def test_parse_docstrings(file_1):
    from pep257 import parse_docstrings as pd
    print pd(file_1, 'def')



def test_skip_til_scope(file_1):
    from pep257 import skip_til_scope as sts
    token_gen = tk.generate_tokens(StringIO(file_1).readline)
    for i in token_gen:
        print i
    token_gen = tk.generate_tokens(StringIO(file_1).readline)
    print '*' * 30
    print sts(token_gen, 'class')

#    assert False




def test_parse_docstring(file_1):
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


def test_abs_char():
    from pep257 import abs_char as ac
    assert ac((1, 0), 'foo') == 0
    assert ac((1, 2), 'foo') == 2
    assert ac((2, 0), 'foo\nbar') == 4


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


