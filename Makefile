# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE.txt file.

# This makefile is just a cheatsheet to remind me of some commonly used
# commands. I generally am executing these commands on Ubuntu, or on WindowsXP
# with Cygwin binaries at the start of the PATH.

NAME=colorama

help: ## Display help for documented make targets.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-7s\033[0m %s\n", $$1, $$2}'


# bootstrap environment

virtualenv=~/.virtualenvs/colorama
pip=$(virtualenv)/bin/pip
syspython=python3.8
python=$(virtualenv)/bin/python
twine=$(virtualenv)/bin/twine
version=$(shell $(python) setup.py --version)

clean: ## Remove build artifacts, .pyc files, virtualenv
	-rm -rf build dist MANIFEST colorama.egg-info $(virtualenv)
	-find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
.PHONY: clean

$(virtualenv):
	$(syspython) -m venv --clear $(virtualenv)
	$(pip) install --upgrade pip

venv: $(virtualenv) ## Create or clear a virtualenv
.PHONY: venv

bootstrap: venv ## Populate the virtualenv
	$(pip) install -r requirements.txt -r requirements-dev.txt
.PHONY: bootstrap


# development

tags: ## Create tags file
	ctags -R ${NAME}
.PHONY: tags

test: ## Run tests
	$(python) -m unittest discover -p *_test.py
.PHONY: test


# build packages

build: ## Build a release (sdist and wheel)
	$(python) -m pip install --upgrade setuptools wheel
	$(python) setup.py sdist bdist_wheel
.PHONY: build

test-release: build ## Test a built release
	./test-release
.PHONY: test-release

release: ## Upload a built release
	$(twine) upload dist/colorama-$(version)*{.whl,.tar.gz}
.PHONY: release

