import tempfile
import unittest
from pathlib import Path
from room_reservation import BookingStore


class BookingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = str(Path(self.tmp.name) / 'test.db')
        self.store = BookingStore(self.path)

    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()

    def book(self, start='10:00', end='11:00', **changes):
        args = dict(room=' stc 340 ', day='2027-01-15', start=start, end=end, owner='Demo')
        args.update(changes)
        return self.store.reserve(**args)

    def test_persists_after_reopen(self):
        self.book()
        self.store.close()
        self.store = BookingStore(self.path)
        self.assertEqual(self.store.list()[0][1], 'STC 340')

    def test_overlap_rejected(self):
        self.book()
        for start, end in [('10:00', '11:00'), ('09:30', '10:30'), ('10:30', '11:30'), ('09:00', '12:00')]:
            with self.subTest(start=start), self.assertRaises(ValueError):
                self.book(start, end)
        self.assertEqual(len(self.store.list()), 1)

    def test_adjacent_and_other_dates_allowed(self):
        self.book()
        self.book('11:00', '12:00')
        self.book(day='2027-01-16')
        self.assertEqual(len(self.store.list()), 3)

    def test_invalid_inputs(self):
        for change in [dict(day='2027-02-30'), dict(start='25:00'), dict(end='09:00'), dict(owner=' '), dict(room='unknown')]:
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.book(**change)

    def test_cancel_requires_matching_name(self):
        bid = self.book()
        with self.assertRaises(ValueError):
            self.store.cancel(bid, 'Other')
        self.store.cancel(bid, 'Demo')
        self.assertEqual(self.store.list(), [])


if __name__ == '__main__':
    unittest.main()
