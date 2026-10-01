import json
import tempfile
import threading
import unittest
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from server import make_server
from room_reservation import BookingStore

class ApiTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=Path(self.tmp.name)/'test.db'
        self.server=make_server(0,self.path)
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True)
        self.thread.start()
        self.url=f'http://127.0.0.1:{self.server.server_port}'
    def tearDown(self):
        self.server.shutdown(); self.server.server_close(); self.thread.join(); self.tmp.cleanup()
    def request(self,path,data=None,origin=None):
        headers={'Content-Type':'application/json'}
        if origin: headers['Origin']=origin
        req=Request(self.url+path,data=json.dumps(data).encode() if data is not None else None,headers=headers)
        try:
            with urlopen(req) as r: return r.status,json.load(r)
        except HTTPError as e: return e.code,json.load(e)
    def booking(self):
        return dict(room='STC 340',day='2027-01-15',start='10:00',end='11:00',owner='Test')
    def test_persistence_and_cancel(self):
        status,result=self.request('/api/bookings',self.booking()); self.assertEqual(status,201)
        store=BookingStore(self.path)
        self.assertEqual(len(store.list()),1); store.close()
        self.assertEqual(self.request('/api/bookings')[1][0]['start'],'10:00')
        self.assertEqual(self.request('/api/cancel',dict(id=result['id'],owner='Wrong'))[0],400)
        self.assertEqual(self.request('/api/cancel',dict(id=result['id'],owner='Test'))[0],200)
        self.assertEqual(self.request('/api/bookings')[1],[])
    def test_concurrent_conflict(self):
        self.request('/api/bookings')
        with ThreadPoolExecutor(2) as pool:
            results=list(pool.map(lambda _:self.request('/api/bookings',self.booking())[0],range(2)))
        self.assertEqual(sorted(results),[201,409])
    def test_validation_and_origin(self):
        data=self.booking();data['day']='2027-02-30'
        self.assertEqual(self.request('/api/bookings',data)[0],400)
        self.assertEqual(self.request('/api/bookings',self.booking(),'https://example.com')[0],403)
        self.assertEqual(self.request('/bookings.db')[0],404)
        self.assertEqual(self.request('/api/bookings',[])[0],400)
if __name__=='__main__': unittest.main()
