#!/usr/bin/env python

import sys
import logging
import click
import scancodestatus

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="'time': %(asctime)-15s, 'filename': %(name)s, 'level':  %(levelname)s ,'linenumber': %(lineno)d, 'message': %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
    stream=sys.stdout)

@click.command()
@click.option('--dirpath', type=click.Path(exists=True, dir_okay=True),\
              required=True, help='Directory path of scanresults.\
              For example --dirpath=/path')
@click.option('--jsonfilepath', type=click.Path(exists=True, dir_okay=True),\
              required=True, help='Directory path of scanresults.\
              For example --jsonfilepath=/jsonfilepath')
def checkstatus(dirpath, jsonfilepath):
    """  cli will check the json result file and create a summary report """
    checkdirectory = scancodestatus.Scanstatus(dirpath, jsonfilepath)
    exitcode = checkdirectory.scanLogResults()
    logger.debug("The exicode is exitcode")
    sys.exit(exitcode)


if __name__ == '__main__':
    checkstatus()
