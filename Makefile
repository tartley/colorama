# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE.txt file.

# This makefile is just a cheatsheet to remind me of some commonly used
# commands. I generally am executing these commands on Ubuntu, or on WindowsXP
# with Cygwin binaries at the start of the PATH.

NAME=colorama

help: ## Display help for documented make targets.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-7s\033[0m %s\n", $$1, $$2}'

clean: ## Remove build artifacts and .pyc files
	-rm -rf build dist MANIFEST colorama.egg-info
	-find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
.PHONY: clean

build: clean ## Build an sdist and wheel
	python setup.py sdist bdist_wheel
.PHONY: sdist

upload: ## Upload our sdist and wheel
	twine upload dist/*
.PHONY: release

test: ## Run tests
	python -m unittest discover -p *_test.py
.PHONY: test

tags: ## Create tags file
	ctags -R ${NAME}
.PHONY: tags

