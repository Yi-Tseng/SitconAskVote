 # -*- coding: utf-8 -*-

import json

from django.shortcuts import render, redirect
from question.models import Question, WantListen
from django.http import HttpResponse


def ask(request):

    if not request.user or not request.user.is_authenticated():
        return redirect('/user/login')

    if request.method == 'GET':
        return render(request, 'ask.html')

    # create question
    title = request.POST['title']
    context = request.POST['context']
    author = request.user

    new_que = Question()

    # TODO: add xss protection
    new_que.title = title
    new_que.text = context
    new_que.author = author
    new_que.save()

    # TODO: add error message
    return redirect('/question/view')

def view_question(request):
    questions = Question.objects.all()

    # Update want count
    # TODO: need other method to update this count

    for que in questions:
        count = WantListen.objects.filter(question=que.id).count()
        que.want = count
        que.save()

    popular = list(questions)
    newest = list(questions)

    popular.sort(key=lambda x: x.want, reverse=True)
    newest.sort(key=lambda x: x.id, reverse=True)

    want_list = []

    if request.user and request.user.is_authenticated():
        want_list = WantListen.objects.filter(user=request.user)
        want_list = [w.question.id for w in want_list]
    
    return render(request, 'view.html', {'popular':popular, 'newest':newest, 'want_list':want_list})


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


