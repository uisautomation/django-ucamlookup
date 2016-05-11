import logging
import os
import sys
import django
from django.conf import settings
from django.test.runner import DiscoverRunner

DIRNAME = os.path.dirname(__file__)

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
        'ucamlookup',
    ),
    MIDDLEWARE_CLASSES=(
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                # insert your TEMPLATE_DIRS here
            ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                    # list if you haven't customized them:
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]
)

logging.basicConfig()

django.setup()
test_runner = DiscoverRunner()

failures = test_runner.run_tests(['ucamlookup', ])
if failures:
    sys.exit(failures)
