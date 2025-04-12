from django.utils import timezone
from django import forms
from django.forms.widgets import DateTimeInput

class CustomEventForm(forms.Form):
    name = forms.CharField(max_length=100, required=True),
    email = forms.EmailField(max_length=100, required=True),

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
    location = forms.CharField(max_length=100, required=True)

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if start_time and start_time < timezone.now():
            self.add_error('start_time', 'Start time cannot be in the past.')
        if start_time and end_time and end_time <= start_time:
            self.add_error('start_time', 'Start time must be before end time.')
        return cleaned_data