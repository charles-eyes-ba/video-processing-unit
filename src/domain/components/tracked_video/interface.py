from abc import ABC, abstractmethod
from src.common.abstract_attribute import abstract_attribute
from src.models.video_feed import VideoFeed
from src.models.video_config import VideoConfig
from src.models.status import Status
from .dependencies import TrackedVideoDependencies


class TrackedVideo(ABC):
    """ Handle a tracked video """
    
    @abstract_attribute
    def id(self) -> str:
        """ ID (same of video_feed.id) """
        raise NotImplementedError('id() must be defined')
    
    
    @abstract_attribute
    def frame_collector_status(self) -> Status:
        """ Video detector status """
        raise NotImplementedError('frame_collector_status() must be defined')
    
    
    @abstract_attribute
    def object_detector_status(self) -> Status:
        """ Video detector status """
        raise NotImplementedError('object_detector_status() must be defined')
    
    
    @abstractmethod
    def __init__(self, dependencies: TrackedVideoDependencies, video_feed: VideoFeed):
        """
        Initializer
        
        Paramters
        ---------
        video_feed: VideoFeed
            The video feed to track
        dependencies: TrackedVideoDependencies
            Dependencies for the component
        """
        raise NotImplementedError('__init__() must be defined')
        
    
    @abstractmethod    
    def set_config(self, config: VideoConfig):
        """
        Run/Stop the workers following the config
        
        Paramters
        ---------
        config: VideoConfig
            Config to run/stop all the workers
        """
        raise NotImplementedError('set_config() must be defined')
    
    
    @abstractmethod    
    def stop(self):
        """ Stop to track the video """
        raise NotImplementedError('stop() must be defined')
        
    
    @abstractmethod
    def setup_detector(self, on_object_detection, on_error):
        """
        Initialize and start detection in the video
        
        Parameters
        ----------
        on_object_detection: function
            Callback when a new detection happens
        on_error: function
            Callback when the video results in error
        """
        raise NotImplementedError('start_detector() must be defined')