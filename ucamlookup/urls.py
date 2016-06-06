import django
from django.conf.urls import patterns, url
from ucamlookup.views import find_people, find_groups


if django.VERSION[0] <= 1 and django.VERSION[1] <= 7:
    urlpatterns = patterns(
        '',
        url(r'findPeople$', find_people, name='ucamlookup_find_people'),
        url(r'findGroups$', find_groups, name='ucamlookup_find_groups'),
    )
else:
    urlpatterns = [
        url(r'findPeople$', find_people, name='ucamlookup_find_people'),
        url(r'findGroups$', find_groups, name='ucamlookup_find_groups'),
    ]
