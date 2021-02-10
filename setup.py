from setuptools import setup, find_packages

setup(
    name='alma-location-checker',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'argparse',
        'logzero',
        'pyyaml',
        'requests',
        'colorama',
        'blessings',
        'beautifultable'
    ],
    entry_points='''
        [console_scripts]
        alma-location-checker=alma_location_checker.checker:cli
    '''
)