#!/usr/bin/env python

try:
    import subprocess
    has_subprocess = True
except:
    has_subprocess = False

from distutils.core import setup
from distutils.cmd import Command

import django_auth_iam

class docs(Command):

    description = "generate documentation"
    user_options = []

    def initialize_options(self): pass
    def finalize_options(self): pass

    def run(self):
        path = 'docs/_build/{0}'.format(django_auth_iam.__version__)
        mode = 'html'
        try:
            os.makedirs(path)
        except:
            pass
        if has_subprocess:
            status = subprocess.call(['sphinx-build', '-E', '-b', mode, 'docs', path])
            if status:
                raise RuntimeError("documentation step '{0}' failed".format(mode))
            print ''
            print "Documentation step '{0}' performed, results here:".format(mode)
            print ' {0}/'.format(path)
        else:
            print '`setup.py docs` is not supported for this version of Python.'

setup(
    name='django-auth-iam',
    version=django_auth_iam.__version__,
    description='Django authentication backend using Amazon IAM',
    long_description='''This is a Django authentication backend that authenticates against the Amazon IAM service.''',
    url='https://github.com/viewworld/django-auth-iam/',
    author='Michael Budde',
    author_email='mb@viewworld.dk',
    license='BSD',
    packages=['django_auth_iam'],
    classifiers=[],
    keywords=['django', 'amazon', 'authentication', 'auth'],
    requires=['boto', 'PyCrypto', 'py_bcrypt'],
    cmdclass={'docs': docs}
)
