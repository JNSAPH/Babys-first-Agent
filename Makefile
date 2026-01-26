VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: help venv install run test freeze clean

help:
	@echo "Common targets:" \
	&& echo "  make venv     - create virtual environment" \
	&& echo "  make install  - install dependencies into venv" \
	&& echo "  make run      - run the app" \
	&& echo "  make test     - run pytest" \
	&& echo "  make freeze   - pin dependencies to requirements.txt" \
	&& echo "  make clean    - remove venv and caches"

venv:
	python3 -m venv $(VENV)

shell:
	@echo "Run 'source $(VENV)/bin/activate' to activate the virtual environment."

install:
	@echo "Checking for virtual environment..."
	if [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found. Creating..."; \
		make venv; \
	else \
		echo "Virtual environment found."; \
	fi
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt

run:
	PYTHONWARNINGS="ignore:Core Pydantic V1 functionality" \
	PYTHONPATH=src \
	$(PYTHON) -m main

run-lg:
	PYTHONWARNINGS="ignore:Core Pydantic V1 functionality" \
	PYTHONPATH=src \
	$(PYTHON) -m graph

test:
	PYTHONPATH=src $(PYTHON) -m pytest -q

freeze:
	$(PIP) freeze > requirements.txt

clean:
	rm -rf $(VENV) __pycache__ */__pycache__ .pytest_cache *.egg-info build dist