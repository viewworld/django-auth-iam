
Usage
=====


Creating users
--------------

:mod:`django_auth_iam` is not integrated with the Django admin
interface. You can instead use a python shell or script to create your
users. You can start a python shell with ``python manage.py shell``::

    >>> from django_auth_iam.models import User
    >>> User.create('user1', 'password')
    User<...>
    >>> User.create('user2', 'foo1234')
    User<...>
    >>> user = User.get_by_username('user1')
    >>> user.delete()

Passwords are automatically hashed before they are stored. To change a users
password you can use the method
:meth:`~django_auth_iam.models.User.change_password`::

    >>> user = User.create('testuser', 'pass')
    >>> user.password == 'pass'
    True
    >>> user.change_password('pass', 'spam')
    >>> print user.password
    $2a$12$hmYnBI/VdPjxZep1lbIcLObBlN.LYYXRanL/1AMYlaJeIn30aBOjO
    >>> user.password == 'spam'
    True
