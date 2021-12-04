import socketio

from .namespaces.root_namespca import RootNamespace
from .namespaces.detection_namescape import DetectionNamespace

class WebSocket:
    """ Class that handles the websocket connection """
    def __init__(self, url):
        self.root_namespace = RootNamespace('/')
        self.detection_namespace = DetectionNamespace('/detection')

        self._socketio = socketio.Client()
        self._socketio.register_namespace(self.root_namespace)
        self._socketio.register_namespace(self.detection_namespace)

        self._socketio.connect(url)

    def send_detections(self, id, classes):
        """ Send detections to server """
        self.detection_namespace.emit(
            'video_processor_update', # TODO: update name
            {
                'id': id,
                'detections': classes
            }
        )