from django import template
from model.models import ModelImage

register = template.Library()



@register.filter
def get_model_image(model):
	image = ModelImage.objects.filter(parent = model)[0]
	return image.file.url


@register.filter
def model_images(model):
	return ModelImage.objects.filter(parent = model)