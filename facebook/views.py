# -*- coding: utf-8 -*-
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
import django.contrib.auth as auth
from facepy import GraphAPI
from os import urandom
from base64 import urlsafe_b64encode

# Create your views here.
def login(request):


    if 'token' not in request.GET:
        redirect('/user/login')

    access_token = request.GET['token']
    graph = GraphAPI(access_token)

    info = graph.get('me?fields=name,email,verified')
    name = info['name']
    verified = info['verified']
    email = info['email']

    print '[FB info]:', name, verified, email

    if not verified:
        return render(request, 'login.html', {'error': 'FB 帳號未驗證'})

    try:
        user = auth.authenticate(username=email, password=access_token[:32])
        auth.login(request, user)

    except User.DoesNotExist:
        user = User()
        user.username = email
        user.email = email
        user.last_name = name
        password = access_token[:32]
        user.set_password(password)
        user.is_active = True
        user.save()
        auth.login(request, user)
        print 'login to user', user.username

    return redirect('/')


