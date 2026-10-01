# Roomly — reservation interface

Open `reservations.html` through a local web server, for example `python -m http.server 8000`, then visit `http://localhost:8000/reservations.html`.

This AI-assisted redesign builds on the campus room reservation concept with room cards, search, group-size filtering, a time-slot availability view, a booking dialog, cancellation, and browser persistence. It uses the same six room names as the Python project. Capacities and amenities are illustrative sample data.

## Scope

This is an interactive frontend prototype. Bookings are saved in this browser's local storage, not the Python SQLite database. It has no user accounts or administrator authorization and makes no real campus reservations. Concurrent cross-tab writes are not transactional. The Python CLI remains a separate implementation with transactional overlap checks.

## Next integration milestone

Connect this interface to an authenticated backend using the existing SQLite booking logic. Enforce ownership, validation, conflict checks, and cancellation on the server. Add calendar and recurring-booking flows after that foundation is verified.

## Verified locally
Browser checks covered booking creation, persistence after refresh, rejection of an overlapping booking, inline cancellation, capacity and room-name filters, and desktop/mobile layouts. JavaScript syntax validation passed.
