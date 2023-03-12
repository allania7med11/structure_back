from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from myclient import views as myclient_views
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('auth/', myclient_views.auth),
]
