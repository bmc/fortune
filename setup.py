#!/usr/bin/env python
#
# EasyInstall setup script for paragrep
#
# $Id$
# ---------------------------------------------------------------------------

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
        result['long_description'] = 'Fortune program'
    return result

info = load_info()

# Now the setup stuff.

NAME = 'fortune'
DOWNLOAD_URL = ('http://pypi.python.org/packages/source/f/%s/%s-%s.tar.gz' %
                (NAME, NAME, info['__version__']))

setup(name             = NAME,
      download_url     = DOWNLOAD_URL,
      version          = info['__version__'],
      description      = 'Python version of old BSD Unix fortune program',
      long_description = info['long_description'],
      packages         = find_packages(),
      url              = info['__url__'],
      license          = info['__license__'],
      author           = info['__author__'],
      author_email     = info['__email__'],
      entry_points     = {'console_scripts' : ['fortune=fortune:main']},
      install_requires = ['grizzled-python>=1.0'],
      classifiers      = ['Intended Audience :: End Users/Desktop',
                          'Operating System :: OS Independent',
                          'Topic :: Games/Entertainment',
                          'License :: OSI Approved :: BSD License',
                          'Programming Language :: Python',
                          'Topic :: Text Processing :: Filters']
)
