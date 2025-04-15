from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomEventForm
from .models import Event, Registration
from django.http import JsonResponse
from .locations import GTLocations
import json
from django.urls import reverse

@login_required
def main_view(request):
    form = CustomEventForm()
    created_events = Event.objects.filter(created_by=request.user)
    starred_events = Event.objects.filter(starred_by=request.user)
    events = Event.objects.all()
    registered_events = request.user.registered_events.all()


    locations_dict = {}
    for location_name in GTLocations.get_location_names():
        location = GTLocations.get_location(location_name)
        if location:
            locations_dict[location_name] = {
                "lat": location["latitude"],
                "lng": location["longitude"],
                "name": location["name"]
            }

    locations_json = json.dumps(locations_dict)

    if request.method == 'POST':
        if 'submit_register' in request.POST:
            event_id = request.POST.get('event_id')
            event = Event.objects.get(id=event_id)
            Registration.objects.create(
                user = request.user,
                event = event,
            )

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})


            redirect_url = f"{reverse('main')}?just_registered=true&event_id={event_id}"
            return redirect(redirect_url)

        else:
            form = CustomEventForm(request.POST)
            print(form.is_valid())
            print(form.errors)

            if form.is_valid() and 'submit_event' in request.POST:
                cd = form.cleaned_data
                location_value = cd['location']

                custom_location = request.POST.get('custom_location')
                custom_lat = request.POST.get('custom_lat')
                custom_lng = request.POST.get('custom_lng')

                if location_value == "Custom" and custom_location:
                    location_value = custom_location

                event = Event.objects.create(
                    title=cd['title'],
                    description=cd['description'],
                    start_time=cd['start_time'],
                    end_time=cd['end_time'],
                    location=location_value,
                    created_by=request.user
                )

                if custom_lat and custom_lng:
                    event.custom_lat = float(custom_lat)
                    event.custom_lng = float(custom_lng)
                    event.save()

                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True})
                return redirect('main')
            else:
                print("this is what is happening")
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        if form.is_valid() and 'submit_event' in request.POST:
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
        elif 'submit_register' in request.POST:
            event_id = request.POST.get('event_id')
            event = Event.objects.get(id=event_id)
            registration = Registration.objects.create(
                user=request.user,
                event=event,
            )

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'qr_code_url': registration.qr_code.url
                })
        else:
            print("this is what is happening")
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    return render(request, 'main/index.html', {
        'form': form,
        'created_events': created_events,
        'starred_events': starred_events,
        'events': events,
        'registered_events': registered_events,
        'locations_json': locations_json,
    })

@login_required
def unregister_event(request, event_id):
    registration = Registration.objects.get(
        event_id=event_id,
        user=request.user,
    )
    if request.method == "POST":
        registration.delete()
    return redirect('main')

@login_required
def delete_event(request, event_id):
    form = CustomEventForm()
    created_events = Event.objects.filter(created_by=request.user)
    event = get_object_or_404(Event, id=event_id, created_by=request.user)
    if request.method == "POST":
        event.delete()
    return redirect('main')

@login_required
def toggle_star_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        if request.user in event.starred_by.all():
            event.starred_by.remove(request.user)
        else:
            event.starred_by.add(request.user)

    return redirect('main')

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)

    if request.method == "POST":
        form = CustomEventForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            location_value = cd['location']

            # Check if custom location was provided
            custom_location = request.POST.get('custom_location')
            custom_lat = request.POST.get('custom_lat')
            custom_lng = request.POST.get('custom_lng')

            if location_value == "Custom" and custom_location:
                location_value = custom_location

            event.title = cd['title']
            event.description = cd['description']
            event.start_time = cd['start_time']
            event.end_time = cd['end_time']
            event.location = location_value


            if custom_lat and custom_lng:
                event.custom_lat = float(custom_lat)
                event.custom_lng = float(custom_lng)

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