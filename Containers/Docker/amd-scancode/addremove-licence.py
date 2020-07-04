#!/usr/bin/env python

import sys
import os
import addremovelicensess
import logger
import click


logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout)
logger.setLevel(logging.DEBUG)

@click.command()
@click.option('--dirpath', required=True, help='Directory path of scanresults. For example --dirpath=/path')
def license(licenceoption):
    try:
        path = dirpath
        # Check if path exits
        if os.path.exists(path):
            checkdirectory = scancodestatus.Scanstatus(path)
            exitcode = checkdirectory.scanLogResults()
            return exitcode
        else:
            return 1
    except OSError as err:
        logger.debug("OS error: {0}".format(err))
        logger.debug("Not able to find/list/sort the files")
    except IndexError as err:
        logger.debug("No log files present")
        totalIssues = totalIssues + 1
        return totalIssues

def removelicense(dirpath):
    try:
        path = dirpath
        # Check if path exits
        if os.path.exists(path):
            checkdirectory = scancodestatus.Scanstatus(path)
            exitcode = checkdirectory.scanLogResults()
            return exitcode
        else:
            return 1
    except OSError as err:
        logger.debug("OS error: {0}".format(err))
        logger.debug("Not able to find/list/sort the files")
    except IndexError as err:
        logger.debug("No log files present")
        totalIssues = totalIssues + 1
        return totalIssues

if __name__ == "__main__":
    statusexitcode = errorchecking(sys.argv[1])
    print(statusexitcode)
    sys.exit(statusexitcode)
