
import threading
import uuid
import json
import time
import traceback
from threading import Event

from pycommio.send_receive import send_msg, get_msg
from pycommio.errors import NoEventHandlerError


class ConnectionHandler(object):

    PING = 'ping'
    PONG = 'pong'
    EVENT = 'event'
    EVENT_COMPLETE = 'event_complete'

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
        self._events = {}

    def send_event(self, event_name, data=None,
                   await_completion=False,
                   callback=None):
        event_id = self._send_message(
            ConnectionHandler.EVENT,
            name=event_name,
            data=data)

    def _send_data(self, data):
        self._send_lock.acquire(True)
        send_msg(self._socket, data)
        self._send_lock.release()

    def get_id(self):
        return self._client_id

    def _generate_client_id(self):
        # Tempmorary solution
        return uuid.uuid4().hex

    def _generate_message_id(self):
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
            print('Sending Ping')
            self._send_message(ConnectionHandler.PING)
            time.sleep(self._ping_interval)

    def teardown(self):
        self._loop = False
        print('connection lost')
        if self._event_handler.on_disconnect:
            self._event_handler.on_disconnect(self)
        self._socket.close()

    def _send_message(self, _type, name=None, data=None):
        msg_id = self._generate_message_id()
        self._send_data(json.dumps(
            {'type': _type,
             'data': data,
             'id': msg_id,
             'name': name}
        ))
        return msg_id

    def _get_event_handler(self, event_name):
        """Return event handler for a given event"""
        if event_name in self._event_handler.events:
            return self._event_handler.events[event_name]
        else:
            raise NoEventHandlerError(
                'No event handler availble for event: %s' % event_name)

    def _handle_message(self, data):
        return_data = None
        if data['type'] == ConnectionHandler.PING:
            print('Received ping - sending pong')
            self._send_message(ConnectionHandler.PONG)
        elif data['type'] == ConnectionHandler.PONG:
            print('resv pong')
        elif data['type'] == ConnectionHandler.EVENT:
            if data['name'] in self._event_handler.events:
                event_handler = self._get_event_handler(data['name'])
                return_data = event_handler(self, data['data'])
        else:
            raise Exception('Unknown message type: {0}'.format(data['type']))

    def _read_handler(self):
        try:
            while self._loop:
                data_str = get_msg(self._socket)
                if data_str:
                    try:
                        data = json.loads(data_str)
                        try:
                            self._handle_message(data)
                        except Exception as exc:
                            print('Message handle failure: {0}'.format(exc))
                    except Exception as exc:
                        print('Error whilst handling message: {0}'.format(str(exc)))
                        print(traceback.format_exc())
        finally:
            self.teardown()
