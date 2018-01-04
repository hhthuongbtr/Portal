from event.models import *
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
import json
from django.core.exceptions import ObjectDoesNotExist
from setting.DateTime import DateTime
from BLL.event import Event as EventBLL
from accounts.user_info import *


#######################################################################
#                                                                     #
#-------------------------------EVENT---------------------------------#
#                                                                     #
#######################################################################
class EventList:
    """
    List all events, or create a new event.
    """
    @csrf_exempt
    def routing(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login')
        if request.method == "GET":
            return self.get(request)
        elif request.method == "POST":
            return self.post(request)

    @csrf_exempt
    def get(self, request):
        args = {}
        try:
            event_list = Event.objects.all()
        except Exception as e:
            args["detail"] = str(e)
            data = json.dumps(args)
            return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)
        if event_list:
            args_event_list=[]
            for event in event_list:
                args_event_list.append(Event().parse_object_as_json_fortmat(event))
            args["detail"] = "OK"
            args["event_list"] = args_event_list
        else:
            args["detail"] = "Event is empty"
        data = json.dumps(args)
        return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)

    @csrf_exempt
    def post(self, request):
        agrs={}
        try:
            data = json.loads(request.body)
        except Exception as e:
            agrs["detail"] = "No data input found!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        flag = False
        if ('end_date' in data):
            flag = True
            end_date = data['end_date']
            date_time = DateTime()
            end_date = date_time.conver_human_creadeble_2_unix_timetamp_local(end_date)
        else:
            end_date = 0;
        if ('name' in data):
            flag = True
            name = data['name'].encode("utf-8")
        else:
            agrs["detail"] = "Name not empty!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        if ('start_date' in data):
            flag = True
            start_date = data['start_date']
            date_time = DateTime()
            start_date = date_time.conver_human_creadeble_2_unix_timetamp_local(start_date)
        else:
            start_date = 0;
        if ('active' in data):
            flag = True
            active = data['active']
            if active:
                active = 1
            else:
                active = 0
        else:
            active = 1;
        if ('create_date' in data):
            flag = True
            create_date = data['create_date']
        else:
            date_time = DateTime()
            create_date = date_time.get_now();
        if ('region' in data):
            flag = True
            region = data['region'].encode("utf-8")
        else:
            region = "HCM";
        if ('location' in data):
            flag = True
            location = data['location']
        else:
            location = ""

        if flag:
            new_obj_event = Event(name = name,
                location = location,
                region = region,
                start_date = start_date,
                end_date = end_date,
                create_date = create_date,
                active = active
                )
            new_obj_event.save()
            agrs["detail"] = "Successfully added event: %s"%(name)
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=202)
        else:
            agrs["detail"] = "Invalid data input!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        return HttpResponse(status=400)

    @csrf_exempt
    def standby(self, request):
        args = {}
        date_time = DateTime()
        now = date_time.get_now()
        standby_list = Event.objects.filter(
            active = 1,
            end_date__gt = now
            )
        if standby_list:
            args_standby_list=[]
            for event in standby_list:
                args_standby_list.append(Event().parse_object_as_json_fortmat(event))
            args["detail"] = "OK"
            args["event_standby_list"] = args_standby_list
        else:
            args["detail"] = "Event is empty"
        data = json.dumps(args)
        return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)

