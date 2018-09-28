# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=30)
    uphone = models.CharField(max_length=11)

class MsgId(models.Model):
    name = models.CharField(max_length=20)
    appid = models.CharField(max_length=32)
    sid = models.CharField(max_length=32)
    token = models.CharField(max_length=32)