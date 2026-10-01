"""Room booking CLI: SQLite persistence, validated times, overlap prevention."""
import argparse
import sqlite3
from datetime import datetime

ROOMS = ('Benson 220', 'Smith 370', 'Romney 260', 'Clark 198', 'STC 340', 'Spori 450')


class BookingStore:
    def __init__(self, path='bookings.db'):
        self.db = sqlite3.connect(path)
        self.db.execute('CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY, room TEXT, day TEXT, start INTEGER, end INTEGER, owner TEXT)')

    def reserve(self, room, day, start, end, owner):
        canonical = next((r for r in ROOMS if r.lower() == room.strip().lower()), None)
        if not canonical:
            raise ValueError('Unknown room.')
        if not owner.strip():
            raise ValueError('A booking name is required.')
        try:
            day = datetime.strptime(day, '%Y-%m-%d').date().isoformat()
            times = [datetime.strptime(t, '%H:%M') for t in (start, end)]
        except ValueError:
            raise ValueError('Use YYYY-MM-DD for dates and HH:MM (24-hour) for times.') from None
        start, end = [t.hour * 60 + t.minute for t in times]
        if start >= end:
            raise ValueError('End time must be after start time on the same day.')
        try:
            self.db.execute('BEGIN IMMEDIATE')
            conflict = self.db.execute('SELECT id FROM bookings WHERE room=? AND day=? AND start<? AND end>?', (canonical, day, end, start)).fetchone()
            if conflict:
                raise ValueError('This time overlaps an existing reservation.')
            cursor = self.db.execute('INSERT INTO bookings(room,day,start,end,owner) VALUES(?,?,?,?,?)', (canonical, day, start, end, owner.strip()))
            self.db.commit()
            return cursor.lastrowid
        except Exception:
            self.db.rollback()
            raise

    def cancel(self, booking_id, owner):
        with self.db:
            cursor = self.db.execute('DELETE FROM bookings WHERE id=? AND owner=?', (booking_id, owner.strip()))
        if not cursor.rowcount:
            raise ValueError('Booking not found for that name.')

    def list(self):
        return self.db.execute('SELECT id,room,day,start,end,owner FROM bookings ORDER BY day,start').fetchall()

    def close(self):
        self.db.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', default='bookings.db')
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('rooms')
    commands.add_parser('list')
    reserve = commands.add_parser('reserve')
    for field in ('room', 'day', 'start', 'end', 'owner'):
        reserve.add_argument('--' + field, required=True)
    cancel = commands.add_parser('cancel')
    cancel.add_argument('id', type=int)
    cancel.add_argument('--owner', required=True)
    args = parser.parse_args()
    store = BookingStore(args.db)
    try:
        if args.command == 'rooms':
            print('\n'.join(ROOMS))
        elif args.command == 'reserve':
            print('Booking created:', store.reserve(args.room, args.day, args.start, args.end, args.owner))
        elif args.command == 'cancel':
            store.cancel(args.id, args.owner)
            print('Booking cancelled.')
        else:
            for row in store.list():
                bid, room, day, start, end, owner = row
                print(f'{bid}: {room} | {day} | {start//60:02}:{start%60:02}-{end//60:02}:{end%60:02} | {owner}')
    except ValueError as error:
        parser.exit(1, str(error) + '\n')
    finally:
        store.close()


if __name__ == '__main__':
    main()
