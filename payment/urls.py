from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
	path('cart', views.showCart, name = 'showcart'),
	path('vip', views.showVip, name = 'showvip'),
	path('stripeaccount', views.stripeAccount, name = 'stripeaccount'),

	path('checkout-session/<int:total>-<int:amount>', views.checkout_session_view, name = 'checkout-session'),
	path('checkout/success', views.checkout_session_view_success, name = 'checkout-session-success'),
	path('checkout/cancel', views.checkout_session_view_success, name = 'checkout-session-cancel'),

	path('vip-purchase', views.vip_purchase, name = 'vip_purchase'),
	path('vip/success', views.vip_purchase_success, name = 'vip-purchase-success'),
	path('vip/cancel', views.vip_purchase_cancel, name = 'vip-purchase-cancel'),

	path('webhooks/stripe', views.stripe_webhook, name = 'stripe-webhook'),
]