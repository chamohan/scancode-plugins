#!/usr/bin/env python
# In case of any issue please write chamohan@amd.com

import json
import sys
import os

path = '/artifacts'
os.chdir(path)
files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
no_license = 0
oldest = files[0]
#latest  json file name
filename = files[-2]
counter = 0

with open(filename) as f:
    data = json.load(f)
    modifications_counter = 0
    for i in data['files']:
        if i['keywordsline']:
            print("keywords present")
            print(i['keywordsline'])
            print(i['matchedlines'])
            counter = counter + 1

        if i['licenses'] is None:
            no_license = no_license + 1
        else:
            for j in i['licenses']:
                try:
                    if j['score'] != 100.0:
                        modifications_counter = modifications_counter + 1
                except Exception:
                    pass


if modifications_counter > 0:
    print("The total number of files containing no linceses are %d" %(no_license))
    print("Number of linceses Modifications %d" %(modifications_counter))
    print("The number of times keywords present in files %s" %(counter))
    print("Failed")
    sys.exit(1)
else:
    print("Tests Passed")
