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
    text = request.POST['context']
    author = request.user

    if len(title) == 0:
        error = '標題不可以為空白'
    if len(title) > 64:
        error = '標題長度有誤'

    if len(text) == 0:
        error = '內容不可以為空白'
    if len(text) > 64:
        error = '內容長度有誤'

    if not error:
        new_que = Question()
        new_que.title = title
        new_que.text = text
        new_que.author = author
        new_que.save()

        return redirect('/question/view')

    else:
        context = {}
        context['error'] = error
        context['title'] = title
        context['text'] = text
        return render(request, 'ask.html', context)

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
    context = {}

    if request.method == 'GET':

        if 'qid' not in request.GET:
            context['message'] = 'Oops, 好像有東西出錯了，請再試一次'
            context['auto_jump_location'] = '/question/view'
            return render(request, 'msg.html', context)

        qid = request.GET['qid']

        try:
            question = Question.objects.get(id=qid)

            if question.author.id != request.user.id:
                context['message'] = '請左轉 HITCON，謝謝'
                context['auto_jump_location'] = 'http://hitcon.org/'
                return render(request, 'msg.html', context)

            context['question'] = question
            return render(request, 'edit.html', context)

        except Exception, e:
            context['message'] = 'Oops, 好像有東西出錯了，請再試一次'
            return render(request, 'msg.html', context)

    qid = request.POST['qid']
    title = request.POST['title']
    text = request.POST['context']

    if len(title) == 0 or len(text) == 0:
        context['error'] = '標題或內容長度不得為零，請再試一次'

    try:
        question = Question.objects.get(id=qid)

        if question.author.id != request.user.id:
            context['message'] = '請左轉 HITCON，謝謝'
            context['auto_jump_location'] = 'http://hitcon.org/'
            return render(request, 'msg.html', context)

        context['question'] = question

        if 'error' not in context:
            question.title = title
            question.text = text
            question.save()
            context['error'] = '問題儲存完成'

        return render(request, 'edit.html', context)

    except:
        context['message'] = 'Oops, 好像有東西出錯了，請再試一次'
        return render(request, 'msg.html', context)


@login_required
def delete(request):
    context = {}

    try:
        que = Question.objects.get(id=request.GET['qid'])

        if que.author == request.user or request.user.is_staff:
            want_list = WantListen.objects.filter(question=que)

            for wl in want_list:
                wl.delete()

            que.delete()

        else:
            context['message'] = '請左轉 HITCON，謝謝'
            context['auto_jump_location'] = 'http://hitcon.org/'
            return render(request, 'msg.html', context)

    except:
        context['message'] = 'Oops, 好像有東西出錯了，請再試一次'
        context['auto_jump_location'] = '/question/view'
        return render(request, 'msg.html', context)

    return redirect('/question/view')

@login_required
def solve(request):
    context = {}

    try:
        que = Question.objects.get(id=request.GET['qid'])

        if request.user.is_staff:
            que.solved = True
            que.save()

    except:
        context['message'] = 'Oops, 好像有東西出錯了，請再試一次'
        context['auto_jump_location'] = '/question/view'
        return render(request, 'msg.html', context)

    return redirect('/question/view')

@login_required
def unsolve(request):
    context = {}

    try:
        que = Question.objects.get(id=request.GET['qid'])

        if request.user.is_staff:
            que.solved = False
            que.save()

    except:
        context['message'] = 'Oops, 好像有東西出錯了，請再試一次'
        context['auto_jump_location'] = '/question/view'
        return render(request, 'msg.html', context)

    return redirect('/question/view')

def live_view(request):
    return render(request, 'live.html')

