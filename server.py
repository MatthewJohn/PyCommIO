

import socket

from connection_handler import ConnectionHandler
from communication_base import CommunicationBase


class Server(CommunicationBase):

    def __init__(self):
        self.running = False
        self.connections = {}
        super(Server, self).__init__()

    def start(self, address, port):
        try:
            self.running = True
            # Create socket object
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Bind to port/address
            self.socket.bind((address, port))
            self.socket.listen(5)
            while self.running:
                # Handle connection
                client, address = self.socket.accept()

                client_obj = ConnectionHandler(client, self._event_handler, address)
                self.connections[client_obj.get_id()] = client_obj
                client_obj.start_thread()
        except KeyboardInterrupt:
            self.close()
            raise

    def close(self):
        for connection_id in self.connections:
            try:
                self.connections[connection_id].teardown()
            except:
                pass


if __name__ == '__main__':
    server = Server()
    @server.on_connect()
    def conn(conn):
        print 'got a connection'
        conn.send_event('welcome', '')
    @server.on('test')
    def test(conn, data):
        print 'got test data: %s' % data
    server.start('0.0.0.0', 5000)