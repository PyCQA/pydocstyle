from __future__ import with_statement
from setuptools import setup, find_packages
import sys

# Do not update the version manually - it is managed by `bumpversion`.
version = '3.0.1rc'


requirements = [
    'snowballstemmer',
]


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
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='pydocstyle, PEP 257, pep257, PEP 8, pep8, docstrings',
    packages=find_packages('src', exclude=["tests", "tests.*"]),
    package_dir={'': 'src'},
    package_data={'pydocstyle': ['data/*.txt']},
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'pydocstyle = pydocstyle.cli:main',
        ],
        'pydocstyle_styles': [
            'pydocstyle.base = pydocstyle.checkers.style.base',
            'pydocstyle.numpy = pydocstyle.checkers.style.numpy',
            'pydocstyle.other = pydocstyle.checkers.style.other',
        ]
    },
)
