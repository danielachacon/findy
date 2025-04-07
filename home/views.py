from django.shortcuts import render


def start(request):
    template_data = {}
    template_data['title'] = 'Start'
    
    # Debug information
    print("Session ID:", request.session.session_key)
    print("User authenticated:", request.user.is_authenticated)
    if request.user.is_authenticated:
        print("Username:", request.user.username)
        print("User email:", request.user.email)
    
    context = {
        'template_data': template_data,
        'user': request.user,
    }
    
    return render(request, 'home/start.html', context)


def about(request):
    template_data = {}
    template_data['title'] = 'Findy'
    return render(request, 'home/about.html', {'template_data': template_data})