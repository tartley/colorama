#!/usr/bin/env python
# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
import os
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


NAME = 'colorama'


def get_long_description(filename):
    readme = os.path.join(os.path.dirname(__file__), filename)
    return open(readme).read()

def read_file(path):
    with open(os.path.join(os.path.dirname(__file__), path)) as fp:
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
    long_description=read_file('README.txt'),
    keywords='color colour terminal text ansi windows crossplatform xplatform',
    author='Jonathan Hartley',
    author_email='tartley@tartley.com',
    url='https://pypi.python.org/pypi/colorama',
    license='BSD',
    packages=[NAME],
    # see classifiers http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Topic :: Terminals',
    ]
)

