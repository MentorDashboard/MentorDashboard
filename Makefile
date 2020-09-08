test:
	pytest tests/

cov:
	pytest -v --cov-report term --cov=src tests/

install:
	pipenv install