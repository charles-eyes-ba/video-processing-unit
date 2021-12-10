from threading import Thread
from time import sleep

from .interface import VideoProcessor

class VideoProcessorImpl(VideoProcessor):
    def __init__(self, id, video_feed, dnn, delay=5):
        self.id = id
        self._dnn = dnn
        self._delay = delay
        self._last_detections_classes = []
        self.is_running = False
        
        self._video_feed = video_feed
        self._video_feed.setup_callbacks(on_error=self._on_video_feed_error)

        self._on_object_detection = None
        self._on_error = None

        self._thread = Thread(target=self.__loop)
        self._thread.daemon = True


    # * Setups
    def setup_callbacks(self, on_object_detection=None, on_error=None):
        self._on_object_detection = on_object_detection
        self._on_error = on_error


    # * Methods
    def start(self):
        self.is_running = True
        self._video_feed.start()
        self._thread.start()
        
        
    def stop(self):
        self.is_running = False
        self._video_feed.stop()


    # * Video Feed callbacks
    def _on_video_feed_error(self, id, exception):
        """ 
        Callback for the video feed error 
        
        Parameters
        ----------
        id : str
            The id of the camera
        exception : Exception
            The exception that occurred
        """
        self.is_running = False
        self.on_error(id, exception)
    

    # * Main loop
    def __loop(self):
        """ Main loop of the video processor """
        while self.is_running:
            frame = self._video_feed.pop_lastest_frame()

            if frame is not None:
                boxes, scores, classes = self._dnn.predict(frame)

                hasNewDetections = self._last_detections_classes != classes
                if hasNewDetections:
                    self._last_detections_classes = classes
                    if self.on_object_detection is not None:
                        self.on_object_detection(self.id, classes)

            sleep(self._delay)