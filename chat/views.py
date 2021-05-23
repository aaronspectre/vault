from django.shortcuts import render

import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import ChatMessage

@csrf_exempt
def handle(request):
	if request.method == 'POST':
		message = ChatMessage()
		message.author = request.user.author
		message.message = json.loads(request.body)
		message.date = timezone.now()
		message.save()
	return JsonResponse({'message': message.message, 'author': request.user.username}, safe=False)


@csrf_exempt
def update(request):
	if request.method == 'POST':
		chat = ChatMessage.objects.order_by('-date')[:10]
		messages = list()
		for message in chat:
			messages.append({'author': message.author.username, 'message': message.message})

		return JsonResponse({'messages': messages}, safe=False)