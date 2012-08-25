#!/usr/bin/env python
import sys

from django.conf import settings


if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'hilbert',
        ),
        SITE_ID=1,
        SECRET_KEY='django-hilbert-test-secrets',
        ROOT_URLCONF='hilbert.tests.urls',
        LOGIN_URL='/login/',
        LOGIN_REDIRECT_URL='/',
    )


from django.test.utils import get_runner


def runtests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['hilbert', ])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()

