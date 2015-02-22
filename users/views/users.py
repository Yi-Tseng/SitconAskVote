 # -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group
from django.shortcuts import render

@sensitive_variables('password')
def register(request):

    if request.user and request.user.is_authenticated():
        return redirect('/')

    if not request.POST:
        return render(request, 'register.html')

    email = request.POST.get('email')
    nickname = request.POST.get('nick')

