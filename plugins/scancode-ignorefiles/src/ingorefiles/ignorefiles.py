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
    Ignore scan of files and directories  stored in scancode cache.
    """

    options = [
        CommandLineOption(('--ignore-files',),
                          is_flag=True,
                          help='Ignore files.',
                          sort_order=10,
                          help_group=PRE_SCAN_GROUP)
    ]

    def is_enabled(self, ignore_files, **kwargs):
        return ignore_files

    def process_codebase(self, codebase, ignore_files, **kwargs):

        """
        Remove files and Resources from the resource tree.

        """

        if not ignore_files:
            return

        resources_to_remove = []

        # Walking over the given codebase to collect resource of files to remove.

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
    try:
        # connect to redis server and check the files present
        t = file_present(location)

    return t 

    except OSError as err:
        logger.debug("OS error: {0}".format(err))
        logger.debug("Not able to find/list/sort the files")
    except ValueError as err:
        logger.debug("No JSON object could be decoded")
    except IndexError as err:
        logger.debug("No log files present") 
        totalIssues = totalIssues + 1
        sys.exit(totalIssues)
         

