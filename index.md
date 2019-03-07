---
title: fortune -- Display random quotes
layout: withTOC
---

## Introduction

*fortune* is yet another implementation of the Unix-style *fortune* program
that displays a random message from a database of quotations. Conceptually,
it's similar to the BSD fortune program originally written by [Ken Arnold][].
Unlike Arnold's program, this version is written in [Python][] and should
run anywhere there's a Python interpreter.

[Ken Arnold]: http://en.wikipedia.org/wiki/Ken_Arnold
[Python]: http://www.python.org/

## Usage

    fortune [OPTIONS] [fortune_File]

### Options

- `-h`, `--help`: show help and exit
- `-V`, `--version`: show version and exit.

If `fortune_file` is omitted, *fortune* looks at the `FORTUNE_FILE` environment
variable for the path. If that environment variable isn't set, *fortune*
aborts with an error.

### The fortune cookie database

Like Arnold's *fortune* program, this version uses a database of fortunes
(the *fortune cookie database*) generated from a text file. The text file
consists of possible multi-line quotes, separated by lines consisting of a
single "%" character. For example:

    Don't go around saying the world owes you a living.  The world owes you
    nothing.  It was here first.
            -- Mark Twain
    %
    Every normal man must be tempted at times to spit on his hands, hoist the
    black flag, and begin slitting throats.
            -- H.L. Mencken
    %
    Behind every argument is someone's ignorance.
            -- Louis Brandeis


### Displaying fortunes

Once you have a fortune file (and, as noted below, you're free to use
[mine][fortunes], you can generate a random fortune simply by running the 
*fortune* with the path to your text fortunes file:

    fortune /path/to/fortunes

Again, as noted above, if the fortune file path is omitted, *fortune* looks
for the path in the `FORTUNE_FILE` environment variable. If that
environment variable isn't set, *fortune* aborts with an error.

## Getting and installing *fortune*

**Note:** As of version 1.1.0, *fortune* only supports Python 3.6 or better.

### Installing via pip

Because *fortune* is available via [PyPI][], if you have [pip][] installed
on your system, installing *fortune* is as easy as running this command
(usually as `root` or the system administrator):

    pip install fortune

### Installing from source

You can also install *fortune* from source. Either download the source
(as a zip or tarball) from <http://github.com/bmc/fortune/downloads>, or
you can make a local read-only clone of the [Git repository][] using one of
the following commands:

    $ git clone git://github.com/bmc/fortune.git
    $ git clone http://github.com/bmc/fortune.git

If you don't have [git][], you can download the source distribution, as a
zipfile or a tarball, from the [Git repository][].

Once you have a local `fortune` source directory, change your working directory
to the source directory, and type:

    python setup.py install

To install it somewhere other than the default location (such as in your
home directory) type:

    python setup.py install --prefix=$HOME

## Differences from the BSD *fortune* program

This version of *fortune* does not provide some of the more advanced
capabilities of the original BSD program. For instance, it lacks:

* the ability to mark offensive and inoffensive fortunes
* the ability to separate long and short quotes
* the ability to print all fortunes matching a regular expression

It does, however, provide the most important function: The ability to
display a random quote from a set of quotes.

## My Fortune Cookie Database

I have a fortune cookie file that contains more than 2,800 fortunes I've
collected, from various sources, over the last 30 years. Feel free to
download it from [here][fortunes].

[fortunes]: http://github.com/bmc/fortunes

## Author

Brian M. Clapper, [bmc@clapper.org][]

## Copyright

Copyright &copy; 2008-2019 Brian M. Clapper

## License

BSD license. See accompanying [license][] file.

[license]: https://github.com/bmc/fortune/blob/master/LICENSE.md
[pip]: http://pip-installer.org/
[PyPI]: http://pypi.python.org/pypi
[Git repository]: http://github.com/bmc/fortune.git
[bmc@clapper.org]: mailto:bmc@clapper.org
[git]: http://git-scm.com/
