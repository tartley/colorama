#!/usr/bin/env python
# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.

from __future__ import with_statement

from io import open
import os
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


NAME = 'colorama'


def read_file(path, encoding='ascii'):
    with open(os.path.join(os.path.dirname(__file__), path),
              encoding=encoding) as fp:
        return fp.read()

def _get_version_match(content):
    # Search for lines of the form: # __version__ = 'ver'
    regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
    version_match = re.search(regex, content, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

def get_version(path):
    return _get_version_match(read_file(path))

setup(
    name=NAME,
    version=get_version(os.path.join('colorama', '__init__.py')),
    description='Cross-platform colored terminal text.',
    long_description=read_file('README.rst'),
    keywords='color colour terminal text ansi windows crossplatform xplatform',
    author='Jonathan Hartley',
    author_email='tartley@tartley.com',
    maintainer='Arnon Yaari',
    url='https://github.com/tartley/colorama',
    license='BSD',
    packages=[NAME],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    # see classifiers https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Terminals',
    ]
)
