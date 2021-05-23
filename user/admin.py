from django.contrib import admin

# Register your models here.
from .models import StripeAccount, Author

admin.site.register(StripeAccount)
admin.site.register(Author)