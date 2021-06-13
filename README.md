Latte - Automatic Time Tracker for Linux
====================================

Stable: [![Build Status](https://secure.travis-ci.org/flakas/Latte.png?branch=master)](http://travis-ci.org/flakas/Latte)
Development: [![Build Status](https://secure.travis-ci.org/flakas/Latte.png?branch=development)](http://travis-ci.org/flakas/Latte)

Developing
----------

```
git clone git://github.com/flakas/Latte.git
cd Latte
python setup.py clean develop
```

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

`latte run`

or in the background:
`latte run --silent &`

### Stats

To analyze log data you can use the built in analyzer:

Syntax: `latte stats {windows,apps,tags} [OPTIONS]`

- `latte stats windows` to analyze log data from past 24 hours by window title
- `latte stats -h` to print an help message

Time options:

- `--time-all` to analyze all known log data
- `--time-seconds S` to analyze log data created in last S seconds
- `--time-days D` to analyze log data created in last D days
- `--time-weeks W` to analyze log data created in last W weeks
- `--time-months M` to analyze log data created in last M months

By default `latte stats` will analyze logs created in past 24 hours.

Displaying:

- `--display-all` Display all found entries from the chosen time interval
- `--display-limit N` Display up to N top entries
- `--display-time SECONDS` Displays entries that have the accumulated time greater than SECONDS

Tags:

- `--tags` show stats for the comma-separated tag names

### Tagging

Latte can tag logs with custom tags for easier grouping and analytics.

Add tags:
- `latte tags add <name> [--window-title=<regex>] [--window-class=<regex>] [--window-instance=<regex>] [--tag=<regex>]`
- Filtering is based on Python's regular expressions using case-insensitive values;
- Window title, class, instance and tag filters are optional. All specified filters must match for the tag to be assigned.

Delete tags:
- `latte tags delete <name>`

Show all tags:
- `latte tags show`

Forcibly retag all logs:
- `latte tags retag`

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
