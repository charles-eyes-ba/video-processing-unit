from src.domain.websocket import WebSocket

class MockWebSocket(WebSocket):
    
    def __init__(self):
        self.on_video_feeds_update = None
        self.on_add_video_feed = None
        self.on_remove_video_feed = None
        self.root_namespace = None
        self.detection_namespace = None
        self.config_namespace = None
        
        self._on_video_feeds_update = None
        self._on_add_video_feed = None
        self._on_remove_video_feed = None
        
        self.requested_config = False
        self.connected = False
        self.connected_params = None
        self.sent_detections = False
        self.sent_detections_params = None
        self.sent_error = False
        self.sent_error_params = None


    def setup_callbacks(self, 
                        on_connect=None, 
                        on_connect_error=None, 
                        on_disconnect=None, 
                        on_video_feeds_update=None, 
                        on_add_video_feed=None, 
                        on_remove_video_feed=None):
        self.on_connect = on_connect
        self.on_connect_error = on_connect_error
        self.on_disconnect = on_disconnect
        self._on_video_feeds_update = on_video_feeds_update
        self._on_add_video_feed = on_add_video_feed
        self._on_remove_video_feed = on_remove_video_feed
    

    def connect(self, url):
        self.connected = True
        self.connected_params = (url)
        

    def request_configs(self):
        self.requested_config = True


    def send_detections(self, id, classes):
        self.sent_detections = True
        self.sent_detections_params = (id, classes)
        
        
    def send_error(self, id, error):
        self.sent_error = True
        self.sent_error_params = (id, error)