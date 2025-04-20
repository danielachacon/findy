const announcementOverlay = document.getElementById("announcement-overlay");
const announcementForm = document.getElementById("announcement-form");

function openAnnouncementPopup(eventId) {
    document.getElementById('announcement_event_id').value = eventId;
    announcementForm.action = "{% url 'make_announcement' 0 %}".replace('0', eventId);
    createdEventsOverlay.classList.add("hidden");
    announcementOverlay.classList.remove("hidden");
}

function closeAnnouncementPopup() {
    announcementOverlay.classList.add("hidden");
}

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
        popup.classList.add("hidden");
        createdEventsOverlay.classList.add("hidden");
        announcementOverlay.classList.add("hidden");
    }
});

announcementOverlay.addEventListener("click", (e) => {
    if (e.target === announcementOverlay) {
        announcementOverlay.classList.add("hidden");
    }
});

document.addEventListener('DOMContentLoaded', function() {
    announcementForm.addEventListener('submit', function(e) {
        const announcementText = document.getElementById('id_announcement_text').value;

        if (!announcementText.trim()) {
            e.preventDefault();
            alert('Please enter an announcement message');
            return false;
        }
    });
});

let gtLocations = {};
try {
    const locationDataElement = document.getElementById('location-data');
    if (locationDataElement && locationDataElement.dataset.locations) {
        gtLocations = JSON.parse(locationDataElement.dataset.locations);
    } else {
        console.error("Location data not found in the DOM");
    }
} catch (e) {
    console.error("Error parsing location data:", e);
}

const georgiaTechBounds = L.latLngBounds(
    L.latLng(33.770, -84.405),
    L.latLng(33.780, -84.385)
);

const map = L.map('map', {
    minZoom: 16,
    maxZoom: 18,
    maxBounds: georgiaTechBounds,
    maxBoundsViscosity: 1.0,
}).setView([33.7756, -84.3963], 16);

