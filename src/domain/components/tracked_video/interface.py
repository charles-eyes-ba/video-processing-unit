from abc import ABC, abstractmethod
from src.common.abstract_attribute import abstract_attribute
from src.models.video_feed import VideoFeed
from src.domain.components.video_detector import VideoDetector


class TrackedVideo(ABC):
    
    @abstract_attribute
    def video_feed(self) -> VideoFeed:
        """ Video feed infos """
        raise NotImplementedError('video_feed() must be defined')
    
    
    @abstract_attribute
    def video_detector(self) -> VideoDetector or None:
        """ Video detector information if exists """
        raise NotImplementedError('video_detector() must be defined')
    
    
    @abstractmethod
    def __init__(self, id: str, url: str):
        """
        Initializer
        
        Paramters
        ---------
        dependencies: DependencyInjector
            Dependencies to use if necessary
        id: str
            ID for the video
        url: str
            URL to retrive the video
        """
        raise NotImplementedError('__init__() must be defined')
        
    
    @abstractmethod
    def start_detector(self, on_object_detection, on_error):
        """
        Initialize and start detection in the video
        
        Parameters
        ----------
        on_object_detection : function
            Callback when a new detection happens
        on_error : function
            Callback when the video results in error
        """
        raise NotImplementedError('start_detector() must be defined')