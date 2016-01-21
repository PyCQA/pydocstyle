# -*- coding: utf-8 -*-

"""Use tox or py.test to run the test-suite."""

from __future__ import with_statement
from collections import namedtuple
from functools import partial

import sys
import os
import mock
import shlex
import shutil
import tempfile
import textwrap
import subprocess

from .. import pep257

__all__ = ()


class Pep257Env(object):
    """An isolated environment where pep257.py can be run.

    Since running pep257.py as a script is affected by local config files, it's
    important that tests will run in an isolated environment. This class should
    be used as a context manager and offers utility methods for adding files
    to the environment and changing the environment's configuration.

    """

    Result = namedtuple('Result', ('out', 'err', 'code'))

    def __init__(self):
        self.tempdir = None

    def write_config(self, prefix='', **kwargs):
        """Change an environment config file.

        Applies changes to `tox.ini` relative to `tempdir/prefix`.
        If the given path prefix does not exist it is created.

        """
        base = os.path.join(self.tempdir, prefix) if prefix else self.tempdir
        if not os.path.isdir(base):
            self.makedirs(base)

        with open(os.path.join(base, 'tox.ini'), 'wt') as conf:
            conf.write("[pep257]\n")
            for k, v in kwargs.items():
                conf.write("{0} = {1}\n".format(k.replace('_', '-'), v))

    def open(self, path, *args, **kwargs):
        """Open a file in the environment.

        The file path should be relative to the base of the environment.

        """
        return open(os.path.join(self.tempdir, path), *args, **kwargs)

    def makedirs(self, path, *args, **kwargs):
        """Create a directory in a path relative to the environment base."""
        os.makedirs(os.path.join(self.tempdir, path), *args, **kwargs)

    def invoke_pep257(self, args="", target=None):
        """Run pep257.py on the environment base folder with the given args.

        If `target` is not None, will run pep257 on `target` instead of
        the environment base folder.

        """
        pep257_location = os.path.join(os.path.dirname(__file__),
                                       '..', 'pep257.py')
        run_target = self.tempdir if target is None else \
            os.path.join(self.tempdir, target)

        cmd = shlex.split("python {0} {1} {2}"
                          .format(pep257_location, run_target, args),
                          posix=False)
        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
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
        pass


def parse_errors(err):
    """Parse `err` to a dictionary of {filename: error_codes}.

    This is for test purposes only. All file names should be different.

    """
    print(err)
    result = {}
    py_ext = '.py'
    lines = err.split('\n')
    while lines:
        curr_line = lines.pop(0)
        filename = curr_line[:curr_line.find(py_ext) + len(py_ext)]
        if os.path.isfile(filename):
            if lines:
                err_line = lines.pop(0).strip()
                err_code = err_line.split(':')[0]
                basename = os.path.basename(filename)
                result.setdefault(basename, set()).add(err_code)

    return result


def test_pep257_conformance():
    relative = partial(os.path.join, os.path.dirname(__file__))
    errors = list(pep257.check([relative('..', 'pep257.py'),
                                relative('test_pep257.py')],
                               select=pep257.conventions.pep257))
    assert errors == [], errors


def test_ignore_list():
    function_to_check = textwrap.dedent('''
        def function_with_bad_docstring(foo):
            """ does spacinwithout a period in the end
            no blank line after one-liner is bad. Also this - """
            return foo
    ''')
    expected_error_codes = set(('D100', 'D400', 'D401', 'D205', 'D209',
                                'D210', 'D403'))
    mock_open = mock.mock_open(read_data=function_to_check)
    from .. import pep257
    with mock.patch.object(pep257, 'tokenize_open', mock_open, create=True):
        errors = tuple(pep257.check(['filepath']))
        error_codes = set(error.code for error in errors)
        assert error_codes == expected_error_codes

    # We need to recreate the mock, otherwise the read file is empty
    mock_open = mock.mock_open(read_data=function_to_check)
    with mock.patch.object(pep257, 'tokenize_open', mock_open, create=True):
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

        env.write_config(ignore='D100')
        _, err, code = env.invoke_pep257()
        assert code == 1
        assert 'D100' not in err
        assert 'D103' in err

        env.write_config(ignore='')
        _, err, code = env.invoke_pep257()
        assert code == 1
        assert 'D100' in err
        assert 'D103' in err

        env.write_config(ignore='D100,D103')
        _, err, code = env.invoke_pep257()
        assert code == 0
        assert 'D100' not in err
        assert 'D103' not in err


def test_verbose():
    """Test that passing --verbose to pep257 prints more information."""
    with Pep257Env() as env:
        with env.open('example.py', 'wt') as example:
            example.write('"""Module docstring."""\n')

        out, _, code = env.invoke_pep257()
        assert code == 0
        assert 'example.py' not in out

        out, _, code = env.invoke_pep257(args="--verbose")
        assert code == 0
        assert 'example.py' in out


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
    """Test choosing error codes with `--select` in the CLI."""
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
    """Test choosing error codes with `select` in the config file."""
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


