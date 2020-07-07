# Copyright (c) 2019 AMD Inc. and others. All rights reserved.
# For any issue please write to chamohan@amd.com

import attr

from plugincode.post_scan import PostScanPlugin
from scancode import CommandLineOption
from scancode import POST_SCAN_GROUP
import redis
import json
import logging
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout)
logger.setLevel(logging.DEBUG)

# Tracing flags
TRACE = False
SCAN= False

@post_scan_impl
class ScanCache(PostScanPlugin):
    """
    Store the SHA1 and MD4 hash of files to redis server
    """
    resource_attributes = dict(scan_cache=attr.ib(default=attr.Factory(dict)))

    options = [
        CommandLineOption(('--scancache',),\
                          is_flag=True, default=False,\
                          help='True/False option to store the jason result in redis cache',\
                          help_group=POST_SCAN_GROUP),

        CommandLineOption(('--redisurl',),\
                          type=str, default='localhost',\
                          required_options=['scancacache'],\
                          help='redis url for the redis cache',\
                          help_group=POST_SCAN_GROUP),
    ]

    def is_enabled(self, scan_cache, redisurl, **kwargs):
        return scan_cache and redisurl

    def process_codebase(self, codebase, scan_cache, redisurl, **kwargs):
        """
        Save the first time scan of results in redis database.
        """
        redisList = []
        try:
            with open('/amd-scancode/redisserver.yml') as data:
                 redisList = yaml.safe_load(data)

            if len(searchList) == 0:
                log_debug("The file is either not yaml formatted or contain no data")
                sys.exit("The file is does not have login password data ")
        except IOError:
            log_debug("File not accessible")
            sys.exit("File not accessible")

        if not self.is_enabled(scan_cache):
            try:
                r = redis.Redis(host=redisurl, port=6379, db=0)

                r.execute_command('JSON.SET', 'object', '.', json.dumps(codebase))
            except AttributeError:
                # add scan_cache regardless if there is license info or not
                logger.dubug("not able to save the resource in redis cache")
                continue
