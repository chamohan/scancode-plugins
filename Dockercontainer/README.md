# Docker image for AMD Scancode imange


# Getting started
```sh
Docker run -v /src:/src:ro -v /logs:/logs -v /artifacts:/artifacts -v /statistics:/statistics scancodeimages/amd_scancode
docker run -it -v `pwd`/src/:/src scancodeimages/amd_scancode

# Your should see the verbose output of the scan

# The result file will be available as result.json and result.html

```

## About
By default this image scans for info, licenses, copyrights, packages, emails and urls in the `/r]src` directory. Use volume mappings ( `-v`) to mount the respective folder. The resulting file will be available as `licenses.json`.

To accelerate the scan, this image uses `N-1` available processors.
After the scan, you can use the Scancode Workbench for json file and browser for html file to analyse. 

