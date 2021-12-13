from threading import Thread
from time import sleep

from src.common.call import call
from .interface import Detector

class DetectorImpl(Detector):
    def __init__(self, id, frame_collector, dnn, delay=5):
        self.id = id
        self._dnn = dnn
        self._delay = delay
        self._last_detections_classes = []
        self._is_running = False
        
        self._frame_collector = frame_collector
        self._frame_collector.setup_callbacks(on_error=self._on_frame_collector_error)

        self._on_object_detection = None
        self._on_error = None
        self._thread = None


    # * Setups
    def setup_callbacks(self, on_object_detection=None, on_error=None):
        self._on_object_detection = on_object_detection
        self._on_error = on_error


    # * Methods
    def start(self):
        self._frame_collector.start()
        
        if self._thread.is_alive():
            return
        self._is_running = True
        self._thread = Thread(target=self.__loop)
        self._thread.daemon = True
        self._thread.start()
        
        
    def stop(self):
        self._is_running = False
        self._frame_collector.stop()
        
        
    def pause(self):
        self._is_running = False


    # * Video Feed callbacks
    def _on_frame_collector_error(self, exception):
        """ 
        Callback for the video capture error
        
        Parameters
        ----------
        exception : Exception
            The exception that occurred
        """
        self.stop()
        self._on_error(self.id, exception)
    

    # * Main loop
    def __loop(self):
        """ Main loop of the detector """
        while self._is_running:
            frame = self._frame_collector.pop_lastest_frame()

            if frame is not None:
                boxes, scores, classes = self._dnn.predict(frame)

                hasNewDetections = self._last_detections_classes != classes
                if hasNewDetections or True:
                    self._last_detections_classes = classes
                    call(self._on_object_detection, self.id, classes)

            sleep(self._delay)