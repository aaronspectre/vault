from django.contrib import admin

from .models import PaymentSession, Debt

admin.site.register(PaymentSession)
admin.site.register(Debt)