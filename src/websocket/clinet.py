import socketio

class RootNamespace(socketio.ClientNamespace):
    def on_connect(self):
        print('connected to server')

    def on_disconnect(self):
        print('disconnected from server')

    def on_reconnect(self):
        print('reconnected to server')

class DetecionNamesapce(socketio.ClientNamespace):
    pass

class WebSocket:
    def __init__(self, url):
        self.root_namespace = RootNamespace('/')
        self.detection_namespace = DetecionNamesapce('/detection')

        self._socketio = socketio.Client()
        self._socketio.register_namespace(self.root_namespace)
        self._socketio.register_namespace(self.detection_namespace)

        self._socketio.connect(url)

    def send_detections(self, id, classes):
        self.detection_namespace.emit(
            'video_processor_update', # TODO: update name
            {
                'id': id,
                'detections': classes
            }
        )