.PHONY: help venv conda format style black lint check coverage pypi
.DEFAULT_GOAL = help

PROJECT_NAME = pyvortex
PROJECT_DIR = pyvortex
PYTHON = python
PIP = pip
CONDA = conda
SHELL = bash

help:
	@printf "Usage:\n"
	@grep -E '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[1;34mmake %-10s\033[0m%s\n", $$1, $$2}'
	
develop:
	python setup.py develop
	
doc:
	pdoc -f --html $(PROJECT_DIR) --output-dir docs
	mv ./docs/$(PROJECT_DIR)/* ./docs
	rm -rf ./docs/$(PROJECT_DIR)
	
server:
	pdoc --http : $(PROJECT_DIR)
	
install:
	python setup.py install

conda:  # Set up a conda environment for development.
	@printf "Creating conda environment...\n"
	${CONDA} create --yes --name ${PROJECT_NAME}-env python=3.7
	( \
	${CONDA} activate ${PROJECT_NAME}-env; \
	${PIP} install -U pip; \
	${PIP} install -U setuptools wheel; \
	${PIP} install -r requirements.txt; \
	${CONDA} deactivate; \
	)
	@printf "\n\nConda environment created! \033[1;34mRun \`conda activate ${PROJECT_NAME}-env\` to activate it.\033[0m\n\n\n"

venv:  # Set up a Python virtual environment for development.
	@printf "Creating Python virtual environment...\n"
	rm -rf ${PROJECT_NAME}-venv
	${PYTHON} -m venv ${PROJECT_NAME}-venv
	( \
	source ${PROJECT_NAME}-venv/bin/activate; \
	${PIP} install -U pip; \
	${PIP} install -U setuptools wheel; \
	${PIP} install -r requirements.txt; \
	deactivate; \
	)
	@printf "\n\nVirtual environment created! \033[1;34mRun \`source ${PROJECT_NAME}-venv/bin/activate\` to activate it.\033[0m\n\n\n"

format:
	@printf "Checking code style with black...\n"
	black --check ${PROJECT_DIR} 
	@printf "\033[1;34mBlack passes!\033[0m\n\n"

style:
	@printf "Checking code style with pylint...\n"
	pylint ${PROJECT_DIR} 
	@printf "\033[1;34mPylint passes!\033[0m\n\n"

black:  # Format code in-place using black.
	black ${PROJECT_DIR}

test:  # Test code using pytest.
	pytest -v tests/ ${PROJECT_DIR} --cov=${PROJECT_DIR} --cov-report=xml --html=testing-report.html --self-contained-html

coverage: test
	diff-cover coverage.xml --compare-branch=main --fail-under=100

pypi:
	${PYTHON} setup.py clean --all
	${PYTHON} setup.py rotate --match=.tar.gz,.whl,.egg,.zip --keep=0
	${PYTHON} setup.py sdist bdist_wheel
	twine upload --skip-existing dist/*

lint: format style  # Lint code using pydocstyle, black and pylint.

check: lint test coverage  # Both lint and test code. Runs `make lint` followed by `make test`.

clean: 
	rm -rf ./build 
	rm -rf ./dist 
	rm -rf ./*-venv
	rm -rf ./*egg* 
	rm -rf ./pyvortex/__pycache__
