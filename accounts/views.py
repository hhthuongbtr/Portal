from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status
import json
from accounts.user_info import *
from django.shortcuts import render, redirect
from accounts.models import *
from setting import settings
from setting.DateTime import *
            
# ------------auth
@require_http_methods(['GET', 'POST'])
@csrf_exempt
def log_in(request):
    if request.method=='POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        agrs = {}
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                request.session['has_commented'] = True 
                #Set session timeout
                request.session.set_expiry(settings.AUTO_LOGOUT_DELAY * 60)
                return HttpResponse(status=status.HTTP_202_ACCEPTED)
        else:
            agrs["detail"] = "Incorrect username or password!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
    '''User is really login, logout user session'''
    log_out(request)
    return render_to_response('accounts/login.html')
    
def log_out(request):
    logout(request)
    response = HttpResponseRedirect('/accounts/login')
    response.delete_cookie('user_location')
    return response

@require_http_methods(['GET', 'POST'])
@csrf_exempt
def password_change(request):
    if request.method == 'POST':
        agrs = {}
        data = json.loads(request.body)
        oldpassword = data['oldpassword']
        newpassword = data['newpassword']
        retypepassword = data['retypepassword']
        #Check password input incorrect
        if newpassword != retypepassword:
            agrs["detail"] = "Sorry, passwords do not match!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        #check new password with current password
        username = request.user.username
        user = user = authenticate(username=username, password=oldpassword)
        if user is None:
            agrs["detail"] = "Sorry, password not correct!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        #Check new pass word  not same old password
        if newpassword == oldpassword:
            agrs["detail"] = "Sorry, new password same old password!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)

        user = User.objects.get(pk=int(request.user.id))
        user.set_password(newpassword)
        user = user.save()
        update_session_auth_hash(request, user)
        agrs["detail"] = "Password change success!"
        messages = json.dumps(agrs)
        return HttpResponse(messages, content_type='application/json', status=202)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    user = user_info(request)
    return render_to_response('accounts/password_change.html', user)

@require_http_methods(['GET', 'POST'])
@csrf_exempt
def profile(request):
    if request.method == 'GET':
        user = user_info(request)
        return render_to_response('accounts/profile.html', user)
    agrs = {}
    if request.method == 'POST':
        user = User.objects.get(pk=int(request.user.id))
        data = json.loads(request.body)
        first_name = data['first_name'].strip()
        last_name = data['last_name'].strip()
        email = data['email'].strip()
        flag = 0
        if user.first_name != first_name:
            user.first_name = first_name
            flag = 1
        if  user.last_name != last_name:
            user.last_name = last_name
            flag = 1
        if user.email != email:
            user.email = email
            flag = 1
        if flag:
            user.save()
            agrs["detail"] = "Profile change sucessfuly!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=202)
        agrs["detail"] = "Info! Profile no change."
        messages = json.dumps(agrs)
        return HttpResponse(messages, content_type='application/json', status=203)
    agrs["detail"] = "Eror! unknow."
    messages = json.dumps(agrs)
    return HttpResponse(messages, content_type='application/json', status=203)



@require_http_methods(['GET'])
def profile_json(request):
    user = User.objects.get(pk=int(request.user.id))
    agrs = []
    agrs.append({
        'username'      : user.username,
        'email'         : user.email,
        'first_name'    : user.first_name,
        'last_name'     : user.last_name,
        'is_staff'      : user.is_staff,
        'is_active'     : user.is_active,
        'date_joined'   : DateTime().conver_human_creadeble_2_unix_timetamp_local(str(user.date_joined)),
        'last_login'    : DateTime().conver_human_creadeble_2_unix_timetamp_local(str(user.last_login))
        })
    return HttpResponse(json.dumps(agrs), content_type='application/json', status=200)
