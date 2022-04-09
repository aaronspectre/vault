from django.db import models

from django.contrib.auth.models import User
from django.conf import settings



class Category(models.Model):
	name = models.CharField(max_length = 40)
	amount = models.IntegerField(default = 0)
	img = models.ImageField(upload_to = 'static/storage/img/categories')
	sign = models.CharField(max_length = 30, default = 'exclamation')

	def __str__(self):
		return self.name




class Mod(models.Model):
	model_name = models.CharField(max_length = 30)
	model_desc = models.TextField()
	model_price = models.FloatField()
	model_author_price = models.FloatField(default = 0)
	model_date = models.DateTimeField()
	model_views = models.IntegerField(default = 0)
	model_tags = models.JSONField()
	model_tool = models.CharField(max_length = 50)
	model_favs = models.IntegerField(default = 0)
	model_category = models.ForeignKey(Category, on_delete=models.PROTECT)
	model_author = models.ForeignKey(User, on_delete=models.PROTECT)
	model_link = models.URLField()

	def __str__(self):
		return self.model_name;


class ModelFile(models.Model):
	parent = models.ForeignKey(Mod, on_delete = models.CASCADE)
	file = models.FileField(upload_to='static/storage/models')

	def __str__(self):
		return self.parent.model_name


class ModelImage(models.Model):
	parent = models.ForeignKey(Mod, on_delete = models.CASCADE)
	file = models.ImageField(upload_to = 'static/storage/img/models')

	def __str__(self):
		return self.parent.model_name