# Copyright (c) 2019 AMD Inc. and others. All rights reserved.
# for any issue please email to chamohan@amd.com

import attr

from plugincode.post_scan import PostScanPlugin
from scancode import CommandLineOption
from scancode import POST_SCAN_GROUP

import sys

class NoLicenses(PostScanPlugin):

    """
    Add the "no_licenses" attribute to a resouce if it does not contain any license
    """

    resource_attributes = dict(no_licenses=attr.ib(default=attr.Factory(dict)))

    sort_order = 9


    options = [
        CommandLineOption(('--no-licenses',),
            is_flag=True, default=False,
            help='Generate a list of no licences files',
            help_group=POST_SCAN_GROUP),
    ]

    def is_enabled(self, no_licenses, **kwargs):
        return no_licenses

    def process_codebase(self, codebase, no_licenses, **kwargs):
        """
        Populate a no_license mapping with four attributes: filename, label,
        icon, and color_code at the File Resource level.
        """
        if not self.is_enabled(no_licenses):
            return

        for resource in codebase.walk(topdown=True):
            if not resource.is_file:
                continue

            try:
                resource_no_licenses = set([entry.get('short_name') for entry in resource.licenses])

            except AttributeError:
                # add no_licenses regardless if there is license info or not
                logger.dubug("add no_licenses regardless if there is license info or not")
                resource.no_licenses = {}
                codebase.save_resource(resource)
                continue

            for license in resource_no_licenses:
                if license:
                    resource.no_licenses = "%s is Present"%(license)
                    codebase.save_resource(resource)
