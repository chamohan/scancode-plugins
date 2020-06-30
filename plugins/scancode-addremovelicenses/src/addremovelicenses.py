import json
import logging
import os
import sys
import yaml
from shutil import copyfile
import click

@click.command()
@click.option('--licencefile', default=1, help='Enter the path of License file')
@click.option('--metadatafile', prompt='metadata file path', help = 'Enter the metadata file path')


from shutil import copyfile
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout)
logger.setLevel(logging.DEBUG)

class AddRemoveLicenses:
     

    def __init__(self, licensefile, licensemetadatafile, licensepolicyfile):

        self.licensefile = licensefile
        self.licensemetadatafile = licensemetadatafile
        self.licensepolicyfile = licensepolicyfile

    def extract_file_extension(self):
        licenseFilepath= ""
        metadataFilepath = ""
        licenseFileExtension = ""
        metadataFileExtension = ""
        fileExtensions = []
        licenseFilepath , licenseFileExtension = os.path.splitext(self.licensefile)
        metadataFilepath, metadataFileExtension = os.path.splitext(self.licensemetadatafile)
        fileExtensions.append(metadataFileExtension)
        fileExtensions.append(licenseFileExtension)
        return fileExtensions


    def is_licencefile_notempty(self):
        # Check if file exist and it is not empty
        return os.path.exists(self.licensefile) and os.stat(self.licensefile).st_size != 0

    def is_metadatafile_yaml(self, file_name):
        # check if the file exist and it is a valid yaml
        return os.path.exists(self.licensemetadatafile) and yaml.safe_load(self.licensemetadatafile)

    def is_licencepolicy_notempty(self):
        # Check if file exist and it is not empty
        return os.path.exists(self.licensepolicyfile) and os.stat(self.licensepolicyfile).st_size != 0


    def copy_files_scancode(self, licenseFileTargetLocation, MetadataFileTargetLocation ):
        # Copy the files to scancode license location
        # adding exception handling
        licenseFileTargetlocation = '/src/scancode/python3-virtualenv/lib/python3.6/site-packages/licensedcode/data/licenses'
        
        try:
            copyfile(self.licensefile, licenseFileTargetLocation)
        except IOError as e:
            print("Unable to copy file. %s" % e)
            exit(1)
        except:
            print("Unexpected error:", sys.exc_info())
            return(1)
        try:
            copyfile(self.licensemetadatafile, MetadataFileTargetLocation)
        except IOError as e:
            print("Unable to copy file. %s" % e)
            exit(1)
        except:
            print("Unexpected error:", sys.exc_info())
            return(1)

    def error_message(errortype):
        try:
            if errortype == 'licensefile':
                print ("Check the license file, it is either not present or empty ")
            if errortype == 'metadatafile':
                print( "Check the file, it is either not present of not correct yaml")
        except ValueError as err:
            logger.debug("Check the file")

    def update_licensepolicyfile(self):
        #Update the licensepolicyfile
        try:
            with open(self.licensepolicyfilepath) as f:
                data = json.load(f)
                for i in data['files']:
                    # update the licence policy file
                    if i['license_policy']['label'] == 'Approved License':
                        self.update_licencepolicyfile(self)


    def AddScanCodeLicense(self):
        checklicense = ""
        checkmetadata = ""

        try:
            is_correct_extension = []
            checklicense = self.is_licencefile_notempty(self)
            checkmetadata = self.is_metadatafile_yaml(self)
            if checklicense and checkmetadata:
                is_correct_extension = self.extract_file_extension(self)
                if is_correct_extension[0] == '.LICENSE' and is_correct_extension[1] == '.yml':
                    self.copy_files_scancode()
            else:
                logger.debug("Files were not present")

        except IOError as err:
            logger.debug("Could not copy files")
            logger.debug("")
        except KeyboardInterrupt as err:
            logger.debug('Caught KeyboardInterrupt')
        except IndexError as err:
            logger.debug("Index error")
        except OSError as err:
            logger.debug("OS error: {0}".format(err))
            logger.debug("Not able to find/list/sort the files")
        except ValueError as err:
            logger.debug("No JSON object could be decoded")
        except IndexError as err:
            logger.debug("No log files present")
            sys.exit("Run command Again")

        # make changes in
        try:
            with open(self.licensemetadatafile) as f:
                data = json.load(f)
                modifications_counter = 0
                for i in data['files']:
                    # Checking for licence policy in  file
                        if i['license_policy']['label'] == 'Approved License':
                            self.update_licencepolicyfile(self)

        except RuntimeError:
            logger.debug("RuntimeError: {0}".format(err))


            sys.exit(1)

