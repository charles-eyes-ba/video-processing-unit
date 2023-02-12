from abc import ABC, abstractmethod
from src.models.video_feed import VideoFeed

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.domain.dependencies.ai_engine import AIEngine
    from src.domain.dependencies.video_capture import VideoCapture
    from src.domain.components.video_detector import VideoDetector
    from src.domain.components.tracked_video import TrackedVideo
    from src.domain.dependencies.websocket import WebSocket


class DependencyInjector(ABC):
    
    # * AI Engine
    @abstractmethod
    def ai_engine(self) -> 'AIEngine':
        """ Return an instance of AIEngine """
        raise NotImplementedError('ai_engine() must be defined')
    
    
    # * Video Capture
    @abstractmethod
    def video_capture(self, url: str) -> 'VideoCapture':
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
    def video_detector(self, video_capture: 'VideoCapture', ai_engine: 'AIEngine', delay: int = 5) -> 'VideoDetector':
        """ 
        Return an instance of VideoDetector 
        
        Parameters
        ----------
        video_capture : VideoCapture
            Video capture to analyze
        ai_engine : AIEngine
            AI framework to use in the video
        delay : int
            Delay to rerun AI alg
        """
        raise NotImplementedError('video_detector() must be defined')
    
    
    # * Tracked Video
    @abstractmethod
    def tracked_video(self, video_feed: 'VideoFeed') -> 'TrackedVideo':
        """ 
        Return an instance of VideoDetector 
        
        Parameters
        ----------
        video_feed : VideoFeed
            video feed to track
        """
        raise NotImplementedError('tracked_video() must be defined')
    
    
    # * WebSocket
    @abstractmethod
    def websocket(self) -> 'WebSocket':
        """ Return an instance of WebSocket """
        raise NotImplementedError('websocket() must be defined')