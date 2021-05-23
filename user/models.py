from django.db import models

from django.contrib.auth.models import User


class Author(User):
	avatar = models.ImageField(upload_to = 'static/storage/img/user')
	cart = models.JSONField(default = list())
	favs = models.JSONField(default = list())
	bio = models.CharField(max_length = 255, default = 'Bio')
	website = models.URLField()
	location = models.CharField(max_length = 100, default = 'Moon, Utopia')
	favtool = models.CharField(max_length = 50)
	phone = models.CharField(max_length = 20)
	gender = models.CharField(max_length = 10, default = 'None')
	credit = models.CharField(max_length = 20)
	coins = models.JSONField(default= list())

	stripe_account = models.IntegerField(default = -1)
	paypal_account = models.IntegerField(default = -1)

	notifications = models.JSONField(default=list())
	payments = models.JSONField(default=list())
	vipstatus = models.BooleanField(default=False)
	bought = models.JSONField(default = list())

	warnings = models.IntegerField(default = 0)
	reports = models.JSONField(default = list())



class StripeAccount(models.Model):
	account_id = models.CharField(max_length = 30)
	country = models.CharField(max_length = 10)
	transfers = models.CharField(max_length = 10)
	email = models.EmailField()
	business_profile = models.JSONField()
	charges_enabled = models.BooleanField()
	external_account = models.JSONField()
	submitted = models.BooleanField()

	def __str__(self):
		return f'{self.email} - {self.account_id}'