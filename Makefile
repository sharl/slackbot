all: build

build:
	docker-compose build

.env: env
	echo UID=$(shell id -u)  > $@
	echo GID=$(shell id -g) >> $@

env:
	rm -f .env
