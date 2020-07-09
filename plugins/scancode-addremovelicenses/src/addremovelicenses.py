import logging
import os
import sys
import logging
from shutil import copyfile
import yaml

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="'time': %(asctime)-15s, 'filename': %(name)s, 'level':  %(levelname)s ,'linenumber': %(lineno)d, 'message': %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
    stream=sys.stdout)

class LicensesOps:

    def __init__(self, licensefile, licensemetadatafile, \
                 license_file_targetlocation, metadata_file_targetlocation, license_key):

        self.licensefile = licensefile
        self.license_key = license_key
        self.licensemetadatafile = licensemetadatafile
        self.license_file_targetlocation = license_file_targetlocation
        self.metadata_file_targetlocation = metadata_file_targetlocation

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

    def copy_files_scancode(self):
        # Copy the files to scancode license location
        # adding exception handling
        try:
            copyfile(self.licensefile, self.license_file_targetlocation)
            copyfile(self.licensemetadatafile, self.metadata_file_targetlocation)
            return "success"
        except ValueError:
            print("Unexpected error:", sys.exc_info())
            return "copy failed"

    def error_message(self, errortype):
        try:
            if errortype == 'licensefile':
                print("Check the license file, it is either not present or empty")
            if errortype == 'metadatafile':
                print("Check the file, it is either not present of not correct yaml")
        except ValueError as err:
            logger.debug("Check the file, %s" % err)

    def add_scan_code_license(self):
        try:
            is_correct_extension = []
            checklicense = self.is_licencefile_notempty()
            checkmetadata = self.is_metadatafile_yaml()
            if checklicense and checkmetadata:
                is_correct_extension = self.extract_file_extension()
                if is_correct_extension[0] == '.LICENSE' and is_correct_extension[1] == '.yml':
                    copyfiles = self.copy_files_scancode()
                logger.debug("License installation was , %s", copyfiles)
                return copyfiles
            else:
                logger.debug('Files were not present')
                sys.exit(1)
        except IOError as err:
            logger.debug("Could not copy files, %s"% err)
        except KeyboardInterrupt as err:
            logger.debug("Caught KeyboardInterrupt, %s" % err)
            sys.exit(1)
        except IndexError as err:
            logger.debug("Index error, %s" % err)
            logger.debug("Not able to find/list/sort the files")
            sys.exit("Run command Again")


    def list_licences(self, extension):
        try:
            return (f for f in os.listdir(self.license_file_targetlocation) \
                    if f.endswith('.' + extension))
        except OSError as err:
            logger.debug("OS error: {0}".format(err))
            logger.debug("Not able to find the licenses")
            sys.exit(1)

    def remove_licenses(self):

        try:
            os.chdir(self.license_file_targetlocation)
            # remove  .LICENSE FILE
            if (os.path.isfile("self.license_key" + ".LICENSE")):
                os.remove("self.license_key"+".LICENSE")
            # remove metadata file
            os.chdir(self.metadata_file_targetlocation)
            if (os.path.isfile("self.license_key"+".yml")):
                os.remove("self.license"+".yml")
        except OSError as err:
            logger.debug("OS error: {0}".format(err))
            logger.debug("Not able to delete the  files")
            sys.exit(1)
