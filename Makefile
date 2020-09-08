test:
	pytest tests/

cov:
	pytest -v --cov-report term-missing --cov=src tests/

install:
	pipenv install