import json
import logging
import os
import sys
import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout)
logger.setLevel(logging.DEBUG)

class Scanstatus:

    def __init__(self, directorypath, jsonlogpath):

        self.directorypath = directorypath 
        self.jsonlogpath = jsonlogpath

    def scanLogResults(self):
        code = 0
        keywords = 0
        matching_keywords = []
        line_numbers = []
        line_no = 0
        matched_lines = []
        keywordsCounter = 0
        files_with_license = 0
        files_without_license = 0
        licensePolicy = 0
        approvedLicenses = 0
        prohibitedLicenses = 0
        totalIssues = 0
        summary_report = {}
         

        try:
            os.chdir(self.directorypath)
            files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
            no_license = 0
            # latest  json report file name created with time stamp
            filename = files[-1]
        except OSError as err:
            logger.debug("OS error: {0}".format(err))
            logger.debug("Not able to find/list/sort the files")
        except ValueError as err:
            logger.debug("No JSON object could be decoded")
        except IndexError as err:
            logger.debug("No log files present") 
            totalIssues = totalIssues + 1
            sys.exit(totalIssues)
         

        try:
            with open(filename) as f:
                data = json.load(f)
                modifications_counter = 0
                for i in data['files']:
                    # Checking keywords in file
                    if i['keywordsline']:
                        logger.debug("File Name %s" % (i['path']))
                        logger.debug("Number of keywords %d" % (i['keywordsline']))
                        for m in i['matchedlines']:
                            keywordsCounter = keywordsCounter + 1

                    # Checking Licenses in file

                    if not i['no_licenses']:
                        files_with_license = files_with_license + 1
                    else:
                        files_without_license = files_without_license + 1
                        logger.debug("File Name %s is under %s License" % (i['path'], i['no_licenses']))

                    # Checking Not Approved Licences and Approved License

                    if not i['license_policy']:
                        licensePolicy = licensePolicy + 1
                    else:
                        if i['license_policy']['label'] == 'Approved License':
                            approvedLicenses = approvedLicenses + 1
                            logger.debug("The file %s has %s" % (i['path'], i['license_policy']['label']))
                        elif i['license_policy']['label'] == 'Prohibited Licenses':
                            prohibitedLicenses = prohibitedLicenses + 1
                            logger.debug("The file %s has %s" % (i['path'], i['license_policy']['label']))

                    # Checking license Modifications in files

                    if i['licenses'] is None:
                        no_license = no_license + 1
                    else:
                        for j in i['licenses']:
                            try:
                                if j['score'] != 100.0:
                                    modifications_counter = modifications_counter + 1
                            except Exception:
                                continue

            if modifications_counter > 0:
                totalIssues = (modifications_counter + keywordsCounter + prohibitedLicenses + no_license)
                summary_report['files_without_licenses'] = no_license 
                summary_report['number_of_license_modifications'] = modifications_counter
                summary_report['number_of_times_keywords'] = keywordsCounter
                summary_report['number_of_prohibited_licenses'] = prohibitedLicenses
                summary_report['number_of_approved_licenses'] = approvedLicenses
                summary_report['Total_issues'] = totalIssues
                summary_report['Status'] = "Failed"
                try:
                    with open(self.jsonlogpath/datetime.datetime.now().summary.json, 'w') as\
                            jsonoutfile:
                        json.dump(summary_report, jsonoutfile)
                except RuntimeError as err:
                    logger.debug("OS error: {0}".format(err))
                    logger.debug("Not able to the write json file")
                return(totalIssues)
     
            if modifications_counter == 0:
                summary_report ['number_of_approved_licenses'] = approvedLicenses 
                summary_report['Status'] = "Passed"
                return(approvedLicenses)
        except RuntimeError as err:
            logger.debug("RuntimeError: {0}".format(err))
            return(totalIssues)


