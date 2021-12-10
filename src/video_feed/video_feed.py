from threading import Thread
from copy import deepcopy

from .exceptions import VideoFeedConnectionLost, VideoFeedCouldNotConntect

import cv2

class VideoFeed:
    """
    Class that wraps a video capture object and provides a lastest frame. It starts a thread that updates the lastest frame.
    
    Attributes
    ----------
    status : bool
        True if the lastest frame is valid
    frame : numpy.ndarray
        Lastest frame
    width : int
        Width of the video feed
    height : int
        Height of the video feed
    fps : int
        Frames per second of the video feed
    on_connection_error : function
        Function to be called when the video feed receive an error. 
        The function must accept a exception (VideoFeedConnectionLost, VideoFeedCouldNotConntect) as parameter.
        
    Methods
    -------
    release()
        Release the video capture object
    pop_lastest_frame()
        Pop the lastest frame
    """
    def __init__(self, feed_url, on_connection_error=None):
        """
        Parameters
        ----------
        feed_url : str or int
            URL (str) or code (int) to access remote video or local camera
        """
        self.status = None
        self.frame = None
        
        self.width = None
        self.height = None
        self.fps = None
        
        self.on_connection_error = on_connection_error
        
        self._video_capture = None
        self._feed_url = feed_url
        
        self._thread = Thread(target=self.__loop, args=())
        self._thread.daemon = True
        self._thread.start()
        
        
    def release(self):
        """ Release the video capture object """
        self._video_capture.release()


    def pop_lastest_frame(self):
        """ 
        Pop the lastest frame 
        
        Returns
        -------
        numpy.ndarray
            Lastest frame
        """
        frame = deepcopy(self.frame)
        self.frame = None
        return frame


    def __loop(self):
        """ 
        Loop that updates the lastest frame.
        
        Raises
        ------
        VideoFeedCouldNotConntect
            If the video feed could not be connected. Message Format: Could not connect to {feed_url}
        VideoFeedConnectionLost
            If the video feed connection was lost. Message Format: Lost connection to {feed_url}
        """
        try:
            self._video_capture = cv2.VideoCapture(self._feed_url)
        except Exception as e:
            exception = VideoFeedCouldNotConntect(f'Could not connect to {self._feed_url}')
            self.on_connection_error(exception)
            return
        
        self.width = int(self._video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self._video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self._video_capture.get(cv2.CAP_PROP_FPS))
        
        while True:
            try:
                self.status, self.frame = self._video_capture.read()
            except Exception as e:
                exception = VideoFeedConnectionLost(f'Lost connection to {self._feed_url}')
                self.on_connection_error(exception)
                return