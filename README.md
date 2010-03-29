fortune: Display random quotes
==============================

## Introduction

`fortune` is yet another implementation of the Unix-style `fortune` program
that displays a random message from a database of quotations. Conceptually,
it's similar to the BSD fortune program originally written by [Ken Arnold][].
Unlike Arnold's program, this version is written in [Python][] and should
run anywhere there's a Python interpreter.

[Ken Arnold][]: http://en.wikipedia.org/wiki/Ken_Arnold
[Python][]: http://www.python.org/

## The fortune cookie database

Like Arnold's `fortune` program, this version uses a database of fortunes
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

Before `fortune` can use the fortune cookie database, you must generate an
index. Unlike Arnold's version of `fortune`, you use the `fortune` program
itself to generate the database, instead of a separate `strfile` program.
For example, if your fortune cookies are in a file called `fortunes`, you
generate the database with this command:

    $ fortune -u fortunes

You should run `fortune -u` whenever you change your fortune cookie file.

## Using `fortune`

Once you have your fortune cookie database and index in place, you

To install "fortune" in the default location, type:

	python setup.py install

To install it somewhere else (e.g., your home directory) type:

	python setup.py install --prefix=$HOME

You can also install "fortune" with easy_install:

	easy_install fortune
