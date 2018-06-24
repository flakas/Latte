try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

config = {
    'description': 'Automatic rule based Linux Time Tracker',
    'long_description': long_description,
    'long_description_content_type': 'text/markdown',
    'author': 'Tautvidas Sipavicius',
    'author_email': 'flakas@tautvidas.com',
    'url': 'https://github.com/flakas/Latte',
    'install_requires': ['sqlalchemy'],
    'packages': ['latte', 'latte.analyzer', 'latte.os'],
    'scripts': ['bin/latte', 'bin/lattestats'],
    'version': '4.0',
    'name': 'latte',
    'classifiers': (
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
    ),
}

setup(**config)
