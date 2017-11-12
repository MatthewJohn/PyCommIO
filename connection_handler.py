
import threading
import uuid
import json
import time

from send_receive import send_msg, get_msg


class ConnectionHandler(object):

    def __init__(self, socket, event_handler, address,
                 ping_internal=5, connection_timeout=10):
        self._send_lock = threading.Lock()
        self._event_handler = event_handler
        self._socket = socket
        self._address = address
        self._loop = False
        self._client_id = self._generate_client_id()
        self._ping_interval = ping_internal
        self._connection_timeout = connection_timeout
        self._socket.settimeout(self._connection_timeout)
        self._recv_thread = threading.Thread(target=self._read_handler)
        self._ping_thread = None

    def send_event(self, event_name, data):
        self._send_data(json.dumps({'type': 'event', 'event': event_name, 'data': data}))

    def _send_data(self, data):
        self._send_lock.acquire(True)
        send_msg(self._socket, data)
        self._send_lock.release()

    def get_id(self):
        return self._client_id

    def _generate_client_id(self):
        # Tempmorary solution
        return uuid.uuid4().hex

    def start_thread(self, ping=False):
        self._loop = True
        self._recv_thread.start()
        if self._event_handler.on_connect:
            self._event_handler.on_connect(self)

        # Start ping thread
        if ping:
            self._ping_thread = threading.Thread(target=self._ping)
            self._ping_thread.start()

    def _ping(self):
        while self._loop:
            print 'Sending Ping'
            self._send_data(json.dumps({'type': 'ping'}))
            time.sleep(self._ping_interval)

    def teardown(self):
        self._loop = False
        print 'connection lost'
        if self._event_handler.on_disconnect:
            self._event_handler.on_disconnect(self)
        self._socket.close()

    def _handle_message(self, data):
        if data['type'] == 'ping':
            print 'Received ping - sending pong'
            self._send_data(json.dumps({'type': 'pong'}))
        elif data['type'] == 'pong':
            print 'resv pong'
        elif data['type'] == 'event':
            if data['event'] in self._event_handler.events:
                self._event_handler.events[data['event']](self, data['data'])

    def _read_handler(self):
        try:
            while self._loop:
                data_str = get_msg(self._socket)
                if data_str:
                    try:
                        data = json.loads(data_str)
                        self._handle_message(data)
                    except:
                        print 'Bad message: %s' % data_str
        except:
            self.teardown()