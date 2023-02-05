import logging
import socketio

from src2.common.call import call
from src2.domain.websocket import WebSocket
from .namespaces.root_namespace import RootNamespace

class WebSocketIO(WebSocket):
    
    def __init__(self):
        self._on_connect_callback = None
        self._on_connect_error_callback = None
        self._on_disconnect_callback = None
        self._on_video_feeds_update_callback = None
        self._on_add_video_feed_callback = None
        self._on_remove_video_feed_callback = None
        
        self._root_namespace = self._generate_root_namespace()

        self._socketio = socketio.Client()
        self._socketio.register_namespace(self._root_namespace)


    # * Setups
    def setup_callbacks(
        self, 
        on_connect: function = None, 
        on_connect_error: function = None, 
        on_disconnect: function = None, 
        on_video_feeds_update: function = None, 
        on_add_video_feed: function = None, 
        on_remove_video_feed: function = None
    ):
        self._on_connect_callback = on_connect
        self._on_connect_error_callback = on_connect_error
        self._on_disconnect_callback = on_disconnect
        self._on_video_feeds_update_callback = on_video_feeds_update
        self._on_add_video_feed_callback = on_add_video_feed
        self._on_remove_video_feed_callback = on_remove_video_feed
    
    
    # * Methods
    def connect(self, url):
        self._socketio.connect(url)
        

    # * Send Methods
    def request_configs(self):
        try:
            self._root_namespace.emit(RootNamespace.UNIT_CONFIGURATION)
        except:
            logging.error('WS:Error requesting configs')


    def send_detections(self, id, classes):
        try:
            self._root_namespace.emit(RootNamespace.DETECT, { 'id': id, 'classes': classes })
        except:
            logging.error('WS:Error sending detections')
    
    
    def send_error(self, id, error):
        try:
            self._root_namespace.emit(RootNamespace.ERROR, { 'id': id, 'error': error.message })
        except:
            logging.error('WS:Error sending error')
    
    
    # * Generate Namespace
    def _generate_root_namespace(self):
        """ Generate the config namespace """
        root_namespace = RootNamespace()
        root_namespace.setup_callbacks(
            on_connect=self._on_connect, 
            on_connect_error=self._on_connect_error, 
            on_disconnect=self._on_disconnect, 
            on_request_unit_configuration=self._on_request_unit_configuration,
            on_add_video_feed=self._on_add_video_feed,
            on_remove_video_feed=self._on_remove_video_feed
        )
        return root_namespace
    

    # * Receive Events
    def _on_connect(self):
        """ On connect event """
        logging.debug('WS:Connected event')
        call(self._on_connect_callback)
        
        
    def _on_connect_error(self, data):
        """ On connect error event """
        logging.debug('WS:Connect error event')
        call(self._on_connect_error_callback)


    def _on_disconnect(self):
        """ On disconnect event """
        logging.debug('WS:Disconnected event')
        call(self._on_disconnect_callback)
        
    
    def _on_request_unit_configuration(self, config):
        """ 
        On receive configs from server 
        
        Parameters
        ----------
        config : dict
            All video feeds configs
        """
        logging.debug('WS:Request unit configuration event')
        call(self._on_video_feeds_update_callback, config['cameras'])
            
            
    def _on_add_video_feed(self, video_feed):
        """ 
        On add a video feed to the server 
        
        Parameters
        ----------
        video_feed : dict
            The video feed to add
        """
        logging.debug('WS:Add video feed event')
        call(self._on_add_video_feed_callback, video_feed)
            
            
    def _on_remove_video_feed(self, video_feed_id):
        """ 
        On remove a video feed from the server 
        
        Parameters
        ----------
        video_feed_id : str
            The id of the video feed to remove
        """
        logging.debug('WS:Remove video feed event')
        call(self._on_remove_video_feed_callback, video_feed_id)