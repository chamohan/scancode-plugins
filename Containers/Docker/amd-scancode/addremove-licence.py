#!/usr/bin/env python
import sys
import os
import addremovelicensess
import logger
import click

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout)
logger.setLevel(logging.DEBUG)

@click.group()
def addcli():
    pass

@addcli.command()
@click.command(context_settings={"ignore_unknown_options": True})
@click.argument('addlicense', type=click.Path(exists=True, dir_okay=False, readable=True))
@click.argument('licensemetadata', type=click.Path(exit=True, dir_okay=False, readable=True))
def addlicense(addlicense, licensemetadat):
    try:
        addthelicense = addremovelicensess.LicensesOps()
        install_license = addthelicense.add_scan_code_license(addlicense,licensemetadat)
        if install_license:
            return("success")
        else:
            return("failure")
    except OSError as err:
        logger.debug("OS error: {0}".format(err))
        logger.debug("Not able to find/list/sort the files")

@click.group()
def removecli():
    pass

@removecli.command()
@click.option('--removelicense', help("Licence key of the license to be removed"))
def removelicense(removelicense):

    try:
        deletethelicense =  addremovelicensess.LicensesOps()
        deletethelicense.remove_license(removelicense)
        if deletethelicense:
            return("success")
        else:
            return("failure")
    except OSError as err:
        logger.debug("OS error: {0}".format(err))
        logger.debug("Not able to find/list/sort the files")

@click.group()
def listcli():
    pass

@listcli.command()
@click.option('--listalllicenses', help(" list all the licences currently available"))
def listalllicense():

    try:
        deletethelicense =  addremovelicensess.LicensesOps()
        deletethelicense.remove_license(removelicense)
        if deletethelicense:
            return("suuccess")
        else:
            return("failure")
    except OSError as err:
        logger.debug("OS error: {0}".format(err))
        logger.debug("Not able to find/list/sort the files")


cli = click.CommandCollection(sources=[addcli, removecli, listcli])

if __name__ == '__main__':
    cli()
