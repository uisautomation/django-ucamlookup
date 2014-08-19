from django.db import models


class LookupGroup(models.Model):
    name = models.CharField(max_length=250)
    lookup_id = models.IntegerField()