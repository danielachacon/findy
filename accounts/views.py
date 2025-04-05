from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from .forms import CustomRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from .email import send_verification_email
from django.contrib.sites.shortcuts import get_current_site

User = get_user_model()
def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False

            user.token = default_token_generator.make_token(user)

            user.save()
            send_verification_email(user, request)

            login(request, user)

            login_url = f"{request.scheme}://{get_current_site(request).domain}/accounts/login/"

            return render(request, 'accounts/verification_screen.html', {
                'user': user,
                'login_url': login_url,
            })
        else:
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = CustomRegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                login(request, user)
                return render(request, 'accounts/login_success.html', {'user': user})
            else:
                error_message = "Your account is inactive. Please verify your email to activate your account."
                return render(request, 'accounts/login.html', {'form': form, 'error_message': error_message})
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})