
import socket
from connection_handler import ConnectionHandler
from send_receive import send_msg

class Client(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        # Create a TCP/IP socket
        self.socket = socket.create_connection((self.host, self.port))
        try:
            # Send data
            
            conn = ConnectionHandler(self, self.socket)

            send_msg(self.socket, 'test MESSAGE!')
        finally:
            self.socket.close()

client = Client('localhost', 5000)
client.connect()
