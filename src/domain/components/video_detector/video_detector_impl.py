from threading import Thread, Event
from time import sleep
from src.domain.dependencies.ai_engine import AIEngine
from src.domain.dependencies.video_capture import VideoCapture
from src.common.call import call
from src.common.logger import logger
from .interface import VideoDetector


class VideoDetectorImpl(VideoDetector):
    def __init__(
        self, 
        video_capture: VideoCapture, 
        ai_engine: AIEngine, 
        delay: int = 5
    ):
        self._video_capture = video_capture
        self._ai_engine = ai_engine
        self._delay = delay
        
        self._last_detected_objects = []
        self._event = Event()
        self._thread = None
        
        self._on_object_detection = None
        self._on_error = None
        
        self._video_capture.setup_callbacks(
            on_error=self._on_video_capture_error
        )
        logger.debug(f'Initialized')


    # * Video Feed callbacks
    def _on_video_capture_error(self, exception: Exception):
        """ 
        Callback for the video capture error
        
        Parameters
        ----------
        exception : Exception
            The exception that occurred
        """
        logger.debug(f'Got an video capture error {exception}')
        self.stop()
        self._on_error(exception)
        
        
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

        self._event.clear()
        self._video_capture.start()
        self._thread = Thread(target=self._video_detector_loop)
        self._thread.name = f' Thread-Video Detector {self._video_capture.url}'
        self._thread.daemon = True
        self._thread.start()
        logger.debug('Started')
        
        
    def stop(self):
        self._video_capture.stop()
        self._event.set()
        logger.debug('Stopped')
    

    # * Main loop
    def _video_detector_loop(self):
        """ Main loop of the video detector """
        while True:
            if self._event.is_set():
                break
            
            frame = self._video_capture.lastest_frame()

            if frame is not None:
                objects = self._ai_engine.extract_objects(frame)

                hasNewDetections = self._last_detected_objects != objects
                if hasNewDetections:
                    self._last_detected_objects = objects
                    call(self._on_object_detection, objects)
                    logger.debug(f'Detection callback called {objects}')

            sleep(self._delay)
        logger.debug('Ending the thread')