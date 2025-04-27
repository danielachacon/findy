from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomEventForm, EventSearchForm
from .models import Event, Registration, Announcement, Waitlist
from django.http import JsonResponse
from .locations import GTLocations
import json
from django.urls import reverse
from django.contrib import messages
from django.db.models import F
import uuid

@login_required
def main_view(request):
    # Debug prints
    print(f"\nCurrent user: {request.user.username}")
    print("All events in database:")
    for event in Event.objects.all():
        print(f"- {event.title} (ID: {event.id}, Created by: {event.created_by.username})")

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
            if event.get_registration_count() < event.max_capacity:
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
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': 'Event is at full capacity.'
                    })

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
                    max_capacity=cd['max_capacity'],
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

    return render(request, 'main/index.html', {
        'form': form,
        'created_events': created_events,
        'starred_events': starred_events,
        'events': events,
        'registered_events': registered_events,
        'locations_json': locations_json,
        'announcements': Announcement.objects.filter(event__in=registered_events).order_by('-created_at'),
    })


@login_required
def make_announcement(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)

    if request.method == 'POST':
        announcement_text = request.POST.get('announcement_text')
        if announcement_text:
            announcement = Announcement.objects.create(
                event=event,
                message=announcement_text,
                created_by=request.user
            )

            registered_count = event.registered_users.count()

            if registered_count > 0:
                messages.success(request,
                                f"Announcement posted successfully. It will be visible to {registered_count} registered attendees.")
            else:
                messages.info(request, "Announcement posted successfully, but there are no registered attendees yet.")
        else:
            messages.error(request, "Announcement text cannot be empty.")
    
    return redirect('main')


@login_required
def notifications_view(request):
    """
    Returns notifications for AJAX request to populate the notifications popup
    """
    registered_events = request.user.registered_events.all()
    announcements = Announcement.objects.filter(event__in=registered_events).order_by('-created_at')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        notifications_data = []
        for announcement in announcements:
            notifications_data.append({
                'event_title': announcement.event.title,
                'message': announcement.message,
                'created_at': announcement.created_at.strftime("%b %d, %Y %H:%M"),
                'created_by': announcement.created_by.username
            })
        return JsonResponse({'success': True, 'notifications': notifications_data})
    
    return redirect('main')

@login_required
def unregister_event(request, event_id):
    if request.method == "POST":
        try:
            registration = Registration.objects.get(
                event_id=event_id,
                user=request.user,
            )
            registration.delete()
            messages.success(request, "You have been unregistered from the event.")
        except Registration.DoesNotExist:
            messages.error(request, "You are not registered for this event.")
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

        # Get the 'next' parameter from the form
        next_url = request.POST.get('next', request.META.get('HTTP_REFERER', reverse('main')))

        # If there are search parameters, add them back to the redirect URL
        search_params = request.POST.get('search_params')
        if search_params:
            next_url = f"{next_url}?{search_params}"

        # Redirect to the 'next' URL with the query parameters intact
        return redirect(next_url)

    return redirect('main')

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)

    if request.method == "POST":
        form = CustomEventForm(request.POST, instance=event)
        if form.is_valid():
            cd = form.cleaned_data
            location_value = cd['location']

            custom_location = request.POST.get('custom_location')
            custom_lat = request.POST.get('custom_lat')
            custom_lng = request.POST.get('custom_lng')

            if location_value == "Custom" and custom_location:
                location_value = custom_location

            event.title = cd['title']
            event.description = cd['description']
            event.start_time = cd['start_time']
            event.end_time = cd['end_time']
            event.max_capacity = cd['max_capacity']
            event.location = location_value

            if custom_lat and custom_lng:
                event.custom_lat = float(custom_lat)
                event.custom_lng = float(custom_lng)

            event.save()
            return redirect('main')
    else:
        gt_location_names = GTLocations.get_location_names()
        location_value = event.location if event.location in gt_location_names else "Custom"
        custom_location_value = event.location if location_value == "Custom" else ''

        form = CustomEventForm(initial={
            'title': event.title,
            'description': event.description,
            'start_time': event.start_time,
            'end_time': event.end_time,
            'max_capacity': event.max_capacity,
            'location': location_value,
            'custom_location': custom_location_value,
            'custom_lat': event.custom_lat,
            'custom_lng': event.custom_lng,
        })

    return render(request, 'main/edit_event.html', {'form': form, 'event': event})

@login_required
def join_waitlist(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if (event.get_registration_count() < event.max_capacity):
        messages.warning(request, "Event not at max capacity.")
        return redirect('main')

    if not Waitlist.objects.filter(event=event, user=request.user).exists():
        last_position = Waitlist.objects.filter(event=event).order_by('-position').first()
        new_position = 1 if not last_position else last_position.position + 1

        Waitlist.objects.create(
            event=event,
            user=request.user,
            position=new_position
        )

        messages.success(request, f"You've been added to the waitlist at position {new_position}")
    else:
        messages.warning(request, "You're already on the waitlist for this event")

    return redirect('main')

@login_required
def leave_waitlist(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    try:
        waitlist_entry = Waitlist.objects.get(event=event, user=request.user)
        leaving_position = waitlist_entry.position

        waitlist_entry.delete()

        Waitlist.objects.filter(
            event=event,
            position__gt=leaving_position
        ).update(
            position=F('position') - 1
        )

        messages.success(request, f"You've left the waitlist for this event")
    except Waitlist.DoesNotExist:
        messages.warning(request, "You're not on the waitlist for this event")

    return redirect('main')

@login_required
def validate_event_code(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    message = None
    is_valid = False
    
    if request.method == 'POST':
        code = request.POST.get('registration_code', '')
        
        # Validate UUID format first
        try:
            # Try to parse the code as UUID
            uuid.UUID(code)
            
            # If valid UUID, check if it exists
            try:
                registration = Registration.objects.get(
                    event=event,
                    registration_code=code
                )
                message = "Valid registration code!"
                is_valid = True
            except Registration.DoesNotExist:
                message = "Invalid registration code for this event"
                is_valid = False
                
        except ValueError:
            message = "Invalid code format"
            is_valid = False
    
    return JsonResponse({
        'message': message,
        'is_valid': is_valid
    })

@login_required
def create_event_view(request):
    form = CustomEventForm(request.POST or None)
    show_modal = False

    if request.method == 'POST':
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('main')  # Replace with your actual redirect
        else:
            show_modal = True  # Keep the modal open if the form is invalid

    return render(request, 'main/index.html', {
        'form': form,
        'show_create_modal': show_modal
    })

@login_required
def event_search(request):
    form = EventSearchForm(request.GET or None)
    registered_events = request.user.registered_events.all()
    starred_events = request.user.starred_events.all()
    events = Event.objects.all()

    if form.is_valid():
        event_title = form.cleaned_data.get('event_title')
        start_time_min = form.cleaned_data.get('start_time_min')
        end_time_max = form.cleaned_data.get('end_time_max')
        location = form.cleaned_data.get('location')
        is_full = form.cleaned_data.get('is_full')

        if event_title:
            events = events.filter(title__icontains=event_title)

        if start_time_min:
            events = events.filter(start_time__gte=start_time_min)

        if end_time_max:
            events = events.filter(end_time__lte=end_time_max)

        if location:
            events = events.filter(location=location)

        if is_full == 'False':
            events = [event for event in events if not event.is_full()]

    context = {
        'form': form,
        'events': events,
        'registered_events': registered_events,
        'starred_events': starred_events,
        'events_open': True
    }

    return render(request, 'main/index.html', context)