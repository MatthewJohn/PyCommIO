
import threading
import uuid
import json

from send_receive import send_msg, get_msg


class ConnectionHandler(object):

    def __init__(self, socket, event_handler, address):
        self._send_lock = threading.Lock()
        self._event_handler = event_handler
        self._socket = socket
        self._address = address
        self._loop = False
        self._client_id = self._generate_client_id()
        self._thread = threading.Thread(target=self._read_handler)

    def send_event(self, event_name, data):
        self._send_data(json.dumps({'event': event_name, 'data': data}))

    def _send_data(self, data):
        self._send_lock.acquire(True)
        send_msg(self._socket, data)
        self._send_lock.release()

    def get_id(self):
        return self._client_id

    def _generate_client_id(self):
        # Tempmorary solution
        return uuid.uuid4().hex

    def start_thread(self):
        self._loop = True
        self._thread.start()
        if self._event_handler.on_connect:
            self._event_handler.on_connect(self)

    def teardown(self):
        self._loop = False
        if self._event_handler.on_disconnect:
            self._event_handler.on_disconnect(self)
        self._socket.close()

    def _read_handler(self):
        try:
            while self._loop:
                data_str = get_msg(self._socket)
                if data_str:
                    try:
                        data = json.loads(data_str)
                        if data['event'] in self._event_handler.events:
                            self._event_handler.events[data['event']](self, data['data'])
                    except:
                        print 'Bad message: %s' % data_str
        except:
            self.teardown()