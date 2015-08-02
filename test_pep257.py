# -*- coding: utf-8 -*-

"""Use tox or py.test to run the test-suite."""

from __future__ import with_statement
from collections import namedtuple

import sys
import os
import mock
import shlex
import pytest
import shutil
import tempfile
import textwrap
import subprocess

import pep257

__all__ = ()


class Pep257Env():

    """An isolated environment where pep257.py can be run.

    Since running pep257.py as a script is affected by local config files, it's
    important that tests will run in an isolated environment. This class should
    be used as a context manager and offers utility methods for adding files
    to the environment and changing the environment's configuration.

    """

    Result = namedtuple('Result', ('out', 'err', 'code'))

    def __init__(self):
        self.tempdir = None

    def write_config(self, **kwargs):
        """Change the environment's config file."""
        with open(os.path.join(self.tempdir, 'tox.ini'), 'wt') as conf:
            conf.write("[pep257]\n")
            for k, v in kwargs.items():
                conf.write("{0} = {1}\n".format(k.replace('_', '-'), v))

    def open(self, path, *args, **kwargs):
        """Open a file in the environment.

        The file path should be relative to the base of the environment.

        """
        return open(os.path.join(self.tempdir, path), *args, **kwargs)

    def invoke_pep257(self, args=""):
        """Run pep257.py on the environment base folder with the given args."""
        pep257_location = os.path.join(os.path.dirname(__file__), 'pep257')
        cmd = shlex.split("python {0} {1} {2}"
                          .format(pep257_location, self.tempdir, args),
                          posix=False)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        return self.Result(out=out.decode('utf-8'),
                           err=err.decode('utf-8'),
                           code=p.returncode)

    def __enter__(self):
        self.tempdir = tempfile.mkdtemp()
        # Make sure we won't be affected by other config files
        self.write_config()
        return self

    def __exit__(self, *args, **kwargs):
        shutil.rmtree(self.tempdir)


def test_pep257_conformance():
    errors = list(pep257.check(['pep257.py', 'test_pep257.py']))
    print(errors)
    assert errors == []


def test_ignore_list():
    function_to_check = textwrap.dedent('''
        def function_with_bad_docstring(foo):
            """ does spacinwithout a period in the end
            no blank line after one-liner is bad. Also this - """
            return foo
    ''')
    expected_error_codes = set(('D100', 'D400', 'D401', 'D205', 'D209',
                                'D210'))
    mock_open = mock.mock_open(read_data=function_to_check)
    with mock.patch('pep257.tokenize_open', mock_open, create=True):
        errors = tuple(pep257.check(['filepath']))
        error_codes = set(error.code for error in errors)
        assert error_codes == expected_error_codes

    # We need to recreate the mock, otherwise the read file is empty
    mock_open = mock.mock_open(read_data=function_to_check)
    with mock.patch('pep257.tokenize_open', mock_open, create=True):
        errors = tuple(pep257.check(['filepath'], ignore=['D100', 'D202']))
        error_codes = set(error.code for error in errors)
        assert error_codes == expected_error_codes - set(('D100', 'D202'))


def test_config_file():
    """Test that options are correctly loaded from a config file.

    This test create a temporary directory and creates two files in it: a
    Python file that has two pep257 violations (D100 and D103) and a config
    file (tox.ini). This test alternates settings in the config file and checks
    that pep257 gives the correct output.

    """
    with Pep257Env() as env:
        with env.open('example.py', 'wt') as example:
            example.write(textwrap.dedent("""\
                def foo():
                    pass
            """))

        env.write_config(ignore='D100', verbose=True)
        out, err, code = env.invoke_pep257()
        assert code == 1
        assert 'D100' not in err
        assert 'D103' in err
        assert 'example.py' in out

        env.write_config(ignore='', verbose=True)
        out, err, code = env.invoke_pep257()
        assert code == 1
        assert 'D100' in err
        assert 'D103' in err
        assert 'example.py' in out

        env.write_config(ignore='D100,D103', verbose=False)
        out, err, code = env.invoke_pep257()
        assert code == 0
        assert 'D100' not in err
        assert 'D103' not in err
        assert 'example.py' not in out

        env.write_config(ignore='', verbose=False)
        out, err, code = env.invoke_pep257()
        assert code == 1
        assert 'D100' in err
        assert 'D103' in err
        assert 'example.py' not in out


