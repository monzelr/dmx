#!/usr/bin/env python

"""The setup script."""

import sys
import os

use_distutils = False

from setuptools import setup

# information by the package provider
from dmx import __version__ as version
from dmx import __author__ as author
from dmx import __email__ as author_email

# this is only necessary when not using setuptools/distribute
from sphinx.setup_command import BuildDoc

requirements = ["numpy>=1.13.0",
                "pyserial>=3.2"]

test_requirements = ["numpy>=1.13.0",
                     "pyserial>=3.2"]

python_requires = '>=3.6'
classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Programming Language :: Python :: 3.8',
]
description = "A python module to control one DMX Universe with a USB to RS-485 adapter."
install_requires = requirements
long_description = ""
keywords = 'DMX, RS-485'
name = 'dmx'
test_suite = 'tests'
url = 'https://gitlab.com/monzelr/dmx'
zip_safe = False

setup(
    author=author,
    author_email=author_email,
    python_requires=python_requires,
    classifiers=classifiers,
    description=description,
    install_requires=requirements,
    keywords=keywords,
    name=name,
    packages=['dmx', os.path.join('dmx',"documentation")],
    cmdclass={'build_sphinx': BuildDoc},
    test_suite=test_suite,
    tests_require=test_requirements,
    url=url,
    license="BSD 3-Clause License",
    version=version,
    zip_safe=zip_safe,
    command_options = {
                      'build_sphinx': {
                          'project': ('setup.py', name),
                          'version': ('setup.py', version),
                          'release': ('setup.py', version),
                          'source_dir': ('setup.py', 'documentation')}}
)

