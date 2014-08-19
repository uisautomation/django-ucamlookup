from django.core.exceptions import ValidationError
import re
from ibisclient import *

conn = createConnection()

def get_users_from_query(search_string):
    """ Returns the list of people based on the search string using the lookup ucam service
        :param search_string: the search string
    """
    persons = PersonMethods(conn).search(query=search_string)

    return map((lambda person: {'crsid': person.identifier.value, 'visibleName': person.visibleName}),
               persons)


def return_visibleName_by_crsid(crsid):
    person = PersonMethods(conn).getPerson(scheme='crsid', identifier=crsid)
    return person.visibleName if person is not None else ''


def get_groups_from_query(search_string):
    """ Returns the list of groups based on the search string using the lookup ucam service
        :param search_string: the search string
    """
    groups = GroupMethods(conn).search(query=search_string)

    return map((lambda group: {'groupid': int(group.groupid), 'title': group.title}),
               groups)


def return_title_by_groupid(groupid):
    group = GroupMethods(conn).getGroup(groupid=groupid)
    # TODO If a group does not exists in lookup should we allow it?
    if group is None:
        raise ValidationError("The group with id %(groupid)s does not exist in Lookup", code='invalid',
                              params={'groupid': groupid},)
    return group.title if group is not None else ''


def get_group_ids_of_a_user_in_lookup(user):
    """ Returns the list of groups of a user in the lookup service
    :param user: the user
    :return: the list of group_ids
    """

    group_list = PersonMethods(conn).getGroups(scheme="crsid", identifier=user.username)
    return map(lambda group: int(group.groupid), group_list)


def get_institutions(user=None):
    """ Returns the list of institutions using the lookup ucam service. The institutions of the user doing
    the request will be shown first
        :param user: the user doing the request
    """

    all_institutions = InstitutionMethods(conn).allInsts(includeCancelled=False)
    # filter all the institutions that were created for store year students
    all_institutions = filter(lambda institution: re.match(r'.*\d{2}$', institution.id) is None, all_institutions)

    if user is not None:
        try:
            all_institutions = PersonMethods(conn).getInsts("crsid", user.username) + all_institutions
        except IbisException:
            pass

    return map((lambda institution: (institution.instid, institution.name)), all_institutions)


def get_institution_name_by_id(institution_id, all_institutions=None):
    if all_institutions is not None:
        instname = next((institution[1] for institution in all_institutions if institution[0] == institution_id), None)
    else:
        institution = InstitutionMethods(conn).getInst(instid=institution_id)
        instname = institution.name if institution is not None else None

    return instname if instname is not None else 'This institution no longer exists in the database'


def user_in_groups(user, groups):
    """ Check in the lookup webservice if the user is member of any of the groups given
    :param user: the user
    :param groups: the list of groups
    :return: True if the user belongs to any of the groups or False otherwise
    """

    user_group_list = get_group_ids_of_a_user_in_lookup(user)
    groups = filter(lambda group: group.lookup_id in user_group_list, groups)
    if len(groups) > 0:
        return True
    else:
        return False