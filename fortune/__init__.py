"""
# Introduction

`fortune` is a stripped-down implementation of the classic BSD Unix
`fortune` command. It combines the capabilities of the `strfile` command
(which produces the fortune index file) and the `fortune` command (which
displays a random fortune). It reads the traditional `fortune` program's
text file format.

# Usage

Usage:

    fortune [OPTIONS] /path/to/fortunes

    OPTIONS

    -h, --help      Show usage and exit.
    -u, --update    Update the index file.
    -q, --quiet     When updating the index file, do so quietly.
    -V, --version   Show version and exit.

If you omit the path, `fortune` looks at the `FORTUNE_FILE` environment
variable. If that environment variable isn't set, `fortune` aborts.

# Fortune Cookie File Format

A fortune cookie file is a text file full of quotes. The format is simple:
The file consists of paragraphs separated by lines containing a single '%'
character. For example::

    A little caution outflanks a large cavalry.
        -- Bismarck
    %
    A little retrospection shows that although many fine, useful software
    systems have been designed by committees and built as part of multipart
    projects, those software systems that have excited passionate fans are
    those that are the products of one or a few designing minds, great
    designers. Consider Unix, APL, Pascal, Modula, the Smalltalk interface,
    even Fortran; and contrast them with Cobol, PL/I, Algol, MVS/370, and
    MS-DOS.
        -- Fred Brooks, Jr.
    %
    A man is not old until regrets take the place of dreams.
        -- John Barrymore


# Generating a Random Fortune

Just run:

    fortune /path/to/fortunes

If your `FORTUNE_FILE` environment variable is set, you can run it as

    fortune

# Differences

This version of `fortune` does not provide some of the more advanced
capabilities of the original BSD program. For instance, it lacks:

- the ability to mark offensive and inoffensive fortunes
- the ability to separate long and short quotes
- the ability to print all fortunes matching a regular expression

It does, however, provide the most important function: The ability to display
a random quote from a set of quotes.
"""

__docformat__ = 'markdown'

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import random
import os
import sys
import codecs
import re

from optparse import OptionParser

sys.stdout.reconfigure(encoding='utf-8')

# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

__all__ = ['main', 'get_random_fortune']

# Info about the module
__version__   = '1.1.1'
__author__    = 'Brian M. Clapper'
__email__     = 'bmc@clapper.org'
__url__       = 'http://software.clapper.org/fortune/'
__copyright__ = '2008-2023 Brian M. Clapper'
__license__   = 'BSD-style license'

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

def _random_int(start, end):
    try:
        # Use SystemRandom, if it's available, since it's likely to have
        # more entropy.
        r = random.SystemRandom()
    except:
        r = random

    return r.randint(start, end)

def _read_fortunes(fortune_file):
    """ Yield fortunes as lists of lines """
    with codecs.open(fortune_file, mode='r', encoding='utf-8') as f:
        contents = f.read()

    lines = [line.rstrip() for line in contents.split('\n')]

    delim = re.compile(r'^%$')

    fortunes = []
    cur = []

    def save_if_nonempty(buf):
        fortune = '\n'.join(buf)
        if fortune.strip():
            fortunes.append(fortune)

    for line in lines:
        if delim.match(line):
            save_if_nonempty(cur)
            cur = []
            continue

        cur.append(line)

    if cur:
        save_if_nonempty(cur)

    return fortunes

def get_random_fortune(fortune_file):
    """
    Get a random fortune from the specified file. Barfs if the corresponding
    `.dat` file isn't present.

    :Parameters:
        fortune_file : str
            path to file containing fortune cookies

    :rtype:  str
    :return: the random fortune
    """
    fortunes = list(_read_fortunes(fortune_file))
    randomRecord = _random_int(0, len(fortunes) - 1)
    return fortunes[randomRecord]

def main():
    """
    Main program.
    """
    usage = 'Usage: %prog [OPTIONS] [fortune_file]'
    arg_parser = OptionParser(usage=usage)
    arg_parser.add_option('-V', '--version', action='store_true',
                          dest='show_version', help='Show version and exit.')
    arg_parser.epilog = 'If fortune_file is omitted, fortune looks at the ' \
                        'FORTUNE_FILE environment variable for the path.'

    options, args = arg_parser.parse_args(sys.argv)
    if len(args) == 2:
        fortune_file = args[1]

    else:
        try:
            fortune_file = os.environ['FORTUNE_FILE']
        except KeyError:
            print('Missing fortune file.', file=sys.stderr)
            print(usage, file=sys.stderr)
            sys.exit(1)

    try:
        if options.show_version:
            print('fortune, version {}'.format(__version__))
        else:
            print(get_random_fortune(fortune_file))
    except ValueError as msg:
        print(msg, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
