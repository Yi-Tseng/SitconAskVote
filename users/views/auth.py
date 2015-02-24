# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.views.decorators.debug import sensitive_post_parameters
import django.contrib.auth as auth

@sensitive_post_parameters('password')
def login(request):

    context = {}

    if request.user and request.user.is_authenticated():
        return redirect('/')

    if request.method == 'GET':
        return render(request, 'login.html', context)

    username = request.POST['email']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)

    if user != None:

        if user.is_active:
            auth.login(request, user)

            return redirect('/')

        context['error'] = '帳號未啟用'

    else:
        context['error'] = '帳號或密碼錯誤'
    

    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('/')
