
import threading
import uuid

from send_receive import send_msg, get_msg


class ConnectionHandler(object):

    def __init__(self, conn, address=None):
        self._send_lock = threading.Lock()
        self._conn = conn
        self._address = address
        self._loop = False
        self._client_id = self._generate_client_id()
        self._thread = threading.Thread(target=self._socket_handler)

    def send_data(self, data):
        self._send_lock.aquire(True)
        self._conn.send(data)
        self._send_lock.release()

    def get_id(self):
        return self._client_id

    def _generate_client_id(self):
        # Tempmorary solution
        return uuid.uuid4().hex

    def start_thread(self):
        self._loop = True
        self._thread.start()

    def teardown(self):
        self._loop = False
        self._conn.close()

    def _socket_handler(self):
        try:
            while self._loop:
                data = get_msg(self._conn)
                if data:
                    print data
        except:
            self.teardown()