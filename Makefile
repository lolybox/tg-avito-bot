.PHONY: install run test clean docker-build docker-up docker-down

# Переменные
BOT_NAME = avito-bot
PYTHON = python3

install:
	@echo "Installing dependencies..."
	$(PYTHON) -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt

run:
	@echo "Running bot..."
	$(PYTHON) bots/main.py

test:
	@echo "Running tests..."
	pytest tests/ -v

clean:
	@echo "Cleaning..."
	rm -rf venv/
	rm -rf __pycache__/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true

docker-build:
	@echo "Building Docker image..."
	docker-compose build

docker-up:
	@echo "Starting containers..."
	docker-compose up -d

docker-down:
	@echo "Stopping containers..."
	docker-compose down

logs:
	@echo "Showing logs..."
	docker-compose logs -f bot

setup-git:
	@echo "Setting up git repository..."
	git init
	@echo "# $(BOT_NAME)\n\nTelegram Avito Monitor Bot" > README.md
	@echo "Repository initialized!"

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies and setup virtual environment"
	@echo "  make run        - Run the Telegram bot"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Clean up Python cache and virtual env"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-up  - Start Docker containers"
	@echo "  make docker-down - Stop Docker containers"
	@echo "  make logs       - View container logs"
	@echo "  make help       - Show this help message"
