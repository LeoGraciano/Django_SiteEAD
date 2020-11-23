from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.index, name='index'),
    path('detalhes/<str:slug>/', views.details, name='details'),
    path('inscricao/<str:slug>/', views.enrollment, name='enrollment'),
    path('anuncios/<str:slug>/', views.announcements, name='announcements'),
    path('cancelar-inscricao/<str:slug>/',
         views.undo_enrollment, name='undo_enrollment'),
    path('comentario/<str:slug>/<int:pk>/', views.show_announcement,
         name='show_announcement'),



]
