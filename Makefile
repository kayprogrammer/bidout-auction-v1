ifneq (,$(wildcard ./.env))
include .env
export 
ENV_FILE_PARAM = --env-file .env

endif

build:
	docker-compose up --build -d --remove-orphans

up:
	docker-compose up -d

down:
	docker-compose down

show-logs:
	docker-compose logs

migrate:
	docker compose exec web python3.11 manage.py migrate

makemigrations:
	docker compose exec web python3.11 manage.py makemigrations

superuser:
	docker compose exec web python3.11 manage.py createsuperuser

collectstatic:
	docker compose exec web python3.11 manage.py collectstatic --no-input --clear