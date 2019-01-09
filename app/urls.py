from django.urls import path
from .views import * 

urlpatterns = [
    path('', index, name='index'),
    path('append', append, name='append'),
    path('edit', edit, name='edit'),
    path('upload', find_images, name='upload')
]