class EventDetail:
    """
    Retrieve, update or delete a event instance.
    """
    @csrf_exempt
    def routing(self, request, pk):
        if request.method == "GET":
            return self.get(request, pk)
        elif request.method == "PUT":
            return self.put(request, pk)
        elif request.method == "DELETE":
            return self.delete(request, pk)

    @csrf_exempt
    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return None

    @csrf_exempt
    def get(self, request, pk):
        args = {}
        event = self.get_object(pk)
        if event:
            args_event = []
            args_event.append(Event().parse_object_as_json_fortmat(event))
            args["detail"] = 'OK'
            args['event'] = args_event
        else:
            args["detail"] = 'Not found.'
        data = json.dumps(args)
        return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)

    @csrf_exempt
    def put(self, request, pk):
        agrs={}
        event = self.get_object(pk)
        if not event:
            args["detail"] = 'Event ID not found.'
            data = json.dumps(args)
            return HttpResponse(data, content_type='application/json', status=203)
        try:
            data = json.loads(request.body)
        except Exception as e:
            agrs["detail"] = "No data input found!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        flag = False
        if ('end_date' in data):
            flag = True
            end_date = data['end_date']
            date_time = DateTime()
            end_date = date_time.conver_human_creadeble_2_unix_timetamp_local(end_date)
            event.end_date = end_date
        if ('name' in data):
            flag = True
            name = data['name'].encode("utf-8")
            event.name = name
        else:
            agrs["detail"] = "Name not empty!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        if ('start_date' in data):
            flag = True
            start_date = data['start_date']
            date_time = DateTime()
            start_date = date_time.conver_human_creadeble_2_unix_timetamp_local(start_date)
            event.start_date = start_date
        if ('active' in data):
            flag = True
            active = data['active']
            if active:
                active = 1
            else:
                active = 0
            event.active = active
        if ('region' in data):
            flag = True
            region = data['region'].encode("utf-8")
            event.region = region
        if ('location' in data):
            flag = True
            location = data['location']
            event.location = location
        if flag:
            event.save()
            agrs["detail"] = "Successfully edited event: %s"%(name)
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=202)
        else:
            agrs["detail"] = "Invalid data input!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        return HttpResponse(status=400)

    @csrf_exempt
    def delete(self, request, pk):
        agrs={}
        event = self.get_object(pk)
        if not event:
            args["detail"] = 'Event ID not found.'
            data = json.dumps(args)
            return HttpResponse(data, content_type='application/json', status=203)
        event.delete()
        return HttpResponse(status=204)

#######################################################################
#                                                                     #
#------------------------------ENCODER--------------------------------#
#                                                                     #
#######################################################################
class EncoderList:
    """
    List all snippets, or create a new encoder.
    """
    @csrf_exempt
    def routing(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login')
        if request.method == "GET":
            return self.get(request)
        elif request.method == "POST":
            return self.post(request)

    @csrf_exempt
    def get(self, request):
        args = {}
        try:
            encoder_list = Encoder.objects.all()
        except Exception as e:
            args["detail"] = str(e)
            data = json.dumps(args)
            return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)
        if encoder_list:
            args_encoder_list=[]
            for encoder in encoder_list:
                args_encoder_list.append(Encoder().parse_object_as_json_fortmat(encoder))
            args["detail"] = "OK"
            args["encoder_list"] = args_encoder_list
        else:
            args["detail"] = "encoder is empty"
        data = json.dumps(args)
        return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)

    @csrf_exempt
    def post(self, request):
        agrs={}
        try:
            data = json.loads(request.body)
        except Exception as e:
            agrs["detail"] = "No data input found!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        flag = False
        if ('name' in data):
            flag = True
            name = data['name'].encode("utf-8")
        else:
            agrs["detail"] = "Name not empty!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        if ('ip_monitor' in data):
            flag = True
            ip_monitor = data['ip_monitor']
        else:
            agrs["detail"] = "Ip monitor not empty!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        if ('active' in data):
            flag = True
            active = data['active']
        else:
            active = 0
        if ('source_main' in data):
            flag = True
            source_main = data['source_main']
        else:
            source_main = "";
        if ('source_backup' in data):
            flag = True
            source_backup = data['source_backup']
        else:
            source_backup = ""

        if flag:
            new_obj_event = Encoder(name = name,
                ip_monitor = ip_monitor,
                source_main = source_main,
                source_backup = source_backup,
                active = active
                )
            new_obj_event.save()
            agrs["detail"] = "Successfully added encoder: %s"%(name)
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=202)
        else:
            agrs["detail"] = "Invalid data input!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        return HttpResponse(status=400)

    @csrf_exempt
    def standby(self, request):
        args = {}
        date_time = DateTime()
        now = date_time.get_now()
        standby_list = Encoder.objects.filter(
            active = 1
            )
        if standby_list:
            args_standby_list=[]
            for encoder in standby_list:
                args_standby_list.append(Encoder().parse_object_as_json_fortmat(encoder))
            args["detail"] = "OK"
            args["encoder_standby_list"] = args_standby_list
        else:
            args["detail"] = "Encoder is empty"
        data = json.dumps(args)
        return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)

