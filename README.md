Latte - Linux Automatic Time Tracker
====================================

An attempt to build an automatic time tracker for Linux

Stable: [![Build Status](https://secure.travis-ci.org/flakas/Latte.png?branch=master)](http://travis-ci.org/flakas/Latte)
Development: [![Build Status](https://secure.travis-ci.org/flakas/Latte.png?branch=development)](http://travis-ci.org/flakas/Latte)

Installation
------------

Use these installation commands to install `Latte`:

```
git clone git://github.com/flakas/Latte.git
cd Latte
python setup.py install
```

OR

You can install it from Python Package Index (PIP):
```
pip install latte
```

Configuration
-------------

Configuration scripts are saved in `~/.latte` folder.

- `categories.py` should contain user defined classes for categories (see example configuration in `doc/config/categories.py`)
- `projects.py` should contain user defined classes for projects (see example configuration in `doc/config/projects.py`)

Statistics files are stored in `~/.latte/stats` folder

Usage
-----

Run the binary script either in foreground:

`latte`

or in background:
`latte &`

To analyze log data you can use the built in analyzer:

- `latte analyze` to analyze all log data
- `latte analyze X d` analyze log data from past X days, where X is any positive integer
- `latte analyze X w` analyze log data from past X weeks, where X is any positive integer
- `latte analyze X m` analyze log data from past X months, where X is any positive integer
- `latte analyze X` analyze log data from past X seconds, where X is any positive integer

Goal
----

To build an Automatic Time Tracker for Linux that:

- keeps track of windows where the user spends time
- is aware if the user is active or not
- collects information for analysis and statistics
- Can assign time and activities to specific projects and/or categories based on
  specific rules defined by user (Regular Expressions possibly)

Tasks
-----

Tasks ordered in random manner:

- Functionality to check if the user is active (mouse and/or keyboard activity tracking)
- User defined application configuration (paths, timer durations)
- Add comments to the code
- Add configuration examples
- Write documentation
- Add a wiki
- Better log data processing functionality
- Distribution through PIP
- 'Do not track' functionality
- Better analytics log filtering

License
-------

MIT license, check LICENSE.txt
