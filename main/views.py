import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


from model.models import Mod, Category
from chat.models import ChatMessage



def index(request):
	categories = Category.objects.all()
	return render(request, 'main/index.html', {'categories': categories})

def dashboard(request):
	chat = ChatMessage.objects.order_by('-date')[:10]

	dash_message = None
	if len(request.user.author.notifications) > 0:
		dash_message = request.user.author.notifications
	modelset = Mod.objects.filter(model_author = request.user).order_by('-model_date')
	categories = Category.objects.all()
	return render(request, 'main/dashboard.html', {'categories': categories, 'modelset': modelset, 'dash_message': dash_message, 'messages': chat})


@csrf_exempt
def deleteNote(request):
	if request.method == 'POST':
		for message in request.user.author.notifications:
			if json.loads(request.body) in message.values():
				request.user.author.notifications.remove(message)
				request.user.author.save()
	return HttpResponse(status=200)