class EncoderDetail:
    """
    Retrieve, update or delete a encoder instance.
    """
    @csrf_exempt
    def routing(self, request, pk):
        if request.method == "GET":
            return self.get(request, pk)
        elif request.method == "PUT":
            return self.put(request, pk)
        elif request.method == "DELETE":
            return self.delete(request, pk)

    @csrf_exempt
    def get_object(self, pk):
        try:
            return Encoder.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return None

    @csrf_exempt
    def get(self, request, pk):
        args = {}
        encoder = self.get_object(pk)
        if encoder:
            args_encoder = []
            args_encoder.append(Encoder().parse_object_as_json_fortmat(encoder))
            args["detail"] = 'OK'
            args['encoder'] = args_encoder
        else:
            args["detail"] = 'Not found.'
        data = json.dumps(args)
        return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)

    @csrf_exempt
    def put(self, request, pk):
        agrs={}
        encoder = self.get_object(pk)
        if not encoder:
            args["detail"] = 'Encoder ID not found.'
            data = json.dumps(args)
            return HttpResponse(data, content_type='application/json', status=203)
        try:
            data = json.loads(request.body)
        except Exception as e:
            agrs["detail"] = "No data input found!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        flag = False
        if ('name' in data):
            flag = True
            name = data['name'].encode("utf-8")
            encoder.name = name
        else:
            agrs["detail"] = "Name not empty!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        if ('ip_monitor' in data):
            flag = True
            ip_monitor = data['ip_monitor']
            encoder.ip_monitor = ip_monitor
        if ('active' in data):
            flag = True
            active = data['active']
            if active:
                active = 1
            else:
                active = 0
            encoder.active = active
        if ('source_main' in data):
            flag = True
            source_main = data['source_main']
            encoder.source_main = source_main
        if ('source_backup' in data):
            flag = True
            source_backup = data['source_backup']
            encoder.source_backup = source_backup
        if flag:
            encoder.save()
            agrs["detail"] = "Successfully edited encoder: %s"%(name)
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=202)
        else:
            agrs["detail"] = "Invalid data input!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        return HttpResponse(status=400)

    @csrf_exempt
    def delete(self, request, pk):
        agrs={}
        encoder = self.get_object(pk)
        if not encoder:
            args["detail"] = 'Encoder ID not found.'
            data = json.dumps(args)
            return HttpResponse(data, content_type='application/json', status=203)
        encoder.delete()
        return HttpResponse(status=204)

