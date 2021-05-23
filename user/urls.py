from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
	path('registration', views.registration, name = 'registration'),
	path('registration/create_user', views.create_user, name = 'create_user'),
	path('login', views.loginform, name = 'loginform'),
	path('login/handle', views.loginUser, name = 'loginUser'),

	path('profile', views.profile, name = 'profile'),
	path('profile/favourites', views.user_favs, name = 'user_favs'),
	path('profile/cart', views.user_cart, name = 'user_cart'),
	path('profile/archive', views.user_archive, name = 'user_archive'),
	path('profile/logout', views.user_logout, name = 'user_logout'),
	path('profile/settings&<str:type>', views.user_settings, name = 'user_settings'),
	path('profile/settings/changesettings', views.changeSettings, name = 'changeSettings'),
	path('profile/settings/changepass', views.changeSecurity, name = 'changeSecurity'),
	path('profile/coins', views.userCoins, name = 'userCoins'),
]