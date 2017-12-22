from __future__ import unicode_literals
from django.db import models
from setting.DateTime import DateTime

class Encoder(models.Model):
    name = models.CharField(max_length=255)
    ip_monitor = models.CharField(max_length=16, blank=True, null=True)
    source_main = models.CharField(max_length=25, blank=True, null=True)
    source_backup = models.CharField(max_length=25, blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'encoder'

    def parse_object_as_json_fortmat(self, encoder):
        args = {
                 'id'               : encoder.id,
                 'name'             : encoder.name,
                 'ip_monitor'       : encoder.ip_monitor,
                 'source_main'      : encoder.source_main,
                 'source_backup'    : encoder.source_backup,
                 'active'           : True if encoder.active else False
                }
        return args

class Event(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=60, blank=True, null=True)
    start_date = models.IntegerField(blank=True, null=True)
    end_date = models.IntegerField(blank=True, null=True)
    create_date = models.IntegerField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'event'
    ordering = ('-start_date',)

    def parse_object_as_json_fortmat(self, event):
        date_time = DateTime()
        args = {
                 'id'               : event.id,
                 'name'             : event.name,
                 'location'         : event.location,
                 'region'           : event.region,
                 'start_date'       : str(date_time.convert_unix_timestamp_2_human_creadeble(event.start_date)),
                 'end_date'         : str(date_time.convert_unix_timestamp_2_human_creadeble(event.end_date)),
                 'create_date'      : str(date_time.convert_unix_timestamp_2_human_creadeble(event.create_date)),
                 'active'           : True if event.active else False
                }
        return args

class EventMonitor(models.Model):
    pid = models.IntegerField(blank=True, null=True)
    event = models.ForeignKey(Event, models.DO_NOTHING)
    encoder = models.ForeignKey(Encoder, models.DO_NOTHING)
    service_check = models.ForeignKey('ServiceCheck', models.DO_NOTHING)
    status = models.IntegerField(blank=True, null=True)
    last_update = models.IntegerField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    descr = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'event_monitor'
        unique_together = (('id', 'event', 'encoder', 'service_check'),)

    def parse_object_as_json_fortmat(self, event_monitor):
        agrs = {
                'id'                : event_monitor.id,
                'pid'               : event_monitor.pid,
                'event_id'          : event_monitor.event_id,
                'encoder_id'        : event_monitor.encoder_id,
                'service_check_id'  : event_monitor.service_check_id,
                'status'            : event_monitor.status,
                'last_update'       : event_monitor.last_update,
                'active'            : True if event_monitor.active else False,
                'descr'             : event_monitor.descr
                }
        return agrs


class ServiceCheck(models.Model):
    name = models.CharField(max_length=255)
    active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'service_check'

    def parse_object_as_json_fortmat(self, service_check):
        args = {
                 'id'               : service_check.id,
                 'name'             : service_check.name,
                 'active'           : True if service_check.active else False
                }
        return args