from socketio import ClientNamespace
from src.common.call import call

class RootNamespace(ClientNamespace):
    """ Class that handles the root namespace """
    
    def __init__(self):
        super().__init__(namespace='/')
        self.on_connect_callback = None
        self.on_connect_error_callback = None
        self.on_disconnect_callback = None
        self.on_reconnect_callback = None
    
    
    def setup_callbacks(self, on_connect=None, on_connect_error=None, on_disconnect=None):
        """
        Setup the callbacks
        
        Parameters
        ----------
        on_connect : function
            Callback for when the connection is established
        on_connect_error : function
            Callback for when the connection fails
        on_disconnect : function
            Callback for when the connection is closed
        on_reconnect : function
            Callback for when the connection is re-established
        """
        self.on_connect_callback = on_connect
        self.on_connect_error_callback = on_connect_error
        self.on_disconnect_callback = on_disconnect
    
    
    def on_connect(self):
        """ Callback for when the connection is established """
        call(self.on_connect_callback)


    def on_connect_error(self, data):
        """ Callback for when the connection fails """
        call(self.on_connect_error_callback, data)


    def on_disconnect(self):
        """ Callback for when the connection is closed """
        call(self.on_disconnect_callback)