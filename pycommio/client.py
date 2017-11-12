
import socket

from pycommio.connection_handler import ConnectionHandler
from pycommio.communication_base import CommunicationBase


class Client(CommunicationBase):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = None
        super(Client, self).__init__()

    def connect(self):
        # Create a TCP/IP socket
        address = (self.host, self.port)
        sock = socket.create_connection(address)
        try:
            # Send data
            self.conn = ConnectionHandler(sock, self._event_handler, address)
            self.conn.start_thread()
        except:
            self.close()
            raise
    
    def close(self):
        self.conn.teardown()

    def send_event(self, *args, **kwargs):
        return self.conn.send_event(*args, **kwargs)

if __name__ == '__main__':
    client = Client('localhost', 5000)
    client.connect()
