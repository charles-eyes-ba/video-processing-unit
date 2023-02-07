from src.models.video_feed import VideoFeed
from src.models.video_config import VideoConfig
from src.models.video_status import VideoStatus
from src.domain.components.video_detector import VideoDetector
from src.common.logger import logger
from .interface import TrackedVideo


class TrackedVideoImpl(TrackedVideo):
    
    @property
    def video_feed(self) -> VideoFeed:
        return self._video_feed
    
    # * Video Detector
    @property
    def video_detector(self) -> VideoDetector or None:
        return self._video_detector
    
    @property
    def video_detector_status(self) -> VideoStatus:
        return self._video_detector_status
    
    
    # * Init
    def __init__(self, video_feed: VideoFeed):
        self._video_feed = video_feed
        self._video_detector = None
        self._video_detector_status = VideoStatus.OFF
        logger.debug('Initialized')
        
        
    # * Interfaces
    def set_config(self, config: VideoConfig):
        logger.debug(f'New config received {config.__dict__}')
        if config.run_detector:
            self._video_detector_status = VideoStatus.RUNNING
            self._video_detector.start()
        else:
            self._video_detector_status = VideoStatus.OFF
            self._video_detector.stop()
        
    
    def stop(self):
        logger.debug('Stopping')
        self._video_detector.stop()
        
        
    # * Detector
    def add_detector(self, video_detector: VideoDetector, on_object_detection, on_error):
        logger.debug('Adding detector')
        def _object_detection(objects: list[str]):
            on_object_detection(self._video_feed.id, objects)
            
        def _error(error: Exception):
            self._video_detector.stop()
            self._video_detector_status = VideoStatus.ERROR
            on_error(self._video_feed.id, error)
            
        self._video_detector = video_detector
        self._video_detector.setup_callbacks(
            _object_detection,
            _error
        )