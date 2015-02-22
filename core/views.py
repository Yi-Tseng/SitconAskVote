from django.shortcuts import render

def index(request):
	context = {}

	if request.user.is_authenticated():
		context['username'] = request.user.first_name


	return render(request, 'index.html', context)
