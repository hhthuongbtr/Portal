
from __future__ import unicode_literals

from django.db import models

class Logs(models.Model):
    host = models.CharField(max_length=128, blank=True, null=True)
    facility = models.CharField(max_length=10, blank=True, null=True)
    priority = models.CharField(max_length=10, blank=True, null=True)
    level = models.CharField(max_length=10, blank=True, null=True)
    tag = models.CharField(max_length=10, blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    program = models.CharField(max_length=15, blank=True, null=True)
    msg = models.TextField(blank=True, null=True)
    seq = models.BigIntegerField()
    counter = models.IntegerField()
    fo = models.DateTimeField(blank=True, null=True)
    lo = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'logs'

    def __unicode__(self):
        return unicode(self.program)