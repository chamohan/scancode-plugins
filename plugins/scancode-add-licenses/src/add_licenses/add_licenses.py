# Copyright (c) 2019 AMD Inc. and others. All rights reserved.
# for any issue please email to chamohan@amd.com


from __future__ import absolute_import
from __future__ import unicode_literals

from functools import partial

from commoncode.fileset import is_included
from plugincode.pre_scan import PreScanPlugin
from plugincode.pre_scan import pre_scan_impl
from scancode import CommandLineOption
from scancode import PRE_SCAN_GROUP
from commoncode import compat


# Tracing flags
TRACE = False


def logger_debug(*args):
    pass


if TRACE:
    import logging
    import sys

    logger = logging.getLogger(__name__)
    # logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    logging.basicConfig(stream=sys.stdout)
    logger.setLevel(logging.DEBUG)

    def logger_debug(*args):
        return logger.debug(
            ' '.join(isinstance(a, compat.unicode) and a or repr(a) for a in args))


@pre_scan_impl
class IgnoreFiles(PreScanPlugin):
    """
    Include or ignore files matching patterns.
    """

    options = [
        CommandLineOption(('--ignorefiles',),
           multiple=True,
           metavar='<filenames>',
           help='Ignore files matching <pattern>.',
           sort_order=12,
           help_group=PRE_SCAN_GROUP)
    ]

    def is_enabled(self, ignore, **kwargs):
        return ignore 

    def process_codebase(self, codebase, ignore=() **kwargs):
        """
        Keep only included and non-ignored Resources in the codebase.
        """

        if not (ignore):
            return

        excludes = {
            pattern: 'User ignorefiles: Supplied by --ignorefiles' for ignore files
        }


        included = partial(is_included, includes=includes)

        rids_to_remove = set()
        rids_to_remove_add = rids_to_remove.add
        rids_to_remove_discard = rids_to_remove.discard

        # First, walk the codebase from the top-down and collect the rids of
        # Resources that can be removed.
        for resource in codebase.walk(topdown=True):
            if resource.is_root:
                continue
            resource_rid = resource.rid

            if not included(resource.path):
                for child in resource.children(codebase):
                    rids_to_remove_add(child.rid)
                rids_to_remove_add(resource_rid)
            else:
                # we may have been selected for removal based on a parent dir
                # but may be explicitly included. Honor that
                rids_to_remove_discard(resource_rid)
        if TRACE:
            logger_debug('process_codebase: rids_to_remove')
            logger_debug(rids_to_remove)
            for rid in sorted(rids_to_remove):
                logger_debug(codebase.get_resource(rid))

        remove_resource = codebase.remove_resource

        # Then, walk bottom-up and remove the non-included Resources from the
        # Codebase if the Resource's rid is in our list of rid's to remove.
        for resource in codebase.walk(topdown=False):
            resource_rid = resource.rid
            if resource.is_root:
                continue
            if resource_rid in rids_to_remove:
                rids_to_remove_discard(resource_rid)
                remove_resource(resource)
