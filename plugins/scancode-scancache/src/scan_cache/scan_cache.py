# Copyright (c) 2019 AMD Inc. and others. All rights reserved.
# For any issue please write to chamohan@amd.com

import attr

from plugincode.post_scan import PostScanPlugin
from scancode import CommandLineOption
from scancode import POST_SCAN_GROUP

import logging
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout)
logger.setLevel(logging.DEBUG)


class ScanCache(PostScanPlugin):

    """
    Store the SHA1 and MD4 hash of files to redis server
    """

    resource_attributes = dict(scan_cache=attr.ib(default=attr.Factory(dict)))

    options = [
        CommandLineOption(('--scancache',),\
            is_flag=True, default=False,\
            help='Generate a list of no licences files',\
            help_group=POST_SCAN_GROUP),
    ]

    def is_enabled(self, scan_cache, **kwargs):
        return scan_cache

    def process_codebase(self, codebase, scan_cache, **kwargs):
        """
        Save the first time scan of results in redis database.
        """
        if not self.is_enabled(scan_cache):
            return

        for resource in codebase.walk(topdown=True):

            if not resource.is_file:
                continue

            try:
                #read the result and save it in redis cache
                resource_scan_cache = set([entry.get('short_name') for entry in resource.licenses])

            except AttributeError:
                # add scan_cache regardless if there is license info or not
                logger.dubug("not able to save the resource in redis cache")
                continue
