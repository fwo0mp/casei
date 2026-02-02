.PHONY: help install run shell migrate makemigrations createsuperuser \
        docker-up docker-down docker-build docker-logs docker-shell docker-migrate docker-createsuperuser \
        update-standings ncaa-schedule nfl-schedule estimate-scores check-games set-next-games

# Default target
help:
	@echo "Local Development (requires local postgres/memcached):"
	@echo "  make install          - Install dependencies with uv"
	@echo "  make run              - Run development server"
	@echo "  make shell            - Open Django shell"
	@echo "  make migrate          - Run database migrations"
	@echo "  make makemigrations   - Create new migrations"
	@echo "  make createsuperuser  - Create admin user"
	@echo ""
	@echo "Local Setup:"
	@echo "  make setup-local-data       - Populate DB with test data"
	@echo "  make setup-local-data-reset - Reset and repopulate test data"
	@echo "  make docker-setup-local-data       - Populate DB (Docker)"
	@echo "  make docker-setup-local-data-reset - Reset and repopulate (Docker)"
	@echo ""
	@echo "Docker Commands:"
	@echo "  make docker-up        - Start all services"
	@echo "  make docker-down      - Stop all services"
	@echo "  make docker-down-v    - Stop all services and remove volumes"
	@echo "  make docker-build     - Rebuild Docker images"
	@echo "  make docker-logs      - View container logs"
	@echo "  make docker-shell     - Open Django shell in container"
	@echo "  make docker-bash      - Open bash shell in container"
	@echo "  make docker-migrate   - Run migrations in container"
	@echo "  make docker-createsuperuser - Create admin user in container"
	@echo ""
	@echo "Data Commands (local):"
	@echo "  make update-standings - Update team scores from real results"
	@echo "  make ncaa-schedule    - Fetch NCAA game schedule"
	@echo "  make nfl-schedule     - Fetch NFL game schedule"
	@echo "  make estimate-scores  - Calculate estimated positions"
	@echo "  make check-games      - Process completed games"
	@echo "  make set-next-games   - Update next game cache"

# =============================================================================
# Local Development
# =============================================================================

install:
	uv sync

run:
	uv run python manage.py runserver

shell:
	uv run python manage.py shell

migrate:
	uv run python manage.py migrate

makemigrations:
	uv run python manage.py makemigrations

createsuperuser:
	uv run python manage.py createsuperuser

# =============================================================================
# Docker
# =============================================================================

docker-up:
	docker compose up

docker-up-d:
	docker compose up -d

docker-down:
	docker compose down

docker-down-v:
	docker compose down -v

docker-build:
	docker compose build

docker-logs:
	docker compose logs -f

docker-shell:
	docker compose exec web uv run python manage.py shell

docker-bash:
	docker compose exec web bash

docker-migrate:
	docker compose exec web uv run python manage.py migrate

docker-createsuperuser:
	docker compose exec web uv run python manage.py createsuperuser

# =============================================================================
# Local Setup
# =============================================================================

setup-local-data:
	uv run python manage.py setup_local_data

setup-local-data-reset:
	uv run python manage.py setup_local_data --reset

docker-setup-local-data:
	docker compose exec web uv run python manage.py setup_local_data

docker-setup-local-data-reset:
	docker compose exec web uv run python manage.py setup_local_data --reset

# =============================================================================
# Data Import/Update Commands
# =============================================================================

update-standings:
	uv run python manage.py update_standings

ncaa-schedule:
	uv run python manage.py ncaa_schedule_scraper

nfl-schedule:
	uv run python manage.py nfl_schedule_scraper

estimate-scores:
	uv run python manage.py estimate_scores

check-games:
	uv run python manage.py check_games

set-next-games:
	uv run python manage.py set_next_games
