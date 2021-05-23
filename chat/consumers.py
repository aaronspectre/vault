import json

from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone
from django.shortcuts import get_object_or_404

from chat.models import ChatMessage
from user.models import Author

from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
	def connect(self):
		async_to_sync(self.channel_layer.group_add)('chat', self.channel_name)
		self.accept()

	def disconnect(self, close_code):
		async_to_sync(self.channel_layer.group_discard)("chat", self.channel_name)

	def receive(self, text_data):
		async_to_sync(self.channel_layer.group_send)(
			'chat',
			{
				'type': 'chat_message',
				'message': text_data
			}
		)

		chat_message = ChatMessage()
		chat_message.message = json.loads(text_data)['message']
		chat_message.author = get_object_or_404(Author, username = json.loads(text_data)['author'])
		chat_message.date = timezone.now()
		chat_message.save()


	def chat_message(self, event):
		message = json.loads(event['message'])['message']
		author = json.loads(event['message'])['author']

		self.send(text_data=json.dumps({'message': message, 'author': author}))