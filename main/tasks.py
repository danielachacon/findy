from django.utils.timezone import now, timedelta
from django.conf import settings
from django.core.mail import send_mail
from .models import Event
import pytz

def send_event_reminders():
    eastern = pytz.timezone('America/New_York')

    upcoming_events = Event.objects.filter(
        start_time__lte=now() + timedelta(minutes=30),
        start_time__gt=now(),
        reminder_sent=False
    )
    for event in upcoming_events:
        local_start_time = event.start_time.astimezone(eastern)

        for user in event.registered_users.all():
            send_mail(
                subject=f"Reminder: {event.title} starts in 30 minutes!",
                message=(
                    f"Hi {user.username},\n\n"
                    f"This is a reminder that the event '{event.title}' will start at "
                    f"{local_start_time.strftime('%B %d, %Y at %I:%M %p %Z')}.\n\n"
                    f"Location: {event.location}\n\n"
                    f"Thank you,\nFindy Team"
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=True,
            )
        event.reminder_sent = True
        event.save()