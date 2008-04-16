#!/usr/bin/env python
#
# EasyInstall setup script for paragrep
#
# $Id$
# ---------------------------------------------------------------------------

import ez_setup
ez_setup.use_setuptools(download_delay=2)
from setuptools import setup, find_packages

import sys
import os

# Now the setup stuff.

setup (name             = 'fortune',
       version          = '0.1',
       description      = 'Python version of old BSD Unix fortune program',
       packages         = find_packages(),
       url              = 'http://www.clapper.org/software/python/fortune',
       license          = 'BSD license',
       author           = 'Brian M. Clapper',
       author_email     = 'bmc@clapper.org',
       entry_points     = {'console_scripts' : ['fortune=fortune:main']},
       install_requires = ['grizzled>=0.2'],
       classifiers = [
        'Intended Audience :: End Users/Desktop',
        'Operating SYstem :: OS Independent',
        'Topic :: Games/Entertainment',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Text Processing :: Filters'
        ]
)
