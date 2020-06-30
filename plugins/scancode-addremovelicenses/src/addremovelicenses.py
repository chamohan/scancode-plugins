import logging
import os
import sys
from shutil import copyfile
import yaml

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout)
logger.setLevel(logging.DEBUG)

class AddRemoveLicenses:

    def __init__(self, licensefile, licensemetadatafile, licensepolicyfile):

        self.licensefile = licensefile
        self.licensemetadatafile = licensemetadatafile
        self.licensepolicyfile = licensepolicyfile

    def extract_file_extension(self):
        license_file_path = ""
        metadata_file_path = ""
        license_file_extension = ""
        metadata_file_extension = ""
        file_extensions = []
        license_file_path, license_file_extension = os.path.splitext(self.licensefile)
        metadata_file_path, metadata_file_extension = os.path.splitext(self.licensemetadatafile)
        file_extensions.append(metadata_file_extension)
        file_extensions.append(license_file_extension)
        return file_extensions


    def is_licencefile_notempty(self):
        # Check if file exist and it is not empty
        return os.path.exists(self.licensefile) and os.stat(self.licensefile).st_size != 0

    def is_metadatafile_yaml(self):
        # check if the file exist and it is a valid yaml
        return os.path.exists(self.licensemetadatafile) and yaml.safe_load(self.licensemetadatafile)

    def is_licencepolicy_notempty(self):
        # Check if file exist and it is not empty
        return os.path.exists(self.licensepolicyfile) and \
            os.stat(self.licensepolicyfile).st_size != 0


    def copy_files_scancode(self, license_file_targetlocation, metadata_file_targetlocation):
        # Copy the files to scancode license location
        # adding exception handling
        license_file_targetlocation = '/src/scancode/python3-virtualenv/lib/python3.6/site-packages/licensedcode/data/licenses'
        try:
            copyfile(self.licensefile, license_file_targetlocation)
        except IOError as err:
            print("Unable to copy file. %s" % err)
            sys.exit(1)
        except:
            print("Unexpected error:", sys.exc_info())
            sys.exit(1)
        try:
            copyfile(self.licensemetadatafile, metadata_file_targetlocation)
        except IOError as err:
            print("Unable to copy file. %s" % err)
            sys.exit(1)
        except:
            print("Unexpected error:", sys.exc_info())
            sys.exit(1)

    def error_message(self, errortype):
        try:
            if errortype == 'licensefile':
                print("Check the license file, it is either not present or empty")
            if errortype == 'metadatafile':
                print("Check the file, it is either not present of not correct yaml")
        except ValueError as err:
            logger.debug("Check the file, %s" % err)

    def add_scan_code_license(self):
        checklicense = ""
        checkmetadata = ""

        try:
            is_correct_extension = []
            checklicense = self.is_licencefile_notempty()
            checkmetadata = self.is_metadatafile_yaml()
            if checklicense and checkmetadata:
                is_correct_extension = self.extract_file_extension()
                if is_correct_extension[0] == '.LICENSE' and is_correct_extension[1] == '.yml':
                    copy_files_scancode(self)
            else:
                logger.debug("Files were not present")

        except IOError as err:
            logger.debug("Could not copy files, %s"% err)
        except KeyboardInterrupt as err:
            logger.debug("Caught KeyboardInterrupt, %s" % err)
        except IndexError as err:
            logger.debug("Index error, %s" % err)
        except OSError as err:
            logger.debug("OS error: {0}".format(err))
            logger.debug("Not able to find/list/sort the files")
        except ValueError as err:
            logger.debug("No JSON object could be decoded")
        except IndexError as err:
            logger.debug("No log files present")
            sys.exit("Run command Again")
