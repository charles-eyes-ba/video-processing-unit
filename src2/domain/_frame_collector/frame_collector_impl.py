from threading import Thread
from copy import deepcopy

from src2.common.call import call
from .interface import FrameCollector

class FrameCollectorImpl(FrameCollector):
    def __init__(self, video_capture):
        self._frame = None
        self._is_running = False
        self._video_capture = video_capture
        
        self._on_error = None
        self._thread = None
        
        
    # * Setups
    def setup_callbacks(self, on_error=None):
        self._on_error = on_error
        
      
    # * Methods  
    def start(self):
        if self._thread is not None and self._thread.is_alive():
            return
        
        self._is_running = True
        self._thread = Thread(target=self.__loop)
        self._thread.daemon = True
        self._thread.start()
    
    
    def stop(self):
        self._is_running = False
    
    
    def pop_lastest_frame(self):
        frame = deepcopy(self._frame)
        self._frame = None
        return frame
    
    
    def release(self):
        self._video_capture.release()
        self._is_running = False


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
        while self._is_running:
            try:
                self._frame = self._video_capture.read()
            except Exception as e:
                call(self._on_error, e)
                break
        self.release()