 # -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from question.models import Question, WantListen

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
    
    return render(request, 'view.html', {'popular':popular, 'newest':newest})
