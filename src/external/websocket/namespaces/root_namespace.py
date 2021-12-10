from socketio import ClientNamespace

class RootNamespace(ClientNamespace):
    """ Class that handles the root namespace """
    
    def __init__(self):
        super().__init__(namespace='/')
        self.on_connect_callback = None
        self.on_connect_error_callback = None
        self.on_disconnect_callback = None
        self.on_reconnect_callback = None
    
    def on_connect(self):
        """ Callback for when the connection is established """
        if self.on_connect_callback != None:
            self.on_connect_callback()

    def on_connect_error(self, data):
        """ Callback for when the connection fails """
        if self.on_connect_error_callback != None:
            self.on_connect_error_callback(data)

    def on_disconnect(self):
        """ Callback for when the connection is closed """
        if self.on_disconnect_callback != None:
            self.on_disconnect_callback()

    def on_reconnect(self):
        """ Callback for when the connection is re-established """
        if self.on_reconnect_callback != None:
            self.on_reconnect_callback()