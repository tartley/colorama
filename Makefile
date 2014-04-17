# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.

# This makefile is just a cheatsheet to remind me of some commonly used
# commands. I generally am executing these commands on Ubuntu, or on WindowsXP
# with Cygwin binaries at the start of the PATH.

NAME=colorama

clean:
	-rm -rf build dist MANIFEST colorama.egg-info
	-find . -name '*.py[oc]' -exec rm {} \;
.PHONY: clean

sdist: clean
	python setup.py sdist --formats=zip,gztar
.PHONY: sdist

register: clean
	python setup.py sdist --formats=zip,gztar register 
.PHONY: release

upload: clean
	python setup.py sdist --formats=zip,gztar register upload
.PHONY: release

test:
	python -m unittest discover -p *_test.py
.PHONY: test

tags:
	ctags -R ${NAME}
.PHONY: tags

