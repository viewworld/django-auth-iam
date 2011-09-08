
Settings
========

:mod:`django-auth-iam` has the following settings that control how it works.


IAM_USER_CLASS
^^^^^^^^^^^^^^

:Default: ``'django_auth_iam.models.User'`` (:class:`django_auth_iam.models.User`)

Controls what class that is used when instanciating a IAM user
object. This should either be the default value or point a subclass of
the default class. You can use this to add extra attributes to your
user model::

    import django_auth_iam.models
    from boto.sdb.db.property import *

    class MyUser(django_auth_iam.models.User):

        favorite_color = StringProperty()

And in your ``settings.py``::

    IAM_USER_CLASS = 'myapp.models.MyUser'

.. seealso::

    The API documentation for :mod:`boto` contains the documentation of
    the different property types.