#######################################################################
#                                                                     #
#------------------------------SERVICECHECK---------------------------#
#                                                                     #
#######################################################################
class ServiceCheckList:
    """
    List all snippets, or create a new encoder.
    """
    @csrf_exempt
    def routing(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login')
        if request.method == "GET":
            return self.get(request)
        elif request.method == "POST":
            return self.post(request)

    @csrf_exempt
    def get(self, request):
        args = {}
        try:
            service_check_list = ServiceCheck.objects.all()
        except Exception as e:
            args["detail"] = str(e)
            data = json.dumps(args)
            return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)
        if service_check_list:
            args_service_check_list=[]
            for service_check in service_check_list:
                args_service_check_list.append(ServiceCheck().parse_object_as_json_fortmat(service_check))
            args["detail"] = "OK"
            args["service_check_list"] = args_service_check_list
        else:
            args["detail"] = "service_check is empty"
        data = json.dumps(args)
        return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)

    @csrf_exempt
    def post(self, request):
        agrs={}
        try:
            data = json.loads(request.body)
        except Exception as e:
            agrs["detail"] = "No data input found!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        flag = False
        if ('name' in data):
            flag = True
            name = data['name'].encode("utf-8")
        else:
            agrs["detail"] = "Name not empty!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        if ('active' in data):
            flag = True
            active = data['active']
        else:
            active = 0

        if flag:
            new_obj_service_check = ServiceCheck(name = name,
                active = active
                )
            new_obj_service_check.save()
            agrs["detail"] = "Successfully added service check : %s"%(name)
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=202)
        else:
            agrs["detail"] = "Invalid data input!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        return HttpResponse(status=400)

    @csrf_exempt
    def standby(self, request):
        args = {}
        date_time = DateTime()
        now = date_time.get_now()
        standby_list = ServiceCheck.objects.filter(
            active = 1
            )
        if standby_list:
            args_standby_list=[]
            for service in standby_list:
                args_standby_list.append(ServiceCheck().parse_object_as_json_fortmat(service))
            args["detail"] = "OK"
            args["service_check_standby_list"] = args_standby_list
        else:
            args["detail"] = "Service is empty"
        data = json.dumps(args)
        return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)

class ServiceCheckDetail:
    """
    Retrieve, update or delete a service check instance.
    """
    @csrf_exempt
    def routing(self, request, pk):
        if request.method == "GET":
            return self.get(request, pk)
        elif request.method == "PUT":
            return self.put(request, pk)
        elif request.method == "DELETE":
            return self.delete(request, pk)

    @csrf_exempt
    def get_object(self, pk):
        try:
            return ServiceCheck.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return None

    @csrf_exempt
    def get(self, request, pk):
        args = {}
        service_check = self.get_object(pk)
        if service_check:
            args_service_check = []
            args_service_check.append(ServiceCheck().parse_object_as_json_fortmat(service_check))
            args["detail"] = 'OK'
            args['service_check'] = args_service_check
        else:
            args["detail"] = 'Not found.'
        data = json.dumps(args)
        return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)

    @csrf_exempt
    def put(self, request, pk):
        agrs={}
        service_check = self.get_object(pk)
        if not service_check:
            args["detail"] = 'Service check ID not found.'
            data = json.dumps(args)
            return HttpResponse(data, content_type='application/json', status=203)
        try:
            data = json.loads(request.body)
        except Exception as e:
            agrs["detail"] = "No data input found!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        flag = False
        if ('name' in data):
            flag = True
            name = data['name'].encode("utf-8")
            service_check.name = name
        else:
            agrs["detail"] = "Name not empty!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        if ('active' in data):
            flag = True
            active = data['active']
            if active:
                active = 1
            else:
                active = 0
            service_check.active = active
        if flag:
            service_check.save()
            agrs["detail"] = "Successfully edited service check: %s"%(name)
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=202)
        else:
            agrs["detail"] = "Invalid data input!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        return HttpResponse(status=400)

    @csrf_exempt
    def delete(self, request, pk):
        agrs={}
        service_check = self.get_object(pk)
        if not service_check:
            args["detail"] = 'Service check ID not found.'
            data = json.dumps(args)
            return HttpResponse(data, content_type='application/json', status=203)
        service_check.delete()
        return HttpResponse(status=204)

