from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start, name='home.start'),
    path('about/', views.about, name='home.about'),
]