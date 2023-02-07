from abc import ABC, abstractmethod

from src.domain.dependencies.ai_engine import AIEngine
from src.domain.dependencies.video_capture import VideoCapture
from src.domain.components.video_detector import VideoDetector
from src.domain.components.tracked_video import TrackedVideo

class DependencyInjector(ABC):
    
    # * AI Engine
    @abstractmethod
    def ai_engine(self) -> AIEngine:
        """ Return an instance of AIEngine """
        raise NotImplementedError('ai_engine() must be defined')
    
    
    # * Video Capture
    @abstractmethod
    def video_capture(self, url: str) -> VideoCapture:
        """ 
        Return an instance of VideoCapture 
        
        Parameters
        ----------
        url : str
            URL to retrive the video
        """
        raise NotImplementedError('video_capture() must be defined')
    
    
    # * Video Detector
    @abstractmethod
    def video_detector(self, video_capture: VideoCapture, ai_engine: AIEngine, delay: int = 5) -> VideoDetector:
        """ 
        Return an instance of VideoDetector 
        
        Parameters
        ----------
        video_capture : VideoCapture
            Video capture to analyze
        ai_engine : AIEngine
            AI framework to use in the video
        """
        raise NotImplementedError('video_detector() must be defined')
    
    
    # * Tracked Video
    def tracked_video(self, id: str, url: str) -> TrackedVideo:
        """ 
        Return an instance of VideoDetector 
        
        Parameters
        ----------
        id : str
            ID of the video
        url : str
            URL to retrive the video
        """
        raise NotImplementedError('tracked_video() must be defined')