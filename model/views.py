import mimetypes
import uuid

from django.shortcuts import render, get_object_or_404

from django.contrib.auth import logout
from model.models import Mod, Category
from user.models import Author
from model.forms import ModForm
from django.utils import timezone

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required




@login_required
def modelupload(request):
	allowPrice = True
	error = None
	if request.user.author.stripe_account == -1:
		allowPrice = False

	if 'modelupload_error' in request.session.keys():
		error = request.session['modelupload_error']

	form = ModForm()
	cat = Category.objects.all()
	return render(request, 'model/modeluploadform.html', {'formset': form, 'categories': cat, 'allowPrice': allowPrice, 'error': error})


@login_required
def upload(request):
	if request.method == 'POST':
		form = ModForm(request.POST, request.FILES)
		if form.is_valid():
			category = get_object_or_404(Category, name = request.POST['model_category'])

			mod = Mod()
			mod.model_name = request.POST['model_name']
			mod.model_desc = request.POST['model_description']
			mod.model_price = request.POST['model_price']
			mod.model_author_price = request.POST['model_author_price']
			mod.model_file = request.FILES['model_file']
			mod.model_image = request.FILES['model_image'];
			mod.model_date = timezone.now()
			mod.model_author = request.user
			mod.model_category = category
			mod.model_tags = request.POST['model_tags'].replace(' ', '').split(',')
			mod.model_tool = request.POST['model_tool']
			mod.model_link = uuid.uuid4().hex
			mod.save()

			category.amount+=1
			category.save()

			return HttpResponseRedirect(reverse('user:profile'))
		else:
			request.session['modelupload_error'] = 'Please check your data and submit again.'
			return HttpResponseRedirect(reverse('model:modelupload'))



def modelView(request, id):
	categories = Category.objects.all()
	model = get_object_or_404(Mod, id = id)
	model.model_views+=1
	model.save()

	referer = request.META.get('HTTP_REFERER')
	return render(request, 'model/modelview.html', {'model': model, 'categories': categories, 'referer': referer})



@login_required
def deleteModel(request, id):
	mod = get_object_or_404(Mod, id = id)

	if request.user.username != mod.model_author.username:
		return securityCheck(request)

	category = get_object_or_404(Category, name = mod.model_category)
	category.amount -= 1
	category.save()
	mod.delete()

	return HttpResponseRedirect(reverse('user:profile'))



@login_required
def downloadModel(request, link):
	model = get_object_or_404(Mod, model_link = link)
	
	path = model.model_file.url
	filename = f'{model.model_name}.{model.model_file.name[len(model.model_file.name)-3:]}'
	mime_type, _ = mimetypes.guess_type(path)
	response = HttpResponse(model.model_file, content_type=mime_type)
	response['Content-Disposition'] = "attachment; filename=%s" % filename
	return response



def modelEdit(request, id):
	model = get_object_or_404(Mod, id=id)

	if model.model_author.username != request.user.username:
		return securityCheck(request)

	allowPrice = True
	categories = Category.objects.all()

	if request.user.author.stripe_account == -1:
		allowPrice = False

	return render(request, 'model/modelEdit.html', {'model': model, 'categories': categories, 'allowPrice': allowPrice})


def modelEditHandle(request, id):
	if request.method == 'POST':
		model = get_object_or_404(Mod, id=id)
		model.model_name = request.POST['name']
		model.model_price = request.POST['price']
		model.model_author_price = request.POST['author_price']
		model.model_tags = request.POST['tags'].replace(' ', '').split(',')
		model.model_tool = request.POST['tool']
		model.model_desc = request.POST['desc']
		model.model_category = get_object_or_404(Category, name = request.POST['cat'])
		model.model_date = timezone.now()
		model.save()
		return HttpResponseRedirect(reverse('main:dashboard'))
	else:
		request.session['profile_message'] = 'Error occured while handling operation.'
		request.session['profile_message_type'] = 'danger'
		return HttpResponseRedirect(reverse('user:profile'))





def securityCheck(request):
	if request.user.is_staff:
		return HttpResponseRedirect(reverse('main:dashboard'))

	request.user.author.warnings += 1
	if request.user.author.warnings >= 5:
		guilty = request.user
		admin = get_object_or_404(Author, username = 'admin')
		modelset = Mod.objects.filter(model_author = guilty)
		for model in modelset:
			model.model_author = admin
			model.save()
		logout(request)
		guilty.delete()
		return	HttpResponseRedirect(reverse('main:index'))

	request.user.author.notifications.append({'title':'Warning!', 'message':f'We detected, suspicious activity on your account. We will delete your account, if you will continue illegal activity. Warnings {request.user.author.warnings}/5'})
	request.user.author.save()
	return	HttpResponseRedirect(reverse('main:dashboard'))