from django.contrib.auth.models import User, Group
from django.db.models.signals import pre_save
from django.dispatch import receiver
from utils import *


@receiver(pre_save, sender=User)
def add_name_to_user(instance, **kwargs):
    user = instance
    if user is not None:
        user.last_name = return_visibleName_by_crsid(user.username)


@receiver(pre_save, sender=Group)
def add_title_to_group(instance, **kwargs):
    group = instance
    if group is not None:
        group.name = return_title_by_groupid(group.id)