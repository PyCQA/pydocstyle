from __future__ import with_statement
import os
from setuptools import setup


this_dir = os.path.dirname(__file__)

with open(os.path.join(this_dir, 'src', 'pydocstyle', 'utils.py')) as f:
    for line in f:
        if line.startswith('__version__'):
            version = eval(line.split('=')[-1])


setup(
    name='pydocstyle',
    version=version,
    description="Python docstring style checker",
    long_description=open('README.rst').read(),
    license='MIT',
    author='Amir Rachum',
    author_email='amir@rachum.com',
    url='https://github.com/PyCQA/pydocstyle/',
    classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='pydocstyle, PEP 257, pep257, PEP 8, pep8, docstrings',
    packages=('pydocstyle',),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'pydocstyle = pydocstyle.cli:main',
            'pep257 = pydocstyle.cli:main_pep257',
        ],
    },
)
