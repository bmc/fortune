# $Id$

"""
Introduction
============

C{fortune} is a stripped-down implementation of the classic BSD Unix
C{fortune} command. It combines the capabilities of the C{strfile} command
(which produces the fortune index file) and the C{fortune} command (which
displays a random fortune). It reads the traditional C{fortune} program's text
file format.

Usage
=====

Usage::

    fortune [OPTIONS] /path/to/fortunes

    OPTIONS

    -u, --update    Update the index file

If you omit the path, C{fortune} looks at the C{FORTUNE_FILE} environment
variable. If that environment variable isn't set, C{fortune} aborts.

Fortune Cookie File Format
==========================

A fortune cookie file is a text file full of quotes. The format is simple:
The file consists of paragraphs separated by lines containing a single '%'
character. For example::

    %
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

For efficiency and speed, C{fortune} uses an index file to store the offsets
and lengths of every fortune in the text fortune file. So, before you can use
C{fortune} to read a random fortune, you have to generate the data file. With
the traditional BSD C{fortune} program, you used the I{strfile}(8) command
to generate the index. With I{this} fortune program, however, you simply
pass a special argument to the C{fortune} command::

    fortune -u /path/to/fortunes

That command will generate a binary C{/path/to/fortunes.dat} file that
contains the index. You should run C{fortune -u} whenever you change the text
fortune file.

Generating a Random Fortune
===========================

Once you have an index file, you can generate a random fortune simply by
running the C{fortune} utility with the path to your text fortunes file::

    fortune /path/to/fortunes

Differences
===========

This version of C{fortune} does not provide some of the more advanced
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

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

2. The end-user documentation included with the redistribution, if any,
   must include the following acknowlegement:

      This product includes software developed by Brian M. Clapper
      (bmc@clapper.org, U{http://www.clapper.org/bmc/}). That software is
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

__all__ = ['main', 'getRandomFortune', 'makeFortuneDataFile']

# ---------------------------------------------------------------------------
# Internal Constants
# ---------------------------------------------------------------------------

_PICKLE_PROTOCOL = 2

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

def getRandomFortune(fortuneFile):
    """
    Get a random fortune from the specified file. Barfs if the corresponding
    C{.dat} file isn't present.

    @type fortuneFile:  str
    @param fortuneFile: path to file containing fortune cookies

    @rtype:  str
    @return: the random fortune
    """
    fortuneIndexFile = fortuneFile + '.dat'
    if not os.path.exists(fortuneIndexFile):
        raise ValueError, 'Can\'t find file "%s"' % fortuneDat

    fortuneIndex = open(fortuneIndexFile)
    data = pickle.load(fortuneIndex)
    fortuneIndex.close()
    randomRecord = random.randint(0, len(data))
    (start, length) = data[randomRecord]

    f = open(fortuneFile)
    f.seek(start)
    fortuneCookie = f.read(length)
    f.close()
    return fortuneCookie

def _readFortunes(fortuneFile):
    """ Yield fortunes as lists of lines """
    result = []
    start = None
    pos = 0
    for line in fortuneFile:
        if line == "%\n":
            yield (start, pos - start, result)
            result = []
            start = None
        else:
            if not start:
                start = pos
            result.append(line)
        pos += len(line)

    if result:
        yield (start, pos - start, result)

def makeFortuneDataFile(fortuneFile, quiet=False):
    """
    Create or update the data file for a fortune cookie file.

    @type fortuneFile:  str
    @param fortuneFile: path to file containing fortune cookies

    @type quiet:  boolean
    @param quiet: If C{True}
    """
    fortuneIndexFile = fortuneFile + '.dat'
    if not quiet:
        print 'Updating "%s" from "%s"...' % (fortuneIndexFile, fortuneFile)

    data = []
    shortest = sys.maxint
    longest = 0
    for start, length, fortune in _readFortunes(open(fortuneFile)):
        data += [(start, length)]
        shortest = min(shortest, length)
        longest = max(longest, length)

    fortuneIndex = open(fortuneIndexFile, 'wb')
    pickle.dump(data, fortuneIndex, _PICKLE_PROTOCOL)
    fortuneIndex.close()

    if not quiet:
        print 'Processed %d fortunes.\nLongest: %d\nShortest %d' %\
              (len(data), longest, shortest)

def main():
    """
    Main program.
    """
    usage = 'Usage: %s [OPTIONS] fortuneFile' % os.path.basename(sys.argv[0])
    argParser = CommandLineParser(usage=usage)
    argParser.addOption('-u', '--update', action='store_true', dest='update',
                        help='Update the index file, instead of printing a '
                             'fortune.')
    argParser.addOption('-q', '--quiet', action='store_true', dest='quiet',
                        help="When updating the index file, don't emit " \
                             "messages.")

    argParser.epilogue = 'If <fortuneFile> is omitted, fortune looks at the ' \
                         'FORTUNE_FILE environment variable for the path.'

    options, args = argParser.parseArgs(sys.argv)
    if len(args) == 2:
        fortuneFile = args[1]
    else:
        try:
            fortuneFile = os.environ['FORTUNE_FILE']
        except KeyError:
            argParser.showUsage('Missing fortune file.')

    if options.update:
        makeFortuneDataFile(fortuneFile)
    else:
        sys.stdout.write(getRandomFortune(fortuneFile))

if __name__ == '__main__':
    main()
