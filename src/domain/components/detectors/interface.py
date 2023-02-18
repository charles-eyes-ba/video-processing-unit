from abc import ABC, abstractmethod
from src.common.abstract_attribute import abstract_attribute
from src.domain.dependencies.video_capture import VideoCapture
from src.domain.dependencies.ai_engine import AIEngine


class Detector(ABC):
    """ Common interface for all detectos """
    
    @abstract_attribute
    def id(self) -> str:
        """ ID (same of video_feed.id) """
        raise NotImplementedError('id() must be defined')
    
    
    @abstractmethod
    def __init__(self, video_capture: VideoCapture, ai_engine: AIEngine, delay: int):
        """
        Initializer
        
        Parameters
        ----------
        video_capture : VideoCapture
            Video capture to analyze
        ai_engine : AIEngine
            Framework to execute the IA algorithms
        delay : int
            Delay to rerun the IA algorithms
        """
        raise NotImplementedError('__init__() not implemented')


    @abstractmethod
    def start(self):
        """ Start the detector """
        raise NotImplementedError('start() not implemented')
        
    
    @abstractmethod
    def stop(self):
        """ Stop the detector """
        raise NotImplementedError('stop() not implemented')