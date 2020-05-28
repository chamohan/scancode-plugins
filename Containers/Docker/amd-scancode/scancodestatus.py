#!/usr/bin/env python
# In case of any issue please write chamohan@amd.com
# Author : Chander

import json
import sys
import os

path = '/artifacts'
os.chdir(path)
files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
no_license = 0
#latest  json file name
filename = files[-2]
keywordsCounter = 0
files_with_license = 0
files_without_license = 0
licensePolicy = 0
approvedLicenses = 0
prohibitedLicenses = 0
totalIssues = 0

try:

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


            # Checking Not Approved Licences and Approved License

            if not i['license_policy']:
               licensePolicy = licensePolicy + 1
            else:
                if i['license_policy']['label'] == 'Approved License':
                    approvedLicenses = approvedLicenses + 1
                    print("The file %s has %s" %(i['path'],i['license_policy']['label']))
                elif i['license_policy']['label'] == 'Prohibited Licenses':
                    prohibitedLicenses = prohibitedLicenses + 1
                    print("The file %s has %s" %(i['path'],i['license_policy']['label']))

            # Checking license Modifications in files


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
        totalIssues = ( modifications_counter + keywordsCounter + prohibitedLicenses + no_license )
        print("-----Summary Report------")
        print("The total number of files containing no linceses are %d" %(no_license))
        print("Number of linceses Modifications %d" %(modifications_counter))
        print("The number of times keywords were present in files %s" %(keywordsCounter))
        print("The number of Prohibited Licenses are %s" %(prohibitedLicenses))
        print("The number of Approved Linceses are %s" %(approvedLicenses))
        print("The Total number of issues are %s" %(totalIssues))
        print("Failed")
        sys.exit(totalIssues)
    else:
        print("The number of Approved Linceses are %s" %(approvedLicenses))
        print("Tests Passed")
        sys.exit(approvedLicenses)

except OSError as err:
    print("OS error: {0}".format(err))
    sys.exit(totalIssues)
