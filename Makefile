PYTHON := python3
VENV := .venv
ACTIVATE := source $(VENV)/bin/activate

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
	$(PYTHON) -m venv $(VENV)

activate:
	$(ACTIVATE)

install: venv
	$(ACTIVATE) && pip install --upgrade pip setuptools wheel
	$(ACTIVATE) && pip install -r requirements.txt

run:
	export PYTHONWARNINGS="ignore:Core Pydantic V1 functionality" # Suppress pydantic.v1 deprecation warnings, use Python 3.12 for future development
	$(ACTIVATE) && PYTHONPATH=src python -m main

test:
	$(ACTIVATE) && PYTHONPATH=src pytest -q

freeze:
	$(ACTIVATE) && pip freeze > requirements.txt

clean:
	rm -rf $(VENV) __pycache__ */__pycache__ .pytest_cache *.egg-info build dist
