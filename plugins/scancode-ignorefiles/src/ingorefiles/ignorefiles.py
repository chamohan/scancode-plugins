import json
import logging
import os
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout)
logger.setLevel(logging.DEBUG)
from functools import partial


from plugincode.pre_scan import PreScanPlugin
from plugincode.pre_scan import pre_scan_impl
from scancode import CommandLineOption
from scancode import PRE_SCAN_GROUP
from typecode.contenttype import get_type


@pre_scan_impl
class IgnoreFiles(PreScanPlugin):
    """
    Ignore files stored in scancode cache.
    """

    options = [
        CommandLineOption(('--ignore-files',),
                          is_flag=True,
                          help='Ignore files.',
                          sort_order=10,
                          help_group=PRE_SCAN_GROUP)
    ]

    def is_enabled(self, ignore_files, **kwargs):
        return ignore_binaries

    def process_codebase(self, codebase, ignore_files, **kwargs):
        """
        Remove files and Resources from the resource tree.
        """
        if not ignore_files:
            return

        resources_to_remove = []

        # walk the codebase to collect resource of files to remove.
        for resource in codebase.walk():
            if not resource.is_file:
                continue

            if is_filepresentincache(resource.location):
                resources_to_remove.append(resource)

        # second, effectively remove the files
        for resource in resources_to_remove:
            resource.remove(codebase)


def is_filepresentincache(location):
    """
    Return True if the resource at location is a file in redis cache.
    """
    t = get_type(location)
    return (
            t.is_binary
            or t.is_archive
            or t.is_media
            or t.is_office_doc
            or t.is_compressed
            or t.is_filesystem
            or t.is_winexe
            or t.is_elf
            or t.is_java_class
            or t.is_datao
    )
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
                logger.debug("-----Summary Report------")
                logger.debug("The total number of files containing no linceses are %d" % (no_license))
                logger.debug("Number of linceses Modifications %d" % (modifications_counter))
                logger.debug("The number of times keywords were present in files %s" % (keywordsCounter))
                logger.debug("The number of Prohibited Licenses are %s" % (prohibitedLicenses))
                logger.debug("The number of Approved Linceses are %s" % (approvedLicenses))
                logger.debug("The Total number of issues are %s" % (totalIssues))
                logger.debug("Failed")
                sys.exit(totalIssues)
            else:
                logger.debug("The number of Approved Linceses are %s" % (approvedLicenses))
                logger.debug("Tests Passed")
                sys.exit(approvedLicenses)

        except RuntimeError:
            logger.debug("RuntimeError: {0}".format(err))
            sys.exit(totalIssues)
}