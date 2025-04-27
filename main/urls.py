from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('create-event/', views.create_event_view, name='create_event'),
    path('events/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('events/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('events/unregister/<int:event_id>/',views.unregister_event, name='unregister_event'),
    path('event/<int:event_id>/star/', views.toggle_star_event, name='toggle_star_event'),
    path('event/<int:event_id>/make_announcement/', views.make_announcement, name='make_announcement'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('event/<int:event_id>/join-waitlist/', views.join_waitlist, name='join_waitlist'),
    path('event/<int:event_id>/leave-waitlist/', views.leave_waitlist, name='leave_waitlist'),
    path('validate-code/<int:event_id>/', views.validate_event_code, name='validate_event_code'),
    path('userprofile/', include('userprofile.urls')),
]