L.tileLayer('https://{s}.tile.openstreetmap.de/{z}/{x}/{y}.png', {
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

L.polygon([
    [33.770, -84.405], [33.770, -84.385],
    [33.780, -84.385], [33.780, -84.405]
], {
    color: "#003B5C",
    fillOpacity: 0.05,
    weight: 2
}).addTo(map);

const popup = document.getElementById("popup-overlay");
const rpopup = document.getElementById("register-popup");
const closeBtn = document.querySelector("#popup .events");
const closeRBtn = document.querySelector("#popup .registers");
const registerForm = document.getElementById("register-form");
const createdEventsOverlay = document.getElementById("created-events-overlay");

function openPopup() {
    popup.classList.remove("hidden");
}

function openCreatedEventsPopup() {
    createdEventsOverlay.classList.remove("hidden");
}

function closeCreatedEventsPopup() {
    createdEventsOverlay.classList.add("hidden");
}

let customLocationSelected = false;

function addLocationMarker(locationName, eventTitle, customLat, customLng) {
    if (customLat !== undefined && customLng !== undefined) {
        L.marker([customLat, customLng])
            .addTo(map)
            .bindPopup(eventTitle || 'Custom Location')
            .openPopup();

        map.setView([customLat, customLng], 17);
        return;
    }

    if (gtLocations[locationName]) {
        const loc = gtLocations[locationName];
        const popupContent = eventTitle || loc.name;

        L.marker([loc.lat, loc.lng])
            .addTo(map)
            .bindPopup(popupContent)
            .openPopup();

        map.setView([loc.lat, loc.lng], 17);
    } else {
        const events = document.querySelectorAll('.event-item');
        let customCoords = null;

        events.forEach(function(eventItem) {
            const eventLocation = eventItem.getAttribute('data-location');
            const eventCustomLat = eventItem.getAttribute('data-custom-lat');
            const eventCustomLng = eventItem.getAttribute('data-custom-lng');

            if (eventLocation === locationName && eventCustomLat && eventCustomLng) {
                customCoords = {
                    lat: parseFloat(eventCustomLat),
                    lng: parseFloat(eventCustomLng)
                };
            }
        });

        if (customCoords) {
            L.marker([customCoords.lat, customCoords.lng])
                .addTo(map)
                .bindPopup(eventTitle || locationName)
                .openPopup();

            map.setView([customCoords.lat, customCoords.lng], 17);
        }
    }
}

function openRPopup(eventId) {
    const eventItem = document.querySelector(`[data-event-id="${eventId}"]`);
    if (eventItem) {
        const currentEventLocation = eventItem.getAttribute('data-location');
        document.getElementById('event_location_field').value = currentEventLocation;
    }

    document.getElementById('event_id_field').value = eventId;
    rpopup.classList.remove("hidden");
}

document.addEventListener('DOMContentLoaded', function() {
    const locationDropdown = document.querySelector('[name="location"]');
    const customLocationField = document.getElementById('custom-location-field');
    const customLocationInput = document.getElementById('id_custom_location');
    const customLatField = document.getElementById('custom_lat_field');
    const customLngField = document.getElementById('custom_lng_field');
    let formValues = {};
    let customMarker = null;

    const confirmButton = document.createElement('button');
    confirmButton.id = 'confirm-location';
    confirmButton.textContent = 'Use This Location';
    confirmButton.className = 'confirm-location-button hidden';
    document.body.appendChild(confirmButton);

    const mapInstructions = document.createElement('div');
    mapInstructions.id = 'map-instructions';
    mapInstructions.textContent = 'Click on the map to select your custom location';
    mapInstructions.className = 'map-instructions hidden';
    document.body.appendChild(mapInstructions);

    function storeFormData() {
        const form = document.querySelector('#popup-overlay form');
        const formElements = form.elements;
        for (let i = 0; i < formElements.length; i++) {
            if (formElements[i].name) {
                formValues[formElements[i].name] = formElements[i].value;
            }
        }
    }

    function restoreFormData() {
        const form = document.querySelector('#popup-overlay form');
        const formElements = form.elements;
        for (let i = 0; i < formElements.length; i++) {
            if (formElements[i].name && formValues[formElements[i].name]) {
                formElements[i].value = formValues[formElements[i].name];
            }
        }

        locationDropdown.value = "Custom";
        customLocationField.style.display = 'block';
        customLocationInput.disabled = false;
        customLocationInput.focus();
    }

    function handleMapClick(e) {
        if (customMarker) {
            map.removeLayer(customMarker);
        }

        const lat = e.latlng.lat;
        const lng = e.latlng.lng;

        customLatField.value = lat;
        customLngField.value = lng;

        customMarker = L.marker([lat, lng]).addTo(map);
        customMarker.bindPopup('Your custom location').openPopup();

        confirmButton.classList.remove("hidden");
        confirmButton.disabled = false;
    }

    if (locationDropdown && customLocationField && customLocationInput) {
        customLocationSelected = locationDropdown.value === "Custom";
        if (customLocationSelected) {
            customLocationField.style.display = 'block';
        } else {
            customLocationField.style.display = 'none';
            customLocationInput.disabled = true;
        }

        locationDropdown.addEventListener('change', function() {
            customLocationSelected = this.value === "Custom";

            if (customLocationSelected) {
                storeFormData();
                customLocationField.style.display = 'block';
                customLocationInput.disabled = false;
                popup.classList.add("hidden");
                mapInstructions.classList.remove("hidden");
                map.on('click', handleMapClick);
            } else {
                customLocationField.style.display = 'none';
                customLocationInput.disabled = true;
                map.off('click', handleMapClick);

                if (customMarker) {
                    map.removeLayer(customMarker);
                    customMarker = null;
                }

                mapInstructions.classList.add("hidden");
                confirmButton.classList.add("hidden");
            }
        });
    }

    confirmButton.addEventListener('click', function() {
        if (!customLatField.value || !customLngField.value) {
            alert('Please select a location on the map first');
            return;
        }

        popup.classList.remove("hidden");
        confirmButton.classList.add("hidden");
        mapInstructions.classList.add("hidden");
        map.off('click', handleMapClick);
        restoreFormData();
    });

    const eventForm = document.querySelector('#popup-overlay form');
    if (eventForm) {
        eventForm.addEventListener('submit', function(e) {
            if (customLocationSelected) {
                const customLocationInput = document.getElementById('id_custom_location');

                if (!customLocationInput.value.trim()) {
                    e.preventDefault();
                    customLocationInput.value = '';
                    customLocationInput.focus();
                    return false;
                }

                if (!customLatField.value || !customLngField.value) {
                    e.preventDefault();
                    alert('Please select a location on the map first');
                    popup.classList.add("hidden");
                    mapInstructions.classList.remove("hidden");
                    map.on('click', handleMapClick);
                    return false;
                }
            }
        });
    }

    const urlParams = new URLSearchParams(window.location.search);
    const justRegistered = urlParams.get('just_registered');
    const registeredEventId = urlParams.get('event_id');

    const registeredEvents = document.querySelectorAll('#box:nth-of-type(2) .event-item');
    let justRegisteredEvent = null;

    registeredEvents.forEach(function(eventItem) {
        const locationName = eventItem.getAttribute('data-location');
        const eventId = eventItem.getAttribute('data-event-id');

        let eventTitle = locationName;
        const titleElement = eventItem.querySelector('h3');
        if (titleElement) {
            eventTitle = titleElement.textContent.trim();
        }

        if (justRegistered === 'true' && eventId === registeredEventId) {
            justRegisteredEvent = eventItem;
        }

        if (locationName && gtLocations[locationName]) {
            addLocationMarker(locationName, eventTitle);
        } else {
            const lat = parseFloat(eventItem.getAttribute('data-custom-lat'));
            const lng = parseFloat(eventItem.getAttribute('data-custom-lng'));
            if (!isNaN(lat) && !isNaN(lng)) {
                addLocationMarker(locationName, eventTitle, lat, lng);
            }
        }
    });

    if (justRegisteredEvent) {
        const locationName = justRegisteredEvent.getAttribute('data-location');

        if (locationName && gtLocations[locationName]) {
            const location = gtLocations[locationName];
            map.setView([location.lat, location.lng], 17);
        } else {
            const lat = parseFloat(justRegisteredEvent.getAttribute('data-custom-lat'));
            const lng = parseFloat(justRegisteredEvent.getAttribute('data-custom-lng'));
            if (!isNaN(lat) && !isNaN(lng)) {
                map.setView([lat, lng], 17);
            }
        }
    } else if (registeredEvents.length > 0) {
        const firstEvent = registeredEvents[0];
        const locationName = firstEvent.getAttribute('data-location');

        if (locationName && gtLocations[locationName]) {
            const location = gtLocations[locationName];
            map.setView([location.lat, location.lng], 17);
        } else {
            const lat = parseFloat(firstEvent.getAttribute('data-custom-lat'));
            const lng = parseFloat(firstEvent.getAttribute('data-custom-lng'));
            if (!isNaN(lat) && !isNaN(lng)) {
                map.setView([lat, lng], 17);
            }
        }
    }
});

registerForm.addEventListener('submit', function(e) {
    e.preventDefault();

    const eventId = document.getElementById('event_id_field').value;
    const eventItem = document.querySelector(`[data-event-id="${eventId}"]`);

    if (eventItem) {
        const locationName = eventItem.getAttribute('data-location');
        const customLat = eventItem.getAttribute('data-custom-lat');
        const customLng = eventItem.getAttribute('data-custom-lng');

        let eventTitle = locationName;
        const titleElement = eventItem.querySelector('h3');
        if (titleElement) {
            eventTitle = titleElement.textContent.trim();
        }

        if (customLat && customLng) {
            const lat = parseFloat(customLat);
            const lng = parseFloat(customLng);

            L.marker([lat, lng])
                .addTo(map)
                .bindPopup(eventTitle)
                .openPopup();

            map.setView([lat, lng], 17);
        } else if (locationName && gtLocations[locationName]) {
            addLocationMarker(locationName, eventTitle);
        }
    }

    const submitButton = document.createElement('input');
    submitButton.type = 'hidden';
    submitButton.name = 'submit_register';
    submitButton.value = 'true';
    registerForm.appendChild(submitButton);

    setTimeout(() => {
        registerForm.submit();
    }, 800);
});

closeBtn.addEventListener("click", () => popup.classList.add("hidden"));
closeRBtn.addEventListener("click", () => rpopup.classList.add("hidden"));
popup.addEventListener("click", (e) => {
    if (e.target === popup) popup.classList.add("hidden");
});

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
        popup.classList.add("hidden");
        createdEventsOverlay.classList.add("hidden");
        announcementOverlay.classList.add("hidden");
        notificationsOverlay.classList.add("hidden");
    }
});

