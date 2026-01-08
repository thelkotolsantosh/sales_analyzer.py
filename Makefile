.PHONY: help install install-dev test lint format type-check clean run examples docs

help:
	@echo "BI Analyst - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install production dependencies"
	@echo "  make install-dev      Install development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make lint             Run flake8 linter"
	@echo "  make format           Format code with black"
	@echo "  make type-check       Run mypy type checking"
	@echo "  make test             Run pytest test suite"
	@echo "  make test-cov         Run tests with coverage report"
	@echo ""
	@echo "Utilities:"
	@echo "  make run              Run example analysis"
	@echo "  make examples         Run all examples"
	@echo "  make clean            Remove build artifacts and cache"
	@echo "  make build            Build distribution packages"
	@echo ""

# Installation targets
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -e ".[dev]"
	pip install build twine

# Testing targets
test:
	pytest test_sales_analyzer.py -v

test-cov:
	pytest test_sales_analyzer.py -v --cov=bi_analyst --cov-report=html --cov-report=term

# Linting and formatting targets
lint:
	flake8 bi_analyst/ test_sales_analyzer.py examples.py

format:
	black bi_analyst/ test_sales_analyzer.py examples.py

type-check:
	mypy bi_analyst/ --ignore-missing-imports

# Running targets
run:
	python -m bi_analyst.sales_analyzer

examples:
	python examples.py

# Building targets
build: clean
	python -m build

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf dashboards/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

.DEFAULT_GOAL := help
