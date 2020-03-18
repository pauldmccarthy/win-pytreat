#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages

# Import version number from
# the project package (see
# the section on versioning).
from mypackage import __version__

# Read in requirements from
# the requirements.txt file.
with open('requirements.txt', 'rt') as f:
    requirements = [l.strip() for l in f.readlines()]

# Generate a list of all of the
# packages that are in your project.
packages = find_packages()

setup(

    name='Example project',
    description='Example Python project for PyTreat',
    url='https://git.fmrib.ox.ac.uk/fsl/pytreat-practicals-2020/',
    author='Paul McCarthy',
    author_email='pauldmccarthy@gmail.com',
    license='Apache License Version 2.0',

    packages=packages,

    version=__version__,

    install_requires=requirements,

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
