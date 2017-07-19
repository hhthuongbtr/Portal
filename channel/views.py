# coding: utf8
import json
from django.db.models import Q
from django.db import transaction, connection,IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse 
from django.views.decorators.csrf import ensure_csrf_cookie
from datetime import timedelta, datetime,date
from setting.customSQL import *
from channel.models import *
from channel.utils import *
from log.models import *
from log.utils import *
from agent.models import *
from django.core.cache import cache
from calendar import month
import unicodedata
#Phan trang
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.user_info import *
import time

# Create your views here.
def channel_list(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	user = user_info(request)
	return render_to_response('channel/channel.html', user)

def channel_json(request):
	#cmd = "SELECT * FROM channel ORDER BY name ASC LIMIT " + str((page-1)*record_per_page) +"," + str(record_per_page)
	cmd = "SELECT * FROM channel ORDER BY name ASC"
	list_channel = my_custom_sql(cmd)
	print len(list_channel)
	args = []
	for i in list_channel:
		args.append({ 'id'		: i[0] if i[0] else None,
					'name'		: i[1] if i[1] else None,
					'descr'		: i[2] if i[2] else None,
					'active'	: i[4] if i[4] else 0,
					})
	json_data = json.dumps({"channels": args})
	return HttpResponse(json_data, content_type='application/json', status=200)

@csrf_exempt
def channel_control(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	if not request.user.is_staff:
		return HttpResponseRedirect('/channel')
	if request.method == 'POST':
		if 'btnadd' in request.POST:
			return render_to_response('channel/add.html')
		if 'btndelete' in request.POST:
			channel_id_deletes = request.POST.getlist('sellectChannel', '')
			suscess =0
			err = 0
			for channel in channel_id_deletes:
				if check_channel_exist_profile(channel) == False:
					cnl = Channel.objects.get(pk = int(channel))
					msg = "user %s delete channel_id %s name %s"%(request.user.username, channel, cnl.name)
					insert_log('channel', "delete", "", msg)
					cnl.delete()
					suscess +=1
				else:
					err +=1
			if err > 0:
				return HttpResponse('<script>alert(" Khong the xoa %s channel co profile dang chay, %s channel da xoa!")</script>' %(err, suscess))
			else:
				return HttpResponseRedirect('/channel/')
		if 'btnactive' in request.POST:
			channel_id_actives = request.POST.getlist('sellectChannel', '')
			for channel in channel_id_actives:
				cnl = Channel.objects.get(pk = int(channel))
				cnl.active = 1
				msg = "user %s change status to active on channel_id %s name %s"%(request.user.username, channel, cnl.name)
				insert_log('channel', "status", "", msg)
				cnl.save()
			return HttpResponseRedirect('/channel/')
		if 'btndeactive' in request.POST:
			channel_id_deactives = request.POST.getlist('sellectChannel', '')
			for channel in channel_id_deactives:
				cnl = Channel.objects.get(pk = int(channel))
				cnl.active = 0
				msg = "user %s change status to deactive on channel_id %s name %s"%(request.user.username, channel, cnl.name)
				insert_log('channel', "status", "", msg)
				cnl.save()
			return HttpResponseRedirect('/channel/')


@csrf_exempt
def edit_channel(request, channel_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	if not request.user.is_staff:
		return HttpResponseRedirect('/channel')
	if request.method == 'POST':
		if 'save' in request.POST:
			cnl = Channel.objects.get(pk = int(channel_id))
			cnl.name = request.POST.get('name', '').strip()#Cut space
			cnl.descr = request.POST.get('descr', '').strip()#Cut space
			print request.POST.get('descr', '')
			atve = request.POST.get('active', '')
			print atve
			if atve == "on":
				cnl.active = 1
			else:
				cnl.active = 0
			msg = "user %s edit channel_id %s name %s"%(request.user.username, cnl.id, cnl.name)
			insert_log('channel', "edit", "", msg)
			cnl.save()
			return HttpResponseRedirect('/channel/')
	channel_data = get_channel_by_id(channel_id)
	args = {}
	args['channel_data'] = channel_data
	return render_to_response('channel/edit.html', args)

@csrf_exempt
def add_channel(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	if not request.user.is_staff:
		return HttpResponseRedirect('/channel')
	if request.method == 'POST':
		if 'save' in request.POST:
			name = request.POST.get('name', '').strip()#Cut space
			descr = request.POST.get('descr', '').strip()#Cut space
			atve = request.POST.get('active', '')
			if atve == "on":
				active = 1
			else:
				active = 0
			group_id = 0
			obj_channel = Channel(name=name, descr = descr, group_id=group_id, active=active)
			msg = "user %s add new channel name %s"%(request.user.username, name)
			insert_log('channel', "add", "", msg)
			obj_channel.save()
			return HttpResponseRedirect('/channel/')
		else:
			return HttpResponseRedirect('/channel/')
	else:
		return render_to_response('channel/add.html')


"""
------------------------------------------------------------------------------------------------------------------
Channel Group
--------------------------------------------------------------------------------------------------------------------

"""

def channel_group(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	user = user_info(request)
	return render_to_response('channel/group/channel_group.html', user)

def channel_group_json(request):
	#list_group = getDataGroupList()
	group_list = my_custom_sql("SELECT g.id,g.name,count(pg.profile_id) as profile_count FROM `group` as g LEFT JOIN profile_group as pg ON pg.group_id = g.id GROUP BY g.id;")
	args = []
	for i in group_list:
		args.append({ 'id'				: i[0] if i[0] else None,
					'name'				: i[1] if i[1] else None,
					'count_profile'		: i[2] if i[2] else 0,
					})
	json_data = json.dumps({"group": args})
	return HttpResponse(json_data, content_type='application/json', status=200)
@csrf_exempt
def channel_group_control(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	if not request.user.is_staff:
		return HttpResponseRedirect('/channel/group/')
	if request.method == 'POST':
		if 'btnadd' in request.POST:
			return render_to_response('channel/group/add.html')
		if 'btndelete' in request.POST:
			group_id_deletes= request.POST.getlist('sellectgroup', '')
			for group in group_id_deletes:
				obj_group = Group.objects.get(pk = int(group))
				msg = "user %s delete group_id %s name %s"%(request.user.username, group, obj_group.name)
				insert_log('group', "delete", "", msg)
				obj_group.delete()
			return HttpResponseRedirect('/channel/group/')

def group_view(request, group_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	args={}
	args['group_id'] = group_id
	args['id'] = request.user.id
	args['email'] = request.user.email
	args['is_superuser'] = request.user.is_superuser
	args['is_staff'] = 'true' if request.user.is_staff else 'false'
	return render_to_response('channel/group/channel_group_view.html', args)
	
	
def group_view_json(request, group_id):
	cmd = "select profile.id,channel.name as channel_name, profile.ip as profile_ip, profile.type as type, `group`.name as group_name from channel,profile,`group`,profile_group as pg where profile.channel_id=channel.id and pg.profile_id=profile.id and pg.group_id=`group`.id and pg.group_id = %s ORDER BY channel.name,profile.ip;"%(group_id)
	list_profile_of_group = my_custom_sql(cmd)
	args = []
	for profile in list_profile_of_group:
		args.append({'id'			:profile[0] if profile[0] else None,
					'channel_name'	:profile[1] if profile[1] else None,
					'type'			:profile[3] if profile[3] else "",
					'ip'			:profile[2] if profile[2] else "",

			})
	json_data = json.dumps({"channel_profile": args})
	return HttpResponse(json_data, content_type='application/json', status=200)

@csrf_exempt
def edit_group(request, group_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	if not request.user.is_staff:
		return HttpResponseRedirect('/channel/group/')
	if request.method == 'POST':
		if 'save' in request.POST:
			obj_group = Group.objects.get(pk = int(group_id))
			obj_group.name = request.POST.get('name', '').strip()#Cut space
			msg = "user %s edit group_id %s name %s"%(request.user.username, obj_group.id, obj_group.name)
			insert_log('group', "edit", "", msg)
			obj_group.save()
			return HttpResponseRedirect('/channel/group/')
	group_data = get_group_data_by_id(group_id)
	args = {}
	args['group_data'] = group_data
	return render_to_response('channel/group/edit.html', args)

@csrf_exempt
def add_group(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	if not request.user.is_staff:
		return HttpResponseRedirect('/channel/group/')
	if request.method == 'POST':
		if 'save' in request.POST:
			name = request.POST.get('name', '').strip()#Cut space
			obj_group = Group(name=name)
			msg = "user %s addes new group name %s"%(request.user.username, name)
			insert_log('group', "add", "", msg)
			obj_group.save()
			return HttpResponseRedirect('/channel/group/')
		else:
			return HttpResponseRedirect('/channel/group/')
	else:
		return render_to_response('channel/group/add.html')

@csrf_exempt
def channel_group_id_control(request, group_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	if not request.user.is_staff:
		return HttpResponseRedirect('/channel/group/'+str(group_id)+'/')
	if request.method == 'POST':
		if 'btnadd' in request.POST:
			args = {}
			args['group_id'] = group_id
			return render_to_response('channel/group/profile_group/add.html', args)
		if 'btndelete' in request.POST:
			profile_id_delete= request.POST.getlist('sellectProfileOfGroup', '')
			for profile in profile_id_delete:
				cmd = "DELETE FROM `profile_group` WHERE `profile_id` = %s and `group_id` = %s ;"%(profile, group_id)
				my_custom_sql(cmd)
				msg = "user %s remove profile_id %s from group %s"%(request.user.username, profile, group_id)
				insert_log('profile_group', "remove", "", msg)
			return HttpResponseRedirect('/channel/group/'+str(group_id)+'/')

@csrf_exempt
def channel_group_id_add(request, group_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	if not request.user.is_staff:
		return HttpResponseRedirect('/channel/group/'+str(group_id)+'/')
	if request.method == 'POST':
		if 'save' in request.POST:
			profile_id_add= request.POST.getlist('SellectProfile', '')
			for profile in profile_id_add:
				check_exist = my_custom_sql("SELECT * FROM `profile_group` WHERE `profile_id` = %s and `group_id` = %s ;"%(profile, group_id))
				print check_exist
				if len(check_exist) <1:
					obj_profile_group = ProfileGroup(profile_id = profile,permission = 0, group_id = group_id)
					msg = "user %s added profile_id %s to group %s"%(request.user.username, profile, group_id)
					insert_log('profile_group', "add", "", msg)
					obj_profile_group.save()
			return HttpResponseRedirect('/channel/group/'+str(group_id)+'/')
	else:
		return HttpResponseRedirect('/channel/group/'+str(group_id)+'/')

#"""
#------------------------------------------------------------------------------------------------------------------
#profile
#--------------------------------------------------------------------------------------------------------------------
#
#"""

# profile: dung SQL truy van
def channel_profile_json(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	page = int(request.GET.get('page', 1))
	record_per_page = int(request.GET.get('record_per_page', 200))
	cmd = "SELECT channel.name,profile.id,profile.ip,profile.channel_id,profile.type,profile.monitor,profile.active,profile.status,profile.descr,profile.protocol,from_unixtime(profile.last_update) as last_update FROM profile,channel WHERE profile.channel_id=channel.id ORDER BY profile.status,channel.name"
	list_profile = my_custom_sql(cmd)
	if len(list_profile) < 1:
		return HttpResponse("Empty!")
	args = []
	for profile in list_profile:
		args.append({'id'			:profile[1] if profile[1]else None,
					'channel_name'	:profile[0] if profile[0] else "No name",
					'type'			:profile[4] if profile[4] else "",
					'ip'			:profile[2] if profile[2] else "",
					'protocol'		:profile[9] if profile[9] else "",
					'status'		:profile[7] if profile[7] else 0,
					'active'		:profile[6] if profile[6] else 0,
					'monitor'		:profile[5] if profile[5] else 0,
					'group'			:get_group_by_profile_id(int(profile[1])) if profile[1] else "No group",
					'descr'			:profile[8] if profile[8] else "",
					'last_update'	:str(profile[10]) if profile[10] else "",
			})
	json_data = json.dumps({"profile": args})
	return HttpResponse(json_data, content_type='application/json', status=200)


def channel_profile(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	user = user_info(request)
	return render_to_response('channel/profile/profile.html', user)

@csrf_exempt
def channel_profile_control(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	if not request.user.is_staff:
		return HttpResponseRedirect('/channel/profile/')
	if request.method == 'POST':
		if 'btnadd' in request.POST:
			list_group = Group.objects.all()
			list_channel = getChannelList()
			args = {}
			args['channels'] = list_channel
			args['groups'] = list_group
			return render_to_response('channel/profile/add.html',args)
		if 'btndelete' in request.POST:
			profile_id_delete = request.POST.getlist('SellectProfile', '')
			for profile in profile_id_delete:
				delete_profile_by_id(profile)
				msg = "user %s deleted profile_id %s"%(request.user.username, profile)
				insert_log('profile', "delete", "", msg)
			return HttpResponseRedirect('/channel/profile/')
		if 'btnactive' in request.POST:
			profile_id_active = request.POST.getlist('SellectProfile', '')
			for profile in profile_id_active:
				obj_profile = Profile.objects.get(pk = int(profile))
				obj_profile.active = 1
				msg = "user %s change status to active on profile_id %s ip %s, %s"%(request.user.username, profile, obj_profile.ip, obj_profile.type)
				insert_log('profile', "status", "", msg)
				obj_profile.save()
			return HttpResponseRedirect('/channel/profile/')
		if 'btndeactive' in request.POST:
			profile_id_active = request.POST.getlist('SellectProfile', '')
			for profile in profile_id_active:
				obj_profile = Profile.objects.get(pk = int(profile))
				obj_profile.active = 0
				msg = "user %s change status to deactive on profile_id %s ip %s, %s"%(request.user.username, profile, obj_profile.ip, obj_profile.type)
				insert_log('profile', "status", "", msg)
				obj_profile.save()
			return HttpResponseRedirect('/channel/profile/')

@csrf_exempt
def edit_profile(request, profile_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	if not request.user.is_staff:
		return HttpResponseRedirect('/channel/profile/')
	if request.method == 'POST':
		if 'save' in request.POST:
			channel = int(request.POST.get('channel', ''))
			ip = request.POST.get('ip','').strip()#Cut space
			profile = request.POST.get('profile', '')
			protocol = request.POST.get('protocol', '')
			descr = request.POST.get('descr')
			mon = request.POST.get('monitor','')
			groups = request.POST.getlist('group','')
			if mon == 'Yes':
				monitor = 1
			else:
				monitor = 0
			atve = request.POST.get('active','')
			if atve == "yes":
				active = 1
			else:
				active = 0
			obj_profile = Profile.objects.get(pk = int(profile_id))
			obj_profile.channel_id =channel
			obj_profile.ip = ip
			obj_profile.profile = profile
			obj_profile.protocol = protocol
			obj_profile.descr = descr
			obj_profile.monitor = monitor
			obj_profile.active =active
			obj_profile.save()
			cmd = "DELETE FROM `profile_group` WHERE profile_id = " + str(profile_id)
			my_custom_sql(cmd)
			for group in groups:
				if check_profile_group_exist(profile_id, group) == False:
					obj_profile_group = ProfileGroup(profile_id=profile_id, group_id=group, permission=0)
					obj_profile_group.save()
			msg = "user %s edited profile_id %s"%(request.user.username, profile_id)
			insert_log('profile', "edit", "", msg)
			return HttpResponseRedirect('/channel/profile/')
	list_group_checked = get_group_by_profile_id(profile_id)
	list_group = Group.objects.all()
	profile = Profile.objects.filter(id = profile_id)
	list_channel = getChannelList()
	args = {}
	args['channels'] = list_channel
	args['groups'] = list_group
	args['group_checked'] = list_group_checked
	args['profile'] = profile
	return render_to_response('channel/profile/edit.html',args)

@csrf_exempt
def add_profile(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	if not request.user.is_staff:
		return HttpResponseRedirect('/channel/profile/')
	if request.method == 'POST':
		if 'save' in request.POST:
			channel = int(request.POST.get('channel', ''))
			ip = request.POST.get('ip','').strip()#Cut space
			profile = request.POST.get('profile', '')
			protocol = request.POST.get('protocol', '')
			descr = request.POST.get('descr')
			mon = request.POST.get('monitor','')
			groups = request.POST.getlist('group','')
			if mon == 'Yes':
				monitor = 1
			else:
				monitor = 0
			atve = request.POST.get('active','')
			if atve == "yes":
				active = 1
			else:
				active = 0
			last_update = int(time.time())
			obj_profile = Profile(ip=ip, descr=descr, status=0,type=profile, channel_id=channel, protocol= protocol, logo=0, graph = 0,check=0, sendmail=0, monitor=monitor, mediainfo=0, streamguru = 0, last_update = last_update, change_status=0, active=active)
			msg = "user %s added new profile ip %s, %s"%(request.user.username, ip, profile)
			insert_log('profile', "status", "", msg)
			obj_profile.save()
			for group in groups:
				print group
				print obj_profile.id 
				obj_profile_group = ProfileGroup(profile_id=obj_profile.id, group_id=group, permission=0)
				obj_profile_group.save()
			return HttpResponseRedirect('/channel/profile/')
	list_group = Group.objects.all()
	list_channel = getChannelList()
	args = {}
	args['channels'] = list_channel
	args['groups'] = list_group
	return render_to_response('channel/profile/add.html',args)

def profile_list_by_group(request):
	cmd = "SELECT pbc.id, c.name, pbc.ip, pbc.type, pbc.group_name FROM (SELECT g.name as group_name, p.id ,p.ip ,p.channel_id as channel_id ,p.type FROM  `profile_group` AS pg LEFT JOIN  `group` AS g ON pg.group_id = g.id LEFT JOIN  `profile` AS p ON pg.profile_id = p.id) as pbc, `channel` as c WHERE pbc.channel_id = c.id;"
	profile_list = my_custom_sql(cmd)
	if len(profile_list) < 1:
		return HttpResponse("Empty!")
	args = []
	for profile in profile_list:
		args.append({'id'			:profile[0] if profile[0]else None,
					'channel_name'	:profile[1] if profile[1] else "No name",
					'ip'			:profile[2] if profile[2] else "",
					'type'			:profile[3] if profile[3] else "",
					'group_name'	:profile[4] if profile[4] else "",
			})
	json_data = json.dumps({"profile_by_group": args})
	return HttpResponse(json_data, content_type='application/json', status=200)

def profile_list_by_item(request, profile_id):
	cmd = "SELECT channel.name,profile.type, profile.ip, profile.id FROM profile,channel WHERE profile.channel_id=channel.id and profile.id = "+profile_id+";"
	profile_list = my_custom_sql(cmd)
	if len(profile_list) < 1:
		return HttpResponse("Empty!")
	args = []
	for profile in profile_list:
		args.append({'id'			:profile[3] if profile[3]else None,
					'channel_name'	:profile[0] if profile[0] else "No name",
					'ip'			:profile[2] if profile[2] else "",
					'type'			:profile[1] if profile[1] else "",
			})
	json_data = json.dumps({"profile_by_item": args})
	return HttpResponse(json_data, content_type='application/json', status=200)