#######################################################################
#                                                                     #
#-----------------------------EVENTMONITOR----------------------------#
#                                                                     #
#######################################################################
class EventMonitorList:
    """
    List all snippets, or create a new encoder.
    """
    @csrf_exempt
    def routing(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login')
        if request.method == "GET":
            return self.get(request)
        elif request.method == "POST":
            return self.post(request)

    @csrf_exempt
    def get(self, request):
        args = {}
        try:
            event_monitor_list = EventMonitor.objects.all()
        except Exception as e:
            args["detail"] = str(e)
            data = json.dumps(args)
            return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)
        if event_monitor_list:
            args_event_monitor_list=[]
            for event_monitor in event_monitor_list:
                args_event_monitor_list.append(EventMonitor().parse_object_as_json_fortmat(event_monitor))
            args["detail"] = "OK"
            args["event_monitor_list"] = args_event_monitor_list
        else:
            args["detail"] = "service_check is empty"
        data = json.dumps(args)
        return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)

    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        flag = False
        #status
        if ('status' in data):
            status = data['status']
            flag = True
        else:
            status = None
        #pid
        if ('pid' in data):
            pid = data['pid']
            flag = True
        else:
            pid = None
        if ('active' in data):
            active = data['active']
            if active:
                active = 1
            else:
                active = 0
            flag = True
        else:
            active = 1

        if ('service_check_id' in data):
            service_check_id = data['service_check_id']
            flag = True
        else:
            service_check_id = None
        if ('descr' in data):
            descr = data['descr']
            flag = True
        else:
            descr = ""
        if ('event_id' in data):
            event_id = data['event_id']
            flag = True
        else:
            event_id = None
        if ('encoder_id' in data):
            encoder_id = data['encoder_id']
            flag = True
        else:
            encoder_id = None
        if ('last_update' in data):
            last_update = data['last_update']
            flag = True
        else:
            date_time = DateTime()
            now = date_time.get_now()
            last_update = now
        if flag:
            event_monitor = EventMonitor(
                 pid = pid,
                 event_id = event_id,
                 encoder_id = encoder_id,
                 service_check_id = service_check_id,
                 status = status,
                 last_update = last_update,
                 active = active,
                 descr = descr
                )
            event_monitor.save()
            return HttpResponse(status=202)
        return HttpResponse(status=400)

    @csrf_exempt
    def standby(self, request):
        pass

class EventMonitorDetail:
    """
    Retrieve, update or delete a encoder instance.
    """
    @csrf_exempt
    def routing(self, request, pk):
        if request.method == "GET":
            return self.get(request, pk)
        elif request.method == "PUT":
            return self.put(request, pk)
        elif request.method == "DELETE":
            return self.delete(request, pk)

    @csrf_exempt
    def get_object(self, pk):
        try:
            return EventMonitor.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return None

    @csrf_exempt
    def get(self, request, pk):
        args = {}
        event_monitor = self.get_object(pk)
        if event_monitor:
            args_event_monitor = []
            args_event_monitor.append(EventMonitor().parse_object_as_json_fortmat(event_monitor))
            args["detail"] = 'OK'
            args['event_monitor'] = args_event_monitor
        else:
            args["detail"] = 'Not found.'
        data = json.dumps(args)
        return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)

    @csrf_exempt
    def put(self, request, pk):
        try:
            data = json.loads(request.body)
        except Exception as e:
            agrs["detail"] = "No data input found!"
            messages = json.dumps(agrs)
        if data:
            event_monitor = self.get_object(pk)
            flag = False
            #status
            if ('status' in data):
                event_monitor.status = data['status']
                flag = True
            #pid
            if ('pid' in data):
                event_monitor.pid = data['pid']
                flag = True
            if ('active' in data):
                active = 1 if data['active'] else 0
                event_monitor.active = data['active']
                flag = True
            if ('service_check_id' in data):
                event_monitor.service_check_id = data['service_check_id']
                flag = True
            if ('descr' in data):
                event_monitor.descr = data['descr']
                flag = True
            if ('event_id' in data):
                event_monitor.event_id = data['event_id']
                flag = True
            if ('encoder_id' in data):
                event_monitor.encoder_id = data['encoder_id']
                flag = True
            if ('last_update' in data):
                event_monitor.last_update = data['last_update']
                flag = True
            else:
                date_time = DateTime()
                now = date_time.get_now()
                event_monitor.last_update = now
            if flag:
                event_monitor.save()
                return HttpResponse(status=202)
        return HttpResponse(status=400)

    @csrf_exempt
    def delete(self, request, pk):
        print "aa"
        agrs={}
        event_monitor = self.get_object(pk)
        if not event_monitor:
            args["detail"] = 'Event monitor ID not found.'
            data = json.dumps(args)
            return HttpResponse(data, content_type='application/json', status=203)
        event_monitor.delete()
        return HttpResponse(status=204)

