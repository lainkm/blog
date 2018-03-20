from __future__ import absolute_import, unicode_literals
# from celery import shared_task
 
# @shared_task
# def add(x, y):
#     return x + y
#  
from django.db.models import F
from .models import Article
from blo import celery_app

 
@celery_app.task
def incr_readtimes(article_id):
	print('read_times + 1...')
	return Article.objects.filter(id=article_id).update(read_times=F('read_times') + 1)

