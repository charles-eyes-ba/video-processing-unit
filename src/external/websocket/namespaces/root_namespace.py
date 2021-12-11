from socketio import ClientNamespace

class RootNamespace(ClientNamespace):
    """ Class that handles the root namespace """
    
    def __init__(self):
        super().__init__(namespace='/')
        self.on_connect_callback = None
        self.on_connect_error_callback = None
        self.on_disconnect_callback = None
        self.on_reconnect_callback = None
    
    
    def setup_callbacks(self, on_connect=None, on_connect_error=None, on_disconnect=None, on_reconnect=None):
        self.on_connect_callback = on_connect
        self.on_connect_error_callback = on_connect_error
        self.on_disconnect_callback = on_disconnect
        self.on_reconnect_callback = on_reconnect
    
    
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