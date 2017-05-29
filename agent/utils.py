import datetime
from django.views.decorators.csrf import csrf_exempt
from channel.utils import *
from agent.models import *
from itertools import chain
from setting.customSQL import *

def get_agent_data_by_id(agent_id):
	obj_agent = Agent.objects.filter(id = agent_id)
	return obj_agent


