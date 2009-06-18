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

def load_info():
    import re

    # Look for identifiers beginning with "__" at the beginning of the line.

    result = {}
    pattern = re.compile(r'^(__\w+__)\s*=\s*[\'"]([^\'"]*)[\'"]')
    here = os.path.dirname(os.path.abspath(sys.argv[0]))
    for line in open(os.path.join(here, 'fortune', '__init__.py'), 'r'):
        match = pattern.match(line)
        if match:
            result[match.group(1)] = match.group(2)

    sys.path = [here] + sys.path
    mf = os.path.join(here, 'fortune', '__init__.py')
    try:
        m = imp.load_module('fortune', open(mf), mf,
                            ('__init__.py', 'r', imp.PY_SOURCE))
        result['long_description'] = m.__doc__
    except:
        result['long_description'] = DESCRIPTION
    return result

info = load_info()

# Now the setup stuff.

setup(name             = 'fortune',
      version          = info['__version__'],
      description      = 'Python version of old BSD Unix fortune program',
      long_description = info['long_description'],
      packages         = find_packages(),
      url              = info['__url__'],
      license          = info['__license__'],
      author           = info['__author__'],
      author_email     = info['__email__'],
      entry_points     = {'console_scripts' : ['fortune=fortune:main']},
      install_requires = ['grizzled>=0.6'],
      classifiers      = ['Intended Audience :: End Users/Desktop',
                          'Operating System :: OS Independent',
                          'Topic :: Games/Entertainment',
                          'License :: OSI Approved :: BSD License',
                          'Programming Language :: Python',
                          'Topic :: Text Processing :: Filters']
)
