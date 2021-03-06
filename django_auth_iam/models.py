
"""
django_auth_iam.models
~~~~~~~~~~~~~~~~~~~~~~~~

This module provides user and group models.

:copyright: (c) 2011  ViewWorld ApS
:license: GPLv3, see LICENSE for details.

"""

import boto
from boto.exception import BotoServerError
from boto.sdb.db.model import Model
from boto.sdb.db.property import StringProperty

from .properties import BCryptPasswordProperty
from .utils import encrypt_key, decrypt_key


class User(Model):

    username = StringProperty(required=True, unique=True)
    """Username for the user."""
    password = BCryptPasswordProperty()
    """Password for the user.

    The password is automatically hashed with :mod:`bcrypt` when it is
    stored. The password can be set and compared using standard
    operators.

    >>> user = User()
    >>> user.password = 'foo'
    >>> user.password == 'foo'
    True
    >>> user.password != 'bar'
    True
    >>> print user.password
    $2a$12$REbzH3KM5YdyAO6d8lGHSu2zeQZ2i4CzXpV4Y2HbIO7BYSCt9Plo.

    .. note::

        Setting a new password does not re-encrypt the secret key. Use
        :meth:`User.change_password` for changing the password and
        re-encrypting the secret key in one step.

    """
    access_key = StringProperty()
    """Access key to Amazon services."""
    enc_secret_key = StringProperty()
    """Encrypted secret key to Amazon services."""

    class AlreadyExist(Exception):
        def __init__(self, username):
            Exception.__init__(self, 'a user with the username "{0}" already '
                               'exist'.format(username))

    def get_secret_key(self, password):
        """Get the decrypted secret key.

        :param password: the unhashed password for the user.

        """
        return decrypt_key(self.enc_secret_key, password)

    @classmethod
    def get_by_username(cls, username):
        """Get a user by username. Returns ``None`` if the user is
        not found.

        """
        user = tuple(cls.find(username=username, limit=1))
        if len(user) == 0:
            return None
        return user[0]

    @classmethod
    def create(cls, username, password, force=False):
        """Create a new user. Raises :exc:`.User.AlreadyExist` if the
        user already exist in IAM.

        May also raise :class:`boto.exception.BotoServerError`.
        """
        if force:
            cls._delete_iam_user(username)
        cls._create_iam_user(username)
        user = cls.get_by_username(username)
        if user is None:
            user = cls()
        user.username = username
        user.password = password
        cls._create_access_key(user, password)
        user.put()
        return user

    @classmethod
    def _create_iam_user(cls, username):
        iam = boto.connect_iam()
        try:
            iam.create_user(username)
        except BotoServerError as e:
            if e.status == 409:
                raise cls.AlreadyExist(username)
            else:
                raise e

    @staticmethod
    def _create_access_key(user, password):
        iam = boto.connect_iam()
        response = iam.create_access_key(user.username)
        result = response['create_access_key_response']['create_access_key_result']
        access_key = result['access_key']['access_key_id']
        secret_key = result['access_key']['secret_access_key']
        enc_secret_key = encrypt_key(secret_key.encode('utf8'), password)
        user.access_key = access_key
        user.enc_secret_key = enc_secret_key

    def delete(self):
        """Delete the user from IAM and SimpleDB.

        May raise :exc:`boto.exception.BotoServerError`.

        """
        User._delete_iam_user(self.username)
        super(User, self).delete()

    @staticmethod
    def _delete_iam_user(username):
        try:
            iam = boto.connect_iam()
            response = iam.get_all_access_keys(username)
            key_ids = [k['access_key_id'] for k in
                       response['list_access_keys_response']
                       ['list_access_keys_result']['access_key_metadata']]
            for key in key_ids:
                iam.delete_access_key(key, username)
            iam.delete_user(username)
        except BotoServerError as e:
            if e.status != 404:
                raise e

    def change_password(self, cur_password, new_password):
        """Helper method for changing the password and re-encrypting the
        secret key.

        :param cur_password: the user's current password.
        :param new_password: the user's new password.

        """
        self.password = new_password
        secret_key = self.get_secret_key(cur_password)
        self.enc_secret_key = encrypt_key(secret_key, new_password)


class Group(Model):

    name = StringProperty(required=True, unique=True)
    """Group name."""

    class AlreadyExist(Exception):
        def __init__(self, name):
            Exception.__init__(self, 'a group with the name "{0}" already exist'
                               .format(name))

    @classmethod
    def get_by_name(cls, name):
        """Get a group by name. Returns ``None`` if the group is not found."""
        group = tuple(cls.find(name=name, limit=1))
        if len(group) == 0:
            return None
        return group[0]

    @classmethod
    def create(cls, name, force=False):
        """Create a new group. Raises :exc:`.Group.AlreadyExist` if
        the group already exist in IAM.

        May also raise :class:`boto.exception.BotoServerError`.

        """
        if force:
            cls._delete_iam_group(name)
        cls._create_iam_group(name)
        group = cls.get_by_name(name)
        if group is None:
            group = cls()
        group.put()
        return group

    @classmethod
    def _create_iam_group(cls, name):
        iam = boto.connect_iam()
        try:
            iam.create_group(name)
        except BotoServerError as e:
            if e.status == 409:
                raise cls.AlreadyExist(username)
            else:
                raise e

    def delete(self):
        """Delete the group from IAM and SimpleDB.

        May raise :exc:`boto.exception.BotoServerError`.

        """
        Group._delete_iam_group(self.name)
        super(Group, self).delete()

    @staticmethod
    def _delete_iam_group(name):
        try:
            iam = boto.connect_iam()
            iam.delete_group(name)
        except BotoServerError as e:
            if e.status != 404:
                raise e