document.getElementById("created-events-button").addEventListener("click", openCreatedEventsPopup);

createdEventsOverlay.addEventListener("click", (e) => {
    if (e.target === createdEventsOverlay) {
        createdEventsOverlay.classList.add("hidden");
    }
});

flatpickr(".datetimepicker", {
    enableTime: true,
    dateFormat: "Y-m-d H:i",
    time_24hr: false
});

const notificationsOverlay = document.getElementById("notifications-overlay");
const notificationsContainer = document.getElementById("notifications-popup").querySelector(".notifications-list");

function openNotificationsPopup() {
    notificationsContainer.innerHTML = '<div class="loading">Loading notifications...</div>';
    notificationsOverlay.classList.remove("hidden");

    fetch("{% url 'notifications' %}", {
        method: "GET",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            notificationsContainer.innerHTML = '';

            if (data.notifications.length === 0) {
                notificationsContainer.innerHTML = '<div class="no-notifications">You have no notifications at this time.</div>';
            } else {
                data.notifications.forEach(notification => {
                    const notificationCard = document.createElement('li');
                    notificationCard.className = 'notification-card';

                    notificationCard.innerHTML = `
                        <div class="notification-header">
                            <div class="notification-event">${notification.event_title}</div>
                            <div class="notification-date">${notification.created_at}</div>
                        </div>
                        <div class="notification-message">${notification.message}</div>
                    `;

                    notificationsContainer.appendChild(notificationCard);
                });
            }
        } else {
            notificationsContainer.innerHTML = '<div class="error">Error loading notifications</div>';
        }
    })
    .catch(error => {
        console.error("Error fetching notifications:", error);
        notificationsContainer.innerHTML = '<div class="error">Error loading notifications</div>';
    });
}

function closeNotificationsPopup() {
    notificationsOverlay.classList.add("hidden");
}

notificationsOverlay.addEventListener("click", (e) => {
    if (e.target === notificationsOverlay) {
        notificationsOverlay.classList.add("hidden");
    }
});