try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Automatic rule based Linux Time Tracker',
    'author': 'Tautvidas Sipavicius',
    'url': 'https://github.com/flakas/Latte',
    'install_requires': [],
    'packages': ['latte', 'latte.Categories', 'latte.Projects'],
    'scripts': ['bin/latte'],
    'version': '1.0',
    'name': 'latte'
}

setup(**config)
