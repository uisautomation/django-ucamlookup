from django.conf.urls import patterns, url
from views import find_people, find_groups

urlpatterns = patterns('',
    url(r'findPeople$', find_people, name='ucamlookup_find_people'),
    url(r'findGroups$', find_groups, name='ucamlookup_find_groups'),
)