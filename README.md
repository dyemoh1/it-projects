# David Yemoh — IT Project Lab

Practical work in networking, application development, and troubleshooting. I'm a Computer Information Technology student at BYU–Idaho, graduating in 2028, with Security+ and eJPT certifications.

## Projects

| Project | Demonstrates | Status |
| --- | --- | --- |
| [Cisco home lab](HOME-LAB.md) | VLANs, switch management, connectivity verification | Existing lab documented; fresh screenshots pending |
| [Campus room reservations](room_reservation.py) | Python, SQLite, validation, conflict handling, automated tests | Local CLI; tested with synthetic bookings |
| [Firebase project manager](FIREBASE.md) | Google sign-in, Firestore CRUD, ownership rules, safe text rendering | Source prepared; cloud integration requires setup and verification |

## Roomly reservation interface

[Open the design](reservations.html) · [Setup and limitations](RESERVATIONS-WEB.md)

A responsive room-finding dashboard with date, time, capacity and search filters, booking confirmation, overlap prevention, and saved reservations. Run a local web server and open reservations.html. Bookings are stored in this browser; this prototype is separate from the Python SQLite app and does not book real rooms.

## Try the Python project

Python 3.10 or later; no third-party packages required.

```sh
python -m unittest -v test_room_reservation.py
python room_reservation.py rooms
python room_reservation.py reserve --room "STC 340" --day 2027-01-15 --start 10:00 --end 11:00 --owner Demo
python room_reservation.py list
python room_reservation.py cancel 1 --owner Demo
```

Bookings persist in a local SQLite database. Dates and times are validated; overlapping bookings for the same room and day are rejected, while adjacent bookings are allowed. Cancellation checks the booking name. **Names are not authentication**: this is a local learning tool, not a multi-user production booking service.

## Project history and attribution

The Firebase and Python projects originated in coursework with a mixture of personal work and starter material. Exact historical authorship of individual sections is not established; I do not claim all original code as independently authored.

This portfolio edition was prepared with AI assistance. The Python CLI was rewritten from the original in-memory booking concept to add SQLite persistence, date/time validation, overlap checks, and standard-library tests. Firebase changes replace unsafe HTML interpolation, organize CRUD handlers, and provide owner-scoped rules and setup instructions. These new improvements should be understood and practiced before presenting them as independently implemented skills.

## Verification

Run the included Python tests to reproduce the local checks. Firebase authentication, deployed Firestore rules, and live cloud CRUD have not been verified. No production data or credentials are included.

[GitHub profile](https://github.com/dyemoh1) · [LinkedIn](https://www.linkedin.com/in/david-yemoh-479b7a281/)

