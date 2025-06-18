.PHONY: run install migrate test lint docker-build docker-up docker-down

VENV = .venv/bin/
NAME ?= auto

ifeq ($(OS),Windows_NT)
    VENV = .venv/Scripts/
endif

ENV ?= development

run:
	ENV=$(ENV) $(VENV)python main.py

install:
	$(VENV)pip install --upgrade pip && \
	$(VENV)pip install -r requirements.txt

gen-migration:
	$(VENV)alembic revision --autogenerate -m "$(NAME)"

migrate:
	$(VENV)alembic upgrade head

test:
	$(VENV)pytest --disable-warnings

docker-build:
	docker build -t mybot:latest .

docker-up:
	docker compose up -d

docker-down:
	docker compose down