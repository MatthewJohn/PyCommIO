

from event_handler import EventHandler

class CommunicationBase(object):

    def __init__(self):
        self._event_handler = EventHandler()

    def on_connect(self, fnc):
        self._event_handler.on_connect = fnc
        return fnc

    def on(self, event_name):
        def register_function(fnc):
            self._event_handler.events[event_name] = fnc
            print self._event_handler.events
            return fnc
        register_function.event_name = event_name
        return register_function

    def on_disconnect(self, fnc):
        self._event_handler.on_disconnect = fnc
        return fnc
