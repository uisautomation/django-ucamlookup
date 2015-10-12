import os, sys
from django.core.management import execute_from_command_line
from django.conf import settings
settings.configure(
    DEBUG=False,
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'test.db', }},
    TIME_ZONE='Europe/London',
    USE_TZ=True,
    ROOT_URLCONF='ucamlookup.urls',
    PROJECT_APPS = (
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
        'django_jenkins', ),
    MIDDLEWARE_CLASSES=(
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
    JENKINS_TASKS = (
        'django_jenkins.tasks.run_pylint',
    #    'django_jenkins.tasks.run_csslint',
        'django_jenkins.tasks.run_pep8',
        'django_jenkins.tasks.run_pyflakes',
        'django_jenkins.tasks.run_sloccount',
    ),
    PEP8_RCFILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'jenkins/pep8'),
    PYLINT_RCFILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'jenkins/pylint'),
)

execute_from_command_line(sys.argv)