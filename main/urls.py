from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('events/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('events/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('events/unregister/<int:event_id>/',views.unregister_event, name='unregister_event'),
    path('event/<int:event_id>/star/', views.toggle_star_event, name='toggle_star_event')
]