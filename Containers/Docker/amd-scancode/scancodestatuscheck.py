#!/usr/bin/env python

import scancodestatus
import sys
import os

def errorchecking(dirpath):
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
