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
	rm -f Containers/Docker/plugins/*
	rm -f Containers/Docker/amd-scancode/scancode-*/build/*
	rm -f Containers/Docker/amd-scancode/scancode-*/dist/*
	rm -fr plugins/scancode-*/build/*
	rm -fr plugins/scancode-*/dist/*


.DEFAULT_GOAL := help

help:
	echo "Run as make build or make clean or make build-nc or make stop"
	echo " make clean"
	echo " make build"

build: ## Build the container
	pip install wheel
	./createwheeler.sh
	docker build -t $(APP_NAME) -f Containers/Docker/Dockerfile .

build-nc: ## Build the container without caching
	./createwheeler.sh
	docker build --no-cache -t $(APP_NAME) -f Containers/Docker/Dockerfile .

stop: ## Sto and remove a running container
	docker stop $(APP_NAME); docker rm $(APP_NAME)
