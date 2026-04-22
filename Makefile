.PHONY: run test install clean docker-build format lint verify health

run:
	python simulator.py

test:
	pytest tests/

verify:
	python tools/verify_sensors.py

health:
	python simulator.py --health

install:
	pip install -r requirements.txt

format:
	black .
	isort .

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

clean:
	powershell -Command "Get-ChildItem -Path . -Include __pycache__ -Recurse | Remove-Item -Recurse -Force"
	rm -rf .pytest_cache .coverage htmlcov .mypy_cache .ruff_cache
	rm -rf data_cache/*.json

docker-build:
	docker build -t smart-city-simulator .

clean-logs:
	rm -rf *.log simulator.log*

clean-cache:
	rm -rf data_cache/*.json

clean-all: clean clean-logs clean-cache
	@echo "All build artifacts, logs, and caches cleared."

verify:
	python tools/verify_sensors.py

export-test:
	python -c "from utils.data_exporter import *"
