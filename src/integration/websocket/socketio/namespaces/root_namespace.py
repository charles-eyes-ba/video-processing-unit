from socketio import ClientNamespace
from src.common.call import call

class RootNamespace(ClientNamespace):
    """ Class that handles the root namespace """
    
    VIDEO_FEED_IDS = 'video_feed_ids'
    DETECT = 'detect'
    ERROR = 'error'
    
    def __init__(self):
        super().__init__(namespace='/')
        self._on_connect_callback = None
        self._on_connect_error_callback = None
        self._on_disconnect_callback = None
        self._on_request_current_video_feed_list_callback = None
        self._on_video_feed_list_update_callback = None
        self._on_add_video_feed_callback = None
        self._on_remove_video_feed_callback = None
    
    
    def setup_callbacks(
        self, 
        on_connect = None, 
        on_connect_error = None, 
        on_disconnect = None, 
        on_request_current_video_feed_list = None,
        on_video_feed_list_update = None, 
        on_add_video_feed = None, 
        on_remove_video_feed = None
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
        _on_video_feed_list_update_callback : function
            Callback for the request_unit_configuration event
        on_add_video_feed : function
            Callback for the add_video_feed event
        on_remove_video_feed : function
            Callback for the remove_video_feed event
        """
        self._on_connect_callback = on_connect
        self._on_connect_error_callback = on_connect_error
        self._on_disconnect_callback = on_disconnect
        self._on_request_current_video_feed_list_callback = on_request_current_video_feed_list
        self._on_video_feed_list_update_callback = on_video_feed_list_update
        self._on_add_video_feed_callback = on_add_video_feed
        self._on_remove_video_feed_callback = on_remove_video_feed
    
    
    # * Life Cycle
    def on_connect(self):
        """ Callback for when the connection is established """
        call(self._on_connect_callback)


    def on_connect_error(self, data):
        """ Callback for when the connection fails """
        call(self._on_connect_error_callback)


    def on_disconnect(self):
        """ Callback for when the connection is closed """
        call(self._on_disconnect_callback)
        
        
    # * Video Feeds
    def on_request_current_video_feed_list(self):
        """ Callback for when the server request the current video feed list """
        call(self._on_request_current_video_feed_list_callback)
    
    
    def on_video_feed_list_update(self, data):
        """ Callback for the video_feed_list_update event """
        call(self._on_video_feed_list_update_callback, data)
        
        
    def on_add_video_feed(self, data):
        """ Callback for the add_video_feed event """
        call(self._on_add_video_feed_callback, data)
        

    def on_remove_video_feed(self, data):
        """ Callback for the remove_video_feed event """
        call(self._on_remove_video_feed_callback, data)