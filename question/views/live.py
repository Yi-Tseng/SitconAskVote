import json
from django.shortcuts import render, redirect
from question.models import Question, WantListen
from django.http import HttpResponse
from django.forms.models import model_to_dict

def get_current_live_question(request):
    live_question = None
    context = {'question': None}

    try:
        live_question = Question.objects.get(live=True)

        context = {'question': {'author': live_question.author.last_name, 'text': live_question.text, 'title': live_question.title}}

    except Question.DoesNotExist:
        pass

    return HttpResponse(json.dumps(context), content_type="application/json")

def set_live(request):

    context = {'question': None}

    if 'qid' in request.GET:
        qid = request.GET['qid']

        try:
            live_questions = Question.objects.filter(live=True)

            for live_question in live_questions:
                live_question.live = False
                live_question.save()

        except Question.DoesNotExist:
            pass

        try:
            live_question = Question.objects.get(id=qid)
            live_question.live = True
            live_question.save()

        except Question.DoesNotExist:
            pass

    return redirect('/question/view')

def live_view(request):
    context = {'question': None}
    try:
        context['question'] = Question.objects.get(live=True)
    except Exception, e:
        pass

    return render(request, 'live.html', context)

