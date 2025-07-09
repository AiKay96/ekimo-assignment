amend:
	git commit --amend --no-edit -a
	
install:
	uv sync

lock:
	uv lock

update:
	uv lock --upgrade

format:
	uv run ruff format src tests
	uv run ruff check src tests --fix

format-unsafe:
	uv run ruff check src tests --fix --unsafe-fixes

lint:
	uv pip check
	uv run ruff format src tests --check
	uv run ruff check src tests
	uv run mypy src tests

test:
	uv run pytest tests/unit tests/integration \
		--cov \
		--last-failed \
		--approvaltests-use-reporter='PythonNative'

test-e2e:
	uv run pytest tests/e2e \
		--approvaltests-use-reporter='PythonNative'

test-ci:
	uv run pytest tests/unit tests/integration

run:
	uv run -m src.runner run

sync:
	uv run -m src.runner sync
