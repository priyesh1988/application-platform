.PHONY: up down test

up:
	docker compose up --build

down:
	docker compose down -v

test:
	python -m compileall app
