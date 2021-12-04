from threading import Thread
from copy import deepcopy

import cv2

class VideoFeed:
    """
    Class that wraps a video capture object and provides a lastest frame
    
    Parameters
    ----------
    feed_url : str or int
        URL (str) or code (int) to access remote video or local camera
    """
    def __init__(self, feed_url):
        self.status = None
        self.frame = None
        
        self._video_capture = None
        self._feed_url = feed_url
        
        self.width = None
        self.height = None
        self.fps = None
        
        self._thread = Thread(target=self._update, args=())
        self._thread.daemon = True
        self._thread.start()
        
        
    def start(self):
        """ Start the video feed """
        
        
    def release(self):
        """ Release the video capture object """
        self._video_capture.release()


    def pop_lastest_frame(self):
        """ Pop the lastest frame """
        frame = deepcopy(self.frame)
        self.frame = None
        return frame


    def _update(self):
        """ Update the lastest frame """
        self._video_capture = cv2.VideoCapture(self._feed_url)
        
        self.width = int(self._video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self._video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self._video_capture.get(cv2.CAP_PROP_FPS))
        
        while True:
            self.status, self.frame = self._video_capture.read()