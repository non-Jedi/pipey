'''A setuptools-based setup module for pipey'''

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get long description from README
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description= f.read()

setup(
    name = 'pipey'
    version = '0.0.0.dev0',
    url = 'https://github.com/non-Jedi/pipey',
    author = 'Adam Beckmeyer',
    license = 'LGPLv3',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Engineers',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3',],
    keywords = 'pressure pipe piping',
    packages = ['pipey'],
    package_dir = {'pipey': 'pipey'},
    package_data = {'pipey' : ['data/*.csv']},
    install_requires= ['pint',],
    entry_points= {
        'console_scripts': [
          'pipey = pipey.pipey_cli:main'
        ]
    },
    )
