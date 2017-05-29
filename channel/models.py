from __future__ import unicode_literals

from django.db import models



class Channel(models.Model):
    name = models.CharField(max_length=45)
    descr = models.CharField(max_length=100)
    group_id = models.IntegerField()
    active = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'channel'
    def __unicode__(self):
        return unicode(self.name)

    def update_name(self, name):
        self.name = name
        self.save()

class Group(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        db_table = 'group'
    def __unicode__(self):
        return unicode(self.name)
        
    def update_name(self, name):
        self.name = name
        self.save()

class Profile(models.Model):
    ip = models.CharField(unique=True, max_length=100)
    descr = models.CharField(max_length=100)
    status = models.IntegerField()
    type = models.CharField(max_length=32)
    channel = models.ForeignKey(Channel, models.DO_NOTHING)
    protocol = models.CharField(max_length=10)
    graph = models.IntegerField()
    logo = models.IntegerField()
    check = models.IntegerField()
    sendmail = models.IntegerField()
    monitor = models.IntegerField()
    mediainfo = models.IntegerField()
    streamguru = models.IntegerField()
    last_update = models.IntegerField()
    change_status = models.IntegerField()
    active = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'profile'
        unique_together = (('id', 'ip'),)
    def __unicode__(self):
        return unicode(self.ip)


class ProfileGroup(models.Model):
    profile_id = models.IntegerField()
    permission = models.SmallIntegerField()
    group_id = models.IntegerField()

    class Meta:
        db_table = 'profile_group'
        unique_together = (('profile_id', 'group_id'),)

    def __unicode__(self):
        return unicode(self.group_id)

