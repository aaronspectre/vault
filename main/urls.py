from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
	path('', views.index, name = 'index'),
	path('dashboard', views.dashboard, name = 'dashboard'),
	path('dashboard/deleteNote', views.deleteNote, name = 'deleteNote'),
]