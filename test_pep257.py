"""Use tox or py.test to run the test-suite."""
# -*- coding: utf-8 -*-
from __future__ import with_statement

import os
import mock
import shutil
import shlex
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

    def __init__(self):
        self.tempdir = None

    def write_config(self, ignore, verbose):
        """Change the environment's config file."""
        with open(os.path.join(self.tempdir, 'tox.ini'), 'wt') as conf:
            conf.write(textwrap.dedent("""\
                [pep257]
                ignore = {0}
                verbose = {1}
            """.format(ignore, verbose)))

    def open(self, path, *args, **kwargs):
        """Open a file in the environment.

        The file path should be relative to the base of the environment.

        """
        return open(os.path.join(self.tempdir, path), *args, **kwargs)

    def invoke_pep257(self, args=""):
        """Run pep257.py on the environment base folder with the given args."""
        pep257_location = os.path.join(os.path.dirname(__file__), 'pep257')
        cmd = shlex.split("{0} {1} {2}"
                          .format(pep257_location, self.tempdir, args))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        return out.decode('utf-8'), err.decode('utf-8')

    def __enter__(self):
        self.tempdir = tempfile.mkdtemp()
        return self

    def __exit__(self, *args, **kwargs):
        shutil.rmtree(self.tempdir)


def test_pep257_conformance():
    errors = list(pep257.check(['pep257.py', 'test_pep257.py']))
    print(errors)
    assert errors == []


def test_ignore_list():
    function_to_check = """def function_with_bad_docstring(foo):
    \"\"\" does spacing without a period in the end
    no blank line after one-liner is bad. Also this - \"\"\"
    return foo
    """
    expected_error_codes = set(('D100', 'D400', 'D401', 'D205', 'D209'))
    mock_open = mock.mock_open(read_data=function_to_check)
    with mock.patch('pep257.open', mock_open, create=True):
        errors = tuple(pep257.check(['filepath']))
        error_codes = set(error.code for error in errors)
        assert error_codes == expected_error_codes

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
        out, err = env.invoke_pep257()
        assert 'D100' not in err
        assert 'D103' in err
        assert 'example.py' in out

        env.write_config(ignore='', verbose=True)
        out, err = env.invoke_pep257()
        assert 'D100' in err
        assert 'D103' in err
        assert 'example.py' in out

        env.write_config(ignore='D100,D103', verbose=False)
        out, err = env.invoke_pep257()
        assert 'D100' not in err
        assert 'D103' not in err
        assert 'example.py' not in out

        env.write_config(ignore='', verbose=False)
        out, err = env.invoke_pep257()
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

        out, err = env.invoke_pep257(args='--count')
        assert out == '2\n'
