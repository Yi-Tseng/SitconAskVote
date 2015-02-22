 # -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group
from django.shortcuts import render
from django.views.decorators.debug import sensitive_post_parameters

@sensitive_post_parameters('password')
def register(request):

    if request.user and request.user.is_authenticated():
        return redirect('/')

    if not request.POST:
        return render(request, 'register.html')

    email = request.POST.get('email')
    nickname = request.POST.get('nick')


