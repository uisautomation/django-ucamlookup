import os
import sys
from django.core.management import execute_from_command_line
from django.conf import settings

settings.configure(
    DEBUG=False,
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'test.db', }},
    TIME_ZONE='Europe/London',
    USE_TZ=True,
    ROOT_URLCONF='ucamlookup.urls',
    PROJECT_APPS=(
        'ucamlookup',
    ),
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'ucamlookup',
        'django_jenkins',
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
    ],
    JENKINS_TASKS=(
        'django_jenkins.tasks.run_pylint',
    #    'django_jenkins.tasks.run_csslint',
        'django_jenkins.tasks.run_pep8',
        'django_jenkins.tasks.run_pyflakes',
        'django_jenkins.tasks.run_sloccount',
    ),
    PEP8_RCFILE=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'jenkins/pep8'),
    PYLINT_RCFILE=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'jenkins/pylint'),
)

execute_from_command_line(sys.argv)
