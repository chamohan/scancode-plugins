# How to Build the Dockerimage and container for Scancode

```
*  Run Makefiles
*  INSTALL
*  replace the vars in deploy.env
*  define the version script

# Clean the temp build files if any
    * make clean
# Following will Build the Dockerimage and Run the Container
    * make build
# Now the Docker Container is ready so run the 
    * docker run -it -v /src:/src -v  /logs:/logs -v /artifacts:/artifacts -v /statistics:/statistics amd-scancode:latest

# Check the exit status 
    * $echo $?

# Build the container with differnt config and deploy file
    * make cnf=another_config.env dpl=another_deploy.env build

```

# Steps to Clean the workspace and Build and Run the Container
```

*  make clean

*  make build

*  docker run -it -v /src:/src -v  /logs:/logs -v /artifacts:/artifacts -v /statistics:/statistics amd-scancodelatest:latest

*  $echo $?

```
