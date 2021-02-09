#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='alma-location-checker',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'logzero',
        'pyyaml'
    ],
    entry_points='''
        [console_scripts]
        alma-location-checker=alma_location_checker.checker:cli
    '''
)