### General commands ###
build-web:
	@docker-compose build web

up:
	@docker-compose up -d

stop:
	@docker-compose stop

down:
	@docker-compose down

restart-web:
	@docker-compose restart web

up-web:
	@docker-compose up -d web

stop-web:
	@docker-compose stop web

bash-web:
	@docker-compose exec web bash

syncdb:
	@docker-compose exec web python3 manage.py makemigrations
	@docker-compose exec web python3 manage.py migrate

mergedb:
	@docker-compose exec web python3 manage.py makemigrations --merge

migratedb:
	@docker-compose exec web python3 manage.py migrate

createsuperuser:
	@docker-compose exec web python3 manage.py createsuperuser

collectstatic:
	@docker-compose exec web python3 manage.py collectstatic --clear

createsuperuser_default:
	 @docker-compose exec web python3 manage.py createsuperuser --username admin --email admin@gmail.com  --noinput
token:
	@docker-compose exec web python3 manage.py drf_create_token admin