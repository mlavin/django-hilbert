import os
import sys

from django.conf import settings


if not settings.configured:
    settings.configure(
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'test.db',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'hilbert',
        ],
        ROOT_URLCONF = 'hilbert.tests.urls',
    )


from django.test.simple import run_tests


def runtests(*test_args):
    if not test_args:
        test_args = ['hilbert']
    parent = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", )
    sys.path.insert(0, parent)
    failures = run_tests(test_args, verbosity=1, interactive=True)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])

