# Docker image for AMD Scancode imange


# Getting started
```sh
Docker run -v /src:/src:ro -v /logs:/logs -v /artifacts:/artifacts -v /statistics:/statistics scancodeimages/amd_scancode
docker run -it -v `pwd`/src/:/src scancodeimages/amd_scancode
docker run -it -v /data/chamohan/src:/src -v  /data/chamohan/logs:/logs -v /data/chamohan/artifacts:/artifacts -v /data/chamohan/statistics:/statistics scancodeimages/amd_scancode /bin/bash




scancode  -clpeui  --package --processes 64 --classify --keywordsscan --verbose --full-root --json-pp rocrinfo.json /src/rocrinfo --license-policy ./amd_licence_policy.yml --summary --summary-with-details --license-text --license-text-diagnostics --is-license-text  --license-diag  --no-licenses  --licence-modifications --custom-output license-modification-list.html --custom-template license-modification-template.html | while IFS= read -r line; do printf '%s %s\n' "$(date)" "$line"; done >>/logs/logfile 2>&1

 
# Your should see the verbose output of the scan

# The result file will be available as result.json and result.html

```

## About
By default this image scans for info, licenses, copyrights, packages, emails and urls in the `/src` directory. Use volume mappings ( `-v`) to mount the respective folder. The resulting file will be available as `licenses.json`.

To accelerate the scan, this image uses `N-1` available processors.
After the scan, you can use the Scancode Workbench for json file and browser for html file to analyse. 

