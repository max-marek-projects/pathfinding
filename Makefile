WORKDIR = .

lint:
	uv run ruff format --check ${WORKDIR}
	uv run ruff check ${WORKDIR}
	uv run mypy ${WORKDIR}
	uv run ty check ${WORKDIR}

lint-fix:
	uv run ruff format ${WORKDIR}
	uv run ruff check --fix ${WORKDIR}
	uv run mypy ${WORKDIR}
	uv run ty check ${WORKDIR}

run-wave:
	uv run main_wave.py

run-a-star:
	uv run main_a_star.py

req:
	uv sync

req-style:
	uv sync --extra style
