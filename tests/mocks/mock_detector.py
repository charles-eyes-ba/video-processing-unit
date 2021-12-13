from src.domain.detector import Detector

class MockDetector(Detector):
    def __init__(self, id, frame_collector, dnn, delay=5):
        self.id = id
        self._frame_collector = frame_collector
        
        self._on_object_detection = None
        self._on_error = None
        
        self.started = False
        self.stopped = False


    def setup_callbacks(self, on_object_detection=None, on_error=None):
        self._on_object_detection = on_object_detection
        self._on_error = on_error


    def start(self):
        self.started = True
        
    
    def stop(self):
        self.stopped = True