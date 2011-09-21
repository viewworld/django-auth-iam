# -*- encoding: utf-8 -*-

import boto

from boto.sdb.db.model import Model
from django.test import TestCase

from . import utils
from .properties import BCryptPassword, BCryptPasswordProperty

class TestEncryption(TestCase):
    def test_reversable(self):
        password = 'foobar123'
        key = 'AKIAIOSFODNN7EXAMPLE'
        enc_key = utils.encrypt_key(key, password)
        self.assertEqual(key, utils.decrypt_key(enc_key, password))
        # Test with unicode data
        key = u'AKIAIOSFODNN7EXHHE}O±J¸ZOXZÆL]}@¡ØÆLAMPLE'
        enc_key = utils.encrypt_key(key.encode('utf8'), password)
        self.assertEqual(key, utils.decrypt_key(enc_key, password).decode('utf8'))

    def test_types(self):
        password = 'foobar123'
        key = 'AKIAIOSFODNN7EXAMPLE'
        self.assertIsInstance(key, str)
        enc_key = utils.encrypt_key(key, password)
        self.assertIsInstance(enc_key, str)
        dec_key = utils.decrypt_key(enc_key, password)
        self.assertIsInstance(dec_key, str)


class TestBCryptPassword(TestCase):

    def test_init(self):
        p = BCryptPassword()
        self.assertEqual(str(p), '')
        self.assertEqual(len(p), 0)
        p = BCryptPassword('')
        self.assertEqual(str(p), '')
        self.assertEqual(len(p), 0)
        p = BCryptPassword('$2a$12$8Khdz89/84OwXYsN8zxCQ.AqYKMux9SagW1/sMEfWE9TLjN6dZ42m')
        self.assertNotEqual(str(p), '')
        self.assertNotEqual(len(p), 0)

    def test_set(self):
        p = BCryptPassword()
        p.set('')
        self.assertEqual(str(p), '')
        self.assertEqual(len(p), 0)
        p = BCryptPassword()
        p.set('test')
        self.assertNotEqual(str(p), '')
        self.assertNotEqual(len(p), 0)

    def test_compare(self):
        p = BCryptPassword()
        self.assertFalse(p == '')
        self.assertFalse(p != '')
        self.assertFalse(p == 'test')
        self.assertFalse(p == None)
        p.set('test')
        self.assertFalse(p == '')
        self.assertTrue(p != '')
        self.assertTrue(p == 'test')
        self.assertFalse(p == None)

    def test_invalid(self):
        p = BCryptPassword()
        self.assertTrue(p.is_invalid())
        p = BCryptPassword('')
        self.assertTrue(p.is_invalid())
        p = BCryptPassword('$2a$12$8Khdz89/84OwXYsN8zxCQ.AqYKMux9SagW1/sMEfWE9TLjN6dZ42m')
        self.assertFalse(p.is_invalid())

    def test_reinit(self):
        p = BCryptPassword()
        p.set('test')
        hash = str(p)
        p = BCryptPassword(hash)
        self.assertTrue(p == 'test')

    def test_badhash(self):
        with self.assertRaises(ValueError):
            p = BCryptPassword('badhash')


class TestModel(Model):
    __consistent__ = True

    p = BCryptPasswordProperty()

class TestBCryptPasswordProperty(TestCase):

    def setUp(self):
        sdb = boto.connect_sdb()
        sdb.create_domain('test_domain')

    def tearDown(self):
        sdb = boto.connect_sdb()
        sdb.delete_domain('test_domain')

    def test_settings(self):
        t = TestModel()
        self.assertEqual(str(t.p), '')
        self.assertFalse(t.p == '')
        self.assertTrue(t.p.is_invalid())
        t.p = 'test'
        self.assertNotEqual(str(t.p), '')
        self.assertTrue(t.p == 'test')
        self.assertFalse(t.p.is_invalid())
        
    def test_save(self):
        t = TestModel()
        t.p = 'test123'
        t = t.put()
        id = t.id
        t = TestModel.get_by_id(id)
        self.assertFalse(t.p.is_invalid())
        self.assertIsInstance(t.p.str, basestring)
        self.assertTrue(t.p == 'test123')
