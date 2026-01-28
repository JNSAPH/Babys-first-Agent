.PHONY: help up

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev:
	PYTHONDONTWRITEBYTECODE=1 uv run langgraph dev 

dev-no-browser:
	PYTHONDONTWRITEBYTECODE=1 uv run langgraph dev --no-browser

run-graph-export:  ## Export the graph visualization
	PYTHONDONTWRITEBYTECODE=1 uv run python graph_export.py

clear-cache:  ## Clear Python cache files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .uvcache
	rm -rf .langgraph_api
	rm -rf agent.egg-info

clear: clear-cache ## Clear cache and virtual environment
	rm -rf .venv