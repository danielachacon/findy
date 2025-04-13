from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    registered_users = models.ManyToManyField(
        User,
        through='Registration',
        related_name='registered_events',
        blank=True,
    )

    def __str__(self):
        return f"{self.title} @ {self.start_time.strftime('%b %d, %Y %I:%M %p')}"

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.event} @ {self.user.username}"