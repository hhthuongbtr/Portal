from __future__ import unicode_literals

from django.db import models

class Agent(models.Model):
    name = models.CharField(unique=True, max_length=45)
    ip = models.CharField(unique=True, max_length=45)
    descr = models.CharField(max_length=100)
    thread = models.IntegerField()
    cpu = models.IntegerField()
    mem = models.IntegerField()
    disk = models.IntegerField()
    last_update = models.IntegerField()
    active = models.IntegerField()
    lng = models.CharField(max_length=20)
    lat = models.CharField(max_length=20)

    class Meta:
        db_table = 'agent'

class ProfileAgent(models.Model):
    profile_id = models.IntegerField()
    agent_id = models.IntegerField()
    status = models.IntegerField()
    analyzer_status = models.IntegerField()
    dropframe = models.IntegerField()
    dropframe_threshold = models.IntegerField()
    discontinuity = models.IntegerField()
    discontinuity_threshold = models.IntegerField()
    check = models.IntegerField()
    video = models.IntegerField()
    audio = models.IntegerField()
    monitor = models.IntegerField()
    analyzer = models.IntegerField()
    last_update = models.IntegerField()

    class Meta:
        db_table = 'profile_agent'
        unique_together = (('profile_id', 'agent_id'),)
