from django.db.models import Q
from channel.models import *
from log.models import *
from itertools import chain
from django.db import connection
from django.utils import timezone

def insert_log(server, tag, program, msg):
    date_time = str(timezone.now())
    cmd = "INSERT INTO logs (host,tag,program,msg,datetime,seq) VALUES ('" + server + "','" + tag + "','" + "Portal web" + "','" + msg + "','" + date_time + "',0)"
    cursor = connection.cursor()
    cursor.execute(cmd)
    row = cursor.fetchall()

def get_log_list():
    cmd = "SELECT id,host,tag,program,msg,datetime FROM logs WHERE seq=100 ORDER BY datetime DESC"
    cursor = connection.cursor()
    cursor.execute(cmd)
    row = cursor.fetchall()
    return row
def insert_log_TS(agent, tag, program, msg):
    date_time = None
    cmd = cmd = "INSERT INTO logs (hoset,tag,program,msg,datetime,seq) VALUES ('" + agent + "','" + tag + "','" + program + "','" + msg + "','" + date_time + "',200)"
    cursor = connection.cursor()
    cursor.execute(cmd)
    row = cursor.fetchall()
def delete_log(log_id):
    obj_log = Logs.objects.get(pk = int(log_id))
    if obj_log:
        obj_log.delete()