# make
# #   1. Go into each plugin directory, execute python3 setup.py bdist_wheel
# # make docker
# #   1. Copy all generated *.whl files into a folder named plugins in Containers/Docker/  directory
# #   2. Go into Containers/Docker and execute docker build -t amd-scancode .
# #   3. Delete Containers/Docker/plugins folder.
#

# import deploy config
# You can change the default deploy config with `make cnf="deploy_special.env" release`
dpl ?= deploy.env
include $(dpl)
export $(shell sed 's/=.*//' $(dpl))

.PHONY: clean 

clean: ## This help.
	rm -R Containers/Docker/plugins/*
	rm -R Containers/Docker/amd-scancode/scancode-*/build/*
	rm -R Containers/Docker/amd-scancode/scancode-*/dist/*

.DEFAULT_GOAL := help

help:
	echo "Run as make build or make clean or make build-nc or make stop"


build: ## Build the container
	./createwheeler.sh
	cd Containers/Docker/;docker build -t $(APP_NAME) .

build-nc: ## Build the container without caching
	./createwheeler.sh
	cd Containers/Docker/;docker build --no-cache -t $(APP_NAME) .

run: ## Run container 
	docker run -i -t --rm --env-file=./config.env -p=$(PORT):$(PORT) --name="$(APP_NAME)" $(APP_NAME)


stop: ## Sto and remove a running container
	docker stop $(APP_NAME); docker rm $(APP_NAME)

# Docker tagging
tag: tag-latest tag-version 

tag-latest: ## Generate container `{version}` tag
	@echo 'create tag latest'
	docker tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):latest

tag-version: ## Generate container `latest` tag
	@echo 'create tag $(VERSION)'
	docker tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):$(VERSION)

