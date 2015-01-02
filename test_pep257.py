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
    tempdir = tempfile.mkdtemp()

    def write_config(ignore, verbose):
        with open(os.path.join(tempdir, 'tox.ini'), 'wt') as conf:
            conf.write(textwrap.dedent("""\
                [pep257]
                ignore = {0}
                verbose = {1}
            """.format(ignore, verbose)))

    def invoke_pep257():
        pep257_location = os.path.join(os.path.dirname(__file__), 'pep257.py')
        cmd = shlex.split("python {0} {1}".format(pep257_location, tempdir))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        return out.decode('utf-8'), err.decode('utf-8')

    try:
        with open(os.path.join(tempdir, 'example.py'), 'wt') as example:
            example.write(textwrap.dedent("""\
                def foo():
                    pass
            """))

        write_config(ignore='D100', verbose=True)
        out, err = invoke_pep257()
        assert 'D100' not in err
        assert 'D103' in err
        assert 'example.py' in out

        write_config(ignore='', verbose=True)
        out, err = invoke_pep257()
        assert 'D100' in err
        assert 'D103' in err
        assert 'example.py' in out

        write_config(ignore='D100,D103', verbose=False)
        out, err = invoke_pep257()
        assert 'D100' not in err
        assert 'D103' not in err
        assert 'example.py' not in out

        write_config(ignore='', verbose=False)
        out, err = invoke_pep257()
        assert 'D100' in err
        assert 'D103' in err
        assert 'example.py' not in out

    finally:
        shutil.rmtree(tempdir)
