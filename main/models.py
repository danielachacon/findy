from django.contrib.auth import get_user_model
from django.db import models
import uuid
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.utils.timezone import now
from django.utils import timezone


User = get_user_model()

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_capacity = models.PositiveIntegerField(default=100)
    location = models.CharField(max_length=255)
    custom_lat = models.FloatField(null=True, blank=True)
    custom_lng = models.FloatField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    created_at = models.DateTimeField(auto_now_add=True)
    reminder_sent = models.BooleanField(default=False)

    registered_users = models.ManyToManyField(
        User,
        through='Registration',
        related_name='registered_events',
        blank=True,
    )

    starred_by = models.ManyToManyField(
        User,
        related_name='starred_events',
        blank=True
    )

    def get_registration_count(self):
        return self.registered_users.count()

    def is_full(self):
        return self.get_registration_count() >= self.max_capacity

    def __str__(self):
        return f"{self.title} @ {self.start_time.strftime('%b %d, %Y %I:%M %p')}"

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_code = models.UUIDField(unique=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    class Meta:
        unique_together = ('user', 'event')

    def delete(self, *args, **kwargs):
        event = self.event
        super().delete(*args, **kwargs)
        
        first_in_line = event.waitlist_entries.first()
        if first_in_line:
            Registration.objects.create(
                user=first_in_line.user,
                event=event
            )
            first_in_line.delete()
            
            send_mail(
                f'Spot Available in {event.title}',
                f'A spot has opened up in {event.title} and you have been automatically registered!',
                'from@example.com',
                [first_in_line.user.email],
                fail_silently=True,
            )

    def __str__(self):
        return f"{self.event} @ {self.user.username} : Code: {self.registration_code}"
    
    def save(self, *args, **kwargs):
        if not self.registration_code:
            self.registration_code = uuid.uuid4()
        if not self.qr_code:
            self.generate_qr_code()
        super().save(*args, **kwargs)

    
    def generate_qr_code(self):
        qr = qrcode.QRCode(version=1, box_size=4, border=5)
        data = f"Event: {self.event.title}\nUser: {self.user.username}\nCode: {self.registration_code}"
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        filename = f'qr_{self.event.id}_{self.user.id}_{self.registration_code}.png'
        self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)
        
    def delete_qr(self, *args, **kwargs):
        if self.qr_code:
            self.qr_code.delete(save=False)
        super().delete(*args, **kwargs)


class Announcement(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='announcements')
    message = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements')
    created_at = models.DateTimeField(auto_now_add=True)
    dismissed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Announcement for {self.event.title} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class Waitlist(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='waitlist_entries')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='waitlisted_events')
    position = models.PositiveIntegerField()

    class Meta:
        unique_together = ('user', 'event')
        ordering = ['position']

    def __str__(self):
        return f"{self.user.username} - #{self.position} for {self.event.title}"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='feedbacks')
    feedback = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'event')
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback by {self.user.username} for {self.event.title}"
