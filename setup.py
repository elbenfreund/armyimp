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
    'Django==2.0.2',
    'dj-database-url==0.4.2',
    'django-braces==1.12.0',
    'django-configurations==2.0',
    'django-crispy-forms==1.7.0',
    'django-grappelli==2.11.1',
    'django-model-utils==3.1.1',
    'django-nested-admin==3.0.21',
    'djangorestframework==3.7.7',
    'envdir==0.7',
    'psycopg2-binary==2.7.4',
    'pytz==2018.3',
    'rules==1.3',
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
