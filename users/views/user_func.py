 # -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.decorators import login_required
from users.models import ResetPasswordToken, UserRegisterToken
from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mail
from os import urandom
from base64 import urlsafe_b64encode

@sensitive_post_parameters('password')
def register(request):

    context = {}
    if request.user and request.user.is_authenticated():
        return redirect('/')

    if request.method == 'GET':
        if 'token' in request.GET:
            try:
                token = UserRegisterToken.objects.get(token=request.GET['token'])
                user = token.user
                user.is_active = True
                user.save()

            except UserRegisterToken.DoesNotExist:
                return render(request, 'msg.html', {'message': 'Oops, 沒有這一個 Token 喔。'})

            return redirect('/')

        else:
            return render(request, 'register.html')

    email = request.POST.get('email')
    nickname = request.POST.get('nickname')
    password = request.POST.get('password')

    user = User()

    if not email or lem(email) == 0:
        context['error'] = '請輸入 email'
    if User.objects.filter(email=email).count() < 1:
        user.username = email
        user.email = email
        user.last_name = nickname
        user.set_password(password)
        user.is_active = False
        user.save()

        token = UserRegisterToken()
        token.user = user
        token.token = urlsafe_b64encode(urandom(16))[:-2]
        token.save()

        template = get_template('email.html')
        text_content = '請至 http://140.113.110.7/user/register?token=' + token.token + '完成信箱驗證。'
        subject = '[Hacker, 給問嗎？]註冊確認信'
        from_email = 'admin@ask.sitcon.org'
        send_mail(subject, text_content, from_email, [user.email])

    else:
        context['error'] = '此 email 已註冊'


    if 'error' in context:
        return render(request, 'register.html', context)

    else:
        # TODO: send check email
        context['message'] = '註冊確認信已寄至您的信箱'
        return render(request, 'msg.html', context)

@login_required
def profile(request):

    error = None

    if request.method == 'GET':
        return render(request, 'profile.html')

    user = request.user
    nickname = request.POST['nickname']
    password = request.POST['password']
    user.last_name = nickname

    if password != '':
        user.set_password(password)

    if len(nickname) == 0:
        error = '暱稱長度需大於零'

    if error is None:
        user.save()

    return render(request, 'profile.html', {'error': error})

def forget(request):

    if request.method == 'POST':

        if 'email' not in request.POST or 'password' not in request.POST:
            return render(request, 'forget.html', {'error': '請輸入信箱及新密碼'})

        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
            token = ResetPasswordToken()
            token.user = user
            token.password = password

            # from staff.sitcon.org
            token.token = urlsafe_b64encode(urandom(16))[:-2]
            token.save()

            template = get_template('email.html')
            text_content = '請至 http://140.113.110.7/user/forget?token=' + token.token + '重設密碼。'
            subject = '[Hacker, 給問嗎？]密碼重設信件'
            from_email = 'admin@ask.sitcon.org'
            send_mail(subject, text_content, from_email, [user.email])

            return render(request, 'msg.html', {'message': '請前往信箱檢查密碼信件'})

        except User.DoesNotExist:
            return render(request, 'forget.html', {'error': '信箱未註冊'})

    if 'token' not in request.GET:
        return render(request, 'forget.html')

    message = ''
    token_str = request.GET['token']

    try:
        token = ResetPasswordToken.objects.get(token=token_str)
        new_pwd = token.password
        user = token.user

        user.set_password(new_pwd)
        user.save()
        token.delete()

        message = '密碼重設完成，請用您新的密碼登入'

    except ResetPasswordToken.DoesNotExist:
        message = 'Token 錯誤，若有疑問，請大聲呼叫管理員。'

    except Exception:
        message = 'Oops, 不知道哪邊出錯了 O_O？'

    return render(request, 'msg.html', {'message': message})

