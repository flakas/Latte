Latte - Linux Automatic Time Tracker
====================================

An attempt to build an automatic time tracker for Linux

Stable: [![Build Status](https://secure.travis-ci.org/flakas/Latte.png?branch=master)](http://travis-ci.org/flakas/Latte)
Development: [![Build Status](https://secure.travis-ci.org/flakas/Latte.png?branch=development)](http://travis-ci.org/flakas/Latte)

Installation
------------

Install from the latest source:

```
git clone git://github.com/flakas/Latte.git
cd Latte
python setup.py install
```

*OR*

Install from PIP (Python Package Index):

```
pip install latte
```

Configuration
-------------

Configuration files are saved in `~/.config/latte` folder.

Statistics files are stored in `~/.config/latte` folder (configurable)

Usage
-----

Run the binary script either in foreground:

`latte`

or in background:
`latte &`

To analyze log data you can use the built in analyzer:

- `lattestats` to analyze log data from past 24 hours
- `lattestats all`   Analyze all log data
- `lattestats X d` analyze log data from past X days, where X is any positive integer
- `lattestats X w` analyze log data from past X weeks, where X is any positive integer
- `lattestats X m` analyze log data from past X months, where X is any positive integer
- `lattestats X` analyze log data from past X seconds, where X is any positive integer

Dependencies
--------

This application requires:

- `xprop` to detect active window title for log tracking

Goal
----

To build an Automatic Time Tracker for Linux that:

- keeps track of windows where the user spends time
- is aware if the user is active or not
- collects information for personal analysis and statistics
- can classify activities based on user defined rules
- ignores unwanted and sensitive information

License
-------

MIT license, check LICENSE.txt
