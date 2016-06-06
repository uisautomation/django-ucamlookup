from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from ucamlookup.models import LookupGroup
from ucamlookup.utils import return_visibleName_by_crsid, return_title_by_groupid


@receiver(pre_save, sender=User)
def add_name_to_user(instance, **kwargs):
    user = instance
    if user is not None:
        user.last_name = return_visibleName_by_crsid(user.username)[:30]


@receiver(pre_save, sender=LookupGroup)
def add_title_to_group(instance, **kwargs):
    group = instance
    if group is not None:
        group.name = return_title_by_groupid(group.lookup_id)[:80]
