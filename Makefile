.PHONY: compile-dependencies sync format

compile-dependencies:
	uv pip compile requirements.in -o requirements.txt --emit-index-url --python-version=3.12
	uv pip compile requirements-dev.in -o requirements-dev.txt --emit-index-url --python-version=3.12

sync:
	uv pip sync requirements.txt requirements-dev.txt

format:
	ruff format src/