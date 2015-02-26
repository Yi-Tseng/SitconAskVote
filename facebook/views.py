from django.shortcuts import redirect
from facepy import GraphAPI
from core.private_data import fb_config
from urlparse import parse_qs

# Create your views here.
def login(request):
    
    if 'code' not in request.GET:
    	return redirect('/user/login')

    code = request.get['code']
    graph = GraphAPI()
    response = graph.get(
        path='oauth/access_token',
        client_id=fb_config['app_id'],
        client_secret=fb_config['secret'],
        redirect_uri='http://ask.sitcon.org/',
        code=code
    )

    data = parse_qs(response)
    graph = GraphAPI(data['access_token'][0])
    print graph.get('/me')


