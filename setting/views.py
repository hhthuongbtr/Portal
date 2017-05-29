import os
import sys
#import vlc
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
from Portal.customSQL import *
from agent.models import *
from agent.utils import *
from django.core.cache import cache
from calendar import month
import unicodedata
#Phan trang
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import struct

# Create your views here.

