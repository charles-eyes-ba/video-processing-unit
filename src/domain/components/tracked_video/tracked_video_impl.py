from src.models.video_feed import VideoFeed
from src.domain.components.video_detector import VideoDetector
from .interface import TrackedVideo


class TrackedVideoImpl(TrackedVideo):
    
    @property
    def video_feed(self) -> VideoFeed:
        return self._video_feed
    
    
    @property
    def video_detector(self) -> VideoDetector or None:
        return self._video_detector
    
    
    def __init__(self, video_feed: VideoFeed):
        self._video_feed = video_feed
        self._video_detector = None
        
        
    def add_detector(self, video_detector: VideoDetector, on_object_detection, on_error):
        self._video_detector = video_detector
        self._video_detector.setup_callbacks(
            on_object_detection = lambda objects: on_object_detection(self._video_feed.id, objects),
            on_error = lambda error: on_error(self._video_feed.id, error)
        )
        self._video_detector.start()