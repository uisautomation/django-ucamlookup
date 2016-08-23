from django.conf.urls import url
from ucamlookup.views import find_people, find_groups


urlpatterns = [
    url(r'findPeople$', find_people, name='ucamlookup_find_people'),
    url(r'findGroups$', find_groups, name='ucamlookup_find_groups'),
]
