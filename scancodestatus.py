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
keywordsCounter = 0
files_with_license = 0
files_without_license = 0

with open(filename) as f:
    data = json.load(f)
    modifications_counter = 0
    for i in data['files']:
        # Checking keywords in file
        if i['keywordsline']:
            print("File Name %s" %(i['path']))
            print("Number of keywords %d" %(i['keywordsline']))
            for m in i['matchedlines']:
                print(m)
            keywordsCounter = keywordsCounter + 1

        # Checking Licenses in file

        if not i['no_licenses']:
            files_with_license = files_with_license + 1
        else:
            files_without_license = files_without_license + 1
            print("File Name %s is under %s License" %(i['path'],i['no_licenses']))

        # Checking license Modifications in files

        if i['licenses'] is None:
            no_license = no_license + 1
        else:
            for j in i['licenses']:
                try:
                    if j['score'] != 100.0:
                        #print(j['score'])
                        #print(i['path'])
                        #print(i['licenses'])
                        #print(i['licence_modifications'])
                        modifications_counter = modifications_counter + 1
                except Exception:
                    pass


if modifications_counter > 0:
    print("-----Summary Report------")
    print("The total number of files containing no linceses are %d" %(no_license))
    print("Number of linceses Modifications %d" %(modifications_counter))
    print("The number of times keywords were present in files %s" %(keywordsCounter))
    print("Tests Failed")
    sys.exit(1)
else:
    print("Tests Passed")
