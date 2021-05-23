from django.urls import path

from . import views

app_name = 'chat'

urlpatterns =  [
	path('handle', views.handle, name = 'handle'),
	path('update', views.update, name = 'update'),
]