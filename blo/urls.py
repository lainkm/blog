"""blo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from article.feeds import AllArticlesRssFeed
# import xawdmin
from beatemail import views as email_views

urlpatterns = [
    # path('all/rss/', AllArticlesRssFeed(), name='rss'),
    # path('article/', include('article.urls')),
    # path('comments/', include('comments.urls')),
    # path('admin/', admin.site.urls),
    # path('search/', include('haystack.urls'))

    path('all/rss/', AllArticlesRssFeed(), name='rss'),
    path('', include('article.urls')),
    path('', include('comments.urls')),
    path('lainly_admin/', admin.site.urls),
    path('search/', include('haystack.urls')),
    # path('xadmin/', xadmin.site.urls),
    path('email/', email_views.index, name='email'),
    path('summernote/', include('django_summernote.urls')),

]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
