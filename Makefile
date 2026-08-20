.PHONY: install install-dev test lint format run-ui run-api run-cli clean docker-build docker-up

PYTHON ?= python

install:
	$(PYTHON) -m pip install -r requirements.txt

install-dev:
	$(PYTHON) -m pip install -r requirements-dev.txt

test:
	$(PYTHON) -m pytest tests/ -v --tb=short

lint:
	$(PYTHON) -m ruff check src/ tests/ cli/

format:
	$(PYTHON) -m ruff format src/ tests/ cli/

run-ui:
	$(PYTHON) -m streamlit run src/research_system/ui/streamlit_app.py

run-api:
	$(PYTHON) -m uvicorn src.research_system.api.server:app --host 0.0.0.0 --port 8000 --reload

run-cli:
	$(PYTHON) cli/main.py --interactive

docker-build:
	docker build -t research-core-ai:latest .

docker-up:
	docker compose up --build

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/
