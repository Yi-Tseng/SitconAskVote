 # -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from question.models import Question

def ask(request):

    if not request.user or not request.user.is_authenticated():
        return redirect('/user/login')

    if request.method == 'GET':
        return render('ask.html')

    # create question
    title = request.POST.title
    context = request.POST.context
    author = request.user.id

    print title, context, author

    



def view_question(request):
    questions = Question.objects.get()
    return render('view.html', {'questions':questions})
