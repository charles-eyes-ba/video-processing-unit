from threading import Thread
from time import sleep

class VideoProcessor:
    """ 
    Class that handles the video feed and the detection of the objects

    Attributes
    ----------
    id : str
        The id of the video processar (camera id)
    on_object_detection : function
        The function to call when an object is detected. The function must have the following signature: function(camera_id, classes)
        
    Methods
    -------
    start()
        Start the video processor
    """
    def __init__(self, id, video_feed, dnn, delay=5, on_object_detection=None):
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
        self._video_feed = video_feed
        self._dnn = dnn
        self._delay = delay
        self._last_detections_classes = []

        self._thread = Thread(target=self.__loop)
        self._thread.daemon = True

        self.on_object_detection = on_object_detection


    def start(self):
        """ Start the video processor """
        self._thread.start()


    def __loop(self):
        """ Main loop of the video processor """
        while True:
            frame = self._video_feed.pop_lastest_frame()

            if frame is not None:
                boxes, scores, classes = self._dnn.predict(frame)

                hasNewDetections = self._last_detections_classes != classes
                if hasNewDetections:
                    self._last_detections_classes = classes
                    self.on_object_detection(self.id, classes)

            sleep(self._delay)