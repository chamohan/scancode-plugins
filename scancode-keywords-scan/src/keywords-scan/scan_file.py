from __future__ import absolute_import, print_function


import typecode
from commoncode.filetype import counter
from commoncode.functional import memoize
from commoncode import filetype


@memoize
def file_lines_count(location, keywords):
    """
    Return a tuple of (code, comment) line counts in a source text file at
    `location`. Memoization guarantees that we do only one pass on a file.
    """

    code = 0
    comment = 0

    T = typecode.contenttype.get_type(location)
    if not T.is_source:
        return code, comment

    with open(location, 'rb') as lines:
        for line in lines:
            if any(word in line for word in keywords):
                    comment += 1
                else:
                    code += 1
    return code, comment


def code_lines_count(location):
    code, _comment = file_lines_count(location)
    return code


def comment_lines_count(location):
    _code, comment = file_lines_count(location)
    return comment


filetype.counting_functions.update({
    'code_lines': code_lines_count,
    'comment_lines': comment_lines_count
})


def get_code_lines_count(location):
    """
    Return the cumulative number of lines of code in the whole directory tree
    at `location`. Use 0 if `location` is not a source file.
    """
    return counter(location, 'code_lines')


def get_comment_lines_count(location):
    """
    Return the cumulative number of lines of comments in the whole directory
    tree at `location`. Use 0 if `location` is not a source file.
    """
    return counter(location, 'comment_lines')
