try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Automatic rule based Linux Time Tracker',
    'author': 'Tautvidas Sipavicius',
    'url': 'https://github.com/flakas/Latte',
    'install_requires': ['nose'],
    'packages': ['latte'],
    'name': 'Latte'
}

setup(**config)
