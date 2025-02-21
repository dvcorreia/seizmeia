all: run

run: ## Runs the service locally
	python -m seizmeia

bup: ## Start development environment services
	docker compose up --build --detach

down: ## Stop development environment services
	docker compose down --remove-orphans

log: logs ## Shows container logs
logs:
	docker compose logs -f seizmeia

format: ## Formats code.
	python -m isort .
	python -m black .

test: ## Tests code.
	python -m pytest

lint: ## Lint code.
	python -m ruff check --fix .

coverage: ## Gets code test coverage.
	coverage erase
	coverage run --source=./seizmeia -m pytest 1> /dev/null
	coverage report

typecheck:
	python -m mypy seizmeia

ci: ## Run python CI pipeline (build stages and other non-python specific are not accounted here).
	python -m tox

env: ## Creates a virtual environment.
	python -m venv .venv

sync: install
install: ## Installs packages for development (note: don't forget to activate your virtual env)
	python -m pip install pip-tools
	python -m piptools sync requirements.txt requirements-dev.txt

freeze: ## Freezes current packages defined in the pyproject.toml (TODO: remove --resolver=backtracking on pip-tool 7.0.0).
	python -m piptools compile --resolver=backtracking --generate-hashes -o requirements.txt pyproject.toml
	python -m piptools compile --resolver=backtracking --generate-hashes --extra dev -o requirements-dev.txt pyproject.toml

precommit: pre-commit
pre-commit: ## Runs pre-commit checks.
	pre-commit run --all-files

docs: ## Serve documentation.
	python -m mkdocs serve

clear: clean ## Clears the repository.
clean:
	rm -rf **/__pycache__ .mypy_cache .pytest_cache .vscode .coverage **/*.egg-info *.egg-info .ruff_cache .tox venv .venv build dist

help: ## Show this help.
	@printf "\033[32m\xE2\x9c\x93 usage: make [target]\n\033[0m"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
