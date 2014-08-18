from django.contrib.auth.models import User, Group
from django.test import TestCase
from ucamlookup import user_in_groups


class UcamLookupTests(TestCase):

    def test_get_or_create_user_or_group(self):
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username="amc203")
        user1 = User.objects.create_user(username="amc203")
        user2 = User.objects.get(username="amc203")
        self.assertEqual(user1.id, user2.id)

        with self.assertRaises(Group.DoesNotExist):
            Group.objects.get(pk=101888)
        group1 = Group.objects.create(pk=101888)
        group2 = Group.objects.get(pk=101888)
        self.assertEqual(group1.id, group2.id)

    def test_user_in_groups(self):
        amc203 = User.objects.create_user(username="amc203")
        information_systems_group = Group.objects.create(pk=101888)
        self.assertTrue(user_in_groups(amc203, [information_systems_group]))
        finance_group = Group.objects.create(pk=101923)
        self.assertFalse(user_in_groups(amc203, [finance_group]))