Latte - Linux Automatic Time Tracker
====================================

A proof of concept automated time tracker, intended for Ubuntu Linux.

Stable: [![Build Status](https://secure.travis-ci.org/flakas/Latte.png?branch=master)](http://travis-ci.org/flakas/Latte)
Development: [![Build Status](https://secure.travis-ci.org/flakas/Latte.png?branch=development)](http://travis-ci.org/flakas/Latte)


Installing and upgrading
-----------------------

Install (upgrade) from the latest source:

```
git clone git://github.com/flakas/Latte.git
cd Latte
python setup.py install
```

*OR*

Install via PIP (Python Package Index):

```
pip install latte
```

Upgrade via PIP:

```
pip install latte --upgrade
```

Configuration
-------------

Configuration files are saved in `~/.config/latte` folder.

Statistics files are stored in `~/.config/latte` folder (configurable)

Usage
-----

Run the binary script either in foreground:

`latte`

or in the background:
`latte --silent &`

To analyze log data you can use the built in analyzer:

Syntax: `lattestats [OPTIONS]`

- `lattestats` to analyze log data from past 24 hours by window title
- `lattestats -h` to print an help message

Time options:
- `-t all`  to analyze log data from past 24 hours
- `-t X d`  analyze log data from past X days, where X is any positive integer
- `-t X w`  analyze log data from past X weeks, where X is any positive integer
- `-t X m`  analyze log data from past X months, where X is any positive integer
- `-t X` 	analyze log data from past X seconds, where X is any positive integer

Grouping options:

- `-g title`    (default) Groups entries by window name
- `-g instance` Groups entries by application name
- `-g class`    Groups entries by application class

Ordering

- `-o desc`    (default) Orders entries by descending duration
- `-o asc` 		Orders entries by ascending duration

Displaying:

- `-d all`    (default) Displays all entries for the time interval chosen
- `-d X`      Displays up to X entries, where X is any positive integer
- `-d X s`    Displays only entries that have a share of the analyzed logs greater than X, where X is any number between 0 and 100
- `-d X t`    Displays only entries that have a spent time greater than X, where X is the time in seconds

Dependencies
--------

This application requires:

- `xprop` to detect active window title for log tracking

These dependencies are optional, but without them some functionality will not work:

- `libX11.so` and `libXss.so` to detect whether user is inactive (packages `libx11-dev` and `libxss-dev`)

Goal
----

To build an Automatic Time Tracker for Linux that:

- keeps track of windows where the user spends time
- is aware if the user is active or not
- collects information for personal analysis and statistics
- can classify activities based on user defined rules
- ignores unwanted and sensitive information

All without any human intervention (except for the initial set up).

License
-------

MIT license, check LICENSE.txt
