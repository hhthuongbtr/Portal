"""Portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls')),
"""
from channel.views import *
from agent.views import *
from django.conf.urls import include, url
from django.contrib import admin
from accounts.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
	#==============================
	# URL of Admin
	#==============================
    url(r'^admin/', admin.site.urls),
    url(r'^$', channel_list),
    url(r'^test/$', test_login),

    #==============================
    # URL of accounts
    #==============================
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'accounts/login.html'}),
    url(r'^accounts/logout/$', logout_view),
    url(r'^accounts/auth/$', auth_view),
    url(r'^accounts/invalid/$', invalid_login),
    url(r'^password/$', change_password, name='change_password'),

	#==============================
	# URL of channel
	#==============================
    #url(r'^test$', test, name='test'),
    url(r'^channel/$', channel_list),
    url(r'^channel/json/$', channel_json),
    url(r'^channel/control/$', channel_control),

    url(r'^channel/add/$', add_channel),
    url(r'^channel/edit/(?P<channel_id>\d+)/$', edit_channel),

    #group 
    url(r'^channel/group/$', channel_group),
    url(r'^channel/group/json/$', channel_group_json),
    url(r'^channel/group/control/$', channel_group_control),

    url(r'^channel/group/add/$', add_group),
    url(r'^channel/group/edit/(?P<group_id>\d+)/$', edit_group),

    url(r'^channel/group/(?P<group_id>\d+)/control/$', channel_group_id_control),
    url(r'^channel/group/(?P<group_id>\d+)/add/$', channel_group_id_add),

    url(r'^channel/group/(?P<group_id>\d+)/json/$', group_view_json),
    url(r'^channel/group/(?P<group_id>\d+)/$', group_view),

    #profile
    url(r'^channel/profile/$', channel_profile),
    url(r'^channel/profile/json/$', channel_profile_json),
    url(r'^channel/profile/control/$', channel_profile_control),

    url(r'^channel/profile/add/$', add_profile),
    url(r'^channel/profile/edit/(?P<profile_id>\d+)/$', edit_profile),


    #==============================
    # URL of agent
    #==============================
    #agent 
    url(r'^agent/$', agent_view),
    url(r'^agent/json/$', agent_view_json),
    url(r'^agent/control/$', agent_control),

    url(r'^agent/add/$', add_agent),
    url(r'^agent/edit/(?P<agent_id>\d+)/$', edit_agent),

    url(r'^agent/monitor/$', profile_agent_view),
    url(r'^agent/monitor/json/$', profile_agent_view_json),
    url(r'^agent/monitor/control/$', profile_agent_control),

    url(r'^agent/monitor/add/$', add_profile_agent),
    url(r'^agent/monitor/edit/(?P<profile_agent_id>\d+)/$', edit_profile_agent),


    #API
    url(r'^agent/monitor/add/pbg/json/$', profile_list_by_group),
    url(r'^agent/monitor/edit/(?P<profile_id>\d+)/json/$', profile_list_by_item),

    url(r'^agent/monitor/(?P<profile_agent_id>\d+)/json/$', profile_agent_by_item_json),
    


	#==============================
	# URL of log
	#==============================
]
