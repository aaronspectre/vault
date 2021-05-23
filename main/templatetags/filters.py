from django import template

register = template.Library()



@register.filter
def tagparse(tags):
	text = ''
	i = 0
	for tag in tags:
		if i != 0:
			text += f', {tag}'
		else:
			text = tag
			i+=1
	return text


@register.filter
def toStr(val):
	return str(val)



@register.filter
def total(modelset):
	price = 0
	for model in modelset:
		price+=model.model_price

	return price


@register.filter
def convert(modelset):
	price = 0
	for model in modelset:
		price+=model.model_price

	return int(round(price*100))



@register.filter
def makeArray(obj):
	a = list()

	for item in obj:
		a.append(item.id)

	return a



@register.filter
def modelDownload(model):
	if model.model_price == 0:
		return True
	else:
		return False


@register.filter
def viewFree(price):
	if price == 0:
		return 'Free'
	else:
		return f'{price}$'