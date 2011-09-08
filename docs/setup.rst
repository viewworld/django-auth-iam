
Installation
============

:mod:`django-auth-iam` can be installed with pip:

.. code-block:: console

    $ pip install django-auth-iam

Your Amazon credentials need to be specified in a configuration file
that looks like this:

.. code-block:: cfg

    [Credentials]
    aws_access_key_id = AKEIAJLXJFEXAMPLE
    aws_secret_access_key = TLJASY/(ASF+fasdAJIdfWLasJfljaeisljae

    [DB]
    db_name = my_example_user_domain

Users will be stored in SimpleDB in the domain specified by
``db_name``. This file can be saved where ever you want. To tell
:mod:`boto` where it can find this file you need to set the
``BOTO_CONFIG`` environment variable. This can be done in your
``settings.py`` file::

    import os
    os.environ['BOTO_CONFIG'] = '/path/to/your/boto.cfg'

In your Django configuration you also need to set
``AUTHENTICATION_BACKEND``::

    AUTHENTICATION_BACKEND = (
        'django_auth_iam.backends.AmazonIAMBackend'
    )

Requirements
------------

:mod:`django_auth_iam` currently depends on the development version of :mod:`boto`.
You can install this with the following command:

.. code-block:: console

    $ pip install -e git+git://github.com/boto/boto.git#egg=boto
