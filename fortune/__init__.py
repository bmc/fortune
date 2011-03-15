# $Id$

"""
Introduction
============

``fortune`` is a stripped-down implementation of the classic BSD Unix
``fortune`` command. It combines the capabilities of the ``strfile`` command
(which produces the fortune index file) and the ``fortune`` command (which
displays a random fortune). It reads the traditional ``fortune`` program's
text file format.

Usage
=====

Usage::

    fortune [OPTIONS] /path/to/fortunes

    OPTIONS

    -h, --help      Show usage and exit.
    -u, --update    Update the index file.
    -q, --quiet     When updating the index file, do so quietly.
    -V, --version   Show version and exit.

If you omit the path, ``fortune`` looks at the ``FORTUNE_FILE`` environment
variable. If that environment variable isn't set, ``fortune`` aborts.

Fortune Cookie File Format
==========================

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


The Index File
==============

For efficiency and speed, ``fortune`` uses an index file to store the offsets
and lengths of every fortune in the text fortune file. So, before you can use
``fortune`` to read a random fortune, you have to generate the data file. With
the traditional BSD ``fortune`` program, you used the I{strfile}(8) command
to generate the index. With I{this} fortune program, however, you simply
pass a special argument to the ``fortune`` command::

    fortune -u /path/to/fortunes

That command will generate a binary ``/path/to/fortunes.dat`` file that
contains the index. You should run ``fortune -u`` whenever you change the text
fortune file.

Generating a Random Fortune
===========================

Once you have an index file, you can generate a random fortune simply by
running the ``fortune`` utility with the path to your text fortunes file::

    fortune /path/to/fortunes

Differences
===========

This version of ``fortune`` does not provide some of the more advanced
capabilities of the original BSD program. For instance, it lacks:

- the ability to mark offensive and inoffensive fortunes
- the ability to separate long and short quotes
- the ability to print all fortunes matching a regular expression

It does, however, provide the most important function: The ability to display
a random quote from a set of quotes.

License and Copyright Info
==========================

Copyright (c) 2008 Brian M. Clapper

This is free software, released under the following BSD-like license:

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

 - Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

 - The end-user documentation included with the redistribution, if any,
   must include the following acknowlegement:

   This product includes software developed by Brian M. Clapper
   (bmc@clapper.org, http://www.clapper.org/bmc/). That software is
   copyright (c) 2008 Brian M. Clapper.

   Alternately, this acknowlegement may appear in the software itself, if
   and wherever such third-party acknowlegements normally appear.

THIS SOFTWARE IS PROVIDED B{AS IS} AND ANY EXPRESSED OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BRIAN M.
CLAPPER BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import random
import os
import sys
import cPickle as pickle

from grizzled.cmdline import CommandLineParser

# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

__all__ = ['main', 'get_random_fortune', 'make_fortune_data_file']

# Info about the module
__version__   = '1.0'
__author__    = 'Brian M. Clapper'
__email__     = 'bmc@clapper.org'
__url__       = 'http://software.clapper.org/fortune/'
__copyright__ = '2008-2011 Brian M. Clapper'
__license__   = 'BSD-style license'

# ---------------------------------------------------------------------------
# Internal Constants
# ---------------------------------------------------------------------------

_PICKLE_PROTOCOL = 2

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

def random_int(start, end):
    try:
        # Use SystemRandom, if it's available, since it's likely to have
        # more entropy.
        r = random.SystemRandom()
    except:
        r = random

    return r.randint(start, end)

def get_random_fortune(fortune_file):
    """
    Get a random fortune from the specified file. Barfs if the corresponding
    ``.dat`` file isn't present.

    :Parameters:
        fortune_file : str
            path to file containing fortune cookies

    :rtype:  str
    :return: the random fortune
    """
    fortune_index_file = fortune_file + '.dat'
    if not os.path.exists(fortune_index_file):
        raise ValueError, 'Can\'t find file "%s"' % fortune_index_file

    fortuneIndex = open(fortune_index_file)
    data = pickle.load(fortuneIndex)
    fortuneIndex.close()
    randomRecord = random_int(0, len(data) - 1)
    (start, length) = data[randomRecord]

    f = open(fortune_file, 'rU')
    f.seek(start)
    fortuneCookie = f.read(length)
    f.close()
    return fortuneCookie

def _read_fortunes(fortune_file):
    """ Yield fortunes as lists of lines """
    result = []
    start = None
    pos = 0
    for line in fortune_file:
        if line == "%\n":
            if pos == 0: # "%" at top of file. Skip it.
                continue
            yield (start, pos - start, result)
            result = []
            start = None
        else:
            if start == None:
                start = pos
            result.append(line)
        pos += len(line)

    if result:
        yield (start, pos - start, result)

def make_fortune_data_file(fortune_file, quiet=False):
    """
    Create or update the data file for a fortune cookie file.

    :Parameters:
        fortune_file : str
            path to file containing fortune cookies
        quiet : bool
            If ``True``, don't display progress messages
    """
    fortune_index_file = fortune_file + '.dat'
    if not quiet:
        print 'Updating "%s" from "%s"...' % (fortune_index_file, fortune_file)

    data = []
    shortest = sys.maxint
    longest = 0
    for start, length, fortune in _read_fortunes(open(fortune_file, 'rU')):
        data += [(start, length)]
        shortest = min(shortest, length)
        longest = max(longest, length)

    fortuneIndex = open(fortune_index_file, 'wb')
    pickle.dump(data, fortuneIndex, _PICKLE_PROTOCOL)
    fortuneIndex.close()

    if not quiet:
        print 'Processed %d fortunes.\nLongest: %d\nShortest %d' %\
              (len(data), longest, shortest)

def main():
    """
    Main program.
    """
    usage = 'Usage: %s [OPTIONS] fortune_file' % os.path.basename(sys.argv[0])
    arg_parser = CommandLineParser(usage=usage)
    arg_parser.add_option('-q', '--quiet', action='store_true', dest='quiet',
                          help="When updating the index file, don't emit " \
                               "messages.")
    arg_parser.add_option('-u', '--update', action='store_true', dest='update',
                          help='Update the index file, instead of printing a '
                               'fortune.')
    arg_parser.add_option('-V', '--version', action='store_true',
                          dest='show_version', help='Show version and exit.')

    arg_parser.epilogue = 'If <fortune_file> is omitted, fortune looks at the ' \
                          'FORTUNE_FILE environment variable for the path.'

    options, args = arg_parser.parse_args(sys.argv)
    if len(args) == 2:
        fortune_file = args[1]

    else:
        try:
            fortune_file = os.environ['FORTUNE_FILE']
        except KeyError:
            arg_parser.show_usage('Missing fortune file.')

    try:
        if options.show_version:
            print 'fortune, version %s' % __version__
        elif options.update:
            make_fortune_data_file(fortune_file)
        else:
            sys.stdout.write(get_random_fortune(fortune_file))
    except ValueError, msg:
        print >> sys.stderr, msg
        sys.exit(1)

if __name__ == '__main__':
    main()
