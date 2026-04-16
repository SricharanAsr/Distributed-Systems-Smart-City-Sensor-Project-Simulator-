.PHONY: run test install clean docker-build

run:
	python simulator.py

test:
	pytest test_sensors.py

install:
	pip install -r requirements.txt

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	rm -rf .pytest_cache .coverage htmlcov

docker-build:
	docker build -t smart-city-simulator .

# Extraneous targets
