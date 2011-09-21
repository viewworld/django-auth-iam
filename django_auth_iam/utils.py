
"""
django_auth_iam.utils
~~~~~~~~~~~~~~~~~~~~~~~~

This module provides utility functions.

:copyright: (c) 2011  ViewWorld ApS
:license: GPLv3, see LICENSE for details.

"""

import hashlib
from Crypto.Cipher import AES


def encrypt_key(plain, password):
    if isinstance(plain, unicode):
        raise ValueError('unicode string is not allowed')
    encryption_key = hashlib.sha256(password).digest()
    encryptor = AES.new(encryption_key, AES.MODE_CBC)
    plain += ' ' * (16 - len(plain) % 16)
    cipher = encryptor.encrypt(plain)
    return cipher.encode('base64')

def decrypt_key(cipher, password):
    cipher = cipher.decode('base64')
    encryption_key = hashlib.sha256(password).digest()
    decryptor = AES.new(encryption_key, AES.MODE_CBC)
    plain = decryptor.decrypt(cipher).rstrip(' ')
    return plain
