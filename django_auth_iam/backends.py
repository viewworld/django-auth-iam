
"""
django_auth_iam.backends
~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a backend for use with Django's authentication
framework.

:copyright: (c) 2011  ViewWorld Aps
:license: GPLv3, see LICENSE for details.

"""

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured

import logging
logger = logging.getLogger('django_auth_iam')


IAM_USER_CLASS = getattr(settings, 'IAM_USER_CLASS', 'django_auth_iam.models.User')


class AmazonIAMBackend(ModelBackend):
    """
    Authenticates against Amazon's IAM service.
    """

    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def __init__(self):
        self.user_class = self._load_user_class()

    def _load_user_class(self):
        module, sep, attr = IAM_USER_CLASS.rpartition('.')
        try:
            mod = import_module(module)
        except ImportError, e:
            raise ImproperlyConfigured('Error importing user class module '
                                       '{0}: "{1}"'.format(module, e))
        except ValueError, e:
            raise ImproperlyConfigured('Error importing user class module. '
                                       'Is IAM_USER_CLASS a string?')
        try:
            cls = getattr(mod, attr)
        except AttributeError:
            raise ImproperlyConfigured('Module "{0}" does not define a '
                                       '"{1}" user class'.format(module, attr))
        return cls

    def authenticate(self, username=None, password=None):
        iamuser = self.user_class.get_by_username(username)
        if iamuser is None or iamuser.password != password:
            logger.info('Authentication FAILED for user `{0}`'.format(username))
            return None
        secret_key = iamuser.get_secret_key(password)
        user, created = User.objects.get_or_create(username=username)
        user.aws_credentials = (iamuser.access_key, secret_key)
        user.iam_user = iamuser
        logger.info('Authentication SUCCEEDED for user `{0}`'.format(username))
        return user
