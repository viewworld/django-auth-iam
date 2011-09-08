#!/usr/bin/env python
import os
import sys
from os.path import join

from django.conf import settings

os.environ['BOTO_CONFIG'] = os.path.abspath('test_boto.cfg')

if not settings.configured:
    settings.configure(
        DATABASE_ENGINE='sqlite3',
        INSTALLED_APPS=[
            'django_auth_iam',
        ],
        AUTHENTICATION_BACKENDS = (
            'django_auth_iam.backends.AmazonIAMBackend',
        )
    )

from django.test.simple import run_tests


def runtests(*test_args):
    if not test_args:
        test_args = ['django_auth_iam']
    failures = run_tests(test_args, verbosity=1, interactive=True)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
