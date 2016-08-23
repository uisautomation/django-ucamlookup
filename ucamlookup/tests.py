import json
import sys
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.test import TestCase
from ucamlookup.models import LookupGroup
from ucamlookup.utils import user_in_groups, get_users_from_query, return_visibleName_by_crsid, get_groups_from_query, \
    return_title_by_groupid, get_group_ids_of_a_user_in_lookup, get_institutions, get_institution_name_by_id, \
    validate_crsids


class UcamLookupTests(TestCase):

    def test_add_name_to_user_and_add_title_to_group(self):
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username="amc203")
        user1 = User.objects.create_user(username="amc203")
        user2 = User.objects.get(username="amc203")
        self.assertEqual(user1.id, user2.id)
        self.assertEqual(user2.last_name, "Dr Abraham Martin Campillo")

        with self.assertRaises(LookupGroup.DoesNotExist):
            LookupGroup.objects.get(lookup_id="101888")
        group1 = LookupGroup.objects.create(lookup_id="101888")
        group2 = LookupGroup.objects.get(lookup_id="101888")
        self.assertEqual(group1.id, group2.id)
        self.assertEqual(group2.name, "CS Information Systems team")
        self.assertEqual(str(group2), "CS Information Systems team (101888)")

    def test_user_in_groups(self):
        amc203 = User.objects.create_user(username="amc203")
        information_systems_group = LookupGroup.objects.create(lookup_id="101888")
        self.assertTrue(user_in_groups(amc203, [information_systems_group]))
        finance_group = LookupGroup.objects.create(lookup_id="101923")
        self.assertFalse(user_in_groups(amc203, [finance_group]))

    def test_get_users_from_query(self):
        results = get_users_from_query("amc203")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['crsid'], "amc203")
        self.assertEqual(results[0]['visibleName'], "Dr Abraham Martin Campillo")

        results = get_users_from_query("Abraham Martin Campillo")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['crsid'], "amc203")
        self.assertEqual(results[0]['visibleName'], "Dr Abraham Martin Campillo")

    def test_return_visibleName_by_crsid(self):
        result = return_visibleName_by_crsid("amc203")
        self.assertEqual(result, "Dr Abraham Martin Campillo")
        result = return_visibleName_by_crsid("amc20311")
        self.assertEqual(result, '')

    def test_get_groups_from_query(self):
        results = get_groups_from_query("Information Systems")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['groupid'], "101888")
        self.assertEqual(results[0]['title'], "CS Information Systems team")

    def test_return_title_by_groupid(self):
        result = return_title_by_groupid("101888")
        self.assertEqual(result, "CS Information Systems team")

        with self.assertRaises(ValidationError):
            return_title_by_groupid("203840928304982")

    def test_get_groups_of_a_user_in_lookup(self):
        amc203 = User.objects.create_user(username="amc203")
        information_systems_group = LookupGroup.objects.create(lookup_id="101888")
        amc203_groups = get_group_ids_of_a_user_in_lookup(amc203)
        self.assertIn(information_systems_group.lookup_id, amc203_groups)

    def test_get_institutions(self):
        results = get_institutions()
        self.assertIn(("UIS", "University Information Services"), results)

    def test_get_institutions_with_user(self):
        amc203 = User.objects.create_user(username="amc203")
        results = get_institutions(user=amc203)
        self.assertIn(("UIS", "University Information Services"), results)

    def test_get_institution_name_by_id(self):
        result = get_institution_name_by_id(institution_id="UIS")
        self.assertEqual("University Information Services", result)

    def test_get_institution_name_by_id_with_cache(self):
        all_institutions = get_institutions()
        result = get_institution_name_by_id(institution_id="UIS", all_institutions=all_institutions)
        self.assertEqual("University Information Services", result)

        test_user = User.objects.create_user(username="test0001")
        results = get_institutions(user=test_user)

        self.assertEqual(all_institutions, results)

    def test_views_without_login(self):
        response = self.client.get(reverse('ucamlookup_find_people'), {'query': 'amc203', 'searchId_u': '1'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
        response = self.client.get(reverse('ucamlookup_find_groups'), {'query': 'Information Systems',
                                                                       'searchId_g': '1'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_findpeople_view(self):
        User.objects.create_user(username="amc203", password="test")
        self.assertTrue(self.client.login(username='amc203', password="test"))
        response = self.client.get(reverse('ucamlookup_find_people'), {'query': 'amc203', 'searchId_u': '1'})
        if sys.version_info >= (3,0):
            jsonresponse = json.loads(response.content.decode('utf-8'))
        else:
            jsonresponse = json.loads(response.content)
        self.assertIn('persons', jsonresponse)
        self.assertIn('searchId_u', jsonresponse)
        self.assertEqual(jsonresponse['searchId_u'], "1")
        self.assertEqual(len(jsonresponse['persons']), 1)
        self.assertEqual(jsonresponse['persons'][0]['visibleName'], "Dr Abraham Martin Campillo")
        self.assertEqual(jsonresponse['persons'][0]['crsid'], "amc203")

    def test_findgroups_view(self):
        User.objects.create_user(username="amc203", password="test")
        self.assertTrue(self.client.login(username='amc203', password="test"))
        response = self.client.get(reverse('ucamlookup_find_groups'), {'query': 'Information Systems',
                                                                       'searchId_g': '1'})
        if sys.version_info >= (3,0):
            jsonresponse = json.loads(response.content.decode('utf-8'))
        else:
            jsonresponse = json.loads(response.content)
        self.assertIn('groups', jsonresponse)
        self.assertIn('searchId_g', jsonresponse)
        self.assertEqual(jsonresponse['searchId_g'], "1")
        self.assertEqual(len(jsonresponse['groups']), 1)
        self.assertEqual(jsonresponse['groups'][0]['groupid'], "101888")
        self.assertEqual(jsonresponse['groups'][0]['title'], "CS Information Systems team")

    def test_validate_crsids(self):
        # users do not exist in the DB
        crsid_list = "amc203,jw35"
        user_list = validate_crsids(crsid_list)
        self.assertEqual(user_list[0].username, "amc203")
        self.assertEqual(user_list[1].username, "jw35")

        # users exist in the DB
        user_list = validate_crsids(crsid_list)
        self.assertEqual(user_list[0].username, "amc203")
        self.assertEqual(user_list[1].username, "jw35")

        user_list = validate_crsids("")
        self.assertEqual(len(user_list), 0)

        user_list = validate_crsids(None)
        self.assertEqual(len(user_list), 0)

        with self.assertRaises(ValidationError):
            validate_crsids("kaskvdkam20e9mciasmdimadf")
