from django.shortcuts import render, redirect
from django.views.decorators.debug import sensitive_post_parameters
import django.contrib.auth as auth

@sensitive_post_parameters('password')
def login(request):

    context = {}

    if request.user.is_authenticated():
        return redirect('/')

    # get
    if not request.POST:
        return render(request, 'login.html', context)

    if 'submit' in request.POST:
        username = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:
                auth.login(request, user)

                return redirect('/')

            context['error'] = 'account_disabled'

        else:
            context['error'] = 'invalid_login'
    else:
        context['error'] = request.GET.get('status')

    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('users:login')
