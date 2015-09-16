try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Automatic rule based Linux Time Tracker',
    'author': 'Tautvidas Sipavicius',
    'author_email': 'flakas@tautvidas.com',
    'url': 'https://github.com/flakas/Latte',
    'install_requires': ['sqlalchemy','pysqlite'],
    'packages': ['latte'],
    'scripts': ['bin/latte', 'bin/lattestats'],
    'version': '3.0',
    'name': 'latte'
}

setup(**config)
