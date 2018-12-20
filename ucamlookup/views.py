import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from ucamlookup.utils import get_users_from_query, get_groups_from_query


@login_required
def find_people(request):
    persons = get_users_from_query(request.GET.get('query'))
    return HttpResponse(json.dumps({'searchId_u': request.GET.get('searchId_u'), 'persons': persons}),
                        content_type='application/json')


@login_required
def find_groups(request):
    groups = get_groups_from_query(request.GET.get('query'))
    return HttpResponse(json.dumps({'searchId_g': request.GET.get('searchId_g'), 'groups': groups}),
                        content_type='application/json')
