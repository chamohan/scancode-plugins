import re

from collections import OrderedDict
from commoncode.filetype import counter
from commoncode import filetype
from plugincode.scan import ScanPlugin
from plugincode.scan import scan_impl
from scancode import CommandLineOption
from scancode import SCAN_GROUP

import click
import attr
import yaml

from os.path import exists
from commoncode.fileutils import PATH_TYPE


import logging
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout)
logger.setLevel(logging.DEBUG)


@scan_impl
class KeywordsLinesScanner(ScanPlugin):
    """
        Scan the number of lines of code and lines of the keywords
    """
    resource_attributes = OrderedDict(
        codelines=attr.ib(default=attr.Factory(int), repr=False),
        keywordsline=attr.ib(default=attr.Factory(int), repr=False),
        matchedlines=attr.ib(default=attr.Factory(list), repr=False),

    )

    options = [
        CommandLineOption(('--keyword-scan',),
                          type=click.Path(
                              exists=True, file_okay=True, dir_okay=False,
                              readable=True, path_type=PATH_TYPE),
                          metavar='FILE',
                          help='Use this yml file to read the keywords',
                          help_group=SCAN_GROUP,
                          sort_order=100),
    ]

    def is_enabled(self, keyword_scan, **kwargs):
        print("The start line")
        print(keyword_scan)
        print("The end line")
        return keyword_scan

    def get_scanner(self, **kwargs):
        print("This is the message")
        print(keyword_scan)
        print("The end message")
        return get_keywordsscan


def get_keywordsscan(location, keyword_scan, **kwargs):

    codelines = 0
    keywordsline = 0
    matchedlines = []
    codelines, keywordsline, matchedlines = file_lines_count(location, keyword_scan)

    return OrderedDict(
        codelines=codelines,
        keywordsline=keywordsline,
        matchedlines=matchedlines
    )


def file_lines_count(location, keyword_scan):
    """
    Return a tuple of (code, keywords, matching_keywords, line_numbers) line
    counts in a source text file at `location`.
    """
    code = 0
    keywords = 0
    line_numbers = []
    line_no = 0
    matched_lines = []
    searchList = []

    try:
        with open(keyword_scan) as data:
            searchList = yaml.safe_load(data)

        if len(searchList) == 0:
            logger.debug("The file is either not yaml formatted or contain no data")
            sys.exit("The file is either not yaml formatted or contain no data")

    except IOError:
        logger.debug("File not accessible")
        sys.exit("File not accessible")

    try:
        with open(location, 'rb') as lines:

            for line in lines:
                line = line.decode('utf-8')
                line_no += 1
                if re.findall(r"(?=("+'|'.join(searchList)+r"))", line):
                    keywords += 1
                    line_numbers.append(line_no)
                    matched_test = "line no %d has - %s keywords" %(line_no, line)
                    matched_lines.append(matched_test)
                else:
                    code += 1
    except IOError:
        logger.debug("File not accessible")
        sys.exit("File not accessible")
    return code, keywords, matched_lines


def code_lines_count(location):
    code, _keywords, matched_lines = file_lines_count(location)
    return code


def keywords_lines_count(location):
    _code, keywords, matched_lines = file_lines_count(location)
    return keywords

def matched_lines(location):
    code, _keywords, matched_lines = file_lines_count(location)
    return matched_lines


filetype.counting_functions.update({
    'code_lines': code_lines_count,
    'keywords_lines': keywords_lines_count,
    'matched_lines': matched_lines
})

