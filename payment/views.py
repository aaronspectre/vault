import stripe
import json

from django.conf import settings

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from model.models import Mod
from user.models import Author, StripeAccount
from .models import PaymentSession, Debt


stripe.api_key = settings.STRIPE_PRIVATE_KEY



#Handle payment
@login_required
def showCart(request):
	modelset = Mod.objects.filter(id__in = request.user.author.cart)
	return render(request, 'payment/showCart.html', {'modelset': modelset, 'public_key': settings.STRIPE_PUBLIC_KEY})


@login_required
def showVip(request):
	return render(request, 'payment/showVip.html', {'public_key': settings.STRIPE_PUBLIC_KEY})




@login_required
def checkout_session_view(request, total, amount):
	YOUR_DOMAIN = 'http://localhost:8000'
	checkout_session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[
			{
				'price_data': {
					'currency': 'usd',
					'unit_amount': int(total),
					'product_data': {
						'name': f'Set of 3d models ({amount})'
					},
				},
				'quantity': 1,
			},
		],
		metadata = {'models': json.loads(request.body), 'author': request.user.username},
		mode='payment',
		success_url=YOUR_DOMAIN + '/payment/checkout/success',
		cancel_url=YOUR_DOMAIN + '/payment/checkout/cancel',
	)
	return JsonResponse({'id': checkout_session.id})


@login_required
def checkout_session_view_success(request):
	# request.user.author.cart = []
	request.user.author.save()
	request.session['profile_message'] = 'Payment Successfuly completed! Go to your Archive to Download.'
	request.session['profile_message_type'] = 'profile-message-success'
	return HttpResponseRedirect(reverse('user:profile'))

@login_required
def checkout_session_view_cancel(request):
	request.session['profile_message'] = 'Error occured during payment.'
	request.session['profile_message_type'] = 'profile-message-danger'
	return HttpResponseRedirect(reverse('user:profile'))








@login_required
def vip_purchase(request):
	YOUR_DOMAIN = 'http://localhost:8000'
	body = json.loads(request.body)
	tariff = body['tariff']
	price = body['price']
	checkout_session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[
			{
				'price_data': {
					'currency': 'usd',
					'unit_amount': price,
					'product_data': {
						'name': f'VIP status: {tariff}'
					},
				},
				'quantity': 1,
			},
		],
		metadata = {'author': request.user.username, 'vip': True},
		mode='payment',
		success_url=YOUR_DOMAIN + '/payment/vip/success',
		cancel_url=YOUR_DOMAIN + '/payment/vip/cancel',
	)
	return JsonResponse({'id': checkout_session.id})


@login_required
def vip_purchase_success(request):
	request.session['profile_message'] = 'Payment Successfuly completed! Now you have VIP status!'
	request.session['profile_message_type'] = 'profile-message-success'
	return HttpResponseRedirect(reverse('user:profile'))


@login_required
def vip_purchase_cancel(request):
	request.session['profile_message'] = 'Error occured during payment. Try again later.'
	request.session['profile_message_type'] = 'profile-message-danger'
	return HttpResponseRedirect(reverse('user:profile'))







