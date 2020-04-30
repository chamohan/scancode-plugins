from __future__ import absolute_import
from __future__ import unicode_literals

from collections import OrderedDict
from functools import partial
from itertools import chain

import attr
import scanfile.py

from commoncode import fileutils
from plugincode.scan import ScanPlugin
from plugincode.scan import scan_impl
from scancode import CommandLineOption
from scancode import SCAN_GROUP
from typecode import contenttype

from sourcecode import kernel
from sourcecode.metrics import file_lines_count


@scan_impl
class 	KeywordsLinesScanner(ScanPlugin):
    """
    Scan the number of lines of code and lines of the comments.
    """
    resource_attributes = OrderedDict(
        codelines=attr.ib(default=attr.Factory(int), repr=False),
        keywordsline=attr.ib(default=attr.Factory(int), repr=False),

    )

    options = [
        CommandLineOption(('--keywordsscan',),
            is_flag=True, default=False,
            help='  Scan the number of lines of code and search for keywords.',
            help_group=SCAN_GROUP,
            sort_order=100),
    ]

    def is_enabled(self, keywordsscan, **kwargs):
        return keywordsscan

    def get_scanner(self, **kwargs):
        return get_keywordsscan


def get_keywordsscan(location, **kwargs):
    """
    Return the cumulative number of lines of code in the whole directory tree
    at `location`. Use 0 if `location` is not a source file.
    """
    codelines = 0
    keywordsline = 0
    codelines, keywordsline = file_lines_count(location)
    return OrderedDict(
        codelines=codelines,
        keywordsline=keywordsline
    )
