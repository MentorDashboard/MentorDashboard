app_name = mentordashboard

test:
	pytest tests/

cov:
	pytest -v --cov-report term-missing --cov=app tests/

install:
	pipenv install

format:
	black .

css:
	npm run css

build:
	npm run build

build:
	@docker build -t $(app_name) .
run:
	docker run --detach -p 8003:8003 $(app_name)
kill:
	@echo 'Killing container...'
	@docker ps | grep $(app_name) | awk '{print $$1}' | xargs docker