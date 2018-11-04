from setuptools import setup, find_packages
import os
import re
from os import path
from io import open

VERSION = os.environ.get("PACKAGE_VERSION", None)
try:
    assert re.match("^([0-9]+\.)+[0-9]+$", VERSION)
except Exception as e:
    print('Invalid version string: "{}"'.format(VERSION))
    raise e

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-rest-atlas',

    version=VERSION,

    description='Wrapper around Django rest framework for better routing experience',

    long_description=long_description,

    long_description_content_type='text/markdown',

    url='https://github.com/Arnoldosmium/django-rest-atlas',

    author='Arnold Lin',

    # author_email=None,  # TODO: put the right email

    classifiers=[
        'Development Status :: 4 - Beta',

        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='django rest djangorestframework api',

    packages=find_packages(exclude=['contrib', 'docs', 'test']),

    install_requires=[
        'Django>=2.0',
        'djangorestframework>=3.8.2',
        'django-filter>=1.1.0',
    ],

    extras_require={
        'test': ['pytest', 'pyyaml'],
    },
)
