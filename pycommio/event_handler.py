

class EventHandler(object):

    def __init__(self):
        self.events = {}
        self.on_connect = None
        self.on_disconnect = None
