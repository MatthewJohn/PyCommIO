

import socket

from connection_handler import ConnectionHandler


class Server(object):

    def __init__(self):
        self.running = False
        self.connections = {}

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

                client_obj = ConnectionHandler(self, client, address)
                self.connections[client_obj.get_id()] = client_obj
                client_obj.start_thread()
        except KeyboardInterrupt:
            self.stop_server()
            raise

    def stop_server(self):
        for connection_id in self.connections:
            try:
                self.connections[connection_id].teardown()
            except:
                pass


if __name__ == '__main__':
    server = Server()
    server.start('0.0.0.0', 5000)