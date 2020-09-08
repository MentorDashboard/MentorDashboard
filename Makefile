test:
	pytest tests/

cov:
	pytest --cov=src tests/

cov-report:
	coverage report -m

install:
	pipenv install