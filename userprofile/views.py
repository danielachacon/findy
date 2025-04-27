from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import EditProfileForm

@login_required
def user_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'userprofile/userprofile.html', {
        'user': request.user,
        'profile': profile
    })

@login_required
def edit_profile(request):
    profile = request.user.profile  # assuming OneToOneField to User

    if request.method == 'POST':
        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES['profile_picture']
            profile.save()
        return redirect('user_profile')  # or whatever your profile page is named

    return render(request, 'edit_profile.html', {'profile': profile})
