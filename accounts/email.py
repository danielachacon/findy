from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model

User = get_user_model()

def send_verification_email(user, request):
    uid = urlsafe_base64_encode(str(user.pk).encode())
    token_url = f"{request.scheme}://{get_current_site(request).domain}/accounts/verify/{uid}/{user.token}/"
    login_url = f"{request.scheme}://{get_current_site(request).domain}/accounts/login/"
    subject = "Email Verification"
    message = render_to_string('accounts/verification_email.html', {
        'user': user,
        'token_url': token_url,
        'login_url': login_url,
    })

    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], html_message=message)
    except Exception as e:
        print("EMAIL ERROR:", e)

    return HttpResponse("Verification email sent.")

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and user.token == token:
        user.is_active = True
        user.token = ''
        user.save()
        return render(request, 'accounts/login_success.html', {'message': 'Your email has been verified. You can now log in.'})
    else:
        return HttpResponse('Invalid or expired link.', status=400)