def test_missing_docstring_in_package():
    with Pep257Env() as env:
        with env.open('__init__.py', 'wt') as init:
            pass  # an empty package file
        out, err, code = env.invoke_pep257()
        assert code == 1
        assert 'D100' not in err  # shouldn't be treated as a module
        assert 'D104' in err  # missing docstring in package


def test_illegal_convention():
    with Pep257Env() as env:
        out, err, code = env.invoke_pep257('--convention=illegal_conv')
        assert code == 2
        assert "Illegal convention 'illegal_conv'." in err
        assert 'Possible conventions: pep257' in err


def test_empty_select_cli():
    """Test excluding all error codes with `--select=` in the CLI."""
    with Pep257Env() as env:
        with env.open('example.py', 'wt') as example:
            example.write(textwrap.dedent("""\
                def foo():
                    pass
            """))

        _, _, code = env.invoke_pep257(args="--select=")
        assert code == 0


def test_empty_select_config():
    """Test excluding all error codes with `select=` in the config file."""
    with Pep257Env() as env:
        with env.open('example.py', 'wt') as example:
            example.write(textwrap.dedent("""\
                def foo():
                    pass
            """))

        env.write_config(select="")
        _, _, code = env.invoke_pep257()
        assert code == 0


def test_empty_select_with_added_error():
    """Test excluding all errors but one."""
    with Pep257Env() as env:
        with env.open('example.py', 'wt') as example:
            example.write(textwrap.dedent("""\
                def foo():
                    pass
            """))

        env.write_config(select="")
        _, err, code = env.invoke_pep257(args="--add-select=D100")
        assert code == 1
        assert 'D100' in err
        assert 'D101' not in err
        assert 'D103' not in err


def test_pep257_convention():
    """Test that the 'pep257' convention options has the correct errors."""
    with Pep257Env() as env:
        with env.open('example.py', 'wt') as example:
            example.write(textwrap.dedent('''
                class Foo(object):


                    """Docstring for this class"""
                    def foo():
                        pass
            '''))

        env.write_config(convention="pep257")
        _, err, code = env.invoke_pep257()
        assert code == 1
        assert 'D100' in err
        assert 'D211' in err
        assert 'D203' not in err


def test_config_file_inheritance():
    """Test configuration files inheritance.

    The test creates 2 configuration files:

    env_base
    +-- tox.ini
    |   This configuration will set `select=`.
    +-- A
        +-- tox.ini
        |   This configuration will set `inherit=false`.
        +-- test.py
            The file will contain code that violates D100,D103.

    When invoking pep257, the first config file found in the base directory
    will set `select=`, so no error codes should be checked.
    The `A/tox.ini` configuration file sets `inherit=false` but has an empty
    configuration, therefore the default convention will be checked.

    We expect pep257 to ignore the `select=` configuration and raise all
    the errors stated above.

    """
    with Pep257Env() as env:
        env.write_config(select='')
        env.write_config(prefix='A', inherit=False)

        with env.open(os.path.join('A', 'test.py'), 'wt') as test:
            test.write(textwrap.dedent("""\
                def bar():
                    pass
            """))

        _, err, code = env.invoke_pep257()

        assert code == 1
        assert 'D100' in err
        assert 'D103' in err


def test_config_file_cumulative_add_ignores():
    """Test that add-ignore is cumulative.

    env_base
    +-- tox.ini
    |   This configuration will set `select=D100,D103` and `add-ignore=D100`.
    +-- base.py
    |   Will violate D100,D103
    +-- A
        +-- tox.ini
        |   This configuration will set `add-ignore=D103`.
        +-- a.py
            Will violate D100,D103.

    The desired result is that `base.py` will fail with D103 and
    `a.py` will pass.

    """
    with Pep257Env() as env:
        env.write_config(select='D100,D103', add_ignore='D100')
        env.write_config(prefix='A', add_ignore='D103')

        test_content = textwrap.dedent("""\
            def foo():
                pass
        """)

        with env.open('base.py', 'wt') as test:
            test.write(test_content)

        with env.open(os.path.join('A', 'a.py'), 'wt') as test:
            test.write(test_content)

        _, err, code = env.invoke_pep257()

        err = parse_errors(err)

        assert code == 1
        assert 'base.py' in err, err
        assert 'a.py' not in err, err
        assert 'D100' not in err['base.py'], err
        assert 'D103' in err['base.py'], err


