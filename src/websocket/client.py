import socketio

from .namespaces.root_namespca import RootNamespace
from .namespaces.detection_namescape import DetectionNamespace
from .namespaces.config_namespcae import ConfigNamespace

class WebSocket:
    """ 
    Class that handles the websocket connection 

    Parameters
    ----------
    url : str
        The url of the websocket server
    """
    def __init__(self, url):
        self.root_namespace = RootNamespace('/')
        self.detection_namespace = DetectionNamespace('/detection')
        self.config_namespace = ConfigNamespace('/config')

        self._socketio = socketio.Client()
        self._socketio.register_namespace(self.root_namespace)
        self._socketio.register_namespace(self.detection_namespace)
        self._socketio.register_namespace(self.config_namespace)

        self._socketio.connect(url)


    # * Send Methods
    def request_configs(self):
        """ Request configs from server """
        self.config_namespace.emit('request_unit_configuration')


    def send_detections(self, id, classes):
        """ Send detections to server """
        self.detection_namespace.emit('detect', { 'id': id, 'detections': classes })