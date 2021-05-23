import json

from django.shortcuts import render, get_object_or_404

from model.models import Mod, Category
from user.models import Author

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt



def searchEngine(request):
	if request.method == 'GET':
		categories = Category.objects.all()
		if request.GET['type'] == 'byname':
			modelset = Mod.objects.filter(model_name__icontains = request.GET['query'])
			return render(request, 'engine/result.html', {'query': request.GET['query'], 'modelset': modelset, 'categories': categories})
		elif request.GET['type'] == 'category':
			modelset = Mod.objects.filter(model_category = Category.objects.get(name = request.GET['query']))
			return render(request, 'engine/result.html', {'query': request.GET['query'], 'categories': categories, 'modelset': modelset})
		elif request.GET['type'] == 'filter':
			if request.GET['query'] == 'all':
				modelset = Mod.objects.all()[:20]
			elif request.GET['query'] == 'new':
				modelset = Mod.objects.order_by('-model_date')[:20]
			elif request.GET['query'] == 'popular':
				modelset = Mod.objects.order_by('-model_views')[:20]
			else:
				modelset = Mod.objects.all()[:20]

			return render(request, 'engine/result.html', {'query': request.GET['query'], 'categories': categories, 'modelset': modelset})

		else:
			return HttpResponseRedirect(reverse('main:dashboard'))




def stranger(request, username):
	strangerUser = Author.objects.get(username = username)
	if request.user.username == strangerUser.username:
		return HttpResponseRedirect(reverse('user:profile'))
	modelset = Mod.objects.filter(model_author = strangerUser)
	return render(request, 'engine/stranger.html', {'stranger': strangerUser, 'modelset': modelset})



def findFriend(request):
	topusers = Author.objects.order_by('coins').exclude(username = request.user)
	userset = Author.objects.filter(username__icontains = request.POST['query']).exclude(username = request.user.username)
	return render(request, 'user/coins.html', {'userset': userset, 'topusers': topusers})



@csrf_exempt
@login_required
def sendReport(request):
	body = json.loads(request.body)
	message = body['reason']

	user = get_object_or_404(Author, username = body['user'])
	sender = get_object_or_404(Author, username = body['sender'])
	user.reports.append({'sender': sender.username, 'reason': message})
	user.save()

	if len(user.reports) >= 3:
		admin = get_object_or_404(Author, id = 1)
		admin.notifications.append({'title': 'Check request', 'message': f'Reachred report limit for {user.username}.'})
		admin.save()

	return HttpResponse(status=200)


@login_required
def addTo(request, *args):
	#Adding to Favs
	if request.GET['to'] == 'favs':
		if validateAdd(request, request.user.author.favs, request.GET['model_id']):
			return HttpResponseRedirect(reverse('user:user_favs'))
		if Mod.objects.get(id = request.GET['model_id']).model_author == request.user.author:
			return HttpResponseRedirect(reverse('user:user_favs'))
		request.user.author.favs.append(request.GET['model_id'])
		request.user.author.save()
		model = Mod.objects.get(id = request.GET['model_id'])
		model.model_favs += 1
		model.save()
		return HttpResponseRedirect(reverse('user:user_favs'))


	#Adding to Cart
	elif request.GET['to'] == 'cart':
		if validateAdd(request, request.user.author.cart, request.GET['model_id']):
			return HttpResponseRedirect(reverse('user:user_cart'))
		request.user.author.cart.append(request.GET['model_id'])
		request.user.author.save()
		return HttpResponseRedirect(reverse('user:user_cart'))


	#Adding to Subs
	elif request.GET['to'] == 'subs':
		suser = get_object_or_404(Author, id = request.GET['userid'])
		if validateAdd(request, suser.coins, request.user.id):
			return HttpResponseRedirect(reverse(request.GET['back'], args=(suser.username,)))
		suser.coins.append(request.user.id)
		suser.save()
		if request.GET['back'] == 'stranger':
			return HttpResponseRedirect(reverse('engine:stranger', args=(suser.username,)))
		else:
			return HttpResponseRedirect(reverse('user:userCoins'))

	else:
		return HttpResponseRedirect(reverse('main:index'))



@login_required
def removeFrom(request, *args):
	if request.GET['from'] == 'favs':
		request.user.author.favs.remove(request.GET['model_id'])
		request.user.author.save()
		return HttpResponseRedirect(reverse('user:user_favs'))
	elif request.GET['from'] == 'cart':
		request.user.author.cart.remove(request.GET['model_id'])
		request.user.author.save()
		return HttpResponseRedirect(reverse('user:user_cart'))
	elif request.GET['from'] == 'subs':
		suser = get_object_or_404(Author, id = request.GET['userid'])
		suser.coins.remove(request.user.id)
		suser.save()
		if request.GET['back'] == 'stranger':
			return HttpResponseRedirect(reverse('engine:stranger', args=(suser.username,)))
		else:
			return HttpResponseRedirect(reverse('user:userCoins'))
	else:
		return HttpResponseRedirect(reverse('main:index'))


def validateAdd(request, item, element):
	if element in item:
		return True