import cv2
from threading import Thread, Event, Lock
from copy import deepcopy
from src.common.logger import logger
from src.domain.dependencies.video_capture import VideoCapture
from src.common.call import call
from .exceptions import VideoCaptureCouldNotConnect, VideoCaptureConnectionLost


class OpenCVVideoCapture(VideoCapture):
    
    @property
    def url(self) -> str:
        return self._url
    
    
    def __init__(self, url: str):
        self._url = url
        self._cap = None
        self._frame = None
        self._on_error = None
        
        self._thread = None
        self._event = Event()
        self._lock = Lock()
        logger.debug(f'Initialized {self._url}')
    
        
    # * Setups
    def setup_callbacks(self, on_error = None):
        self._on_error = on_error
        
        
    # * Methods  
    def start(self):
        if self._thread is not None and self._thread.is_alive():
            return
        
        self._cap = cv2.VideoCapture(self._url)
        if self._cap is None or not self._cap.isOpened():
            exception = VideoCaptureCouldNotConnect(f'Could not connect to video source: {self._url}')
            call(self._on_error, exception)
            return
        
        self._event.clear()
        self._thread = Thread(target=self._loop)
        self._thread.name = f' Thread-Video Capture {self._url}'
        self._thread.daemon = True
        self._thread.start()
        logger.debug(f'Started the capture of {self._url}')
        
        
    def stop(self):
        self._event.set()
        logger.debug(f'Stopped the capture of {self._url}')
        
        
    def lastest_frame(self):
        self._lock.acquire()
        frame_copy = deepcopy(self._frame)
        self._lock.release()
        return frame_copy
        
        
    # * Utils
    def _release(self):
        self._cap.release()
        logger.debug('Released')
    
        
    # * Main loop
    def _loop(self):
        """ 
        Loop that updates the lastest frame.
        
        Raises (at on_error)
        -------------------------------
        VideoFeedConnectionLost
            If the video feed connection was lost. Message Format: Lost connection to {feed_url}
        """
        while True:
            if self._event.is_set():
                break
            try:
                self._lock.acquire()
                _, self._frame = self._cap.read()
                self._lock.release()
                
            except Exception as exception:
                logger.error(f'{self._url}:error')
                call(self._on_error, exception)
                break
            
        self._release()
        logger.debug('Ending the thread')