from setuptools import setup

# Do not update the version manually - it is managed by `bumpversion`.
version = '6.1.1'


requirements = [
    'snowballstemmer',
]
extra_requirements = {
    'toml': ['toml'],
}


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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
    keywords='pydocstyle, PEP 257, pep257, PEP 8, pep8, docstrings',
    packages=('pydocstyle',),
    package_dir={'': 'src'},
    package_data={'pydocstyle': ['data/*.txt']},
    install_requires=requirements,
    extras_require=extra_requirements,
    entry_points={
        'console_scripts': [
            'pydocstyle = pydocstyle.cli:main',
        ],
    },
    project_urls={
        'Release Notes': 'https://www.pydocstyle.org/en/latest/release_notes.html',
    },
)
