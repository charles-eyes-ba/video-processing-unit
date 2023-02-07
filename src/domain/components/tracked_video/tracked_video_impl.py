from src.models.video_feed import VideoFeed
from src.domain.components.video_detector import VideoDetector
from src.dependency_injector import DependencyInjector
from .interface import TrackedVideo


class TrackedVideoImpl(TrackedVideo):
    
    @property
    def video_feed(self) -> VideoFeed:
        return self._video_feed
    
    
    @property
    def video_detector(self) -> VideoDetector or None:
        return self._video_detector
    
    
    def __init__(self, dependencies: DependencyInjector, id: str, url: str):
        self._dependencies = dependencies
        self._video_feed = VideoFeed(id, url)
        self._video_detector = None
        
        
    def start_detector(self, on_object_detection, on_error):
        ai_engine = self._dependencies.ai_engine()
        video_capture = self._dependencies.video_capture(self._video_feed.url)
        self._video_detector = self._dependencies.video_detector(video_capture, ai_engine)
        
        self._video_detector.setup_callbacks(
            on_object_detection = lambda objects: on_object_detection(self._video_feed.id, objects),
            on_error = lambda error: on_object_detection(self._video_feed.id, error)
        )
        self._video_detector.start()