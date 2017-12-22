from django.conf.urls import url
from event import views

urlpatterns = [
    url(r'^api/$', views.EventList().routing),
    url(r'^api/standby/$', views.EventList().standby),
    url(r'^api/(?P<pk>[0-9]+)/$', views.EventDetail().routing),
    url(r'^api/encoder/$', views.EncoderList().routing),
    url(r'^api/encoder/standby/$', views.EncoderList().standby),
    url(r'^api/encoder/(?P<pk>[0-9]+)/$', views.EncoderDetail().routing),
    url(r'^api/service/$', views.ServiceCheckList().routing),
    url(r'^api/service/standby/$', views.ServiceCheckList().standby),
    url(r'^api/service/(?P<pk>[0-9]+)/$', views.ServiceCheckDetail().routing),
    url(r'^api/event_monitor/$', views.EventMonitorList().routing),
    url(r'^api/event_monitor/(?P<pk>[0-9]+)/$', views.EventMonitorDetail().routing),
    url(r'^api/monitor/$', views.MonitorList().routing),
    url(r'^api/running/$', views.MonitorList().get_running_monitor_list),
    url(r'^api/waiting/$', views.MonitorList().get_waiting_monitor_list),
    url(r'^api/completed/$', views.MonitorList().get_completed_monitor_list),
    url(r'^api/monitor/(?P<event_monitor_id>[0-9]+)/$', views.MonitorDetail().routing),
    #/event/
    url(r'^$', views.Template().event),
    url(r'^encoder/$', views.Template().encoder),
    url(r'^service/$', views.Template().service),
    url(r'^monitor/$', views.Template().monitor),
    url(r'^monitor/add/$', views.Template().monitor_add),
    url(r'^monitor/add/step1.html/$', views.Template().monitor_add_step1),
    url(r'^monitor/add/step2.html/$', views.Template().monitor_add_step2),
    url(r'^monitor/add/step3.html/$', views.Template().monitor_add_step3),
    url(r'^monitor/edit/(?P<event_monitor_id>[0-9]+)/$', views.Template().monitor_edit),
    url(r'^monitor/edit/step1.html/$', views.Template().monitor_edit_step1),
    url(r'^monitor/edit/step2.html/$', views.Template().monitor_edit_step2),
    url(r'^monitor/edit/step3.html/$', views.Template().monitor_edit_step3),
]
