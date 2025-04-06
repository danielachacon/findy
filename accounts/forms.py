from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class CustomRegisterForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")

        if User.objects.filter(username=username).exists():
            self.add_error('username', 'Username already exists.')
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Email already in use.')
        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')
        if email and len(email) > 10 and email[-11:] != '@gatech.edu':
            self.add_error('email', 'Please use your Georgia Tech email (e.g., username@gatech.edu)')
        return cleaned_data