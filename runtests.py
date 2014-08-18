import logging
import os, sys
import django

DIRNAME = os.path.dirname(__file__)

from django.conf import settings
settings.configure(
    DEBUG=False,
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'test.db', }},
    TIME_ZONE='Europe/London',
    USE_TZ=True,
    ROOT_URLCONF='ucamlookup.urls',
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'ucamlookup', ),
    MIDDLEWARE_CLASSES=(
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)

logging.basicConfig()

if django.get_version().startswith('1.7'):
    django.setup()
    from django.test.runner import DiscoverRunner
    test_runner = DiscoverRunner()
elif django.get_version().startswith('1.6'):
    from django.test.runner import DiscoverRunner
    test_runner = DiscoverRunner()
else:
    from django.test.simple import DjangoTestSuiteRunner
    test_runner = DjangoTestSuiteRunner(verbosity=1)

failures = test_runner.run_tests(['ucamlookup', ])
if failures:
    sys.exit(failures)