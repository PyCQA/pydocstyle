# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2012 GreenSteam, <http://greensteam.dk/>
#
#    Permission is hereby granted, free of charge, to any person
#    obtaining a copy of this software and associated documentation files
#    (the "Software"), to deal in the Software without restriction,
#    including without limitation the rights to use, copy, modify, merge,
#    publish, distribute, sublicense, and/or sell copies of the Software,
#    and to permit persons to whom the Software is furnished to do so,
#    subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included
#    in all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH
#    THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""`pep257` lives on `GitHub <http://github.com/GreenSteam/pep257/>`_."""

from distutils.core import setup


setup(name='pep257',
      version='0.2.0',
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
      packages=['pep257'],
      scripts=['bin/pep257'])
