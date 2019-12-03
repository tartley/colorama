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

sdist: clean ## Build an sdist file
	python setup.py sdist
.PHONY: sdist

upload: clean ## Upload an sdist file
	python setup.py sdist upload
	python setup.py bdist_wheel upload
.PHONY: release

test: ## Run tests
	python -m unittest discover -p *_test.py
.PHONY: test

tags: ## Create tags file
	ctags -R ${NAME}
.PHONY: tags

