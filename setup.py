"""`pep257` lives on `GitHub <http://github.com/GreenSteam/pep257/>`_."""
from ez_setup import use_setuptools
use_setuptools()

import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    """Test runner that executes py.test.

    Having this class makes it possible to run tests by invoking:
        python setup.py test
    """
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # imported here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

def get_version():
    with open('pep257.py') as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


setup(name='pep257',
      version=get_version(),
      description="Python docstring style checker",
      long_description=__doc__,
      license='MIT',
      author='Vladimir Keleshev, GreenSteam A/S',
      url='https://github.com/GreenSteam/pep257/',
      classifiers=['Intended Audience :: Developers',
                   'Environment :: Console',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 3',
                   'Operating System :: OS Independent',
                   'License :: OSI Approved :: MIT License'],
      keywords='PEP 257, pep257, PEP 8, pep8, docstrings',
      py_modules=['pep257'],
      scripts=['pep257'],
      tests_require=['pytest==2.2.4', 'mock==0.8', 'pep8==1.4.5'],
      cmdclass = {'test': PyTest},)
