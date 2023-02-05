from socketio import ClientNamespace
from src2.common.call import call

class RootNamespace(ClientNamespace):
    """ Class that handles the root namespace """
    
    UNIT_CONFIGURATION = 'request_unit_configuration'
    DETECT = 'detect'
    ERROR = 'error'
    
    def __init__(self):
        super().__init__(namespace='/')
        self.on_connect_callback = None
        self.on_connect_error_callback = None
        self.on_disconnect_callback = None
        self.on_request_unit_configuration_callback = None
        self.on_add_video_feed_callback = None
        self.on_remove_video_feed_callback = None
    
    
    def setup_callbacks(
        self, 
        on_connect: function = None, 
        on_connect_error: function = None, 
        on_disconnect: function = None, 
        on_request_unit_configuration: function = None, 
        on_add_video_feed: function = None, 
        on_remove_video_feed: function = None
    ):
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
        on_request_unit_configuration : function
            Callback for the request_unit_configuration event
        on_add_video_feed : function
            Callback for the add_camera event
        on_remove_video_feed : function
            Callback for the remove_camera event
        """
        self.on_connect_callback = on_connect
        self.on_connect_error_callback = on_connect_error
        self.on_disconnect_callback = on_disconnect
        self.on_request_unit_configuration_callback = on_request_unit_configuration
        self.on_add_video_feed_callback = on_add_video_feed
        self.on_remove_video_feed_callback = on_remove_video_feed
    
    
    # * Life Cycle
    def on_connect(self):
        """ Callback for when the connection is established """
        call(self.on_connect_callback)


    def on_connect_error(self, data):
        """ Callback for when the connection fails """
        call(self.on_connect_error_callback, data)


    def on_disconnect(self):
        """ Callback for when the connection is closed """
        call(self.on_disconnect_callback)
        
        
    # * Video Feeds
    def on_request_unit_configuration(self, data):
        """ Callback for the request_unit_configuration event """
        call(self.on_request_unit_configuration_callback, data)


    def on_add_camera(self, data):
        """ Callback for the add_camera event """
        call(self.on_add_video_feed_callback, data)
        

    def on_remove_camera(self, data):
        """ Callback for the remove_camera event """
        call(self.on_remove_video_feed_callback, data)