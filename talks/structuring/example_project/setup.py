#!/usr/bin/env python

from setuptools import setup

from mypackage import __version__

with open('requirements.txt', 'rt') as f:
    requirements = [l.strip() for l in f.readlines()]

setup(

    name='Example project',
    description='Example Python project for PyTreat',
    url='https://git.fmrib.ox.ac.uk/fsl/pytreat-2018-practicals/',
    author='Paul McCarthy',
    author_email='pauldmccarthy@gmail.com',
    license='Apache License Version 2.0',

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
