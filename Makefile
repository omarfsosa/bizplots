.PHONY: compile-dependencies sync format

PATH_REQUIREMENTS=requirements
PYTHON_VERSION=3.12

compile-dependencies:
	uv pip compile \
		${PATH_REQUIREMENTS}/requirements.in -o ${PATH_REQUIREMENTS}/requirements.txt \
		--emit-index-url --python-version=${PYTHON_VERSION}
	uv pip compile \
		${PATH_REQUIREMENTS}/requirements-dev.in -o ${PATH_REQUIREMENTS}/requirements-dev.txt \
		--emit-index-url --python-version=${PYTHON_VERSION}

sync:
	uv pip sync \
		${PATH_REQUIREMENTS}/requirements.txt \
		${PATH_REQUIREMENTS}/requirements-dev.txt

format:
	ruff format src/