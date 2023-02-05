from src.common.environment import DEEPSTACK_URL

from src.domain.dependencies.ai_engine import AIEngine
from src.integration.ai_engine.deepstack_engine import DeepStackEngine

from src.domain.dependencies.video_capture import VideoCapture
from src.integration.video_capture.opencv_video_capture import OpenCVVideoCapture

from src.domain.components.video_detector import VideoDetector
from src.domain.components.video_detector.video_detector_impl import VideoDetectorImpl

class Factory:
    
    @staticmethod
    def ai_engine() -> AIEngine:
        return DeepStackEngine(DEEPSTACK_URL)
    
    
    @staticmethod
    def video_capture(url: str) -> VideoCapture:
        return OpenCVVideoCapture(url)
    
    
    @staticmethod
    def video_detector(id: str, video_capture: VideoCapture, ai_engine: AIEngine) -> VideoDetector:
        return VideoDetectorImpl(id, video_capture, ai_engine)