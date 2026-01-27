.PHONY: help run run-graph run-graph-export install clear clear-cache

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install/sync dependencies
	uv sync

run:  ## Run the chain agent
	PYTHONDONTWRITEBYTECODE=1 uv run python chain.py

run-graph:  ## Run the graph agent
	PYTHONDONTWRITEBYTECODE=1 uv run python graph.py --no-cache

run-graph-export:  ## Export the graph visualization
	PYTHONDONTWRITEBYTECODE=1 uv run python graph_export.py --no-cache

clear-cache:  ## Clear Python cache files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .uvcache

clear: clear-cache ## Clear cache and virtual environment
	rm -rf .venv