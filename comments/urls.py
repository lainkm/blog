from django.urls import path

from . import views

app_name = 'comments'
urlpatterns = [
	path('article/<int:pk>', views.post_comment, name='post_comment')
]