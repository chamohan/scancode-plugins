import sys
import os
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
@click.option('--dirpath', required=True, help='Directory path of scanresults. For example --dirpath=/path')
def checkstatus(dirpath):

    if os.path.exists(dirpath):
        checkdirectory = scancodestatus.Scanstatus(dirpath)
        exitcode = checkdirectory.scanLogResults()
        sys.exit(exitcode)
    else:
        logger.debug("No log files present")
        print("No log files")
        sys.exit(1)


if __name__ == '__main__':
    checkstatus()