@csrf_exempt
def stripe_webhook(request):
	payload = request.body
	sig_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None

	try:
		event = stripe.Webhook.construct_event(
			payload, sig_header, settings.STRIPE_WEBHOOK_KEY
		)
	except ValueError as e:
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		return HttpResponse(status=400)


	#Money transfer succeess event
	if event['type'] == 'checkout.session.completed':
		session = event['data']['object']
		author = get_object_or_404(Author, username = session['metadata']['author'])

		if 'vip' in session['metadata'].keys():
			author.vipstatus = True
			author.save()
			return HttpResponse(status=200)


		modelset = Mod.objects.filter(id__in = json.loads(session['metadata']['models']))


		payment = PaymentSession()
		payment.customer_email = session['customer_details']['email']
		payment.user = author
		payment.stripe_customer_id = session['id']
		payment.stripe_customer = session['customer']
		payment.intent = session['payment_intent']
		payment.modelset = json.loads(session['metadata']['models'])
		payment.date = timezone.now()
		payment.amount = session['amount_total']
		payment.save()

		author.payments.append(payment.id)
		modelset = Mod.objects.filter(id__in = json.loads(session['metadata']['models']))
		for model in modelset:
			if model.id not in author.bought:
				author.bought.append(model.id)
		author.save()

		separateTransfer(session)


	#Account creation event
	elif event['type'] == 'account.updated':
		session = event['data']['object']
		user = get_object_or_404(Author, username = session['metadata']['user'])


		if user.stripe_account == -1 and session['details_submitted']:
			account = StripeAccount()
			account.account_id = session['id']
			account.email = session['email']
			account.country = session['country']
			account.business_profile = session['business_profile']
			account.external_account = session['external_accounts']['data'][0]
			account.charges_enabled = session['charges_enabled']
			account.transfers = session['capabilities']['transfers']
			account.submitted = session['details_submitted']
			account.save()
			user.stripe_account = account.id
			user.save()

		elif user.stripe_account != -1 and session['details_submitted']:
			account = get_object_or_404(StripeAccount, id = user.stripe_account)
			account.email = session['email']
			account.country = session['country']
			account.business_profile = session['business_profile']
			account.external_account = session['external_accounts']
			account.charges_enabled = session['charges_enabled']
			account.transfers = session['capabilities']['transfers']
			account.submitted = session['details_submitted']
			account.save()

		elif user.stripe_account == -1 and session['details_submitted'] == False:
			account = StripeAccount()
			account.account_id = session['id']
			account.email = session['email']
			account.country = session['country']
			account.business_profile = session['business_profile']
			account.charges_enabled = session['charges_enabled']
			account.transfers = session['capabilities']['transfers']
			account.submitted = session['details_submitted']
			account.save()
			user.stripe_account = account.id
			user.save()

		elif user.stripe_account != -1 and session['details_submitted'] == False:
			account = get_object_or_404(StripeAccount, id = user.stripe_account)
			account.email = session['email']
			account.country = session['country']
			account.business_profile = session['business_profile']
			account.external_account = session['external_accounts']
			account.charges_enabled = session['charges_enabled']
			account.transfers = session['capabilities']['transfers']
			account.submitted = session['details_submitted']
			account.save()


	return HttpResponse(status=200)



def separateTransfer(session):
	modelset = json.loads(session['metadata']['models'])

	for item in modelset:
		model = get_object_or_404(Mod, id = item)
		debt = Debt()
		debt.amount = model.model_price
		debt.account_id = model.model_author.author.stripe_account
		debt.model = model
		debt.email = model.model_author.email
		debt.save()

	# for model in modelset:
	# 	user = get_object_or_404(Author, username = model.model_author)
	# 	destination = get_object_or_404(StripeAccount, id = user.stripe_account)

	# 	transfer = stripe.Transfer.create(
	# 		amount = model.model_price*100,
	# 		currency = 'usd',
	# 		destination = destination,
	# 	)





@login_required
def stripeAccount(request):

	if request.user.author.stripe_account != -1:
		stripeAcc = get_object_or_404(StripeAccount, id = request.user.author.stripe_account)
		account = stripe.Account.retrieve(stripeAcc.account_id)

		link = stripe.AccountLink.create(
			account = account.id,
			refresh_url = 'http://localhost:8000/payment/stripeaccount',
			return_url = 'http://localhost:8000/user/profile',
			type = 'account_onboarding',
		)

	else:
		account = stripe.Account.create(
			type='express',
			capabilities={
				'card_payments': {
					'requested': True
				},
				'transfers': {
					'requested': True
				}
			},
			metadata = {'user': request.user.username},
		)

		link = stripe.AccountLink.create(
			account = account.id,
			refresh_url = 'http://localhost:8000/paymnet/stripeaccount',
			return_url = 'http://localhost:8000/user/profile',
			type = 'account_onboarding',
		)

	return HttpResponseRedirect(link.url)