from django.urls import path

from . import views

app_name = 'engine'

urlpatterns = [
	path('search/', views.searchEngine, name = 'searchengine'),
	path('stranger/<str:username>', views.stranger, name = 'stranger'),
	path('friend', views.findFriend, name = 'friend'),

	path('report', views.sendReport, name = 'report'),

	path('add/', views.addTo, name = 'addto'),
	path('remove/', views.removeFrom, name = 'removefrom'),
]