# coding: utf8
import json
from django.db.models import Q
from django.db import transaction, connection,IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse 
from datetime import timedelta, datetime,date
from channel.utils import *
from log.models import *
from setting.customSQL import *
from agent.models import *
from agent.utils import *
from log.utils import *
from django.core.cache import cache
from calendar import month
import unicodedata
#Phan trang
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.user_info import *
import time

# Create your views here.

def agent_view(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	user = user_info(request)
	return render_to_response('agent/agent.html', user)

def agent_view_json(request):
	cmd = "SELECT id,name,ip,descr,thread,cpu,mem,disk,from_unixtime(last_update)as last_update,active FROM agent ORDER BY id DESC"
	agent_list = my_custom_sql(cmd)
	if len(agent_list) < 1:
		return HttpResponse('<script>alert("No agent exist!")</script>')
	args = []
	for i in agent_list:
		args.append({ 'id'			: i[0] if i[0] else None,
					'name'			: i[1] if i[1] else "",
					'ip'			: i[2] if i[2] else "",
					'descr'			: i[3] if i[3] else "",
					'thread'		: i[4] if i[4] else 0,
					'cpu'			: i[5] if i[5] else 0,
					'ram'			: i[6] if i[6] else 0,
					'disk'			: i[7] if i[7] else 0,
					'active'		: i[9] if i[9] else 0,
					'last_update'	: str(i[8]) if i[8] else "",
					})
	json_data = json.dumps({"agents": args})
	return HttpResponse(json_data, content_type='application/json', status=200)

@csrf_exempt
def agent_control(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	if not request.user.is_staff:
		return HttpResponseRedirect('/agent/')
	if request.method == 'POST':
		if 'btnadd' in request.POST:
			return render_to_response('agent/add.html')
		if 'btndelete' in request.POST:
			agent_id_delete = request.POST.getlist('SellectAgent', '')
			for agent in agent_id_delete:
				obj_agent = Agent.objects.get(pk = int(agent))
				msg = "user %s deleted host %s ip %s"%(request.user.username, obj_agent.name, obj_agent.ip)
				insert_log(obj_agent.name, "delete", "", msg)
				obj_agent.delete()
			return HttpResponseRedirect('/agent/')
		if 'btnactive' in request.POST:
			agent_id_active = request.POST.getlist('SellectAgent', '')
			for agent in agent_id_active:
				obj_agent = Agent.objects.get(pk = int(agent))
				obj_agent.active = 1
				obj_agent.save()
				msg = "user %s change status deactive to active on host %s ip %s"%(request.user.username, obj_agent.name, obj_agent.ip)
				insert_log(obj_agent.name, "status", "", msg)
			return HttpResponseRedirect('/agent/')
		if 'btndeactive' in request.POST:
			agent_id_deactive = request.POST.getlist('SellectAgent', '')
			for agent in agent_id_deactive:
				obj_agent = Agent.objects.get(pk = int(agent))
				obj_agent.active = 0
				obj_agent.save()
				msg = "user %s change status deactive to active on host %s ip %s"%(request.user.username, obj_agent.name, obj_agent.ip)
				insert_log(str(obj_agent.name), "status", "", msg)
			return HttpResponseRedirect('/agent/')

@csrf_exempt
def add_agent(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	if not request.user.is_staff:
		return HttpResponseRedirect('/agent/')
	if request.method == 'POST':
		if 'save' in request.POST:
			name = request.POST.get('name', '').strip()#Cut space
			ip = request.POST.get('ip', '').strip()#Cut space
			descr = request.POST.get('descr', '').strip()#Cut space
			thread = int(request.POST.get('thread','').strip())
			active = request.POST.get('active', '')
			if active == 'yes':
				active = 1
			elif active == 'no':
				active = 0
			last_update = int(time.time())
			new_obj_agent = Agent(name=name, ip=ip, descr=descr, thread=thread, active=active, cpu=0, mem=0, disk=0, last_update=last_update)
			new_obj_agent.save()
			msg = "user %s added host %s ip %s"%(request.user.username, name, ip)
			insert_log(name, "add", "", msg)
			return HttpResponseRedirect('/agent/')
	return render_to_response('agent/add.html')

@csrf_exempt
def edit_agent(request, agent_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	if not request.user.is_staff:
		return HttpResponseRedirect('/agent/')
	if request.method == 'POST':
		if 'save' in request.POST:
			obj_agent = Agent.objects.get(pk = int(agent_id))
			obj_agent.name = request.POST.get('name', '').strip()#Cut space
			obj_agent.ip = request.POST.get('ip', '').strip()#Cut space
			obj_agent.descr = request.POST.get('descr', '').strip()#Cut space
			obj_agent.thread = request.POST.get('thread','').strip()
			active = request.POST.get('active', '')
			if active == 'on':
				obj_agent.active = 1
			elif active == 'no':
				obj_agent.active = 0
			obj_agent.save()
			msg = "user %s edited host %s ip %s"%(request.user.username, request.POST.get('name', ''), request.POST.get('ip', ''))
			insert_log(obj_agent.name, "edit", "", msg)
			return HttpResponseRedirect('/agent/')
	agent_data = get_agent_data_by_id(agent_id)
	args = {}
	args['agent_data'] = agent_data
	return render_to_response('agent/edit.html', args)
#
#------------------------------------------------------------------------------------------------------------------
#transcode
#--------------------------------------------------------------------------------------------------------------------
#

def profile_agent_view(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	user = user_info(request)
	return render_to_response('agent/profile_agent/profile_agent.html',user)

def  profile_agent_view_json(request):
	cmd = "SELECT pa.id,channel.name as channel_name, profile.type as profile_type,profile.ip as profile_ip, agent.id as agent_id, agent.ip as agent_ip,agent.name as agent_name,pa.status,pa.analyzer_status, pa.dropframe, pa.dropframe_threshold,pa.discontinuity,pa.discontinuity_threshold,pa.check, pa.monitor,pa.analyzer,from_unixtime(pa.last_update) as last_update FROM profile_agent as pa,profile,channel,agent where pa.profile_id=profile.id and pa.agent_id=agent.id and profile.channel_id=channel.id ORDER BY pa.status"
	profile_agent_list = my_custom_sql(cmd)
	if len(profile_agent_list) <1:
		return HttpResponse('<script>alert("No profile agent exist!")</script>')
	args = []
	for i in profile_agent_list:
		args.append({ 'id'			: i[0] if i[0] else None,
					'channel_name'	: i[1] if i[1] else "",
					'type'			: i[2] if i[2] else "",
					'ip'			: i[3] if i[3] else "",
					'agent_name'	: i[6] if i[6] else "",
					'status'		: i[7] if i[7] else 0,
					'status_anylyzer': i[8] if i[8] else 0,
					'drop_frame'	: i[9] if i[9] else 0,
					'dfLim'			: i[10] if i[1] else 0,
					'cceror'		: i[11] if i[1] else 0,
					'ccelim'		: i[12] if i[1] else 0,
					'check'			: i[13] if i[13] else 0,
					'monitor'		: i[14] if i[14] else 0,
					'anylyzer'		: i[15] if i[15] else 0,
					'last_update'	: str(i[16]) if i[16] else "",
					})
	json_data = json.dumps({"profile_agent": args})
	return HttpResponse(json_data, content_type='application/json', status=200)

@csrf_exempt
def profile_agent_control(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	if not request.user.is_staff:
		return HttpResponseRedirect('/agent/monitor')
	if request.method == 'POST':
		if 'btnadd' in request.POST:
			return render_to_response('agent/profile_agent/add.html')
		if 'btndelete' in request.POST:
			profile_agent_id_delete = request.POST.getlist('SellectProfileAgent', '')
			for profile_agent in profile_agent_id_delete:
				obj_profile_agent = ProfileAgent.objects.get(pk = int(profile_agent))
				msg = "user %s deleted monitor profile_id %s on host_id %s"%(request.user.username, obj_profile_agent.profile_id, profile_agent)
				insert_log('monitor', "delete", "", msg)
				obj_profile_agent.delete()
			return HttpResponseRedirect('/agent/monitor/')
		if 'btnmonitor' in request.POST:
			profile_agent_id_active = request.POST.getlist('SellectProfileAgent', '')
			for profile_agent in profile_agent_id_active:
				obj_profile_agent = ProfileAgent.objects.get(pk = int(profile_agent))
				obj_profile_agent.monitor = 1
				msg = "user %s change monitor to active on profile_agent_id %s"%(request.user.username, obj_profile_agent.id)
				insert_log('monitor', "monitor status", "", msg)
				obj_profile_agent.save()
			return HttpResponseRedirect('/agent/monitor/')
		if 'btnnotmonitor' in request.POST:
			profile_agent_id_deactive = request.POST.getlist('SellectProfileAgent', '')
			for profile_agent in profile_agent_id_deactive:
				obj_profile_agent = ProfileAgent.objects.get(pk = int(profile_agent))
				obj_profile_agent.monitor = 0
				msg = "user %s change monitor to deactive on profile_agent_id %s"%(request.user.username, obj_profile_agent.id)
				insert_log('monitor', "monitor status", "", msg)
				obj_profile_agent.save()
			return HttpResponseRedirect('/agent/monitor/')
		if 'btnanalyzer' in request.POST:
			profile_agent_id_active = request.POST.getlist('SellectProfileAgent', '')
			for profile_agent in profile_agent_id_active:
				obj_profile_agent = ProfileAgent.objects.get(pk = int(profile_agent))
				obj_profile_agent.analyzer = 1
				msg = "user %s change analyzer to active on profile_agent_id %s"%(request.user.username, obj_profile_agent.id)
				insert_log('monitor', "analyzer status", "", msg)
				obj_profile_agent.save()
			return HttpResponseRedirect('/agent/monitor/')
		if 'btnnotanalyzer' in request.POST:
			profile_agent_id_deactive = request.POST.getlist('SellectProfileAgent', '')
			for profile_agent in profile_agent_id_deactive:
				obj_profile_agent = ProfileAgent.objects.get(pk = int(profile_agent))
				obj_profile_agent.analyzer = 0
				msg = "user %s change analyzer to deactive on profile_agent_id %s"%(request.user.username, obj_profile_agent.id)
				insert_log('monitor', "analyzer status", "", msg)
				obj_profile_agent.save()
			return HttpResponseRedirect('/agent/monitor/')

@csrf_exempt
def add_profile_agent(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	if not request.user.is_staff:
		return HttpResponseRedirect('/agent/monitor')
	if request.method == 'POST':
		if 'save' in request.POST:
			profiles = request.POST.getlist('SellectProfile','')
			agents = request.POST.getlist('SellectAgent','')
			monitor = int(request.POST.get('monitor', ''))
			anylyzer = int(request.POST.get('analyzer', ''))
			dropframe = int(request.POST.get('dropframe', ''))
			cceror = int(request.POST.get('cceror', ''))
			last_update = int(time.time())
			if len(profiles) * len(agents) > 500:
				return HttpResponse('<script>alert("Over load!")</script>')
			for agent_id in agents:
				print int(agent_id)
				for profile_id in profiles:
					print(profile_id)
					#Check monitoring exist
					cmd = "select id from profile_agent where profile_id='" + profile_id + "' and agent_id='" + agent_id + "';"
					resuft  = my_custom_sql(cmd)
					print resuft
					if len(resuft) < 1:
						obj_profile_agent = ProfileAgent(profile_id = int(profile_id), agent_id = int(agent_id), status = 1, analyzer_status = 1, dropframe = 0, dropframe_threshold = dropframe, discontinuity = 0, discontinuity_threshold = cceror, check = 0, video = 1, audio = 1, monitor = 1, analyzer = anylyzer, last_update = last_update)
						msg = "user %s added monitor profile_id %s on host %s"%(request.user.username, profile_id, agent_id)
						insert_log('monitor', "add", "", msg)
						obj_profile_agent.save()
			return HttpResponseRedirect('/agent/monitor/')

			#return HttpResponseRedirect('/agent/')
	return render_to_response('agent/profile_agent/add.html')

@csrf_exempt
def edit_profile_agent(request, profile_agent_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	if not request.user.is_staff:
		return HttpResponseRedirect('/agent/monitor')
	if request.method == 'POST':
		if 'save' in request.POST:
			profile_id = request.POST.get('profile_id', '').strip()#Cut space
			agent_id = request.POST.get('agent_id', '')#Cut space
			monitor = int(request.POST.get('monitor', ''))#Cut space
			analyzer = int(request.POST.get('analyzer',''))
			dropframe_limit = request.POST.get('dropframe', '')
			cceror = request.POST.get('cceror', '')
			if not dropframe_limit.isdigit() or not dropframe_limit.isdigit():
				return HttpResponse("Please input number!")
			obj_profile_agent = ProfileAgent.objects.get(pk = int(profile_agent_id))
			obj_profile_agent.agent_id= int(agent_id)
			obj_profile_agent.monitor = int(monitor)
			obj_profile_agent.analyzer= int(analyzer)
			obj_profile_agent.dropframe_threshold= int(dropframe_limit)
			obj_profile_agent.discontinuity_threshold = int(cceror)
			obj_profile_agent.last_update = int(time.time())
			msg = "user %s edited profile_agent_id %s"%(request.user.username, profile_agent_id)
			insert_log('monitor', "edit", "", msg)
			if profile_id.isdigit():
				obj_profile_agent.profile_id = int(profile_id)
			obj_profile_agent.save()
			return HttpResponseRedirect('/agent/monitor/')
	args={}
	args['profile_agent_id'] = profile_agent_id
	return render_to_response('agent/profile_agent/edit.html', args)

def  profile_agent_by_item_json(request, profile_agent_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	cmd = "SELECT pa.id,channel.name as channel_name, profile.type as profile_type,profile.ip as profile_ip, agent.id as agent_id, agent.name as agent_name,pa.analyzer_status, pa.dropframe_threshold,pa.discontinuity_threshold, pa.monitor,pa.analyzer, profile.id as profile_id FROM profile_agent as pa,profile,channel,agent where pa.id = " + str(profile_agent_id) + " and pa.profile_id=profile.id and pa.agent_id=agent.id and profile.channel_id=channel.id"
	profile_agent_list = my_custom_sql(cmd)
	if len(profile_agent_list) <1:
		return HttpResponse('<script>alert("No profile agent exist!")</script>')
	args = []
	for i in profile_agent_list:
		args.append({ 'id'			: i[0] if i[0] else None,
					'channel_name'	: i[1] if i[1] else "",
					'type'			: i[2] if i[2] else "",
					'ip'			: i[3] if i[3] else "",
					'agent_id'		: i[4] if i[4] else "",
					'agent_name'	: i[5] if i[5] else "",
					'status_anylyzer': i[6] if i[6] else 0,
					'dropframe_limit'	: i[7] if i[7] else 0,
					'ccerror_limit'		: i[8] if i[8] else 0,
					'monitor'		: i[9] if i[9] else 0,
					'anylyzer'		: i[10] if i[10] else 0,
					})
	json_data = json.dumps({"profile_agent_item": args})
	return HttpResponse(json_data, content_type='application/json', status=200)
