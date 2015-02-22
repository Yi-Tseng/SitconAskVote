 # -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group
from django.shortcuts import render
from django.views.decorators.debug import sensitive_post_parameters

@sensitive_post_parameters('password')
def register(request):
    username = request.POST.get('username')
