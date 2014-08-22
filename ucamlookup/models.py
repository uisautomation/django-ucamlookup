from django.db import models


class LookupGroup(models.Model):
    name = models.CharField(max_length=255)
    lookup_id = models.CharField(max_length=255, unique=True)