from django.urls import path

from . import views

urlpatterns = [
    path('', views.file_upload, name='file_upload'),
    path('success/', views.success, name='success')
]