def test_count():
    """Test that passing --count to pep257 correctly prints the error num."""
    with Pep257Env() as env:
        with env.open('example.py', 'wt') as example:
            example.write(textwrap.dedent("""\
                def foo():
                    pass
            """))

        out, err, code = env.invoke_pep257(args='--count')
        assert code == 1
        assert '2' in out


def test_select_cli():
    """Test choosing error codes with --select in the CLI."""
    with Pep257Env() as env:
        with env.open('example.py', 'wt') as example:
            example.write(textwrap.dedent("""\
                def foo():
                    pass
            """))

        _, err, code = env.invoke_pep257(args="--select=D100")
        assert code == 1
        assert 'D100' in err
        assert 'D103' not in err


def test_select_config():
    """Test choosing error codes with --select in the config file."""
    with Pep257Env() as env:
        with env.open('example.py', 'wt') as example:
            example.write(textwrap.dedent("""\
                def foo():
                    pass
            """))

        env.write_config(select="D100")
        _, err, code = env.invoke_pep257()
        assert code == 1
        assert 'D100' in err
        assert 'D103' not in err


def test_add_select_cli():
    """Test choosing error codes with --add-select in the CLI."""
    with Pep257Env() as env:
        with env.open('example.py', 'wt') as example:
            example.write(textwrap.dedent("""\
                class Foo(object):
                    def foo():
                        pass
            """))

        env.write_config(select="D100")
        _, err, code = env.invoke_pep257(args="--add-select=D101")
        assert code == 1
        assert 'D100' in err
        assert 'D101' in err
        assert 'D103' not in err


def test_add_ignore_cli():
    """Test choosing error codes with --add-ignore in the CLI."""
    with Pep257Env() as env:
        with env.open('example.py', 'wt') as example:
            example.write(textwrap.dedent("""\
                class Foo(object):
                    def foo():
                        pass
            """))

        env.write_config(select="D100,D101")
        _, err, code = env.invoke_pep257(args="--add-ignore=D101")
        assert code == 1
        assert 'D100' in err
        assert 'D101' not in err
        assert 'D103' not in err


def test_conflicting_select_ignore_config():
    """Test that select and ignore are mutually exclusive."""
    with Pep257Env() as env:
        env.write_config(select="D100", ignore="D101")
        _, err, code = env.invoke_pep257()
        assert code == 2
        assert 'mutually exclusive' in err


def test_conflicting_select_convention_config():
    """Test that select and convention are mutually exclusive."""
    with Pep257Env() as env:
        env.write_config(select="D100", convention="pep257")
        _, err, code = env.invoke_pep257()
        assert code == 2
        assert 'mutually exclusive' in err


def test_conflicting_ignore_convention_config():
    """Test that select and convention are mutually exclusive."""
    with Pep257Env() as env:
        env.write_config(ignore="D100", convention="pep257")
        _, err, code = env.invoke_pep257()
        assert code == 2
        assert 'mutually exclusive' in err


def test_unicode_raw():
    """Test acceptance of unicode raw docstrings for python 2.x."""
    if sys.version_info[0] >= 3:
        return  # ur"" is a syntax error in python 3.x

    # This is all to avoid a syntax error for python 3.2
    from codecs import unicode_escape_decode

    def u(x):
        return unicode_escape_decode(x)[0]

    with Pep257Env() as env:
        with env.open('example.py', 'wt') as example:
            example.write(textwrap.dedent(u('''\
                # -*- coding: utf-8 -*-
                def foo():
                    ur"""Check unicode: \u2611 and raw: \\\\\\\\."""
            ''').encode('utf-8')))
        env.write_config(ignore='D100', verbose=True)
        out, err, code = env.invoke_pep257()
        assert code == 0
        assert 'D301' not in err
        assert 'D302' not in err
