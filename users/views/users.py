 # -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group
from django.shortcuts import render

@sensitive_variables('password')
def register(request):
    username = request.POST.get('username')