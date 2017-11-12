
# PyConnIO

A simple two-communication for python server-client scenarios.

Sort of based on socket.io principles, but without the python compatibility issues.


## Server Example

    from pycommio.server import Server
    
    server = Server()
    
    @server.on_connect
    def conn(conn):
        print 'got a connection'
        conn.send_event('welcome', 'Some data')
        conn.send_event('welcome', {'maybe': ['a', 'dict']})
    
    @server.on_disconnect
    def disconnect(conn):
        print 'Connection lost'
    
    @server.on('conn_test')
    def conn_test(conn, data):
        print 'Client initiate: %s' % data
    
    @server.on('test')
    def test(conn, data):
        print 'got test data: %s' % data
    
    server.start('0.0.0.0', 5000)


## Client Example

    from pycommio.client import Client
    
    cl = Client('localhost', 5000)
    
    @cl.on_connect
    def on_conn(conn):
        conn.send_event('conn_test', 'some test data')
    
    @cl.on('welcome')
    def welcome(conn, data):
        print 'Server said: %s' % data
    
    @cl.on_disconnect
    def disconnect(conn):
        print 'Connection lost'
    
    cl.connect()
    cl.send_event('test', 'this is my data')

