from django import forms

class ModForm(forms.Form):
	model_name = forms.CharField(max_length = 40)
	model_description = forms.CharField(max_length = 255)
	model_category = forms.CharField(max_length = 50)
	model_price = forms.FloatField()
	model_author_price = forms.FloatField()
	model_file = forms.FileField(widget = forms.ClearableFileInput(attrs = {'multiple': True}))
	model_image = forms.ImageField()
	model_tags = forms.CharField(max_length = 255)
	model_tool = forms.CharField(max_length = 50)