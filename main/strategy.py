from abc import ABC, abstractmethod
from django.core.mail import send_mail


class NotificationStrategy(ABC):
    @abstractmethod
    def notify(self, event, user):
        pass


class EmailWaitlistStrategy(NotificationStrategy):
    def notify(self, event, user):
        send_mail(
            f'Spot Available in {event.title}',
            f'A spot has opened up in {event.title} and you have been automatically registered!',
            'from@example.com',
            [user.email],
            fail_silently=True,
        )


class NotificationContext:
    def __init__(self, strategy=None):
        self.strategy = strategy or EmailWaitlistStrategy()

    def notify(self, event, user):
        self.strategy.notify(event, user)
