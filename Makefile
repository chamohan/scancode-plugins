dpl ?= deploy.env
include $(dpl)
export $(shell sed 's/=.*//' $(dpl))

.PHONY: clean

clean: ## This help.
	find ./ -name *.egg-info -o -name *.pyc -o -name *.whl -o -name bdist.linux-* -o -name 'lib'|xargs rm -fr

.DEFAULT_GOAL := help

help:
	echo "Run as make build or make clean or make build-nc or make stop"
	echo " make clean"
	echo " make build"

build: ## Build the container
	./createwheeler.sh
	docker build -t $(APP_NAME) -f Containers/Docker/Dockerfile .

build-nc: ## Build the container without caching
	./createwheeler.sh
	docker build --no-cache -t $(APP_NAME) -f Containers/Docker/Dockerfile .

stop: ## Stop and remove a running image and container
	docker rmi -f $(APP_NAME):latest
