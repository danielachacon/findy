from time import localtime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.shortcuts import redirect
from django.utils.timezone import now, localtime

@login_required
def user_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    past_registered_events = request.user.registered_events.filter(end_time__lt=localtime(now()))
    return render(request, 'userprofile/userprofile.html', {
        'user': request.user,
        'profile': profile,
        'past_registered_events': past_registered_events,
    })

@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST' and request.FILES.get('profile_picture'):
        profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        return redirect('user_profile')

    return render(request, 'edit_profile.html', {'profile': profile})
