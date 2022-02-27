from django.urls import path
from model import views

app_name = 'model'

urlpatterns = [
	path('upload', views.modelupload, name = 'modelupload'),
	path('upload/handle', views.upload, name = 'upload'),
	path('delete/<int:id>', views.deleteModel, name = 'delete'),
	path('download/<slug:link>', views.downloadModel, name = 'download'),
	path('view/<int:id>', views.modelView, name = 'modelview'),
	path('edit/<int:id>', views.modelEdit, name = 'modeledit'),
	path('edit/handle/<int:id>', views.modelEditHandle, name = 'modeledithandle'),
]