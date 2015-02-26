from django.shortcuts import redirect
from facepy import GraphAPI
import json

# Create your views here.
def login(request):

    response_data = {}

    if 'token' not in request.GET:
        redirect('/user/login')

    access_token = request.GET['token']
    graph = GraphAPI(access_token)

    print graph.get('me')

    return redirect('/')