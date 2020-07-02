#!/usr/bin/env python

import sys
import os
import logging
import click
import scancodestatus


logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout)
logger.setLevel(logging.DEBUG)

@click.command()
@click.option('--dirpath', required=True, help='Directory path of scanresults. For example --dirpath=/path')
def errorchecking(dirpath):
    try:
        path = dirpath
        # Check if path exits
        if os.path.exists(path):
            checkdirectory = scancodestatus.Scanstatus(path)
            exitcode = checkdirectory.scanLogResults()
            return(exitcode)
    except IndexError as err:
        logger.debug("No log files present", err)
        exitcode = 1
        return(exitcode)

if __name__ == "__main__":
    statusexitcode = errorchecking()
    print(statusexitcode)
    sys.exit(statusexitcode)
