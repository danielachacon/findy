from django import forms
from django.forms import ModelForm, DateTimeInput, Select
from .models import Event
from .locations import GTLocations
from django.utils import timezone

class EventSearchForm(forms.Form):
    event_title = forms.CharField(max_length=100, required=False)

    start_time_min = forms.DateTimeField(
        required=False,
        widget=forms.TextInput(attrs={'type': 'datetime-local'})
    )
    end_time_max = forms.DateTimeField(
        required=False,
        widget=forms.TextInput(attrs={'type': 'datetime-local'})
    )

    location = forms.ChoiceField(
        choices=[('', 'All Locations')] + [(key, value) for key, value in GTLocations._locations.items()],
        required=False
    )

    is_full = forms.ChoiceField(
        choices=[
            ('', 'All Events'),
            ('False', 'Only Not Full')
        ],
        required=False
    )

class CustomEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time', 'max_capacity', 'location']
        widgets = {
            'start_time': DateTimeInput(attrs={
                'class': 'datetimepicker',
                'placeholder': 'Select start time'
            }),
            'end_time': DateTimeInput(attrs={
                'class': 'datetimepicker',
                'placeholder': 'Select end time'
            }),
            'location': Select(attrs={
                'class': 'location-select',
                'style': 'width: 100%; height: 40px;'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        locations = [
            (name, f"{name}")
            for name, data in GTLocations._locations.items()
        ]
        locations.append(('Custom', 'Custom'))

        self.fields['location'].choices = locations

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        max_capacity = cleaned_data.get('max_capacity')
        location = cleaned_data.get('location')

        if start_time and start_time < timezone.now():
            self.add_error('start_time', 'Start time cannot be in the past.')
        if start_time and end_time and end_time <= start_time:
            self.add_error('start_time', 'Start time must be before end time.')
        if max_capacity is not None and max_capacity <= 0:
            self.add_error('max_capacity', 'Max capacity must be greater than 0.')
        return cleaned_data