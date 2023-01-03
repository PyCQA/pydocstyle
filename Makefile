all: format tests

format:
	isort src/pydocstyle
	black src/pydocstyle

tests:
	tox -e py,install
