# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from facebook import views
urlpatterns = patterns(
    '',
    url(r'^login$', views.login),
)
