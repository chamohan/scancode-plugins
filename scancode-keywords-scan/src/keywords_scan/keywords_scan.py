from __future__ import unicode_literals
from __future__ import absolute_import, print_function

import typecode
import re
import attr
from commoncode.filetype import counter
from commoncode.functional import memoize
from commoncode import filetype

from collections import OrderedDict
from functools import partial
from itertools import chain

from commoncode import fileutils
from plugincode.scan import ScanPlugin
from plugincode.scan import scan_impl
from scancode import CommandLineOption
from scancode import SCAN_GROUP
from typecode import contenttype

#from sourcecode import kernel
#from sourcecode.metrics import file_lines_count


@scan_impl
class   KeywordsLinesScanner(ScanPlugin):
    """
        Scan the number of lines of code and lines of the keywordss.
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
    codelines = 0
    keywordsline = 0
    codelines, keywordsline = file_lines_count(location)

    return OrderedDict(
        codelines=codelines,
        keywordsline=keywordsline
    )


#@memoize
def file_lines_count(location):
    """
    Return a tuple of (code, keywords) line counts in a source text file at
    `location`. Memoization guarantees that we do only one pass on a file.
    """

    code = 0
    keywords = 0

    T = typecode.contenttype.get_type(location)
    if not T.is_source:
        return code, keywords

    search_list = ['Gibraltar']

    with open(location, 'rb') as lines:

        for line in lines:
            line = line.decode('utf-8')
            if re.compile('|'.join(search_list),re.IGNORECASE).search(line): 
                keywords += 1
            else:
                code += 1

    return code, keywords

def code_lines_count(location):
    code, _keywords = file_lines_count(location)
    return code


def keywords_lines_count(location):
    _code, keywords = file_lines_count(location)
    return keywords


filetype.counting_functions.update({
    'code_lines': code_lines_count,
    'keywords_lines': keywords_lines_count
})


def get_code_lines_count(location):
    """
    Return the cumulative number of lines of code in the whole directory tree
    at `location`. Use 0 if `location` is not a source file.
    """
    return counter(location, 'code_lines')


def get_keywords_lines_count(location):
    """
    Return the cumulative number of lines of keywordss in the whole directory
    tree at `location`. Use 0 if `location` is not a source file.
    """
    return counter(location, 'keywords_lines')
