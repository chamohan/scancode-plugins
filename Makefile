# make
# #   1. Go into each plugin directory, execute python3 setup.py bdist_wheel
# # make docker
# #   1. Copy all generated *.whl files into a folder named plugins in Containers/Docker/  directory
# #   2. Go into Containers/Docker and execute docker build -t amd-scancode .
# #   3. Delete Containers/Docker/plugins folder.
#
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help


# Build the container
build: ## Build the container
        for d in ./*/ ; do /bin/bash -c "(python3 setup.py bdist_wheel)"; done
	docker build -t $(APP_NAME) .

build-nc: ## Build the container without caching
	  docker build --no-cache -t $(APP_NAME) .

run: ## Run container 
	docker run -i -t --rm --env-file=./config.env -p=$(PORT):$(PORT) --name="$(APP_NAME)" $(APP_NAME)


stop: ## Stop and remove a running container
	docker stop $(APP_NAME); docker rm $(APP_NAME)

# Docker tagging
tag: tag-latest tag-version ## Generate container tags for the `{version}` ans `latest` tags

tag-latest: ## Generate container `{version}` tag
	@echo 'create tag latest'
	docker tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):latest

tag-version: ## Generate container `latest` tag
	@echo 'create tag $(VERSION)'
	docker tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):$(VERSION)

