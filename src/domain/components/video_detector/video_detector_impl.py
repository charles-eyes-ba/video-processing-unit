from threading import Thread
from time import sleep

from src.domain.dependencies.ai_engine import AIEngine
from src.domain.dependencies.video_capture import VideoCapture
from src.common.call import call

from .interface import VideoDetector

from src.common.logger import logger

class VideoDetectorImpl(VideoDetector):
    def __init__(
        self, 
        id: str, 
        video_capture: VideoCapture, 
        ai_engine: AIEngine, 
        delay: int = 5
    ):
        self.id = id
        self._video_capture = video_capture
        self._ai_engine = ai_engine
        self._delay = delay
        
        self._last_detected_objects = []
        self._is_running = False
        self._thread = None
        
        self._on_object_detection = None
        self._on_error = None
        
        self._video_capture.setup_callbacks(on_error=self._on_video_capture_error)
        logger.debug(f'VideoDetectorImpl:{id}:initialized')


    # * Video Feed callbacks
    def _on_video_capture_error(self, exception: Exception):
        """ 
        Callback for the video capture error
        
        Parameters
        ----------
        exception : Exception
            The exception that occurred
        """
        self.stop()
        self._on_error(self.id, exception)
        
        
    # * Setups
    def setup_callbacks(
        self, 
        on_object_detection = None, 
        on_error = None
    ):
        self._on_object_detection = on_object_detection
        self._on_error = on_error


    # * Methods
    def start(self):
        if self._thread is not None and self._thread.is_alive():
            return
        
        self._video_capture.start()
        self._is_running = True
        self._thread = Thread(target=self._loop)
        self._thread.daemon = True
        self._thread.start()
        logger.debug(f'VideoDetectorImpl:{self.id}:started')
        
        
    def stop(self):
        self._is_running = False
        self._video_capture.stop()
        logger.debug(f'VideoDetectorImpl:{self.id}:stopped')
        
        
    def pause(self):
        self._is_running = False
        self._video_capture.pause()
        logger.debug(f'VideoDetectorImpl:{self.id}:paused')
    

    # * Main loop
    def _loop(self):
        """ Main loop of the video detector """
        while self._is_running:
            frame = self._video_capture.lastest_frame()

            if frame is not None:
                objects = self._ai_engine.extract_objects(frame)

                hasNewDetections = self._last_detected_objects != objects
                if hasNewDetections:
                    self._last_detected_objects = objects
                    call(self._on_object_detection, self.id, objects)
                    logger.debug(f'VideoDetectorImpl:{self.id}:_on_object_detection called')

            sleep(self._delay)