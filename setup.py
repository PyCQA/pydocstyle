from __future__ import with_statement
from distutils.core import setup


with open('pep257.py') as f:
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
    py_modules=['pep257'],
    scripts=['pep257'],
)
