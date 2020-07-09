import json
import logging
import os
import sys
import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="'time': %(asctime)-15s, 'filename': %(name)s, 'level':  %(levelname)s ,'linenumber': %(lineno)d, 'message': %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
    stream=sys.stdout)


class Scanstatus:

    def __init__(self, directorypath, jsonlogpath):

        self.directorypath = directorypath
        self.jsonlogpath = jsonlogpath

    def scanLogResults(self):

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
            logger.info("OS error: {0}".format(err))
            logger.info("Not able to find/list/sort the files")

        except ValueError as err:
            logger.info("No JSON object could be decoded")

        except IndexError as err:
            logger.info("No log files present")
            totalIssues = totalIssues + 1
            sys.exit(totalIssues)

        try:
            with open(filename) as f:

                data = json.load(f)
                modifications_counter = 0

                for files_info in data['files']:
                    # Checking keywords in file
                    if files_info['keywordsline']:
                        logger.info("File Name %s" % (i['path']))
                        logger.info("Number of keywords %d" % (i['keywordsline']))

                        for matched_lines in files_info['matchedlines']:
                            keywordsCounter = keywordsCounter + 1

                    # Checking Licenses in file

                    if not files_info['no_licenses']:
                        files_with_license = files_with_license + 1
                    else:
                        files_without_license = files_without_license + 1
                        logger.info(
                            "File Name %s is under %s License" % (files_info['path'], files_info['no_licenses']))

                    # Checking Not Approved Licences and Approved License

                    if not files_info['license_policy']:
                        licensePolicy = licensePolicy + 1
                    else:
                        if files_info['license_policy']['label'] == 'Approved License':
                            approvedLicenses = approvedLicenses + 1
                            logger.info(
                                "The file %s has %s" % (files_info['path'], files_info['license_policy']['label']))

                        elif files_info['license_policy']['label'] == 'Prohibited Licenses':
                            prohibitedLicenses = prohibitedLicenses + 1
                            logger.info(
                                "The file %s has %s" % (files_info['path'], files_info['license_policy']['label']))

                    # Checking license Modifications in files

                    if files_info['licenses'] is None:
                        no_license = no_license + 1
                    else:
                        for license_info in files_info['licenses']:

                            if license_info.get('score') != 100.0 and license_info.get('score') is not None:
                                modifications_counter = modifications_counter + 1

            totalIssues = modifications_counter + keywordsCounter + prohibitedLicenses + no_license

            summary_report['Status'] = "Passed"

            if totalIssues > 0:
                summary_report['Status'] = "Failed"

            summary_report['files_without_licenses'] = no_license
            summary_report['number_of_license_modifications'] = modifications_counter

            summary_report['number_of_times_keywords'] = keywordsCounter
            summary_report['number_of_prohibited_licenses'] = prohibitedLicenses

            summary_report['number_of_approved_licenses'] = approvedLicenses
            summary_report['Total_issues'] = totalIssues

            summary_file_name = datetime.datetime.now()
            summary_file_name = str(summary_file_name) + ".summary.json"
            summary_file_name = self.jsonlogpath + "/" + summary_file_name

            try:
                with open(summary_file_name, 'w') as jsonoutfile:
                    json.dump(summary_report, jsonoutfile)
            except RuntimeError as err:
                logger.info("OS error: {0}".format(err))
                logger.info("Not able to the write json file")

            return (totalIssues)
