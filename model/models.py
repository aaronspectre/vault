from django.db import models

from django.contrib.auth.models import User
from django.forms import ModelForm




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
	model_image = models.ImageField(upload_to = 'static/storage/img/models')
	model_file = models.FileField(upload_to='static/storage/models')
	model_views = models.IntegerField(default = 0)
	model_tags = models.JSONField()
	model_tool = models.CharField(max_length = 50)
	model_favs = models.IntegerField(default = 0)
	model_category = models.ForeignKey(Category, on_delete=models.PROTECT)
	model_author = models.ForeignKey(User, on_delete=models.PROTECT)
	model_link = models.URLField()

	def __str__(self):
		return self.model_name;


class ModForm(ModelForm):
	class Meta:
		model = Mod
		fields = ['model_name', 'model_file', 'model_price', 'model_category', 'model_desc', 'model_image'];
