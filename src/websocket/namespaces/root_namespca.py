from socketio import ClientNamespace

class RootNamespace(ClientNamespace):
    def __init__(self, namespace=None):
        super().__init__(namespace=namespace)
        self.on_connect_callback = None
        self.on_connect_error_callback = None
        self.on_disconnect_callback = None
        self.on_reconnect_callback = None
    
    def on_connect(self):
        if self.on_connect_callback != None:
            self.on_connect_callback()

    def on_connect_error(self, data):
        if self.on_connect_error_callback != None:
            self.on_connect_error_callback(data)

    def on_disconnect(self):
        if self.on_disconnect_callback != None:
            self.on_disconnect_callback()

    def on_reconnect(self):
        if self.on_reconnect_callback != None:
            self.on_reconnect_callback()