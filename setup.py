#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from codecs import open

from setuptools import find_packages, setup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def read(*paths):
    """Build a file path from *paths and return the contents."""
    with open(os.path.join(*paths), 'r', 'utf-8') as f:
        return f.read()


extras_require = {
    'mailgun': [
        'django-mailgun==0.8.0',
    ],
    'raven': [
        'raven==5.8.1',
    ],
}


requires = [
    'Django==3.1.3',
    'dj-database-url==0.5.0',
    'django-braces==1.14.0',
    'django-configurations==2.2',
    'django-crispy-forms==1.10.0',
    'django-grappelli==2.14.2',
    'django-model-utils==4.0.0',
    'django-nested-admin==3.3.2',
    'djangorestframework==3.12.2',
    'envdir==1.0.1',
    'psycopg2-binary==2.8.6',
    'pytz==2020.4',
    'rules==2.2',
]


setup(
    name='armyimp',
    version='0.1.0',
    description='The universal FLOSS armylist builder.',
    long_description=read(BASE_DIR, 'README.rst'),
    author='eric goller',
    author_email='elbenfreund@DenkenInEchtzeit.net',
    packages=find_packages(),
    include_package_data=True,
    scripts=['manage.py'],
    install_requires=requires,
    license='AGPL3',
    zip_safe=False,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',

        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
