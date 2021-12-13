import socketio

from src.common.call import call
from .interface import WebSocket
from .namespaces.root_namespace import RootNamespace
from .namespaces.detection_namespace import DetectionNamespace
from .namespaces.config_namespace import ConfigNamespace

class WebSocketIO(WebSocket):
    
    def __init__(self):
        self.on_video_feeds_update = None
        self.on_add_video_feed = None
        self.on_remove_video_feed = None
        
        self.root_namespace = self._generate_root_namespace()
        self.detection_namespace = self._generate_detection_namespace()
        self.config_namespace = self._generate_config_namespace()

        self._socketio = socketio.Client()
        self._socketio.register_namespace(self.root_namespace)
        self._socketio.register_namespace(self.detection_namespace)
        self._socketio.register_namespace(self.config_namespace)


    # * Setups
    def setup_callbacks(self, on_video_feeds_update=None, on_add_video_feed=None, on_remove_video_feed=None):
        self.on_video_feeds_update = on_video_feeds_update
        self.on_add_video_feed = on_add_video_feed
        self.on_remove_video_feed = on_remove_video_feed
    
    
    # * Methods
    def connect(self, url):
        self._socketio.connect(url)
        

    # * Send Methods
    def request_configs(self):
        self.config_namespace.emit(ConfigNamespace.REQUEST_UNIT_CONFIGURATION)


    def send_detections(self, id, classes):
        self.detection_namespace.emit(DetectionNamespace.DETECT, { 'id': id, 'detections': classes })
    
    
    def send_error(self, id, error):
        raise NotImplementedError('send_error() must be implemented')
    
    
    # * Generate Namespace
    def _generate_root_namespace(self):
        """ Generate the root namespace """
        return RootNamespace()


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
    

    # * Receive Config Namespace
    def _on_request_unit_configuration(self, config):
        """ 
        Receive configs from server 
        
        Parameters
        ----------
        config : dict
            All video feeds configs
        """
        call(self.on_video_feeds_update, config['cameras'])
            
            
    def _on_add_camera(self, video_feed):
        """ 
        Add a video feed to the server 
        
        Parameters
        ----------
        video_feed : dict
            The video feed to add
        """
        call(self.on_add_video_feed, video_feed)
            
            
    def _on_remove_camera(self, video_feed_id):
        """ 
        Remove a video feed from the server 
        
        Parameters
        ----------
        video_feed_id : str
            The id of the video feed to remove
        """
        call(self.on_remove_video_feed, video_feed_id)