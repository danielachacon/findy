from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomEventForm
from .models import Event
from django.http import JsonResponse

@login_required
def main_view(request):
    form = CustomEventForm()
    created_events = Event.objects.filter(created_by=request.user)
    events = Event.objects.all()

    if request.method == 'POST':
        form = CustomEventForm(request.POST)
        if form.is_valid() and submit_event in request.POST:
            cd = form.cleaned_data
            event = Event.objects.create(
                title=cd['title'],
                description=cd['description'],
                start_time=cd['start_time'],
                end_time=cd['end_time'],
                location=cd['location'],
                created_by=request.user
            )
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
        elif form.is_valid() and submit_register in request.POST:
            cd = form.cleaned_data
            event_id = request.POST.get('event_id')
            event = Event.objects.get(id=event_id)
            user = EventUser.objects.create(
                name=cd['name'],
                email=cd['email']
            )

            Registration.objects.create(
                user = user,
                event = event,
            )

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    return render(request, 'main/index.html', {
        'form': form,
        'created_events': created_events,
        'events':events
    })

@login_required
def delete_event(request, event_id):
    form = CustomEventForm()
    created_events = Event.objects.filter(created_by=request.user)
    event = get_object_or_404(Event, id=event_id, created_by=request.user)
    if request.method == "POST":
        event.delete()
    return redirect('main')

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)

    if request.method == "POST":
        form = CustomEventForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            event.title = cd['title']
            event.description = cd['description']
            event.start_time = cd['start_time']
            event.end_time = cd['end_time']
            event.location = cd['location']
            event.save()
            return redirect('main')
    else:
        form = CustomEventForm(initial={
            'title': event.title,
            'description': event.description,
            'start_time': event.start_time,
            'end_time': event.end_time,
            'location': event.location,
        })

    return render(request, 'main/edit_event.html', {'form': form, 'event': event})