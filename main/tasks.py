from celery import shared_task
from django.utils import timezone
from .models import Event
from django.contrib.auth import get_user_model

@shared_task
def create_30_minute_reminders():
    now = timezone.now()
    upcoming_window_start = now
    upcoming_window_end = now + timedelta(minutes=30)

    events = Event.objects.filter(start_time__range=(upcoming_window_start, upcoming_window_end))

    for event in events:
        registered_users = event.registered_users.all()
        for user in registered_users:
            exists = Announcement.objects.filter(
                event=event,
                created_by=user,
                special_type="30_min_reminder"
            ).exists()

            if not exists:
                Announcement.objects.create(
                    event=event,
                    message=f"Reminder: '{event.title}' starts soon!",
                    created_by=user,
                    special_type="30_min_reminder"
                )
                console.log("created reminder!");