from django.db.models import Q
from channel.models import *
from log.models import *
from itertools import chain
from django.db import connection

def my_custom_sql(cmd):
    cursor = connection.cursor()
    cursor.execute(cmd)
    row = cursor.fetchall()
    return row
    cursor.close()