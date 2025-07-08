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
	uv check
	uv run ruff format src tests --check
	uv run ruff check src tests
	uv run mypy src tests

test:
	uv run pytest src tests \
		--cov \
		--last-failed

test-ci:
	uv run pytest src tests
