from django.urls import path
from . import views
from .email import verify_email

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('verify/<str:uidb64>/<str:token>/', verify_email, name='verify_email'),
]