dpl ?= deploy.env
include $(dpl)
export $(shell sed 's/=.*//' $(dpl))

.PHONY: clean

clean: ## This help.
	rm -f Containers/Docker/plugins/*
	rm -f Containers/Docker/amd-scancode/scancode-*/build/*
	rm -f Containers/Docker/amd-scancode/scancode-*/dist/*
	rm -fr plugins/scancode-*/build/*
	rm -fr plugins/scancode-*/dist/*
	rm -fr plugins/scancode-licence-modifications/src/*.egg-info


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
	docker stop $(APP_NAME); docker rmi -f  $(APP_NAME):latest
