from abc import ABC, abstractmethod
from src.domain.dependencies.ai_engine import AIEngine
from src.domain.dependencies.video_capture import VideoCapture
from src.domain.components.detectors.object_detector import ObjectDetector


class TrackedVideoDependencies(ABC):
    
    # * AI Engine
    @abstractmethod
    def ai_engine(self) -> AIEngine:
        """ Return an instance of AIEngine """
        raise NotImplementedError('ai_engine() must be defined')
    
    
    # * Video Capture
    @abstractmethod
    def video_capture(self, id: str, url: str) -> VideoCapture:
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
    def object_detector(self, id: str, video_capture: VideoCapture, ai_engine: AIEngine, delay: int = 5) -> ObjectDetector:
        """ 
        Return an instance of ObjectDetector 
        
        Parameters
        ----------
        video_capture : VideoCapture
            Video capture to analyze
        ai_engine : AIEngine
            AI framework to use in the video
        delay : int
            Delay to rerun AI alg
        """
        raise NotImplementedError('object_detector() must be defined')