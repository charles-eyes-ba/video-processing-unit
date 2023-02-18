from src.common.environment import DEEPSTACK_URL, WEBSOCKET_URL
from src.models.video_feed import VideoFeed
from src.domain.dependencies.ai_engine import AIEngine
from src.integration.ai_engine.deepstack_engine import DeepStackEngine
from src.domain.dependencies.video_capture import VideoCapture
from src.integration.video_capture.opencv_video_capture import OpenCVVideoCapture
from src.domain.components.video_detector import VideoDetector
from src.domain.components.video_detector.video_detector_impl import VideoDetectorImpl
from src.domain.components.tracked_video import TrackedVideo
from src.domain.components.tracked_video.tracked_video_impl import TrackedVideoImpl
from src.domain.dependencies.websocket import WebSocket
from src.integration.websocket.socketio import WebSocketIO
from src.domain.components.tracked_video.dependencies import TrackedVideoDependencies
from src.domain.components.main_unit.dependencies import MainUnitDependencies


class DependencyInjector(TrackedVideoDependencies, MainUnitDependencies):
    
    def __init__(self):
        self.__ai_engine_shared = DeepStackEngine(DEEPSTACK_URL)
        self.__websocket = WebSocketIO(WEBSOCKET_URL)
        
    
    # * AI Engine
    def ai_engine(self) -> AIEngine:
        """ Return an instance of AIEngine """
        return self.__ai_engine_shared
    
    
    # * Video Capture
    def video_capture(self, id: str, url: str) -> VideoCapture:
        """ 
        Return an instance of VideoCapture 
        
        Parameters
        ----------
        url : str
            URL to retrive the video
        """
        return OpenCVVideoCapture(id, url)
    
    
    # * Video Detector
    def video_detector(self, id: str, video_capture: VideoCapture, ai_engine: AIEngine, delay: int = 5) -> VideoDetector:
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
        return VideoDetectorImpl(id, video_capture, ai_engine, delay)
    
    
    # * Tracked Video
    def tracked_video(self, video_feed: VideoFeed) -> TrackedVideo:
        """ 
        Return an instance of VideoDetector 
        
        Parameters
        ----------
        video_feed : VideoFeed
            video feed to track
        """
        return TrackedVideoImpl(self, video_feed)
    
    
    # * WebSocket
    def websocket(self) -> WebSocket:
        """ Return an instance of WebSocket """
        return self.__websocket