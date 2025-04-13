from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
] 