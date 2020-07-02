#!/usr/bin/env python

import click
import scancodestatus
import sys
import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout)
logger.setLevel(logging.DEBUG)

click.command()
@click.option('--dirpath', help='Directory path of scan result location')
def errorchecking(dirpath):
    try:
        path = dirpath
        # Check if path exits
        if os.path.exists(path):
            checkdirectory = scancodestatus.Scanstatus(path)
            exitcode = checkdirectory.scanLogResults()
            return exitcode
    except OSError as err:
        logger.debug("OS error: {0}".format(err))
        logger.debug("Not able to find/list/sort the files")
    except IndexError as err:
        logger.debug("No log files present")
        totalIssues = totalIssues + 1
        return totalIssues

if __name__ == "__main__":
    statusexitcode = errorchecking()
    print(statusexitcode)
    sys.exit(statusexitcode)
