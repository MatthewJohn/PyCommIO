



# Server Example

    from server import Server
    
    server = Server()
    
    @server.on_connect
    def conn(conn):
        print 'got a connection'
        conn.send_event('welcome', 'Some data')
        conn.send_event('welcome', {'maybe': ['a', 'dict']})
    
    @server.on('test')
    def test(conn, data):
        print 'got test data: %s' % data
    
    server.start('0.0.0.0', 5000)


# Client Example

    from client import Client

    cl = Client('localhost', 5000)

    @cl.on('welcome')
    def welcome(conn, data):
        print 'Server said: %s' % data
    
    cl.connect()
    cl.send_event('test', 'this is my data')

