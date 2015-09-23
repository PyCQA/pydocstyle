from __future__ import with_statement
import os
from setuptools import setup


with open(os.path.join('src', 'pep257.py')) as f:
    for line in f:
        if line.startswith('__version__'):
            version = eval(line.split('=')[-1])


setup(
    name='pep257',
    version=version,
    description="Python docstring style checker",
    long_description=open('README.rst').read(),
    license='MIT',
    author='Vladimir Keleshev',
    url='https://github.com/GreenSteam/pep257/',
    classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='PEP 257, pep257, PEP 8, pep8, docstrings',
    package_dir={'': 'src'},
    py_modules=['pep257'],
    entry_points={
        'console_scripts': [
            'pep257 = pep257:main',
        ],
    },
)
