from django.db import models

from user.models import Author


class ChatMessage(models.Model):
	message = models.CharField(max_length = 20)
	date = models.DateTimeField()
	author = models.ForeignKey(Author, on_delete = models.CASCADE)

	def __str__(self):
		return f'{self.author} - {self.message}'