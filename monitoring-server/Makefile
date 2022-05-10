SHELL=/bin/bash

UID:=$(SHELL id -u)
GID:=$(SHELL id -g)

export UID GID

app-build:
	docker compose build

app-up:
	docker compose up

app-bash:
	docker compose run --rm flask /bin/bash	

app-flask-shell:
	docker compose run  --rm flask flask shell

app-db-reinit: app-db-clear-db app-db-clear-samples app-db-init-samples app-db-recreate-rooms

app-db-init-samples:
	docker compose run  --rm flask flask database init-sample-data

app-db-clear-samples:
	docker compose run  --rm flask flask database clear-sample-data

app-db-clear-db:
	docker compose run  --rm flask flask database clear-db

app-db-clear-users:
	docker compose run  --rm flask flask database clear-user-data

app-db-recreate-rooms:
	docker compose run  --rm flask flask database recreate-rooms

.PHONY: app-up
