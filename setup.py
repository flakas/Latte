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
    'python_requires': '>=3.6',
    'install_requires': ['sqlalchemy==1.4.5'],
    'test_suite': 'tests',
    'tests_require': ['mock>=2.0.0', 'nose==1.3.7'],
    'packages': ['latte'],
    'entry_points': {'console_scripts': ['latte=latte.cli:main']},
    'version': '5.0-dev',
    'name': 'latte',
    'classifiers': (
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
    ),
}

setup(**config)
