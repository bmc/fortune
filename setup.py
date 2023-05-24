#!/usr/bin/env python

from setuptools import setup, find_packages

import sys
import os
import imp

# Load the long description

if sys.version_info[0:2] < (3, 6):
    columns = int(os.environ.get('COLUMNS', '80')) - 1
    msg = ('As of version 1.1.0, this fortune package no longer supports ' +
           'Python 2. Either upgrade to Python 3.6 or better, or use an ' +
           'older version of fortune (e.g., 1.0.1).')
    sys.stderr.write(msg + '\n')
    raise Exception(msg)

# Load the module.

here = os.path.dirname(os.path.abspath(sys.argv[0]))

def import_from_file(file, name):
    # See https://stackoverflow.com/a/19011259/53495
    import importlib.machinery
    import importlib.util
    loader = importlib.machinery.SourceFileLoader(name, file)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod

def load_info():
    import re

    # Look for identifiers beginning with "__" at the beginning of the line.

    result = {}
    mod = import_from_file(os.path.join(here, 'fortune', '__init__.py'),
                           'fortune')

    result['version'] = mod.__version__
    result['long_description'] = mod.__doc__
    result['license'] = mod.__license__
    result['email'] = mod.__email__
    result['url'] = mod.__url__
    result['author'] = mod.__author__
    result['copyright'] = mod.__copyright__

    return result

info = load_info()

# Now the setup stuff.

setup(name             = 'fortune',
      version          = info['version'],
      description      = 'Python version of old BSD Unix fortune program',
      long_description = info['long_description'],
      packages         = find_packages(),
      url              = info['url'],
      license          = info['license'],
      author           = info['author'],
      author_email     = info['email'],
      entry_points     = {'console_scripts' : ['fortune=fortune:main']},
      install_requires = ['grizzled-python>=1.0'],
      classifiers      = ['Intended Audience :: End Users/Desktop',
                          'Operating System :: OS Independent',
                          'Topic :: Games/Entertainment',
                          'License :: OSI Approved :: Apache Software License',
                          'Programming Language :: Python',
                          'Topic :: Text Processing :: Filters']
)
