from django.shortcuts import redirect
from facepy import GraphAPI
from core.private_data import fb_config
from urlparse import parse_qs
import requests
import urllib

# Create your views here.
def login(request):

    if 'code' not in request.GET:
        return redirect('/user/login')

    code = request.GET['code']

    args = dict(client_id=fb_config['app_id'], redirect_uri="http://ask.sitcon.org/user/login/")
    args["client_secret"] = fb_config['secret']
    args["code"] = code
    token_url = "https://graph.facebook.com/oauth/access_token?"+urllib.urlencode(args)

    r = requests.get(token_url)
    print r.text

    return redirect('/user/login')
