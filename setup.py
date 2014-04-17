#!/usr/bin/env python
# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
from os.path import dirname, join
from distutils.core import setup

from colorama import VERSION


NAME = 'colorama'


def get_long_description(filename):
    readme = join(dirname(__file__), filename)
    return open(readme).read()


setup(
    name=NAME,
    version=VERSION,
    description='Cross-platform colored terminal text.',
    long_description=get_long_description('README.txt'),
    keywords='color colour terminal text ansi windows crossplatform xplatform',
    author='Jonathan Hartley',
    author_email='tartley@tartley.com',
    url='http://code.google.com/p/colorama/',
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

