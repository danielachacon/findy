from django.utils.timezone import localtime
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.core.mail import send_mail
from main.models import Event
from datetime import timedelta

class Command(BaseCommand):
    help = 'Send event reminders to users 30 minutes before the event starts.'

    def handle(self, *args, **kwargs):
        upcoming_events = Event.objects.filter(start_time__lte=now() + timedelta(minutes=30), start_time__gt=now())
        for event in upcoming_events:
            registered_users = event.registered_users.all()
            for user in registered_users:
                try:
                    send_mail(
                        subject=f"Reminder: {event.title} starts in 30 minutes!",
                        message=(
                            f"Hi {user.username},\n\n"
                            f"This is a reminder that the event '{event.title}' will start on {event_start_time}.\n\n"
                            f"Location: {event.location}\n\n"
                            f"Thank you,\nFindy Team"
                        ),
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[user.email],
                        fail_silently=True,
                    )
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Failed to email {user.email}: {e}"))
        self.stdout.write(self.style.SUCCESS('Event reminders sent successfully.'))