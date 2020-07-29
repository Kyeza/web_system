SHELL := /bin/bash

help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

shell:
	docker-compose exec web python manage.pyshell

test:
	docker-compose exec web python manage.py test

logs:
	docker-compose logs -f

superuser:
	docker-compose exec web python manage.py createsuperuser

deploy:
	docker-compose build
	docker-compose up -d

migrate:
	docker-compose exec web python manage.py makemigrations
	docker-compose exec web python manage.py migrate

down:
	docker-compose down