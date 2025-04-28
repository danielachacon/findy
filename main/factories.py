from abc import ABC, abstractmethod
from .models import Event

#This is the abstract interface for the factory design pattern
class EventFactoryInterface(ABC):
    @abstractmethod
    def create_event(self, form_data, user, custom_location=None, custom_lat=None, custom_lng=None):
        pass

#This is the concrete implementation for the factory design pattern, that has the logic for making concrete events
class ConcreteEventFactory(EventFactoryInterface):
    def create_event(self, form_data, user, custom_location=None, custom_lat=None, custom_lng=None):
        location_value = form_data['location']

        if location_value == "Custom" and custom_location:
            location_value = custom_location

        event = Event.objects.create(
            title=form_data['title'],
            description=form_data['description'],
            start_time=form_data['start_time'],
            end_time=form_data['end_time'],
            max_capacity=form_data['max_capacity'],
            location=location_value,
            created_by=user
    )
        if custom_lat and custom_lng:
            event.custom_lat = float(custom_lat)
            event.custom_lng = float(custom_lng)
            event.save()
        return event
