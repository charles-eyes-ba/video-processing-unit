from abc import ABC, abstractmethod
from src.models.video_feed import VideoFeed
from src.domain.components.tracked_video import TrackedVideo
from src.domain.dependencies.websocket import WebSocket


class MainUnitDependencies(ABC):
    
    
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