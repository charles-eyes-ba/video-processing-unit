from .interface import DependencyInjector
from src.common.environment import DEEPSTACK_URL
from src.domain.dependencies.ai_engine import AIEngine
from src.integration.ai_engine.deepstack_engine import DeepStackEngine
from src.domain.dependencies.video_capture import VideoCapture
from src.integration.video_capture.opencv_video_capture import OpenCVVideoCapture
from src.domain.components.video_detector import VideoDetector
from src.domain.components.video_detector.video_detector_impl import VideoDetectorImpl
from src.domain.components.tracked_video import TrackedVideo
from src.domain.components.tracked_video.tracked_video_impl import TrackedVideoImpl


class DependencyInjectorImpl(DependencyInjector):
    
    def __init__(self):
        self.__ai_engine_shared = DeepStackEngine(DEEPSTACK_URL)
        
    
    # * AI Engine
    def ai_engine(self) -> AIEngine:
        return self.__ai_engine_shared
    
    
    # * Video Capture
    def video_capture(self, url: str) -> VideoCapture:
        return OpenCVVideoCapture(url)
    
    
    # * Video Detector
    def video_detector(self, video_capture: VideoCapture, ai_engine: AIEngine, delay: int = 5) -> VideoDetector:
        return VideoDetectorImpl(self, video_capture, ai_engine, delay)
    
    
    # * Tracked Video
    def tracked_video(self, id: str, url: str) -> TrackedVideo:
        return TrackedVideoImpl(self, id, url)
        