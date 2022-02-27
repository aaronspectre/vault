import json

from django.conf import settings

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from model.models import Mod
from user.models import Author
from .models import PaymentSession



#Handle payment
@login_required
def showCart(request):
	modelset = Mod.objects.filter(id__in = request.user.author.cart)
	return render(request, 'payment/showCart.html', {'modelset': modelset})