def test_config_file_cumulative_add_select():
    """Test that add-select is cumulative.

    env_base
    +-- tox.ini
    |   This configuration will set `select=` and `add-select=D100`.
    +-- base.py
    |   Will violate D100,D103
    +-- A
        +-- tox.ini
        |   This configuration will set `add-select=D103`.
        +-- a.py
            Will violate D100,D103.

    The desired result is that `base.py` will fail with D100 and
    `a.py` will fail with D100,D103.

    """
    with Pep257Env() as env:
        env.write_config(select='', add_select='D100')
        env.write_config(prefix='A', add_select='D103')

        test_content = textwrap.dedent("""\
            def foo():
                pass
        """)

        with env.open('base.py', 'wt') as test:
            test.write(test_content)

        with env.open(os.path.join('A', 'a.py'), 'wt') as test:
            test.write(test_content)

        _, err, code = env.invoke_pep257()

        err = parse_errors(err)

        assert code == 1
        assert 'base.py' in err, err
        assert 'a.py' in err, err
        assert err['base.py'] == set(['D100']), err
        assert err['a.py'] == set(['D100', 'D103']), err


def test_config_file_convention_overrides_select():
    """Test that conventions override selected errors.

    env_base
    +-- tox.ini
    |   This configuration will set `select=D103`.
    +-- base.py
    |   Will violate D100.
    +-- A
        +-- tox.ini
        |   This configuration will set `convention=pep257`.
        +-- a.py
            Will violate D100.

    The expected result is that `base.py` will be clear of errors and
    `a.py` will violate D100.

    """
    with Pep257Env() as env:
        env.write_config(select='D103')
        env.write_config(prefix='A', convention='pep257')

        test_content = ""

        with env.open('base.py', 'wt') as test:
            test.write(test_content)

        with env.open(os.path.join('A', 'a.py'), 'wt') as test:
            test.write(test_content)

        _, err, code = env.invoke_pep257()

        assert code == 1
        assert 'D100' in err, err
        assert 'base.py' not in err, err
        assert 'a.py' in err, err


def test_cli_overrides_config_file():
    """Test that the CLI overrides error codes selected in the config file.

    env_base
    +-- tox.ini
    |   This configuration will set `select=D103` and `match-dir=foo`.
    +-- base.py
    |   Will violate D100.
    +-- A
        +-- a.py
            Will violate D100,D103.

    We shall run pep257 with `--convention=pep257`.
    We expect `base.py` to be checked and violate `D100` and that `A/a.py` will
    not be checked because of `match-dir=foo` in the config file.

    """
    with Pep257Env() as env:
        env.write_config(select='D103', match_dir='foo')

        with env.open('base.py', 'wt') as test:
            test.write("")

        env.makedirs('A')
        with env.open(os.path.join('A', 'a.py'), 'wt') as test:
            test.write(textwrap.dedent("""\
                def foo():
                    pass
            """))

        _, err, code = env.invoke_pep257(args="--convention=pep257")

        assert code == 1
        assert 'D100' in err, err
        assert 'D103' not in err, err
        assert 'base.py' in err, err
        assert 'a.py' not in err, err


def test_cli_match_overrides_config_file():
    """Test that the CLI overrides the match clauses in the config file.

    env_base
    +-- tox.ini
    |   This configuration will set `match-dir=foo`.
    +-- base.py
    |   Will violate D100,D103.
    +-- A
        +-- tox.ini
        |   This configuration will set `match=bar.py`.
        +-- a.py
            Will violate D100.

    We shall run pep257 with `--match=a.py` and `--match-dir=A`.
    We expect `base.py` will not be checked and that `A/a.py` will be checked.

    """
    with Pep257Env() as env:
        env.write_config(match_dir='foo')
        env.write_config(prefix='A', match='bar.py')

        with env.open('base.py', 'wt') as test:
            test.write(textwrap.dedent("""\
                def foo():
                    pass
            """))

        with env.open(os.path.join('A', 'a.py'), 'wt') as test:
            test.write("")

        _, err, code = env.invoke_pep257(args="--match=a.py --match-dir=A")

        assert code == 1
        assert 'D100' in err, err
        assert 'D103' not in err, err
        assert 'base.py' not in err, err
        assert 'a.py' in err, err


def test_config_file_convention_overrides_ignore():
    """Test that conventions override ignored errors.

    env_base
    +-- tox.ini
    |   This configuration will set `ignore=D100,D103`.
    +-- base.py
    |   Will violate D100,D103.
    +-- A
        +-- tox.ini
        |   This configuration will set `convention=pep257`.
        +-- a.py
            Will violate D100,D103.

    The expected result is that `base.py` will be clear of errors and
    `a.py` will violate D103.

    """
    with Pep257Env() as env:
        env.write_config(ignore='D100,D103')
        env.write_config(prefix='A', convention='pep257')

        test_content = textwrap.dedent("""\
            def foo():
                pass
        """)

        with env.open('base.py', 'wt') as test:
            test.write(test_content)

        with env.open(os.path.join('A', 'a.py'), 'wt') as test:
            test.write(test_content)

        _, err, code = env.invoke_pep257()

        assert code == 1
        assert 'D100' in err, err
        assert 'D103' in err, err
        assert 'base.py' not in err, err
        assert 'a.py' in err, err


