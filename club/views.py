# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
import json
import requests
import random
from models import *
import hashlib

def index(request):
    uname = request.session.get('uname')
    if uname ==None:
        return render(request, 'club/index.html')
    else:
        context = {'uname':uname}
        return render(request, 'club/user_index.html', context)



def login(request):
    return render(request, 'club/login.html')

def loginHandle(request):
    uname = request.POST['uname']
    upwd = request.POST['upwd']
    sha1 = hashlib.sha1()
    sha1.update(upwd)
    pwd = sha1.hexdigest()
    try:
        user = UserInfo.objects.get(uname=uname)
    except UserInfo.DoesNotExist:
        return HttpResponse('账号不存在')
    else:
        if user.upwd == pwd:
            request.session['uname'] = uname
            request.session.set_expiry(0)
            return HttpResponse('登陆成功')

        return HttpResponse('账号或密码不正确')

def register(request):
    return render(request, 'club/register.html')


def sendmsg(request):
    a = '1234567890'
    captcha = ''
    for i in range(4):
        captcha += a[random.randint(0, 9)]
    phone = request.POST['uphone']
    sha1 = hashlib.sha1()
    sha1.update(phone)
    sha1.update(captcha)
    hashcode = sha1.hexdigest()
    request.session['captcha'] = hashcode
    request.session.set_expiry(60)
    url1 = "https://open.ucpaas.com/ol/sms/sendsms"
    msgid = MsgId.objects.get(name='admin')
    msg = {
        "sid": msgid.sid,
        "token": msgid.token,
        "appid": msgid.appid,
        "templateid": "377122",
        "param": captcha + ',60',
        "mobile": phone,
    }
    headers = {'Content-Type': 'application/json'}
    re = requests.post(url=url1, headers=headers, data=json.dumps(msg)).text
    '''
    {"code":"100015",
     "count":"0",
     "create_date":"",
     "mobile":"1567",
     "msg":"号码不合法",
     "smsid":"",
     "uid":""
     }
    '''
    result = json.loads(re)
    return JsonResponse(result)


def check_uname(request):
    uname = request.POST['uname']
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})


def check_umsg(request):
    try:
        umsg = request.POST['umsg']
        uphone = request.POST['uphone']
    except KeyError:
        return HttpResponse('no')
    else:
        sha1 = hashlib.sha1()
        sha1.update(uphone)
        sha1.update(umsg)
        hashcode = sha1.hexdigest()
        if hashcode == request.session['captcha']:
            return HttpResponse('ok')
        else:
            return HttpResponse('no')

def registerHandle(request):
    post = request.POST
    uname = post.get('uname')
    upwd = post.get('upwd')
    cpwd = post.get('cpwd')
    uphone = post.get('uphone')
    uemail = post.get('uemail')
    if upwd != cpwd:
        return redirect('register/')
    user = UserInfo()
    user.uname = uname
    sha1 = hashlib.sha1()
    sha1.update(upwd)
    pwd = sha1.hexdigest()
    user.upwd = pwd
    user.uemail = uemail
    user.uphone = uphone
    user.save()
    return HttpResponse('注册成功')