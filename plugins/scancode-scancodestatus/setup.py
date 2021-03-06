# -*- encoding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


DESC = '''A lib to scan the json file and return the status'''

setup(
    name='scancode-scancodestatus',
    version='1.0.0',
    license='Apache-2.0 with ScanCode acknowledgment',
    description=DESC,
    long_description=DESC,
    author='Chander',
    author_email='chamohan@amd.com',
    url='https://gitlab.rocm.amd.com/swca/amd-scancode-plugins',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
    install_requires=[
        'datetime',
        'pprint',
    ],

)
