from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
] 