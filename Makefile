.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .pytest_cache/
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint: ## reformat with black and check style with flake8
	isort pyramid_listing_example
	isort tests
	black --line-length=79 pyramid_listing_example tests
	flake8 pyramid_listing_example tests

test: ## run tests quickly with the default Python
	pytest tests -x --disable-warnings -k "not app"

coverage: ## full test suite, check code coverage and open coverage report
	pytest tests --cov=pyramid_listing_example
	coverage html
	$(BROWSER) htmlcov/index.html

devenv: ## setup development environment
	python3 -m venv --prompt pyramid_listing_example .venv
	.venv/bin/pip3 install --upgrade pip
	.venv/bin/pip3 install -e .[testing,dev]
