from django.db import models

from user.models import Author
from model.models import Mod


class PaymentSession(models.Model):
	amount = models.IntegerField(default = 0)
	modelset = models.JSONField(default = list())
	customer_email = models.EmailField()
	stripe_customer_id = models.CharField(max_length = 30)
	stripe_customer = models.CharField(max_length = 30)
	intent = models.CharField(max_length = 30)
	user = models.ForeignKey(Author, on_delete = models.CASCADE)
	date = models.DateTimeField()

	def __str__(self):
		return f'{self.customer_email} -> {self.intent}'



class Debt(models.Model):
	amount = models.IntegerField()
	account_id = models.CharField(max_length = 30)
	model = models.ForeignKey(Mod, on_delete = models.CASCADE)
	email = models.EmailField()

	def __str__(self):
		return f'{self.email} - {self.model}:{self.amount}'