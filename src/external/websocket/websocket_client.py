import socketio

from .namespaces.root_namespace import RootNamespace
from .namespaces.detection_namespace import DetectionNamespace
from .namespaces.config_namespace import ConfigNamespace

class WebSocketClient:
    """ 
    Class that handles the websocket connection 

    Attributes
    ----------
    on_video_feeds_update : function
        Function that is called when the all video feeds are updated
    on_add_video_feed : function
        Function that is called when a new video feed is added
    on_remove_video_feed : function
        Function that is called when a video feed is removed
    root_namespace : RootNamespace
        The root namespace. Can be used to send messages in websocket with root namespace 
    detection_namespace : DetectionNamespace
        The detection namespace. Can be used to send messages in websocket with detection namespace
    config_namespace : ConfigNamespace
        The config namespace. Can be used to send messages in websocket with config namespace
    
    Methods
    -------
    request_configs()
        Request configs from server
    send_detections(id, classes)
        Send detections to server
    """
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
        """ 
        Setup the callbacks 
        
        Parameters
        ----------
        on_video_feeds_update : function
            Function that is called when the all video feeds are updated
        on_add_video_feed : function
            Function that is called when a new video feed is added
        on_remove_video_feed : function
            Function that is called when a video feed is removed
        """
        self.on_video_feeds_update = on_video_feeds_update
        self.on_add_video_feed = on_add_video_feed
        self.on_remove_video_feed = on_remove_video_feed
    
    
    def _generate_root_namespace(self):
        """ Generate the root namespace """
        return RootNamespace()


    def _generate_detection_namespace(self):
        """ Generate the detection namespace """
        return DetectionNamespace()


    def _generate_config_namespace(self):
        """ Generate the config namespace """
        config_namespace = ConfigNamespace()
        config_namespace.on_request_unit_configuration = self._on_request_unit_configuration
        config_namespace.on_add_camera = self._on_add_camera
        config_namespace.on_remove_camera = self._on_remove_camera
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
        if self.on_video_feeds_update is not None:
            self.on_video_feeds_update(config['cameras'])
            
            
    def _on_add_camera(self, video_feed):
        """ 
        Add a video feed to the server 
        
        Parameters
        ----------
        video_feed : dict
            The video feed to add
        """
        if self.on_add_video_feed is not None:
            self.on_add_video_feed(video_feed)
            
            
    def _on_remove_camera(self, video_feed_id):
        """ 
        Remove a video feed from the server 
        
        Parameters
        ----------
        video_feed_id : str
            The id of the video feed to remove
        """
        if self.on_remove_video_feed is not None:
            self.on_remove_video_feed(video_feed_id)
        
        
    # * Methods
    def connect(self, url):
        """
        Parameters
        ----------
        url : str
            The url of the websocket server
        """
        self._socketio.connect(url)
        

    # * Send Methods
    def request_configs(self):
        """ Request configs from server """
        self.config_namespace.emit(ConfigNamespace.REQUEST_UNIT_CONFIGURATION)


    def send_detections(self, id, classes):
        """ 
        Send detections to server 
        
        Parameters
        ----------
        id : str
            The id of the video feed
        classes : list
            The classes name detected in the video feed
        """
        self.detection_namespace.emit(DetectionNamespace.DETECT, { 'id': id, 'detections': classes })