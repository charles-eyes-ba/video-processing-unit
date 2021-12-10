from threading import Thread
from copy import deepcopy

from .interface import VideoFeed
from .exceptions import VideoFeedConnectionLost, VideoFeedCouldNotConntect

import cv2

class VideoFeedOpenCV(VideoFeed):
    def __init__(self, feed_url):
        self.status = None
        self.frame = None
        self.is_running = False
        
        self.width = None
        self.height = None
        self.fps = None
        
        self.on_error = None
        
        self._video_capture = None
        self._feed_url = feed_url
        
        self._thread = Thread(target=self.__loop)
        self._thread.daemon = True
        
        
    # * Setups
    def setup_callbacks(self, on_error=None):
        self.on_error = on_error
        
      
    # * Methods  
    def start(self):
        self.is_running = True
        self._thread.start()
    
    
    def stop(self):
        self.is_running = False
    
    
    def pop_lastest_frame(self):
        frame = deepcopy(self.frame)
        self.frame = None
        return frame
    
    
    def release(self):
        self._video_capture.release()
        self.is_running = False


    # * Main loop
    def __loop(self):
        """ 
        Loop that updates the lastest frame.
        
        Raises (at on_connection_error)
        -------------------------------
        VideoFeedCouldNotConntect
            If the video feed could not be connected. Message Format: Could not connect to {feed_url}
        VideoFeedConnectionLost
            If the video feed connection was lost. Message Format: Lost connection to {feed_url}
        """
        try:
            self._video_capture = cv2.VideoCapture(self._feed_url)
        except Exception as e:
            exception = VideoFeedCouldNotConntect(f'Could not connect to {self._feed_url}')
            if self.on_connection_error is not None:
                self.on_connection_error(exception)
            self.release()
            return
        
        self.width = int(self._video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self._video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self._video_capture.get(cv2.CAP_PROP_FPS))
        
        while self.is_running:
            try:
                self.status, self.frame = self._video_capture.read()
            except Exception as e:
                exception = VideoFeedConnectionLost(f'Lost connection to {self._feed_url}')
                if self.on_connection_error is not None:
                    self.on_connection_error(exception)
                self.release()
                return
        self.release()