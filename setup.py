try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Automatic rule based Linux Time Tracker',
    'author': 'Tautvidas Sipavicius',
    'author_email': 'flakas@tautvidas.com',
    'url': 'https://github.com/flakas/Latte',
    'install_requires': ['sqlalchemy'],
    'packages': ['latte', 'latte.os'],
    'scripts': ['bin/latte', 'bin/lattestats'],
    'version': '4.0',
    'name': 'latte'
}

setup(**config)
