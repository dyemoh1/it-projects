# Roomly — Python and SQLite reservations

A responsive reservation website connected to the Python booking logic and SQLite database. Room capacities and amenities are illustrative; no real campus rooms are reserved.

## Run locally

From this folder, with Python 3.10 or later:

```sh
python server.py
```

Open http://localhost:8001. The same server serves the website and booking API. Bookings persist in `bookings.db` beside the server. Restarting the server or using another browser on this computer preserves the same records. Old browser-only demo bookings are not migrated.

The server binds only to loopback. This is a trusted local demo: booking names are not authentication, all local visitors can see bookings and cancel them. Do not expose it publicly without accounts, ownership enforcement and a production server. GitHub Pages alone cannot run this Python backend.

## CLI and tests

Run from this folder so the CLI uses the same default database:

```sh
python room_reservation.py list
python -m unittest -v
```

Use `python server.py --db PATH --port 8001` for a separate database.

## Behavior and verification

The server validates input and enforces overlap prevention inside a SQLite write transaction. Adjacent bookings are allowed. The website displays server errors and refreshes reservations on page load and window focus. Another user's changes may require a refresh; the server still rejects conflicting bookings.

Automated tests cover persistence, cancellation, validation, concurrent conflicting requests, cross-origin rejection and blocking database-file downloads, alongside the existing booking tests.

[Project history](../PROJECT-HISTORY.md) · [All projects](../README.md)
