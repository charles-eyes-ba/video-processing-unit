import socketio

from src.common.call import call
from .interface import WebSocket
from .namespaces.root_namespace import RootNamespace
from .namespaces.detection_namespace import DetectionNamespace
from .namespaces.config_namespace import ConfigNamespace

class WebSocketIO(WebSocket):
    
    def __init__(self):
        self._on_connect_callback = None
        self._on_connect_error_callback = None
        self._on_disconnect_callback = None
        self._on_video_feeds_update = None
        self._on_add_video_feed = None
        self._on_remove_video_feed = None
        
        self._root_namespace = self._generate_root_namespace()
        self._detection_namespace = self._generate_detection_namespace()
        self._config_namespace = self._generate_config_namespace()

        self._socketio = socketio.Client()
        self._socketio.register_namespace(self._root_namespace)
        self._socketio.register_namespace(self._detection_namespace)
        self._socketio.register_namespace(self._config_namespace)


    # * Setups
    def setup_callbacks(self, 
                        on_connect=None, 
                        on_connect_error=None, 
                        on_disconnect=None, 
                        on_video_feeds_update=None, 
                        on_add_video_feed=None, 
                        on_remove_video_feed=None):
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
        if self._socketio.connected:
            self._config_namespace.emit(ConfigNamespace.REQUEST_UNIT_CONFIGURATION)


    def send_detections(self, id, classes):
        if self._socketio.connected:
            self._detection_namespace.emit(DetectionNamespace.DETECT, { 'id': id, 'detections': classes })
    
    
    def send_error(self, id, error):
        if self._socketio.connected:
            self._detection_namespace.emit(DetectionNamespace.ERROR, { 'id': id, 'error': error.message })
    
    
    # * Generate Namespace
    def _generate_root_namespace(self):
        """ Generate the root namespace """
        root_namespace = RootNamespace()
        root_namespace.setup_callbacks(
            on_connect=self._on_connect, 
            on_connect_error=self._on_connect_error, 
            on_disconnect=self._on_disconnect, 
        )
        return root_namespace


    def _generate_detection_namespace(self):
        """ Generate the detection namespace """
        return DetectionNamespace()


    def _generate_config_namespace(self):
        """ Generate the config namespace """
        config_namespace = ConfigNamespace()
        config_namespace.setup_callbacks(
            on_request_unit_configuration=self._on_request_unit_configuration,
            on_add_camera=self._on_add_camera,
            on_remove_camera=self._on_remove_camera
        )
        return config_namespace
    

    # * Receive Root Namespace
    def _on_connect(self):
        """ Callback for when the connection is established """
        call(self._on_connect_callback)


    def _on_connect_error(self, data):
        """ Callback for when the connection fails """
        call(self._on_connect_error_callback, data)


    def _on_disconnect(self):
        """ Callback for when the connection is closed """
        call(self._on_disconnect_callback)


    # * Receive Config Namespace
    def _on_request_unit_configuration(self, config):
        """ 
        Receive configs from server 
        
        Parameters
        ----------
        config : dict
            All video feeds configs
        """
        call(self._on_video_feeds_update_callback, config['cameras'])
            
            
    def _on_add_camera(self, video_feed):
        """ 
        Add a video feed to the server 
        
        Parameters
        ----------
        video_feed : dict
            The video feed to add
        """
        call(self._on_add_video_feed_callback, video_feed)
            
            
    def _on_remove_camera(self, video_feed_id):
        """ 
        Remove a video feed from the server 
        
        Parameters
        ----------
        video_feed_id : str
            The id of the video feed to remove
        """
        call(self._on_remove_video_feed_callback, video_feed_id)