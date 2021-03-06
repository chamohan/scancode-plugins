# Copyright (c) 2019 AMD Inc. and others. All rights reserved.
# for any issue please email to chamohan@amd.com

import attr

from plugincode.post_scan import PostScanPlugin
from scancode import CommandLineOption
from scancode import POST_SCAN_GROUP

import logging
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="'time': %(asctime)-15s, 'filename': %(name)s, 'level':  %(levelname)s ,'linenumber': %(lineno)d, 'message': %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
    stream=sys.stdout)

class LicenceModifications(PostScanPlugin):

    """
    Add the "licence_modifications" attribute to a resouce if it does not contain any license
    """

    resource_attributes = dict(licence_modifications=attr.ib(default=attr.Factory(dict)))

    options = [
        CommandLineOption(('--licence-modifications',),
            is_flag=True, default=False,
            help='Generate a list of files in case of modified license',
            help_group=POST_SCAN_GROUP),
    ]

    def is_enabled(self, licence_modifications, **kwargs):
        return licence_modifications

    def process_codebase(self, codebase, licence_modifications, **kwargs):
        """
        Populate a licence_modifications mapping with license modification text
        """
        if not self.is_enabled(licence_modifications):
            return

        for resource in codebase.walk(topdown=True):
            if not resource.is_file:
                continue

            try:
                licence_score_match = set([entry.get('score') for entry in resource.licenses])

            except AttributeError:
                # add licence_modifications regardless if there is license modification info or not
                logger.info("Adding licence_modifications regardless if there is license modification info or not")
                resource.licence_modifications = {}
                codebase.save_resource(resource)
                continue

            for licensemodification in licence_score_match:
                if licensemodification != '100.0':
                    modification_score = 100.00 - licensemodification
                    if modification_score != 0.0:
                        resource.licence_modifications = {"modinfo": "license is %s percent modified "%(modification_score)}
                        codebase.save_resource(resource)
