# Docker image for AMD Scancode image


# Getting started
```sh
Docker run -v /src:/src:ro -v /logs:/logs -v /artifacts:/artifacts -v /statistics:/statistics scancodeimages/amd_scancode
docker run -it -v `pwd`/src/:/src scancodeimages/amd_scancode
docker run -it -v /data/chamohan/src:/src -v  /data/chamohan/logs:/logs -v /data/chamohan/artifacts:/artifacts -v /data/chamohan/statistics:/statistics scancodeimages/amd_scancode /bin/bash


# Run Tests :
For Example :
## scancode  -clpeui  --package --processes 64 --classify --keywordsscan --verbose --full-root --json-pp /artifacts/$(date "+%Y.%m.%d-%H.%M.%S")-rocrinfo.json /src/rocrinfo --license-policy ./amd_licence_policy.yml --summary --summary-with-details --license-text --license-text-diagnostics --is-license-text  --license-diag  --no-licenses  --licence-modifications --custom-output /artifacts/$(date "+%Y.%m.%d-%H.%M.%S")-license-modification-report.html --custom-template license-modification-template.html >>/logs/$(date "+%Y.%m.%d-%H.%M.%S")-logfile 2>&1


```

## About

By default this image scans for info, licenses, copyrights, packages, emails and urls in the `/src` directory. 


### /logs will contain  the logs file generated during command execution :filename as  timestamp.log
### /artifacts will contain contain the json and html reports. 
### After the scan, you can use the Scancode Workbench for json file and browser for html file to analyse. 
### /statistics will  have <timestamp:json> contain statistics 

#### Note :
status code will be be zero if no violation found
status code will be  be non zero if violation found
numbers of violations as docker exit status code


### Use volume mappings ( `-v`) to mount the respective folder.

### To accelerate the scan, this image uses `N-1` available processors.


