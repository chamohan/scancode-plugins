# scancode-plugins
Plugins for Running scancode on RoCm

```
# To Install the Plugins
Go to the Plugin Directory
'''cd scancode-toolkit/plugins/scancode-licence-modifications'''

# Run following command
 '''pip install -e .'''

```

```
# Example : 

'''scancode -clpeui  --package --processes 64 --license-text --verbose --full-root --json-pp roctracer.json ../roctracer --license-policy ../amd_licence_policy.yml --classify --summary --summary-with-details  --license-diag --no-licenses --licence-modifications'''
```


# Create Docker iamge and run scancode . Scancode will create  approved, not approved and license modification html report

```
# docker run -it -v /data/chamohan/src:/src -v  /data/chamohan/logs:/logs -v /data/chamohan/artifacts:/artifacts -v /data/chamohan/statistics:/statistics scancodeimages/amd-scancode /bin/bash

# scancode  -clpeui  --package --processes `expr $(nproc --all) - 1` --classify --keywordsscan --verbose --full-root --json-pp /artifacts/$(date "+%Y.%m.%d-%H.%M.%S")-licenses.json /src --license-policy scancode-plugins/amd_licence_policy.yml --summary --summary-with-details --license-text --license-text-diagnostics --is-license-text  --license-diag  --no-licenses  --licence-modifications --custom-output /artifacts/$(date "+%Y.%m.%d-%H.%M.%S")-license-modification-report.html --custom-template scancode-plugins/license-modification-template.html >>/logs/$(date "+%Y.%m.%d-%H.%M.%S")-logfile 2>&1

```
## To check the overall status
Run scancodestatus.py with json results

For example : 
scancodestatus.py roctracer.json


