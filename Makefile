# Makefile for managing your FastAPI app

APP=dashboard_app
HOST=127.0.0.1
PORT=8080
MODULE=main:app  # adjust if your entrypoint is something else

.PHONY: run dev install lint fmt clean test

run:
	uvicorn $(MODULE) --host $(HOST) --port $(PORT)

dev:
	uvicorn $(MODULE) --reload --host $(HOST) --port $(PORT)

install:
	pip install --upgrade pip
	pip install -r requirements.txt

lint:
	ruff .

fmt:
	ruff . --fix

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +

test:
	pytest -v
