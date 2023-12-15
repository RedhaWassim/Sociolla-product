######################
# TESTING AND COVERAGE
######################

# Define a variable for the test file path.
TEST_FILE ?= /home/redha/Documents/projects/NLP/sociolla_project/sociolla/tests/unit_tests

test: 
	poetry run pytest $(TEST_FILE)

integration_tests:
	poetry run pytest tests/integration_tests



######################
# LINTING AND FORMATTING
######################

# Define a variable for Python and notebook files.
PYTHON_FILES=.
lint format: PYTHON_FILES=.
lint_diff format_diff: PYTHON_FILES=$(shell git diff --relative=libs/langchain --name-only --diff-filter=d master | grep -E '\.py$$|\.ipynb$$')

lint lint_diff:
	poetry run mypy $(PYTHON_FILES)
	poetry run black $(PYTHON_FILES) --check
	poetry run ruff .


format format_diff:
	poetry run black $(PYTHON_FILES)
	poetry run ruff --select I --fix $(PYTHON_FILES)

spell_check:
	poetry run codespell --toml pyproject.toml

spell_fix:
	poetry run codespell --toml pyproject.toml -w