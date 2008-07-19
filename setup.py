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
import imp

# Load the long description

here = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path = [here] + sys.path
mf = os.path.join(here, 'fortune', '__init__.py')
m = imp.load_module('fortune', open(mf), mf,
                    ('__init__.py', 'r', imp.PY_SOURCE))
long_description = m.__doc__


# Now the setup stuff.

setup (name             = 'fortune',
       version          = '0.5',
       description      = 'Python version of old BSD Unix fortune program',
       long_description = long_description,
       packages         = find_packages(),
       url              = 'http://www.clapper.org/software/python/fortune',
       license          = 'BSD license',
       author           = 'Brian M. Clapper',
       author_email     = 'bmc@clapper.org',
       entry_points     = {'console_scripts' : ['fortune=fortune:main']},
       install_requires = ['grizzled>=0.6'],
       classifiers = [
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'Topic :: Games/Entertainment',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Text Processing :: Filters'
        ]
)
