from django.utils import timezone
from django import forms
from django.forms.widgets import DateTimeInput, Select
from .locations import GTLocations

class CustomEventForm(forms.Form):
    title = forms.CharField(max_length=50, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    start_time = forms.DateTimeField(
        required=True,
        widget=DateTimeInput(attrs={
            'class': 'datetimepicker',
            'placeholder': 'Select start time'
        })
    )
    end_time = forms.DateTimeField(
        required=True,
        widget=DateTimeInput(attrs={
            'class': 'datetimepicker',
            'placeholder': 'Select end time'
        })
    )
    
    LOCATION_CHOICES = [(location, location) for location in GTLocations.get_location_names()]

    LOCATION_CHOICES.append(("Custom", "Custom"))
    
    location = forms.ChoiceField(
        choices=LOCATION_CHOICES, 
        required=True,
        widget=Select(attrs={
            'class': 'location-select',
            'style': 'width: 100%; height: 40px;'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if start_time and start_time < timezone.now():
            self.add_error('start_time', 'Start time cannot be in the past.')
        if start_time and end_time and end_time <= start_time:
            self.add_error('start_time', 'Start time must be before end time.')
        return cleaned_data