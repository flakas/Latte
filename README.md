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

- `--time-all` to analyze all known log data
- `--time-seconds S` to analyze log data created in last S seconds
- `--time-days D` to analyze log data created in last D days
- `--time-weeks W` to analyze log data created in last W weeks
- `--time-months M` to analyze log data created in last M months

By default `lattestats` will analyze logs created in past 24 hours.

Grouping options:

- `-g title` (default) Groups entries by window name
- `-g instance` Groups entries by application name
- `-g class` Groups entries by application class

Ordering

- `-o desc` (default) Orders entries by descending duration
- `-o asc` Orders entries by ascending duration

Displaying:

- `--display-all` Display all found entries from the chosen time interval
- `--display-limit N` Display up to N top entries
- `--display-share PERCENTAGE` Display entries that have a share of the analyzed logs greater than SHARE, where SHARE is any number between 0 and 100
- `--display-time SECONDS` Displays entries that have the accumulated time greater than SECONDS

Dependencies
--------

This application requires:

- Python 3
- `xprop` to detect active window title for log tracking (`sudo apt-get install x11-utils`)

These dependencies are optional, but without them some functionality will not work:

- `libX11.so` and `libXss.so` to detect whether user is inactive (packages `libx11-dev` and `libxss-dev`, `sudo apt-get install libx11-dev libxss-dev`)

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

Contributors
------------

Special thanks to [contributors](https://github.com/flakas/Latte/graphs/contributors).
