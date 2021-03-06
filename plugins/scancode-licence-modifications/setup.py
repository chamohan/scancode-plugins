# -*- encoding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


DESC = '''A ScanCode post-scan plugin to list the files Modified licence'''

setup(
    name='scancode-licence-modifications',
    version='1.0.0',
    license='Apache-2.0 with ScanCode acknowledgment',
    description=DESC,
    long_description=DESC,
    author='Chander',
    author_email='chamohan@amd.com',
    url='https://gitlab.rocm.amd.com/swca/amd-scancode-plugins.git',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
    keywords=[
        'scancode', 'plugin', 'post-scan'
    ],
    install_requires=[
        'scancode-toolkit',
    ],
    entry_points={
        'scancode_post_scan': [
            'licensemodifications = licence_modifications.licence_modifications:LicenceModifications',
        ],
    }
)
