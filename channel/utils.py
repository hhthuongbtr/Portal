import datetime
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from channel.models import *
from itertools import chain
from django.db import connection
from setting.customSQL import *


def  getChannelList():
	return Channel.objects.all().order_by('name');

def get_channel_by_id(channel_id):
	channel_data = Channel.objects.filter(id = channel_id)
	if len(channel_data) > 0:
		return channel_data
	else:
		return None

def getChannelBaseOnGroup(group_id):
	pass

def getChannelListIMG():
	channel_list_img = Channel.objects.filter(name__icontains = "img") | Channel.objects.filter(name__icontains = "epl")
	if len(channel_list_img) > 0:
		return channel_list_img
	else:
		return None


def get_data_profile_by_group(group_id):
	profile_by_group = ProfileGroup.objects.filter(group_id = group_id)
	if len(profile_by_group) > 0:
		return profile_by_group
	else:
		return None

def get_channel_name_by_id(channel_id):
	obj_channel = Channel.objects.filter(id = channel_id)
	if len(obj_channel) > 0:
		return obj_channel[0].name
	else:
		return "No name"

def get_channel_profile_by_group(arr_channel):
	channel_profile_by_group = list(Profile.objects.filter(id__in = arr_channel))
	return channel_profile_by_group

def delete_channel_by_id(channel_id):
	list_profile_of_channel = Profile.objects.filter(channel_id = channel_id)
	if len(list_profile_of_channel) > 0:
		for profile in list_profile_of_channel:
			delete_profile_by_id(profile.id)
	cnl = Channel.objects.get(pk = int(channel_id))
	cnl.delete()

def check_channel_exist_profile(channel_id):
	list_profile_of_channel = Profile.objects.filter(channel_id = channel_id)
	if len(list_profile_of_channel) > 0:
		return True
	else:
		return False


"""
------------------------------------------------------------------------------------------------------------------
gruop
--------------------------------------------------------------------------------------------------------------------

"""


def getDataGroupList():
	list_group = list(Group.objects.all())
	if len(list_group) > 0:
		return list_group
	else:
		return None

def count_profile(group_id):
	num_profile = ProfileGroup.objects.filter(group_id = group_id).count()
	if int(num_profile) > 0:
		return int(num_profile)
	else:
		return 0

def get_group_data_by_id(group_id):
	group_item = Group.objects.filter(id = group_id)
	return group_item

def get_group_name_by_id(group_id):
	obj_group = Group.objects.filter(id = group_id)
	if len(obj_group) > 0:
		return obj_group[0].name
	else:
		return "No group name"

def get_group_by_profile_id(profile_id):
	cmd = "SELECT `group`.id,`group`.name as name FROM `group`,profile_group as pg,profile WHERE pg.profile_id=profile.id and pg.group_id=`group`.id and pg.profile_id ='" + str(profile_id) + "' ORDER BY pg.group_id";
	groups = my_custom_sql(cmd)
	return groups


"""
------------------------------------------------------------------------------------------------------------------
profile
--------------------------------------------------------------------------------------------------------------------

"""
def get_profle():
	list_profile = Profile.objects.all().order_by('status')
	return list_profile

def get_profile_type_by_profile_id(profile_id):
	obj_profile = Profile.objects.filter(id = profile_id)
	if len(obj_profile) > 0:
		return obj_profile[0].type
	else:
		return "Profile not exist!"

def get_channel_name_by_profile_id(profile_id):
	#Lay thong tin channel ID cua profile
	obj_profile = Profile.objects.filter(id = profile_id)
	if len(obj_profile) > 0:
		channel_id = obj_profile[0].channel_id
		#Lay ten cua channel theo id channel vua tim duoc
		channel_name = get_channel_name_by_id(channel_id)
		if len(channel_name) > 0:
			return channel_name
	else:
		return 'No channel exist!'

def get_profile_ip_from_id(profile_id):
	obj_profile = Profile.objects.filter(id = profile_id)
	if len(obj_profile) > 0:
		return obj_profile[0].ip
	else:
		return "Profile not exist!"
def get_arr_profle_id_by_channel_img():
	list_channel = getChannelListIMG()
	if len(list_channel) >0:
		print list_channel
		arr_channel_id = []
		for i in list_channel:
			arr_channel_id.append(i.id)
		list_profile = list(Profile.objects.filter(channel_id__in = arr_channel_id))
		if len(list_profile) > 0:
			print list_profile
			arr_profile = []
			for x in list_profile:
				arr_profile.append(x.id)
			return arr_profile
		else:
			return "No profile exist!"
	else:
		return "No channel exist!"
				
def get_profile_data_by_id(profile_id):
	obj_profile = Profile.objects.filter(id = profile_id)
	return obj_profile

def delete_profile_by_id(profile_id):
	cmd1 = "DELETE FROM `profile_agent` where profile_id = " + str(profile_id)
	my_custom_sql(cmd1)
	cmd2 = "DELETE FROM `transcode` where input_id = " + str(profile_id)
	my_custom_sql(cmd2)
	cmd3 = "DELETE FROM `profile_group` where profile_id = " + str(profile_id)
	my_custom_sql(cmd3)
	obj_profile = Profile.objects.get(pk = int(profile_id))
	obj_profile.delete()

def check_profile_exist_transcode(profile_id):
	list_transcode_of_profile = Transcode.objects.filter(input_id = profile_id)
	if len(list_transcode_of_profile) > 0:
		return True
	else:
		return False

				
#"""
#------------------------------------------------------------------------------------------------------------------
#profile_gruop
#--------------------------------------------------------------------------------------------------------------------
#
#"""
def check_profile_group_exist(profile_id, group_id):
	obj_profile_group = ProfileGroup.objects.filter(profile_id=profile_id).filter(group_id=group_id)
	if len(obj_profile_group) >0:
		return True
	else:
		return False
