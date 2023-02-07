from abc import ABC, abstractmethod
from src.common.abstract_attribute import abstract_attribute
from src.models.video_feed import VideoFeed
from src.domain.components.video_detector import VideoDetector
from src.dependency_injector import DependencyInjector


class TrackedVideo(ABC):
    
    @abstract_attribute
    def video_feed(self) -> VideoFeed:
        raise NotImplementedError('video_feed() must be defined')
    
    
    @abstract_attribute
    def video_detector(self) -> VideoDetector or None:
        raise NotImplementedError('video_detector() must be defined')
    
    
    @abstractmethod
    def __init__(self, dependencies: DependencyInjector, id: str, url: str):
        raise NotImplementedError('__init__() must be defined')
        
    
    @abstractmethod
    def start_detector(self, on_object_detection, on_error):
        raise NotImplementedError('start_detector() must be defined')