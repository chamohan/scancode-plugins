#!/usr/bin/env python

import sys
import os
import logging
import click
import scancodestatus


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
    except IndexError as err:
        logger.debug("No log files present", err)
        exitcode: int = 1
        return exitcode

if __name__ == "__main__":
    statusexitcode = errorchecking()
    print(statusexitcode)
    sys.exit(statusexitcode)
