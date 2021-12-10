from threading import Thread
from time import sleep

class VideoProcessor:
    """ 
    Class that handles the video feed and the detection of the objects

    Attributes
    ----------
    id : str
        The id of the video processar (camera id)
    is_running : bool
        True if the video processor is running
    on_object_detection : function
        The function to call when an object is detected. The function must have the following signature: function(camera_id, classes)
    on_error : function
        The function to call when an error occurs. The function must have the following signature: function(camera_id, exception)
        
    Methods
    -------
    start()
        Start the video processor
    """
    def __init__(self, id, video_feed, dnn, delay=5):
        """
        Parameters
        ----------
        id : str
            The id of the camera
        video_feed : VideoFeed
            The video feed of the camera
        dnn : DNN
            The Deep Neural Network used to detect objects
        delay : int
            The delay between frames detection
        """
        self.id = id
        self._dnn = dnn
        self._delay = delay
        self._last_detections_classes = []
        self.is_running = False
        
        self._video_feed = video_feed
        self._video_feed.setup_callbacks(on_error=self._on_video_feed_error)

        self.on_object_detection = None
        self.on_error = None

        self._thread = Thread(target=self.__loop)
        self._thread.daemon = True


    # * Setups
    def setup_callbacks(self, on_object_detection=None, on_error=None):
        """ Setup the callbacks for the video processor """
        self.on_object_detection = on_object_detection
        self.on_error = on_error


    # * Methods
    def start(self):
        """ Start the video processor """
        self.is_running = True
        self._video_feed.start()
        self._thread.start()
        
        
    def stop(self):
        """ Stop the video processor """
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