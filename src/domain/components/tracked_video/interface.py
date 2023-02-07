from abc import ABC, abstractmethod
from src.common.abstract_attribute import abstract_attribute
from src.models.video_feed import VideoFeed
from src.domain.components.video_detector import VideoDetector
from src.models.video_status import VideoStatus


class TrackedVideo(ABC):
    
    @abstract_attribute
    def video_feed(self) -> VideoFeed:
        """ Video feed infos """
        raise NotImplementedError('video_feed() must be defined')
    
    
    @abstract_attribute
    def video_detector(self) -> VideoDetector or None:
        """ Video detector information if exists """
        raise NotImplementedError('video_detector() must be defined')
    
    
    @abstract_attribute
    def video_detector_status(self) -> VideoStatus:
        """ Video detector status """
        raise NotImplementedError('video_detector_status() must be defined')
    
    
    @abstractmethod
    def __init__(self, video_feed: VideoFeed):
        """
        Initializer
        
        Paramters
        ---------
        video_feed: VideoFeed
            The video feed to track
        """
        raise NotImplementedError('__init__() must be defined')
        
    
    @abstractmethod    
    def stop(self):
        """ Stop to track the video """
        raise NotImplementedError('stop() must be defined')
        
    
    @abstractmethod
    def add_detector(self, video_detector: VideoDetector, on_object_detection, on_error):
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