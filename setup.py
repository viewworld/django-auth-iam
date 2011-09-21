#!/usr/bin/env python

import os

from setuptools import setup
from distutils.cmd import Command

import django_auth_iam


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name='django-auth-iam',
    version=django_auth_iam.__version__,
    description='Django authentication backend using Amazon IAM',
    long_description=read('README.rst'),
    url='https://github.com/viewworld/django-auth-iam/',
    author='Michael Budde',
    author_email='mb@viewworld.dk',
    license='GPL v3',
    packages=['django_auth_iam'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Topic :: Security',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
    ],
    keywords=['django', 'amazon', 'authentication', 'auth'],
    install_requires=['boto', 'PyCrypto', 'py_bcrypt'],
)
