# Copyright (c) 2019 AMD Inc. and others. All rights reserved.
# for any issue please email to chamohan@amd.com

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import attr

from plugincode.post_scan import PostScanPlugin
from scancode import CommandLineOption
from scancode import POST_SCAN_GROUP

LOGSTRACE = False

def logger_debug(*args):
    pass


if LOGSTRACE:
    import logging
    import sys

    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=sys.stdout)
    logger.setLevel(logging.DEBUG)

    def logger_debug(*args):
        return logger.debug(
            ' '.join(isinstance(a, compat.unicode) and a or repr(a) for a in args))



class scanResults(PostScanPlugin):

    """
    Create the json and HTML scan results reports 
    """

    options = [
                  CommandLineOption(('--scan-results',),
                      is_flag=True, default=False,
                      help='Generate HTML and Json report of scan results ',
                      help_group=POST_SCAN_GROUP),

	          CommandLineOption(('--ignore-files',),
                      multiple=True,
                      help='Ignore files matching names in yaml file.',
                      help_group=POST_SCAN_GROUP),
    ]


    def process_codebase(self, codebase, scan_results, **kwargs):
        """
        Populate a scan_results json for html templates and visual tools 
        """
        if not self.is_enabled(scan_results):
            return

        for resource in codebase.walk(topdown=True):
            if not resource.is_file:
                continue

            try:
                scan_results_license_match = set([entry.get('score') for entry in resource.licenses])
                scan_results_no_license_match = set([entry.get 
                scan_results_keywords_match = set([entry.get
                scan_results_only_license_titles = set([entry.get

            except AttributeError:
                # add scan_results regardless if there is info or not
                resource.scan_results = {}
                codebase.save_resource(resource)
                continue


    def latestJsonReportsfile(self, path):
        os.chdir(path)
        files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
        no_license = 0
        # latest  json report file name created with time stamp
        filename = files[-2]
        return filename

    def scanLogresults():
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
        filename = latestJsonReportsfile()

        try:
            with open(filename) as f:
                data = json.load(f)
                modifications_counter = 0
                for i in data['files']:
                    # Checking keywords in file
                    if i['keywordsline']:
                        logger_debug("File Name %s" % (i['path']))
                        logger_debug("Number of keywords %d" % (i['keywordsline']))
                        for m in i['matchedlines']:
                            keywordsCounter = keywordsCounter + 1

                    # Checking Licenses in file

                    if not i['no_licenses']:
                        files_with_license = files_with_license + 1
                    else:
                        files_without_license = files_without_license + 1
                        logger_debug("File Name %s is under %s License" % (i['path'], i['no_licenses']))

                    # Checking Not Approved Licences and Approved License

                    if not i['license_policy']:
                        licensePolicy = licensePolicy + 1
                    else:
                        if i['license_policy']['label'] == 'Approved License':
                            approvedLicenses = approvedLicenses + 1
                            logger_debug("The file %s has %s" % (i['path'], i['license_policy']['label']))
                        elif i['license_policy']['label'] == 'Prohibited Licenses':
                            prohibitedLicenses = prohibitedLicenses + 1
                            logger_debug("The file %s has %s" % (i['path'], i['license_policy']['label']))

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
                if LOGSTRACE:
                totalIssues = (modifications_counter + keywordsCounter + prohibitedLicenses + no_license)
                logger_debug("-----Summary Report------")
                logger_debug("The total number of files containing no linceses are %d" % (no_license))
                logger_debug("Number of linceses Modifications %d" % (modifications_counter))
                logger_debug("The number of times keywords were present in files %s" % (keywordsCounter))
                logger_debug("The number of Prohibited Licenses are %s" % (prohibitedLicenses))
                logger_debug("The number of Approved Linceses are %s" % (approvedLicenses))
                logger_debug("The Total number of issues are %s" % (totalIssues))
                logger_debug("Failed")
                return totalIssues
            else:
                logger_debug("The number of Approved Linceses are %s" % (approvedLicenses))
                logger_debug("Tests Passed")
                return approvedLicenses

        except OSError as err:
            logger_debug("OS error: {0}".format(err))
            return totalIssues

    startcheck = scanCodeStatus()

exitcode = startcheck.scanLogResults('/artifacts')

sys.exit(exitcode)