class MonitorList:
    @csrf_exempt
    def routing(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login')
        if request.method == "GET":
            return self.get(request)

    @csrf_exempt
    def __init__(self):
        self.event = EventBLL()

    @csrf_exempt
    def get(self, request):
        args = {}
        monitor_list = self.event.get_event_monitor_list()
        args['monitor_list'] = monitor_list
        data = json.dumps(args)
        return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)

    @csrf_exempt
    def get_running_monitor_list(self, request):
        running_monitor_list = self.event.get_running_event_monitor_list()
        data = json.dumps(running_monitor_list)
        return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)

    @csrf_exempt
    def get_waiting_monitor_list(self, request):
        running_monitor_list = self.event.get_waiting_event_monitor_list()
        data = json.dumps(running_monitor_list)
        return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)

    @csrf_exempt
    def get_completed_monitor_list(self, request):
        running_monitor_list = self.event.get_completed_event_monitor_list()
        data = json.dumps(running_monitor_list)
        return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)

class MonitorDetail:
    @csrf_exempt
    def routing(self, request, event_monitor_id):
        if request.method == "GET":
            return self.get(request, event_monitor_id)

    @csrf_exempt
    def __init__(self):
        self.event = EventBLL()

    @csrf_exempt
    def get(self, request, event_monitor_id):
        args = {}
        monitor = self.event.get_event_monitor(event_monitor_id)
        args["monitor"] = monitor
        data = json.dumps(args)
        return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)


class Template:
    @csrf_exempt
    def event(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login')
        user = user_info(request)
        return render_to_response("event/event.html", user)

    @csrf_exempt
    def encoder(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login')
        user = user_info(request)
        return render_to_response("event/encoder.html", user)

    @csrf_exempt
    def service(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login')
        user = user_info(request)
        return render_to_response("event/service.html", user)

    @csrf_exempt
    def monitor(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login')
        user = user_info(request)
        return render_to_response("event/monitor.html", user)

    @csrf_exempt
    def monitor_add(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login')
        user = user_info(request)
        return render_to_response("event/monitor/add/add.html", user)

    @csrf_exempt
    def monitor_add_step1(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login')
        return render_to_response("event/monitor/add/step1.html")

    @csrf_exempt
    def monitor_add_step2(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login')
        return render_to_response("event/monitor/add/step2.html")

    @csrf_exempt
    def monitor_add_step3(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login')
        return render_to_response("event/monitor/add/step3.html")

    @csrf_exempt
    def monitor_edit(self, request, event_monitor_id):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login')
        try:
            monitor = EventMonitor.objects.get(pk=event_monitor_id)
        except ObjectDoesNotExist:
            monitor = None
        if monitor:
            print monitor
            args={}
            args['monitor'] = monitor
            return render_to_response("event/monitor/edit/edit.html", args)
        return self.monitor()

    @csrf_exempt
    def monitor_edit_step1(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login')
        return render_to_response("event/monitor/edit/step1.html")

    @csrf_exempt
    def monitor_edit_step2(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login')
        return render_to_response("event/monitor/edit/step2.html")

    @csrf_exempt
    def monitor_edit_step3(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login')
        return render_to_response("event/monitor/edit/step3.html")


