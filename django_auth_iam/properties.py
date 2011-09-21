
"""
django_auth_iam.models
~~~~~~~~~~~~~~~~~~~~~~~~

This module provides custom models properties.

:copyright: (c) 2011  ViewWorld ApS
:license: GPLv3, see LICENSE for details.

"""

import bcrypt

from boto.sdb.db.property import Property, StringProperty, PasswordProperty
from boto.utils import Password


class BCryptPassword(Password):

    def __init__(self, hash=None, hashfunc=None):
        if hash and not '$' in hash:
            raise ValueError('hash does not look like a proper bcrypt hash')
        elif hash is None:
            hash = ''
        super(BCryptPassword, self).__init__(hash, hashfunc)

    def set(self, value):
        """Set the password.

        The password will be hashed with the bcrypt algorithm before
        being stored.

        """
        if not isinstance(value, basestring):
            raise ValueError('value should be a string')
        if not value:
            self.str = ''
        else:
            self.str = bcrypt.hashpw(value, bcrypt.gensalt())

    def is_invalid(self):
        return self.str == ''

    def __eq__(self, other):
        """Returns ``True`` if the passwords match.

        The other password is hashed before comparing. The time taken
        is independent of the number of characters that match.

        """
        if not self.str or not other:
            return False
        hashed = str(self.str)
        other = bcrypt.hashpw(other, hashed)
        if len(hashed) != len(other):
            return False
        result = 0
        for x, y in zip(hashed, other):
            result |= ord(x) ^ ord(y)
        return result == 0

    def __ne__(self, other):
        if not self.str:
            return False
        return not (self == other)


class BCryptPasswordProperty(PasswordProperty):

    data_type = BCryptPassword
    type_name = 'BCryptPassword'

    def __get__(self, obj, objtype):
        return Property.__get__(self, obj, objtype)
