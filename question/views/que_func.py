 # -*- coding: utf-8 -*-

import json

from django.shortcuts import render, redirect
from question.models import Question, WantListen
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def ask(request):
    error = None

    if request.method == 'GET':
        return render(request, 'ask.html')

    # create question
    title = request.POST['title']
    context = request.POST['context']
    author = request.user

    if len(title) == 0 or len(title) > 64:
        error = '標題長度有誤'

    if len(context) == 0 or len(context) > 64:
        error = '內容長度有誤'

    if not error:
        new_que = Question()
        new_que.title = title
        new_que.text = context
        new_que.author = author
        new_que.save()

        return redirect('/question/view')

    else:
        return render(request, 'ask.html', {'error':error})

def view_question(request):
    questions = Question.objects.all()
    questions = list(questions)
    order_pop = True
    
    if 'order' in request.GET:
        order_pop = (request.GET['order'] == 'popular')


    if order_pop:
        questions.sort(key=lambda x: x.want, reverse=True)

    else:
        questions.sort(key=lambda x: x.id, reverse=True)

    want_list = []
    if request.user and request.user.is_authenticated():
        want_list = WantListen.objects.filter(user=request.user)
        want_list = [w.question.id for w in want_list]
    
    return render(request, 'view.html', {'questions':questions, 'want_list':want_list, 'pop':order_pop})


def want_listen(request):
    response_data = {}

    if 'qid' not in request.GET:
        question_list = Question.objects.all()

        for ql in question_list:
            response_data[ql.id] = ql.want

        return HttpResponse(json.dumps(response_data), content_type="application/json")

    if 'user_want' in request.GET:
        if request.user.is_authenticated():
            want_list = WantListen.objects.filter(user=request.user)
            response_data = [w.question.id for w in want_list]

        return HttpResponse(json.dumps(response_data), content_type="application/json")

    if request.user and request.user.is_authenticated():
        que = None
        try:
            que = Question.objects.get(id=request.GET['qid'])
            want = WantListen.objects.get(user=request.user, question=que)
            want.delete()
            que.want = que.want - 1
            que.save()

        except WantListen.DoesNotExist, e:
            want = WantListen()
            if que != None:
                want.question = que
                want.user = request.user
                want.save()
                que.want = que.want + 1
                que.save()

        except Question.DoesNotExist, e:
            pass

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def edit(request):

    if request.method == 'GET':

        if 'qid' not in request.GET:
            return render(request, 'msg.html', {'message':'Oops, 好像有東西出錯了，請再試一次'})

        qid = request.GET['qid']

        try:
            question = Question.objects.get(id=qid)

            return render(request, 'edit.html', {'question':question})

        except Exception, e:
            return render(request, 'msg.html', {'message':'Oops, 好像有東西出錯了，請再試一次'})

    qid = request.POST['qid']
    title = request.POST['title']
    context = request.POST['context']

    if len(title) == 0 or len(context) == 0:
        return render(request, 'edit.html', {'error':'標題或內容長度不得為零，請再試一次'})

    try:
        question = Question.objects.get(id=qid)
        question.title = title
        question.text = context
        question.save()

        return redirect('/question/view')

    except:
        return render(request, 'msg.html', {'message':'Oops, 好像有東西出錯了，請再試一次'})


@login_required
def delete(request):

    try:
        que = Question.objects.get(id=request.GET['qid'])

        if que.author == request.user or request.user.is_staff:
            want_list = WantListen.objects.filter(question=que)

            for wl in want_list:
                wl.delete()

            que.delete()

    except:
        pass

    return redirect('/question/view')

@login_required
def solve(request):

    try:
        que = Question.objects.get(id=request.GET['qid'])

        if request.user.is_staff:
            que.solved = True
            que.save()

    except:
        pass

    return redirect('/question/view')

@login_required
def unsolve(request):

    try:
        que = Question.objects.get(id=request.GET['qid'])

        if request.user.is_staff:
            que.solved = False
            que.save()

    except:
        pass

    return redirect('/question/view')
