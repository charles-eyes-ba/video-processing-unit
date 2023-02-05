from threading import Thread
from copy import deepcopy
import cv2
import logging

from src.domain.dependencies.video_capture import VideoCapture
from src.common.call import call
from .exceptions import VideoCaptureCouldNotConnect, VideoCaptureConnectionLost

class OpenCVVideoCapture(VideoCapture):
    def __init__(self, url: str):
        self._url = url
        self._cap = None
        self._frame = None
        self._is_running = False
        self._on_error = None
        self._thread = None
        logging.info(':OpenCVVideoCapture: initialized')
    
        
    # * Setups
    def setup_callbacks(self, on_error = None):
        self._on_error = on_error
        
        
    # * Methods  
    def start(self):
        if self._thread is not None and self._thread.is_alive():
            self._is_running = True
            return
        
        self._cap = cv2.VideoCapture(self._url)
        if self._cap is None or not self._cap.isOpened():
            raise VideoCaptureCouldNotConnect(f'Could not connect to video source: {self.__url}')
        
        self._is_running = True
        self._thread = Thread(target=self._loop)
        self._thread.daemon = True
        self._thread.start()
        
        
    def stop(self):
        self._is_running = False
        self._release()
        
        
    def pause(self):
        self._is_running = False
        
        
    def pop_lastest_frame(self):
        frame = deepcopy(self._frame)
        self._frame = None
        return frame
        
        
    # * Utils
    def _release(self):
        self._cap.release()
        self._is_running = False
        
        
    def _read(self):
        try:
            _, frame = self._cap.read()
        except:
            raise VideoCaptureConnectionLost(f'Connection to video source lost: {self._url}')
        return frame
    
        
    # * Main loop
    def _loop(self):
        """ 
        Loop that updates the lastest frame.
        
        Raises (at on_error)
        -------------------------------
        VideoFeedConnectionLost
            If the video feed connection was lost. Message Format: Lost connection to {feed_url}
        """
        while self._is_running:
            try:
                self._frame = self._read()
            except Exception as e:
                call(self._on_error, e)
                break
        self._release()