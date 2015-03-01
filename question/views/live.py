import json
from django.shortcuts import render, redirect
from question.models import Question, WantListen
from django.http import HttpResponse

def get_current_live_question(request):
    live_question = None

    try:
        live_question = Question.objects.get(live=True)

    except Question.DoesNotExist:
        pass

    context = {'question': live_question}
    return HttpResponse(json.dumps(context), content_type="application/json")

def set_live(request):

    context = {'question': None}

    if 'qid' in request.GET:
        qid = request.GET['qid']

        try:
            questions = Question.objects.all()

            for question in questions:

                if question.live and question.id != qid:
                    question.live = False
                    question.save()

                if question.id == qid:
                    question.live = True
                    question.save()
                    context['question'] = question

        except:
            context['error'] = True

    return HttpResponse(json.dumps(context), content_type="application/json")

def live_view(request):
    context = {'question': None}
    try:
        context['question'] = Question.objects.get(live=True)
    except Exception, e:
        pass

    return render(request, 'live.html', context)

