#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse

from .tasks import send_email_async

def index(request):
	for i in range(5):
		send_email_async.delay()
	return HttpResponse(u"5个人即将收到邮件")
