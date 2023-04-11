#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This setup.py is inspired by https://github.com/navdeep-G/setup.py licensed under MIT

import io
import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'sen2cli'
DESCRIPTION = 'Sen2Cube.at commandline interface.'
URL = 'https://github.com/Sen2Cube-at/sen2cli'
EMAIL = 'me@example.com'
AUTHOR = 'Sen2Cube.at'
REQUIRES_PYTHON = '>=3.8.0'
VERSION = None #will be filled from __version__.py '0.1.0'

REQUIRED = [
  'Click~=8.0.1',
  'jsonapi_client~=0.9.7',
  'requests_oauthlib~=1.3.0',
  'oauthlib~=3.0.1'
]

# What packages are optional?
EXTRAS = {
  # 'fancy feature': ['django'],
}

SETUP_REQUIRED = [
  'pylint~=2.6.0',
  'flake8~=3.8.4'
]

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION



setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['sen2cli'],
    entry_points={
      'console_scripts': 'sen2cli=sen2cli:cli'
    },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    setup_requires=SETUP_REQUIRED,
    include_package_data=True,
    license='GPL',
    classifiers=[
      # Trove classifiers
      # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
      'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.8',
      'Development Status :: 3 - Alpha',
      'Environment :: Console',
      'Intended Audience :: Developers',
      'Intended Audience :: End Users/Desktop',
      'Intended Audience :: Science/Research',
      'Intended Audience :: System Administrators',
      'Topic :: Scientific/Engineering :: GIS',
      'Topic :: Utilities'
    ],
)
