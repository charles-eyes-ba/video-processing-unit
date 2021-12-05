import socketio

from .namespaces.root_namespca import RootNamespace
from .namespaces.detection_namespcae import DetectionNamespace
from .namespaces.config_namespcae import ConfigNamespace

class WebSocketClient:
    """ 
    Class that handles the websocket connection 

    Parameters
    ----------
    url : str
        The url of the websocket server
    """
    def __init__(self, url):
        self.on_video_feeds_update = None
        self.on_add_video_feed = None
        self.on_remove_video_feed = None
        
        self.root_namespace = self.generate_root_namespace()
        self.detection_namespace = self.generate_detection_namespace()
        self.config_namespace = self.generate_config_namespace()

        self._socketio = socketio.Client()
        self._socketio.register_namespace(self.root_namespace)
        self._socketio.register_namespace(self.detection_namespace)
        self._socketio.register_namespace(self.config_namespace)

        self._socketio.connect(url)
        self.config_namespace.emit(ConfigNamespace.REQUEST_UNIT_CONFIGURATION)


    # * Setups Namespaces
    def generate_root_namespace(self):
        """ Generate the root namespace """
        return RootNamespace('/')


    def generate_detection_namespace(self):
        """ Generate the detection namespace """
        return DetectionNamespace('/detection')


    def generate_config_namespace(self):
        """ Generate the config namespace """
        config_namespace = ConfigNamespace('/config')
        config_namespace.on_request_unit_configuration = self.on_request_unit_configuration
        config_namespace.on_add_camera = self.on_add_camera
        config_namespace.on_remove_camera = self.on_remove_camera
        return config_namespace
    

    # * Receive Config Namespace
    def on_request_unit_configuration(self, config):
        """ Receive configs from server """
        if self.on_video_feeds_update != None:
            self.on_video_feeds_update(config['cameras'])
            
            
    def on_add_camera(self, vide_feed):
        """ Add a video feed to the server """
        if self.on_add_video_feed != None:
            self.on_add_video_feed(vide_feed)
            
            
    def on_remove_camera(self, video_feed_id):
        """ Remove a video feed from the server """
        if self.on_remove_video_feed != None:
            self.on_remove_video_feed(video_feed_id)
        

    # * Send Methods
    def request_configs(self):
        """ Request configs from server """
        self.config_namespace.emit('request_unit_configuration')


    def send_detections(self, id, classes):
        """ Send detections to server """
        print(f'Sending detections {id}')
        self.detection_namespace.emit('detect', { 'id': id, 'detections': classes })