from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.index, name='index'),
    path('tag/<str:tag>/', views.index, name='index_tagged'),
    path('thread/<str:slug>/', views.thread, name='thread'),
]
