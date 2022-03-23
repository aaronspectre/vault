import json

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import hashers
from django.utils import timezone
from django.core.files import File
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from model.models import Mod
from user.models import Author


def registration(request):
	defaultimg = '/static/main/img/avatar.jpeg'

	file = open('static/currency.list', 'r')
	currencies = json.loads(file.read())
	file.close()
	file = open('static/country.list', 'r')
	countries = json.loads(file.read())
	file.close()
	file = open('static/country.name', 'r')
	countrynames = json.loads(file.read())
	file.close()

	error = None
	if 'reg_error' in request.session.keys():
		error = request.session['reg_error']
	return render(request, 'user/regform.html', {'error': error, 'defimg': defaultimg, 'countries': countries, 'currencies': currencies, 'names': countrynames})


def create_user(request):

	#Passwords match validation
	if request.POST['pass'] == request.POST['cpass']:

		#User exist validation
		if len(Author.objects.filter(username = request.POST['username'])) != 0:
			request.session['reg_error'] = 'User already exists'
			return HttpResponseRedirect(reverse('user:registration'))

		user = Author()
		user.username = request.POST['username']
		user.first_name = request.POST['fname']
		user.last_name = request.POST['lname']
		user.email = request.POST['email']
		user.bio = request.POST['bio']
		user.website = request.POST['website']
		user.phone = request.POST['phone']
		user.favtool = request.POST['tool']
		user.credit = request.POST['credit']
		user.set_password(request.POST['pass'])

		avatar = open('static/main/img/avatar.jpeg', 'rb')
		user.avatar.save(user.username+'.jpeg', File(avatar))
		avatar.close()


		#Defining default values
		if len(request.POST['location'].replace(' ', '')) != 0: user.location = request.POST['location']
		if user.first_name.replace(' ', '') == '': user.first_name = 'WALL-E'
		if user.last_name.replace(' ', '') == '': user.last_name = 'SkyNet'

		#Return 200 code
		user.save()
		login(request, user)
		return HttpResponseRedirect(reverse('main:dashboard'))
	else:
		request.session['reg_error'] = 'Passwords don`t match'
		return HttpResponseRedirect(reverse('user:registration'))



def loginform(request):
	error = None
	if 'login_error' in request.session.keys():
		error = request.session['login_error']
	return render(request, 'user/loginform.html', {'error': error})

def loginUser(request):
	username = request.POST['username']
	password = request.POST['pass']
	user = authenticate(request, username = username, password = password)
	if user is not None:
		login(request, user)
		return HttpResponseRedirect(reverse('main:dashboard'))
	else:
		request.session['login_error'] = 'Incorrect password or username'
		return HttpResponseRedirect(reverse('user:loginform'))




@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('user:loginform'))






@login_required
def profile(request):
	message = {'message': False}
	if 'profile_message' in request.session.keys():
		message['message'] = request.session['profile_message']
		message['type'] = request.session['profile_message_type']
		request.session['profile_message'] = False
	modelset = Mod.objects.filter(model_author = request.user)
	return render(request, 'user/profile.html', {'modelset': modelset, 'type': 'models', 'message': message})

@login_required
def user_favs(request):
	modelset = Mod.objects.filter(id__in = request.user.author.favs)
	return render(request, 'user/profile.html', {'modelset': modelset, 'type': 'favourites'})

@login_required
def user_cart(request):
	modelset = Mod.objects.filter(id__in = request.user.author.cart)
	return render(request, 'user/profile.html', {'modelset': modelset, 'type': 'cart'})

@login_required
def user_archive(request):
	modelset = Mod.objects.filter(id__in = request.user.author.bought)
	return render(request, 'user/profile.html', {'modelset': modelset, 'type': 'archive'})

@login_required
def user_settings(request, type):
	error = None
	if 'change_error' in request.session.keys():
		error = request.session['change_error']
		request.session['change_error'] = None

	if type == 'Payment Accounts':
		if request.user.author.stripe_account != -1:
			return render(request, 'user/userSettings.html', {'type': type, 'error': error})


	return render(request, 'user/userSettings.html', {'type': type, 'error': error})




@login_required
def changeSecurity(request):
	print('I')
	if request.method == 'POST':
		user = get_object_or_404(Author, username = request.user)
		if hashers.check_password(request.POST['opass'], user.password):
			if request.POST['pass'].replace(' ', '') == '' or request.POST['cpass'].replace(' ', '') == '':
				request.session['change_error'] = 'Fill all fields'
				return HttpResponseRedirect(reverse('user:user_settings', args=('Security',)))

			if request.POST['pass'] == request.POST['cpass']:
				user.set_password(request.POST['pass'])
				request.session['profile_message'] = 'Security options changed successfuly!'
				request.session['profile_message_type'] = 'profile-message-success'
				return HttpResponseRedirect(reverse('user:profile'))
			else:
				request.session['change_error'] = 'New Passwords don`t match'
				return HttpResponseRedirect(reverse('user:user_settings', args=('Security',)))
		else:
			request.session['change_error'] = 'Incorrect old password'
			print('old')
			return HttpResponseRedirect(reverse('user:user_settings', args=('Security',)))


@login_required
def changeSettings(request, *args):
	if request.method == 'POST':
		user = get_object_or_404(Author, username = request.user)
		user.first_name = request.POST['fname']
		user.last_name = request.POST['sname']
		user.credit = request.POST['card']
		user.location = request.POST['location']
		user.phone = request.POST['phone']
		user.gender = request.POST['gender']
		user.website = request.POST['website']
		user.favtool = request.POST['tool']
		user.bio = request.POST['bio']
		if 'avatar' in request.FILES.keys():
			user.avatar = request.FILES['avatar']

		user.save()
		request.session['profile_message'] = 'Settings changes saved successfuly!'
		request.session['profile_message_type'] = 'profile-message-success'
	return HttpResponseRedirect(reverse('user:profile'))




@login_required
def userCoins(request, *args):
	topusers = Author.objects.order_by('coins').exclude(username = request.user)
	userset = Author.objects.filter(id__in = request.user.author.coins)
	return render(request, 'user/coins.html', {'userset': userset, 'topusers': topusers})