def test_config_file_ignore_overrides_select():
    """Test that ignoring any error overrides selecting errors.

    env_base
    +-- tox.ini
    |   This configuration will set `select=D100`.
    +-- base.py
    |   Will violate D100,D101,D102.
    +-- A
        +-- tox.ini
        |   This configuration will set `ignore=D102`.
        +-- a.py
            Will violate D100,D101,D102.

    The expected result is that `base.py` will violate D100 and
    `a.py` will violate D100,D101.

    """
    with Pep257Env() as env:
        env.write_config(select='D100')
        env.write_config(prefix='A', ignore='D102')

        test_content = textwrap.dedent("""\
            class Foo(object):
                def bar():
                    pass
        """)

        with env.open('base.py', 'wt') as test:
            test.write(test_content)

        with env.open(os.path.join('A', 'a.py'), 'wt') as test:
            test.write(test_content)

        _, err, code = env.invoke_pep257()

        err = parse_errors(err)

        assert code == 1
        assert 'base.py' in err, err
        assert 'a.py' in err, err
        assert err['base.py'] == set(['D100']), err
        assert err['a.py'] == set(['D100', 'D101']), err


def test_config_file_nearest_to_checked_file():
    """Test that the configuration to each file is the nearest one.

    In this test there will be 2 identical files in 2 branches in the directory
    tree. Both of them will violate the same error codes, but their config
    files will contain different ignores.

    env_base
    +-- tox.ini
    |   This configuration will set `convention=pep257` and `add-ignore=D100`
    +-- base.py
    |   Will violate D100,D101,D102.
    +-- A
    |   +-- a.py
    |       Will violate D100,D101,D102.
    +-- B
        +-- tox.ini
        |   Will set `add-ignore=D101`
        +-- b.py
            Will violate D100,D101,D102.

    We should see that `a.py` and `base.py` act the same and violate
    D101,D102 (since they are both configured by `tox.ini`) and that
    `b.py` violates D102, since it's configured by `B/tox.ini` as well.

    """
    with Pep257Env() as env:
        env.write_config(convention='pep257', add_ignore='D100')
        env.write_config(prefix='B', add_ignore='D101')

        test_content = textwrap.dedent("""\
            class Foo(object):
                def bar():
                    pass
        """)

        with env.open('base.py', 'wt') as test:
            test.write(test_content)

        env.makedirs('A')
        with env.open(os.path.join('A', 'a.py'), 'wt') as test:
            test.write(test_content)

        with env.open(os.path.join('B', 'b.py'), 'wt') as test:
            test.write(test_content)

        _, err, code = env.invoke_pep257()

        err = parse_errors(err)

        assert code == 1
        assert 'base.py' in err, err
        assert 'a.py' in err, err
        assert 'b.py' in err, err
        assert err['base.py'] == set(['D101', 'D102']), err
        assert err['a.py'] == set(['D101', 'D102']), err
        assert err['b.py'] == set(['D102']), err


def test_config_file_nearest_match_re():
    """Test that the `match` and `match-dir` options are handled correctly.

    env_base
    +-- tox.ini
    |   This configuration will set `convention=pep257` and `add-ignore=D100`.
    +-- A
        +-- tox.ini
        |   Will set `match-dir=C`.
        +-- B
        |   +-- b.py
        |       Will violate D100,D103.
        +-- C
            +-- tox.ini
            |   Will set `match=bla.py`.
            +-- c.py
            |   Will violate D100,D103.
            +-- bla.py
                Will violate D100.

    We expect the call to pep257 to be successful, since `b.py` and
    `c.py` are not supposed to be found by the re.

    """
    with Pep257Env() as env:
        env.write_config(convention='pep257', add_ignore='D100')
        env.write_config(prefix='A', match_dir='C')
        env.write_config(prefix=os.path.join('A', 'C'), match='bla.py')

        content = textwrap.dedent("""\
            def foo():
                pass
        """)

        env.makedirs(os.path.join('A', 'B'))
        with env.open(os.path.join('A', 'B', 'b.py'), 'wt') as test:
            test.write(content)

        with env.open(os.path.join('A', 'C', 'c.py'), 'wt') as test:
            test.write(content)

        with env.open(os.path.join('A', 'C', 'bla.py'), 'wt') as test:
            test.write('')

        _, _, code = env.invoke_pep257()

        assert code == 0
