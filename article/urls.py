from django.urls import path

from . import views

app_name = 'article'
# urlpatterns = [
#     path('', views.index, name='index'),
#     path('<int:pk>/', views.detail, name='detail'),
#     path('archives/<int:year>/<int:month>', views.archives, name='archives'),
# ]

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
    path('archives/<int:year>/<int:month>', views.ArchivesView.as_view(), name='archives'),
    path('tag/<int:pk>', views.TagView.as_view(), name='tag'),
    # path('search/', views.search, name='search')
]